---
name: performance-patterns
description: "Language-agnostic performance patterns for allocation, concurrency, I/O, resilience, and caching. Use when profiling hotspots, optimizing a measured hot path, or auditing a module for structural performance defects in the ACT or PROVE phases."
---

# Performance Patterns

Optimize only after correctness and safety hold. Treat intuition about bottlenecks as wrong ~80% of the time: profile first, change one thing at a time, keep only what executable evidence supports.

> **Override.** A project-level performance policy that explicitly supersedes this skill takes precedence.

**Stance:** Every optimization claim cites benchmark evidence (command + output + delta). No measurement, no change.

## When to Load

Load when:

- A profiler or benchmark names a hot path, or you are optimizing code for speed, throughput, latency, or memory.
- Reviewing a module or service for structural defects: missing pools, unbounded concurrency, N+1 queries, wrong data structures.
- Diagnosing where time or memory is spent.

Do **not** load for correctness or clarity work; that is [code-craft](../code-craft/SKILL.md).

## Modes

- **Review (architecture)** broad scan for structural anti-patterns. Parallelize up to 3 concerns: allocation/layout, I/O/concurrency, algorithmic complexity/caching.
- **Review (hot path)** focused analysis of one named function or loop. Sequential.
- **Optimize**: a profiler/benchmark identified the bottleneck. Follow the measure-first cycle sequentially.

## Measure Before You Optimize

The cycle, every time: **Define, Benchmark, Diagnose, Improve, Compare**. Detail in [Measurement methodology](./references/measurement.md).

1. **Define** the target metric (latency, throughput, memory, CPU). No target means random optimization.
2. **Benchmark** isolate one function per benchmark; capture baseline to a file as an audit trail.
3. **Diagnose** rule out external bottlenecks first, then apply the decision tree below.
4. **Improve** ONE change at a time, with a comment naming why.
5. **Compare** use a statistical comparator to confirm significance; paste the delta in the report or commit.

**Rule out external first.** If an off-CPU profiler, distributed trace, or worker dump shows the time is in DB queries, upstream calls, or socket reads, local allocation tuning will not help. Fix that component: caching, pooling, circuit breakers, query tuning.

## Decision Tree: Where Is Time Spent?

Route the profiler signal to the right pattern set.

| Bottleneck | Signal | Action |
|---|---|---|
| Too many allocations | high `alloc_objects` | [Memory patterns](./references/memory-cpu.md) |
| CPU-bound hot loop | dominates CPU profile | [CPU & SIMD](./references/memory-cpu.md) |
| GC pauses / OOM | high GC%, container limit hit | Runtime tuning (memory limit, GC/allocator trigger) |
| Network / I/O latency | workers blocked on I/O | [I/O patterns](./references/io-resilience.md) |
| DNS / TLS overhead | resolver or handshake spans dominate | Cache, pre-resolve, session resumption, ALPN |
| TIME_WAIT storms | short-lived conns, no keep-alive | Pooling, SO_REUSEADDR, keep-alive |
| Repeated expensive work | same fetch/computation repeats | [Caching](./references/io-resilience.md) |
| Wrong algorithm | O(n^2) where O(n) exists | Data-structure swap |
| Lock contention | mutex/block profile hot | [Concurrency](./references/concurrency.md) |
| Slow upstream queries | DB time dominates traces | Query tuning, batching, pool sizing |

## References

- [Measurement methodology](./references/measurement.md) the measure-first cycle, external-bottleneck diagnosis, benchmark and statistical hygiene.
- [Memory, CPU & SIMD](./references/memory-cpu.md) pooling, preallocation, field layout, zero-copy, vectorization, build/runtime tuning.
- [Concurrency](./references/concurrency.md) worker pools, bounded parallelism, atomics, cancellation, structured error collection, backpressure.
- [I/O & resilience](./references/io-resilience.md) buffering, batching, streaming, transport tuning, caching, circuit breakers, load shedding, degradation.
- [Pitfalls](./references/pitfalls.md) the common-mistakes table and cross-cutting checks.

## Cross-References

- [code-craft](../code-craft/SKILL.md) correctness and clarity come before performance; artifact gates (`INTENT:`, `TWINS:`)
- [harness-engineering](../harness-engineering/SKILL.md) deterministic logic in tested code; three-layer verification (L1/L2/L3)
