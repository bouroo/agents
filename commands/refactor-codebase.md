---
description: Structured refactoring — analyze, plan, execute, and verify with tests
---

# Refactor Codebase

1. **Analyze** — map the target area, dependencies, and call sites. Identify the smell, not just the symptom. Check for mutable global state, tight coupling to environment (env vars, CLI args, filesystem paths deep in packages), and missing error handling.

2. **Plan** — write a REASONS canvas (Requirements, Approach, Operations, Safeguards). Lock scope: what we will do, what we will not, what remains open. Tests and benchmarks are part of the plan, not an afterthought.

3. **Baseline** — before touching production code, capture or write tests and benchmarks for the target area. The baseline must prove current behavior and, if performance is a goal, current metrics. No refactor proceeds without a reproducible before/after comparison.

4. **Execute** — make small, atomic commits; keep the build green at every step; preserve public behavior.
   - **Write packages, not monoliths.** Keep entry points minimal (parse, handle errors, delegate). Domain logic returns data, not side effects; returns errors, never crashes.
   - **Code for reading.** Use consistent idiomatic naming; keep functions short; extract low-level "paperwork" into well-named helpers.
   - **Safe by default.** Make invalid states unrepresentable; use validating constructors and named constants instead of magic values. Apply least-privilege to capabilities.
   - **Wrap errors, don't flatten.** Define sentinel errors; wrap with context while preserving the chain so identity checks still work. Never inspect error strings to identify types.
   - **Avoid mutable global state.** Inject dependencies explicitly. If shared mutable state is unavoidable, guard with synchronization or isolate behind a single owner.
   - **Concurrency sparingly.** Introduce concurrency only when required. Confine it to the creating scope; every concurrent task must terminate before its parent exits. Use structured primitives.
   - **Decouple from environment.** Only the entry point reads env vars, CLI args, or filesystem paths. Stream or chunk large data; reuse buffers.
   - **Design for errors.** Check every error. Handle where possible, retry transient failures, propagate the rest. Show usage hints for invalid input.
   - **Optimize deliberately, after correctness.** Preallocate collections when size is known; reuse objects in hot paths; buffer I/O; batch small operations; apply zero-copy and field-alignment where data supports it. Measure before and after; keep only proven improvements.
   - **Log only actionable information.** Structured fields, never secrets. Use tracing for request debugging and metrics for performance, not logs.

5. **Verify** — run formatter, linter, type-checker, and full test suite. Re-profile against the baseline to confirm improvement, not regression.

6. **Sync spec** — update or create the spec to match the refactor; never leave the spec describing the old shape.
