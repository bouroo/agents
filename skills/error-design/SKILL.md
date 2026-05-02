---
name: error-design
description: Language-agnostic error handling patterns — sentinel errors, error wrapping, structured error types, and actionable error messages.
---

# Error Design

## Core Principles

- Always check errors. Handle when possible, retry when appropriate, report otherwise
- Wrap errors with context; don't flatten them into strings
- Define named sentinel errors users can match against
- Use structured error types that preserve the error chain
- Reserve panics/exceptions for internal program errors only
- Show usage hints for incorrect arguments; don't crash

## Sentinel Errors

Define named error values callers can match against. Never inspect error string values.

## Error Wrapping

Add context without losing the original error. Preserve the chain so callers can still match the sentinel value through wrapping.

## Error Categories

| Category | Action |
|----------|--------|
| Recoverable | Retry with backoff, fall back, log and continue |
| User error | Show usage hint, suggest corrections |
| Programming error | Fail fast with clear message |
| External failure | Wrap with context, retry if idempotent |

## Anti-patterns

- Ignoring errors with `_` or empty catch blocks
- Logging and returning the same error (double handling)
- Flattening errors into strings
- Using errors as control flow
- Exposing internal details in user-facing error messages
