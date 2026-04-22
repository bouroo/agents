---
description: Detect project type, run verification pipeline with auto-fix
---

# Verify Project

Run the full verification pipeline for `$ARGUMENTS` (or current working directory if not specified). Detect the project type automatically and execute the appropriate toolchain. Fix any issues found and re-verify until clean or the issue requires human input.

## Steps

### 1. Detect Project Type

Scan the project root for build manifests, lock files, and configuration files to determine the project type and build system.

If no recognized manifest is found, ask the user via `question` to specify the project type or provide guidance.

### 2. Determine Verification Commands

Look for configuration files that indicate the project's toolchain (linters, formatters, test runners, security scanners).

Read the project's build manifest to determine the standard verification commands:

1. Look for scripts defined in the manifest that invoke verification tools.
2. Identify the build system and its standard verification targets.

### 3. Run Verification Pipeline

Execute the verification pipeline using `execute`. Set `$TARGET` to `$ARGUMENTS` if provided, otherwise `.` (current working directory).

Run steps in this order:
1. **Generate** — Run code generation if configured (protobuf generation, OpenAPI generation, etc.)
2. **Lint/Fix** — Run the project's linter with auto-fix
3. **Format** — Run the project's formatter
4. **Security Scan** — Run security/vulnerability checks if configured
5. **Static Analysis** — Run static analysis if configured
6. **Build** — Build the project to verify compilation
7. **Test** — Run the project's test suite

Run the standard verification commands appropriate for the detected build system: code generation, linting with auto-fix, formatting, security scanning, static analysis, building, and testing. Use commands defined in the project's build configuration or standard for the detected ecosystem.

For each step:
- Check if the required tool is installed before running
- If the tool is not found, report the missing tool and ask the user whether to skip or install
- If a step fails, proceed to the auto-fix loop

### 4. Large Project Mode

If `$TARGET` contains more than 100 source files (detected via `glob`), run verification in batches to avoid timeouts and resource exhaustion:

1. Divide source files into groups of 50 files each.
2. Run the pipeline on each batch sequentially.
3. Aggregate results and report any failures with batch context.

This mode can be disabled by setting `$LARGE_PROJECT_MODE=false`.

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
