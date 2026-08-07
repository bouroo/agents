---
description: "Refactor phase (ACT loop): analyze, plan, baseline, execute, verify, and sync a behavior-preserving restructuring with before/after measurement. Use when restructuring existing code for clarity, safety, or performance without changing its observable behavior."
argument-hint: "<module|package|path|file> [--goal=<readability|safety|performance>]"
agent: coder
phase: ACT
---

# Refactor Phase

A behavior-preserving restructuring workflow inside the ACT phase. Measure before and after; keep only what the data supports; apply performance work only after correctness is proven.

> Runs on the **coder** (implementing) agent -- the one with file-edit and shell access -- not the conductor (orchestrator) or discover agent.

## When to use

Restructure existing code that is correct but unclear, unsafe, or slow, without changing its observable behavior. Not for new features, behavior-changing bug fixes, or trivial reformatting.

## Inputs

- **$ARGUMENTS** -- target area (module, package, path, or file). If empty, ask the user which area to target before analyzing; do not guess.
- **Options** (ride inside `$ARGUMENTS`, any order, `key=value`):
  - `--goal=<readability|safety|performance>` -- what the refactor optimizes for. Default: behavior-preserving, data-driven (improve what measurement finds, change nothing observable).
- Parsing `$ARGUMENTS` is this command's job -- the host only forwards the string. See [command inputs](../skills/harness-engineering/references/agent-computer-interface.md).

## Steps

1. **Analyze.** Map the target area, its dependencies, and call sites. Identify the smell, not the symptom. Run CPU, memory, and I/O profilers; record heap profiles and allocation counts for the top contributors. Catalog smells via [refactor-checklist](cmd-refactor/references/refactor-checklist.md).

2. **Plan.** Write a REASONS canvas (see [spec-driven-development](../skills/spec-driven-development/SKILL.md)). Lock scope explicitly; mark unknowns. If `$ARGUMENTS` set `--goal`, let that goal weigh the plan (e.g. `performance` justifies profiler-driven targets, `safety` justifies error-path hardening) -- never to relax the behavior-preserving constraint. Tests and benchmarks are part of the plan, not an afterthought.

3. **Baseline.** Before touching production code, capture or write tests and benchmarks that prove current behavior and, if performance is a goal, current metrics.
   - Tests that read as sentences about behavior: happy path, error path, edge cases.
   - Integration tests for end-to-end flows.
   - Benchmark numbers: latency percentiles, throughput, allocation count, heap size.
   - Commit the baseline. Every later change is measured against it.

4. **Execute.** Make small, atomic commits; keep the build green at every step; preserve public behavior. Apply [code-craft](../skills/code-craft/SKILL.md) (Architecture, Safety, State & Concurrency, Observability) and [performance-patterns](../skills/performance-patterns/SKILL.md) only after correctness is proven. When principles conflict: clarity over concision, simplicity over concision, maintainability over consistency.

5. **Verify.** Run formatter, linter, type-checker, and the full test suite. Re-profile and re-benchmark against the baseline to confirm improvement, not regression. Any metric regresses -> revert and re-plan. Never trade correctness or performance for aesthetics.

6. **Sync spec.** Update or create the spec to match the refactor; never leave it describing the old shape. When code and spec diverge, fix the spec first, then the code -- a stale spec is a bug. If the repo maintains a `docs/` tree and the refactor moved or renamed source files a doc points to, update the affected system/flow doc and its Source map so links still resolve (see [repo-documentation](../skills/repo-documentation/SKILL.md)).

## Success metrics

- Full test suite passes (green build) after every atomic commit.
- Before/after benchmark recorded and compared: no metric regresses beyond an agreed threshold; any improvement cited with evidence.
- Profiler re-run confirms the targeted hot path improved or held.
- Spec and any affected `docs/` entries describe the new shape with no stale references.

## Failure metrics

Abort and hand back to the orchestrator if:

- Baseline tests or benchmarks cannot be captured -- no reproducible before/after comparison is possible.
- Public behavior changes (a previously-passing test fails after a refactor step) and cannot be restored within scope.
- Any measured metric regresses after a step and reverting does not recover it.
- Scope expands beyond the locked plan, or an unknown blocks further safe progress.

## References

- [refactor-checklist](cmd-refactor/references/refactor-checklist.md) -- structural, performance, and correctness smell catalog.
- [code-craft](../skills/code-craft/SKILL.md) -- Architecture, Safety, State & Concurrency, Observability.
- [performance-patterns](../skills/performance-patterns/SKILL.md) -- measure-before-optimize performance patterns.
- [spec-driven-development](../skills/spec-driven-development/SKILL.md) -- REASONS canvas and spec/code sync.
- [repo-documentation](../skills/repo-documentation/SKILL.md) -- keeping the `docs/` tree in sync.
- [AGENTS.md](../AGENTS.md) -- The Loop, Code Craft, Performance.
