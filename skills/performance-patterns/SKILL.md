---
name: performance-patterns
description: Language-agnostic performance patterns for speed, throughput, latency, and memory optimization. Use when optimizing code, profiling hotspots, or refactoring for performance in the PROVE and ACT phases. Emphasizes measuring before optimizing.
---

# Performance Patterns

Apply only after correctness and safety are proven (in the THINK and ACT phases). Measure before and after; keep only what executable evidence supports.

> **Override.** A project-level performance policy that explicitly supersedes this skill takes precedence.

**Stance:** You treat intuition about bottlenecks as wrong ~80% of the time. Profile first; optimize the measured hot path; make one change at a time; cite benchmark evidence in commit messages and reports.

**Modes:**

- **Review mode (architecture)** -- broad scan of a module or service for structural anti-patterns (missing connection pools, unbounded concurrency, wrong data structures, N+1 queries). Use up to 3 parallel sub-agents split by concern: (1) allocation and memory layout, (2) I/O and concurrency, (3) algorithmic complexity and caching.
- **Review mode (hot path)** -- focused analysis of a single function or tight loop the caller named. Sequential.
- **Optimize mode** -- a bottleneck has been identified by a profiler or benchmark. Follow the iterative cycle (define metric -> baseline -> diagnose -> change one thing -> compare) sequentially.

---

## Rule Out External Bottlenecks First

Before optimizing code, verify the bottleneck is in your process. If 90% of latency is a slow DB query or upstream API call, local allocation tuning will not help.

**Diagnose:** (1) an off-CPU profiler shows I/O wait time; if off-CPU dominates, the bottleneck is external. (2) Distributed tracing shows which upstream span is slow. (3) A thread/task dump shows workers blocked in socket reads or DB drivers.

**When external:** optimize that component -- query tuning, caching, connection pools, circuit breakers.

---

## Iterative Methodology (THINK → ACT → PROVE)

The cycle: **Define -> Benchmark -> Diagnose -> Improve -> Compare**.

1. **Define your metric (THINK)** -- latency, throughput, memory, or CPU? Without a target, optimizations are random.
2. **Write an atomic benchmark (THINK)** -- isolate one function per benchmark to avoid result contamination.
3. **Measure baseline (PROVE)** -- capture to a file as an executable audit trail (`report-1.txt`).
4. **Diagnose (THINK)** -- use the Decision Tree below to pick the right tool and section.
5. **Improve (ACT)** -- apply ONE optimization at a time, with an explanatory comment.
6. **Compare (PROVE)** -- use a statistical comparator to confirm significance; paste the comparison in the report/commit so reviewers see the exact delta.
7. **Repeat (GROW)** -- increment the report number, catalog findings, and tackle the next bottleneck.

---

## Decision Tree: Where Is Time Spent?

| Bottleneck | Signal (from profiler) | Action |
|---|---|---|
| Too many allocations | heap `alloc_objects` high | Memory patterns below |
| CPU-bound hot loop | function dominates CPU profile | CPU / SIMD patterns below |
| GC pauses / OOM | high GC%, container memory limit hits | Runtime tuning (memory limit, GC/allocator trigger) |
| Network / I/O latency | threads/tasks blocked on I/O | I/O & networking patterns below |
| Off-CPU in DNS resolution | resolver time in traces | Cache results, pre-resolve IPs, use async/native resolver |
| Off-CPU in TLS handshake | handshake spans dominate | Enable session resumption, ALPN, fast cipher suites |
| Many socket TIME_WAITs | short-lived conns, no keep-alive | Connection pooling, SO_REUSEADDR, keep-alive headers |
| Repeated expensive work | same computation/fetch multiple times | Caching (memoization, single-flight, work avoidance) |
| Wrong algorithm | O(n^2) where O(n) exists | Algorithmic fix -- data structure swap |
| Lock contention | mutex/block profile hot | Concurrency patterns below; reduce critical section |
| Slow upstream queries | DB time dominates traces | Query tuning, batching, connection pool sizing |

---

## Memory Patterns

- **Object pooling** -- reuse objects through a checkout/return pool in tight loops; tune pool size against contention.
- **Preallocation** -- reserve capacity when the final size is known to avoid repeated reallocation and copying. Do not preallocate speculatively (e.g. allocating 10,000 slots when the common case is 10 items).
- **Field alignment** -- order struct/record fields largest -> smallest to minimize padding and improve CPU cache locality.
- **Avoid boxing** -- prefer concrete types over dynamic interfaces or erased generics in hot loops; pass value types directly.
- **Zero-copy** -- pass references, reuse buffers, and slice over views/spans in high-throughput paths.
- **Stack allocation** -- keep short-lived values on the stack; avoid pointers-to-locals and large closure captures.
- **Immutability for sharing** -- share read-only data across threads without locks; construct it fully before publishing.
- **Incremental building** -- use linear-time string/bytes builders instead of repeated string concatenation.
- **Avoid reflection in hot paths** -- typed comparison and access are orders of magnitude faster than dynamic reflection.

