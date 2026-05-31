---
name: effective-code-craft
description: >
  Apply language-agnostic software craftsmanship, performance optimization, and architectural best practices derived from engineering principles.
  Use when writing, reviewing, or refactoring code for clarity, safety, concurrency, testability, or efficiency.
license: MIT
---

# High-Performance Engineering Commandments

A distilled set of architectural, readability, and performance principles applicable across any language or runtime.

## 1. Write Libraries, Not Monoliths

- Structure code as reusable packages/modules with clean public APIs.
- Keep the application entry point (`main`) minimal: parse arguments, handle errors, and delegate to domain packages.
- Return data instead of side effects (e.g., printing); return errors instead of crashing.
- Prefer flat module structures; one package per concern reduces cognitive overhead.

## 2. Test Everything

- Test names should read as sentences describing behavior.
- Focus unit tests on small, user-visible behaviors.
- Add integration tests for end-to-end flows.
- Use tests to "dogfood" your APIs; awkward APIs reveal themselves when consumed.

## 3. Write Code for Reading

- Choose consistent, idiomatic short names for local/loop variables (e.g., `err`, `buf`, `i`, `req`, `resp`, `ctx`).
- Use longer, descriptive names for package-level identifiers.
- Keep functions short; extract low-level "paperwork" into well-named helpers.
- Avoid naming identifiers after built-in types or keywords.
- Acronyms and initialisms should have consistent casing within an identifier (e.g., `APIKey`, `userID`).

## 4. Be Safe by Default

- Design types so that invalid states are unrepresentable ("make illegal states unrepresentable").
- Provide a useful zero value for literals, or a validating constructor with sensible defaults.
- Use named constants instead of magic numbers/strings.
- Apply the principle of least privilege: do not require elevated permissions when configurable minimal permissions suffice.

## 5. Wrap Errors, Don't Flatten

- Define sentinel error values for consumers to match against.
- Add context to errors without losing the original cause; preserve the error chain so `errors.Is`-style checks still work.
- Never inspect error strings to determine error types.

## 6. Avoid Mutable Global State

- Do not rely on package-level mutable variables.
- Do not use mutable default/global instances; always instantiate and configure your own.
- If shared mutable state is unavoidable, guard access with synchronization primitives (mutexes) or isolate it behind a single goroutine/thread with a message channel.

## 7. Use Concurrency Sparingly and Structurally

- Do not introduce concurrency unless it is unavoidable.
- Confine goroutines/threads to the scope where they are created; do not let them leak globally.
- Ensure every concurrent task terminates before its enclosing function exits (use `WaitGroup`, `errgroup`, or structured concurrency primitives).
- When passing channels, specify directionality (send-only or receive-only) to prevent deadlocks.

## 8. Decouple Code from Environment

- Only the application entry point should read environment variables or command-line arguments.
- Let users configure packages however they want; do not hard-code paths, environment assumptions, or file-system dependencies.
- Embed static assets into the binary instead of relying on external files.
- Be frugal with memory: stream or chunk data instead of loading everything at once; reuse buffers.

## 9. Design for Errors

- Always check and handle errors; do not silently ignore them.
- Retry where appropriate; report runtime errors to users and exit gracefully.
- Reserve fatal crashes/panics for unrecoverable internal program errors, not expected runtime failures.
- Show usage hints for invalid inputs instead of crashing.

## 10. Log Only Actionable Information

- Log only actionable errors that someone must fix.
- Use structured logging (e.g., JSON) for machine parsing.
- Never log secrets, credentials, or personal data.
- Do not use logs for request-scoped debugging (use tracing) or performance data (use metrics).

## 11. Performance & Memory Efficiency

- Preallocate collections (slices, maps, arrays) when the final size is known or predictable.
- Keep hot-path values on the stack where possible; avoid unnecessary heap allocations.
- Reuse objects via pooling in high-allocation paths instead of allocating on every iteration.
- Prefer zero-copy techniques (e.g., slicing, views, references) over duplicating data.
- Share immutable data across threads safely without locks.
- Avoid unnecessary interface/indirect boxing in hot loops.
- Pass lightweight request-scoped values through explicit parameters rather than ambient context maps when possible.

## 12. Naming Conventions

- Use `camelCase` for private identifiers and `PascalCase` for public/exported identifiers.
- ASCII letters are strongly preferred in identifiers.
- Getters should use the property name directly (e.g., `owner()`), omitting `get` prefixes.
- Boolean variables and functions should read as assertions (e.g., `isValid`, `hasPermission`, `canRead`).
- Loop/range variables are typically one letter (e.g., `i`, `v`, `k`).

## Guru Meditation

Make it work first, then make it right. Draft a walking skeleton with shameless-green implementation, validate it with real users, and then invest the extra effort in refactoring, simplifying, and improving while the code is still fresh in memory.
