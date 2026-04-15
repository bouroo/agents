---
name: go-excellence
description: Go-specific best practices. Apply when writing, reviewing, or refactoring Go code.
---

# Go Excellence

## Package Design
- Write packages, not programs — your `main()` should only parse flags
- Return useful errors; don't print or panic from libraries
- Use `pkg/errors` or `fmt.Errorf %w` to wrap errors — never flatten

## Error Handling
- Define sentinel errors: `var ErrNotFound = errors.New("not found")`
- Use `errors.Is` / `errors.As` for error inspection
- Always check errors; never ignore with `_`
- Reserve `panic` for truly unrecoverable internal states

## Safety by Default
- Use always-valid values; design types that prevent invalid states
- Avoid mutable global state — package-level vars cause data races
- Don't use `http.DefaultServeMux`

## Concurrency
- Use goroutine worker pools to cap resources
- Ensure goroutines terminate before the enclosing function exits
- Take send OR receive aspect of channels, not both
- Use atomics or mutexes for shared state

## Reading & Naming
- Code is read more than written — optimize for reading
- Conventional casing: `APIKey`, `HTTPClient`, `ID`
- Short names for narrow scope: `i`, `err`, `buf`, `req`, `resp`
- Booleans start with `is`, `has`, `can`, `should`: `isValid`
- Verbs for functions: `Validate`, `Calculate`, `Fetch`
- Nouns for types: `User`, `Repository`, `Handler`

## Logging
- Use structured logging (slog JSON)
- Log only actionable errors — never secrets, tokens, or PII
