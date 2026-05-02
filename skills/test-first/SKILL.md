---
name: test-first
description: Test-Driven Development workflow — write tests before implementation, Red-Green-Refactor cycle, test naming as sentences, integration-first testing.
---

# Test-First Development

## Core Principle

No implementation code before tests. Tests define behavior, get approved, confirm they fail (Red), then implementation makes them pass (Green).

## Red-Green-Refactor

1. **Red** — Write a failing test defining desired behavior
2. **Green** — Write minimal code to make it pass
3. **Refactor** — Clean up while keeping tests green
4. **Repeat** — Next behavior

## Test Naming

Names should be sentences describing expected behavior:
- `testCalculateBill_withOverage_chargesModelSpecificRate`
- `testValidateInput_missingModelId_returns400`

Reader understands what's tested without reading the body.

## What to Test

- **Happy path**: Normal flow
- **Edge cases**: Boundaries, empty inputs, maximum sizes
- **Error paths**: Invalid inputs, missing fields, unauthorized
- **Integration points**: Contracts between modules and services

## Test Priority

1. Contract tests — module boundaries and API contracts
2. Integration tests — components working together
3. Unit tests — individual functions and methods
4. End-to-end tests — complete user workflows

## Integration-First

- Prefer real databases over mocks
- Use actual service instances over stubs
- Contract tests mandatory before implementation
- Only mock external systems you don't control

## Anti-patterns

- Tests after implementation (loses design benefit)
- Testing implementation details instead of behavior
- Over-mocking making tests fragile
- Skipping tests "for now"
