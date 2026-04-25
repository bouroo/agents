---
description: Refactor and optimize code for quality and performance without breaking public API
---

# Refactor & Optimize

Refactor the specified target $ARGUMENTS (or current working directory if not specified) for readability, quality, and performance while preserving the public API contract.

> **Conductor note**: You do NOT execute steps directly. Decompose this command into the subtasks below, delegate each to the correct subagent, and validate every deliverable before proceeding.

## Constraints

- Public API symbols, signatures, and observable behavior must remain unchanged.
- All existing and newly written tests must pass.
- Before/after metrics must be recorded and compared. Any regression blocks completion.

## Phase 1 — Baseline & Safety Net

Delegate the following in parallel where possible:

### 1.1 Discover public API surface
- **Agent**: `explorer`
- **Scope**: Target module(s) identified by $ARGUMENTS
- **Task**: Identify every public symbol (functions, types, methods, constants) and locate call sites across the project.
- **Deliverable**: List of public symbols and files that reference them.

### 1.2 Run existing tests and record baseline
- **Agent**: `tester`
- **Task**: Run the project's test suite for the target code. Record the exact command used and the result (pass/fail count).
- **Deliverable**: Test command, baseline result, and any failing tests noted.

### 1.3 Add missing tests (MANDATORY if absent)
- **Agent**: `tester`
- **Task**: If no tests cover the target code, write tests that verify current behavior before any refactoring begins. Follow existing project test patterns.
- **Deliverable**: New test file paths and confirmation that they pass.
- **Gate**: Do NOT proceed to Phase 2 until tests exist and are green.

### 1.4 Add missing benchmarks (MANDATORY if absent)
- **Agent**: `tester`
- **Task**: If no performance benchmarks exist for the target code, write benchmarks covering the hot paths. Use the project's benchmark conventions.
- **Deliverable**: New benchmark file paths and confirmation that they execute successfully.
- **Gate**: Do NOT proceed to Phase 2 until benchmarks exist and run.

### 1.5 Record baseline metrics
- **Agent**: `tester` (or `implementer` if tester lacks shell access for profiling tools)
- **Task**: Capture baseline metrics before refactoring:
  - Performance: throughput, latency, memory usage (from benchmarks).
  - Complexity: approximate cyclomatic complexity or line count of changed routines.
  - Memory: allocations per operation (if benchmark reports them).
- **Deliverable**: Baseline metrics table.

## Phase 2 — Apply Refactoring

### 2.1 Refactor target code
- **Agent**: `implementer`
- **Scope**: Files identified in Phase 1.1
- **Task**: Apply refactoring principles:
  - **Naming & Readability**: Follow project conventions; short names for narrow scope, descriptive for broad; acronyms uniform case; no type encoding; no shadowing.
  - **Structure**: Minimal visibility; extract helpers; valid initial state in constructors; named constants over magic values.
  - **Error Handling**: Propagate all errors; wrap with context; define sentinel errors for matching.
  - **State & Concurrency**: No mutable global state; explicit dependencies; structured concurrency; immutable sharing.
  - **Performance**: Preallocate collections; pool high-churn objects; minimize padding; zero-copy where possible; stack-friendly local values; buffered I/O; batch operations; worker pools; atomics for simple shared state; lazy init; propagate cancellation.
- **Constraints**:
  - Do NOT change public API signatures or behavior.
  - Do NOT make changes for the sake of change — only improve readability, quality, or performance.
- **Deliverable**: Modified files with summary of changes.

## Phase 3 — Validate & Compare

Delegate the following in parallel where possible:

### 3.1 Re-run tests
- **Agent**: `tester`
- **Task**: Re-run the same test command from Phase 1.2, including any new tests.
- **Deliverable**: Test results. Must be green.
- **Gate**: If tests fail, return to `implementer` to fix. Do NOT proceed until green.

### 3.2 Re-run benchmarks
- **Agent**: `tester`
- **Task**: Re-run the same benchmarks from Phase 1.4 under identical conditions.
- **Deliverable**: Benchmark results.

### 3.3 Run lint / type check
- **Agent**: `implementer` or `tester`
- **Task**: Run the project's lint and type-check commands.
- **Deliverable**: Lint/type-check output. Must have no new errors.

### 3.4 Verify public API unchanged
- **Agent**: `reviewer` or `explorer`
- **Task**: Confirm no public symbols were removed or had signatures changed. Use `grep` or static analysis to verify call sites still resolve.
- **Deliverable**: Confirmation or list of detected API changes.

### 3.5 Compare before & after (MANDATORY)
- **Agent**: `conductor` (you)
- **Task**: Compare the baseline metrics from Phase 1.5 against Phase 3.2 results. Produce a table:
  | Metric | Before | After | Delta | Status |
  |---|---|---|---|---|
- **Gate**: Result must be strictly better or neutral on every metric. If any metric worsened beyond noise threshold, reject the refactor and return to `implementer` with the comparison table. Iterate until all metrics are green or neutral.

## Completion Criteria

Refactor is complete ONLY when:
1. Public API is unchanged (3.4).
2. All tests pass (3.1).
3. Lint / type check is clean (3.3).
4. Before/after comparison shows no regressions (3.5).
5. A comparison table is presented to the user.