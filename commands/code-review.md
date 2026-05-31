---
description: Review code changes for quality, security, and performance issues
agent: plan
---

You are reviewing code changes for quality, security, and performance issues.

## Context

Detected project:
!`ls package.json Cargo.toml go.mod pyproject.toml Makefile build.gradle pom.xml 2>/dev/null | head -10`

Git state:
!`git diff --stat HEAD 2>/dev/null || echo "No git repo or clean working tree"`

## Parameters

$ARGUMENTS

Positional: `$1` = target (files, directories, or branch; e.g., `./src`, `main.go`, `HEAD~1`), `$2` = focus (`full`, `security`, `performance`; default: `full`), `$3` = base branch for comparison (default: `main` or `develop`).

If `$1` is not provided, ask the user for the target, focus, and base branch before proceeding.

## Steps

1. **Detect language and gather changes**
   - Identify manifest files (`go.mod`, `package.json`, `pyproject.toml`, etc.).
   - Determine files to review from `git diff` or the target parameter.
   - Log detected language and file count.

2. **Run static analysis**
   - Execute language-appropriate linter (`golangci-lint`, `ruff`, `eslint`, etc.).
   - Check formatting (`gofmt`, `black`, `prettier`, etc.).
   - Log all errors and formatting issues.

3. **Security scanning**
   - Run language-specific security scanner (`govulncheck`, `pip-audit`, `npm audit`, etc.).
   - Search for hardcoded secrets, API keys, tokens.
   - Categorize vulnerabilities by severity: Critical, High, Medium, Low.

4. **Code inspection**
   - Search for: `TODO`, `FIXME`, `XXX`, `BUG`, debug statements.
   - Review changed files for:
     - Security issues (P0): input validation, hardcoded secrets.
     - Correctness issues (P1): business logic, error handling.
     - Performance issues (P2): allocations, queries, concurrency.
     - Maintainability (P2): function size, documentation, naming.

5. **Generate report**
   - Format findings using priority framework (P0–P3).
   - Provide clear recommendation: Approve, Request Changes, or Block.
   - Include assessment table: Correctness, Security, Performance, Maintainability, Testing.

## Completion Criteria

- Language detected and appropriate tools executed.
- Static analysis completed with results logged.
- Security scan completed with vulnerabilities categorized.
- All changed files reviewed.
- Issues categorized with P0–P3 priorities.
- Report generated with clear recommendation.

## Troubleshooting

- **Linter not found**: install via package manager or skip with warning.
- **Security scanner fails**: report vulnerability details and continue.
- **Large diff (>50 files)**: focus on critical files, suggest incremental review.
- **Unknown language**: fall back to generic patterns (secrets, TODOs) only.
