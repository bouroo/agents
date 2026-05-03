---
name: safe-by-default
description: Language-agnostic safety patterns — always-valid values, input validation, sandboxed access, minimal permissions, and secure defaults.
version: 1.0.0
triggers:
  - safety patterns
  - input validation
  - security defaults
  - designing safe APIs
---

# Safe by Default

Language-agnostic patterns for writing secure, safe code.

## Always-Valid Values

Design types so users cannot accidentally create invalid states:

- Use validating constructors. The zero value should be unusable or safe.
- Make invalid states unrepresentable. Use enums, sum types, or marker interfaces.
- Configuration via `WithX` methods that return a new instance.

```
server := NewServer().WithTimeout(30 * time.Second).WithTLS(cert)
```

## Input Validation

Validate all inputs at system boundaries. Never trust external data:

- Validate at the edge (API handlers, CLI args, file readers).
- Internal code trusts validated data. No re-validation deep in packages.
- Fail fast with clear error messages on invalid input.
- Sanitize for the context: HTML, SQL, shell, path.

## Minimal Permissions

- Request the minimum permissions needed. Never run as root/admin.
- File access scoped to required directories only.
- Network access restricted to needed endpoints.
- Docker containers run as non-root user.

## Secure Defaults

- TLS on by default. Opt-out, not opt-in.
- Timeouts on all network operations. No infinite waits.
- Rate limiting on public endpoints.
- Secrets from environment/secret manager, never hardcoded.

## Rules

- If a type can be in an invalid state, the API is wrong.
- Every external input is hostile until validated.
- Default-deny for permissions and access.
- Security errors are logged, never silently swallowed.

## Checklist

- [ ] Types prevent invalid states by construction
- [ ] Input validated at system boundaries
- [ ] Timeouts set on all I/O operations
- [ ] Minimal permissions requested
- [ ] No secrets in code or logs
- [ ] Defaults are secure
