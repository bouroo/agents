---
name: go-code-quality
description: Language-agnostic code quality principles derived from Go best practices: write for reading, safe by default, wrap errors, avoid mutable globals, structured concurrency, decouple from environment, log actionable info. Use when writing, reviewing, or refactoring code for quality, readability, and maintainability.
license: MIT
metadata:
  author: kilo-config
  version: 1.0.0
  source: JetBrains Go 10x, Alex Edwards naming conventions
---

# Code Quality Commandments

Write code for humans first, compilers second.

## 1. Write Libraries, Not Programs

- Build reusable packages, not monolithic programs
- `main()` only parses flags, handles errors, orchestrates cleanup
- Flexible packages return data instead of printing
- Return errors rather than calling panic/exit
- Keep module structure simple: ideally one package

## 2. Test Everything

- Tests dogfood your APIs—awkward names and inconvenient APIs become obvious
- Test names should be sentences: `TestParseURLReturnsErrorForEmptyInput`
- Focus on small units of user-visible behavior
- Add integration tests for end-to-end checks
- Maintain >80% coverage on business logic
- Write tests before implementation (red-green-refactor)

## 3. Write Code for Reading

- Reduce cognitive load by refactoring
- Flatten nested conditionals; early returns over deep indentation
- Extract helper functions with descriptive names
- One concept per function

### Naming Conventions

- `camelCase` for unexported, `PascalCase` for exported
- Acronyms use consistent case: `HTTPClient`, not `HttpClient`
- `ID` is always uppercase: `userID`, `orderID`
- Short scope = short name (`i`, `err`, `ctx`); broad scope = descriptive name
- Avoid type in name: `count` not `intCount`
- Package names: lowercase, single word, no separators (`ordermanager`)
- Avoid chatter: `customer.New()` not `customer.NewCustomer()`
- Receiver names: 1-3 chars, consistent per type
- Getters: `Address()` not `GetAddress()`; Setters: `SetAddress()`
- Single-method interfaces: name by method + `-er` suffix (`Reader`, `Authorizer`)

### Identifier Length

- Narrow scope, used close to declaration: short names OK (`i`, `p`, `ch`)
- Broad scope, used far from declaration: descriptive names (`count`, `sum`, `results`)
- Use the right length—sometimes terse, sometimes descriptive

### Package Naming

- Lowercase ASCII letters and numbers only
- Simple one-word nouns: `orders`, `customer`, `slug`
- Multiple words concatenated: `ordermanager` not `orderManager`
- Avoid catch-all names: `utils`, `helpers`, `common`, `types`
- Avoid clashes with standard library package names

### File Naming

- One word, lowercase: `cookie.go`, `server.go`
- Multiple words: concatenate (`routingindex.go`) or underscore (`routing_index.go`)—pick one and be consistent
- Suffixes with special meaning: `_test.go`, `_linux.go`, `_amd64.go`

## 4. Be Safe by Default

- Use "always valid values"—design types so users can't create invalid values
- Make zero value useful, or write validating constructor
- Add configuration via `WithX()` methods: `NewWidget().WithTimeout(time.Second)`
- Use named constants instead of magic values: `http.StatusOK` not `200`
- Prevent security holes: validate inputs at boundaries
- Never require elevated privileges; configure minimal permissions

## 5. Wrap Errors, Don't Flatten

- Define sentinel errors: `var ErrNotFound = errors.New("not found")`
- Use `errors.Is()` and `errors.As()` for matching, not `==` or type assertion
- Wrap with context: `fmt.Errorf("loading %s: %w", id, err)`
- Never ignore errors with `_`
- Always check errors, handle if possible, retry where appropriate
- Reserve panic for unrecoverable internal errors only
- Exit gracefully with user-facing messages

## 6. Avoid Mutable Global State

- Package-level variables cause data races
- Use mutexes or channel-guarded goroutines for concurrent access
- Don't use global default objects—create new instances and configure
- Avoid mutable global state; use constructors or singletons with mutexes

## 7. Use Structured Concurrency Sparingly

- Don't introduce concurrency unless unavoidable
- Confine goroutines to their creating scope
- Ensure termination via context, WaitGroup, or errgroup
- Pass directional channels: `chan<-` for send, `<-chan` for receive
- Use `sync.Once` for lazy initialization
- Share data immutably when possible; avoid locks if you can

## 8. Decouple Code from Environment

- Don't use environment variables or args deep in packages—only `main` reads them
- Let users configure packages however they want
- Bundle static data into binary when possible
- Don't hard-code paths; use XDG or configurable directories
- Don't assume disk storage exists or is writable
- Be frugal with memory: handle one chunk at a time, re-use buffers

## 9. Design for Errors

- Show usage hints for incorrect arguments, don't crash
- Let users customize behavior with flags or config
- Report runtime errors to user and exit gracefully
- Validate all inputs at boundaries

## 10. Log Only Actionable Information

- Log only actionable errors someone needs to fix
- Never log secrets or personal data
- Log only actionable information; use tracing for request debugging
- Don't log performance data or statistics—use metrics instead
- Use structured logging (JSON) for machine readability

## Additional Principles

### Readability First

- Write for humans, not compilers
- Flatten nested conditionals
- Early returns over deep indentation
- Extract helper functions with descriptive names

### Structure & Design

- Library-first: reusable packages
- `main()` only orchestrates
- Make zero values useful
- Prefer `WithX()` methods for configuration
- Use named constants over magic values
- Decouple code from environment

### Error Handling

- Always check errors
- Define sentinel errors
- Wrap with context
- Use `errors.Is()` and `errors.As()`
- Reserve panic for unrecoverable errors

### Concurrency

- Use only when necessary
- Confine goroutines to creating scope
- Ensure termination
- Pass directional channels
- Prefer `sync.Once` for lazy init
- Share data immutably

### Performance

- Preallocate slices/maps with known capacity
- Use object pools for frequently allocated objects
- Buffer I/O operations; batch small operations
- Process data in chunks; avoid loading everything into memory
- Align struct fields to minimize padding
- Prefer stack allocation

### Safety & Security

- Always valid values by default
- Never log secrets or personal data
- Validate all inputs at boundaries
- Use path-safe operations to prevent traversal attacks
- Configure minimal permissions

## When to Use

- Writing new code
- Reviewing code for quality
- Refactoring for readability
- Establishing project conventions
- Onboarding new developers
