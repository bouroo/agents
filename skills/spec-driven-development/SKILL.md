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
| **R — Requirements** | Problem, Definition of Done, acceptance criteria |
| **E — Entities** | Domain objects, relationships, boundaries |
| **A — Approach** | Chosen strategy, alternatives rejected, why |
| **S — Structure** | Component placement, dependencies, interfaces |
| **O — Operations** | Concrete, testable implementation steps in order |
| **N — Norms** | Cross-cutting rules: naming, error handling, documentation, clarity |
| **S — Safeguards** | Non-negotiable boundaries: invariants, perf limits, security |

### Template

Use for every non-trivial task. Fill every section. Mark unknowns with `[NEEDS CLARIFICATION]`.

```markdown
## R — Requirements
- Problem statement
- Definition of Done (measurable)
- Acceptance criteria (testable)

## E — Entities
- Domain objects and relationships
- Existing vs. new boundaries
- Data flow between entities

## A — Approach
- Chosen strategy and rationale
- Alternatives considered and rejected
- Key trade-offs

## S — Structure
- Where the change fits in the codebase
- Components, dependencies, interfaces
- Files to create or modify

## O — Operations
- Ordered, testable implementation steps
- Each step precise enough for a subagent to execute without ambiguity
- Test scenarios: happy path, error path, edge cases
- At least one step exercises an end-to-end boundary

## N — Norms
- Naming: scope-proportional, no context/type repetition
- Error handling: explicit returns, guard-clause-first, wrap-with-context
- Documentation: name-first sentences for public symbols
- Style: eliminate nesting, omit zero-value noise
- Reference AGENTS.md "Code Craft Norms" for the full norm set

## S — Safeguards
- Invariants that must hold
- Performance ceilings (latency, memory, size limits with numbers)
- Security rules (no secrets in logs, least privilege)
- Non-negotiable constraints
```

## Core Skills

1. **Abstraction-first** — Design objects, collaborations, and boundaries *before* generating code. Intent precedes implementation.
2. **Alignment** — Lock scope explicitly: what we will do, what we won't, what remains open. Visible in the spec.
3. **Iterative review** — Treat output as a controlled loop (spec → generate → verify → refine), not a one-shot draft.

## Prompt Discipline (think → do)

Structure every generation as a controlled loop, not a one-shot:

1. **Analyze** — read the relevant code/state; restate the problem and change boundary before writing anything.
2. **Plan** — fill the REASONS canvas; name the ordered, testable steps; mark unknowns explicitly.
3. **Execute** — implement one step at a time against the canvas, not intuition.
4. **Review** — verify each step with an executable check before proceeding.

Be specific: name files, symbols, and acceptance criteria; give examples and specify output format. Vague prompts produce vague specs; vague specs produce wrong code. When ambiguous, resolve against best practice and record the assumption — don't silently guess.

