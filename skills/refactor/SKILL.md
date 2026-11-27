---
name: refactor
description: Use to restructure correct-but-unclear, unsafe, or slow code without changing observable behavior — when behavior must stay frozen while the shape changes, or a measured hot path needs work after correctness is proven. Not for new features or behavior-changing fixes.
---

# Refactor Without Behavior Change

Restructure code while observable behavior stays frozen. Measure before and after, keep only what the data supports, and do performance work only after correctness is proven.

## 1. Analyze

- Map the target, its dependencies, and its call sites in one read pass.
- Name the smell, not the symptom: duplication consolidates to one owner, mixed responsibilities split along reasons to change, dead weight deletes.

## 2. Plan

- Lock the scope, list the unknowns, and fix the regression thresholds later comparisons must meet.
- State the `INTENT:` line first, before any edit.

## 3. Baseline before touching code

- Capture what proves current behavior — happy, error, and edge tests — and, when performance is a goal, the measured numbers.
- No reproducible baseline means abort here.

## 4. Execute

- Make small atomic steps, with the checks green at every step.
- Freeze public behavior, and delete stale comments rather than port them to the new shape.

## 5. Verify

- Run the full checks, then re-measure against the baseline.
- Any metric that regresses past the thresholds reverts that step and re-plans.
- Never trade correctness for aesthetics, and touch performance only on a measured hot path.

## 6. Sync the spec

- Update docs and specs to the new shape in the same change, because a stale doc is a bug.

## 7. Verdict

- Report BEHAVIOR PRESERVED / REVERTED / HANDED BACK, with before-and-after evidence: command, output, and delta.
- Hand back when no reproducible baseline exists, public behavior cannot be restored in scope, or scope expands past the locked plan.