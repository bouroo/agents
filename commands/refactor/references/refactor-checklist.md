# Refactor Smell Checklist

Catalog of structural, performance, and correctness smells to scan for during the **Analyze** step. These are the top signals; the full sets live in [effective-code-craft](../../../skills/code-craft/SKILL.md) and [performance-patterns](../../../skills/performance-patterns/SKILL.md). Treat a match as a hypothesis to confirm with profiling or tests, not a verdict.

## Structural smells

Symptoms of coupling, hidden state, and misplaced responsibility.

- **Mutable global state** mutated from multiple call sites -- no single owner, so races and ordering bugs follow.
- **Tight coupling to environment** -- env vars, CLI args, or FS paths read deep inside domain packages instead of injected at the boundary.
- **Monolithic entry points** doing real work instead of parsing input, delegating to focused units, and handling errors at the boundary.

Full set: [effective-code-craft](../../../skills/code-craft/SKILL.md) "Structure & Coupling".

## Performance smells

Symptoms of wasted allocation, I/O, or heap growth. Always confirm with a profiler before acting.

- **Unnecessary allocations in hot loops** -- growing slices/maps without preallocation when the final size is known.
- **Unbuffered or chatty I/O** -- per-element syscalls or database queries that should be batched.
- **Heap escapes** -- pointers to locals, interface boxing, or large closure captures that push work onto the GC.

Full patterns: [performance-patterns](../../../skills/performance-patterns/SKILL.md).

## Correctness smells

Symptoms of errors handled unsafely. These violate the Code Craft hard rules -- they are bugs, not style.

- **Unchecked errors** -- discarded returns, unhandled promises, ignored error values or result channels.
- **In-band errors** -- sentinel values like `-1`, `null`, or empty string instead of an explicit error return.
- **Error string inspection** -- comparing messages with equality or substring tests instead of typed or sentinel matching.

Full rules: [effective-code-craft](../../../skills/code-craft/SKILL.md) "Hard Rules".

## Profiling discipline

Record, do not guess. These measurements are the basis for every later decision: which smell is real, what to change, and whether the change helped.

- **CPU profile** -- top functions by self and cumulative time; find the loops that dominate.
- **Memory/heap profile** -- allocation count and bytes per call site; find where GC pressure originates.
- **I/O trace** -- syscall counts, query counts, lock contention; find chatty or blocking paths.
- **Latency** -- record percentiles (p50/p95/p99), not just means, so tail behavior is visible.
