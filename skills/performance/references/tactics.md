# Performance Tactics

> Load on demand when the profiler has named the bottleneck; routing lives in [performance](../SKILL.md). Time goes to four places: allocation churn, lock contention, syscall counts, and data copying. Apply only after correctness holds ([craft](../../craft/SKILL.md)); confirm each change helped via [measurement](./measurement.md), not intuition.

## Allocation churn

- **Object pooling** reuse objects through a checkout/return pool in tight loops; tune pool size against contention. Pool only hot paths — maintenance can exceed allocation cost on cold ones.
- **Preallocation** reserve capacity when the final size is known, to avoid repeated reallocation and copying. Never preallocate speculatively (10,000 slots for a 10-item common case); preallocate on executable evidence of capacity.
- **Field alignment** order struct/record fields largest to smallest to minimize padding and improve cache locality.
- **Avoid boxing and reflection in hot paths.** Concrete types over erased/dynamic interfaces in loops; typed comparison is 50-200x faster than dynamic reflection.
- **Incremental building** linear-time string/bytes builders over repeated concatenation, which is quadratic in naive forms.
- **Keep short-lived values off the heap.** Avoid pointers-to-locals and large closure captures that force escape; confirm with an allocation profiler.

## Lock contention

- **Atomics before mutexes.** An atomic value (counter, flag, single pointer) is cheaper than a lock, never deadlocks, and stays uncontended. A mutex earns its cost only when the critical section spans multiple fields or guards a non-trivial invariant; when reads dominate writes, prefer a reader-writer split.
- **Worker pools** fixed pool fed by a queue instead of unmanaged per-request tasks; unbounded tasks exhaust memory under load.
- **Bounded concurrency** cap parallelism explicitly (semaphores, tickets, rate limiters) so fan-out cannot overwhelm downstreams or memory.
- **Immutable sharing** share read-only data across threads with no locks; construct fully before publishing.
- **Lazy initialization** defer expensive setup to first use behind once-only synchronization; cold paths pay nothing.
- **Cancellation propagation** thread cancellation tokens and timeouts through every child operation; a missing token leaks workers that outlive their request.
- **Structured error collection** group related concurrent work under shared cancellation and propagate the first meaningful error; one failure must not strand the rest.
- **Bounded queues** explicit capacity so backpressure signals producers to slow down; an unbounded queue turns a load spike into an OOM.

## Syscall count

- **Buffering** wrap unbuffered streams in 4-64 KB buffers to coalesce system calls; a syscall per byte is a classic throughput killer.
- **Batching** accumulate work to a size or time threshold; design for partial success so one failed batch does not lose the unfailed items.
- **Tune transports.** Default HTTP clients and DB drivers ship low idle-connection limits sized down for safety; set them to expected concurrency or they cap throughput silently. Choose by workload: raw TCP/framing for latency, HTTP/2 or /3 for multiplexed request-response, IDL-based RPC for cross-language contracts.
- **Connection reuse** keep-alive, address reuse, pooling — short-lived connections end in TIME_WAIT storms.
- **DNS/TLS** cache resolutions and pre-resolve known hosts behind an async resolver; enable session resumption and ALPN; handshake spans dominate connection-heavy loads.
- **Cache repeated work:** memoize pure computations keyed by inputs; single-flight concurrent identical requests into one call; order checks so the cheap discriminating test runs first.
- **Resilience under load:** circuit breakers open after consecutive failures or latency breach until a probe succeeds; shed load at the edge on measured thresholds; return partial/cached/stale when capacity is exhausted if the domain allows; bounded queues provide the backpressure all of this relies on.

## Data copying

- **Zero-copy** pass references, reuse buffers, slice views/spans in high-throughput paths instead of copying bytes.
- **Stream, don't stage** write formatted output directly to the destination writer rather than through intermediate in-memory buffers.

## Compute & runtime

- **Auto-vectorization first**: keep data contiguous, branch-free, loop-independent; reach for explicit SIMD/intrinsics only when measurement proves auto-vectorization failed on a hot loop. Prefer SoA layout and vector-aligned data.
- **Branch elimination** conditional moves/bitwise masks where measurement supports it; a mispredicted branch costs more than the arithmetic it replaces.
- **Release builds are evidence**; debug builds prove nothing. Container runtimes need memory/GC limits at 80-90% of the limit — no limit eventually means OOM.
- **Unsafe tricks** justified only when profiling shows >10% improvement in a verified hot path; otherwise safety and portability outweigh them.
- **Document why** non-obvious optimizations carry a comment citing benchmark evidence, so cleanup does not silently regress them.

## Pitfall checklist

| Mistake | Fix |
|---|---|
| Optimizing without profiling | Profile first; intuition is wrong ~80% of the time |
| Untuned default HTTP/DB clients | Defaults cap connections low; size to concurrency |
| Logging in hot loops | Guard evaluation behind an enabled-check or lazy attributes |
| Exceptions as control flow in hot path | Stack unwinding allocates; use explicit error returns |
| Reflection / deep equality in production paths | 50-200x slower than typed comparison |
| No container memory limit | Runtime allocation/GC limit at 80-90% of container memory |
| Unsafe tricks without benchmark proof | Only with >10% measured improvement |
| Speculative preallocation | Capacity known via executable evidence only |
| One big benchmark touching everything | Isolate functions; contaminated results mislead |

Cross-cutting: measured before *and* after? one change at a time? external bottleneck ruled out? *why* documented?
