---
name: cmd-refactor
description: "Refactor (ACT): analyze, plan, baseline, execute, verify, and sync a behavior-preserving restructuring with before/after measurement. Use to restructure correct-but-unclear, unsafe, or slow code without changing observable behavior."
---

# Refactor Phase

Behavior-preserving restructuring in the **Build** stage (§4), its diff entering **Test**: measure before and after, keep only what the data supports, and do performance work only after correctness is proven. Not for new features, behavior-changing fixes, or trivial reformatting. **No options: fully autonomous** — target, scope, and thresholds resolve from the repo's own signals and the run proceeds without waiting on the user.

## Target

The module, package, path, or file to restructure. **Empty -> infer from the repo's own signals**: the working diff first, else the most recently changed code — state the chosen target in one line and proceed. **No signal at all (clean tree, no context) -> report there is nothing to refactor and stop** — never fabricate a target. `--goal=<readability|safety|performance>` weights the plan (performance justifies profiler-driven targets, safety error-path hardening) but never relaxes the behavior-preserving constraint.

## Steps

1. **Analyze** — map the target, dependencies, and call sites in one read pass; name smell, not symptom — duplication consolidates one canonical owner, mixed responsibilities split along reasons change, dead weight deletes ([craft](../skills/quality/SKILL.md)).
2. **Plan** — lock scope, list unknowns, and fix the regression thresholds later comparisons must meet; tests and benchmarks are part of the plan, not an afterthought. State the `INTENT:` line first ([craft](../skills/quality/SKILL.md)).
3. **Baseline** — before touching code, capture what proves current behavior and current numbers: behavior-sentence tests (happy, error, edge), integration tests for end-to-end flows, and — when performance is a goal — profile + benchmark output saved to files. Commit it: the baseline is state outside the model, so committed artifacts — tests, profiles, benchmarks — not memory, are what every later step compares against. **No reproducible baseline -> abort here.**
4. **Execute** — small atomic commits, build green at every step, public behavior frozen. Apply [craft](../skills/quality/SKILL.md); apply [performance](../skills/quality/SKILL.md) only after correctness holds and only on measured hot paths. Restructuring falsifies comments first: delete rather than port them to the new shape.
5. **Verify** — formatter, linter, type-checker, full suite, then re-profile and re-benchmark against the baseline. **Any metric regresses -> revert that step and re-plan**; never trade correctness for aesthetics.
6. **Sync spec** — update spec/docs to the new shape; never leave them describing the old one. When code and spec diverge, update the spec to the actual behavior and flag it — correcting the code would change behavior, which this phase forbids. If a `docs/` tree points at something this refactor moved, update it so links still resolve.

## Done =

- Suite green after every atomic commit.
- Before/after recorded with evidence; no metric regresses past the plan's thresholds; improvements cited as command + output + delta.
- Spec and affected docs describe the new shape with no stale references.

Report in this fixed, machine-scannable shape:
```
target: <chosen target + one-line basis>
baseline: <evidence commands/files committed>
commits: <n>
before/after: <metric deltas | n/a>
verdict: BEHAVIOR PRESERVED | REVERTED | HANDED BACK — one-line justification
```

**Hand back when:** no reproducible baseline exists; public behavior changes and cannot be restored in scope; scope expands past the locked plan.

## References

- [quality](../skills/quality/SKILL.md) owns craft, verification, and performance.
