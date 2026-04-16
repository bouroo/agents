---
name: go-performance
description: Language-agnostic performance optimization patterns: memory preallocation, object pooling, struct alignment, zero-copy, buffered I/O, batching, worker pools, atomic ops, lazy init, immutable sharing, context management, escape analysis. Use when optimizing code for performance, reducing latency, or improving memory efficiency.
license: MIT
metadata:
  author: kilo-config
  version: 1.0.0
  source: goperf.dev
---

# Performance Optimization Patterns

Optimize only when necessary. Measure first, then optimize.

## Memory Management & Efficiency

### Object Pooling

Reuse objects to reduce GC pressure and allocation overhead.

- Use sync.Pool for frequently allocated objects
- Pool objects that are expensive to create
- Clear object state before returning to pool
- Don't pool objects with long lifetimes

### Memory Preallocation

Allocate slices and maps with capacity upfront to avoid costly resizes.

- Preallocate slices when size is known: make([]T, 0, capacity)
- Preallocate maps when size is known: make(map[K]V, capacity)
- Avoid repeated append that triggers reallocation
- Use capacity hints for strings.Builder

### Struct Field Alignment

Optimize memory layout to minimize padding and improve locality.

- Group fields by size: largest first (int64, then int32, then int16, then int8)
- Place pointers together, booleans together
- Use struct alignment tools to verify layout
- Consider cache line size (typically 64 bytes) for hot paths

### Avoiding Interface Boxing

Prevent hidden allocations by avoiding unnecessary interface conversions.

- Avoid boxing concrete types into interfaces in hot paths
- Use concrete types when interface isn't needed
- Be aware that method calls on interfaces have small overhead

### Zero-Copy Techniques

Minimize data copying with slicing and buffer tricks.

- Use slice headers to avoid copying: slice[start:end]
- Reuse buffers across operations
- Use bytes.Buffer for efficient string concatenation
- Avoid unnecessary string↔[]byte conversions

### Garbage Collector Efficiency

Reduce GC overhead by minimizing heap usage and reusing memory.

- Minimize heap allocations in hot paths
- Reuse memory via pools or preallocation
- Avoid creating short-lived objects in tight loops
- Monitor GC pause times with runtime metrics

### Stack Allocations and Escape Analysis

Use escape analysis to help values stay on the stack where possible.

- Stack allocation is faster than heap allocation
- Use `go build -gcflags='-m'` to see escape analysis
- Avoid returning pointers to local variables
- Avoid storing pointers in interfaces in hot paths
- Prefer value types over pointer types when size is small

## Concurrency and Synchronization

### Worker Pools

Control concurrency with a fixed-size pool to limit resource usage.

- Use bounded goroutine pools to prevent resource exhaustion
- Size pool based on available resources (CPU, memory, connections)
- Use channels to distribute work to workers
- Ensure workers terminate cleanly on shutdown

### Atomic Operations and Synchronization

Use atomic operations or lightweight locks to manage shared state.

- Use sync/atomic for simple counters and flags
- Prefer atomic over mutex for single-value updates
- Use sync.Mutex for complex state protection
- Use sync.RWMutex when reads vastly outnumber writes
- Minimize critical section duration

### Lazy Initialization

Delay expensive setup logic until it's actually needed.

- Use sync.Once for one-time initialization
- Defer expensive operations until first use
- Cache results of expensive computations
- Use lazy loading for large data structures

### Immutable Data Sharing

Share data safely between goroutines without locks by making it immutable.

- Immutable data requires no synchronization
- Copy-on-write for shared state
- Use immutable data structures for configuration
- Avoid mutating shared data after publication

### Efficient Context Management

Use context to propagate timeouts and cancel signals across goroutines.

- Pass context as first parameter to functions
- Use context.WithTimeout for bounded operations
- Use context.WithCancel for cooperative cancellation
- Check context.Done() in long-running loops
- Don't store context in structs; pass through call chain

## I/O Optimization and Throughput

### Efficient Buffering

Use buffered readers/writers to minimize I/O calls.

- Use bufio.Reader/Writer for small I/O operations
- Buffer size should match typical operation size
- Flush buffers explicitly when done
- Avoid unbuffered I/O in hot paths

### Batching Operations

Combine multiple small operations to reduce round trips and improve throughput.

- Batch database queries when possible
- Batch network requests to reduce latency
- Use bulk operations instead of individual operations
- Size batches based on latency vs throughput tradeoff

## Compiler-Level Optimization

### Compiler Flags

Use build flags for performance tuning.

- -gcflags='-m' for escape analysis
- -ldflags='-s -w' to strip debug info (smaller binaries)
- -gcflags='-l' to disable inlining (debugging)
- Profile before and after to verify improvements

## Performance Workflow

1. **Measure first**: Use profiling to identify bottlenecks
2. **Optimize hot paths**: Focus on code that runs most frequently
3. **Verify improvement**: Benchmark before and after changes
4. **Don't over-optimize**: Readable code > marginal performance gains
5. **Document tradeoffs**: Explain why optimization was necessary

## When to Use

- Profiling reveals performance bottlenecks
- Reducing latency in hot paths
- Improving memory efficiency
- Scaling to handle more concurrent requests
- Reducing GC pressure
- Optimizing I/O throughput

## Anti-Patterns

- Optimizing without measuring
- Premature optimization of cold paths
- Sacrificing readability for marginal gains
- Ignoring algorithmic complexity (O(n²) vs O(n log n))
- Optimizing without verifying improvement
