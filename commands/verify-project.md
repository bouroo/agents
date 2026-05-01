---
description: Verify project integrity — format, lint, type-check, scan, and test
---

# Verify Project

Run all available quality checks on the project: formatting, linting, type-checking, security scanning, and testing.

## Steps

1. **Discover project tools** — identify available tools by checking:
   - Build system files (Makefile, package.json, Cargo.toml, go.mod, pom.xml, etc.)
   - Linter configs (.eslintrc, .golangci.yml, ruff.toml, etc.)
   - Formatter configs (.prettierrc, .editorconfig, etc.)
   - CI configuration for test/lint commands
2. **Format check** — run formatters in check mode
3. **Lint** — run linters with zero-tolerance for warnings
4. **Type check** — run type checkers if available
5. **Security scan** — run security scanners if available
6. **Test** — run the full test suite with coverage if available
7. **Report** — summarize all results with specific file:line references for any failures

## Auto-Fix

If issues are found:

1. Run formatter in fix mode (if safe)
2. Run linter with auto-fix flag (if available)
3. Re-run checks to confirm fixes
4. Report remaining issues that need manual attention

## Output

```markdown
# Project Verification Report

## Formatting
- Status: PASS/FAIL
- Details: [output or file list]

## Linting
- Status: PASS/FAIL
- Issues: [file:line — description]

## Type Checking
- Status: PASS/FAIL
- Errors: [file:line — description]

## Security
- Status: PASS/FAIL
- Findings: [severity — description]

## Tests
- Status: PASS/FAIL
- Coverage: X%
- Failures: [test name — reason]

## Summary
- Total issues: N
- Auto-fixed: M
- Remaining: K
```

## Rules

- Each tool runs individually before project scripts
- Never skip a step — report all results even if one fails
- Auto-fix only safe transformations (formatting, obvious lint fixes)
- After auto-fix, re-run ALL checks, not just the fixed one
