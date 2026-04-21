---
description: Generate, lint, vulncheck, staticcheck, and test with auto-fix
---

# Verify Project

Run the full verification pipeline for `$ARGUMENTS` (or current working directory if not specified). Detect the project type automatically and execute the appropriate toolchain. Fix any issues found and re-verify until clean or the issue requires human input.

## Steps

### 1. Detect Project Type

Use `glob` to detect the project type by looking for build manifests:

| Manifest | Project Type |
|----------|--------------|
| `go.mod` | Go |
| `package.json` / `pnpm-lock.yaml` / `yarn.lock` | Node/TypeScript |
| `Cargo.toml` | Rust |
| `pom.xml` | Java (Maven) |
| `build.gradle` / `build.gradle.kts` | Java (Gradle) |
| `pyproject.toml` / `setup.py` / `requirements.txt` | Python |
| `Gemfile` | Ruby |
| `composer.json` | PHP |
| `*.csproj` / `*.sln` | C# (.NET) |
| `Package.swift` | Swift |
| `*.kts` / `build.gradle.kts` | Kotlin |

If no recognized manifest is found, ask the user via `question` to specify the project type or provide guidance.

### 2. Run Verification Pipeline

Execute the following steps using `execute`. Set `$TARGET` to `$ARGUMENTS` if provided, otherwise `.` (current working directory). Run each step sequentially — stop on the first failure, fix, then restart from that step.

For compiled languages (Go, Rust, Java, C#), append the appropriate path suffix for recursive operations where applicable.

#### Go
1. `go generate $TARGET/...`
2. `golangci-lint run --fix $TARGET/...` (or equivalent)
3. `govulncheck $TARGET/...`
4. `staticcheck $TARGET/...`
5. `go test -v -race $TARGET/...`

#### Node/TypeScript
1. Install dependencies (use appropriate package manager)
2. Run formatter/linter with auto-fix
3. Build if build script exists
4. Run tests

#### Rust
1. `cargo clippy --fix --allow-dirty`
2. `cargo fmt`
3. `cargo build`
4. `cargo test`

#### Java (Maven)
1. `mvn spotless:apply`
2. `mvn compile`
3. `mvn test`

#### Java (Gradle)
1. Apply formatting
2. `build`
3. `test`

#### Python
1. `ruff check --fix .`
2. `ruff format .`
3. Type check if configured
4. Run tests

#### Ruby
1. `bundle exec rubocop -A`
2. Run specs

#### PHP
1. Install dependencies if composer.json present
2. Run code style fixer
3. Run static analysis if configured
4. Run unit tests

#### C# (.NET)
1. `dotnet format --verify-no-changes` (or `dotnet build`)
2. `dotnet test`

#### Swift
1. Format if configured
2. `swift build`
3. `swift test`

#### Kotlin
1. Format
2. `build`
3. `test`

### 3. Large Project Mode

If `$TARGET` contains more than 100 source files (detected via `glob`), run verification in batches to avoid timeouts and resource exhaustion:

1. Divide source files into groups of 50 files each.
2. Run the pipeline on each batch sequentially.
3. Aggregate results and report any failures with batch context.

This mode can be disabled by setting `$LARGE_PROJECT_MODE=false`.

### 4. Tool Availability Check

Before running each step, check if the required tool is installed:

1. Attempt to invoke the tool with `--version` or `version` flag.
2. If the tool is not found:
   - Report which tool is missing
   - Ask the user via `question` whether to skip this step or install the tool
   - If user confirms skip, proceed to next step
   - If user provides installation instructions, execute them and retry

### 5. Auto-Fix Loop

If any step fails:

1. Read the error output carefully.
2. Fix the issue using `edit` or `write`.
3. Re-run only the failed step (not the full pipeline).
4. If the same step fails 3 times, report the issue to the user and ask how to proceed via `question`.

### 6. Report

When all steps pass, output a brief summary:

```
✓ generate — passed
✓ lint — passed (N issues auto-fixed)
✓ vulncheck — passed
✓ staticcheck — passed
✓ test — passed (M tests, 0 failures)
```

For large project mode, include batch statistics:

```
✓ batch 1/N — passed (X files)
✓ batch 2/N — passed (Y files)
...
✓ all N batches — passed (total M files)
```