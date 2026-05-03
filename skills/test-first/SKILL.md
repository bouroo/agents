---
name: test-first
description: Test-Driven Development workflow — write tests before implementation, Red-Green-Refactor cycle, test naming as sentences, integration-first testing.
version: 1.0.0
triggers:
  - TDD workflow
  - test writing
  - writing tests before implementation
  - Red-Green-Refactor
---

# Test-First Development

Test-Driven Development: write tests before implementation.

## Red-Green-Refactor Cycle

1. **Red**: Write a failing test that describes the desired behavior.
2. **Green**: Write the minimum code to make the test pass.
3. **Refactor**: Clean up the code while keeping tests green.
4. **Repeat**: Move to the next behavior.

## Test Naming

Test names are sentences describing user-visible behavior:

```
TestCalculateTotalReturnsZeroForEmptyCart
TestProcessOrderReturnsErrorWhenItemOutOfStock
TestCreateUserSendsWelcomeEmailOnSuccess
```

## Test Priority

1. **Integration tests** — verify real behavior with real dependencies.
2. **Contract tests** — verify API contracts and interfaces.
3. **Unit tests** — verify isolated logic in pure functions.
4. **E2E tests** — verify complete user workflows.

Prefer integration tests over isolated unit tests. Use real databases over mocks. Use actual service instances over stubs.

## Structure

```
func TestXxx(t *testing.T) {
    // Arrange: set up test data and preconditions
    // Act: execute the behavior under test
    // Assert: verify the expected outcome
}
```

## Rules

- No implementation code without a failing test first.
- Tests are committed before the implementation they test.
- Test files live alongside source files, not in a separate tree.
- Mock only external services you don't control. Use real implementations for everything else.
- Every bug gets a regression test before the fix.

## Checklist

- [ ] Test written and failing (Red) before implementation
- [ ] Minimum code to pass (Green)
- [ ] Code refactored while tests stay green
- [ ] Test names read as sentences
- [ ] Integration tests preferred over mocks
- [ ] Bug has regression test
