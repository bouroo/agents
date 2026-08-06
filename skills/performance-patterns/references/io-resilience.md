# I/O & Resilience Patterns

> Load on demand when the profiler shows I/O wait, transport overhead, or repeated expensive work. The decision tree lives in [performance-patterns](../SKILL.md).

## I/O Patterns

- **Buffering** -- wrap unbuffered I/O streams with 4-64 KB buffers to coalesce system calls. A syscall per byte is a common throughput killer.
- **Batching** -- accumulate work to a size or time threshold; design for partial success and backpressure so a failed batch does not lose the unfailed items.
- **Direct streaming** -- write formatted output directly to the destination writer instead of building an intermediate in-memory buffer.
- **Tune transport defaults** -- default HTTP clients and DB drivers ship with low idle-connection limits; size them to match expected concurrency. An untuned default caps throughput silently.
- **Choose transport by workload** -- raw TCP or custom framing for lowest latency; HTTP/2 or HTTP/3 for multiplexed request/response with flow control; an IDL-based RPC layer for cross-language contracts.
- **No panic/exceptions in hot paths** -- stack unwinding and exception-object creation cost real cycles; return explicit errors or status codes.

## Networking

- **DNS** -- cache resolution results, pre-resolve known hosts, and use an async/native resolver. Off-CPU time in the resolver shows up under high load.
- **TLS** -- enable session resumption, ALPN, and fast cipher suites; handshake spans dominate connection-heavy workloads.
- **Connection reuse** -- use keep-alive, SO_REUSEADDR, and connection pooling to avoid TIME_WAIT storms from short-lived connections.

## Caching (avoid repeated work)

- **Memoization** -- cache the result of a pure computation keyed by its inputs; invalidate on input change.
- **Single-flight** -- coalesce concurrent identical requests into one in-flight call; return the shared result to all waiters.
- **Work avoidance** -- the fastest computation is the one you skip. Reorder checks so the cheap, discriminating test runs first.

## Observability hygiene

- **Guarded logging** -- wrap expensive log/trace string computation in an enabled-check; logging calls in hot loops allocate even when the level is disabled.
- **Sample tracing at the edge** -- per-request span creation allocates and shows up in profiles under high load; use head-based sampling.

## Resilience Under Load

- **Circuit breakers** -- open after N consecutive failures or a latency-threshold breach; shed calls until a probe succeeds. Prevents cascading failure through a sick dependency.
- **Active load shedding** -- reject work at the edge when in-flight count or queue depth exceeds a measured threshold; cheaper than accepting work and discarding it after processing.
- **Backpressure signaling** -- bounded queue depth signals upstream producers to slow down; never buffer unbounded input silently.
- **Degradation over failure** -- return partial, cached, or stale responses when capacity is exhausted, if the domain allows it. A stale answer often beats a timeout.

## Source

[Concurrency](./concurrency.md) provides the bounded queues that make backpressure enforceable. Confirm each change via [Measurement methodology](./measurement.md).
