---
name: code-quality
description: Use when writing, reviewing, or refactoring code. Applies to all languages.
---

# Code Quality

## Readability
- Purpose and rationale obvious from code itself
- Complex logic extracted to named functions
- Comments explain *why*, not *what*
- Avoid clever tricks; prefer obvious solutions

## Maintainability
- Predictable names, clear assumptions
- Minimal dependencies — each dependency is a liability
- Consistent style within a codebase
- Small functions with single responsibility

## Safety
- Zero values are useful (don't require initialization)
- Named constants over magic values
- Validate inputs at system boundaries
- Use `os.Root` instead of `os.Open` for file access

## Performance
- Preallocate slices/maps with known capacity
- Use buffered I/O for high-throughput paths
- Profile before optimizing — don't guess
- Keep values on stack via escape analysis

## Testing
- Test behavior, not implementation
- Cover error paths and edge cases
- Integration tests use real dependencies when safe
- Mocks only for non-deterministic or external dependencies

## Review Checklist
- [ ] No god objects (classes/modules doing too much)
- [ ] No circular dependencies
- [ ] No hidden coupling between packages
- [ ] Error handling is explicit and consistent
