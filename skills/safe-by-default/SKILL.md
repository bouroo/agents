---
name: safe-by-default
description: Language-agnostic safety patterns — always-valid values, input validation, sandboxed access, minimal permissions, and secure defaults.
---

# Safe by Default

## Always Valid Values

Design types so invalid states are unrepresentable:

- Use types that make illegal values impossible to construct
- Make the zero value useful, or write a validating constructor
- Use `WithX` methods for optional configuration
- Prefer sum types/enums over raw strings for finite options

## Named Constants

Replace magic values with named constants:

- `http.StatusOK` is self-explanatory; `200` is not
- Define constants so IDEs can auto-complete and prevent typos
- Group related constants using enum/iota patterns

## Input Validation

- Validate all inputs at system boundaries; reject early
- Never trust external data — validate, sanitize, encode
- Use parameterized queries for database access
- Prevent path traversal with sandboxed file access (`os.Root` or equivalent)

## Minimal Permissions

- Never require elevated privileges (root, admin)
- Let users configure the minimal permissions needed
- Use least-privilege principle for all resource access
- Sandbox file operations to prevent directory traversal

## Secure Defaults

- Default to deny; require explicit allow
- Default configurations should be secure, not convenient
- Never log secrets or personal data
- Use TLS for network communication by default
- Hash and salt passwords with modern algorithms

## Error Safety

- Error messages to users should not reveal internal details
- Stack traces belong in logs, not in API responses
- Sanitize error messages at system boundaries

## Checklist

- [ ] Invalid states are unrepresentable in type design
- [ ] All magic values replaced with named constants
- [ ] All external inputs validated at boundaries
- [ ] File access is sandboxed
- [ ] Minimal permissions configured
- [ ] No secrets in logs or error messages
- [ ] Secure defaults (deny-first)
