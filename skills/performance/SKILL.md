---
name: performance
description: Language-agnostic performance optimization patterns for reducing latency, improving memory efficiency, and maximizing throughput.
---

# Performance Optimization Patterns

## 1. Memory Management & Efficiency

- **Memory Preallocation**: Allocate collections with known capacities upfront to avoid dynamic resizing.
- **Object Pooling**: Reuse frequently allocated/deallocated objects to reduce allocation pressure.
- **Data Structure Alignment**: Organize fields to minimize padding and improve CPU cache locality.
- **Avoid Abstraction Overhead**: Prevent hidden allocations from dynamic dispatch, interface boxing, or type casting in hot paths.
- **Zero-Copy Techniques**: Minimize data copying using views, buffers, or sharing between layers.
- **Stack over Heap**: Keep short-lived values on the stack when the language supports it.

## 2. Concurrency & Synchronization

- **Worker Pools**: Control concurrency with fixed-size pools to prevent resource exhaustion.
- **Lock-Free Patterns**: Use atomic operations for simple shared state instead of heavy locking.
- **Batching**: Group operations to amortize overhead (network round-trips, disk I/O, lock acquisition).
- **Sharding**: Partition data by key to reduce contention on shared resources.
- **Read-Write Locks**: Allow concurrent reads when writes are infrequent.

## 3. I/O & Network

- **Connection Pooling**: Reuse connections rather than creating new ones per request.
- **Streaming**: Process data in chunks rather than loading entire payloads into memory.
- **Compression**: Compress large payloads for network transfer; skip for small or already-compressed data.
- **Caching**: Cache computed results with explicit invalidation. Prefer cache-aside pattern.
- **Lazy Loading**: Defer expensive computations until their results are actually needed.

## 4. Algorithmic Efficiency

- **Appropriate Data Structures**: Hash maps for lookups, sorted structures for range queries, graphs for relationships.
- **Early Termination**: Break loops and pipelines as soon as the answer is known.
- **Memoization**: Cache results of pure functions to avoid recomputation.
- **Indexing**: Add indexes for frequent query patterns; measure before and after.

## 5. Measurement & Profiling

- **Benchmark before optimizing**: Measure actual performance before and after each change.
- **Profile hot paths**: Use profiling tools to identify actual bottlenecks, not assumed ones.
- **Load test realistically**: Test with production-like data volumes and concurrency.
- **Track regressions**: Establish baselines and alert on degradation.

## Anti-patterns

- Premature optimization without measurement
- Optimizing code that isn't in a hot path
- Adding caches without eviction policies
- Complex lock hierarchies that cause deadlocks
- Guessing at bottlenecks instead of profiling
