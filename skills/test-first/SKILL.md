---
name: test-first
description: Test-Driven Development workflow — write tests before implementation, Red-Green-Refactor cycle, test naming as sentences, integration-first testing.
---

# Test-First Development

## Core Principle

No implementation code before tests. Tests define behavior, get approved, confirm they fail (Red phase), then implementation makes them pass (Green phase).

## Red-Green-Refactor Cycle

1. **Red**: Write a failing test that defines the desired behavior
2. **Green**: Write the minimal code to make the test pass
3. **Refactor**: Clean up while keeping tests green
4. **Repeat**: Move to the next behavior

## Test Naming

Test names should be sentences describing the expected behavior:

- `testCalculateBill_withOverage_chargesModelSpecificRate`
- `testValidateInput_missingModelId_returns400`
- `testAuthenticate_expiredToken_throwsUnauthorized`

A reader should understand what's tested without reading the test body.

## What to Test

- **Happy path**: The normal flow that works
- **Edge cases**: Boundary values, empty inputs, maximum sizes
- **Error paths**: Invalid inputs, missing fields, unauthorized access
- **Integration points**: Contracts between modules and services

## Test Priority

1. **Contract tests** — Verify module boundaries and API contracts
2. **Integration tests** — Verify components work together correctly
3. **Unit tests** — Verify individual functions and methods
4. **End-to-end tests** — Verify complete user workflows

## Integration-First Testing

- Prefer real databases over mocks
- Use actual service instances over stubs
- Contract tests are mandatory before implementation
- Only mock external systems you don't control

## Test Organization

- Place tests alongside the code they test (language convention)
- Group related tests in describe/context blocks
- Use test fixtures and factories for test data
- Keep tests independent — no ordering dependencies

## Anti-patterns

- Writing tests after implementation (loses the design benefit)
- Testing implementation details instead of behavior
- Over-mocking to the point tests are fragile
- Skipping tests "for now" (they never come back)
- Tests that depend on execution order
- Ignoring failing tests instead of fixing them
