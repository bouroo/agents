---
name: performance
description: Language-agnostic performance optimization patterns for reducing latency, improving memory efficiency, and maximizing throughput.
---
# Performance Optimization Patterns

Language-agnostic performance optimization patterns for reducing latency, improving memory efficiency, and maximizing throughput.

## 1. Memory Management & Efficiency
- **Memory Preallocation**: Allocate collections with known capacities upfront to avoid costly dynamic resizing and reallocation.
- **Object Pooling**: Reuse frequently allocated and deallocated objects to reduce allocation pressure and memory churn.
- **Data Structure Alignment**: Organize fields within structures to minimize padding and improve CPU cache locality.
- **Avoid Abstraction Overhead**: Prevent hidden allocations by avoiding unnecessary dynamic dispatch, interface boxing, or type casting in performance-critical paths.
- **Zero-Copy Techniques**: Minimize data copying by using views, buffers, or sharing techniques when passing data between layers.
- **Stack vs. Heap semantics**: Keep short-lived values on the stack when the language supports it. Avoid returning references to local variables unnecessarily.

## 2. Concurrency & Synchronization
- **Worker Pools**: Control concurrency levels using a fixed-size pool of workers to prevent resource exhaustion and limit context switching.
- **Atomic Operations**: Use lightweight atomic operations instead of heavy locking mechanisms for simple shared state counters or flags.
- **Lazy Initialization**: Delay expensive setup or resource allocation until the exact moment it is actually needed.
- **Immutable Data Sharing**: Share data safely between concurrent tasks without locks by making data structures immutable.
- **Cancellation Propagation**: Efficiently propagate timeouts and cancellation signals across concurrent workflows to abort early and save resources.

## 3. I/O Optimization & Throughput
- **Efficient Buffering**: Use buffered readers and writers to minimize the frequency of expensive system calls when interacting with files or networks.
- **Batching Operations**: Combine multiple small operations (e.g., database inserts, network requests) into a single batch to reduce round-trip latency.
- **Non-blocking I/O**: Do not block threads on I/O operations; use asynchronous paradigms or non-blocking sockets.

## 4. Build-Level Optimization
- **Optimized Builds**: Leverage release builds and optimization flags (e.g., inlining, link-time optimization) for production environments.
- **Profile-Guided Optimization**: Rely on profiling and benchmarking data before applying optimizations. Do not guess where bottlenecks are.

## 5. Large Project Performance
- **Profile at module boundaries**: Identify cross-module bottlenecks by measuring interface-level latency. A slow module interface can cascade into overall system slowdown.
- **Minimize data transfer**: Reduce the volume of data passed between modules or services. Serialize only what is needed; use pagination for large result sets.
- **Cache at the right layer**: Cache expensive computations or remote lookups at the appropriate layer — close to where the data is consumed, not so deep that cache invalidation becomes complex.
- **Monitor in CI/CD**: Track performance metrics in CI/CD pipelines. Fail builds on regressions beyond defined thresholds.
- **Benchmark against spec safeguards**: When the specification defines performance safeguards (latency limits, throughput requirements), validate against these in CI/CD. Fail builds on safeguard violations.