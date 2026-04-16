---
description: Refactor code for clarity, performance, and safety without breaking public API
---

# /refactor

Refactor the target code to improve readability, performance, and safety while preserving all public API contracts.

## Steps

1. **Analyze** — Read the code, identify the public API surface, and map all callers to ensure no breaking changes
2. **Refactor** — Apply improvements below
3. **Validate** — Run linter, type checker, and tests; confirm public API unchanged
4. **Report** — Summarize changes, trade-offs, and remaining issues

## Principles

### Readability
- Flatten nested conditionals; early returns over deep indentation
- Extract helpers with descriptive names; one concept per function
- Reduce cognitive load — write for humans
- Use consistent naming: `err` for errors, `ctx` for contexts, `i` for index, `req`/`resp` for requests/responses
- `camelCase` for private, `PascalCase` for public; acronyms consistent (`HTTPClient`, `userID`)
- Short scope = short name; broad scope = descriptive name
- Avoid type in name (`count` not `intCount`); avoid chatter (`orders.New()` not `orders.NewOrder()`)
- Getters: `Address()` not `GetAddress()`; Setters: `SetAddress()`

### Architecture
- Library-first: reusable packages, `main()` only orchestrates
- Make zero values useful; use validating constructors
- Prefer `WithX()` methods for configuration
- Named constants over magic values
- Avoid mutable global state; use mutexes or channel-guarded goroutines
- Decouple from environment: only `main` reads env vars/args

### Error Handling
- Always check errors; never ignore with `_`
- Define sentinel errors; wrap with context (`%w` pattern)
- Use `errors.Is()` / `errors.As()` for matching
- Reserve `panic` for unrecoverable internal errors

### Concurrency
- Use concurrency only when necessary
- Confine goroutines to their creating scope
- Ensure termination via `context`, `WaitGroup`, or `errgroup`
- Pass directional channels (send-only or receive-only)
- Prefer `sync.Once` for lazy initialization

### Performance
- Preallocate slices/maps with known capacity
- Use object pools for frequently allocated objects
- Buffer I/O; batch small operations
- Process data in chunks; avoid loading everything into memory
- Prefer stack allocation; verify with escape analysis
- Align struct fields to minimize padding

### Safety
- Always valid values by default
- Never log secrets or personal data
- Validate all inputs at boundaries
- Log only actionable information; use tracing for request-scoped debugging
