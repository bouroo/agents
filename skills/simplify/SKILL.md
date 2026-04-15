---
name: simplify
description: Use when refactoring, reducing technical debt, or reviewing code for unnecessary complexity.
---

# Simplification

## Core Principle
**Least mechanism** — Use the simplest solution that solves the problem.

## When to Refactor
- Function does multiple things (SRP violation)
- Naming is misleading or unclear
- Duplication exists across modules
- Knowledge is duplicated (single source of truth broken)
- Tests are brittle or over-specified

## Refactoring Rules
1. **Always have tests** before refactoring
2. **Make one change at a time** — small steps, verify each
3. **Preserve behavior** — tests must pass before and after
4. **No premature abstraction** — wait until duplication appears 3+ times

## Complexity Killers
- Unnecessary interfaces for simple cases
- Over-abstraction in single-method packages
- Framework features ignored in favor of custom solutions
- Extracting helpers for one-time operations

## Signal vs. Noise
High signal-to-noise ratio:
- Verbose logging that isn't actionable
- Comments stating the obvious
- Excessive error wrapping without context
- Boilerplate that does nothing

## Red Flags
- Functions > 40 lines
- Parameters > 5
- Nesting > 3 levels
- Imports > 20 packages
