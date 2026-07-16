---
name: spec-driven-development
description: >
  Specification-first workflow that treats prompts as version-controlled artifacts. Use when starting a new
  feature, resolving ambiguous requirements, or bridging intent and implementation. Grounded in Martin Fowler's
  SPDD and GitHub Spec-kit.
---

# Spec-Driven Development

A prompt-as-artifact workflow. **Spec is truth. Code serves spec, not the reverse.**

## REASONS Canvas

Use this 7-part structure for every spec:

| Section | Capture |
|---|---|
| **R  --  Requirements** | Problem, Definition of Done, acceptance criteria |
| **E  --  Entities** | Domain objects, relationships, boundaries |
| **A  --  Approach** | Chosen strategy, alternatives rejected, why |
| **S  --  Structure** | Component placement, dependencies, interfaces |
| **O  --  Operations** | Concrete, testable implementation steps in order |
| **N  --  Norms** | Cross-cutting rules: naming, error handling, documentation, clarity |
| **S  --  Safeguards** | Non-negotiable boundaries: invariants, perf limits, security |

### Template

Use for every non-trivial task. Fill every section. Mark unknowns with `[NEEDS CLARIFICATION]`.

```markdown
## R  --  Requirements
- Problem statement
- Definition of Done (measurable)
- Acceptance criteria (testable)

## E  --  Entities
- Domain objects and relationships
- Existing vs. new boundaries
- Data flow between entities

## A  --  Approach
- Chosen strategy and rationale
- Alternatives considered and rejected
- Key trade-offs

## S  --  Structure
- Where the change fits in the codebase
- Components, dependencies, interfaces
- Files to create or modify

## O  --  Operations
- Ordered, testable implementation steps
- Each step precise enough for a subagent to execute without ambiguity
- Test scenarios: happy path, error path, edge cases
- At least one step exercises an end-to-end boundary

## N  --  Norms
- Naming: scope-proportional, no context/type repetition
- Error handling: explicit returns, guard-clause-first, wrap-with-context
- Documentation: name-first sentences for public symbols
- Style: eliminate nesting, omit zero-value noise
- Reference AGENTS.md "Code Craft Norms" for the full norm set

## S  --  Safeguards
- Invariants that must hold
- Performance ceilings (latency, memory, size limits with numbers)
- Security rules (no secrets in logs, least privilege)
- Non-negotiable constraints
```

## Core Skills

1. **Abstraction-first**  --  Design objects, collaborations, and boundaries *before* generating code. Intent precedes implementation.
2. **Alignment**  --  Lock scope explicitly: what we will do, what we won't, what remains open. Visible in the spec.
3. **Iterative review**  --  Treat output as a controlled loop (spec → generate → verify → refine), not a one-shot draft.

## Prompt Discipline (think → do)

Follow the general task loop in `AGENTS.md` §3; SPDD-specific work fills the REASONS canvas, records assumptions, and verifies each canvas step with executable checks.

Be specific: name files, symbols, and acceptance criteria; give examples and specify output format. Vague prompts produce vague specs; vague specs produce wrong code. When ambiguous, resolve against best practice and record the assumption -- don't silently guess.

