---
name: test-first
description: Test-First Development (TDD) methodology — write tests before implementation, follow Red-Green-Refactor cycle. Use when writing tests, implementing features, fixing bugs, or when the user mentions TDD, test-driven development, or testing strategy.
---

# Test-First Development

## Red-Green-Refactor Cycle

1. **Red** — Write a failing test that defines the desired behavior
2. **Green** — Write the minimal implementation to make the test pass
3. **Refactor** — Clean up while keeping all tests green
4. **Repeat** for the next behavior

## Rules (Non-Negotiable)

- No implementation code before tests are written and validated as failing
- Tests define behavior; implementation fulfills it
- Every new function/module starts with its test file

## Test Priority Order

Write tests in this order, from outer to inner:

1. **Contract** — Does the public API honor its declared behavior?
2. **Integration** — Do components work together correctly?
3. **End-to-end** — Does the full system produce the expected outcome?
4. **Unit** — Does each isolated function handle its inputs correctly?

## Naming Conventions

- Descriptive sentences, not `testFunction1` — e.g., `TestParseReturnsErrorOnMalformedInput`
- One assertion concept per test
- Name by behavior, not implementation

## Coverage

- Target >80% coverage for business logic
- Test error paths, not just happy paths
- Edge cases: empty inputs, boundary values, nil/null checks
- Use table-driven tests for multiple input/output scenarios:
  - Name each case with a descriptive `name` or `desc` field
  - Include expected error cases alongside success cases
  - Keep each row focused on one behavioral variation

## Test Quality

- Provide clear, actionable diagnostics on failure (include input, expected, actual)
- Avoid change-detector tests that break when implementation details shift
- Prefer real implementations over mocks when practical — test state, not interactions
- Keep tests independent — no ordering dependencies between test cases
- Use test helpers for setup/teardown, but keep the assertion visible in the test body

## What NOT to Test

- Framework or library behavior (trust the dependency)
- Private implementation details likely to change during refactoring
- Exact error message text — match on error type/kind or sentinel values instead

## Workflow Checklist

- [ ] Write failing test for the next behavior
- [ ] Confirm test fails for the right reason
- [ ] Write minimal implementation to pass
- [ ] Confirm test passes
- [ ] Refactor implementation and tests
- [ ] Run full suite — all green
- [ ] Repeat
