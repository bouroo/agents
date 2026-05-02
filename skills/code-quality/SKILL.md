---
name: code-quality
description: Language-agnostic code quality principles for writing, reviewing, and refactoring code. Focus on readability, maintainability, and safety.
---

# Code Quality

## Write Code for Reading

- Consistent names: `err` for errors, `ctx` for contexts, `req`/`resp` for requests/responses
- Good names make code read naturally. Design the architecture, name the components, document the details
- Simplify wordy functions by extracting low-level paperwork into named helpers
- Flatten cognitive speed-bumps — ask a reader where they stumble

## Function Design

- One thing per function. If you need "and" in the description, split it
- Keep functions short enough to understand at a glance
- Extract complex conditionals into named helpers
- Use early returns and guard clauses over deep nesting

## State Management

- Avoid mutable global state; use explicit dependency injection
- Prefer immutability — return new values rather than modifying in place
- Keep state transitions explicit and traceable
- Use concurrency sparingly and keep it strictly confined

## Dependencies

- Decouple code from environment — only entry points access env vars, CLI args, or OS details
- Depend on abstractions (interfaces), not concrete implementations
- Keep external dependencies minimal and pinned
- Use framework features directly rather than wrapping them

## Review Checklist

- [ ] Names consistent and self-explanatory
- [ ] Functions short and single-purpose
- [ ] Errors checked, wrapped, propagated
- [ ] No mutable global state
- [ ] No unnecessary abstractions
- [ ] Code reads top-to-bottom without jumping
