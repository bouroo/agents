---
name: performance-patterns
description: Patterns for writing high-performance software across any language. Covers memory management, concurrency, I/O efficiency, and compiler optimizations. Use when optimizing for speed, throughput, latency, or memory usage.
---

# Performance Patterns

## Memory Management & Efficiency

### Object Pooling

Reuse allocated objects instead of creating new ones repeatedly to reduce allocation overhead and garbage collection pressure.

**When to use:** Frequently created and destroyed objects that are expensive to allocate, especially in hot paths or high-throughput scenarios.

**How:** Maintain a pool of pre-allocated objects. Check out from the pool when needed, return to the pool when done. Balance pool size against memory footprint.

---

### Memory Preallocation

Reserve capacity for collections upfront rather than allowing them to grow incrementally through reallocation.

**When to use:** Collections (lists, maps, arrays) where the approximate size is known in advance, or where growth is deterministic.

**How:** Initialize collections with expected capacity. Avoid repeated reallocation and copying as the collection grows.

---

### Struct Field Alignment

Order struct fields by size (largest to smallest) to minimize padding and improve memory density.

**When to use:** Large data structures that are created frequently or accessed with poor cache locality.

**How:** Place 64-bit fields first, then 32-bit, then 16-bit, then 8-bit. Padding is inserted automatically when sizes mismatch. Profile memory layout impact before optimizing.

---

### Avoiding Type Boxing

Prevent hidden allocations from converting value types to interface types or generic type erasures.

**When to use:** Performance-critical code paths where interface conversions or type erasure occurs frequently.

**How:** Use concrete types where possible. Avoid passing value types to interface-typed parameters unnecessarily. Be aware of language-specific boxing costs.

---

### Zero-Copy Techniques

Minimize data copying by passing references, reusing buffers, and slicing over views instead of duplicating data.

**When to use:** Large data structures, high-throughput data pipelines, or any scenario where copying overhead is significant.

**How:** Pass by reference instead of by value. Reuse buffers across operations. Use slicing or view operations instead of copying full data.

---

### GC Efficiency

Reduce work for the garbage collector by minimizing heap allocations, reusing memory, and preferring value types over heap-allocated types.

**When to use:** Applications with strict latency requirements or high allocation rates that trigger frequent GC cycles.

**How:** Stack-allocate when possible. Reuse objects. Avoid allocations in hot paths. Use arena allocators or object pools for batched workloads.

---

### Stack Allocations

Keep short-lived objects on the stack rather than allowing them to escape to the heap by managing lifetimes carefully.

**When to use:** Performance-critical code where heap allocation and subsequent GC cleanup creates measurable overhead.

**How:** Avoid returning pointers to local variables. Be cautious with closures that capture large objects. Pass values explicitly rather than letting the compiler decide.

---

## Concurrency and Synchronization

### Worker Pools

Limit concurrent operations to a fixed number of workers rather than creating a new execution context per task.

**When to use:** Bounded resources (connections, memory, CPU cores), tasks with high creation overhead, or protecting against thread/execution context explosion.

**How:** Create a fixed pool of workers at startup. Feed them work through a task queue. Reuse workers across tasks rather than spawning per-task.

---

### Atomic Operations

Use hardware atomic operations for shared counters and flags instead of locks to avoid serialization overhead.

**When to use:** Simple shared state like counters, flags, or statistics that do not require complex updates.

**How:** Use atomic primitives provided by the language runtime. Prefer lock-free algorithms when contention is expected to be low.

---

### Lazy Initialization

Defer expensive initialization until the resource is first accessed rather than initializing eagerly at startup.

**When to use:** Expensive resources that may not be needed, or to reduce startup time by deferring non-critical setup.

**How:** Check before initializing. Use synchronization to ensure initialization happens exactly once in concurrent scenarios (e.g., once-per-process flags).

---

### Immutable Data Sharing

Share data between concurrent tasks by making it immutable, eliminating the need for synchronization.

**When to use:** Read-heavy workloads, data that is computed once and read many times, or scenarios where locks create contention.

**How:** Construct data fully before sharing. Do not mutate after sharing. Language features like const, final, or functional data structures support this.

---

### Efficient Cancellation Propagation

Propagate cancellation signals and timeouts across concurrent operations so work stops promptly when no longer needed.

**When to use:** Long-running or blocking concurrent operations, services with latency bounds, or preventing resource leaks from abandoned operations.

**How:** Check cancellation state at natural abort points. Propagate cancellation context to child operations. Ensure goroutines, threads, or tasks respect termination signals.

---

## I/O Optimization and Throughput

### Efficient Buffering

Wrap unbuffered I/O with buffering layers to reduce the number of system calls by coalescing reads and writes.

**When to use:** File I/O, network I/O, or any streaming where syscall overhead dominates, especially with small read/write sizes.

**How:** Use buffered readers and writers. Size buffers appropriately (typically 4KB–64KB depending on workload). Avoid flushing prematurely.

---

### Batching Operations

Combine multiple small operations into a single batch to amortize per-request overhead and improve throughput.

**When to use:** High-latency operations like network calls, database queries, or I/O where per-operation fixed costs dominate.

**How:** Collect operations in a buffer up to a threshold or timeout. Submit as a single batch. Handle partial success gracefully.

---

## Compiler-Level Optimization

### Build-Time Optimization Flags

Enable compiler optimization flags that improve runtime performance through inlining, escape analysis, and dead code elimination.

**When to use:** Production builds where performance matters; especially for hot code paths identified through profiling.

**How:** Enable release/production build modes that enable inlining and optimizations. Use profile-guided optimization when available. Test that optimizations do not break correctness.
