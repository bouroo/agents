---
description: Refactor and optimize code — test, measure, analyze, refactor, verify, sync
---

You are performing a structured refactoring and optimization pass on the specified code.

## Steps

1. **Identify target**: Determine the file, module, or area from the user's request. If `$ARGUMENTS` is empty, use the current working directory.

2. **Lock tests first**:
   - Run existing tests — must be green. If none exist, write integration tests covering observable behavior.
   - Add tests for any untested path the refactoring will touch.
   - **Write benchmarks** for hot paths (loop bodies, allocation-heavy functions, serialization, I/O). Capture baseline measurements. Benchmarks are mandatory, not optional.
   - Record test count, pass/fail, and benchmark numbers as the regression guard.

3. **Profile and measure performance** (do this BEFORE readability analysis):
   - Run the language's escape analysis or allocation profiler to identify heap allocations in hot paths.
   - Run benchmarks capturing memory allocations per operation and latency baselines.
   - Use a CPU and memory profiler (pprof, perf, VTune, etc.) to find hot spots.
   - Identify concrete perf opportunities:
     - Collection/map pre-allocation where size is known or estimable
     - StringBuilder or equivalent instead of string concatenation / formatting in hot paths
     - Object pools for frequently allocated short-lived objects
     - Struct/record field reordering for cache locality (group by size: pointers, then 8-byte, 4-byte, 1-byte)
     - Reducing interface/dynamic dispatch or boxing in hot paths
     - Buffer reuse across function calls instead of per-call allocation
     - Batched I/O instead of per-element reads/writes
     - Removing unnecessary deferred cleanup in hot loops (defer/try-with-resources has overhead per call)
     - Replacing reflection/dynamic dispatch with concrete types or code generation
     - Inlining small functions called in tight loops (check compiler decisions)

4. **Analyze maintainability issues**:
   - **Readability**: Long mixed-abstraction functions, duplicated logic, unclear names, magic values, missing docs on exported symbols
   - **Structure**: Tight coupling, env-dependent code outside entry point, mutable global state, unstructured concurrency
   - **Error handling**: Ignored errors, string comparisons on errors, missing error wrapping, missing context in error chains

5. **Plan changes**: List specific changes in order. Each must be small, preserve behavior, and have clear before/after. Prioritize: performance > structure > readability > error handling. Performance changes must include expected alloc/latency improvement.

6. **Refactor incrementally**: Apply one change at a time. Run tests after each. If tests fail, revert immediately.

7. **Verify**: Run full test suite, lint, typecheck, and benchmarks. Compare benchmark results against baseline — there must be measurable improvement in allocs or latency. If no performance change was possible, explain why in the summary.

8. **Summarize**:

   ```
   ## Refactoring Summary

   **Target**: <file or module path>

   | # | Change | Category | Before | After |
   |---|--------|----------|--------|-------|
   | 1 | <description> | performance/readability/structure/errors | <what existed> | <what replaced it> |

   **Test results**: <count> tests, all green
   **Benchmark delta**: <e.g., -12% allocs, -8% latency>
   **Allocation changes**: <e.g., "XYZ argument moved to stack, eliminated 2 heap allocs"> or "none possible"
   **API changes**: None / <list any flagged changes>
   ```

9. **Sync**: If specs or structured prompts exist, sync refactored code back to them.

## Rules

- Refactoring does NOT change observable behavior. Behavior changes = fix, not refactor.
- **No tests = no refactor.** No benchmarks = no perf optimization.
- One change at a time. Test after each. Fail → revert.
- Extract functions with informative names. Don't just move code.
- Remove dead code. Don't comment it out.
- **Performance changes must be measured.** Never claim improvement without benchmark numbers. If benchmarks show regression, revert.
- Do NOT break the public API. All exported symbols, types, function signatures must remain backward-compatible. Flag any required API change for confirmation.
- Keep concurrency confined to creation scope. Use structured patterns (wait groups, cancellation tokens, scoped tasks).
- Decouple from environment. Only entry point reads env vars, CLI args, file paths.
- Use always-valid values. Named constants over magic values.
- Wrap errors with context. Define named sentinel errors users can match against. Never compare error strings.

## When to Stop

- All identified issues addressed
- Tests green
- Lint and typecheck pass
- Benchmarks show improvement or improvement is provably impossible (documented why)
- Improvement summary produced