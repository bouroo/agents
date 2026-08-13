# Common Performance Pitfalls

> Load on demand as a final checklist. The decision tree lives in [performance-patterns](../SKILL.md).

| Mistake | Fix |
|---|---|
| Optimizing without profiling | Profile first; intuition is wrong ~80% of the time |
| Default HTTP/DB client without transport tuning | Defaults cap idle connections at low numbers; size to concurrency |
| Logging in hot loops | Guard log evaluation with an enabled-check or lazy attributes |
| Exceptions/panics as control flow in hot path | Stack unwinding allocates; use explicit error returns |
| Dynamic reflection / deep equality in production | 50-200x slower than typed comparison; use typed equality |
| No memory limit in containers | Set runtime allocation/GC limit to 80-90% of container memory |
| Unsafe / pointer tricks without benchmark proof | Justified only when profiling shows >10% improvement in a verified hot path |
| Preallocating speculatively | Preallocate only when capacity is known with executable evidence |
| One big benchmark touching everything | Isolate one function per benchmark; contaminated results mislead |

## Cross-cutting checks

- Did you measure before **and** after? A change without a comparison is not evidence.
- Did you change one thing at a time? Confounded changes hide which edit helped or hurt.
- Did you rule out an external bottleneck (DB, upstream, I/O) before tuning code?
- Did you document *why* a non-obvious optimization is faster, so cleanup does not regress it?

## Source

See [Measurement methodology](./measurement.md) for the discipline that prevents these mistakes.
