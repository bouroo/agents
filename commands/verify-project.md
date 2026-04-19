---
description: Generate, lint, vulncheck, staticcheck, and test with auto-fix
---

# Verify Project

Run the full verification pipeline for `$ARGUMENTS` (or current working directory if not specified). Detect the language ecosystem automatically and execute the appropriate toolchain. Fix any issues found and re-verify until clean or the issue requires human input.

## Steps

### 1. Detect Ecosystem

Use `glob` to detect the project type:

- `go.mod` present → Go
- `package.json` present → Node/TypeScript
- `Cargo.toml` present → Rust
- `pom.xml` / `build.gradle` present → Java
- `pyproject.toml` / `setup.py` / `requirements.txt` present → Python
- No recognized manifest → ask the user via `question`

### 2. Run Verification Pipeline

Execute the following steps using `bash`. Set `$TARGET` to `$ARGUMENTS` if provided, otherwise `.` (current working directory). For Go projects, append `/...` to `$TARGET` when running go commands. Run each step sequentially — stop on the first failure, fix, then restart from that step.

#### Go

1. `go generate $TARGET/...`
2. `go run github.com/golangci/golangci-lint/v2/cmd/golangci-lint@latest run --fix $TARGET/...`
3. `govulncheck $TARGET/...`
4. `staticcheck $TARGET/...`
5. `go clean -testcache && go test -v -race $TARGET/...`

#### Node/TypeScript

1. `npm install` (or `pnpm install` / `yarn` based on lockfile)
2. `npx biome check --write .` (or project-configured linter: eslint --fix, prettier --write)
3. `npm run build` (if build script exists)
4. `npm test` (or `vitest run` / `jest --ci`)

#### Rust

1. `cargo clippy --fix --allow-dirty`
2. `cargo fmt`
3. `cargo build`
4. `cargo test`

#### Java

1. `mvn spotless:apply` (or `./gradlew spotlessApply`)
2. `mvn compile` (or `./gradlew build`)
3. `mvn test` (or `./gradlew test`)

#### Python

1. `ruff check --fix .`
2. `ruff format .`
3. `mypy .` (if configured)
4. `pytest` (or `python -m pytest`)

### 3. Auto-Fix Loop

If any step fails:

1. Read the error output carefully.
2. Fix the issue using `edit` or `write`.
3. Re-run only the failed step (not the full pipeline).
4. If the same step fails 3 times, report the issue to the user and ask how to proceed via `question`.

### 4. Report

When all steps pass, output a brief summary:

```
✓ generate — passed
✓ lint — passed (N issues auto-fixed)
✓ vulncheck — passed
✓ staticcheck — passed
✓ test — passed (M tests, 0 failures)
```
