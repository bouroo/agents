---
name: performance
description: Language-agnostic performance optimization patterns for reducing latency, improving memory efficiency, and maximizing throughput.
version: 1.0.0
triggers:
  - performance optimization
  - latency reduction
  - memory efficiency
  - throughput improvement
---

# Performance

Language-agnostic patterns for writing performant code.

## Memory

### Pre-allocation
Allocate slices, maps, and buffers with known or estimated capacity upfront to avoid costly resizes and copies.

### Object Reuse
Reuse buffers and objects via pools or recycling to reduce allocation pressure and GC overhead.

### Efficient Layout
Group struct/object fields by size (largest first) to minimize padding. Keep hot data together for cache locality.

### Zero-Copy
Minimize data copying. Use slicing, references, or views instead of creating new copies.

## Concurrency

### Worker Pools
Control concurrency with fixed-size worker pools. Unbounded goroutine/thread creation exhausts resources.

### Immutable Sharing
Share data between threads/goroutines without locks by making it immutable. Copy-on-write for mutation.

### Batching
Combine multiple small operations into batches to reduce round trips, system calls, and overhead.

## I/O

### Buffered I/O
Use buffered readers/writers to minimize system calls. Process data in chunks, not byte-by-byte.

### Lazy Loading
Defer expensive initialization until actually needed. Load data on first access, not at startup.

## Rules

- **Profile before optimizing.** Measure before and after. Never optimize blind.
- **Benchmark the hot path.** Use the language's benchmarking tools.
- **Optimize the algorithm first.** A better algorithm beats micro-optimizations.
- **Don't sacrifice readability.** Performance hacks need comments explaining why.

## Checklist

- [ ] Profiled to identify actual bottleneck
- [ ] Measured baseline before optimization
- [ ] Pre-allocated where size is known
- [ ] Buffered I/O for hot paths
- [ ] Batched small operations
- [ ] Measured after optimization
