---
name: cmd-verify
description: "Verify phase (PROVE): format, lint, type-check, scan, test, and hook gates with a fix/re-verify loop. Use to leave a working tree passing every quality gate."
---

# Verify Quality-Gate Pipeline

Leave the working tree passing every quality gate. This is the automated layer of **PROVE** in the **Test** stage (§4): gates enforce, prompts only request. Run the stages as one batched pass, not call by call; judgment enters only on findings.

## Scope

Default: the whole working tree. An argument narrows the target (`src/module`, a file list). `--level=<L1|L2|L3>` caps the pipeline at that layer instead of dialing to the change's complexity; lower layers still run. Dial guidance: [verification](../skills/verification/SKILL.md).

## Pipeline

Run each stage in order; on a finding apply the narrowest safe auto-fix at the **root cause** (never a band-aid) and re-run that stage. Cap: **three fix/re-verify iterations on one issue**, then escalate it — the hard verify bound ([verification](../skills/verification/SKILL.md)).

1. **Format** — project formatter; fail if files would change after auto-fix.
2. **Lint** — warnings-as-errors; auto-fix where supported; include the doc-convention linter if configured, else note its absence.
3. **Type-check** — strict; no auto-fix (issues go to review).
4. **Scan** — secrets / SAST / vulnerabilities above threshold fail; **never auto-fix a security finding** — report and escalate.
5. **Test** — the full suite; a green suite is a signal, not proof, so grade high-stakes changes with a **mutation probe** (flip a semantic defect, require FAIL, revert).
6. **Hook gate** — the repo's own verify script(s) (pre-commit/pre-push hooks, `scripts/verify.*`, package-script equivalents) must exit 0; note the absence if none exists.

## Done = CLEAN

All six stages pass with command + exit code + actual output captured (a narrated pass is not evidence), hooks exit 0, and only intended changes remain in the tree. Otherwise report per-stage pass/fail (command, exit code, files changed, outstanding findings) and the final verdict.

**Abort/BLOCKED:** any stage still failing after three iterations; any security finding above threshold.

Before reporting, run the artifact-gate sweep and add every owed `INTENT:`/`TWINS:`/`AUTH:`/`PENDING:` line ([craft](../skills/craft/SKILL.md)); delete scratch artifacts.
