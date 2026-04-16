---
description: Verify project health — lint, security scan, and test with auto-fix
---

# /verify-project

Run the full verification pipeline to check code quality, security, and correctness. Auto-fix issues where possible.

## Steps

1. **Generate** — Run code generation to ensure derived files are up to date
2. **Lint** — Run linter with `--fix` to auto-correct style and common issues
3. **Security** — Scan for known vulnerabilities in dependencies
4. **Static Analysis** — Run static analyzer for deeper code quality checks
5. **Test** — Clear test cache and run full test suite with race detection
6. **Report** — Summarize findings, fixed issues, and remaining failures

## Execution

Run each phase sequentially; stop and report on first failure:

```
go generate ./...
go run github.com/golangci/golangci-lint/v2/cmd/golangci-lint@latest run --fix ./...
govulncheck ./...
staticcheck ./...
go clean -testcache && go test -v -race ./...
```

## Principles

- **Auto-fix first** — Let tools correct what they can before reporting
- **Fail fast** — Surface errors early; don't cascade failures
- **Clean slate** — Always clear test cache before running tests
- **Race detection** — Run tests with `-race` to catch concurrency bugs
- **Zero tolerance** — Treat warnings as errors; fix or explicitly suppress with justification

## Language Adaptation

For non-Go projects, substitute equivalent tools:

| Phase       | Go                    | JavaScript/Node       | Python              | Rust             |
|-------------|-----------------------|-----------------------|---------------------|------------------|
| Generate    | `go generate`         | `npm run generate`    | —                   | `cargo build`    |
| Lint        | `golangci-lint --fix` | `eslint --fix`        | `ruff check --fix`  | `clippy --fix`   |
| Security    | `govulncheck`         | `npm audit`           | `pip-audit`         | `cargo audit`    |
| Static      | `staticcheck`         | `tsc --noEmit`        | `mypy`              | `cargo clippy`   |
| Test        | `go test -race`       | `jest --coverage`     | `pytest -v`         | `cargo test`     |

Detect project language from lock files (`go.mod`, `package.json`, `requirements.txt`, `Cargo.toml`) and run the appropriate toolchain.
