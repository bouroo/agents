---
name: error-design
description: Language-agnostic error handling patterns — sentinel errors, error wrapping, structured error types, and actionable error messages.
version: 1.0.0
triggers:
  - error handling design
  - defining error types
  - error wrapping patterns
  - actionable error messages
---

# Error Design

Language-agnostic patterns for robust error handling.

## Patterns

### Sentinel Errors
Define named error values that callers can match against. Never compare error strings.

```
var ErrNotFound = errors.New("resource not found")
var ErrUnauthorized = errors.New("unauthorized access")
```

### Error Wrapping
Wrap errors with context to preserve the chain. Don't flatten into strings.

```
return fmt.Errorf("processing order %d: %w", orderID, err)
```

### Structured Error Types
Use typed errors when callers need to extract structured information:

```
type ValidationError struct {
    Field   string
    Message string
}
```

### Actionable Messages
Every error reported to users must include:
- **What** happened
- **Where** it happened (which component/operation)
- **What** the user should do about it

## Rules

- Always check errors. Never discard with `_`.
- Don't panic for user-caused conditions. Return errors.
- Wrap errors at package boundaries with context.
- Sentinel errors for conditions callers need to handle.
- Structured errors for conditions callers need to inspect.
- Log the full error chain. Show the actionable message to users.

## Checklist

- [ ] Named sentinel errors for matchable conditions
- [ ] Errors wrapped with context at boundaries
- [ ] No error strings compared with `==`
- [ ] No errors silently discarded
- [ ] User-facing messages are actionable
