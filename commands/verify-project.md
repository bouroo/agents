---
description: Generate, lint, vulncheck, staticcheck, and test with auto-fix
---

# Verify Project

Run the full verification pipeline for `$ARGUMENTS` (or current working directory if not specified). Detect the language ecosystem automatically and execute the appropriate toolchain. Fix any issues found and re-verify until clean or the issue requires human input.

## Steps

### 1. Detect Ecosystem

Use `glob` to detect the project type:

| Manifest | Ecosystem |
|----------|-----------|
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

Execute the following steps using `bash`. Set `$TARGET` to `$ARGUMENTS` if provided, otherwise `.` (current working directory). Run each step sequentially — stop on the first failure, fix, then restart from that step.

For compiled languages (Go, Rust, Java, C#), append the appropriate path suffix for recursive operations where applicable.

#### Go

1. `go generate $TARGET/...`
2. `golangci-lint run --fix $TARGET/...` (or `go run github.com/golangci/golangci-lint/v2/cmd/golangci-lint@latest run --fix $TARGET/...`)
3. `govulncheck $TARGET/...`
4. `staticcheck $TARGET/...`
5. `go test -v -race $TARGET/...`

#### Node/TypeScript

1. `npm install` (or `pnpm install` / `yarn install` based on lockfile presence)
2. `npx biome check --write .` (or `eslint --fix . && prettier --write .`)
3. `npm run build` (if build script exists)
4. `npm test` (or `vitest run` / `jest --ci`)

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

1. `./gradlew spotlessApply`
2. `./gradlew build`
3. `./gradlew test`

#### Python

1. `ruff check --fix .`
2. `ruff format .`
3. `mypy .` (if configured, skip otherwise)
4. `pytest` (or `python -m pytest`)

#### Ruby

1. `bundle exec rubocop -A`
2. `bundle exec rake spec` (or `bundle exec rspec`)

#### PHP

1. `composer install` (if composer.json present)
2. `./vendor/bin/phpcs --standard=PSR12 --colors --fix .` (or `php-cs-fixer fix .`)
3. `./vendor/bin/phpstan analyse .` (if configured)
4. `./vendor/bin/phpunit` (or `php phpunit.phar`)

#### C# (.NET)

1. `dotnet format --verify-no-changes` (or `dotnet build`)
2. `dotnet test`

#### Swift

1. `swiftformat .` (if configured)
2. `swift build`
3. `swift test`

#### Kotlin

1. `./gradlew ktlintFormat` (or `ktlint --format .`)
2. `./gradlew build`
3. `./gradlew test`

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
