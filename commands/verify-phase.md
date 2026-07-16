---
description: Verify phase  --  format, lint, type-check, scan, test, and githook gate with fix/review loop
---

# Verify Phase

Goal: leave the working tree in a state that passes every quality gate, including the repository's githook verify script.

> **Agent:** requires `bash` + `edit`  --  run on the implementing/build agent, not `plan` or `conductor`.

Scope (optional, from arguments): **$ARGUMENTS**. If empty, verify the whole working tree.

## Pipeline

**Gates enforce; prompts only request.** Each stage is a gate: a failure stops progression until the code satisfies the rule. See [harness-engineering](../skills/harness-engineering/SKILL.md) §10.

Run the stages in order. On findings, **auto-fix**, then **re-verify**; repeat until clean or no more auto-fixes are possible, then advance.

1. **Format**  --  apply the project's formatter; fail if files would change after auto-fix.
2. **Lint**  --  run the linter with warnings-as-errors; auto-fix where the toolchain supports it.
3. **Type-check**  --  run the static type checker with strict settings; no auto-fix, so move directly to review on issues.
4. **Scan**  --  run secret/SAST/vulnerability scanners; fail on findings above threshold. Never auto-fix security findings  --  review and escalate.
5. **Test**  --  run the full suite (unit + integration); coverage must meet the spec's Safeguards. A green suite is one signal, not proof  --  for high-trust changes, **grade the tests** with mutation testing (a suite that stays green after mutation is decoration, not coverage). See [harness-engineering](../skills/harness-engineering/SKILL.md) §12.

## Fix/Review Loop

After any stage with remaining issues:

- **Fix**  --  apply the safest, narrowest auto-fixes first. Never band-aid; correct the root cause.
- **Failed-edit recovery ladder**  --  when an edit itself fails (bad match, wrong span), do not retry verbatim: (1) re-read the exact region, (2) adjust the match, (3) retry once; (4) only then widen to a larger span; a full rewrite is last, and you say you fell back and why.
- **Review**  --  if findings are legitimate, patch and re-run. If false positives, document the exception and escalate to the spec's Safeguards.
- **Re-verify**  --  run the stage again. Stop after a maximum of three iterations; escalate unresolved issues.

## Githook Gate

After the pipeline is clean, run the repository's githook verify script(s), in order of preference:

- `.git/hooks/pre-commit` (if executable)
- `.git/hooks/pre-push` (if executable)
- A project-defined verify script (e.g., `scripts/verify.sh`, `npm run githook:verify`, `make githook-verify`, `pnpm verify`)

Enforce a zero exit code. If no githook script exists, note the absence and proceed.

## Reporting

Produce a concise pass/fail summary for every stage: exact command invoked, exit code, files changed (if any), any actionable findings outstanding, and a final verdict  --  **CLEAN** or **BLOCKED**.

Before reporting, run the **artifact-gate sweep**: scan the report once against what this run owed and repair mechanically  --  behavior changed and no `INTENT:` line, add it; defect fixed and no `TWINS:` search line, add it; outward action taken and no `AUTH:` line, add it; prescribed follow-up deliberately untaken and no `PENDING:` line, add it. A clean run passes untouched. Leave behind only intended changes: delete scratch files and test artifacts you created during verification, and note the cleanup.
