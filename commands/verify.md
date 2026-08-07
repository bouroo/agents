---
description: "Verify phase (PROVE) -- format, lint, type-check, scan, test, and githook gate with a fix/review loop. Use to leave the working tree passing every quality gate."
argument-hint: "[scope] [--level=<L1|L2|L3>]"
agent: coder
phase: PROVE
---

# Verify -- Quality-Gate Pipeline

Leave the working tree in a state that passes every quality gate, including the repo's githook verify script. This is the automated layer of the **PROVE** phase.

> **Agent:** requires shell + file-edit access -- run on the mutating worker ([coder](../agents/coder.md)), not the conductor.

**Scope** (optional, from arguments): **$ARGUMENTS**. If empty, verify the whole working tree.

**Options** (ride inside `$ARGUMENTS`, any order, `key=value`; empty keeps the default above):

- `--level=<L1|L2|L3>` -- cap the pipeline at this layer (L1 static, L2 runtime, L3 end-to-end) instead of dialing to the change's complexity. Lower layers still run.

Parsing `$ARGUMENTS` is this command's job -- the host only forwards the string. See [command inputs](../skills/harness-engineering/references/agent-computer-interface.md).

## Pipeline

Gates enforce; prompts only request. Each stage is a gate: a failure stops progression until the code satisfies the rule. Run in order; on findings, **auto-fix** then **re-verify**; repeat until clean or no more auto-fixes are possible, then advance. If `$ARGUMENTS` set `--level`, stop after that layer (L1 static, L2 runtime, L3 end-to-end) instead of dialing to the change's complexity. See [harness-engineering](../skills/harness-engineering/SKILL.md).

1. **Format** -- apply the project's formatter; fail if files would change after auto-fix.
2. **Lint** -- linter with warnings-as-errors; auto-fix where supported. Include the language's **doc-convention linter** so comment noise and missing doc comments are caught computationally (godoc, TSDoc/JSDoc, docstring, rustdoc linters). If none is configured, note the absence and proceed.
3. **Type-check** -- static type checker, strict; no auto-fix, so move directly to review on issues.
4. **Scan** -- secret/SAST/vulnerability scanners; fail above threshold. Never auto-fix security findings -- review and escalate.
5. **Test** -- full suite (unit + integration); coverage must meet the spec's Safeguards. A green suite is one signal, not proof -- for high-trust changes, **grade the tests** with a mutation probe. See the [right-sizing map](../skills/harness-engineering/references/right-sizing.md) for when the full sweep applies vs. a lighter touch.

## Fix/review loop

On remaining issues: apply the safest, narrowest auto-fixes first (correct the root cause, never band-aid); if legitimate, patch and re-run; if false positives, document the exception and escalate to the spec's Safeguards; re-run the stage. Stop after **three iterations** and escalate unresolved issues (the hard verify bound -- do not retry verbatim; re-read, adjust, retry once, then widen, then fall back with an explicit note).

## Githook gate

After the pipeline is clean, run the repo's githook verify script(s), in order of preference: `.git/hooks/pre-commit`, `.git/hooks/pre-push`, or a project-defined verify script (`scripts/verify.sh`, `npm run githook:verify`, `make githook-verify`). Enforce exit 0. If none exists, note the absence and proceed.

## Success metrics

- Every stage reports command + exit code + actual output.
- Final verdict **CLEAN**: all stages pass, githook exit 0, only intended changes remain.

## Failure metrics

- Any stage fails after three iterations -> **BLOCKED**, escalate with the failing checks.
- Security finding above threshold -> **BLOCKED**, never auto-fixed.

## Reporting

Concise pass/fail per stage (command, exit code, files changed, outstanding findings) + final verdict. Before reporting, run the **artifact-gate sweep**: add any owed `INTENT:`/`TWINS:`/`AUTH:`/`PENDING:` line ([code-craft](../skills/code-craft/SKILL.md)). Delete scratch files and test artifacts created during verification; note the cleanup.

## References

- [harness-engineering](../skills/harness-engineering/SKILL.md) -- gates over prompts, the hard verify bound, mutation testing.
- [code-craft](../skills/code-craft/SKILL.md) -- artifact gates.
