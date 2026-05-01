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

Define named error values that callers can match against:

```
var ErrNotFound = errors.New("resource not found")
var ErrUnauthorized = errors.New("unauthorized access")
```

Callers use equality or type checks to branch behavior. Never inspect error string values.

## Error Wrapping

Add context without losing the original error:

```
return fmt.Errorf("processing order %d: %w", orderID, ErrNotFound)
```

This preserves the error chain so callers can still match the sentinel value through the wrapping.

## Structured Error Types

For rich error information, use custom error types:

```
type ValidationError struct {
    Field   string
    Value   interface{}
    Message string
}
```

Callers type-assert to access structured fields. This is better than parsing error strings.

## Error Categories

| Category | Action |
|----------|--------|
| Recoverable | Retry with backoff, fall back to default, log and continue |
| User error | Show usage hint, don't crash, suggest corrections |
| Programming error | Panic or fail fast with clear message |
| External failure | Wrap with context, retry if idempotent, propagate otherwise |

## Anti-patterns

- Ignoring errors with `_` or empty catch blocks
- Logging and returning the same error (double handling)
- Flattening errors into strings with `fmt.Sprintf` + `errors.New`
- Using errors as control flow (exceptions for expected conditions)
- Exposing internal details in error messages returned to users

## Checklist

- [ ] Every error is checked or explicitly documented as safe to ignore
- [ ] Errors are wrapped with operational context
- [ ] Sentinel errors are defined for each domain concept
- [ ] Error types preserve the chain (no flattening)
- [ ] User-facing errors hide internal details
- [ ] Usage hints provided for invalid arguments
