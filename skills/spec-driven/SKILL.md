---
name: spec-driven
description: Structured Prompt-Driven Development (SPDD) workflows — REASONS Canvas for spec creation, prompt-code bidirectional sync, alignment before implementation, and iterative review. Use for planning features, writing specs, or any task where specifications drive code generation.
---

# Structured Prompt-Driven Development (SPDD)

Specifications and structured prompts are first-class delivery artifacts — version controlled, reviewed, reusable, and kept synchronized with code.

## Core Principle

When reality diverges from the spec, fix the spec first — then update the code. Never let spec and code silently diverge.

## The REASONS Canvas

### Abstract Parts (Intent & Design)
- **R — Requirements**: Problem and definition of done
- **E — Entities**: Domain objects, attributes, relationships
- **A — Approach**: Strategy, design decisions, rationale
- **S — Structure**: Where change fits; components and dependencies

### Specific Part (Execution)
- **O — Operations**: Ordered, testable steps down to method signatures

### Governance Parts
- **N — Norms**: Cross-cutting standards (naming, error handling, observability)
- **S — Safeguards**: Non-negotiable boundaries (invariants, limits, security)

## Three Core Skills

1. **Abstraction First** — Design before you generate
2. **Alignment** — Lock intent before writing code
3. **Iterative Review** — Controlled review-and-iterate loop

## Workflow Phases

1. **Story** → Independent, deliverable user stories (INVEST)
2. **Analysis** → Domain keywords, codebase scan, risks and gaps
3. **Canvas** → Generate the REASONS Canvas (executable blueprint)
4. **Generate** → Code task-by-task following Operations, Norms, Safeguards
5. **Test** → Tests from acceptance criteria. Verify coverage against spec
6. **Review** → Check alignment. Categorize adjustments. Sync both directions

## Spec-Code Sync

| Change Type | Direction |
|-------------|-----------|
| New feature | Spec → Code |
| Logic correction | Spec → Code (fix spec first) |
| Bug fix | Spec → Code (fix spec first) |
| Refactoring | Code → Spec (refactor first) |
| Performance | Code → Spec (optimize first) |

## Fitness

SPDD best for: scaled delivery, high compliance, team auditability, cross-cutting consistency.
SPDD overhead for: hotfixes, exploratory spikes, one-off scripts.
