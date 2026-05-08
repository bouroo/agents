---
name: spec-driven-development
description: A specification-first workflow that treats prompts as version-controlled artifacts. Use when starting new features, resolving ambiguous requirements, or bridging gap between intent and implementation. Aligns teams through the REASONS canvas — a shared template for surfacing requirements, entities, approach, structure, operations, norms, and safeguards.
license: MIT
---

# Spec-Driven Development

A prompt-as-artifact workflow. Specs are first-class — they precede code, version with it, and drive implementation.

## Core Principle

**Spec is truth. Code serves spec, not the reverse.**

When reality diverges from spec: fix the spec first, then update the code. Never patch code without updating the spec.

## REASONS Canvas

Use this 7-part structure when drafting any spec:

| Section | What to capture |
|---------|-----------------|
| **R — Requirements** | Problem statement, Definition of Done, acceptance criteria |
| **E — Entities** | Domain objects, relationships, boundaries |
| **A — Approach** | Strategy to meet requirements, alternatives considered |
| **S — Structure** | Where change fits, components, dependencies, interfaces |
| **O — Operations** | Concrete, testable implementation steps |
| **N — Norms** | Cross-cutting engineering rules — naming, observability, defensive coding |
| **S — Safeguards** | Non-negotiable boundaries — invariants, performance limits, security rules |

**Template:**

```
## R — Requirements
[What problem does this solve? What does "done" mean?]

## E — Entities
[Domain objects and their relationships]

## A — Approach
[Strategy, chosen path, alternatives rejected and why]

## S — Structure
[Component placement, dependencies, interfaces]

## O — Operations
[Testable implementation steps in order]

## N — Norms
[Naming conventions, observability, defensive coding rules]

## S — Safeguards
[Invariants, performance ceilings, security boundaries]
```

## Core Skills

1. **Abstraction-first** — Design objects, collaborations, and boundaries *before* generating code. Clarity on intent precedes implementation.
2. **Alignment** — Lock scope explicitly: what we will do, what we won't do, what remains open. Make it visible in the spec.
3. **Iterative review** — Treat output as a controlled loop, not a one-shot draft. Spec → generate → verify → refine → repeat.

## Workflow

1. **Requirements** — Surface the problem, not the solution. Gather from users, stakeholders, existing systems.
2. **Analysis** — Identify entities, constraints, risks. Ask: what is unknown?
3. **Canvas** — Fill the REASONS canvas. Leave no section empty.
4. **Generate** — Write code from spec, not intuition.
5. **Verify** — Test against spec. Does the code satisfy every section?
6. **Refine** — When gaps appear, update the spec first. Then update code.

## Spec Quality Checklist

- [ ] Every REASONS section is filled
- [ ] Requirements have clear acceptance criteria
- [ ] Safeguards specify measurable limits (latency, size, error rates)
- [ ] Norms cover naming, logging, error handling
- [ ] Unknowns are marked explicitly, not glossed over
- [ ] Generated code has no orphaned features (features in code but not in spec)

## Key Rules

- **Sync, not handoff** — spec and code evolve together. A stale spec is a bug.
- **No speculative features** — if it's not in the spec, don't build it.
- **Immutable principles** — don't violate Norms or Safeguards for convenience.
- **Bidirectional feedback** — production reality informs spec evolution.

## When to Use

- Starting a new feature or service
- Resolving ambiguous or conflicting requirements
- Bridging intent and implementation on a team
- Refactoring without losing context