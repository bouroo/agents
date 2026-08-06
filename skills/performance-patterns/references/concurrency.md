# Concurrency Patterns

> Load on demand when the profiler shows lock contention, unbounded fan-out, or leaked background work. The decision tree lives in [performance-patterns](../SKILL.md).

- **Worker pools** -- use a fixed pool fed by a queue instead of spawning unmanaged threads/tasks per request. Unbounded tasks exhaust memory under load.
- **Bounded concurrency** -- cap parallelism explicitly (semaphores, tickets, rate limiters) to prevent unbounded fan-out from overwhelming downstreams or memory.
- **Atomics** -- use hardware atomics for simple counters and flags; prefer lock-free designs only when contention is low. Under heavy contention a mutex is often simpler and as fast.
- **Lazy initialization** -- defer expensive setup until first use, behind thread-safe once-only synchronization, so cold paths pay nothing.
- **Cancellation propagation** -- thread cancellation tokens and timeouts through every child operation; a missing token leaks background workers that outlive the request.
- **Structured error collection** -- group related concurrent work with shared cancellation and propagate the first meaningful error; do not let one failure strand the others.
- **Bounded queues** -- use explicit capacity limits on channels/queues so backpressure signals upstream producers to slow down. An unbounded queue turns a load spike into an OOM.

Resilience under load (circuit breakers, active load shedding, degradation) is enforced at I/O and service boundaries, so it lives in [I/O & resilience](./io-resilience.md). The bounded queues above produce the backpressure those patterns rely on.

## Source

Confirm a concurrency change helped via [Measurement methodology](./measurement.md); lock behavior under contention is notoriously counterintuitive.
