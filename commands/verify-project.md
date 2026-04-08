---
description: Validate project health, deps, lint, security, and tests with auto-fix
agent: code
subtask: true
---

# Verify Project

Run a comprehensive health check on the project with automatic fixing where possible. Use `$ARGUMENTS` to scope to a specific directory or module, or check the entire project if omitted.

**Auto-Fix Mode**: Attempts to fix issues automatically before reporting. Use `--no-fix` flag to run in report-only mode.

## Steps

### 1. Structure

- Use `glob` and `read` to map project layout.
- Verify expected directories exist (`src/`, `pkg/`, `cmd/`, `internal/`, or language-equivalent).
- Check for configuration files (`go.mod`, `package.json`, `Cargo.toml`, `pyproject.toml`, etc.).

### 2. Dependencies

- Run the dependency manager (`go mod verify`, `npm audit`, `cargo audit`, `pip audit`, or equivalent).
- Check for outdated or vulnerable dependencies.
- **Auto-fix**: Run fix commands when available:
  - Go: `go mod tidy`
  - npm: `npm audit fix` (or `npm audit fix --force` for breaking changes)
  - pip: `pip install --upgrade <package>`
  - Rust: `cargo update` for non-breaking updates
- Report any lockfile drift that cannot be auto-fixed.

### 3. Build

- Run the build command (`go build ./...`, `npm run build`, `cargo build`, or equivalent).
- Report compile errors with file and line numbers.

### 4. Lint & Format

- Run the project's linter (`golangci-lint run`, `eslint .`, `cargo clippy`, `ruff check`, or equivalent).
- Run the formatter in check mode (`gofmt -d .`, `prettier --check .`, `cargo fmt --check`, or equivalent).
- **Auto-fix**: Apply fixes where supported:
  - Go: `gofmt -w .`, `golangci-lint run --fix`
  - TypeScript/JS: `eslint . --fix`, `prettier --write .`
  - Rust: `cargo clippy --fix --allow-staged`, `cargo fmt`
  - Python: `ruff check --fix`, `ruff format`, `black .`
- Report violations that cannot be auto-fixed, grouped by rule/type with file paths and line numbers.

### 5. Security

- Scan for hardcoded secrets, API keys, tokens using `grep` for common patterns:
  ```
  grep -rniE '(password|secret|api_key|token|private_key)\s*[:=]' --include='*.go' --include='*.ts' --include='*.py'
  ```
- Check for known vulnerability patterns (SQL injection, path traversal, unsafe deserialization).
- **Auto-fix**: For fixable security issues:
  - Replace hardcoded secrets with environment variable references or placeholder markers
  - Add `.env` to `.gitignore` if missing
  - Generate `.env.example` with placeholder names (no actual values)
  - Flag complex issues (SQL injection, path traversal) for manual review with specific file/line references

### 6. Tests

- Run the full test suite with coverage:
  - Go: `go test -cover -race ./...`
  - Node: `npm test -- --coverage`
  - Rust: `cargo test`
  - Python: `pytest --cov`
- **Auto-fix**: For common test failures:
  - Race conditions: re-run with `-count=3` to confirm flakiness; if confirmed, flag for manual review
  - Timeout failures: increase timeout if test involves I/O or network calls
  - Missing test files: if build/imports reference missing test files, create stub test file with package declaration
- Report:
  - Total tests, passed, failed, skipped
  - Coverage percentage (target >80% for business logic)
  - Any flaky or race-condition failures that require manual intervention

### 7. Auto-Fix Summary

After each fixable issue is addressed, re-run the relevant check to verify the fix succeeded.

Track auto-fix results:
```
## Auto-Fix Summary

| Check        | Issues Found | Fixed | Remaining | Status |
|-------------|--------------|-------|-----------|--------|
| Dependencies| N            | N     | 0         | ✓      |
| Lint        | N            | N     | M         | !      |
| Security    | N            | N     | M         | !      |
| Tests       | N            | N     | M         | !      |
```

### 8. Report

Output a structured health report:

```
## Project Health: <PASS|WARN|FAIL>

| Check        | Status | Details                          |
|-------------|--------|----------------------------------|
| Structure   | ✓/✗/!  | <summary>                        |
| Dependencies| ✓/✗/!  | <summary> (auto-fixed: N issues) |
| Build       | ✓/✗/!  | <summary>                        |
| Lint        | ✓/✗/!  | <summary> (auto-fixed: N issues) |
| Security    | ✓/✗/!  | <summary> (auto-fixed: N issues) |
| Tests       | ✓/✗/!  | <summary>                        |

### Action Items
1. [CRITICAL] ... (requires manual fix)
2. [WARNING] ... (auto-fix attempted, see file:line)
3. [INFO] ... (suggestion for improvement)

### Auto-Fix Applied
- Dependencies: `npm audit fix` - 3 vulnerabilities resolved
- Lint: `eslint --fix` - 12 formatting issues resolved, 2 manual fixes needed
- Security: Replaced 2 hardcoded values with env var placeholders
```

**PASS** = all checks green. **WARN** = non-blocking issues or auto-fix applied successfully. **FAIL** = blocking issues remain (build errors, test failures, unfixable security vulnerabilities).

## Principles

- Fail fast: run quick checks (structure, lint) before slow ones (tests, security audit).
- Be language-agnostic: detect the project's language and toolchain, then use the right commands.
- Report actionable items only — skip noise, include file paths and fix suggestions.
- Auto-fix first: attempt automatic fixes before reporting issues; only flag items requiring manual intervention.
- Safe defaults: never auto-fix without verification; re-run checks after each fix to confirm resolution.
- Preserve intent: when replacing secrets or modifying code, maintain the original functionality while removing the vulnerability.
