---
name: go-performance
description: Use when optimizing Go code for memory, CPU, or throughput.
---

# Go Performance Patterns

## Memory
- **Preallocate** — Allocate slices/maps with capacity when size is known
- **Object pooling** — Reuse objects with `sync.Pool` to reduce GC pressure
- **Struct alignment** — Order fields by size (8, 4, 2, 1 bytes) to minimize padding
- **Escape analysis** — Keep values on stack via inlining; avoid interface boxing

## Concurrency
- **Worker pools** — Fixed-size goroutine pools to cap resource usage
- **Atomic operations** — Use `sync/atomic` for simple shared counters
- **sync.Once** — Lazy initialization for expensive setup
- **Immutable data** — Share data safely between goroutines without locks

## I/O
- **Buffering** — Use `bufio.Reader/Writer` for buffered I/O
- **Batching** — Combine small operations to reduce round-trips

## Context
- Propagate timeouts/cancellations via `context.Context`
- Short-lived contexts prevent goroutine leaks

## Build
- Use `-gcflags` and `-ldflags` for compiler optimization tuning
