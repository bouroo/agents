---
description: Refactor phase — analyze, plan, baseline, execute, and verify with tests
---

# Refactor Phase

A language-agnostic refactoring workflow that integrates architectural principles and performance patterns. Apply these after correctness is proven; measure before and after; keep only what the data supports.

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

Write a REASONS canvas. Lock scope explicitly.

- **R**equirements — problem statement, definition of done, acceptance criteria.
- **E**ntities — domain objects and their relationships.
- **A**pproach — strategy and alternatives considered; reject those not chosen with rationale.
- **S**tructure — components, dependencies, interfaces affected.
- **O**perations — concrete, testable implementation steps in dependency order.
- **N**orms — naming conventions, patterns, and coding standards to apply.
- **S**afeguards — non-negotiable constraints (invariants, performance budgets, security rules).

Mark unknowns explicitly; do not gloss them over. Tests and benchmarks are part of the plan, not an afterthought.

---

## 3. Baseline

Before touching production code, capture or write tests and benchmarks for the target area. The baseline must prove current behavior and, if performance is a goal, current metrics. No refactor proceeds without a reproducible before/after comparison.

- Write tests that read as sentences about behavior. Cover happy path, error path, and edge cases.
- Add integration tests for end-to-end flows.
- Record benchmark numbers: latency percentiles, throughput, allocation count, heap size.
- Commit the baseline. Every subsequent change must be measured against it.

---

## 4. Execute

Make small, atomic commits. Keep the build green at every step. Preserve public behavior. Apply these principles in order; when they conflict, clarity wins over concision, simplicity over concision, and maintainability over consistency.

### Architecture

- **Write libraries, not monoliths.** Keep entry points minimal — parse, handle errors, delegate. Domain logic returns data, not side effects; returns errors, never crashes. Only the entry point reads env vars, CLI args, or filesystem paths; business logic stays pure.
- **Code for reading.** Name length scales with scope: short for locals (`i`, `buf`, `err`), longer at package level. Avoid `get`/`Get` prefixes; start with the noun. Extract low-level paperwork into well-named helpers. Comments explain *why*, not *what*.
- **Decouple from environment.** Embed static assets; stream or chunk large data; reuse buffers. Do not assume specific paths, writable disk, or environment variables exist.

### Safety

- **Safe by default.** Make invalid states unrepresentable. Provide useful zero values or validating constructors. Use named constants instead of magic values. Apply least-privilege to capabilities and permissions.
- **Wrap errors, don't flatten.** Define sentinel errors; wrap with context while preserving the cause chain so identity checks still work. Never inspect error strings to identify error types. Add context only when it conveys new information.
- **Design for errors.** Check every error. Handle where possible, retry transient failures, propagate the rest. Handle errors before continuing with normal flow — indent error paths, keep the happy path unindented. Show usage hints for invalid input. Reserve fatal exits for unrecoverable internal failures.

### State & Concurrency

- **Avoid mutable global state.** Inject dependencies explicitly. If shared mutable state is unavoidable, guard with synchronization or isolate behind a single owner with message passing.
- **Concurrency sparingly.** Introduce concurrency only when required. Confine concurrent tasks to the creating scope; every spawned task must terminate before its parent exits. Use structured concurrency primitives. A sequential solution is usually cheaper to read, test, and debug than a parallel one. Use worker pools fed by queues rather than spawning a task per item. For simple shared counters and flags, prefer atomics over locks.

### Performance — Memory

*Apply only after correctness is proven. Measure before and after; keep only proven improvements.*

- **Preallocate** collections when final size is known or deterministic to avoid repeated reallocation and copying.
- **Pool reusable objects** in hot paths; tune pool size against footprint and contention. Avoid over-allocation — reserving excess capacity wastes memory and hurts cache utilization.
- **Order struct fields largest → smallest** (64-bit → 8-bit) to minimize padding and improve cache locality.
- **Avoid boxing** in hot loops — use concrete types over interface-wrapped or erased generics; pass small structs by value.
- **Prefer zero-copy** — pass references, slices, and views instead of duplicating large buffers.
- **Keep short-lived values on the stack** — avoid pointers-to-locals, large closure captures, and unintended heap escapes.
- **Share immutable data** across workers without locks; construct fully before publishing, never mutate after.
- **Use linear-time builders** (amortized append) for incremental string/buffer construction rather than repeated concatenation.

### Performance — I/O

- **Buffer all I/O** — wrap unbuffered file or network streams with buffered readers/writers (typically 4–64 KB) to coalesce syscalls.
- **Batch small operations** — accumulate up to a size or time threshold, then submit as one batch. Design for partial success and back-pressure.
- **Stream directly** — write formatted output straight to the destination writer/stream, not via intermediate strings or buffers.
- **Guard expensive log/tracing argument computation** with an enabled-check to avoid computing values that are never emitted.

### Performance — Compiler & Build

- **Enable release optimization flags** — inlining, escape analysis, dead-code elimination. Consider profile-guided optimization for hot code.
- **Minimize heap escapes** — pass small structs by value; avoid interface wrapping in hot paths; keep method receivers on structs without unnecessary pointer indirection.

### Observability

- **Log only actionable information.** Structured fields, never secrets. Use tracing for request-scoped debugging and metrics for performance — not logs.

---

## 5. Verify

Run formatter, linter, type-checker, and full test suite. Re-profile and re-benchmark against the baseline to confirm improvement, not regression. If any metric regresses, revert and re-plan. Do not ship a refactor that trades correctness or performance for aesthetics.

---

## 6. Sync Spec

Update or create the spec to match the refactor; never leave the spec describing the old shape. When code and spec diverge, fix the spec first, then the code. A stale spec is a bug.
