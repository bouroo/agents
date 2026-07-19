---
name: performance-patterns
description: >
  Patterns for high-performance software across any language. Covers memory, concurrency, I/O, and compiler
  optimizations. Use when optimizing for speed, throughput, latency, or memory. Grounded in goperf.dev and Google's Go best-practices.
---

# Performance Patterns

Apply only after correctness is proven. Measure before and after; keep what the data supports.

> **Override.** A project-level performance policy that explicitly supersedes this skill takes precedence.

**Stance:** You treat intuition about bottlenecks as wrong ~80% of the time. Profile first; optimize the measured hot path; one change at a time; cite the benchmark in the commit message.

**Modes:**

- **Review mode (architecture)** -- broad scan of a module or service for structural anti-patterns (missing connection pools, unbounded concurrency, wrong data structures, N+1 queries). Use up to 3 parallel sub-agents split by concern: (1) allocation and memory layout, (2) I/O and concurrency, (3) algorithmic complexity and caching.
- **Review mode (hot path)** -- focused analysis of a single function or tight loop the caller named. Sequential.
- **Optimize mode** -- a bottleneck has been identified by a profiler or benchmark. Follow the iterative cycle (define metric -> baseline -> diagnose -> change one thing -> compare) sequentially. Sequential.

## Rule Out External Bottlenecks First

Before optimizing code, verify the bottleneck is in your process. If 90% of latency is a slow DB query or upstream API call, allocation tuning will not help.

**Diagnose:** (1) an off-CPU profiler shows I/O wait time; if off-CPU dominates, the bottleneck is external. (2) Distributed tracing shows which upstream span is slow. (3) A goroutine/thread dump blocked in socket reads or DB drivers = external wait.

**When external:** optimize that component -- query tuning, caching, connection pools, circuit breakers.

## Iterative Methodology

The cycle: **Define -> Benchmark -> Diagnose -> Improve -> Compare**.

1. **Define your metric** -- latency, throughput, memory, or CPU? Without a target, optimizations are random.
2. **Write an atomic benchmark** -- isolate one function per benchmark to avoid result contamination.
3. **Measure baseline** -- capture to a file as an audit trail (`report-1.txt`).
4. **Diagnose** -- use the Decision Tree below to pick the right tool and section.
5. **Improve** -- apply ONE optimization at a time, with an explanatory comment.
6. **Compare** -- use a statistical comparator (e.g. `benchstat`) to confirm significance; paste the comparison in the commit body so reviewers see the exact delta.
7. **Repeat** -- increment the report number, tackle the next bottleneck.

## Decision Tree: Where Is Time Spent?

| Bottleneck | Signal (from profiler) | Action |
|---|---|---|
| Too many allocations | heap `alloc_objects` high | Memory patterns below |
| CPU-bound hot loop | function dominates CPU profile | CPU / SIMD patterns below |
| GC pauses / OOM | high GC%, container limits | Runtime tuning (memory limit, GC trigger) |
| Network / I/O latency (general) | threads blocked on I/O | I/O & networking patterns below |
| Off-CPU in DNS resolution | resolver time in traces | Cache results, pre-resolve IPs, force pure-Go resolver |
| Off-CPU in TLS handshake | handshake spans dominate | Enable session resumption, ALPN, fast cipher suites |
| Many TIME_WAIT sockets | short-lived conns, no keep-alive | Connection pooling, SO_REUSEADDR |
| Repeated expensive work | same computation/fetch multiple times | Caching (singleflight, memoization, work avoidance) |
| Wrong algorithm | O(n^2) where O(n) exists | Algorithmic fix -- data structure swap |
| Lock contention | mutex/block profile hot | Concurrency patterns below; reduce critical section |
| Slow upstream queries | DB time dominates traces | Query tuning, batch, connection pool sizing |

## Memory

- **Object pooling** -- reuse objects through a checkout/return pool in tight loops; tune pool size against contention.
- **Preallocation** -- reserve capacity when the final size is known to avoid repeated reallocation and copying. Do not preallocate speculatively -- `make([]T, 0, 1000)` wastes memory when the common case is 10 items.
- **Field alignment** -- order fields largest -> smallest to minimize padding and improve cache locality.
- **Avoid boxing** -- prefer concrete types over interfaces or erased generics in hot loops; pass value types by value.
- **Zero-copy** -- pass references, reuse buffers, and slice over views in high-throughput paths.
- **Stack allocation** -- keep short-lived values on the stack; avoid pointers-to-locals and large closure captures.
- **Immutability for sharing** -- share read-only data without locks; construct it fully before publishing.
- **Incremental building** -- use a linear-time builder instead of repeated concatenation that becomes quadratic.
- **Avoid reflection in hot paths** -- typed comparison and access are orders of magnitude faster than reflection-based equivalents.

