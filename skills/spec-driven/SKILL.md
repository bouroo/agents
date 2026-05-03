---
name: spec-driven
description: Structured Prompt-Driven Development (SPDD) workflows — REASONS Canvas for spec creation, prompt-code bidirectional sync, alignment before implementation, and iterative review.
version: 1.0.0
triggers:
  - SPDD methodology
  - REASONS Canvas
  - creating specifications
  - structured prompt development
---

# Spec-Driven Development (SPDD)

Structured Prompt-Driven Development: treat specs as first-class delivery artifacts.

## The REASONS Canvas

A seven-part structure that guides intent → design → execution → governance.

### Abstract Parts (Intent & Design)
- **R — Requirements**: What problem are we solving? Definition of Done.
- **E — Entities**: Domain entities and their relationships.
- **A — Approach**: The strategy for meeting the requirements.
- **S — Structure**: Where the change fits in the system. Components and dependencies.

### Specific Part (Execution)
- **O — Operations**: Concrete, testable implementation steps in order.

### Governance Parts (Standards)
- **N — Norms**: Cross-cutting engineering norms (naming, observability, defensive coding).
- **S — Safeguards**: Non-negotiable boundaries (invariants, performance limits, security rules).

## Workflow

```
Story → Analysis → Canvas → Generate → Test → Review → Sync
  ↑                                                      |
  └────────────── repeat until aligned ──────────────────┘
```

1. **Story**: Break requirements into independent, deliverable user stories (INVEST).
2. **Analysis**: Extract domain keywords, scan codebase, produce strategic analysis.
3. **Canvas**: Generate the full REASONS Canvas from analysis.
4. **Generate**: Produce code task-by-task, following Operations, Norms, Safeguards.
5. **Test**: Generate functional tests, then unit tests.
6. **Review**: Classify issues. Logic → update prompt then code. Style → refactor code then sync.
7. **Sync**: Keep Canvas and code synchronized bidirectionally.

## Sync Rules

### Prompt Update (Spec → Code)
When requirements change, update the Canvas first, then regenerate affected code.

### Code Sync (Code → Spec)
When code is refactored or fixed, sync the changes back into the Canvas.

## Rules

- The Canvas is the source of truth. Never manually edit generated code to fix logic.
- When output diverges from intent, fix the Canvas first.
- Never add features beyond what the spec defines.
- Every change must trace to a Canvas section.

## Checklist

- [ ] REASONS Canvas complete (all 7 parts)
- [ ] Operations are concrete and testable
- [ ] Norms and Safeguards defined
- [ ] Code generated task-by-task from Operations
- [ ] Tests cover acceptance criteria
- [ ] Canvas and code synchronized after changes
