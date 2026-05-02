---
description: Format, lint, type-check, scan, and test the project
---

Run full project verification.

$ARGUMENTS

## Workflow

1. **Discover tools** — Read project config to find formatters, linters, type checkers, test runners
2. **Format** — Run formatter (e.g., `gofmt`, `prettier`, `rustfmt`)
3. **Lint** — Run linter (e.g., `golangci-lint`, `eslint`, `clippy`)
4. **Type-check** — Run type checker if applicable (e.g., `tsc --noEmit`, `mypy`)
5. **Test** — Run test suite with coverage
6. **Report** — Summarize results, list failures with suggested fixes

## If Arguments Provided

Use `$ARGUMENTS` as the scope (specific files, directories, or test patterns).

## Auto-Fix

If a tool supports auto-fix, run it in fix mode first, then re-verify.

## Failure Handling

1. Parse the error output
2. Identify root cause
3. Fix the issue
4. Re-run the failing step
5. After fix, re-run ALL steps to check for regressions