## Concurrency

- **Worker pools** -- use a fixed pool fed by a queue instead of spawning one worker per task.
- **Bounded concurrency** -- cap parallelism explicitly (`SetLimit(n)`, semaphores, tickets) to prevent unbounded fan-out under load.
- **Atomics** -- use hardware atomics for simple counters and flags; prefer lock-free designs only when contention is low.
- **Lazy initialization** -- defer expensive setup until first use behind once-only synchronization.
- **Cancellation propagation** -- thread cancellation and timeouts through every child operation; missing this leaks workers.
- **Structured error collection** -- group related work with shared cancellation and propagate the first meaningful error.
- **Directional channels / unbuffered by default** -- distinguish send-only from receive-only channels for compile-time safety; larger buffers mask backpressure, use them only with measured justification.

## I/O

- **Buffering** -- wrap unbuffered I/O with 4-64 KB buffers to coalesce system calls.
- **Batching** -- accumulate work to a size or time threshold; design for partial success and back-pressure.
- **Direct streaming** -- write formatted output directly to the destination writer instead of building intermediates.
- **Tune transport defaults** -- default HTTP clients and DB drivers ship with low idle-connection limits; size them to match your concurrency.
- **Guarded observability** -- wrap expensive log and trace computation in an enabled-check; log calls in hot loops allocate even when the level is disabled.
- **Sample tracing at the edge** -- per-connection spans allocate and show up in heap profiles at 10K+ connections; use head-based sampling, never blindly trace every connection.
- **Choose transport by workload** -- raw TCP/custom framing for lowest latency and per-message control; HTTP/2 for multiplexed request/response with flow control; gRPC for IDL + streaming + cross-language; QUIC for connection migration, 0-RTT, and lossy/mobile paths. Multiplexed HTTP/2 or QUIC typically beats a pool of HTTP/1.1 connections under high concurrency -- measure both before committing.
- **No panic/recover in hot paths** -- stack unwinding and stack-trace allocation cost real cycles; use error returns.

## Resilience Under Load

- **Circuit breakers** -- open after N consecutive failures or latency threshold breach; shed calls until a probe succeeds. Protects latency and upstream cost, not just correctness.
- **Active load shedding** -- reject work at the edge when in-flight count or queue depth exceeds a measured threshold; cheaper than doing work you will discard. Shed before queueing, not after.
- **Backpressure signaling** -- bounded queue depth is the signal to upstream producers to slow down; never silently buffer unbounded. Propagate backpressure through every stage of a pipeline.
- **Degradation over failure** -- when capacity is exhausted, return a partial/cached/stale response instead of an error where the domain allows it.

## SIMD & Vectorization

- **Auto-vectorization first** -- keep data contiguous, branch-free, and loop-independent so the compiler can widen operations.
- **Portable SIMD / intrinsics** -- use explicit SIMD only when auto-vectorization measurably fails on a proven hot loop.
- **Data layout** -- prefer struct-of-arrays over array-of-structs and align data to vector width.
- **Branch elimination** -- use conditional moves or masks in hot loops where measurement supports it.
- **Measure the vectorized path** -- benchmark scalar and vectorized implementations on realistic data.

## Compiler & Runtime

- **Build flags** -- enable release modes and use profile-guided optimization for proven hot code.
- **Escape analysis** -- minimize heap escapes with value types and avoid interface wrapping in hot paths.
- **Runtime limits in containers** -- set the runtime memory limit to ~80-90% of the container memory to prevent OOM kills; tune the GC trigger against live heap.
- **Document optimizations** -- add a comment with the benchmark number explaining *why* a non-obvious pattern is faster, so a future reader does not "clean it up" and regress.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Optimizing without profiling | Profile first -- intuition is wrong ~80% of the time |
| Default HTTP/DB client without transport tuning | Defaults cap idle connections at ~2; size to your concurrency |
| Logging in hot loops | Log calls allocate even when level is disabled; guard with enabled-check, use lazy/attr variants |
| `unsafe` / pointer arithmetic without benchmark proof | Justified only when profiling shows >10% improvement in a verified hot path |
| `reflect.DeepEqual` / generic equality in production | 50-200x slower than typed comparison; use language-native equality |
| No memory limit in containers | Set runtime memory limit to 80-90% of container memory |
| Panic/exception as control flow in hot path | Stack unwinding allocates; use error returns |
| One big benchmark that touches everything | Isolate one function per benchmark; contaminated results mislead |
| Preallocating speculatively | Preallocate only when capacity is known with evidence |

## Cross-References

- [effective-code-craft](../effective-code-craft/SKILL.md) -- correctness and clarity come before performance
- [harness-engineering](../harness-engineering/SKILL.md) §11 -- deterministic logic in tested code, not in the model
