---
name: effective-code-craft
description: >
  A skill for crafting clean, maintainable, production-ready code.
  Use when writing new modules/packages, designing APIs, handling errors,
  writing tests, managing concurrency, or reviewing code for safety and clarity.
  Covers error handling, testing, readability, safe defaults, concurrency best practices,
  and general software craftsmanship — language-agnostic.
license: MIT
---

# Effective Code Craft

Ten universal principles for writing better code.

## 1. Structure Code for Reuse

Separate entry-point logic from domain logic. The top-level module should only handle argument parsing, config, and error reporting. Core logic lives in reusable, importable units.

- Entry points coordinate; they don't contain business rules
- Return data from functions rather than printing or emitting side effects
- Return errors rather than crashing; let callers decide how to handle failures
- Keep module boundaries clean and dependency-free

## 2. Test as You Write

Writing tests forces you to use your own APIs the way users will. Tests are also living documentation of intended behavior.

- Name tests as full sentences describing the expected outcome
- Test small, user-visible units — not internal implementation details
- Cover happy paths, error paths, and edge cases
- Add end-to-end/integration tests to verify system-level behavior

## 3. Design for Reading

Code is read far more often than written. Reduce the cognitive load on readers.

- Use consistent, deliberate naming conventions throughout
- Good names make code read almost like prose
- Extract low-level boilerplate into helpers with clear names
- Document intent at the component level; let code show the implementation

## 4. Make Invalid States Unrepresentable

Design types and APIs so that valid use is the easy path and invalid use is hard or impossible.

- Make zero/default values genuinely useful, not dangerous
- Use named constants instead of magic values scattered through code
- Validate inputs at boundaries; don't let bad data propagate silently
- Never expose internals that could be misused

## 5. Enrich Errors with Context

Errors carry information only if you preserve and augment them. Bare error values lose meaning as they propagate.

- Define named sentinel errors for distinguishable failure modes
- Wrap errors with context rather than converting to strings
- Preserve the error chain so callers can inspect or match specific errors
- Error messages should describe what failed and why, not just what happened

## 6. Avoid Mutable Global State

Global mutable state creates hidden coupling, race conditions, and unpredictable behavior in concurrent environments.

- Avoid package/module-level mutable variables
- Use proper synchronization when state must be shared (locks, atomic operations, ownership transfer)
- Don't rely on global default instances — prefer explicit dependency injection
- Single-owner threads/processes for mutable state simplify reasoning

## 7. Use Concurrency Only When Necessary

Concurrency is a tool, not a goal. Introducing it prematurely adds complexity and risk.

- Don't reach for concurrency unless the problem genuinely requires it
- Keep concurrent code localized and isolated
- Ensure all spawned tasks complete before the enclosing scope exits
- Use structured primitives that make termination explicit and safe

## 8. Decouple from Environment

Business logic should not depend on the execution environment.

- Environment variables and CLI arguments are a top-level concern — keep them out of deep modules
- Configuration flows inward via parameters or config objects, not global lookups
- Process data in bounded chunks to limit memory pressure
- Be explicit about resource limits rather than relying on implicit defaults

## 9. Handle Errors Deliberately

Every unchecked error is a latent bug. Errors are part of your API contract.

- Check errors at every call site where they can occur
- Handle where possible; retry only for transient failures; propagate otherwise
- Report failures gracefully to users with actionable guidance
- Never silently ignore errors — even in fallback paths

## 10. Log Actionable Information Only

Logs are for actionable decisions, not noise. Low-value logs are actively harmful.

- Log only what someone needs to investigate and fix a problem
- Use structured, queryable log fields — avoid unstructured text dumps
- Never log secrets, tokens, keys, or personal data
- Use distributed tracing for request-scoped debugging; use metrics for performance profiling
