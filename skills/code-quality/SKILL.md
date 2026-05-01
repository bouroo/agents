---
name: code-quality
description: Language-agnostic code quality principles for writing, reviewing, and refactoring code. Focus on readability, maintainability, and safety.
---

# Code Quality

## Write Code for Reading

- Use consistent, conventional names: `err` for errors, `ctx` for contexts, `req`/`resp` for requests/responses
- Good names make code read naturally. Design the architecture, name the components, document the details
- Simplify wordy functions by extracting low-level paperwork into named helpers (`createRequest`, `parseResponse`)
- Ask a co-worker to read your code line by line — their stumbles reveal speed-bumps to flatten

## Function Design

- Each function should do one thing. If you need "and" in the description, split it
- Keep functions short enough to understand at a glance
- Extract complex conditionals into named helper functions
- Avoid deep nesting — use early returns and guard clauses

## Error Handling

- Always check errors. Handle when possible, retry when appropriate, report otherwise
- Wrap errors with context; don't flatten them into strings
- Define named sentinel errors users can match against
- Reserve panics/exceptions for internal program errors only
- Show usage hints for incorrect arguments; don't crash

## State Management

- Avoid mutable global state; use explicit dependency injection
- Prefer immutability — return new values rather than modifying in place
- Keep state transitions explicit and traceable
- Use concurrency sparingly and keep it strictly confined

## Dependency Management

- Decouple code from environment — only entry points access env vars, CLI args, or OS details
- Depend on abstractions (interfaces), not concrete implementations
- Keep external dependencies minimal and pinned
- Use framework features directly rather than wrapping them

## Review Checklist

- [ ] Names are consistent and self-explanatory
- [ ] Functions are short and single-purpose
- [ ] Errors are checked, wrapped, and propagated
- [ ] No mutable global state
- [ ] No unnecessary abstractions
- [ ] Code reads top-to-bottom without jumping around
