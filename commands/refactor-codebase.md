---
description: Refactor and optimize code — test, measure, analyze, refactor, verify, sync
---

You are performing a structured refactoring and optimization pass on the specified code.

## Steps

1. **Identify target**: Determine the specific file, module, or area to refactor from the user's request if `$ARGUMENTS` is not set or is empty use current working directory.

2. **Lock tests first**: Before touching any code, ensure a safety net exists:
   - Run existing tests — they must be green. If no tests exist, write integration tests covering the target's observable behavior first.
   - Identify untested code paths. Add tests for any path the refactoring will touch.
   - If optimizing performance, write benchmarks that exercise the hot path. Capture a baseline measurement.
   - Record the test count, pass/fail status, and benchmark numbers. This is your regression guard.

3. **Analyze issues**: Read the target code and flag problems in these categories:

   **Readability**
   - Long functions that mix high-level intent with low-level paperwork
   - Duplicated logic or unclear names that break glanceability
   - Missing or misleading documentation on exported symbols
   - Magic values instead of named constants

   **Structure**
   - Tight coupling, missing abstractions, or wrong responsibility boundaries
   - Environment-dependent code (env vars, CLI args, file paths) outside the entry point
   - Mutable global state; implicit shared objects that invite data races
   - Concurrency that escapes its creation scope or lacks structured termination

   **Performance**
   - Unnecessary allocations — missing pre-allocation on slices/maps, hidden interface boxing
   - Unbuffered or unbatched I/O where buffering/batching would help
   - Objects churned on the heap that could be reused (pooling) or kept on the stack
   - Values escaping to the heap that could stay on the stack — use escape analysis (e.g., `go build -gcflags="-m"`) to find them
   - Missing field-order optimization for struct layout / cache locality

   **Error handling**
   - Ignored errors (`_`), string comparison on errors, or missing context in error chains
   - Flattened errors instead of wrapped ones — sentinel errors should be matchable
   - Missing graceful degradation — crashes where retry or fallback is appropriate

4. **Plan refactoring**: List specific changes in order. Each change must be small, preserve behavior, and have a clear before/after description.

5. **Refactor incrementally**: Apply one change at a time. Run tests after each change. If tests fail, revert immediately and try a different approach.

6. **Verify**: Run full test suite, lint, and typecheck. If benchmarks exist, run them and compare against baseline. Confirm no regressions.

7. **Summarize improvements**: Produce a concise report of what changed and why:

   ```
   ## Refactoring Summary

   **Target**: <file or module path>

   | # | Change | Category | Before | After |
   |---|--------|----------|--------|-------|
   | 1 | <description> | readability/structure/performance/errors | <what existed> | <what replaced it> |

   **Test results**: <count> tests, all green
   **Benchmark delta**: <e.g., -12% allocs, -8% latency, or "N/A">
   **API changes**: None / <list any flagged changes>
   ```

8. **Sync**: If specs or structured prompts exist, sync refactored code back to them.

## Rules

- Refactoring does NOT change observable behavior. If behavior changes, that's a fix, not a refactor.
- **No tests = no refactor.** If the target lacks tests, write them first. Tests are the regression safety net.
- One change at a time. Test after each. If tests fail, revert and try a different approach.
- Extract functions with informative names (`createRequest`, `parseResponse`). Don't just move code around.
- Remove dead code. Don't comment it out.
- Profile before optimizing performance. Measure before and after. Optimise for clarity first, speed second.
- Do NOT break the public API. All exported symbols, types, function signatures, and protocol contracts must remain backward-compatible. If a refactoring requires an API change, flag it explicitly and get confirmation first.
- Keep concurrency confined to its creation scope. Use structured patterns (waitgroups, errgroups, cancellable contexts). Ensure all spawned tasks terminate before the enclosing function exits.
- Decouple from environment. Only the entry point should read env vars, CLI args, or file paths. Keep configuration injectable.
- Use always-valid values. Design types so invalid states are unrepresentable. Prefer named constants over magic values.
- Wrap errors with context (`%w` / equivalent), don't flatten. Define named sentinel errors users can match against. Never compare error strings.

## When to Stop

- All identified issues addressed
- Tests green
- Lint and typecheck pass
- No regressions in benchmarks
- Improvement summary produced
- No further improvements without changing behavior
