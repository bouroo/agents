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

Positional: $1 (target), $2 (focus: full|security|performance), $3 (base branch)

If not provided, ask user for:
- **target**: Files, directories, or branch to review (e.g., `./src`, `main.go`, `HEAD~1`)
- **focus**: `full`, `security`, or `performance` (default: `full`)
- **base**: Base branch for comparison (default: main or develop)

## Steps

1. **Detect language and gather changes**
   - Identify manifest files (go.mod, package.json, pyproject.toml, etc.)
   - Determine files to review from git diff or target parameter
   - Log detected language and file count

2. **Run static analysis**
   - Execute language-appropriate linter (golangci-lint, ruff, eslint, etc.)
   - Check formatting (gofmt, black, prettier, etc.)
   - Log all errors and formatting issues

3. **Security scanning**
   - Run language-specific security scanner (govulncheck, pip-audit, npm audit, etc.)
   - Search for hardcoded secrets, API keys, tokens using grep
   - Categorize vulnerabilities by severity (Critical/High/Medium/Low)

4. **Code inspection**
   - Search for: TODO, FIXME, XXX, BUG, debug statements
   - Review changed files for:
     - Security issues (P0): Input validation, hardcoded secrets
     - Correctness issues (P1): Business logic, error handling
     - Performance issues (P2): Allocations, queries, concurrency
     - Maintainability (P2): Function size, documentation, naming

5. **Generate report**
   - Format findings using priority framework (P0-P3)
   - Provide clear recommendation (Approve/Request Changes/Block)
   - Include assessment table: Correctness, Security, Performance, Maintainability, Testing

## Completion Criteria

- Language detected and appropriate tools executed
- Static analysis completed with results logged
- Security scan completed with vulnerabilities categorized
- All changed files reviewed
- Issues categorized with P0-P3 priorities
- Report generated with clear recommendation

## Troubleshooting

- **Linter not found**: Install via package manager or skip with warning
- **Security scanner fails**: Report vulnerability details and continue
- **Large diff (>50 files)**: Focus on critical files, suggest incremental review
- **Unknown language**: Fall back to generic patterns (secrets, TODOs) only