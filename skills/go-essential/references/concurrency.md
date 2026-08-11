# Go Concurrency & Context in Detail

Reference for `go-essential` §4: channel ownership, channel-vs-mutex-vs-atomic, sync primitives, pipelines, and the pre-spawn checklist.

## 1. Context Propagation

`context.Context` is the "session" of a request  --  propagate the same `ctx` end-to-end: HTTP handler → service → DB → outbound HTTP/gRPC. Cancellations then halt every downstream automatically.

Core rules: `ctx` is always the first parameter, named `ctx context.Context`. Never store it in a struct. Never pass `nil`; use `context.TODO()`. `context.Background()` only at the top boundary (`main`, `init`, tests). `cancel()` MUST run on every control-flow path for `WithCancel` / `WithTimeout` / `WithDeadline`, or timer/cancel state leaks.

```go
// Bad  --  breaks the chain mid-request
func (s *OrderService) Create(ctx context.Context, o Order) error {
    return s.db.ExecContext(context.Background(), "INSERT ...", o.ID)
}

// Good  --  propagates the caller's ctx
func (s *OrderService) Create(ctx context.Context, o Order) error {
    return s.db.ExecContext(ctx, "INSERT ...", o.ID)
}

// Idiom for scoped work  --  defer cancel immediately
func fetch(ctx context.Context) error {
    ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
    defer cancel()
    return doWork(ctx)
}
```

### `context.WithoutCancel` (Go 1.21+) for background work

Background work that must outlive the request (audit logs, async dispatch) needs the request's *values* but not its *cancellation*. `context.WithoutCancel` keeps values like `trace_id` while detaching cancellation  --  better than `context.Background()` (loses values) or the parent ctx (kills the audit when the handler returns):

```go
auditCtx := context.WithoutCancel(ctx)
go h.auditService.LogOrderCreated(auditCtx, order)
```

### Context values

Values carry request-scoped metadata only  --  trace ID, user ID, request ID. Never function parameters. Keys MUST be unexported types to prevent cross-package collisions:

```go
type traceKey struct{}
func WithTraceID(ctx context.Context, id string) context.Context {
    return context.WithValue(ctx, traceKey{}, id)
}
```

## 2. Channel vs Mutex vs Atomic

| Scenario | Use | Why |
| --- | --- | --- |
| Passing data between goroutines | Channel | Communicates ownership transfer |
| Coordinating goroutine lifecycle | Channel + context | Clean shutdown via `select` |
| Protecting shared struct fields | `sync.Mutex` / `sync.RWMutex` | Simple critical sections |
| Simple counters, flags | `sync/atomic` | Lock-free, lower overhead |
| Many readers, few writers on a map | `sync.Map` | Optimized for read-heavy (else `RWMutex`+map) |
| Caching expensive computations | `sync.Once` / `x/sync/singleflight` | Execute once or deduplicate stampedes |

Concurrent read/write on a plain `map` is a **hard crash** (`fatal error: concurrent map read and map write`), not a data race. Protect with a mutex, use `sync.Map`, or switch to a concurrent-safe structure.

## 3. Channel Ownership & Direction

- Only the **sender** closes. Closing from the receiver panics if the sender writes after close; closing twice panics unconditionally.
- Always specify direction (`chan<-`, `<-chan`)  --  the compiler prevents misuse at build time.
- Default to **unbuffered**. Larger buffers mask backpressure; use them only with measured justification (signal channels of size 1, or measured burst absorption).
- Send **copies**, not pointers. Pointers through a channel create invisible shared memory, defeating the channel's purpose.
- Include `ctx.Done()` in every `select` that could block, or the goroutine leaks after caller cancellation.

```go
func generate(ctx context.Context) <-chan int { // receiver-only return
    out := make(chan int)
    go func() {
        defer close(out) // sender owns the close
        for i := 0; ; i++ {
            select {
            case out <- i:
            case <-ctx.Done():
                return
            }
        }
    }()
    return out
}
```

