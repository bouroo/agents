# Memory, CPU & SIMD Patterns

> Load on demand when the profiler points at allocations, a CPU-bound loop, or GC/allocator pressure. The decision tree lives in [performance-patterns](../SKILL.md).

## Memory Patterns

- **Object pooling** -- reuse objects through a checkout/return pool in tight loops; tune pool size against contention. Pool only hot paths; pool maintenance can exceed allocation cost on cold paths.
- **Preallocation** -- reserve capacity when the final size is known to avoid repeated reallocation and copying. Do not preallocate speculatively (e.g. 10,000 slots when the common case is 10 items); preallocate only with executable evidence of capacity.
- **Field alignment** -- order struct/record fields largest to smallest to minimize padding and improve CPU cache locality.
- **Avoid boxing** -- prefer concrete types over dynamic interfaces or erased generics in hot loops; pass value types directly to avoid heap allocation.
- **Zero-copy** -- pass references, reuse buffers, and slice over views/spans in high-throughput paths instead of copying bytes.
- **Stack allocation** -- keep short-lived values on the stack; avoid pointers-to-locals and large closure captures that escape to the heap.
- **Immutability for sharing** -- share read-only data across threads without locks; construct it fully before publishing.
- **Incremental building** -- use linear-time string/bytes builders instead of repeated concatenation, which is quadratic in naive forms.
- **Avoid reflection in hot paths** -- typed comparison and access are 50-200x faster than dynamic reflection; use typed equality and typed access.

## SIMD & Vectorization

- **Auto-vectorization first** -- keep data contiguous, branch-free, and loop-independent so the compiler can vectorize. Most loops need no hand-written SIMD.
- **Portable SIMD / intrinsics** -- use explicit intrinsics only when auto-vectorization measurably fails on a proven hot loop. Prefer portable SIMD types over per-architecture intrinsics.
- **Data layout** -- prefer Struct-of-Arrays (SoA) over Array-of-Structs (AoS), and align data to vector register boundaries, so a vector load is one instruction.
- **Branch elimination** -- use conditional moves or bitwise masks in hot loops where measurement supports it; a mispredicted branch is costlier than the arithmetic it replaces.

## Compiler & Runtime

- **Build flags** -- enable release-mode optimizations (`-O3`, release profile, PGO) for production builds. Debug builds are not evidence.
- **Escape analysis & allocations** -- minimize heap allocation in tight loops by avoiding unnecessary boxing or heap escapes; confirm with an allocation profiler.
- **Runtime limits in containers** -- set container memory limits and runtime allocation/GC thresholds to ~80-90% of the limit to avoid OOM kills. No limit eventually means OOM.
- **Unsafe / pointer tricks** -- justified only when profiling shows >10% improvement in a verified hot path; otherwise the safety and portability cost is not worth it.
- **Document optimizations** -- add a comment with benchmark evidence explaining *why* a non-obvious pattern is faster, so cleanup does not silently regress it.

## Source

Apply only after [effective-code-craft](../../code-craft/SKILL.md) correctness holds. Confirm each change helped via [Measurement methodology](./measurement.md), not intuition.
