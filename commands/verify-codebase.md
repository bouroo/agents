---
description: Format, lint, type-check, scan, and test the project
---

You are running a full verification pass on the project. Execute each step in order and report results.

## Steps

1. **Format**: Run the project's formatter. If no formatter is configured, skip with a note.
2. **Lint**: Run the project's linter. Report any warnings or errors.
3. **Type-check**: Run the project's type checker (if applicable). Report any type errors.
4. **Security scan**: Run any configured security scanner (gosec, npm audit, etc.).
5. **Test**: Run the full test suite. Report pass/fail counts and any failures.
6. **Summary**: Report overall status. List any issues found with file:line references.

## Detection

Check for common tool configurations:
- **Go**: `gofmt`, `go vet`, `golangci-lint`, `go test ./...`
- **TypeScript/JS**: `prettier`, `eslint`, `tsc --noEmit`, `npm test`
- **Python**: `black`/`ruff format`, `ruff`/`flake8`/`pylint`, `mypy`, `pytest`
- **Rust**: `cargo fmt`, `cargo clippy`, `cargo test`
- **Java**: Check for Maven/Gradle configs, use appropriate commands.

## Rules

- Use the exact commands the project is configured with. Don't invent new toolchains.
- If a tool is not installed, note it and move on. Don't fail the whole pipeline.
- Report each step's outcome clearly: PASS / FAIL / SKIP (reason).
- If tests fail, include the failure output with file:line references.
- Don't fix issues — just report them. The user decides what to fix.
