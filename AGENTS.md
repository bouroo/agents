# AGENTS.md

Global coding standards and workflow principles for AI agents.
Language-agnostic. Environment-independent.

## Specification Before Implementation

- **Design before you generate.** Clarify objects, collaborations, and boundaries before writing code.
- **Lock intent before writing code.** Make "what we will do / what we won't do" explicit up front.
- **Treat specs as first-class artifacts.** Version-controlled, reviewed, and maintained alongside code.
- **Sync, don't hand off.** Keep specifications and code synchronized — when either side changes, reflect it back.

## REASONS Canvas

When approaching any non-trivial task, structure your thinking across these dimensions:

- **R**equirements — What problem are we solving? What is the definition of done?
- **E**ntities — Domain objects and their relationships.
- **A**pproach — The strategy to meet the requirements.
- **S**tructure — Where the change fits in the system; components and dependencies.
- **O**perations — Concrete, testable implementation steps.
- **N**orms — Cross-cutting engineering standards (naming, patterns, defensive coding).
- **S**afeguards — Non-negotiable constraints (invariants, performance limits, security rules).

## Code Craftsmanship

### Structure for Reuse
Separate entry-point logic from domain logic. Return data, not side effects. Return errors, don't crash.

### Test as You Write
Name tests as sentences. Cover happy paths, error paths, and edge cases. Tests are living documentation.

### Design for Reading
Consistent naming. Extract boilerplate into named helpers. Document intent at the component level.

### Make Invalid States Unrepresentable
Validate at boundaries. Use constants over magic values. Design types so misuse is hard.

### Enrich Errors with Context
Define named sentinel errors. Wrap with context, don't flatten to strings. Preserve error chains.

### Avoid Mutable Global State
No package-level mutable variables. Use explicit dependency injection over global defaults.

### Use Concurrency Sparingly
Only when the problem requires it. Keep it localized. Ensure all spawned tasks terminate.

### Decouple from Environment
Business logic has no knowledge of env vars, CLI args, or filesystem paths. Config flows inward.

### Handle Errors Deliberately
Check every error. Handle where possible, retry for transient failures, propagate otherwise. Never silently ignore.

### Log Actionable Information Only
Log only what someone needs to investigate and fix. Structured fields, never secrets. Use tracing for request debugging.

## Iterative Review

- Turn output into a controlled loop, not a one-shot draft.
- For logic corrections: update the spec first, then regenerate code.
- For refactoring: change the code first, then sync back to the spec.
- Verify core functionality before optimizing code quality.
- Make it work, then make it right.