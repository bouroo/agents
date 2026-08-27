---
name: performance
description: "Language-agnostic performance discipline: the measure-first cycle, bottleneck routing, and tactic tables organized by the four runtime-overhead sources. Use when profiling hotspots, optimizing a measured hot path, or auditing a module for structural defects."
---

# Performance

Optimize only after correctness holds, and only by measurement.

**Stance:** every optimization claim cites benchmark evidence (command + output + delta). No measurement, no change. Intuition about bottlenecks is wrong ~80% of the time; profile first, change one thing, keep only what executable evidence supports.

**When to load:** a profiler or benchmark names a hot path; you are optimizing speed, throughput, latency, or memory; or you review a module structurally (missing pools, unbounded concurrency, N+1 queries). Do **not** load for correctness or clarity work — that is [craft](../craft/SKILL.md).

## The cycle: Define, Benchmark, Diagnose, Improve, Compare

1. **Define** the target metric (latency, throughput, memory, CPU) and its target value. No target means random optimization.
2. **Benchmark** isolate one function per benchmark; capture the baseline to a numbered file as the audit trail.
3. **Diagnose** rule out external bottlenecks first (below), then route via the overhead table.
4. **Improve** ONE change at a time, with a comment naming why.
5. **Compare** confirm significance with a statistical comparator; paste the delta in report or commit.

Hygiene details: [measurement](references/measurement.md).

## Rule out external bottlenecks first

Before optimizing code, verify the time is actually yours. An off-CPU profiler showing I/O wait, a distributed trace naming a slow upstream span, or a thread dump full of workers blocked on socket reads means local tuning will not move the number — fix that component (query tuning, caching, pooling, batch sizing) and re-profile; the internal hot path may have moved or vanished.

## Route the signal

Time goes to one of four places. Match the profiler signal to the source, then load the countermeasures from [tactics](references/tactics.md):

| Signal | Overhead source | Countermeasures |
|---|---|---|
| high `alloc_objects`, GC pressure | allocation churn | pool, preallocate known sizes, reduce boxing/reflection |
| mutex/block profile hot | lock contention | bound concurrency, share immutably, atomics over locks |
| many small I/O calls | syscall count | buffer, batch, tune transports, cache repeated work |
| memcpy-heavy profiles, large payloads | data copying | zero-copy views/slices, stream, pass references |
| GC pauses / OOM | heap pressure + limits | set runtime memory/GC limits to 80-90% of container limit |

Keep the cheap overrides in mind: wrong algorithm (swap the structure before tuning the loop), repeated expensive work (memoize, single-flight, avoid), slow upstream queries (tune the query, size the pool).

**Scope:** broad structural scans look for pools, bounds, N+1 queries, wrong structures — three passes max (allocation/layout, I/O/concurrency, algorithmic complexity/caching); focused reviews follow the cycle sequentially.

**Goal:** boring code that stays fast when traffic spikes — not clever tricks.
