---
name: cmd-refactor
description: "Refactor (ACT): analyze, plan, baseline, execute, verify, and sync a behavior-preserving restructuring with before/after measurement. Use to restructure correct-but-unclear, unsafe, or slow code without changing observable behavior."
---

# Refactor Phase

Behavior-preserving restructuring in the **Build** stage (§4), its diff entering **Test**: measure before and after, keep only what the data supports, and do performance work only after correctness is proven. Not for new features, behavior-changing fixes, or trivial reformatting.

## Target

The module, package, path, or file to restructure. **Empty -> ask which area before analyzing** — never guess. `--goal=<readability|safety|performance>` weights the plan (performance justifies profiler-driven targets, safety error-path hardening) but never relaxes the behavior-preserving constraint.

## Steps

1. **Analyze** — map the target, its dependencies, and call sites in one read pass; name the smell, not the symptom.
2. **Plan** — lock scope, list unknowns, and fix the regression thresholds later comparisons must meet; tests and benchmarks are part of the plan, not an afterthought. State the `INTENT:` line first ([craft](../skills/craft/SKILL.md)).
3. **Baseline** — before touching code, capture what proves current behavior and current numbers: behavior-sentence tests (happy, error, edge), integration tests for end-to-end flows, and — when performance is a goal — profile + benchmark output saved to files. Commit it; everything later measures against it. **No reproducible baseline -> abort here.**
4. **Execute** — small atomic commits, build green at every step, public behavior frozen. Apply [craft](../skills/craft/SKILL.md); apply [performance](../skills/performance/SKILL.md) only after correctness holds and only on measured hot paths.
5. **Verify** — formatter, linter, type-checker, full suite, then re-profile and re-benchmark against the baseline. **Any metric regresses -> revert that step and re-plan**; never trade correctness for aesthetics.
6. **Sync spec** — update spec/docs to the new shape; never leave them describing the old one. When code and spec diverge, update the spec to the actual behavior and flag it — correcting the code would change behavior, which this phase forbids. If a `docs/` tree points at something this refactor moved, update it so links still resolve.

## Done =

- Suite green after every atomic commit.
- Before/after recorded with evidence; no metric regresses past the plan's thresholds; improvements cited as command + output + delta.
- Spec and affected docs describe the new shape with no stale references.

**Hand back when:** no reproducible baseline exists; public behavior changes and cannot be restored in scope; scope expands past the locked plan.

## References

- [craft](../skills/craft/SKILL.md) commandments, common mistakes, artifact gates.
- [verification](../skills/verification/SKILL.md) three-layer termination, mutation probe.
- [performance](../skills/performance/SKILL.md) measure-first cycle and routing.
