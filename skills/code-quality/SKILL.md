---
name: code-quality
description: Language-agnostic code quality principles for writing, reviewing, and refactoring code. Focus on readability, maintainability, and safety.
version: 1.0.0
triggers:
  - code quality discussions
  - code reviews
  - refactoring
  - writing new code
---

# Code Quality

Language-agnostic principles for writing readable, maintainable, and safe code.

## Principles

### Readability
- Write code for reading, not writing. Co-workers must understand it line by line.
- Use consistent naming: `err` for errors, `ctx` for contexts, `req`/`resp` for requests/responses.
- Design the architecture, name the components, document the details.
- Extract low-level paperwork into small functions with informative names.
- Functions should do one thing. If you need "and" in the name, split it.

### Structure
- Keep functions short. If it doesn't fit on screen, it's too long.
- Limit function parameters. Group related params into a struct or object.
- Avoid deep nesting. Guard clauses return early.
- Organize code by abstraction level. High-level intent at top, details below.

### Consistency
- Follow the conventions already established in the codebase.
- Same pattern for same problem. Don't invent new approaches without reason.
- Imports grouped: stdlib, third-party, internal.

### Comments
- Comments explain WHY, not WHAT. Code explains what.
- Remove commented-out code. Version control remembers.
- No TODO comments without a ticket reference.

## Review Checklist

- [ ] Readable top-to-bottom without jumping between files
- [ ] Consistent naming with the rest of the codebase
- [ ] No magic numbers or strings
- [ ] Functions have single responsibility
- [ ] No unnecessary complexity
- [ ] Error paths are handled explicitly