---

## Concurrency Patterns

- **Worker pools** -- use a fixed pool fed by a queue instead of spawning unmanaged threads/tasks per request.
- **Bounded concurrency** -- cap parallelism explicitly (semaphores, tickets, rate limiters) to prevent unbounded fan-out.
- **Atomics** -- use hardware atomics for simple counters and flags; prefer lock-free designs only when contention is low.
- **Lazy initialization** -- defer expensive setup until first use behind thread-safe once-only synchronization.
- **Cancellation propagation** -- thread cancellation tokens and timeouts through every child operation; missing this leaks background workers.
- **Structured error collection** -- group related concurrent work with shared cancellation and propagate the first meaningful error.
- **Bounded queues** -- use explicit capacity limits on channels/queues so backpressure signals upstream producers to slow down.

---

## I/O Patterns

- **Buffering** -- wrap unbuffered I/O streams with 4-64 KB buffers to coalesce system calls.
- **Batching** -- accumulate work to a size or time threshold; design for partial success and back-pressure.
- **Direct streaming** -- write formatted output directly to the destination writer instead of building intermediate in-memory buffers.
- **Tune transport defaults** -- default HTTP clients and DB drivers ship with low idle-connection limits; size them to match expected concurrency.
- **Guarded observability** -- wrap expensive log/trace string computation in an enabled-check; logging calls in hot loops allocate even when the level is disabled.
- **Sample tracing at the edge** -- per-request span creation allocates and shows up in profiles under high load; use head-based sampling.
- **Choose transport by workload** -- raw TCP/custom framing for lowest latency; HTTP/2 or HTTP/3 for multiplexed request/response with flow control; gRPC for IDL + cross-language RPC.
- **No panic/exceptions in hot paths** -- stack unwinding and exception object creation cost real cycles; return explicit errors or status codes.

---

## Resilience Under Load

- **Circuit breakers** -- open after N consecutive failures or latency threshold breach; shed calls until a probe succeeds.
- **Active load shedding** -- reject work at the edge when in-flight count or queue depth exceeds a measured threshold; cheaper than discarding work after processing.
- **Backpressure signaling** -- bounded queue depth signals upstream producers to slow down; never buffer unbounded input silently.
- **Degradation over failure** -- return partial, cached, or stale responses when capacity is exhausted if the domain allows it.

---

## SIMD & Vectorization

- **Auto-vectorization first** -- keep data contiguous, branch-free, and loop-independent so the compiler can vectorize operations.
- **Portable SIMD / intrinsics** -- use explicit SIMD intrinsics only when auto-vectorization measurably fails on a proven hot loop.
- **Data layout** -- prefer Struct-of-Arrays (SoA) over Array-of-Structs (AoS) and align data to vector register boundaries.
- **Branch elimination** -- use conditional moves or bitwise masks in hot loops where measurement supports it.

---

## Compiler & Runtime

- **Build flags** -- enable release mode optimizations (`-O3`, release profile, PGO) for production builds.
- **Escape analysis & allocations** -- minimize heap allocation in tight loops by avoiding unnecessary boxing or heap escapes.
- **Runtime limits in containers** -- set container memory limits and runtime allocation thresholds to ~80-90% to avoid OOM kills.
- **Document optimizations** -- add a comment with benchmark evidence explaining *why* a non-obvious pattern is faster, preventing accidental regressions during cleanup.

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Optimizing without profiling | Profile first -- intuition is wrong ~80% of the time |
| Default HTTP/DB client without transport tuning | Defaults cap idle connections at low numbers; size to concurrency |
| Logging in hot loops | Guard log evaluation with an enabled-check or lazy attributes |
| Unsafe / pointer tricks without benchmark proof | Justified only when profiling shows >10% improvement in a verified hot path |
| Dynamic reflection / deep equality in production | 50-200x slower than typed comparison; use typed equality |
| No memory limit in containers | Set runtime allocation/GC limit to 80-90% of container memory |
| Exceptions/panics as control flow in hot path | Stack unwinding allocates; use explicit error returns |
| One big benchmark touching everything | Isolate one function per benchmark; contaminated results mislead |
| Preallocating speculatively | Preallocate only when capacity is known with executable evidence |

---

## Cross-References

- [effective-code-craft](../effective-code-craft/SKILL.md) -- correctness and clarity come before performance; artifact gates (`INTENT:`, `TWINS:`)
- [harness-engineering](../harness-engineering/SKILL.md) -- deterministic logic in tested code; three-layer verification (L1/L2/L3)

