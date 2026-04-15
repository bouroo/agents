---
name: context-management
description: Use when working with goroutines, HTTP requests, or any concurrent operations.
---

# Context Management

## Propagation
Always pass `context.Context` as first parameter to functions that:
- Make network calls
- Perform database operations
- Spawn goroutines

## Timeouts & Cancellation
```go
ctx, cancel := context.WithTimeout(parent, 5*time.Second)
defer cancel()
```
- Derive from `context.Background()` for top-level requests
- Derive from incoming context for downstream calls

## Goroutine Lifecycle
Every goroutine must have a termination guarantee:
- Receives on a channel
- Context cancellation signal
- WaitGroup completion

```go
func WorkerPool(ctx context.Context, jobs <-chan Work) {
    var wg sync.WaitGroup
    for i := 0; i < cap(jobs); i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for job := range jobs {
                select {
                case <-ctx.Done():
                    return
                default:
                    process(job)
                }
            }
        }()
    }
    wg.Wait()
}
```

## Anti-patterns
- Don't store context in a struct
- Don't pass `nil` context
- Don't leak goroutines — always ensure termination
