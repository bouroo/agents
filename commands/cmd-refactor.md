---
name: cmd-refactor
description: "Refactor (ACT): analyze, plan, baseline, execute, verify, and sync a behavior-preserving restructuring with before/after measurement. Use to restructure correct-but-unclear, unsafe, or slow code without changing observable behavior."
---

# Refactor Phase

Behavior-preserving restructuring: measure before and after; keep only what the data supports; performance work only after correctness is proven. Not for new features, behavior-changing fixes, or trivial reformatting.

## Target

Argument: the module, package, path, or file to restructure. If empty, ask which area before analyzing - do not guess. Option `--goal=<readability|safety|performance>` weights the plan (performance justifies profiler-driven targets; safety justifies error-path hardening) but never relaxes the behavior-preserving constraint.

## Steps

1. **Analyze.** Map the target area, dependencies, and call sites in one read pass. Identify the smell, not the symptom.
2. **Plan.** Lock scope explicitly; list unknowns. Tests and benchmarks are part of the plan, not an afterthought. State the intent line first ([craft](../skills/craft/SKILL.md) `INTENT:`).
3. **Baseline.** Before touching code, capture what proves current behavior and current numbers: behavior-sentence tests (happy, error, edge), integration tests for end-to-end flows, and - when performance is a goal - profile + benchmark output saved to files. Commit the baseline; everything later measures against it. If no reproducible baseline is capturable, abort here.
4. **Execute.** Small atomic commits, build green at every step, public behavior frozen. Apply [craft](../skills/craft/SKILL.md); apply [performance](../skills/performance/SKILL.md) only after correctness holds and only on measured hot paths.
5. **Verify.** Formatter, linter, type-checker, full suite - then re-profile and re-benchmark against the baseline. Any metric regresses -> revert that step and re-plan; never trade correctness for aesthetics.
6. **Sync spec.** Update spec/docs to match the new shape - never leave them describing the old one. When code and spec diverge, fix the spec first, then the code; if the repo keeps a `docs/` tree and this refactor moved something a doc points at, update that doc so links still resolve.

## Done =

- Suite green after every atomic commit.
- Before/after recorded with evidence: no metric regresses beyond an agreed threshold; improvements cited (command + output + delta).
- Spec and affected docs describe the new shape with no stale references.

Hand back when: no reproducible baseline exists; public behavior changes and cannot be restored in scope; scope expands beyond the locked plan.

## References

- [craft](../skills/craft/SKILL.md) commandments, common mistakes, artifact gates.
- [verification](../skills/verification/SKILL.md) three-layer termination, mutation probe.
- [performance](../skills/performance/SKILL.md) measure-first cycle and routing.
