---
description: Detect project type, run verification pipeline with auto-fix
---

# Verify Project

Run the full verification pipeline for $ARGUMENTS (or current working directory if not specified). Detect the project type automatically and execute the appropriate toolchain. Fix any issues found and re-verify until clean or the issue requires human input.

> **Conductor note**: You do NOT execute steps directly. Decompose this command into the subtasks below, delegate each to the correct subagent, and validate every deliverable before proceeding.

## Constraints

- Every step in the pipeline must be attempted. Do not skip steps because earlier ones failed.
- Auto-fix is mandatory for fixable issues. Only escalate to the user after 3 failed fix attempts on the same issue.
- The pipeline is complete only when build and test steps pass.

## Phase 1 — Discovery

### 1.1 Detect project type and toolchain
- **Agent**: `explorer`
- **Task**: Scan the project root for build manifests, lock files, and configuration files. Determine the project type, build system, and available verification tools (linters, formatters, test runners, security scanners, static analyzers).
- **Deliverable**: Project type, build system, and list of detected verification tools/commands.
- **Gate**: If no recognized manifest is found, ask the user via `question` for the project type before proceeding.

### 1.2 Determine verification commands
- **Agent**: `implementer`
- **Task**: Read the build manifest and config files. Identify the standard commands for: generate, lint (with auto-fix), format, security scan, static analysis, build, test.
- **Deliverable**: Exact command list for each verification step.

## Phase 2 — Verification Pipeline

Set `$TARGET` to $ARGUMENTS if provided, otherwise `.` (current working directory).

### 2.1 Run generate
- **Agent**: `implementer`
- **Task**: Run code generation if configured (e.g., protobuf, OpenAPI, schema generation).
- **Deliverable**: Generate output or confirmation that no generation is needed.

### 2.2 Run lint with auto-fix
- **Agent**: `implementer`
- **Task**:
  1. Run the project's linter with auto-fix enabled.
  2. Re-run the linter in check mode (without auto-fix) to verify zero issues remain.
  3. If issues remain, treat this as a failure and enter Phase 3.
  Record issues found, fixes applied, and any remaining issues.
- **Deliverable**: Lint result. Must report zero issues before proceeding.
- **Note for Go/golangci-lint**: `golangci-lint run --fix` does not auto-fix `staticcheck` duplicate import errors (ST1019). These must be manually fixed by consolidating duplicate imports into a single alias.

### 2.3 Run format
- **Agent**: `implementer`
- **Task**: Run the project's formatter. Record files changed.
- **Deliverable**: Format result.

### 2.4 Run security scan
- **Agent**: `implementer`
- **Task**: Run security/vulnerability checks if configured.
- **Deliverable**: Security scan result or confirmation that no scanner is configured.

### 2.5 Run static analysis
- **Agent**: `implementer`
- **Task**: Run static analysis if configured.
- **Deliverable**: Static analysis result or confirmation that no analyzer is configured.

### 2.6 Build
- **Agent**: `implementer`
- **Task**: Build the project to verify compilation.
- **Deliverable**: Build result. Must pass.
- **Gate**: If build fails, enter Phase 3 (Auto-Fix) before proceeding.

### 2.7 Run tests
- **Agent**: `tester`
- **Task**: Run the project's test suite for `$TARGET`.
- **Deliverable**: Test result (pass/fail count). Must pass.
- **Gate**: If tests fail, enter Phase 3 (Auto-Fix) before proceeding.

### Large Project Mode
- **Agent**: `conductor` (you)
- **Task**: If `$TARGET` contains more than 100 source files (detected via `glob`), instruct `implementer` to run verification in batches:
  1. Divide source files into groups of 50 files each.
  2. Run the pipeline on each batch sequentially.
  3. Aggregate results and report any failures with batch context.
- This mode can be disabled by setting `$LARGE_PROJECT_MODE=false`.

## Phase 3 — Auto-Fix Loop

If any step in Phase 2 fails OR if a step reports remaining issues after auto-fix (e.g., linter still reports errors):

### 3.1 Analyze failure
- **Agent**: `implementer`
- **Task**: Read the error output carefully. Identify root cause.
- **Deliverable**: Failure analysis.

### 3.2 Fix issue
- **Agent**: `implementer`
- **Task**: Fix the issue using `edit` or `write`. For issues not resolvable by auto-fix (e.g., Go duplicate imports requiring alias consolidation, naming conflicts, or unused imports with side effects), apply the semantic fix manually. Do not touch unrelated files.
- **Deliverable**: Modified files list.

### 3.3 Re-verify
- **Agent**: `implementer` or `tester` (whichever owns the failed step)
- **Task**: Re-run ONLY the failed step (not the full pipeline).
- **Deliverable**: Step result.
- **Gate**: If the same step fails 3 times, stop the auto-fix loop and report the issue to the user via `question`.

### 3.4 Resume pipeline
- **Agent**: `conductor` (you)
- **Task**: Once the failed step passes, resume the pipeline from the next step. Repeat Phase 3 for any new failures.

## Phase 4 — Report

### 4.1 Produce summary
- **Agent**: `conductor` (you)
- **Task**: Output a brief summary only after ALL steps pass:

```
✓ generate — passed
✓ lint — passed (N issues auto-fixed)
✓ format — passed
✓ security scan — passed
✓ static analysis — passed
✓ build — passed
✓ test — passed (M tests, 0 failures)
```

For large project mode, include batch statistics:

```
✓ batch 1/N — passed (X files)
✓ batch 2/N — passed (Y files)
...
✓ all N batches — passed (total M files)
```

## Completion Criteria

Verification is complete ONLY when:
1. Project type is detected (1.1).
2. Build passes (2.6).
3. Tests pass (2.7).
4. The linter reports zero issues after auto-fix and any required manual fixes (2.2, 2.3).
5. A summary report is presented to the user (4.1).