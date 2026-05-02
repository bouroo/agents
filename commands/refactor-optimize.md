---
description: Refactor and optimize code — measure, refactor, optimize, sync
---

Refactor and optimize the specified code.

$ARGUMENTS

## Workflow

1. **Measure** — Run benchmarks or identify performance characteristics of the current code
2. **Analyze** — Identify specific bottlenecks, code smells, unnessesary allocations, or structural issues
3. **Plan** — Describe the refactoring or optimization approach before making changes
4. **Refactor** — Make small, incremental changes. Verify each step
5. **Verify** — Re-run benchmarks/tests after each change to confirm improvement without regressions
6. **Sync** — Update spec/plan to reflect structural changes (Code → Spec sync)

## Rules

- One change at a time. Verify before proceeding.
- Never change observable behavior during refactoring — only structure.
- If a refactoring requires behavior change, treat it as a logic correction (fix spec first).
- Always run tests before and after each change.
- If no tests or benchmarks exist, write them first.
- Never break existing public APIs.
- Summary of changes and verification results should be included in the report.