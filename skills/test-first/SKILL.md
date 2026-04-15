---
name: test-first
description: Use before writing implementation code. Red-Green-Refactor cycle for all new functionality.
---

# Test-First Development

## Core Cycle

1. **Red** — Write a failing test that describes expected behavior
2. **Green** — Write minimal code to make it pass
3. **Refactor** — Improve code while tests stay green

## Test Naming
Test names should be sentences describing user-visible behavior:
- `TestValidateEmail_RuleViolation_ReturnsError`
- `TestCalculateTax_NonTaxableJurisdiction_ReturnsZero`

## What to Test
- Small units of user-visible behavior
- Edge cases and error paths
- Integration tests for real database/service interactions

## What NOT to Mock
Prefer real databases and services over mocks for integration tests. Mock only when:
- The dependency is slow or non-deterministic
- The dependency is an external service (payment gateway, etc.)

## Ordering
Create test files BEFORE implementation files. Verify test fails before writing implementation.