**Source:** Kilo -- Prompt Engineering (https://kilo.ai/docs/customize/prompt-engineering).

## Workflow

Use the general loop from `AGENTS.md` §3, with this SPDD sequence:

```
Story → Analysis → Canvas → Generate → Test → Review → Sync
```

1. **Story** -- capture the user problem; surface the problem, not the solution.
2. **Analysis** -- identify entities, constraints, risks, and unknowns.
3. **Canvas** -- fill every REASONS section; mark unknowns explicitly.
4. **Generate** -- write code from the spec, not intuition.
5. **Test** -- verify code satisfies every section of the spec.
6. **Review** -- check for orphans (code without spec) and gaps (spec without code).
7. **Sync** -- update spec and code together; never land one without the other.

### Why the workflow is phased -- cognitive load, not ceremony

Intent confirmation is distributed across steps: problem, design, operations, behavior, and code are checked at separate checkpoints so review attention stays focused.

### Test sequencing -- a deliberate inversion of TDD

- **API / end-to-end tests come early** -- validate behavior at the system boundary.
- **Code review then focuses on human judgment** -- logic, architecture, trade-offs, and non-functional concerns.
- **Unit tests come last as a regression net** -- lock behavior after intent and implementation stabilize.

Grade the tests themselves (mutation testing) -- see [harness-engineering](../harness-engineering/SKILL.md) §12.

## Fitness  --  when to spec, and when not to

SPDD pays off in logic-heavy, repeatable, high-constraint work. Decide up front.

| Fit | Scenario |
|---|---|
| ★★★★★ | Scaled, standardized delivery; high-compliance / hard-constraint systems; multi-person traceable changes; cross-cutting consistency refactors. |
| ★★☆☆☆ | Hotfixes under fire; exploratory spikes; one-off/disposable scripts. |
| ★☆☆☆☆ | Context black holes (domain rules unclear, no boundaries); pure aesthetic/visual work driven by taste, not logic. |

For low-fit cases, skip the canvas and note the assumption. For hotfixes: stabilize first, then close the governance loop afterward (update the spec/asset retroactively so production signal feeds back).

## Three Triggers to Tighten a Spec

When output is wrong, the fix is usually a sharper spec, not a louder prompt:

- **Behavioral mismatch** (output deviates from acceptance criteria) → logic-correction: update the spec first, then regenerate the code.
- **Overcomplicated logic** (solution more elaborate than the problem warrants) → **Approach** or **Operations** is under-specified; tighten the constraints.
- **Instruction failure** (agent ignores a Norm or Safeguard) → make that constraint more prominent and unambiguous in the spec.

## Spec Quality Checklist

Verify before delegation:

- [ ] Every REASONS section filled  --  no empty sections.
- [ ] Requirements have measurable acceptance criteria and a Definition of Done.
- [ ] Safeguards specify numeric limits (latency, size, error rates, quotas).
- [ ] Norms cover naming, logging, error handling.
- [ ] Norms specify scope-proportional naming and guard-clause control flow.
- [ ] No in-band error signaling  --  errors explicit, not sentinel values.
- [ ] Public symbols have name-first doc comments (full sentences).
- [ ] Unknowns marked `[NEEDS CLARIFICATION]`, not glossed over.
- [ ] Operations ordered and testable  --  a subagent can execute sequentially.
- [ ] No orphaned features (in code but not in spec).
- [ ] No orphan requirements (in spec but not in code).

## Key Rules

- **Sync, not handoff**  --  spec and code evolve together; a stale spec is a bug.
- **No speculative features**  --  if it's not in the spec, don't build it.
- **Immutable principles**  --  never violate Norms or Safeguards for convenience.
- **Bidirectional feedback**  --  production reality informs spec evolution.
- **Logic change** → update spec first, then regenerate code; **Refactor (no behavior change)** → change code first, then sync spec. Never land one side without the other.

## Constitutional Gates (Spec-kit)

Keep these SPDD-specific gates; use [effective-code-craft](../effective-code-craft/SKILL.md) for general code norms (naming, error handling, documentation, clarity -- state only SPDD-specific additions in the canvas's N -- Norms section):

- **Simplicity** -- prefer ≤3 projects initially.
- **Anti-abstraction** -- use natural language types; add no valueless layers.
- **Test-first** and **Integration-first** -- write tests before implementation and prefer real-boundary end-to-end coverage.
- **Library-first** and **CLI interface** -- use reusable libraries with a thin CLI shim; make every feature reachable from the command line.
- **Named construction** -- use explicit fields/parameters for external types and omit zero-value defaults.

## When to Use

- Starting a new feature, service, or module.
- Resolving ambiguous or conflicting requirements.
- Bridging intent and implementation across a team.
- Refactoring without losing context.

Skip the canvas (and note the assumption) for trivial fixes, spikes, one-off scripts, or pure aesthetic work  --  see the Fitness table above.