---
name: spec-driven-development
description: >
  Specification-first workflow that treats prompts as version-controlled artifacts. Use when starting a new
  feature, resolving ambiguous requirements, or bridging intent and implementation. Grounded in Martin Fowler's
  SPDD and GitHub Spec-kit.
license: MIT
---

# Spec-Driven Development

A prompt-as-artifact workflow. **Spec is truth. Code serves spec, not the reverse.**

## REASONS Canvas

Use this 7-part structure for every spec:

| Section | Capture |
|---|---|
| **R — Requirements** | Problem, Definition of Done, acceptance criteria |
| **E — Entities** | Domain objects, relationships, boundaries |
| **A — Approach** | Chosen strategy, alternatives rejected, why |
| **S — Structure** | Component placement, dependencies, interfaces |
| **O — Operations** | Concrete, testable implementation steps in order |
| **N — Norms** | Cross-cutting rules: naming, error handling, documentation, code clarity |
| **S — Safeguards** | Non-negotiable boundaries: invariants, perf limits, security |

### Template

```markdown
## R — Requirements
[Problem. What does "done" mean?]

## E — Entities
[Domain objects and relationships]

## A — Approach
[Strategy, alternatives rejected, rationale]

## S — Structure
[Components, dependencies, interfaces]

## O — Operations
[Ordered, testable implementation steps]

## N — Norms
[Naming: scope-proportional, no repetition of context/type. Error handling: explicit, guard-clause-first. Documentation: name-first sentences for public symbols. Style: eliminate nesting, omit zero-value noise.]

## S — Safeguards
[Invariants, performance ceilings, security rules]
```

## Core Skills

1. **Abstraction-first** — Design objects, collaborations, and boundaries *before* generating code. Intent precedes implementation.
2. **Alignment** — Lock scope explicitly: what we will do, what we won't, what remains open. Visible in the spec.
3. **Iterative review** — Treat output as a controlled loop (spec → generate → verify → refine), not a one-shot draft.

## Workflow

Story → Analysis → Canvas → Generate → Test → Review → Sync

1. **Story** — Capture the user problem; surface the problem, not the solution.
2. **Analysis** — Identify entities, constraints, risks, unknowns.
3. **Canvas** — Fill every REASONS section; mark unknowns explicitly.
4. **Generate** — Write code from the spec, not intuition.
5. **Test** — Verify code satisfies every section of the spec.
6. **Review** — Check for orphans (code without spec) and gaps (spec without code).
7. **Sync** — Update spec and code together; never land one without the other.

## Spec Quality Checklist

- [ ] Every REASONS section is filled — no empty sections.
- [ ] Requirements have measurable acceptance criteria and a Definition of Done.
- [ ] Safeguards specify numeric limits (latency, size, error rates, quotas).
- [ ] Norms cover naming, logging, and error handling.
- [ ] Norms specify scope-proportional naming and guard-clause control flow.
- [ ] No in-band error signaling — errors are explicit, not sentinel values.
- [ ] Public symbols have name-first doc comments (full sentences).
- [ ] Unknowns are marked explicitly, not glossed over.
- [ ] Generated code has no orphaned features (in code but not in spec).
- [ ] Generated spec has no orphan requirements (in spec but not in code).

## Key Rules

- **Sync, not handoff** — spec and code evolve together; a stale spec is a bug.
- **No speculative features** — if it is not in the spec, do not build it.
- **Immutable principles** — never violate Norms or Safeguards for convenience.
- **Bidirectional feedback** — production reality informs spec evolution.

## Constitutional Gates (Spec-kit)

- **Simplicity** — prefer ≤3 projects at the initial implementation stage.
- **Anti-abstraction** — use the language's natural types; do not introduce a layer that does not add value.
- **Test-first** — write tests before implementation; tests encode the spec.
- **Integration-first** — prefer end-to-end tests that exercise real boundaries.
- **Library-first** — structure as reusable libraries with a thin CLI shim on top.
- **CLI interface** — every feature should be reachable from the command line.
- **Guard clauses** — handle errors and edge cases first; keep the happy path unindented.
- **No in-band errors** — return explicit error values, never overload return values to signal failure.
- **Eliminate repetition** — names must not repeat package, type, or surrounding context information.
- **Named construction** — use explicit field/parameter names when constructing external types; omit zero-value defaults.

## Norms Reference

Language-agnostic norms derived from production style guides. Specify these in the **N — Norms** section of every spec.

### Naming

- **Scope-proportional** — name length proportional to scope size and inversely proportional to usage frequency. Single-letter names for tiny scopes (`i`, `err`); descriptive names for package-level symbols.
- **No repetition** — names must not repeat their enclosing context. `db.Load`, not `db.LoadFromDatabase`. `count`, not `userCount` inside a `UserCount` method.
- **No type-in-name** — omit type information from variable names. `users`, not `usersSlice`; `limit`, not `limitInt`.

### Error Handling

- **Explicit returns** — functions that can fail return a separate error value, not in-band sentinels (-1, null, empty string).
- **Guard-clause flow** — handle errors and edge cases at the top of the function; keep the happy path unindented. Avoid else-after-return.
- **Wrap, don't flatten** — add context when propagating; preserve the cause chain. Never inspect error strings to branch.

### Documentation

- **Name-first sentences** — doc comments for public symbols begin with the symbol's name as a full sentence: `// Encode writes the JSON encoding of req to w.`
- **Show usage** — provide runnable examples for non-trivial APIs. Examples live in test files.

### Code Clarity

- **Eliminate nesting** — prefer early returns and guard clauses over deeply nested conditionals.
- **Omit zero-value noise** — only specify non-default values in construction. Default is zero/nil/false unless stated otherwise.
- **Named fields for external types** — always use explicit field names when constructing types from other packages.

## When to Use

- Starting a new feature, service, or module.
- Resolving ambiguous or conflicting requirements.
- Bridging intent and implementation across a team.
- Refactoring without losing context.