## 4. Sync Primitives Quick Reference

| Primitive | Use case | Key notes |
| --- | --- | --- |
| `sync.Mutex` | Protect shared state | Short critical sections; never across I/O |
| `sync.RWMutex` | Many readers, few writers | Never upgrade `RLock` → `Lock` (deadlock); release then re-acquire |
| `sync/atomic` | Single-value state (counter, flag, pointer) -- prefer over a mutex | Typed atomics (Go 1.19+): `atomic.Int64`, `atomic.Bool`, `atomic.Pointer[T]`; `atomic.Value` for an arbitrary snapshot type. A `sync.Mutex` around one value is a wasted lock |
| `sync.Map` | Concurrent map, read-heavy | Write-once/read-many or disjoint key sets; use `RWMutex`+map otherwise |
| `sync.Pool` | Reuse temporary objects | `Reset()` before `Put()`; entries may be reclaimed at any GC |
| `sync.Once` | One-time initialization | Go 1.21+: `OnceFunc`, `OnceValue`, `OnceValues` |
| `sync.WaitGroup` | Wait for simple goroutines | Go 1.25+: `wg.Go(func(){...})`; never `Add` inside the goroutine |
| `x/sync/singleflight` | Deduplicate concurrent calls | Prevents cache stampedes on the same key |
| `x/sync/errgroup` | Goroutine group + errors | `SetLimit(n)` replaces hand-rolled worker pools |

A panic in any goroutine crashes the whole process. Recover at goroutine boundaries in production code and log with a stack trace.

### Atomic over mutex for single-value state

A `sync.Mutex` around one counter or flag is a wasted lock -- the typed atomic is cheaper and cannot deadlock. Reach for a mutex only when the critical section spans multiple fields or guards an invariant.

```go
// Avoid: a lock around a single counter
type Counter struct {
    mu    sync.Mutex
    count int
}
func (c *Counter) Add()      { c.mu.Lock(); c.count++; c.mu.Unlock() }
func (c *Counter) Get() int  { c.mu.Lock(); defer c.mu.Unlock(); return c.count }

// Prefer: a typed atomic (Go 1.19+)
type Counter struct{ count atomic.Int64 }
func (c *Counter) Add()     { c.count.Add(1) }
func (c *Counter) Get() int { return int(c.count.Load()) }
```

Use `atomic.Pointer[T]` for a single pointer swapped as a unit, and `atomic.Value` only for an arbitrary snapshot type the typed atomics do not cover. `sync.Once` / `OnceValue` (§4) is the atomic answer for once-only initialization -- never a guarded `init bool`.

## 5. WaitGroup vs errgroup

| Need | Use |
| --- | --- |
| Wait, errors not needed | `sync.WaitGroup` (or `wg.Go` on Go 1.25+) |
| Wait + first error wins | `errgroup.Group` |
| Wait + cancel siblings on first error | `errgroup.WithContext` |
| Wait + bounded concurrency | `errgroup.SetLimit(n)` |

```go
g, ctx := errgroup.WithContext(parentCtx)
g.SetLimit(10) // bounded worker pool  --  no hand-rolled semaphore
for _, task := range tasks {
    task := task
    g.Go(func() error { return process(ctx, task) })
}
return g.Wait()
```

## 6. Goroutine Pre-Spawn Checklist

Before every `go func(){...}` or `go method()`, answer five questions:

- **How will it exit?**  --  context cancellation, done channel, or explicit signal.
- **Can I signal it to stop?**  --  pass `context.Context` or a done channel it selects on.
- **Can I wait for it?**  --  `sync.WaitGroup`, `wg.Go`, or `errgroup`.
- **Who owns the channels?**  --  the creator/sender owns and closes.
- **Should this be synchronous instead?**  --  don't add concurrency without a measured need. Goroutines are cheap but not free; every one is a lifecycle you must manage.

