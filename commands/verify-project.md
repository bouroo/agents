---
description: Verify project — format, lint (auto-fix), vulnerability scan, static analysis, and run tests. Language-agnostic.
agent: general
subtask: true
---

# Verify Project

Run a full verification pipeline on the current project: format, lint with auto-fix, vulnerability scan, static analysis, and test suite. The language is detected automatically from project markers.

## Steps

### 1. Initialize Tracking

Use `todowrite` to create a task list:
- Detect project language(s)
- Run code generation (if applicable)
- Format and lint with auto-fix
- Vulnerability scan
- Static analysis / type check
- Run test suite
- Fix issues, if any
- Report results

### 2. Detect Project Language

Use `glob` and `read` to identify the project language by checking for marker files in the project root:

| Marker File(s) | Language |
|---|---|
| `go.mod` | Go |
| `package.json` | TypeScript / JavaScript |
| `Cargo.toml` | Rust |
| `pom.xml` or `build.gradle` / `build.gradle.kts` | Java / Kotlin |
| `pyproject.toml`, `setup.py`, `setup.cfg`, `requirements.txt` | Python |
| `Gemfile` | Ruby |
| `composer.json` | PHP |
| `*.sln`, `*.csproj` | C# / .NET |

If multiple languages are detected, run the pipeline for each. Use `$ARGUMENTS` as a target path override if provided (default: `.`).

### 3. Run Pipeline per Language

Execute each stage **in order**. If a stage fails, attempt auto-fix and re-run once. If still failing, report the error and continue to the next stage.

---

#### Go

```bash
# Code generation
go generate ./...

# Format
gofmt -w .

# Lint with auto-fix
go run github.com/golangci/golangci-lint/v2/cmd/golangci-lint@latest run --fix ./...

# Vulnerability scan
go run golang.org/x/vulncheck/cmd/govulncheck@latest ./...

# Static analysis
go run honnef.co/go/tools/cmd/staticcheck@latest ./...

# Run tests with race detection
go clean -testcache && go test -v -race ./...
```

---

#### TypeScript / JavaScript

Detect the package manager first: check for `pnpm-lock.yaml`, `yarn.lock`, `bun.lockb`, then fall back to `npm`.

```bash
# Install dependencies if needed
<npm|pnpm|yarn|bun> install

# Format and lint with auto-fix (prefer biome if configured, else eslint+prettier)
npx @biomejs/biome check --fix --unsafe .                            # if biome.json exists
npx eslint --fix . && npx prettier --write .                          # if .eslintrc* / eslint.config.* exists

# Type check
npx tsc --noEmit                                                      # if tsconfig.json exists

# Vulnerability scan
<npm|pnpm|yarn> audit                                                 # or: npx better-npm-audit audit
npx better-npm-audit audit                                            # if available

# Run tests
npx vitest run --coverage                                             # if vitest configured
npx jest --coverage                                                   # if jest configured
```

---

#### Rust

```bash
# Format
cargo fmt

# Lint with auto-fix
cargo clippy --fix --allow-dirty --allow-staged

# Vulnerability scan (install if missing)
cargo audit

# Run tests
cargo clean && cargo test --all-features
```

---

#### Java / Kotlin (Maven)

```bash
# Format
mvn spotless:apply                                                    # if spotless plugin configured
mvn fmt:format                                                        # if fmt plugin configured

# Compile and analyze
mvn compile                                                           # fail fast on syntax errors
mvn spotbugs:check                                                    # if spotbugs plugin configured
mvn pmd:check                                                         # if pmd plugin configured

# Vulnerability scan
mvn org.owasp:dependency-check:check                                  # if OWASP plugin configured

# Run tests
mvn test
```

#### Java / Kotlin (Gradle)

```bash
# Format
./gradlew spotlessApply                                               # if spotless plugin configured

# Compile, lint, and test
./gradlew clean check
```

---

#### Python

```bash
# Format
ruff format .                                                         # or: black .
ruff check --fix --unsafe-fixes .                                     # or: autoflake --fix-all --remove-all-unused-imports

# Type check
mypy .                                                                # or: pyright

# Vulnerability scan
pip-audit                                                             # or: safety check

# Run tests
pytest -v --tb=short                                                  # with coverage if configured
```

---

#### Ruby

```bash
# Format and lint with auto-fix
bundle exec rubocop -A

# Vulnerability scan
bundle audit

# Run tests
bundle exec rspec                                                     # or: bundle exec minitest
```

---

#### PHP

```bash
# Format
vendor/bin/php-cs-fixer fix                                           # or: vendor/bin/pint

# Static analysis
vendor/bin/phpstan analyse                                            # or: vendor/bin/psalm

# Vulnerability scan
composer audit

# Run tests
vendor/bin/pest --parallel                                            # or: vendor/bin/phpunit
```

---

#### C# / .NET

```bash
# Format
dotnet format

# Vulnerability scan
dotnet list package --vulnerable --include-transitive

# Run tests
dotnet clean && dotnet test --verbosity normal
```

---

### 4. Handle Failures

For each stage that fails:

1. **Read the error output** carefully. Use `read` to inspect relevant source files if needed.
2. **Auto-fix**: The commands above include auto-fix flags (`--fix`, `-A`, `--fix --unsafe-fixes`, etc.). If the first pass fails, the auto-fix should resolve it.
3. **Re-run** the failing stage once after auto-fix.
4. **If still failing**: Use `edit` to manually fix the issue if the cause is straightforward and obvious (e.g., missing import, unused variable). Do NOT refactor or redesign code — only fix what prevents the pipeline from passing.
5. **Report remaining failures** in the final summary.

### 5. Report Results

Output a structured summary:

```markdown
## Verify Project Report

### Language(s) Detected
- <language> (<evidence>)

### Pipeline Results

| Stage | Status | Details |
|---|---|---|
| Code Generation | ✅ / ❌ / ⏭️ | <output summary> |
| Format & Lint | ✅ / ❌ / ⏭️ | <output summary> |
| Vulnerability Scan | ✅ / ❌ / ⏭️ | <output summary> |
| Static Analysis | ✅ / ❌ / ⏭️ | <output summary> |
| Tests | ✅ / ❌ / ⏭️ | <output summary> |

### Issues Found
<detailed list of any failures or warnings>

### Verdict
<PASS — all stages green | PARTIAL — some non-critical issues | FAIL — blocking issues require attention>
```

### 6. Completion

Mark all tasks complete in `todowrite`.

## Notes

- `⏭️` means the stage was skipped (e.g., tool not installed, no config file present). Never skip silently — always note why.
- All `bash` commands must run from the project root directory unless `$ARGUMENTS` specifies a subpath.
- For monorepos with multiple languages, run the full pipeline for each detected language.
- Do NOT install global tools that aren't already present. If a tool is missing, note it in the report and skip that stage.
- Auto-fix changes are applied directly to the source files. The user should review changes after the command completes.

Trigger this workflow by typing `/verify-project` in the chat. Pass an optional path: `/verify-project ./pkg/server`.