**Source:** Kilo — Prompt Engineering (https://kilo.ai/docs/customize/prompt-engineering).

## Workflow

```
Story → Analysis → Canvas → Generate → Test → Review → Sync
  ↑                                                      |
  └────────────── repeat until aligned ──────────────────┘
```

1. **Story** — Capture the user problem; surface the problem, not the solution.
2. **Analysis** — Identify entities, constraints, risks, unknowns.
3. **Canvas** — Fill every REASONS section; mark unknowns explicitly.
4. **Generate** — Write code from the spec, not intuition.
5. **Test** — Verify code satisfies every section of the spec.
6. **Review** — Check for orphans (code without spec) and gaps (spec without code).
7. **Sync** — Update spec and code together; never land one without the other.

### Why the workflow is phased — cognitive load, not ceremony

Intent confirmation is *distributed* across steps, not compressed into one review. A single large review overwhelms the reviewer — they skim, defer, or approve by default — and intent drifts even when everything looks correct on paper. Each checkpoint stays small: Step 2 pins the *problem*, Step 3 the *why/what*, Step 4 the *design/operations*, Step 5 the *behavior*, Step 6 the *code*. By code review, requirements and design are already signed off, so attention goes to what matters.

### Test sequencing — a deliberate inversion of TDD

Classic TDD uses tests to shape design through fast feedback. SPDD distributes the same outcomes differently:

- **API / end-to-end tests come early** — validate behavior at the system boundary so you only review code that actually works. Generated code is cheap; little value reviewing implementation that doesn't satisfy intended behavior.
- **Code review then focuses on what only humans can judge** — logic, architecture, trade-offs, non-functional concerns.
- **Unit tests come last as a regression net** — once intent is explicit in the canvas and the implementation has stabilized, generate unit tests to lock behavior in. Generating them earlier means rewriting after review-driven changes.

Grade the tests themselves (mutation testing) — see [harness-engineering](../harness-engineering/SKILL.md) §12.

## Fitness — when to spec, and when not to

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

- [ ] Every REASONS section filled — no empty sections.
- [ ] Requirements have measurable acceptance criteria and a Definition of Done.
- [ ] Safeguards specify numeric limits (latency, size, error rates, quotas).
- [ ] Norms cover naming, logging, error handling.
- [ ] Norms specify scope-proportional naming and guard-clause control flow.
- [ ] No in-band error signaling — errors explicit, not sentinel values.
- [ ] Public symbols have name-first doc comments (full sentences).
- [ ] Unknowns marked `[NEEDS CLARIFICATION]`, not glossed over.
- [ ] Operations ordered and testable — a subagent can execute sequentially.
- [ ] No orphaned features (in code but not in spec).
- [ ] No orphan requirements (in spec but not in code).

## Key Rules

- **Sync, not handoff** — spec and code evolve together; a stale spec is a bug.
- **No speculative features** — if it's not in the spec, don't build it.
- **Immutable principles** — never violate Norms or Safeguards for convenience.
- **Bidirectional feedback** — production reality informs spec evolution.
- **Logic change** → update spec first, then regenerate code; **Refactor (no behavior change)** → change code first, then sync spec. Never land one side without the other.

## Constitutional Gates (Spec-kit)

- **Simplicity** — prefer ≤3 projects at the initial implementation stage.
- **Anti-abstraction** — use the language's natural types; don't introduce a layer that adds no value.
- **Test-first** — write tests before implementation; tests encode the spec.
- **Integration-first** — prefer end-to-end tests that exercise real boundaries.
- **Library-first** — structure as reusable libraries with a thin CLI shim on top.
- **CLI interface** — every feature reachable from the command line.
- **Guard clauses** — handle errors and edge cases first; keep the happy path unindented.
- **No in-band errors** — return explicit error values, never overload return values to signal failure.
- **Eliminate repetition** — names must not repeat package, type, or surrounding context.
- **Named construction** — use explicit field/parameter names when constructing external types; omit zero-value defaults.

## Norms Reference

Language-agnostic norms derived from production style guides. Specify these in the **N — Norms** section of every spec.

### Naming

- **Scope-proportional** — name length proportional to scope, inversely proportional to usage. Single-letter names for tiny scopes (`i`, `err`); descriptive names at package level.
- **No repetition** — names must not repeat enclosing context. `db.Load`, not `db.LoadFromDatabase`. `count`, not `userCount` inside `UserCount`.
- **No type-in-name** — omit type info from variable names. `users`, not `usersSlice`; `limit`, not `limitInt`.

### Error Handling

- **Explicit returns** — functions that can fail return a separate error value, not in-band sentinels (-1, null, "").
- **Guard-clause flow** — handle errors and edge cases at the top; keep the happy path unindented. Avoid else-after-return.
- **Wrap, don't flatten** — add context when propagating; preserve the cause chain. Never inspect error strings to branch.

### Documentation

- **Name-first sentences** — doc comments for public symbols begin with the symbol's name as a full sentence: `// Encode writes the JSON encoding of req to w.`
- **Show usage** — provide runnable examples for non-trivial APIs; examples live in test files.

### Code Clarity

- **Eliminate nesting** — prefer early returns and guard clauses over deeply nested conditionals.
- **Omit zero-value noise** — only specify non-default values in construction. Default is zero/nil/false unless stated.
- **Named fields for external types** — always use explicit field names when constructing types from other packages.

## When to Use

- Starting a new feature, service, or module.
- Resolving ambiguous or conflicting requirements.
- Bridging intent and implementation across a team.
- Refactoring without losing context.

Skip the canvas (and note the assumption) for trivial fixes, spikes, one-off scripts, or pure aesthetic work — see the Fitness table above.