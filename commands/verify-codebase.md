---
description: Format, lint, type-check, scan, and test the project
---

Run a full verification pass. Execute each step in order; report PASS/FAIL/SKIP per step.

## Context
Detected project files:
!`ls package.json Cargo.toml go.mod pyproject.toml Makefile build.gradle pom.xml 2>/dev/null | head -10`

Current git status:
!`git status --short 2>/dev/null || echo "Not a git repo"`

## Pipeline (in order)
1. **Format** — Run project formatter. Skip if none configured.
2. **Lint** — Run project linter. Report warnings/errors.
3. **Type-check** — Run type checker if available.
4. **Security scan** — Run configured scanner.
5. **Test** — Run full test suite. Report pass/fail with file:line refs for failures.
6. **Fix** — Apply tool auto-fixers first, then fix root cause manually. Do NOT break public API.
7. **Verify** — Re-run only the failing check to confirm fix before proceeding.
8. **Summary** — Report each step outcome. List unresolved issues with file:line refs.

## Invariants
- Use exact commands project is configured with. Don't invent new toolchains.
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