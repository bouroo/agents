---
description: Verify phase — format, lint, type-check, scan, test, and githook gate with fix/review loop
---

# Verify Phase

Goal: leave the working tree in a state that passes every quality gate, including the repository's githook verify script.

Scope (optional, from arguments): **$ARGUMENTS**. If empty, verify the whole working tree.

## Pipeline

**Gates enforce; prompts only request.** Each stage below is a gate: a failure stops progression until the code satisfies the rule, leaving only the one path forward — produce a solution that passes. See [harness-engineering](../skills/harness-engineering/SKILL.md) §10.

Run the following stages in order. If a stage produces findings, attempt **auto-fix**, then **re-verify**. Repeat until the stage is clean or no more auto-fixes are possible. Only then proceed to the next stage.

1. **Format** — apply the project's formatter; fail if files would change after auto-fix.
2. **Lint** — run the configured linter with warnings-as-errors; auto-fix where the toolchain supports it.
3. **Type-check** — run the static type checker with strict settings; no auto-fix, so move directly to review if issues remain.
4. **Scan** — run secret/SAST/vulnerability scanners; fail on any finding above the agreed threshold. Never auto-fix security findings; review and escalate.
5. **Test** — run the full test suite (unit + integration); require coverage to meet the Safeguards defined in the spec. A green suite is one signal, not proof — when the change is high-trust, **grade the tests** with mutation testing (mutate the implementation; a suite that stays green is decoration, not coverage). See [harness-engineering](../skills/harness-engineering/SKILL.md) §12.

## Fix/Review Loop

After any stage that still has issues:

- **Fix** — apply the safest, narrowest auto-fixes first. Never band-aid; correct the root cause.
- **Review** — inspect remaining findings. If they are legitimate, patch them and re-run the stage. If they are false positives, document the exception and escalate to the spec's Safeguards section.
- **Re-verify** — run the stage again. If it still fails, repeat the loop. Stop after a maximum of three iterations to avoid infinite loops; escalate unresolved issues.

## Githook Gate

After the pipeline is fully clean, run the repository's githook verify script(s). Look for, in order of preference:

- `.git/hooks/pre-commit` (if executable)
- `.git/hooks/pre-push` (if executable)
- A project-defined verify script (e.g., `scripts/verify.sh`, `npm run githook:verify`, `make githook-verify`, `pnpm verify`, etc.)

Execute the discovered script(s) and enforce a zero exit code. If no githook script exists, note the absence and proceed.

## Reporting

Produce a concise pass/fail summary for every stage, including:
- Exact command invoked
- Exit code
- Files changed (if any)
- Any actionable findings still outstanding
- Final verdict: **CLEAN** or **BLOCKED**
