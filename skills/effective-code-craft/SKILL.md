---
name: effective-code-craft
description: >
  Apply language-agnostic software craftsmanship principles. Use when writing, reviewing, or refactoring
  code for clarity, safety, testability, or efficiency. Grounded in the JetBrains 10x rules and the
  Google style guide.
compatibility: opencode, kilo
disable-model-invocation: false
---

# Effective Code Craft

Ten commandments for high-quality code, distilled from the JetBrains 10x rules and Google style principles.

## Style Priorities

Apply in order; when they conflict, the higher priority wins.

1. **Clarity** — purpose and rationale are obvious to the reader, who sees *what* and *why*, through their lens, not the author's.
2. **Simplicity** — simplest solution that works; least mechanism: prefer core language → standard library → third-party.
3. **Concision** — high signal-to-noise; eliminate repetition, opaque names, and unnecessary abstraction.
4. **Maintainability** — easy for the next programmer to change correctly; APIs grow gracefully with minimal coupling.
5. **Consistency** — match the surrounding codebase; in a tie, consistency beats personal taste.

## 1. Write Libraries, Not Monoliths

- Structure code as reusable packages with clean public APIs; keep the entry point minimal (parse, handle errors, delegate).
- Return data, not side effects. Return errors, never crash.
- Apply least mechanism: reach for built-ins before frameworks.

## 2. Test Everything

- Test names read as sentences about behavior. Cover happy path, error path, edge cases.
- Add integration tests for end-to-end flows; use tests to dogfood your own APIs.
- Prefer runnable examples as living documentation that cannot drift from the code.
- Grade the tests, not just the code: a green suite is one signal, not proof. Prefer mutation testing to expose tests that pass without exercising logic — see [harness-engineering](../harness-engineering/SKILL.md) §12.

## 3. Code for Reading

- Name length scales with scope: short for locals (`i`, `buf`, `err`), longer at package level. Single-word names first; add words only to disambiguate.
- Omit type-like words (`users` over `userSlice`) and context the surrounding API already provides (`count`, not `userCount`, inside `UserCount`).
- Avoid `get`/`Get` prefixes; start with the noun. Don't repeat package names in exported symbols (`widget.New`, not `widget.NewWidget`).
- Comments explain *why*, not *what*. Doc comments are full sentences beginning with the symbol's name.

## 4. Safe by Default

- Make invalid states unrepresentable; provide a useful zero value or a validating constructor.
- Use named constants, not magic values. Apply least-privilege to capabilities and permissions.
- Encode rules in types, constants, and validators rather than model judgment — deterministic logic belongs in tested code, not the LLM (see [harness-engineering](../harness-engineering/SKILL.md) §11).
- Avoid in-band errors (sentinel values like `-1`, `null`); use explicit error returns or `ok` booleans.

## 5. Wrap Errors, Don't Flatten

- Define sentinel errors; wrap with context while preserving the chain (so `Is`/`As` still work).
- Never inspect error strings to identify error types.
- Add context only when it conveys new information; don't restate what the underlying error already says.

## 6. No Mutable Globals

- No package-level mutable variables. Inject dependencies explicitly.
- If shared mutable state is unavoidable, guard with synchronization or isolate behind a single owner with message passing.

## 7. Concurrency Sparingly

- Introduce concurrency only when required. Confine threads/tasks to the creating scope; never leak globally.
- Every concurrent task must terminate before its parent exits. Use structured concurrency primitives.
- Simplicity first: a sequential solution is usually cheaper to read, test, and debug than a parallel one.

## 8. Decouple from Environment

- Only the entry point reads env vars, CLI args, or filesystem paths. Business logic stays pure.
- Embed static assets; stream or chunk large data; reuse buffers.
- Factor out repeated scaffolding (table-driven patterns) so differences stand out clearly.

## 9. Design for Errors

- Handle errors before continuing with the normal flow — indent error paths, keep the happy path unindented.
- Check every error. Handle where possible, retry transient failures, propagate the rest.
- Show usage hints for invalid input. Reserve fatal exits for unrecoverable internal failures.

## 10. Log Actionable Information Only

- Log only what someone must investigate and fix. Structured fields, never secrets.
- Use tracing for request debugging and metrics for performance, not logs.

## Guru Meditation

Make it work, then make it right — walking skeleton first, real users second, refactor while it is fresh. When in doubt, choose the simpler mechanism and the clearer name.
