# Verification, Mutation Probe, and Verdict

Depth for the validator. The [SKILL.md](../../../agents/validator.md) owns the contract; this owns the detail. For deeper adversarial audits, align with the [judge protocol](../../workflows/cmd-judge/judge-protocol.md).

## verify (PROVE)

Independently re-run the worker's claimed L1/L2/L3 evidence. Do not trust the handoff narrative re-execute.

- **L1 static:** lint, type-check, format.
- **L2 runtime:** tests run; app starts; critical paths execute.
- **L3 end-to-end:** at least one path crosses a real boundary.

For every claim re-run: capture command + exit code + actual output and compare against the claimed result. A mismatch (claimed pass, actual fail; or claimed output, different output) is a fraud. Stale evidence (from an earlier change, not this one) is a fraud.

## Mutation probe

Make a targeted change that should break `done_cmd` (flip a condition, delete a guard). If `done_cmd` still passes, the test is theater the verification is invalid and the verdict is REFUTED with the theater as the repro. Revert the probe before returning. A leftover probe is a structural failure.

## judge (PROVE) fraud hunt

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

## Verdict (not negotiated)

Issue exactly one:
- **VERIFIED** every claim holds under independent re-run; executable evidence present; mutation probe caught; probes reverted; tree clean.
- **VERIFIED WITH CAVEATS** reproducible evidence plus documented non-blocking findings; name every caveat.
- **REFUTED** any claim fails under re-run, or the mutation probe exposes test theater. Include the repro and route to `worker (fix)`.

Temporary probes may edit scaffolding but every probe must be reverted.

## Hard verify bound

The third failed cycle on one issue triggers hand-back; never start a fourth. Include all three cycles, the repro, and a hypothesis.

## When you get stuck

Return `REFUTED` (a claim you cannot re-run cannot be verified) or `blocked`:

1. **Repro:** the minimal failing input or the claim you could not independently re-run.
2. **Hypothesis:** one sentence naming the spec gap, environment constraint, weak test, or stale evidence.

Do not brute-force past the bound.
