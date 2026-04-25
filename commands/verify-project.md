---
description: Detect project type, run verification pipeline with auto-fix
---

# Verify Project

Run the full verification pipeline for $ARGUMENTS (or current working directory if not specified). Detect the project type automatically and execute the appropriate toolchain. Fix any issues found and re-verify until clean or the issue requires human input.

> **Conductor note**: You do NOT execute steps directly. Decompose this command into the subtasks below, delegate each to the correct subagent, and validate every deliverable before proceeding.

> **CRITICAL**: This command requires manual file editing for issues that auto-fixers cannot resolve (e.g., duplicate imports). You MUST use `edit` or `write` tools to fix these issues. Auto-fix flags alone are NOT sufficient.

## Constraints

- Every step in the pipeline must be attempted. Do not skip steps because earlier ones failed.
- Auto-fix is mandatory for fixable issues. Only escalate to the user after 3 failed fix attempts on the same issue.
- The pipeline is complete only when build and test steps pass.

## Phase 1 — Discovery

### 1.1 Detect project type and toolchain
- **Agent**: `explorer`
- **Task**: Scan the project root for build manifests, lock files, and configuration files to determine project type, build system, and available verification tools.
- **Deliverable**: Project type, build system, and list of detected verification tools/commands.
- **Gate**: If no recognized manifest is found, ask the user via `question` for the project type before proceeding.

### 1.2 Determine verification commands
- **Agent**: `implementer`
- **Task**: Read the build manifest and config files. Identify the standard commands for: generate, lint (with auto-fix), format, security scan, static analysis, build, test.
- **Deliverable**: Exact command list for each verification step.
- **Note**: Also check for project-specific verification scripts such as pre-commit hooks, Makefile targets, CI scripts, or local verification scripts. If such scripts exist, record them as they may run multiple tools in sequence.

## Phase 2 — Verification Pipeline

Set `$TARGET` to $ARGUMENTS if provided, otherwise `.` (current working directory).

### 2.1 Run generate
- **Agent**: `implementer`
- **Task**: Run code generation if configured (e.g., protobuf, OpenAPI, schema generation).
- **Deliverable**: Generate output or confirmation that no generation is needed.

### 2.2 Run lint with auto-fix
- **Agent**: `implementer`
- **Task**:
  1. Identify ALL configured lint tools for the project.
  2. **MANDATORY**: Run EACH lint tool individually BEFORE running any project verification script.
  3. For each tool: run with auto-fix (if supported), then run in check mode to verify zero issues.
  4. If ANY individual lint tool reports issues, treat this as a failure and enter Phase 3.
  5. Only after ALL individual lint tools report zero issues, run the project's full verification script if one exists.
  6. If the script fails, parse the output, enter Phase 3, fix the issue, re-run the failed individual tool, then re-run the script.
- **Deliverable**: Lint result from ALL configured tools. EACH must report zero issues before proceeding.
- **Common tool families**: compiler linters, style checkers, type checkers, security scanners. Run these if no configured tools are detected.
- **Note**: Some issues (e.g., duplicate imports) require manual code edits. No auto-fix tool handles these.

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

If any step in Phase 2 fails OR if a step reports remaining issues after auto-fix:

### 3.1 Analyze failure
- **Agent**: `implementer`
- **Task**: Read the error output carefully. Identify root cause. Determine:
  1. Which specific tool failed
  2. The exact error message and file location
  3. Whether the error is auto-fixable or requires manual intervention
- **Deliverable**: Failure analysis with specific tool name and root cause.

### 3.2 Fix issue
- **Agent**: `implementer`
- **Task**: Fix the issue using `edit` or `write`. For issues not resolvable by auto-fix, apply the semantic fix manually. Do not touch unrelated files.
- **Reminder**: You are in the Auto-Fix Loop because a lint tool reported issues. You MUST fix the underlying code and re-run the specific failing tool. Do NOT skip re-running the tool.
- **Manual fix for duplicate imports**:
  1. Read the file reported in the lint error.
  2. Find the import block. Look for the same package path imported multiple times with different aliases.
  3. Choose ONE alias to keep (prefer the most descriptive one).
  4. Delete ALL other lines importing the same package.
  5. Search the entire file for usages of the deleted aliases and replace each with the kept alias.
  6. Save the file and run formatter.
  7. Re-scan for more duplicate imports in the same file.
  8. Repeat for every set of duplicates.
  9. Re-run the failing tool to verify all errors are gone.
- **Deliverable**: Modified files list.

### 3.3 Re-verify
- **Agent**: `implementer` or `tester` (whichever owns the failed step)
- **Task**: Re-run the failed verification. For lint fixes:
  - First re-run the specific failing tool to verify zero issues.
  - Then re-run ALL other configured lint tools to ensure no regressions.
  - Finally, if the project has a verification script, re-run the full script.
  ALL must pass before proceeding.
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

(End of file - total 175 lines)