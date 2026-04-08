---
name: spec-driven-dev
description: Specification-Driven Development (SDD) workflow — transform requirements into executable specifications that generate code. Use when planning features, writing PRDs, creating implementation plans, or when the user mentions specifications, requirements, or spec-driven development.
---

# Specification-Driven Development

**Core Principle:** Specifications are the primary artifact; code is their expression. Code serves specifications, not the reverse.

## Workflow

1. **Write the spec** — Express intent in natural language before writing any code
2. **Clarify ambiguities** — Mark unknowns with `[NEEDS CLARIFICATION: question]` — never guess
3. **Derive tests from spec** — Each requirement maps to at least one test case
4. **Implement to satisfy spec** — Code is last-mile implementation of spec intent
5. **Verify against spec** — Every technical decision links back to a specific requirement

## Spec Structure

Every specification document must include these sections:

- **Purpose** — What this feature does and why it exists
- **Requirements** — Numbered, testable acceptance criteria
- **Constraints** — Performance, security, compatibility boundaries
- **Interfaces** — Input/output contracts (API signatures, data shapes)
- **Error cases** — Expected failure modes and handling
- **Out of scope** — Explicitly state what is NOT included

## Spec Quality Checks

Before proceeding to implementation, validate:

- Can each requirement be tested with a pass/fail result?
- Are edge cases and error paths specified?
- Are there ambiguities a reviewer would question?
- Is the scope bounded (includes "out of scope" section)?

If any check fails, revise the spec before writing code.

## Test Derivation

- Every requirement produces at least one test case
- Happy paths, edge cases, and error paths all get tests
- Test names should reference the requirement they validate
- If a requirement lacks a clear test, the requirement is too vague

## Anti-patterns

- **No speculative features** — build only what's specified
- **No gold-plating** — resist adding features beyond the spec
- **No implementation details in specs** — specs describe WHAT, not HOW
- **No orphan code** — every line traces back to a requirement

## Living Specs

- Update specs when requirements change, then update code
- Specs are the source of truth during code review
- If spec and code disagree: spec wins (update code) unless spec is wrong (fix spec first, then code)
- Never modify code to diverge from spec without updating the spec

## Three-Phase Workflow

For non-trivial features, run these phases explicitly:

1. **Specify** — Convert feature description to full spec. Produce `specs/<branch>/spec.md`.
2. **Plan** — Map spec requirements to technical decisions. Document rationale. Produce `specs/<branch>/plan.md` + supporting artifacts.
3. **Tasks** — Derive executable task list from plan. Mark independent tasks `[parallel]`. Produce `specs/<branch>/tasks.md`.

Each phase is a gate: don't start Plan until Specify is complete; don't start Tasks until Plan is validated.

## Spec Artifact Structure

Every non-trivial spec populates this directory under `specs/<feature-slug>/`:

| File | Purpose |
|------|---------|
| `spec.md` | Requirements, constraints, interfaces, error cases, out-of-scope |
| `plan.md` | Architecture overview, requirement-to-decision mapping, trade-offs |
| `data-model.md` | Schema definitions, entity relationships, type contracts |
| `contracts/` | API specs, event definitions, function interfaces |
| `research.md` | Technical investigation findings, library evaluations |
| `tasks.md` | Executable task list with parallelism annotations (`[parallel]`/`[sequential]`) |
| `quickstart.md` | Key validation scenarios confirming the feature works end-to-end |

## Constitutional Foundation

These articles are non-negotiable gates before any implementation begins:

| Article | Rule |
|---------|------|
| **I** | Every feature begins as a standalone library with a clean interface |
| **II** | Libraries expose functionality through CLI/API interfaces producing structured output |
| **III** | Test-First: tests written and approved before any implementation code |
| **VII** | Simplicity: max 3 active projects; added complexity requires documented justification |
| **VIII** | Anti-Abstraction: use framework features directly; one model representation per concept |
| **IX** | Integration-First Testing: real databases and actual services; no mocks at system boundaries |

## Pre-Implementation Gates

Before writing implementation code, verify all three pass:

- **Simplicity gate** — Does this solution use the fewest moving parts that satisfy the spec?
- **Anti-Abstraction gate** — Are we using framework features directly rather than wrapping them?
- **Integration-First gate** — Do tests hit real dependencies rather than mocked stand-ins?

If any gate fails, redesign before proceeding.

## Operational Feedback Loop

Specs are not frozen after deployment:
- Production metrics (latency, error rates, user behavior) → new non-functional requirements
- Performance bottlenecks → constraints section updates
- Support incidents → error cases section additions
- Multiple implementation branches can explore different optimization targets from the same spec

Update the spec first; then update the code to match.

## Decision Rule

When in doubt, ask: *"Which requirement does this serve?"* If there's no answer, don't build it.
