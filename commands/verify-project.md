---
description: Verify project health — lint, security scan, and test with auto-fix
---

# /verify-project

Run the full verification pipeline to check code quality, security, and correctness. Auto-fix issues where possible.

## Steps

1. **Detect** — Identify project language and select toolchain
2. **Generate** — Run code generation to ensure derived files are up to date
3. **Lint** — Run linter with `--fix` to auto-correct style and common issues
4. **Static Pre-check** — Run static analysis to find fixable issues, then auto-fix them
5. **Security** — Scan for known vulnerabilities in dependencies
6. **Static Analysis** — Run final static analysis pass to confirm clean
7. **Test** — Clear test cache and run full test suite
8. **Report** — Summarize findings, fixed issues, and remaining failures

## Language Detection

Detect project language by checking for lock/manifest files in priority order:

| Priority | File            | Language        |
|----------|-----------------|-----------------|
| 1        | `go.mod`        | Go              |
| 2        | `Cargo.toml`    | Rust            |
| 3        | `package.json`  | JavaScript/Node |
| 4        | `requirements.txt` or `pyproject.toml` | Python |
| 5        | `pom.xml`       | Java            |
| 6        | `Gemfile`       | Ruby            |

## Toolchain Matrix

Set tool variables based on detected language:

| Phase       | Go                    | Rust                  | JavaScript/Node       | Python              | Java              | Ruby              |
|-------------|-----------------------|-----------------------|-----------------------|---------------------|-------------------|-------------------|
| Generate    | `go generate ./...`   | `cargo build`         | `npm run generate`    | —                   | `mvn generate-sources` | `rake generate` |
| Lint        | `golangci-lint run --fix` | `cargo clippy --fix` | `eslint --fix`        | `ruff check --fix`  | `checkstyle`      | `rubocop -a`      |
| Static      | `staticcheck`         | `cargo clippy`        | `tsc --noEmit`        | `mypy`              | `spotbugs`        | `rubocop`         |
| Security    | `govulncheck`         | `cargo audit`         | `npm audit`           | `pip-audit`         | `owasp-dependency-check` | `bundler-audit` |
| Test        | `go test -race ./...` | `cargo test`          | `jest --coverage`     | `pytest -v`         | `mvn test`        | `rake test`       |
| Test Clear  | `go clean -testcache` | —                     | `jest --clearCache`   | `pytest --cache-clear` | `mvn clean test` | `rake tmp:clear`  |

## Execution

Run each phase sequentially; stop and report on first failure:

```bash
# Phase 1: Detect language and set tool variables
# (agent determines language from manifest files above)

# Phase 2: Generate
$GENERATE_CMD

# Phase 3: Lint with auto-fix
$LINT_CMD --fix ./...

# Phase 4: Static pre-check — find fixable issues
$STATIC_CMD ./...

# If fixable issues found (see Auto-Fix Rules below), fix them, then re-run:
$STATIC_CMD ./...

# Phase 5: Security scan
$SECURITY_CMD ./...

# Phase 6: Final static check (must pass clean)
$STATIC_CMD ./...

# Phase 7: Test
$TEST_CLEAR_CMD 2>/dev/null || true  # Some languages have no clear command
$TEST_CMD
```

## Auto-Fix Rules

When static analysis or linters report these fixable issues, correct them automatically:

### Doc Comment Style (all languages)

| Pattern | Fix |
|---------|-----|
| Doc comment doesn't start with the declared name | Rewrite to start with the function/type/variable name |

**Go example (ST1020/ST1021):**
```go
// Before: Run starts the consumer loop
// After:  ConsumerRun starts the consumer loop
func ConsumerRun() { ... }
```

**JavaScript/TypeScript example:**
```ts
// Before: handles user authentication
// After:  authenticateUser validates credentials and returns a session
function authenticateUser(creds: Credentials): Session { ... }
```

**Python example:**
```python
# Before: calculates the total price
# After:  calculate_total computes the final price including tax
def calculate_total(items: list[Item]) -> float: ...
```

**Rust example:**
```rust
// Before: creates a new connection pool
// After:  ConnectionPool creates a new pool with the given config
impl ConnectionPool {
    pub fn new(config: Config) -> Self { ... }
}
```

### Unused Imports/Variables
- Remove unused imports, variables, and dead code when safe to do so

### Formatting
- Apply language formatter: `gofmt`, `cargo fmt`, `prettier`, `black`, `rustfmt`

## Principles

- **Auto-fix first** — Let tools correct what they can before reporting
- **Fix mechanical issues** — Doc comment style, formatting, and unused imports are always safe to auto-correct
- **Fail fast** — Surface errors early; don't cascade failures
- **Clean slate** — Always clear test cache before running tests
- **Race detection** — Run tests with race detection when the language supports it
- **Zero tolerance** — Treat warnings as errors; fix or explicitly suppress with justification
