# Observability - Depth

Loaded on demand from [go-essential](../SKILL.md) §11. The short rules live there; this file is
the why, the worked code, and the inspection patterns.

A feature is not production-ready until it is observable. The five signals - logs, metrics,
traces, profiles, RUM - answer different questions and compose into full visibility.

## The Five Signals

| Signal     | Question                    | Default tool           | Use for                                   |
| ---------- | --------------------------- | ---------------------- | ----------------------------------------- |
| **Logs**   | What happened?              | `log/slog`             | Discrete events, errors, audit trails     |
| **Metrics**| How much / how fast?        | Prometheus client      | Aggregated measurements, alerting, SLOs   |
| **Traces** | Where did time go?         | OpenTelemetry          | Request flow across services, latency     |
| **Profiles** | Why slow / memory-hungry? | `pprof`, Pyroscope     | CPU hotspots, memory leaks, contention    |
| **RUM**    | How do users experience it? | PostHog, Segment      | Product analytics, funnels, session replay|

## Structured Logging with slog

`slog` (Go 1.21+) is the stdlib structured logger. Production services emit JSON, not freeform
strings.

```go
// Setup at process start
logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
    Level: slog.LevelInfo,
}))
slog.SetDefault(logger)

// Context variants carry trace_id/span_id automatically when bridged
slog.InfoContext(ctx, "order created", "order_id", orderID, "amount", total)
```

**Log levels:**

- **Debug** - development only; never enabled in production by default.
- **Info** - normal operations; the "audit trail" of successful unit-of-work completion.
- **Warn** - degraded but functional; needs attention but not urgent.
- **Error** - failures requiring attention.

**Hot-path logging:** if a log line is inside a tight loop or hot request path, use
`slog.LogAttrs(ctx, slog.LevelDebug, msg, attrs...)` - at disabled levels it skips the
key-value boxing that `slog.Info(...)` would allocate.

### Go 1.26+: slog multi-handler

For simple fan-out (e.g., stdout + an audit sink), prefer stdlib `slog.NewMultiHandler` before
adding a third-party handler-composition dependency.

```go
logger := slog.New(slog.NewMultiHandler(
    slog.NewJSONHandler(os.Stdout, nil),
    auditHandler,
))
```

### Migrating Legacy Loggers

If the project still uses `zap`, `logrus`, or `zerolog`:

1. Add `slog` as the new default via `slog.SetDefault()`.
2. Bridge handlers route slog output through the legacy logger during migration - install a
   bridging handler that delegates to the old sink.
3. Convert callsites incrementally: `zap.L().Info(...)` → `slog.Info(...)`.
4. Once all callsites convert, drop the bridge and the legacy dependency.

## Metrics: Prometheus

### Histogram vs Summary

**Always prefer Histogram for latency.** Summaries cannot aggregate across instances, so a
service with 10 replicas and a Summary per replica cannot compute a fleet-wide P99. Histograms
support `histogram_quantile()` in PromQL and aggregate cleanly.

```go
var httpDuration = prometheus.NewHistogramVec(
    prometheus.HistogramOpts{
        Name:    "http_request_duration_seconds",
        Buckets: prometheus.DefBuckets, // tune to your latency profile
    },
    []string{"method", "route"},
)
```

### Cardinality Discipline

A label series is one time series. A metric with `user_id` as a label on a high-traffic endpoint
creates one time series per user - millions of users means millions of time series, and
Prometheus OOMs.

```go
// ✗ Bad - unbounded cardinality
httpRequests.WithLabelValues(r.Method, r.URL.Path, userID).Inc()

// ✓ Good - bounded cardinality (route pattern, not full URL)
httpRequests.WithLabelValues(r.Method, routePattern).Inc()
```

**Rule:** label values must come from a small, closed set. Method, route pattern, status class
(`2xx`, `4xx`, `5xx`), error code - yes. User ID, full URL, request ID, session ID - no.

### Track Percentiles

P50 (median), P90, P99, P99.9 - the tail matters. A P50 of 50ms with a P99 of 5s is a broken
service for 1% of users. Wire `histogram_quantile(0.99, rate(...[5m]))` into dashboards and
alert rules.

## Distributed Tracing: OpenTelemetry

Configure the TracerProvider early at process start, then add spans everywhere.

```go
// Setup once at startup
tp, err := otel.TracerProviderFromConfig(/* ... */)
if err != nil { log.Fatal(err) }
otel.SetTracerProvider(tp)

// In the handler
func (s *OrderService) Create(ctx context.Context, o Order) error {
    ctx, span := tp.Tracer("order").Start(ctx, "OrderService.Create")
    defer span.End()

    if err := s.repo.Insert(ctx, o); err != nil {
        span.RecordError(err)
        span.SetStatus(codes.Error, err.Error())
        return err
    }
    return nil
}
```

