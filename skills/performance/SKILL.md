---
name: performance
description: Language-agnostic performance optimization patterns for reducing latency, improving memory efficiency, and maximizing throughput.
---

# Performance Optimization Patterns

## Memory Management

- **Preallocation**: Allocate collections with known capacities upfront
- **Object Pooling**: Reuse frequently allocated/deallocated objects
- **Data Alignment**: Organize fields to minimize padding and improve cache locality
- **Zero-Copy**: Minimize data copying using views, buffers, or sharing
- **Stack over Heap**: Keep short-lived values on the stack when possible

## Concurrency

- **Worker Pools**: Fixed-size pools to prevent resource exhaustion
- **Lock-Free**: Atomic operations for simple shared state
- **Batching**: Group operations to amortize overhead
- **Sharding**: Partition data by key to reduce contention

## I/O & Network

- **Connection Pooling**: Reuse connections per request
- **Streaming**: Process data in chunks, not entire payloads
- **Caching**: Computed results with explicit invalidation. Cache-aside pattern
- **Lazy Loading**: Defer expensive computations until needed

## Measurement

- Benchmark before optimizing. Measure before and after each change.
- Profile hot paths to identify actual bottlenecks.
- Load test with production-like volumes and concurrency.
- Track regressions with baselines and alerts.

## Anti-patterns

- Premature optimization without measurement
- Optimizing code outside hot paths
- Adding caches without eviction policies
- Complex lock hierarchies causing deadlocks
