---
description: Format, lint, type-check, scan, and test the project
agent: debug
---

You are running a full verification pass on the codebase. Execute each step in order; report PASS/FAIL/SKIP per step.

## Context

Detected project files:
!`ls package.json Cargo.toml go.mod pyproject.toml Makefile build.gradle pom.xml 2>/dev/null | head -10`

Current git status:
!`git status --short 2>/dev/null || echo "Not a git repo"`

## Scope

$ARGUMENTS (positional: `$1` = specific files or directories to focus on; optional).

## Pipeline (in order)

1. **Format** — run project formatter. Skip if none configured.
2. **Lint** — run project linter. Report warnings/errors.
3. **Type-check** — run type checker if available.
4. **Security scan** — run configured scanner.
5. **Test** — run full test suite, git hooks test. Report pass/fail with file:line refs for failures.
6. **Fix** — apply tool auto-fixers first, then fix root cause manually. Do NOT break public API.
7. **Verify** — re-run only the failing check to confirm fix before proceeding.
8. **Summary** — report each step outcome. List unresolved issues with file:line refs.

## Fix/Verify Loop

When a step fails:
1. Apply auto-fix if available (formatter, linter --fix, etc.).
2. If manual fix needed, make smallest change possible.
3. Re-run the failing step to confirm.
4. Only proceed when step passes.

## Invariants

- Use exact commands the project is configured with. Don't invent new toolchains.
- If a tool is not installed, SKIP and continue. Don't abort pipeline.
- Every failure must include a file:line reference. No dangling issue reports.
- After manual fixes, always check `git diff` to verify only intended changes.
- Sync verification findings back to specs if they reveal spec issues.

## Rules

- **Handle errors deliberately**: check every error, handle where possible, propagate otherwise.
- **Make invalid states unrepresentable**: validate at boundaries.
- **Test first**: tests are living documentation, not afterthought.
- **Traceability**: every issue links to a specific file:line.
- **Measure, don't guess**: if performance is in scope, benchmark before optimizing.
