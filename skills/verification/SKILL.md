---
name: verification
description: "Proving work is actually done: right-sizing the controls, three-layer termination, evidence audit, mutation probes, adversarial judging with fraud hunting, and the GROW loop. Use when verifying beyond static checks, judging a done report, or when a verify cycle fails."
---

# Verification

**Stance:** "done" is the most common lie an agent tells. Its costume is verification theater — a transcript containing "the tests passed", "the build is green" while the observation is missing: intent to verify narrated, result asserted, captured command/exit/output absent. The other failure modes burn budget; this one ships broken work labeled *done* and breaks the trust budget every other check depends on. A gate that can fail is worth ten reminders that cannot.

> **Override.** A project-level harness spec that explicitly supersedes this skill wins.

## Right-size first (refuse the Average Answer Trap)

Plot the job on two axes: **action complexity** (tools, decisions, outward effects coordinated) and **context complexity** (state gathered and retained).

| Axes | Example job | Layers | Mutation probe | Judge | Artifact lines | Retro |
|---|---|---|---|---|---|---|
| Low / Low | typo, rename, format-only | L1 only | no | no | note skips | no |
| Mid / Mid | fix within a module, runtime behavior | L1 + L2 | behavior-bearing lines | on demand | `INTENT:` / `TWINS:` owed | if a failure recurred |
| High / High | cross-boundary, infra, security | L1 + L2 + L3 | yes | yes | full + decision log | yes |

Two traps: the **Average Answer Trap** runs hardest-job controls on every task (a one-line typo does not need a judge); the **Kirby Effect** leaves components that encoded a model limitation after models improved — revisit each addition when a stronger model lands. Executable evidence is never optional; the dial chooses layers, never lowers the standard. When window or scope strains: **Reduce** actions, **Offload** context to `.agents/`, **Isolate** concerns (WIP 1). This doctrine calibrates source-code agents only; other domains build their own minimum viable harness.

## Termination: three layers

- **L1 static** lint, type-check, format — every source change.
- **L2 runtime** tests run, critical paths execute, app starts — when the change runs.
- **L3 end-to-end** one path crosses a real boundary — when the change crosses one (`n/a` allowed with a one-line reason).

Guides steer before act, sensors detect after: run the cheapest check earliest; prefer computational sensors (deterministic, fast) over inferential ones (LLM judgment, costly). A red test beats a narrative pass; if review conflicts with a red test, the red test wins.

## Executable evidence

Every done claim carries command (literal), exit code (explicit), and actual output (captured, not paraphrased) — on disk where it survives compaction. **Evidence audit**, five questions asked of any done claim:

1. Is the command literally present, not paraphrased?
2. Is the exit code captured?
3. Is the output the runner's own success/diff line, not a summary?
4. Does the claim match the observation word-for-word?
5. Does the asserted behavior equal what the check actually exercises?

Any "no" means unverified; the unit is not done.

## Mutation probe

Introduce a single semantic defect (flip a boolean, shift a bound, drop a guard); run the suite and require it to FAIL; revert and confirm PASSES. A suite that cannot catch a deliberate defect is theater — the check itself becomes the defect under review.

## Judge a finished report

Judging changes nothing — read and run only; minutes, not hours. Hunt in order (the first hit usually explains the rest):

1. Establish ground truth: **the diff outranks the report.**
2. Diff test files first — asserts dropped or weakened, tolerances loosened, skips added, mocks swapped for real calls, assertions edited toward new wrong behavior.
3. Trace each `AUTH:` quote against the conversation; an outward effect without authorization covering *this exact action* is fraud.
4. Confirm presence and truth of every owed artifact line (`INTENT:`/`TWINS:`/`AUTH:`/`PENDING:`).
5. Re-run every re-runnable claim (cap 3 reproductions per claim); sweep debris and scope creep.
6. Resolve conflicts by authority rank: user statement > spec > checks > current code.

Labels: a claim that cannot be re-run is **UNVERIFIABLE**, never assumed true; UNVERIFIABLE on a load-bearing claim forces caveats. Verdict is exactly one of **VERIFIED / VERIFIED WITH CAVEATS / REFUTED** — refutation names the claim and shows contradicting output plus smallest fix; never soften a refutation to be polite, never inflate a caveat to look rigorous. If the environment to verify is missing, hand back rather than guess.

## Diagnosis

Reason backward from the observed failure to the state that produced it and name the root cause before writing the next change; a symptom patch that leaves the cause in place is a defect. Route surprises backward, never forward: contradiction at PROVE returns to THINK; a mechanical mistake returns to ACT.

## GROW

A recurring failure is a **harness problem, not a prompt problem**: prompt tweaks smooth edges; durable reliability updates the surrounding system. Catalog failure modes in `.agents/plans/{slug}/retro.md` (cite doctrine by rule, not by rottable path), convert findings into deterministic gates, track failure frequency per category and halt to upgrade sensors when a budget blows.

| Failure mode | Looks like | Primary fix |
|---|---|---|
| Tool-routing drift | `cat`/`grep`/`find` via shell instead of built-ins | capability routing rule |
| Verification theater | "tests pass" without captured output | evidence audit + mutation probe |
| Scope creep / spec betrayal | edits outside the ask; code against spec | `INTENT:` gate + authority rank |
| Recurring class (>= 2 units) | same failure shape repeats | halt; retro -> gate |

## References

- [flowcharts](references/flowcharts.md) the whole discipline as executable decision charts.
- [craft](../craft/SKILL.md) the artifact gates this skill audits.
- [performance](../performance/SKILL.md) measurement claims meet this evidence standard too.
