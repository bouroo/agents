---
description: Refactor and optimize code — test, measure, analyze, refactor, verify, sync
---

# Structured Refactoring & Optimization

**Target**: $ARGUMENTS

**Context**: !`git diff --stat HEAD 2>/dev/null || echo "No git repo or clean working tree"`

## Workflow

### 1. Lock Tests First
- Run existing tests — must be green.
- Write integration tests covering observable behavior for any untested paths.
- Add benchmarks for hot paths. Capture baseline numbers.

### 2. Measure Before Optimizing
- Run allocation profiler / escape analysis on hot paths.
- Run benchmarks: capture memory allocations/op and latency baselines.
- Identify concrete opportunities (preallocation, pooling, cache locality, buffered I/O, worker pools).

### 3. Analyze Maintainability
- **Readability**: mixed abstractions, duplicated logic, unclear names, magic values.
- **Structure**: tight coupling, env-dependent code outside entry point, mutable global state.
- **Error handling**: ignored errors, string comparisons on errors, missing wrapping.

### 4. Plan Changes
- List specific, small, behavior-preserving changes with clear before/after.
- Priority: performance > structure > readability > error handling.

### 5. Refactor Incrementally
- One change at a time. Run tests after each. Revert on failure.

### 6. Verify
- Run full test suite, lint, typecheck.
- Re-run benchmarks. Compare against baseline.

### 7. Summarize

| Change | Lines | Tests | Benchmark (before → after) |
|--------|-------|-------|----------------------------|
| ... | ... | ... | ... |

### 8. Sync
- Update specs/prompts to reflect refactored code if they exist.

## Invariants
- No tests = no refactor. No benchmarks = no perf optimization.
- Observable behavior must not change.
- Extract with informative names. Remove dead code — don't comment it out.
- Performance claims require numbers.
- Never break public API.
- Use named constants over magic values.
- Wrap errors with context; define named sentinel errors.