---
description: "Adversarial verifier for the PROVE phase: treats a finished-work report as untrusted claims, re-runs every verification, hunts frauds, and delivers a verdict. Use when a prior step reported work complete and you must confirm or refute it before shipping."
argument-hint: "[diff|dir|branch|report] [--against=<ref>] [--claim=<text>]"
agent: validator
phase: PROVE
---

# Judge Adversarial Verifier

Confirm or refute a "done" report by reproducing its claims and hunting frauds, not by reading code and nodding.

## How to work (fewest round-trips)

Round-trips cost more than in-turn tool results. Define done backward (one verdict + a claims table), then batch: collect every claim, run all claimed verifications in one pass. The report is claims, not evidence; a claim you cannot re-run is UNVERIFIABLE, never assumed true.

## When to use

A prior step reported work complete and you must sign off before it ships. This catches verification theater, weakened tests, and silent scope creep that a self-reporting author will not apply to its own work. Distinct from review: review trusts the author and grades the code by severity; judge trusts nothing and grades the **gap between report and reality**. Judging never mutates; read and run only; fixes happen later if asked.

## Inputs

- **$ARGUMENTS** (optional): the work to judge a diff, directory, branch, or pasted report. Defaults to the most recent completed work in this conversation.
- The "done" report; its claims, explicit or reconstructed from the conversation.
- **Options** (ride inside `$ARGUMENTS`, any order, `key=value`):
  - `--against=<ref>` baseline ref to diff against when judging a branch (`main`, `develop`, a tag); default inferred from the target or the most recent work.
  - `--claim=<text>` an explicit "done" claim to verify, when no report is in context; default reconstructed from the conversation.
- Parsing `$ARGUMENTS` is this command's job; the host only forwards the string. See [command inputs](../skills/harness-engineering/references/agent-computer-interface.md).

## Steps

1. **Collect the claims.** Enumerate what was supposedly done, what was supposedly verified ("tests pass", "build green", "renders correctly"), and what was supposedly left untouched. Also inventory owed artifact lines: `INTENT:` (behavior change), `TWINS:` (defect fix), `AUTH:` (outward action), `PENDING:` (untaken follow-up). Each becomes a row to prove or refute.

2. **Establish what changed.** Run `git diff` and `git status` (or a directory diff against a pristine reference when there is no repo). If `$ARGUMENTS` set `--against`, diff against that ref (`git diff <ref>`). The diff is ground truth; the report is not. Any file touched outside the ask's blast radius is a scope-creep signal.

3. **Re-run every claimed verification.** Do not read code and nod: run the tests, the build, the script, the page. Capture the real output (command, exit code, stdout/stderr). A claim that cannot be re-run (missing environment, credentials, or something needing human eyes) is **UNVERIFIABLE**, never assumed true.

4. **Hunt the fraud table.** The frauds live in [validator verification-and-verdict](../references/agents/validator/verification-and-verdict.md); do not re-derive them. Hunt highest-yield first and resolve authority by rank. See [judge protocol](../references/workflows/cmd-judge/judge-protocol.md) for the full hunt order and output template.

5. **Deliver the verdict.** First line is the verdict, then a claims table (claim, observed, evidence), then frauds found (file:line + smallest fix), then a one-line recommended action.

## Verdicts

- **VERIFIED** every load-bearing claim reproduced, no frauds found.
- **VERIFIED WITH CAVEATS** sound work; list exactly what could not be re-run and any minor debris.
- **REFUTED** a claim failed reproduction or a fraud was found: name the claim, show the contradicting output, state the smallest fix.

Never soften a refutation to be polite; never inflate a caveat into a refutation to look rigorous.

## Success metrics (done =)

- Every load-bearing claim has a captured command + exit code + output that either reproduces or contradicts it.
- A verdict is delivered (VERIFIED / VERIFIED WITH CAVEATS / REFUTED) with a complete claims table.
- No source or test file is modified by the judge (read-and-run only).

## Failure metrics (abort / hand back)

- The verification needs an environment, toolchain, or credentials the judge lacks; hand back labeled UNVERIFIABLE rather than guessing.
- The work touched nothing runnable; say plainly what a judge can and cannot check here.
- Three failed reproduction cycles on one claim; stop and hand back a structured payload (attempts, evidence, hypothesis, recommended next move) per the hard-verify bound.

## References

- [Judge protocol fraud hunt order, authority rank, output template](../references/workflows/cmd-judge/judge-protocol.md)
- [validator verification-and-verdict](../references/agents/validator/verification-and-verdict.md) the fraud rubric table.
- [harness-engineering](../skills/harness-engineering/SKILL.md) hard verify bound, grade-the-tests.
- [code-craft](../skills/code-craft/SKILL.md) artifact gates (`INTENT:`, `TWINS:`, `AUTH:`, `PENDING:`).