If any answer is "I don't know", write the synchronous version first; add concurrency only after it is correct and profiled.

## 7. Pipelines & Worker Pools

A pipeline chains stages  --  each receives from an upstream channel, processes, and sends to a downstream channel. Three rules:

- Producer closes its output channel (`defer close(out)`); receivers terminate on `ok == false`.
- Every `select` inside a stage includes `ctx.Done()`.
- Bound concurrency with `errgroup.SetLimit(n)`; do not hand-roll semaphore channels.

Bounded fan-out:

```go
func processAll(ctx context.Context, items []Item) error {
    g, ctx := errgroup.WithContext(ctx)
    g.SetLimit(runtime.NumCPU())
    for _, it := range items {
        it := it
        g.Go(func() error { return transform(ctx, it) })
    }
    return g.Wait()
}
```

Go 1.23+ `range`-over-func iterators and `samber/ro` provide pipeline composition (`Pipe` / `FromSlice` / `Map` / `Filter` / `Pull`). Prefer `errgroup.SetLimit` over hand-rolled worker pools whenever errors must propagate.

## 8. Goroutine Leak Detection

Catch leaks in tests with `go.uber.org/goleak`:

```go
// Per-test
func TestSomething(t *testing.T) {
    defer goleak.VerifyNone(t)
    // ...
}

// Whole package
func TestMain(m *testing.M) { goleak.VerifyTestMain(m) }
```

Go 1.26 ships an experimental `goroutineleakprofile` gated by `GOEXPERIMENT=goroutineleakprofile`  --  useful for production diagnostics but **not** a stable default. Treat goleak + `go test -race ./...` as standard, plus `runtime.NumGoroutine()` and `/debug/pprof/goroutine?debug=2` for ad-hoc inspection.

## 9. Common Mistakes

| Mistake | Fix |
| --- | --- |
| Fire-and-forget goroutine | Provide a stop mechanism (context or done channel) and a way to wait |
| Closing channel from receiver | Only the sender closes |
| `time.After` in a hot loop | Reuse `time.NewTimer` + `Reset` (Go 1.23+ makes this safe) |
| Missing `ctx.Done()` in `select` | Always select on context to allow cancellation |
| Unbounded goroutine spawning | Use `errgroup.SetLimit(n)` or a semaphore |
| Sharing pointer via channel | Send copies or immutable values |
| `wg.Add` inside the goroutine | Call `Add` before `go`; `Wait` may return early otherwise |
| Forgetting `-race` in CI | Always run `go test -race ./...` |
| Mutex held across I/O | Keep critical sections short; never across network or channel ops |
| Mutex guarding one counter/flag | Drop the lock; use a typed atomic (`atomic.Int64` / `Bool` / `Pointer[T]`) |

## 10. Checklist

- [ ] `ctx` is the first parameter, propagated end-to-end (handler → service → DB → outbound).
- [ ] `cancel()` is deferred immediately on `WithCancel` / `WithTimeout` / `WithDeadline`.
- [ ] `context.WithoutCancel` is used for background work that must outlive the request.
- [ ] Context value keys are unexported types; values are request-scoped metadata only.
- [ ] Every goroutine has a documented exit (context or done channel).
- [ ] Every goroutine can be waited on (`WaitGroup`, `wg.Go`, or `errgroup`).
- [ ] Channels are directional (`chan<-` / `<-chan`) and sender-owned.
- [ ] `errgroup.SetLimit` bounds parallel work; no hand-rolled worker pools.
- [ ] Each guarded value that stands alone (one counter, flag, or pointer) is a typed atomic, not a mutex.
- [ ] `select` always includes `ctx.Done()` when blocking on a channel.
- [ ] `goleak.VerifyNone(t)` (or `TestMain`) runs in every package's tests.
- [ ] CI runs `go test -race ./...` on every PR.

