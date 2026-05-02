---
description: Format, lint, type-check, scan, and test the project
agent: implementer
---

Run full project verification. Execute all steps autonomously without stopping for confirmation between steps.

$ARGUMENTS

## Workflow

1. **Discover tools** — Read project config to find formatters, linters, type checkers, test runners
2. **Format** — Run formatter (e.g., `gofmt`, `prettier`, `rustfmt`)
3. **Lint** — Run linter (e.g., `golangci-lint`, `eslint`, `clippy`)
4. **Type-check** — Run type checker if applicable (e.g., `tsc --noEmit`, `mypy`)
5. **Test** — Run test suite with coverage
6. **Report** — Summarize results, list failures with suggested fixes

**Do not stop after each step.** Run all verification steps in sequence, then report.

## If Arguments Provided

Use `$ARGUMENTS` as the scope (specific files, directories, or test patterns).

## Auto-Fix

If a tool supports auto-fix, run it in fix mode first, then re-verify. Apply fixes autonomously — do not ask for permission.

## Failure Handling

When a step fails:
1. Parse the error output
2. Identify root cause
3. Fix the issue
4. Re-run the failing step
5. After fix, re-run ALL steps to check for regressions

**Fix failures autonomously.** Only stop and report if the same failure persists after two fix attempts.

## Rules

- **Execute the full workflow.** Do not stop after each step to ask whether to continue.
- Auto-fix what can be auto-fixed. Report what requires manual intervention.
- If all steps pass, say so concisely — no need for a lengthy report.
- If arguments specify a scope, only run verification within that scope.