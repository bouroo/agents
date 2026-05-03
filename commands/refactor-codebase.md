---
description: Refactor and optimize code — measure, analyze, refactor, verify, sync
---

You are performing a structured refactoring and optimization pass on the specified code.

## Steps

1. **Identify target**: Determine the specific file, module, or area to refactor from the user's request.
2. **Measure baseline**: Run existing tests to confirm green. Note any performance benchmarks if relevant.
3. **Analyze issues**: Read the target code and identify:
   - Code smells (long functions, duplicated logic, unclear names)
   - Performance issues (unnecessary allocations, missing pre-allocation, unbuffered I/O)
   - Structural issues (tight coupling, missing abstractions, wrong responsibilities)
4. **Plan refactoring**: List the specific changes in order. Each change should be small and preserve behavior.
5. **Refactor incrementally**: Apply one change at a time. Run tests after each.
6. **Verify**: Run full test suite. Run lint and typecheck. Confirm no regressions.
7. **Sync**: If specs or structured prompts exist, sync refactored code back to them.

## Rules

- Refactoring does NOT change observable behavior. If behavior changes, that's a fix, not a refactor.
- One change at a time. Test after each.
- If tests fail after a refactor step, revert and try a different approach.
- Extract functions with informative names. Don't just move code around.
- Remove dead code. Don't comment it out.
- Profile before optimizing performance. Measure before and after.

## When to Stop

- All identified issues addressed
- Tests green
- Lint and typecheck pass
- No further improvements without changing behavior
