---
name: error-design
description: Use when designing error types, error handling patterns, or API error responses.
---

# Error Design

## Sentinel Errors
Define named error values for conditions callers may check:
```go
var (
    ErrNotFound   = errors.New("not found")
    ErrInvalidInput = errors.New("invalid input")
)
```

## Wrapping
Use `fmt.Errorf("%w", err)` to preserve error chain for `errors.Is`/`errors.As`.
Never flatten errors: `return err` loses context.

## Type Assertions on Errors
Avoid `err.(type)` switches. Use `errors.As` for typed errors:
```go
var perr *ValidationError
if errors.As(err, &perr) {
    perr.Field // access specific fields
}
```

## API Error Responses
Return structured errors with machine-readable codes and human messages:
```go
type ErrorResponse struct {
    Code    string `json:"code"`
    Message string `json:"message"`
}
```

## Don't
- Never `fmt.Println(err)` or silently ignore errors with `_`
- Never return `nil` for an error — it's ambiguous
- Reserve `panic` for truly unrecoverable states

## Library Errors
Return errors to callers; don't log them. Let the application layer decide logging.
