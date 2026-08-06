# Coder Modes, Mutation Probe, and Judgment

Depth for the coder. The [SKILL.md](../../coder.md) owns the contract; this owns the detail.

## implement (ACT)

1. Read SCOPE and `done_cmd` before editing.
2. Make the smallest change that satisfies the spec.
3. Run `done_cmd`; capture command + exit code + output.
4. Emit `INTENT: <user-visible behavior change>` on the first behavior-changing edit.
5. Return the handoff. If `done_cmd` is red, return `failed` with the repro -- do not explain it away.

## fix (ACT)

1. **Repro first.** Re-run the supplied failing input before touching code: no repro, no fix.
2. Patch **one** bug (one root cause, not a sweep).
3. Add a regression test that fails before the patch and passes after.
4. Emit `TWINS: <failing input + fixed expectation>`.
5. Search the whole project for the same wrong construct; if found, flag siblings under `PENDING:` (do not fix out of SCOPE).

## verify (PROVE)

Dial the layers to job complexity ([right-sizing](../../../skills/harness-engineering/references/right-sizing.md)); the dial chooses which layers, never the evidence standard.

- **L1 static:** lint, type-check, format. Every source change.
- **L2 runtime:** tests run; app starts; critical paths execute. When the change runs.
- **L3 end-to-end:** at least one path crosses a real boundary. When the change crosses one (`n/a` allowed with a one-line reason).

For every layer run: capture command + exit code + actual output. A narrated pass is not evidence. If a layer is red, return `failed` with the repro. If read-only review conflicts with a red test, the red test wins.

**Mutation probe:** make a targeted change that should break `done_cmd` (flip a condition, delete a guard). If `done_cmd` still passes, the test is theater -- the verification is invalid until the test catches the mutation. Revert the probe before returning.

## judge (PROVE)

Treat the "done" report as **claims**, not facts. Independently re-run at least one claimed check. Hunt frauds:

| # | Fraud | Probe |
|---|---|---|
| 1 | Weakened/skipped check | Re-run the exact `done_cmd`; confirm exit code |
| 2 | False completion | Confirm the claimed output matches actual output |
| 3 | Scope creep | Diff SCOPE vs files touched |
| 4 | Spec betrayal | Re-check DONE_WHEN, not just `done_cmd` |
| 5 | Test theater | Mutation probe (above) |
| 6 | Leftover probe/debris | Confirm a clean tree |
| 7 | Stale evidence | Re-run; evidence must be from this change |
| 8 | Hidden assumption | Inspect environment/version pins |
| 9 | Negotiated verdict | Reject any "mostly works"; one verdict only |

Issue exactly one verdict:
- **VERIFIED** -- every claim holds under re-run; executable evidence present; probes reverted.
- **VERIFIED WITH CAVEATS** -- reproducible evidence plus documented non-blocking findings.
- **REFUTED** -- any claim fails under re-run.

Verdicts are not negotiated. Temporary judge probes may edit scaffolding but every probe must be reverted.

## Hard verify bound

The third failed cycle on one issue triggers hand-back; never start a fourth. Include all three cycles, the repro, and a hypothesis in the handback.

## When you get stuck

Return `blocked` (or `REFUTED` in judge mode):

1. **Repro:** minimal failing input or smallest scope exposing the ambiguity.
2. **Hypothesis:** one sentence naming the spec gap, dependency, environment constraint, weak test, or stale evidence.

Do not brute-force past the bound.
