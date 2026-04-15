---
name: security-by-default
description: Use when designing APIs, handling user input, or managing secrets.
---

# Security by Default

## Input Validation
- Validate at system boundaries; reject invalid input early
- Never trust user input — sanitize and validate all external data
- Use parameterized queries — never concatenate user input into SQL

## Secrets Management
- Never hardcode credentials, tokens, or keys in source
- Use environment variables or secret managers
- Never log secrets, tokens, or PII

## Authentication & Authorization
- Implement principle of least privilege
- Validate permissions at every boundary crossing
- Use timeouts on credential-bearing operations

## Data Handling
- Encrypt sensitive data at rest and in transit
- Mask PII in logs and error messages
- Use secure defaults; don't rely on users to configure security

## Dependency Security
- Keep dependencies updated
- Audit dependencies for known vulnerabilities
- Pin to specific versions in production

## Anti-patterns
- Don't eval user input
- Don't expose internal state in error messages
- Don't use predictable IDs for sensitive resources
