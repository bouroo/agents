# Go Performance & Memory Optimization

Reference for `go-essential` §5: escape analysis, preallocation, `sync.Pool`, interface boxing, and the pprof workflow.

## 0. Methodology First

Intuition about bottlenecks is wrong ~80% of the time. **Profile before optimizing.**

1. **Rule out external bottlenecks.** Use `fgprof` (on-CPU + off-CPU), the goroutine profile, or distributed tracing. If 90% of latency is a DB or upstream call, allocation tuning will not help. Fix the upstream.
2. **Define the metric.** Latency, throughput, memory, or CPU   without a target, optimization is random.
3. **Iterative cycle:** baseline benchmark → diagnose (pprof) → ONE change with explanatory comment → re-measure with `benchstat`. Commit the `benchstat` output in the commit body.
4. **Document optimizations.** Add a code comment explaining *why* a pattern is faster, with benchmark numbers when available. Future readers need the context to avoid reverting an "unnecessary" optimization.

```bash
go test -bench=BenchmarkMyFunc -benchmem -count=6 ./pkg/... | tee /tmp/report-1.txt
# ...apply ONE optimization...
go test -bench=BenchmarkMyFunc -benchmem -count=6 ./pkg/... | tee /tmp/report-2.txt
benchstat /tmp/report-1.txt /tmp/report-2.txt
```

## 1. Stack vs Heap (Escape Analysis)

Go decides allocation at compile time via escape analysis.

- **Stack allocation** is essentially free   no GC cost. Function-scoped, small, non-escaping values live here.
- **Heap allocation** carries GC pressure and is the most common performance tax.

### What escapes
1. Returning a pointer or reference to a local variable.
2. Storing a value into an `any` / `interface{}` (including `fmt.Println`, `slog.Info` arguments in some paths).
3. Values that are too large for the stack or whose size is not known at compile time.

### Inspecting
```bash
go build -gcflags="-m" ./...
go build -gcflags="-m -m" ./...   # verbose, with reasons
```
Lines marked `escapes to heap` are candidates for restructuring   usually by returning by value instead of by pointer.

### When escaping is fine
- Returning a pointer from a constructor (`NewThing()`)   idiomatic and clear.
- Values that must outlive the function (globals, goroutine sends, struct fields).
- Small, infrequent allocations outside the hot path.
- When preventing the escape would hurt readability more than it helps.

## 2. Slice and Map Preallocation

A slice doubles capacity on growth, causing repeated allocation + copy. A map rehashes as it grows.

```go
// Bad   multiple reallocations as the slice grows
var result []string
for _, v := range items { result = append(result, v.Name) }

// Good   one allocation
result := make([]string, 0, len(items))
for _, v := range items { result = append(result, v.Name) }

// Maps: same idea
m := make(map[string]int, len(items))
```

**Skip preallocation when** input sizes are highly variable (risk of over-allocation + GC churn) or when profiling shows the growth cost is not a real bottleneck.

## 3. `sync.Pool` for Hot-Path Object Reuse

`sync.Pool` reuses short-lived objects across allocations, removing GC pressure in high-throughput code.

```go
var bufPool = sync.Pool{
    New: func() any { return new(bytes.Buffer) },
}

func handleRequest() {
    buf := bufPool.Get().(*bytes.Buffer)
    buf.Reset()            // ALWAYS reset before use
    defer bufPool.Put(buf) // return to pool
    // ...use buf...
}
```

### Rules
- ALWAYS `Reset()` (or zero the relevant fields) before `Put()` and after `Get()`   pooled objects retain stale data.
- Pool entries can be reclaimed at any GC, so `New` must always be valid.
- Do **not** pool when objects are long-lived, shared across goroutines, rarely reused, or when pooling adds complexity without measured benefit.

## 4. Interface Boxing and Reflection

- Passing a concrete value to an `any` parameter forces a heap allocation for the boxed value.
- `slog.Info` / `fmt.Printf` take `...any`; in hot paths use `slog.LogAttrs` with typed `slog.Attr` values to avoid boxing.
- `reflect.DeepEqual` is 50 200× slower than typed comparison. Use `slices.Equal`, `maps.Equal`, `bytes.Equal`.
- `panic`/`recover` allocates a stack trace and unwinds.  Use error returns, never as control flow.

## 5. `unsafe` and Zero-Copy Conversions

`[]byte(string)` and `string([]byte)` copy the backing array. In verified hot paths, a zero-copy `unsafe` conversion is acceptable **only with benchmark proof of a meaningful improvement**:

```go
// unsafe.String / unsafe.Slice (Go 1.20+)   no copy
b := unsafe.Slice(unsafe.StringData(s), len(s))
```

Document why the lifetime is safe (the original string must remain live and immutable for the lifetime of the byte slice). Without benchmark proof, do not reach for `unsafe`.

## 6. Worker Pools and Concurrency

- Default to the scheduler: for bounded, low-concurrency work, plain goroutines are often faster than a pool.
- Use a pool when workloads are bursty, unbounded, or you need to cap in-flight goroutines to protect downstreams.
- `errgroup.SetLimit(n)` provides a bounded worker pool with first-error cancellation   do not hand-roll one with channels.
- Send copies on channels, not pointers.  Pointers create invisible shared state.

See `go-essential` §4 for the full concurrency rules.

## 7. Runtime Tuning

- **`GOMEMLIMIT`**: set to 80-90% of container memory to prevent OOM kills and soften GC pauses.
- **`GOGC`**   adjust only after measuring GC% in pprof; default 100 is usually correct.
- **`GOMAXPROCS`**   in containers, use `automaxprocs` to match CPU limits; otherwise the runtime may over-schedule.
- **PGO (`-pgo=auto`)**: profile-guided optimization once the benchmarks are stable. Typically 2-7% CPU win.

## 8. Common Mistakes

| Mistake | Fix |
| --- | --- |
| Optimizing without profiling | Profile first   intuition is wrong ~80% of the time |
| `make([]T, 0)` then `append` in a loop | `make([]T, 0, knownLen)` |
| `reflect.DeepEqual` in production | `slices.Equal` / `maps.Equal` / `bytes.Equal` |
| `slog.Info` with `any` args in hot loop | `slog.LogAttrs` with typed attrs |
| `panic`/`recover` as control flow | Return errors |
| `unsafe` without benchmark proof | Only when pprof shows >10% win in a verified hot path |
| No GC tuning in containers | `GOMEMLIMIT` = 80-90% of container memory |
| Default `http.Client` Transport | Set `MaxIdleConnsPerHost` (default 2) to match concurrency |
| Logging in hot loops | Logging prevents inlining and allocates even when disabled |

