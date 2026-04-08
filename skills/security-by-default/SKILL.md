---
name: security-by-default
description: Security-by-default design principles — safe defaults, input validation, path traversal prevention, secrets management, and least-privilege access. Use when handling user input, file access, authentication, authorization, or when the user mentions security, vulnerabilities, or safe defaults.
---

# Security by Default

Apply these principles whenever writing code that handles input, files, auth, networking, or data storage.

## Input Validation

- Validate all inputs at system boundaries: API handlers, CLI entry points, file readers, message consumers
- Never trust user input — sanitize and validate before processing
- Use **allowlists** over denylists where possible
- Validate types, ranges, lengths, and formats explicitly
- Reject unexpected input early; return clear, actionable error messages

## Path Traversal Prevention

- Use rooted/contained file access — never pass user input directly to file path operations
- Resolve paths and verify they stay within expected directories before access
- Never construct file paths from untrusted input without validation
- Prefer safe APIs that operate on file descriptors or handles over raw path strings

## Secrets Management

- Never commit secrets, API keys, tokens, or credentials to version control
- Use environment variables or secret managers for sensitive configuration
- Never log secrets, passwords, PII, or personal data
- Log only actionable information; scrub sensitive fields from log output

## Least Privilege

- Never run as root/admin unless absolutely necessary
- Grant minimum permissions required for each operation
- Prefer read-only access when writes aren't needed
- Scope tokens and credentials to the narrowest required permissions

## Safe Defaults

- Make safe values the default; require explicit opt-in for dangerous operations
- Design types that prevent invalid states — make illegal states unrepresentable
- Default to deny; require explicit allow
- Use secure defaults for crypto: modern algorithms (AES-256-GCM, Ed25519), adequate key sizes, authenticated encryption modes
- Set short expiration on tokens; require refresh

## Common Patterns

- **Parameterize queries** — never concatenate user input into SQL, shell commands, or URIs
- Set appropriate **timeouts** on all external calls (HTTP, DB, RPC)
- Use **HTTPS/TLS** for all network communication; disable fallback to plaintext
- Apply **rate limiting** on public-facing endpoints
- **Escape output** appropriate to context (HTML, JSON, shell, SQL)
- Use **constant-time comparison** for secrets and tokens to prevent timing attacks
- Keep dependencies updated; pin versions and audit for known vulnerabilities
