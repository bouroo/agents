---
name: performance-patterns
description: >
  Patterns for high-performance software across any language. Covers memory, concurrency, I/O, and compiler
  optimizations. Use when optimizing for speed, throughput, latency, or memory. Grounded in goperf.dev and Google's Go best-practices.
---

# Performance Patterns

Apply only after correctness is proven. Measure before and after; keep what the data supports.

## Memory

- **Object pooling**  --  in tight loops or hot paths, reuse via a checkout/return pool; tune size against footprint and contention.
- **Preallocation**  --  when a collection's final size is known, reserve capacity up front to avoid repeated reallocation and copying.
- **Field alignment**  --  for large or frequently allocated structs, order fields largest → smallest (64 → 8 bit) to minimize padding and improve cache locality.
- **Avoid boxing**  --  in hot loops use concrete types over interface/erased generics; pass value types by value to prevent hidden heap allocations.
- **Zero-copy**  --  for large data or high-throughput pipelines, pass references, reuse buffers, slice over views instead of duplicating.
- **Stack allocation**  --  keep short-lived values on the stack by avoiding pointers-to-locals, large closure captures, unintended escape.
- **Immutability for sharing**  --  share read-only data across workers without locks; construct fully before publishing, never mutate after.
- **Over-allocation**  --  preallocate only what's needed; reserving excess wastes memory and can hurt cache utilization and GC throughput. Validate hints with benchmarks.
- **Incremental building**  --  for strings/buffers built piece-by-piece, use a linear-time builder (amortized append) rather than repeated concatenation (quadratic in pieces).

## Concurrency

- **Worker pools**  --  when tasks are small or resources bounded, use a fixed pool fed by a queue rather than spawning a context per task.
- **Atomics**  --  for simple shared counters/flags, use hardware atomics; prefer lock-free only when contention stays low.
- **Lazy initialization**  --  defer expensive setup to first use, guarded by once-only synchronization; reduces startup time and unused work.
- **Cancellation propagation**  --  thread cancellation/timeout context through every child operation; check at natural abort points and on blocking calls.
- **Structured error collection**  --  for related concurrent operations, group with shared cancellation and propagate only the first meaningful error; avoid accumulating all errors unless callers need them.
- **Directional channels**  --  specify data-flow direction (send-only vs receive-only) so the compiler enforces ownership and prevents accidental misuse.

## I/O

- **Buffering**  --  wrap unbuffered file/network I/O with buffered readers/writers (typically 4-64 KB) to coalesce syscalls and amortize fixed cost.
- **Batching**  --  accumulate small operations up to a size or time threshold, then submit as one batch; design for partial success and back-pressure.
- **Direct streaming**  --  write formatted output directly to the destination writer/stream instead of constructing an intermediate string/buffer to pass downstream.
- **Guarded observability**  --  wrap expensive log/tracing argument computation in an enabled-check to avoid computing values never emitted; prefer lazy evaluation for verbose/debug output.

## SIMD & Vectorization

- **Auto-vectorization first**  --  prefer compiler auto-vectorization: keep data contiguous and aligned (struct-of-arrays, not array-of-structs), branch-free, and loop-independent so the compiler can widen it.
- **Portable SIMD / intrinsics**  --  drop to explicit SIMD only when auto-vectorization measurably fails on a proven hot loop; verify the vectorized path produces identical results.
- **Data layout**  --  favor struct-of-arrays over array-of-structs for SIMD-friendly access patterns; align buffers to vector width (16/32/64 bytes) when targeting explicit SIMD.
- **Branch elimination**  --  replace branches with conditional moves, masks, or predication in hot loops; branches inside SIMD lanes serialize execution.
- **Measure the vectorized path**  --  compare scalar vs vectorized on realistic data; gains depend on data size, alignment, and the target ISA. No SIMD lands without a benchmark.

## Compiler

- **Build flags**  --  enable release/production modes (inlining, escape analysis, dead-code elimination); consider profile-guided optimization for hot code.
- **Escape analysis**  --  minimize heap escapes by passing small structs by value, keeping method receivers on structs without pointer indirection when possible, and avoiding interface wrapping in hot paths.