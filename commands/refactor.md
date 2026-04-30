---
description: Refactor and optimize code for quality and performance without breaking public API
---

# Refactor & Optimize

Refactor target `$ARGUMENTS` (or cwd) for readability, quality, performance while preserving public API.

> **Conductor**: Decompose into subtasks, delegate to subagents, validate every deliverable.

## Constraints
- Public API symbols, signatures, observable behavior unchanged
- All existing + new tests pass
- Before/after metrics recorded; regression blocks completion

## Phase 1 — Baseline & Safety Net

### 1.1 Discover public API surface
- **Delegate to**: discovery agent
- **Task**: Identify public symbols (functions, types, methods, constants). Locate call sites.
- **Deliverable**: List of public symbols + files referencing them.

### 1.2 Run existing tests — record baseline
- **Delegate to**: testing agent
- **Task**: Run test suite for target code. Record command + result.
- **Deliverable**: Test command, baseline result, failing tests noted.

### 1.3 Add missing tests (MANDATORY if absent)
- **Delegate to**: testing agent
- **Task**: Write tests verifying current behavior before refactoring. Follow project patterns.
- **Deliverable**: New test file paths, confirmation passing.
- **Gate**: Do NOT proceed to Phase 2 until tests green.

### 1.4 Add missing benchmarks (MANDATORY if absent)
- **Delegate to**: testing agent
- **Task**: Write benchmarks for hot paths. Use project conventions.
- **Deliverable**: New benchmark paths, confirmation running.
- **Gate**: Do NOT proceed to Phase 2 until benchmarks exist.

### 1.5 Record baseline metrics
- **Delegate to**: testing or implementation agent
- **Task**: Capture metrics:
  - Performance: throughput, latency, memory (from benchmarks)
  - Complexity: cyclomatic complexity, line count
  - Memory: allocations per operation
- **Deliverable**: Baseline metrics table.

## Phase 2 — Apply Refactoring

### 2.1 Refactor target code
- **Delegate to**: implementation agent
- **Scope**: Files from 1.1
- **Principles**:
  - **Naming**: Follow conventions; descriptive for broad scope, short for narrow; no type encoding
  - **Structure**: Minimal visibility; extract helpers; named constants; valid initial state
  - **Error Handling**: Propagate all errors; wrap with context; sentinel errors
  - **State/Concurrency**: No mutable global state; explicit dependencies; structured concurrency; immutable sharing
  - **Performance**: Preallocate collections; pool high-churn objects; batch I/O; minimize copies; lazy-init; efficient data structures; avoid allocations
- **Spec-Code Sync**: For refactoring, update code first then sync spec. If design improvement found, update plan/spec.
- **Constraints**: DO NOT change public API signatures or behavior. No changes for sake of change.
- **Deliverable**: Modified files + summary of changes.

## Phase 2.5 — Sync Specifications

### 2.5.1 Sync refactored structure to spec
- **Delegate to**: implementation agent
- **Scope**: Specs in `plans/` or `spdd/`
- **Task**: Update specs for:
  - Renamed/restructured types and functions
  - Changed internal dependencies
  - New constants or extracted helpers
- **Deliverable**: Updated spec files.
- **Constraint**: Only update for non-behavior changes. Behavior change = logic correction, return to Phase 2.

## Phase 3 — Validate & Compare

### 3.1 Re-run tests
- **Delegate to**: testing agent
- **Task**: Re-run same command from 1.2 + new tests.
- **Deliverable**: Test results (must be green).
- **Gate**: If fail, return to implementation agent. Do NOT proceed until green.

### 3.2 Re-run benchmarks
- **Delegate to**: testing agent
- **Task**: Re-run same benchmarks from 1.4.
- **Deliverable**: Benchmark results.

### 3.3 Run lint / type check
- **Delegate to**: implementation or testing agent
- **Task**: Run lint + type-check commands.
- **Deliverable**: Output must have no new errors.

### 3.4 Verify public API unchanged
- **Delegate to**: review or discovery agent
- **Task**: Confirm no public symbols removed or signature changed. Verify call sites resolve.
- **Deliverable**: Confirmation or list of API changes.

### 3.5 Compare before & after (MANDATORY)
- **Owner**: conductor
- **Task**: Compare 1.5 vs 3.2 metrics:

| Metric | Before | After | Delta | Status |
|--------|--------|-------|-------|--------|
| | | | | |

- **Gate**: All metrics must be better or neutral. Reject if any regress beyond noise threshold.

## Completion Criteria

1. Public API unchanged (3.4)
2. All tests pass (3.1)
3. Lint/type check clean (3.3)
4. Before/after comparison shows no regressions (3.5)
5. Spec files synchronized (Phase 2.5)
6. Comparison table presented to user