---
name: cmd-verify
description: "Verify phase (PROVE): format, lint, type-check, scan, test, and hook gates with a fix/re-verify loop. Use to leave a working tree passing every quality gate."
---

# Verify Quality-Gate Pipeline

Leave the working tree passing every quality gate. This is the automated layer of **PROVE**: gates enforce, prompts only request. One invocation runs every deterministic stage; judgment enters only on findings. This pipeline is a macro instance - run the stages as batched execution, not call by call.

## Scope

Default: the whole working tree. An optional argument narrows the target (`src/module`, a file list). Option `--level=<L1|L2|L3>` caps the pipeline at that layer (L1 static, L2 runtime, L3 end-to-end) instead of dialing to the change's complexity; lower layers still run. Dial guidance: [verification](../skills/verification/SKILL.md).

## Pipeline

Run in order; on findings apply the safest narrowest auto-fix (**correct the root cause**, never band-aid), re-run the stage, repeat until clean, then advance.

1. **Format** project formatter; fail if files would change after auto-fix.
2. **Lint** warnings-as-errors; auto-fix where supported. Include the language's doc-convention linter if configured; otherwise note the absence.
3. **Type-check** strict; no auto-fix - issues go straight to review.
4. **Scan** secrets / SAST / vulnerabilities; fail above threshold. **Never auto-fix security findings** - report and escalate.
5. **Test** the full suite (unit + integration). A green suite is one signal, not proof: for high-stakes changes grade the tests with a **mutation probe** (flip a semantic defect, require FAIL, revert).

**Hook gate:** after the pipeline is clean, run the repo's own verify script(s) (pre-commit/pre-push hooks, `scripts/verify.*`, package-script equivalents) and enforce exit 0; note the absence if none exists.

## Bound

Stop after **three fix/re-verify iterations** on the same issue and escalate unresolved items - the hard verify bound applies to this pipeline too ([verification](../skills/verification/SKILL.md)).

## Done = CLEAN

- Every stage reports command + exit code + actual output (a narrated pass is not evidence).
- All stages pass, hooks exit 0, only intended changes remain in the tree.

Abort/BLOCKED: any stage failing after three iterations; any security finding above threshold (never auto-fixed).

## Reporting

Pass/fail per stage (command, exit code, files changed, outstanding findings), then the final verdict. Before reporting, run the artifact-gate sweep - add any owed `INTENT:`/`TWINS:`/`AUTH:`/`PENDING:` line ([craft](../skills/craft/SKILL.md)) - and delete scratch artifacts.
