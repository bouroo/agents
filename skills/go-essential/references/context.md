# Context - Depth

Loaded on demand from [go-essential](../SKILL.md) §7. The short rules live there; this file is
the why, the worked code, and the failure modes.

`context.Context` is the "session" of a request - it ties together every operation in the same
unit of work and propagates cancellation, deadlines, and request-scoped values across API
boundaries.

## The Core Rule: Propagate the Chain

The same context MUST propagate through the entire call chain: HTTP handler → service → DB →
external APIs. Breaking the chain defeats cancellation, trace propagation, and deadline
enforcement.

```go
// ✗ Bad - creates a new context, breaking the chain
func (s *OrderService) Create(ctx context.Context, order Order) error {
    return s.db.ExecContext(context.Background(), "INSERT INTO orders ...", order.ID)
}

// ✓ Good - propagates the caller's context
func (s *OrderService) Create(ctx context.Context, order Order) error {
    return s.db.ExecContext(ctx, "INSERT INTO orders ...", order.ID)
}
```

## First Parameter, Named `ctx`

```go
func DoThing(ctx context.Context, x int) error { ... }
```

- Always first.
- Always named `ctx` (not `context` - shadows the package; not `c` - too short).
- Never stored in a struct. Pass explicitly through function parameters.

## Creating Contexts

| Situation                                  | Use                                 |
| ------------------------------------------ | ----------------------------------- |
| Entry point (main, init, test)             | `context.Background()`              |
| Caller doesn't provide one yet             | `context.TODO()`                    |
| HTTP handler                               | `r.Context()`                       |
| Need manual cancellation                   | `context.WithCancel(parent)`        |
| Need a timeout                             | `context.WithTimeout(parent, d)`    |
| Need an absolute deadline                  | `context.WithDeadline(parent, t)`   |
| Background work outliving the parent       | `context.WithoutCancel(parent)` (Go 1.21+) |

**`Background()` vs `TODO()`:** both return a non-cancelable context. `Background()` is for the
top of the call chain (main, init, tests). `TODO()` is a placeholder - "I know I need a context
here but I haven't plumbed one yet." Linters flag `TODO()` left in production code.

## Cancellation, Timeouts, Deadlines

```go
ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
defer cancel()

resp, err := httpClient.Do(req.WithContext(ctx))
if err != nil {
    return fmt.Errorf("calling upstream: %w", err)
}
defer resp.Body.Close()
```

**Call `cancel()` on every path.** Use `defer cancel()` immediately after creating the context.
If you forget, the context (and any resources it tracks) leak until the parent times out.

### Listening for Cancellation

```go
select {
case <-ctx.Done():
    return ctx.Err()
case result := <-work:
    return result
}
```

**Long loops** check `ctx.Err()` periodically:

```go
for _, item := range items {
    if err := ctx.Err(); err != nil {
        return err
    }
    process(item)
}
```

### `AfterFunc` (Go 1.21+)

Register a callback that fires when the context is cancelled - useful for cleanup or signaling
without a goroutine parked on `select`.

```go
stop := context.AfterFunc(ctx, func() {
    // fires when ctx is cancelled
    cleanup()
})
defer stop() // unregister if the work completes normally
```

## Context Values

Context values carry **request-scoped metadata only** - request ID, user ID, trace context,
tenant ID. NEVER function parameters (those go in the function signature).

**Unexported key types prevent collisions:**

```go
type ctxKey int
const (
    keyRequestID ctxKey = iota
    keyUserID
)

func WithRequestID(ctx context.Context, id string) context.Context {
    return context.WithValue(ctx, keyRequestID, id)
}

func RequestID(ctx context.Context) string {
    if v, ok := ctx.Value(keyRequestID).(string); ok {
        return v
    }
    return ""
}
```

**Accessor functions** wrap the `WithValue`/`Value` pair so callers never see the key. The key
type is unexported; no other package can read or overwrite the value.

## WithoutCancel

`context.WithoutCancel(parent)` (Go 1.21+) returns a copy of the parent that does not cancel
when the parent does. Use for background work spawned by a request handler that must complete
even if the client disconnects - audit logs, cleanup, "fire-and-track" notifications.

```go
func (s *OrderService) Create(ctx context.Context, o Order) error {
    if err := s.repo.Insert(ctx, o); err != nil {
        return err
    }
    // Audit log must persist even if the client disconnects
    go s.audit.Log(context.WithoutCancel(ctx), "order_created", o.ID)
    return nil
}
```

The audit goroutine still needs its own bounded lifecycle - pair `WithoutCancel` with a service-
level shutdown context so the process doesn't exit mid-write.

## HTTP Servers and Clients

```go
// Server - the handler gets a request-scoped context
func (h *Handler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context() // cancelled when the client disconnects
    // ... pass ctx through to services
}

// Client - attach the context to the request
req := req.WithContext(ctx)
resp, err := httpClient.Do(req)
```

## Databases

Always use the `*Context` variants - `QueryContext`, `ExecContext`, `BeginTx` with a context.
The non-context variants (`Query`, `Exec`) block indefinitely on a slow query.

```go
// ✗ Bad
rows, err := db.Query("SELECT ...")

// ✓ Good
rows, err := db.QueryContext(ctx, "SELECT ...")
```

## Cross-Service Tracing

Context carries `trace_id` and `span_id` across service boundaries. OpenTelemetry injects and
extracts trace context via HTTP headers, gRPC metadata, or message-queue properties. Always
propagating the context keeps traces continuous; breaking the chain creates orphan spans.

See [Observability](./observability.md) for the tracing integration details.

## Common Mistakes

```go
// ✗ Bad - storing context in a struct
type Service struct {
    ctx context.Context // leaks; the struct outlives any single request
}

// ✓ Good - pass ctx as a parameter to each method
func (s *Service) Do(ctx context.Context, x int) error { ... }
```

```go
// ✗ Bad - nil context panics in some stdlib functions
func Do(ctx context.Context) {
    if ctx == nil {
        ctx = context.Background() // NEVER do this; pass a real context
    }
}

// ✓ Good - use context.TODO() at the caller, fix it later
Do(context.TODO())
```

```go
// ✗ Bad - string key collides with other packages
ctx = context.WithValue(ctx, "user_id", 42)

// ✓ Good - unexported key type
type ctxKey int
const keyUserID ctxKey = 1
ctx = context.WithValue(ctx, keyUserID, 42)
```

## Enforce with Linters

`govet` and `staticcheck` catch many context pitfalls:

- `lostcancel` - `WithCancel`/`WithTimeout`/`WithDeadline` without a `cancel()` call on every
  path.
- `context-as-argument` - context not first parameter.
- `context-keys-type` - string or known-type key used for `context.WithValue`.
