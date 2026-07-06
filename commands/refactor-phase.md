---
description: Refactor phase — analyze, plan, baseline, execute, and verify with tests
---

# Refactor Phase

A language-agnostic refactoring workflow. Apply engineering norms and performance patterns **after** correctness is proven; measure before and after; keep only what the data supports.

> **Agent:** requires `edit` + `bash` — run on the implementing/build agent, not `plan` or `conductor`.

Target area (optional): **$ARGUMENTS**. If empty, ask the user which module/package/path to target before analyzing.

---

## 1. Analyze

Map the target area, its dependencies, and call sites. Identify the smell, not just the symptom.

**Structural smells:**
- Mutable global state — package-level variables mutated from multiple call sites.
- Tight coupling to environment — env vars, CLI args, or filesystem paths accessed deep in domain packages instead of the entry point.
- Monolithic entry points — `main` doing real work instead of parsing, delegating, and handling errors.
- Side-effecting domain logic — functions that print, exit, or mutate external state instead of returning data and errors.

**Performance smells:**
- Unnecessary allocations — repeated allocation/destruction of objects in hot loops (should pool or reuse).
- Missing preallocation — collections grown incrementally when final size is known or estimable.
- Excessive copying — large buffers or structs passed by value when a reference, slice, or view would suffice.
- Unbuffered I/O — raw file or network reads/writes without buffering (typically 4–64 KB).
- Small frequent operations — per-element syscalls, DB queries, or network round trips that should be batched.
- Heap escapes — short-lived values that escape to the heap due to pointers-to-locals, interface boxing, or large closure captures.
- Suboptimal data layout — struct fields not ordered largest-to-smallest, causing padding waste.
- N+1 patterns — sequential I/O or DB calls inside loops instead of bulk/batched operations.

**Correctness smells:**
- Unchecked errors — discarded return values, ignored error channels, or `_` assignments.
- In-band errors — sentinel values like `-1`, `null`, or empty string used instead of explicit error returns.
- Error string inspection — comparing error messages with `==` or `contains` instead of typed/sentinel error matching.
- Missing cancellation propagation — concurrent tasks spawned without timeout or cancellation context.

Run CPU, memory, and I/O profilers. Identify the top contributors. Record heap profiles and allocation counts. These measurements form the basis for all subsequent decisions.

---

## 2. Plan

Write a REASONS canvas — see `AGENTS.md` §4. Lock scope explicitly. Mark unknowns; tests and benchmarks are part of the plan, not an afterthought.

---

## 3. Baseline

Before touching production code, capture or write tests and benchmarks for the target area. The baseline must prove current behavior and, if performance is a goal, current metrics. No refactor proceeds without a reproducible before/after comparison.

- Write tests that read as sentences about behavior. Cover happy path, error path, and edge cases.
- Add integration tests for end-to-end flows.
- Record benchmark numbers: latency percentiles, throughput, allocation count, heap size.
- Commit the baseline. Every subsequent change must be measured against it.

---

## 4. Execute

Make small, atomic commits. Keep the build green at every step. Preserve public behavior. When principles conflict, clarity wins over concision, simplicity over concision, and maintainability over consistency.

Apply engineering norms — see `AGENTS.md` §5 and `skills/effective-code-craft` (Architecture: libraries not monoliths, code for reading, decouple from environment; Safety: safe by default, wrap errors with context, design for errors; State & Concurrency: avoid mutable globals, use concurrency sparingly, prefer worker pools, prefer atomics for simple counters; Observability: actionable structured logs, tracing for request debugging, metrics for performance).

Apply performance patterns — see `AGENTS.md` §6 and `skills/performance-patterns`. **Apply only after correctness is proven; measure before/after; revert regressions.** Covers memory (preallocate, pool, order fields, avoid boxing, prefer zero-copy, keep on stack, share immutable, linear-time builders), I/O (buffer, batch, stream direct, guard expensive log/tracing args), and compiler/build (release flags, PGO for hot code, minimize escapes).

---

## 5. Verify

Run formatter, linter, type-checker, and full test suite. Re-profile and re-benchmark against the baseline to confirm improvement, not regression. If any metric regresses, revert and re-plan. Do not ship a refactor that trades correctness or performance for aesthetics.

---

## 6. Sync Spec

Update or create the spec to match the refactor; never leave the spec describing the old shape. When code and spec diverge, fix the spec first, then the code. A stale spec is a bug.