**Span every meaningful operation:** service methods, DB queries, external API calls, message
queue sends/receives. Record errors with `span.RecordError()` and set status to `Error`.

## Context Propagation

Context carries `trace_id`, `span_id`, and deadlines across service boundaries. Always use the
`*Context` variant of every API:

```go
// ✗ Bad - breaks trace propagation, ignores deadline
rows, err := db.Query("SELECT ...")

// ✓ Good - context flows through; trace and deadline preserved
rows, err := db.QueryContext(ctx, "SELECT ...")
```

HTTP clients: `http.NewRequestWithContext(ctx, ...)`; gRPC: the client propagates the context
automatically; message queues: serialize trace headers into the message metadata.

## Correlating Signals

### Logs + Traces: otelslog bridge

```go
import "go.opentelemetry.io/contrib/bridges/otelslog"

logger := otelslog.NewHandler("my-service")
slog.SetDefault(slog.New(logger))

// Every call with context now includes trace_id and span_id
slog.InfoContext(ctx, "order created", "order_id", orderID)
// Output: {"trace_id":"abc123","span_id":"def456","msg":"order created",...}
```

### Metrics + Traces: Exemplars

Attach a `trace_id` exemplar to histogram observations so a P99 spike links directly to the
offending trace.

```go
obs := httpDuration.WithLabelValues("POST", "/orders")
if eo, ok := obs.(prometheus.ExemplarObserver); ok {
    eo.ObserveWithExemplar(duration, prometheus.Labels{"trace_id": traceID})
} else {
    obs.Observe(duration)
}
```

## Profiling

Toggle pprof on/off via env vars without redeploying. Protect pprof endpoints behind auth in
production - they expose goroutine stacks and memory that can leak secrets.

```go
import _ "net/http/pprof"

// Mount on an internal port or behind auth
go func() {
    log.Println(http.ListenAndServe("localhost:6060", nil))
}()
```

For continuous profiling in production, run Pyroscope or a similar always-on profiler with a
sample rate that keeps overhead under ~1% CPU.

## Alerting

Alert on the four golden signals with explicit `for:` durations to avoid flapping:

- **Latency** - P99 above SLO threshold for 5m.
- **Traffic** - unusual spike or drop sustained for 10m.
- **Errors** - error rate above 1% for 5m.
- **Saturation** - CPU > 90%, memory near `GOMEMLIMIT`, goroutine count climbing.

**Common mistakes:**

- Using `irate()` instead of `rate()` - `irate` only looks at the last two samples and is noisy.
- Missing `for:` duration - every transient blip pages someone.
- Alerting on absolute counts instead of rates - traffic growth makes absolute-count alerts
  irrelevant.

## Definition of Done

A feature is not production-ready until:

- [ ] **Metrics declared** - counters for operations/errors, histograms for latencies, gauges for
      saturation. PromQL queries and alert rules live as comments above the metric declaration.
- [ ] **Logging is proper** - structured with `slog`, context variants used, no PII, errors
      logged XOR returned (never both).
- [ ] **Spans created** - every service method, DB query, external call has a span; errors
      recorded with `span.RecordError()`.
- [ ] **Dashboards and alerts wired** - the PromQL from metric comments is in Grafana and in
      Prometheus alerting rules.
- [ ] **RUM events tracked** - key business events tracked server-side; identity key is
      `user_id`, not email; consent checked before tracking.

## Common Mistakes

```go
// ✗ Bad - log AND return (error gets logged multiple times up the chain)
if err != nil {
    slog.Error("query failed", "error", err)
    return fmt.Errorf("query: %w", err)
}

// ✓ Good - return with context, log once at the top of the call chain
if err != nil {
    return fmt.Errorf("querying users: %w", err)
}
```

```go
// ✗ Bad - high-cardinality label
httpRequests.WithLabelValues(r.Method, r.URL.Path, userID).Inc()

// ✓ Good - bounded labels only
httpRequests.WithLabelValues(r.Method, routePattern).Inc()
```

```go
// ✗ Bad - Summary for latency (cannot aggregate across instances)
prometheus.NewSummary(prometheus.SummaryOpts{
    Name:       "http_request_duration_seconds",
    Objectives: map[float64]float64{0.99: 0.001},
})

// ✓ Good - Histogram (aggregatable, supports histogram_quantile)
prometheus.NewHistogram(prometheus.HistogramOpts{
    Name:    "http_request_duration_seconds",
    Buckets: prometheus.DefBuckets,
})
```
