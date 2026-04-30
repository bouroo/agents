---
description: Refactor and optimize code for quality and performance without breaking public API
---

# Refactor & Optimize

Refactor the specified target `$ARGUMENTS` (or current working directory if not specified) for readability, quality, and performance while preserving the public API contract.

> **Conductor note**: You do NOT execute steps directly. Decompose this command into the subtasks below, delegate each to the correct subagent, and validate every deliverable before proceeding.

## Constraints

- Public API symbols, signatures, and observable behavior must remain unchanged.
- All existing and newly written tests must pass.
- Before/after metrics must be recorded and compared. Any regression blocks completion.

## Phase 1 — Baseline & Safety Net

Delegate the following in parallel where possible:

### 1.1 Discover public API surface
- **Delegate to**: exploration-capable subagent
- **Scope**: Target module(s) identified by `$ARGUMENTS`
- **Task**: Identify every public symbol (functions, types, methods, constants) and locate call sites across the project.
- **Deliverable**: List of public symbols and files that reference them.

### 1.2 Run existing tests and record baseline
- **Delegate to**: testing-capable subagent
- **Task**: Run the project's test suite for the target code. Record the exact command used and the result (pass/fail count).
- **Deliverable**: Test command, baseline result, and any failing tests noted.

### 1.3 Add missing tests (MANDATORY if absent)
- **Delegate to**: testing-capable subagent
- **Task**: If no tests cover the target code, write tests that verify current behavior before any refactoring begins. Follow existing project test patterns.
- **Deliverable**: New test file paths and confirmation that they pass.
- **Gate**: Do NOT proceed to Phase 2 until tests exist and are green.

### 1.4 Add missing benchmarks (MANDATORY if absent)
- **Delegate to**: testing-capable subagent
- **Task**: If no performance benchmarks exist for the target code, write benchmarks covering the hot paths. Use the project's benchmark conventions.
- **Deliverable**: New benchmark file paths and confirmation that they execute successfully.
- **Gate**: Do NOT proceed to Phase 2 until benchmarks exist and run.

### 1.5 Record baseline metrics
- **Delegate to**: testing or implementation subagent (prefer testing if available)
- **Task**: Capture baseline metrics before refactoring:
  - Performance: throughput, latency, memory usage (from benchmarks).
  - Complexity: approximate cyclomatic complexity or line count of changed routines.
  - Memory: allocations per operation (if benchmark reports them).
- **Deliverable**: Baseline metrics table.

## Phase 2 — Apply Refactoring

### 2.1 Refactor target code
- **Delegate to**: implementation-capable subagent
- **Scope**: Files identified in Phase 1.1
- **Task**: Apply refactoring principles:
  - **Naming & Readability**: Follow project conventions; short names for narrow scope, descriptive for broad; acronyms uniform case; no type encoding; no shadowing.
  - **Structure**: Minimal visibility; extract helpers; valid initial state in constructors; named constants over magic values.
  - **Error Handling**: Propagate all errors; wrap with context; define sentinel errors for matching.
  - **State & Concurrency**: No mutable global state; explicit dependencies; structured concurrency; immutable sharing.
  - **Performance**: Preallocate collections when size is known; pool high-churn objects; batch I/O; minimize copies; lazy-init expensive resources; use efficient data structures.
  - **Spec-Code Sync**: For refactoring changes, update code first then sync the spec. If the refactoring reveals a design improvement, update the plan/spec file to reflect it.
- **Constraints**:
  - Do NOT change public API signatures or behavior.
  - Do NOT make changes for the sake of change — only improve readability, quality, or performance.
- **Deliverable**: Modified files with summary of changes.

## Phase 2.5 — Sync Specifications

### 2.5.1 Sync refactored structure back to spec
- **Delegate to**: implementation-capable subagent
- **Scope**: Plan files or specification documents in `plans/` or `spdd/` directories
- **Task**: For each refactored module, update the corresponding spec to reflect:
  - Renamed or restructured types and functions
  - Changed internal dependencies or collaborations
  - New constants or extracted helpers
- **Deliverable**: Updated spec files matching the refactored code.
- **Constraint**: Only update specs for changes that do NOT alter observable behavior. If behavior changed, that's a logic correction — go back to Phase 2.

## Phase 3 — Validate & Compare

Delegate the following in parallel where possible:

### 3.1 Re-run tests
- **Delegate to**: testing-capable subagent
- **Task**: Re-run the same test command from Phase 1.2, including any new tests.
- **Deliverable**: Test results. Must be green.
- **Gate**: If tests fail, return to the implementation subagent to fix. Do NOT proceed until green.

### 3.2 Re-run benchmarks
- **Delegate to**: testing-capable subagent
- **Task**: Re-run the same benchmarks from Phase 1.4 under identical conditions.
- **Deliverable**: Benchmark results.

### 3.3 Run lint / type check
- **Delegate to**: implementation or testing subagent
- **Task**: Run the project's lint and type-check commands.
- **Deliverable**: Lint/type-check output. Must have no new errors.

### 3.4 Verify public API unchanged
- **Delegate to**: review or exploration subagent
- **Task**: Confirm no public symbols were removed or had signatures changed. Use content search or static analysis to verify call sites still resolve.
- **Deliverable**: Confirmation or list of detected API changes.

### 3.5 Compare before & after (MANDATORY)
- **Owner**: conductor (you)
- **Task**: Compare the baseline metrics from Phase 1.5 against Phase 3.2 results. Produce a table:
  | Metric | Before | After | Delta | Status |
  |---|---|---|---|---|
- **Gate**: Result must be strictly better or neutral on every metric. If any metric worsened beyond noise threshold, reject the refactor and return to the implementation subagent with the comparison table. Iterate until all metrics are green or neutral.

## Completion Criteria

Refactor is complete ONLY when:
1. Public API is unchanged (3.4).
2. All tests pass (3.1).
3. Lint / type check is clean (3.3).
4. Before/after comparison shows no regressions (3.5).
5. Spec files are synchronized with refactored code (Phase 2.5).
6. A comparison table is presented to the user.

(End of file - total 87 lines)