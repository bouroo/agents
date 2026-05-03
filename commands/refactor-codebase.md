---
description: Refactor and optimize code — test, measure, analyze, refactor, verify, sync
subtask: true
---

You are performing a structured refactoring and optimization pass on the specified code.

## Target

$ARGUMENTS

## Context

Working tree status:
!`git diff --stat HEAD 2>/dev/null || echo "No git repo or clean working tree"`

## Steps

1. **Identify target**: Determine the file, module, or area from the user's request above. If no target is specified, use the current working directory.

2. **Lock tests first**:
   - Run existing tests — must be green. If none exist, write integration tests covering observable behavior.
   - Add tests for any untested path the refactoring will touch.
   - **Write benchmarks** for hot paths (loop bodies, allocation-heavy functions, serialization, I/O). Capture baseline measurements.
   - Record test count, pass/fail, and benchmark numbers as the regression guard.

3. **Profile and measure performance** (do this BEFORE readability analysis):
   - Run the language's escape analysis or allocation profiler to identify heap allocations in hot paths.
   - Run benchmarks capturing memory allocations per operation and latency baselines.
   - Identify concrete perf opportunities:
     - Collection/map pre-allocation where size is known or estimable
     - StringBuilder or equivalent instead of string concatenation in hot paths
     - Object pools for frequently allocated short-lived objects
     - Struct/record field reordering for cache locality
     - Reducing interface/dynamic dispatch or boxing in hot paths
     - Buffer reuse across function calls instead of per-call allocation
     - Batched I/O instead of per-element reads/writes
     - Replacing reflection/dynamic dispatch with concrete types or code generation

4. **Analyze maintainability issues**:
   - **Readability**: Long mixed-abstraction functions, duplicated logic, unclear names, magic values
   - **Structure**: Tight coupling, env-dependent code outside entry point, mutable global state
   - **Error handling**: Ignored errors, string comparisons on errors, missing error wrapping

5. **Plan changes**: List specific changes in order. Each must be small, preserve behavior, and have clear before/after. Prioritize: performance > structure > readability > error handling.

6. **Refactor incrementally**: Apply one change at a time. Run tests after each. If tests fail, revert immediately.

7. **Verify**: Run full test suite, lint, typecheck, and benchmarks. Capture benchmark output for comparison. Compare against baseline.

8. **Summarize**:

   ```
   ## Refactoring Summary

   **Target**: <file or module path>

   | # | Change | Category | Before | After |
   |---|--------|----------|--------|-------|
   | 1 | <description> | performance/readability/structure/errors | <what existed> | <what replaced it> |

   **Test results**: <count> tests, all green

   **Benchmark comparison**:
   | Metric | Before | After | Change |
   |--------|--------|-------|--------|
   | ns/op  | <value> | <value> | <±%> |
   | allocs/op | <value> | <value> | <±%> |
   | bytes/op | <value> | <value> | <±%> |
   ```

9. **Sync**: If specs or structured prompts exist, sync refactored code back to them.

## Context Management

- Refactoring generates many tool outputs (profiler runs, benchmarks, test results). Use `/compact` between phases (measure → analyze → refactor) to keep context lean.
- Record benchmark baselines in the refactoring summary — they survive compaction.
- Use file:line references instead of quoting full functions in the change plan.

## Rules

- Refactoring does NOT change observable behavior. Behavior changes = fix, not refactor.
- **No tests = no refactor.** No benchmarks = no perf optimization.
- One change at a time. Test after each. Fail → revert.
- Extract functions with informative names. Don't just move code.
- Remove dead code. Don't comment it out.
- **Performance changes must be measured.** Never claim improvement without benchmark numbers.
- Do NOT break the public API.
- Use always-valid values. Named constants over magic values.
- Wrap errors with context. Define named sentinel errors.
