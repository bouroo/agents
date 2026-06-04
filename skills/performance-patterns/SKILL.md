---
name: performance-patterns
description: >
  Patterns for high-performance software across any language. Covers memory, concurrency, I/O, and compiler
  optimizations. Use when optimizing for speed, throughput, latency, or memory. Grounded in goperf.dev and Google's Go best-practices.
---

# Performance Patterns

Apply these only after correctness is proven. Measure before and after; keep what the data supports.

## Memory

- **Object pooling** — when objects are allocated and destroyed in tight loops or hot paths, reuse via a checkout/return pool; tune size against footprint and contention.
- **Preallocation** — when a collection's final size is known or deterministic, reserve capacity up front to avoid repeated reallocation and copying.
- **Field alignment** — when structs are large or allocated frequently, order fields largest → smallest (64 → 8 bit) to minimize padding and improve cache locality.
- **Avoid boxing** — in hot loops, use concrete types over interface/erased generics; pass value types by value to prevent hidden heap allocations.
- **Zero-copy** — for large data or high-throughput pipelines, pass references, reuse buffers, and slice over views instead of duplicating.
- **Stack allocation** — keep short-lived values on the stack by avoiding pointers-to-locals, large closure captures, and unintended escape.
- **Immutability for sharing** — share read-only data across workers without locks; construct fully before publishing, never mutate after.
- **Over-allocation** — preallocate only what is needed; reserving excess capacity wastes memory and can hurt cache utilization and GC throughput. Validate hints with benchmarks.
- **Incremental building** — when constructing strings or buffers piece-by-piece, use a linear-time builder (amortized append) rather than repeated concatenation, which is quadratic in the number of pieces.

## Concurrency

- **Worker pools** — when tasks are small or resources are bounded, use a fixed pool fed by a queue rather than spawning a context per task.
- **Atomics** — for simple shared counters and flags, use hardware atomics; prefer lock-free only when contention stays low.
- **Lazy initialization** — defer expensive setup to first use, guarded by once-only synchronization; reduces startup time and unused work.
- **Cancellation propagation** — thread cancellation/timeout context through every child operation; check at natural abort points and on blocking calls.
- **Structured error collection** — when running related operations concurrently, group them with shared cancellation and propagate only the first meaningful error; avoid accumulating all errors unless callers need them.
- **Directional channels** — specify data-flow direction on channels, pipes, or queues (send-only vs receive-only) to let the compiler enforce ownership and prevent accidental misuse.

## I/O

- **Buffering** — wrap unbuffered file or network I/O with buffered readers/writers (typically 4–64 KB) to coalesce syscalls and amortize fixed cost.
- **Batching** — accumulate small operations up to a size or time threshold, then submit as one batch; design for partial success and back-pressure.
- **Direct streaming** — write formatted output directly to the destination writer/stream rather than constructing an intermediate string or buffer just to pass it downstream.
- **Guarded observability** — wrap expensive log/tracing argument computation in an enabled-check to avoid computing values that will never be emitted; prefer lazy evaluation for verbose or debug-level output.

## Compiler

- **Build flags** — enable release/production modes (inlining, escape analysis, dead-code elimination) and consider profile-guided optimization for hot code.
- **Escape analysis** — minimize heap escapes by passing small structs by value, keeping method receivers on structs without pointer indirection when possible, and avoiding interface wrapping in hot paths.
