# Performance - Depth

Loaded on demand from [go-essential](../SKILL.md) §10. The core discipline lives there; this
file covers the diagnostic decision tree, optimization patterns, and runtime tuning.

> **Stance:** intuition about bottlenecks is wrong ~80% of the time. Profile first; optimize the
> measured hot path; one change at a time; cite the benchmark in the commit message.

## Rule Out External Bottlenecks First

Before optimizing Go code, verify the bottleneck is in your process. If 90% of latency is a slow
DB query or upstream API call, allocation tuning will not help.

**Diagnose:**

1. **`fgprof`** - captures on-CPU *and* off-CPU (I/O wait) time. If off-CPU dominates, the
   bottleneck is external.
2. **`go tool pprof`** goroutine profile - many goroutines blocked in `net.(*conn).Read` or
   `database/sql` = external wait.
3. **Distributed tracing** (OpenTelemetry) - span breakdown shows which upstream is slow.

**When external:** optimize that component - query tuning, caching, connection pools, circuit
breakers. See the [Caching Patterns](#caching) section below.

## Iterative Methodology

The cycle: **Define → Baseline → Diagnose → Improve → Compare**. One change at a time is the
discipline.

1. **Define your metric** - latency, throughput, memory, or CPU. Without a target,
   optimizations are random.
2. **Write an atomic benchmark** - isolate one function per benchmark so results aren't
   contaminated.
3. **Measure baseline:**

   ```bash
   go test -bench=BenchmarkMyFunc -benchmem -count=6 ./pkg/... | tee /tmp/report-1.txt
   ```

4. **Diagnose** - use the decision tree below to pick the right tool and pattern.
5. **Improve** - apply ONE optimization at a time. Add a code comment explaining *why* it's
   faster (with benchmark numbers when available) so a future reader doesn't revert it as
   "unnecessary."
6. **Compare:**

   ```bash
   benchstat /tmp/report-1.txt /tmp/report-2.txt
   ```

   Confirms statistical significance.
7. **Commit** - paste the benchstat output in the commit body; use `perf(scope): summary`.
8. **Repeat** - increment the report number, tackle the next bottleneck. Keep all
   `/tmp/report-*.txt` files as an audit trail.

## Decision Tree - Where Is Time Spent?

| Bottleneck                  | Signal (from pprof)                    | Pattern                                    |
| --------------------------- | -------------------------------------- | ------------------------------------------ |
| Too many allocations        | `alloc_objects` high in heap profile   | [Memory](#memory)                          |
| CPU-bound hot loop          | function dominates CPU profile         | [CPU](#cpu)                                |
| GC pauses / OOM             | high GC%, container limits             | [Runtime tuning](#runtime-tuning)          |
| Network / I/O latency       | goroutines blocked on I/O              | [I/O & networking](#io--networking)        |
| Repeated expensive work     | same computation/fetch multiple times  | [Caching](#caching)                        |
| Wrong algorithm             | O(n²) where O(n) exists                | [Algorithmic complexity](#caching)         |
| Lock contention             | mutex/block profile hot                | [Concurrency](./concurrency.md)            |
| Slow queries                | DB time dominates traces               | Tune query, pool, add cache                |

## Memory

Allocation reduction yields the biggest ROI in Go - the GC is fast but not free, and reducing
allocations per request often matters more than micro-optimizing CPU.

- **Preallocate slices and maps when size is known:**

  ```go
  users := make([]User, 0, len(ids))         // capacity known
  m := make(map[string]int, len(items))      // size known
  ```

  Do not preallocate speculatively (`make([]T, 0, 1000)` when the common case is 10 items).

- **`strings.Builder` for concatenation in loops.** `+` allocates a fresh string each time.

- **`sync.Pool` for short-lived, high-allocation objects** (buffers, decoded JSON envelopes).
  Always `Reset()` before `Put()`. Pooling reduces GC pressure, not allocation count in the
  profile.

- **Mind struct field alignment.** Reorder fields from largest to smallest to avoid padding:

  ```go
  // ✗ 24 bytes (padding between bool and int64)
  type Bad struct { b bool; x int64; y int32 }
  // ✓ 16 bytes (no padding)
  type Good struct { x int64; y int32; b bool }
  ```

  Run `fieldalignment` to find candidates:

  ```bash
  go install golang.org/x/tools/go/analysis/passes/fieldalignment/cmd/fieldalignment@latest
  fieldalignment -fix ./...
  ```

- **Escape analysis** - know what forces heap allocation: returning a pointer to a local;
  assigning to an interface (boxing); closures capturing a pointer; slices growing past cap.
  Inspect with `go build -gcflags="-m"`.

- **Beware `append` backing-array leaks.** Slicing a large buffer and keeping a small subslice
  retains the whole backing array. Copy: `out := make([]byte, 8); copy(out, big[:8])`.

## CPU

- **Inlining matters more than micro-tricks.** Small, leaf functions get inlined; the compiler
  won't inline functions with `defer`, `panic`, `recover`, complex loops, or `select`. Inspect
  with `go build -gcflags="-m"`. Avoid defeating inlining in hot paths.
- **Cache locality - traverse data the way it's laid out.** Column-major over row-major;
  contiguous slices over pointer-chasing linked structures; `[][]int` (one allocation per row)
  vs a flat `[]int` with manual indexing for large matrices.
- **False sharing.** Adjacent fields written by different goroutines cause cache-line
  invalidation. Pad to a cache line (64 bytes) for hot shared counters:

  ```go
  type Counter struct {
      n  int64
      _  [56]byte   // pad to 64 bytes
  }
  ```

- **Instruction-level parallelism (ILP).** Avoid data dependencies in tight loops; the CPU can
  issue multiple independent ops per cycle.
- **Avoid reflection in hot paths.** `reflect.DeepEqual` is 50-200× slower than typed
  comparison - use `slices.Equal`, `maps.Equal`, `bytes.Equal`.
- **`unsafe` only with benchmark proof.** Justified only when profiling shows >10% improvement in
  a verified hot path. Isolate and document.

## I/O & Networking

- **Tune the HTTP transport.** The default `http.Client{}` shares a `DefaultTransport` whose
  `MaxIdleConnsPerHost` is **2** - fatal under any real concurrency. Set it to match your
  concurrency level:

  ```go
  client := &http.Client{
      Transport: &http.Transport{
          MaxIdleConns:        100,
          MaxIdleConnsPerHost: 100,
          IdleConnTimeout:     90 * time.Second,
      },
      Timeout: 10 * time.Second,
  }
  ```

  Reuse one `*http.Client` across the process; do not create one per request.

- **Stream large transfers** (DB rows → HTTP response). Materializing millions of rows causes
  OOM; streaming keeps memory constant. `rows.Next()` + `json.Encoder.Write` instead of
  `rows-to-slice` then `json.Marshal`.

- **JSON performance.** `encoding/json` is reflection-based. For hot paths, reach for
  `encoding/json/v2` (Go 1.25+), `bytedance/sonic`, `goccy/go-json`, or code generation
  (`easyjson`, `ffjson`).

- **Batch DB operations.** A single multi-row `INSERT` beats N single-row inserts. Use
  `database/sql` `Begin`/`Prepare`/`Exec` batches or a query builder.

- **cgo has a cost.** Each cgo call crosses the Go↔C boundary (~100-200ns) and prevents the
  scheduler from running that goroutine on a different OS thread. Avoid cgo in hot paths;
  rewrite in pure Go if the call is frequent.

## Caching

- **Work avoidance is the fastest code.** The cheapest computation is the one you don't do.
- **`sync.Once` / `OnceValue` / `OnceValues`** for one-time computation.
- **`golang.org/x/sync/singleflight`** to deduplicate concurrent identical calls - cache-stampede
  prevention.
- **In-memory cache with TTL and eviction** (`ristretto`, `bigcache`,
  `ristretto`) for repeated expensive reads. Mind eviction policy (LRU, LFU, S3FIFO, TinyLFU),
  sharding, and stale-while-revalidate semantics.
- **Algorithmic complexity first.** A cache can't save an O(n²) algorithm. Choose the right data
  structure before caching: maps for O(1) lookup, sorted slices + `slices.BinarySearch` for
  ordered scans, `btree` for range queries.
- **Compile regexps once at package level.** `regexp.MustCompile` is O(n) in pattern length and
  allocates; recompiling per request is a silent hotspot.

## Runtime Tuning

- **`GOMEMLIMIT`** - set to 80-90% of container memory to prevent OOM kills. Without it, the GC
  sees unlimited memory and won't tighten until the kernel kills the process.

- **`GOGC`** - controls GC trigger as a percentage of live heap (default 100 = double the heap).
  Lower = more frequent GC (less memory, more CPU). Raise only with measurement; pair with
  `GOMEMLIMIT` in containers.

- **`GOMAXPROCS`** - defaults to the number of logical CPUs. In containers with CPU limits, set
  via `automaxprocs` (`go.uber.org/automaxprocs`) so the runtime sees the cgroup quota instead of
  the host CPU count.

- **Profile-Guided Optimization (PGO)** - Go 1.21+. Collect a CPU profile from production,
  place it at `default.pgo` in the main package, rebuild. Typical gains 2-7% with no code change.

- **GC diagnostics:**

  ```bash
  GODEBUG=gctrace=1 ./myapp 2>gc.log
  ```

  Each line: trigger reason, live heap, GC pause. Long pauses point to large heaps (raise
  `GOGC` or reduce allocations) or pointer-dense data (work avoidance / pooling).

## Common Mistakes

| Mistake                                          | Fix                                                                 |
| ------------------------------------------------ | ------------------------------------------------------------------- |
| Optimizing without profiling                     | Profile with pprof first - intuition is wrong ~80% of the time      |
| Default `http.Client` without Transport tuning   | `MaxIdleConnsPerHost` defaults to 2; set to match concurrency       |
| Logging in hot loops                             | Even disabled-level calls allocate; use `slog.LogAttrs`             |
| `panic`/`recover` as control flow                | Allocates a stack trace and unwinds; use error returns              |
| `unsafe` without benchmark proof                 | Only justified when profiling shows >10% in a verified hot path     |
| No GC tuning in containers                       | Set `GOMEMLIMIT` to 80-90% of container memory                      |
| `reflect.DeepEqual` in production                | 50-200× slower; use `slices.Equal`, `maps.Equal`, `bytes.Equal`     |
| Speculative preallocation                        | Preallocate only when size is known; otherwise wastes memory        |
| `sync.Pool` item not Reset before Put            | Next user sees stale state                                          |
| Struct fields in arbitrary order                 | Reorder largest-to-smallest to eliminate padding; run fieldalignment |
| Rebuilding regexp per request                    | `regexp.MustCompile` once at package level                          |
| Creating `*http.Client` per request              | Reuse one client process-wide                                       |

## Audit Sub-Agents (Parallel)

When reviewing performance across a package or service, split into 3 parallel sub-agents:

1. **Allocation and memory layout** - escapes, backing-array leaks, struct alignment, pooling
   opportunities, preallocation.
2. **I/O and concurrency** - HTTP transport config, streaming vs. materialization, batch
   opportunities, unbounded goroutine spawning, lock contention.
3. **Algorithmic complexity and caching** - O(n²) hot spots, missing caches, repeated regexp
   compilation, work avoidance, singleflight opportunities.

## Cross-References

- Depth on benchmarking methodology (`b.Loop()`, `benchstat`, profiling from benchmarks): see
  [Testing](./testing.md).
- Worker pools, `sync.Pool` API, goroutine lifecycle, lock contention: see
  [Concurrency](./concurrency.md).
- Continuous profiling in production: see [Observability](./observability.md).
- Language-agnostic performance patterns (concurrency, I/O, compiler optimizations):
  [performance-patterns](../../performance-patterns/SKILL.md).
