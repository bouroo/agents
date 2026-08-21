---
description: "Refactor phase (ACT loop): analyze, plan, baseline, execute, verify, and sync a behavior-preserving restructuring with before/after measurement. Use when restructuring existing code for clarity, safety, or performance without changing its observable behavior."
argument-hint: "<module|package|path|file> [--goal=<readability|safety|performance>]"
---

# Refactor Phase

A behavior-preserving restructuring workflow inside the ACT phase. Measure before and after; keep only what the data supports; performance work only after correctness is proven.

> Runs on the **worker** (implementing) agent -- the one with file-edit and shell access. **Not as one delegation:** analyze on `discover (explore)`, then hand the plan to `worker` per bounded unit; each unit gets its own `done_cmd` and evidence. A fresh-context worker handed the whole workflow stalls mid-analysis; the worker should return `partial` with a unit split, and the orchestrator re-delegates.

## How to work (fewest round-trips)

Round-trips cost more than in-turn tool results. Define done backward (green suite after every commit, before/after numbers recorded, spec and docs describe the new shape), then batch: map the target and call sites in one read pass, profile in one pass, then edit, then verify. A regressed metric or red test stops the step.

## When to use

Restructure existing code that is correct but unclear, unsafe, or slow, without changing its observable behavior. Not for new features, behavior-changing bug fixes, or trivial reformatting.

## Inputs

- **$ARGUMENTS** target area (module, package, path, or file). If empty, ask the user which area to target before analyzing; do not guess.
- **Options** (ride inside `$ARGUMENTS`, any order, `key=value`):
  - `--goal=<readability|safety|performance>` what the refactor optimizes for. Default: behavior-preserving, data-driven (improve what measurement finds, change nothing observable).
- Parsing `$ARGUMENTS` is this command's job; the host only forwards the string. See [command inputs](../skills/harness-engineering/references/agent-computer-interface.md).

## Steps

1. **Analyze.** Map the target area, dependencies, and call sites. Identify the smell, not the symptom. Run CPU, memory, and I/O profilers; record heap profiles and allocation counts for the top contributors. Catalog smells via [refactor-checklist](../references/workflows/cmd-refactor/refactor-checklist.md).

2. **Plan.** Write a REASONS canvas (see [spec-driven-development](../skills/spec-driven-development/SKILL.md)). Lock scope explicitly; mark unknowns. If `$ARGUMENTS` set `--goal`, let it weigh the plan (`performance` justifies profiler-driven targets, `safety` justifies error-path hardening) without relaxing the behavior-preserving constraint. Tests and benchmarks are part of the plan, not an afterthought.

3. **Baseline.** Before touching production code, capture tests and benchmarks that prove current behavior and, if performance is a goal, current metrics: behavior-sentence tests (happy, error, edge), integration tests for end-to-end flows, benchmark numbers (latency percentiles, throughput, allocation count, heap size). Commit the baseline; every later change is measured against it.

4. **Execute.** Make small, atomic commits; keep the build green at every step; preserve public behavior. Apply [code-craft](../skills/code-craft/SKILL.md) and, only after correctness is proven, [performance-patterns](../skills/performance-patterns/SKILL.md). When principles conflict: clarity over concision, simplicity over concision, maintainability over consistency.

5. **Verify.** Run formatter, linter, type-checker, and the full suite. Re-profile and re-benchmark against the baseline to confirm improvement, not regression. Any metric regresses -> revert and re-plan. Never trade correctness or performance for aesthetics.

6. **Sync spec.** Update or create the spec to match the refactor; never leave it describing the old shape. When code and spec diverge, fix the spec first, then the code. If the repo maintains a `docs/` tree and the refactor moved or renamed source files a doc points to, update the affected system/flow doc and its Source map so links still resolve (see [repo-documentation](../skills/repo-documentation/SKILL.md)).

## Success metrics (done =)

- Full suite passes (green build) after every atomic commit.
- Before/after benchmark recorded and compared: no metric regresses beyond an agreed threshold; any improvement cited with evidence.
- Profiler re-run confirms the targeted hot path improved or held.
- Spec and any affected `docs/` entries describe the new shape with no stale references.

## Failure metrics (abort / hand back)

- Baseline tests or benchmarks cannot be captured. No reproducible before/after comparison is possible.
- Public behavior changes (a previously-passing test fails after a refactor step) and cannot be restored within scope.
- Any measured metric regresses after a step and reverting does not recover it.
- Scope expands beyond the locked plan, or an unknown blocks further safe progress.

## References

- [refactor-checklist](../references/workflows/cmd-refactor/refactor-checklist.md) structural, performance, and correctness smell catalog.
- [code-craft](../skills/code-craft/SKILL.md) hard rules, ten commandments, common mistakes.
- [performance-patterns](../skills/performance-patterns/SKILL.md) measure-before-optimize patterns.
- [spec-driven-development](../skills/spec-driven-development/SKILL.md) REASONS canvas and spec/code sync.
- [repo-documentation](../skills/repo-documentation/SKILL.md) keeping the `docs/` tree in sync.
