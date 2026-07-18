# Concurrency - Depth

Loaded on demand from [go-essential](../SKILL.md) §6. The core principles live there; this file
covers channels/select, sync primitives, pipelines, and audit patterns.

## Channels and Select

```go
// Directed channels document intent and let the compiler enforce it
func worker(ctx context.Context, jobs <-chan Job, results chan<- Result) {
    for {
        select {
        case <-ctx.Done():
            return
        case j, ok := <-jobs:
            if !ok { return }      // channel closed by sender
            results <- process(j)
        }
    }
}
```

- **Sender owns and closes.** A receiver closing the channel panics if the sender writes after
  close.
- **Default to unbuffered.** Buffering masks backpressure; use only with measured justification
  (e.g., smoothing a bursty producer).
- **Always include `ctx.Done()` in `select`** - without it the goroutine leaks after caller
  cancellation.
- **Avoid `time.After` in hot loops** - each call allocates a fresh timer:

  ```go
  // ✗ Allocates per iteration
  for {
      select {
      case <-ctx.Done(): return
      case <-time.After(5 * time.Second): doWork()
      }
  }

  // ✓ Reuse a timer
  t := time.NewTimer(5 * time.Second); defer t.Stop()
  for {
      if !t.Stop() { select { case <-t.C: default: } }
      t.Reset(5 * time.Second)
      select {
      case <-ctx.Done(): return
      case <-t.C: doWork()
      }
  }
  ```

- **Send copies, not pointers.** A pointer on a channel is shared memory - defeats the channel's
  purpose.

## Sync Primitives

| Primitive              | Use case                                  | Key notes                                                                  |
| ---------------------- | ----------------------------------------- | -------------------------------------------------------------------------- |
| `sync.Mutex`           | Protect shared state                      | Keep critical sections short; never hold across I/O                        |
| `sync.RWMutex`         | Many readers, few writers                 | Never upgrade `RLock` to `Lock` (deadlock)                                 |
| `sync/atomic`          | Simple counters, flags                    | Prefer typed atomics (Go 1.19+): `atomic.Int64`, `atomic.Bool`             |
| `sync.Map`             | Concurrent map, read-heavy                | No explicit locking; use `RWMutex`+map when writes dominate                |
| `sync.Pool`            | Reuse temporary objects                   | Always `Reset()` before `Put()`; reduces GC pressure                       |
| `sync.Once`            | One-time init                             | Go 1.21+: `OnceFunc`, `OnceValue`, `OnceValues`                            |
| `sync.WaitGroup`       | Fire-and-forget goroutine groups          | Go 1.25+: prefer `wg.Go(func(){ ... })`. `Add` before `go`, not inside     |
| `x/sync/singleflight`  | Deduplicate concurrent identical calls    | Cache-stampede prevention                                                  |
| `x/sync/errgroup`      | Goroutine group with error/cancel         | `SetLimit(n)` replaces hand-rolled worker pools                            |

```go
// errgroup with bounded concurrency and sibling cancellation
g, ctx := errgroup.WithContext(ctx)
g.SetLimit(8)
for _, url := range urls {
    url := url
    g.Go(func() error {
        return fetch(ctx, url)
    })
}
if err := g.Wait(); err != nil { return err }
```

`wg.Add` must be called **before** `go` - calling it inside the goroutine lets `Wait` return
early.

## Pipelines and Worker Pools

```go
// Generator → stage → stage → sink, each stage a goroutine, ctx propagates
func gen(ctx context.Context, nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for _, n := range nums {
            select {
            case <-ctx.Done(): return
            case out <- n:
            }
        }
    }()
    return out
}

func sq(ctx context.Context, in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for n := range in {
            select {
            case <-ctx.Done(): return
            case out <- n * n:
            }
        }
    }()
    return out
}

// Fan-out/fan-in: spawn N sq workers reading from `in`, merge their outputs.
```

Go 1.23+ offers `iter.Seq[T]` iterators and range-over-func, which often replace hand-rolled
channel pipelines for non-concurrent transformations. For concurrent fan-out, `errgroup` with
`SetLimit` is usually clearer than channels.

## Goroutine Leaks

A leaked goroutine runs forever because nothing can tell it to stop. Symptoms: steady growth in
`runtime.NumGoroutine()`, slow memory growth, eventual OOM or fd exhaustion.

Detection:

- Tests: `go.uber.org/goleak.VerifyTestMain(m)` in `TestMain`.
- Live: `/debug/pprof/goroutine?debug=2` stack dump.
- Race checks: `go test -race ./...`.
- Go 1.26+ experimental `GOEXPERIMENT=goroutineleakprofile` - do not rely on as default.

Fix pattern: every `go` statement must have a corresponding stop mechanism (ctx, done channel,
WaitGroup) and a clear owner.

## Common Mistakes

| Mistake                                        | Fix                                                                |
| ---------------------------------------------- | ------------------------------------------------------------------ |
| Fire-and-forget goroutine                      | Provide stop mechanism (context, done channel)                     |
| Closing channel from receiver                  | Only the sender closes                                             |
| `time.After` in hot loop                       | Reuse `time.NewTimer` + `Reset`                                    |
| Missing `ctx.Done()` in `select`               | Always select on context                                           |
| Unbounded goroutine spawning                   | `errgroup.SetLimit(n)` or semaphore                                |
| Sharing pointer via channel                    | Send copies or immutable values                                    |
| `wg.Add` inside goroutine                      | Call `Add` before `go` - `Wait` may return early                   |
| Forgetting `-race` in CI                       | Always `go test -race ./...`                                       |
| Mutex held across I/O                          | Keep critical sections short                                       |
| Concurrent map read/write                      | Hard crash - `sync.Map` or `RWMutex` + map                         |
| RLock then upgrade to Lock                     | Deadlock - acquire Lock from the start if mutation is needed       |
| `sync.Pool` item not Reset before Put          | Next user sees stale state                                         |

## Audit Sub-Agents (Parallel)

When auditing concurrency across a codebase, split into 5 parallel sub-agents:

1. **Goroutine spawns** - every `go func` / `go method` has a shutdown mechanism and clear owner.
2. **Shared state** - mutable globals and shared fields without synchronization.
3. **Channel usage** - ownership, direction, closure, buffer sizes.
4. **Hot patterns** - `time.After` in loops, missing `ctx.Done()` in select, unbounded spawning.
5. **Primitives** - mutex usage, `sync.Map`, atomics, documented thread-safety.
