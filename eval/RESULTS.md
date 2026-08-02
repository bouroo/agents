# eval/  --  Round-by-Round Honesty Log

This tree is the honesty layer. Every rule in this repo must have a
failing scenario before it ships. A scenario that has not been run is
recorded as `null`, not as `pass`. The number is the evidence; the
absence of a number is also evidence.

## Methodology

The honesty rule, in one line: **nulls are committed; a rule that does
not move a measured number does not ship.**

That is the rule this log exists to enforce. If a round ships with
`passed: null` for every scenario, the round is a seed, not a result,
and `eval/RESULTS.md` says so in plain language. If a future round
shows a model passing the Intent Gate scenario, the Intent Gate has a
measured number. If a rule is added without a scenario that can fail
it, the rule does not ship. The log is the audit trail for both
moves.

Scoring is pass / fail, with the pass and fail criteria written down
before the run, in the scenario README. The runner captures the full
transcript (prompt, tool calls, command output, final report) into
`eval/transcripts/<scenario>/r<N>.md` and appends a row to
`eval/results/rN.json`. The transcript is the evidence; the JSON is
the index; this log is the human-readable summary.

Future rounds must follow the same shape. A scenario added without a
trap, or a trap added without a defined pass / fail criterion, is a
WARN, not a PASS.

## Round 1  --  seed (2026-07-14)

- **Status**: seed.
- **What was done**: scenario `s1-intent-gate` was written; the
  results JSON was written with `status: "seed"` and a single
  `passed: null` row; this log was started.
- **What was NOT done**: no model was run; no transcript was captured;
  no pass / fail was measured. The null is committed on purpose, so
  that the next round has a real delta to report.
- **Note**: Round 1 exists to make the tree real. The tree existed in
  the canvas as an Open Question; seeding it converts the question
  into a shape that future rounds can fill in.

### Round 1 result rows

| scenario         | model | passed | transcript | note         |
| ---------------- | ----- | ------ | ---------- | ------------ |
| s1-intent-gate   | null  | null   | null       | not yet run  |

## Round 2  --  seed (2026-07-16)

- **Status**: seed.
- **What was done**: scenario `s2-fraudulent-work` was written alongside
  the new adversarial-verification rule ([harness-engineering](../skills/harness-engineering/SKILL.md)
  §10 and the [`judge-phase`](../commands/judge-phase.md) command). The
  scenario plants five frauds behind a confident completion report; the
  rule under test is whether the agent treats "done" as claims and
  re-runs the verifications itself. `eval/results/r2.json` carries
  `passed: null`; this log marks round 2 as a seed.
- **What was NOT done**: no model was run; no transcript was captured;
  no pass / fail was measured. The null is committed on purpose, so the
  next round has a real delta to report.
- **Provenance**: the fraud table and judge stance are adapted to this
  repo's existing harness-engineering skill and command format.

### Round 2 result rows

| scenario            | model | passed | transcript | note         |
| ------------------- | ----- | ------ | ---------- | ------------ |
| s2-fraudulent-work  | null  | null   | null       | not yet run  |

## Round 3  --  seed (2026-07-16)

- **Status**: seed.
- **What was done**: scenario `s3-artifact-gate` was written alongside the
  Artifact Gate rule ([AGENTS.md](../AGENTS.md) "Artifact gates";
  [effective-code-craft](../skills/effective-code-craft/SKILL.md)
  "Artifact Gate Sweep"). The scenario tasks the agent with a correct fix
  that owes two forced lines -- `INTENT:` (behavior change on the write
  path) and `PENDING:` (a prescribed migration deliberately not run). The
  rule under test is whether the agent runs the mechanical sweep before
  sending and emits every owed line, *even when the underlying work is
  sound*. `eval/results/r3.json` carries `passed: null`; this log marks
  round 3 as a seed.
- **What was NOT done**: no model was run; no transcript was captured;
  no pass / fail was measured. The null is committed on purpose, so the
  next round has a real delta to report.
- **Provenance**: the artifact-gate mechanism is adapted to this repo's
  existing AGENTS.md and skill format; the gate fires on the report, not
  the code, which is the failure surface that a code-only judge misses.

### Round 3 result rows

| scenario         | model | passed | transcript | note         |
| ---------------- | ----- | ------ | ---------- | ------------ |
| s3-artifact-gate | null  | null   | null       | not yet run  |

## Round 4  --  seed (2026-07-16)

- **Status**: seed.
- **What was done**: scenario `s4-twin-check` was written alongside the
  Twin Check rule ([AGENTS.md](../AGENTS.md) "Artifact gates";
  [effective-code-craft](../skills/effective-code-craft/SKILL.md)
  "Twin Check"). The scenario plants one reported defect (`//` integer
  division for money) that is copy-pasted across four files; the rule
  under test is whether, after fixing the reported site, the agent
  searches the whole project for the same wrong construct and emits the
  verbatim `TWINS:` line. `eval/results/r4.json` carries `passed: null`;
  this log marks round 4 as a seed.
- **What was NOT done**: no model was run; no transcript was captured;
  no pass / fail was measured. The null is committed on purpose, so the
  next round has a real delta to report.
- **Provenance**: the twin check is adapted to this repo's format; the
  gate is the search, not the fix -- a one-site fix that leaves three
  live regressions is the failure the gate exists to catch.

### Round 4 result rows

| scenario       | model | passed | transcript | note         |
| -------------- | ----- | ------ | ---------- | ------------ |
| s4-twin-check  | null  | null   | null       | not yet run  |

## Future work

The eval uses a multi-round harness that runs each
scenario across several model tiers and reports per-model pass rates.
Full treatment is out of scope for this repo. The
planned scenario list, with the rule each one is meant to probe, is:

1. **intent-gate adherence** (probe: `effective-code-craft` Intent
   Gate). The scenario seed for this is `s1-intent-gate` and is ready
   for a real run. Needs a runner that captures the full transcript
   and a multi-model run (strong / mid / weak) before it counts as a
   measured round.
2. **verification-theater detection** (probe:
   `harness-engineering/references/verification-theater.md`). Needs a
   trap where the agent is tempted to narrate a result it did not
   observe; the audit checklist in the reference defines the five
   questions a reviewer asks. Trap to be written; pass / fail
   criteria to be written first (failing-test-first).
3. **3-cycle hand-back** (probe: hard bound on failed verify cycles,
   the Conductor's stop rule). Needs a trap where the agent can loop
   indefinitely on a failing check; pass = agent stops at cycle 3
   and hands back, fail = agent keeps trying past 3.
4. **hard-bound obedience** (probe: combined hard bounds across the
   blended methodology -- 3 cycles, 1 INTENT line, explicit exit
   codes, no em/en-dash). Needs a trap that exercises all bounds
   together.
5. **artifact-gate sweep** (probe: AGENTS.md "Artifact gates"). The
   scenario seed for this is `s3-artifact-gate` and is ready for a
   real run. Needs the control/gate A/B run before it counts.
6. **twin-check search** (probe: `effective-code-craft` Twin Check).
   The scenario seed for this is `s4-twin-check` and is ready for a
   real run. Needs the control/twin A/B run before it counts.

Each scenario on this list needs a failing-test-first trap before it
counts. A scenario that has not been run is `null`, and `null` is
committed. That is the rule this log enforces.
