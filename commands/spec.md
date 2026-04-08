---
description: Transform a feature description into a gated spec → plan → tasks pipeline
agent: code
subtask: true
---

# Spec

Transform `$ARGUMENTS` into a complete, gated specification pipeline:
**Specify → Plan → Tasks**

Each phase produces artifacts and requires explicit sign-off before proceeding.

---

## Phase 1: Specify

**Goal:** Produce `specs/<feature-slug>/spec.md` with all six required sections.

1. Parse `$ARGUMENTS` into a slug: lowercase, hyphens, no spaces (e.g., `oauth2-google-login`)
2. Ask clarifying questions for any section that is ambiguous — use `[NEEDS CLARIFICATION: question]` as a placeholder while waiting
3. Fill out all six sections:

```markdown
# <Feature Name>

## Purpose
What this feature does and why it exists.

## Requirements
Numbered, testable acceptance criteria:
1. The system SHALL ...
2. The system SHALL ...

## Constraints
Performance, security, compatibility, and scope boundaries.

## Interfaces
Input/output contracts: API signatures, data shapes, CLI flags, event schemas.

## Error Cases
Expected failure modes and their required handling.

## Out of Scope
Explicitly list what is NOT included in this feature.
```

4. Run the Spec Quality Check:
   - Can each requirement be tested with pass/fail?
   - Are edge cases and error paths specified?
   - Is scope bounded (out-of-scope section present)?
   - No ambiguities a reviewer would question?

5. **STOP** — Present spec to user. Do not proceed to Phase 2 until user approves.

---

## Phase 2: Plan

**Goal:** Produce `specs/<feature-slug>/plan.md` and supporting artifacts mapping every requirement to a technical decision.

1. Read `specs/<feature-slug>/spec.md`
2. For each requirement, document:
   - The design decision that satisfies it
   - Rationale (why this approach over alternatives)
   - Trade-offs accepted
3. Apply Constitutional Compliance check before writing the plan:
   - **Article I** — Does the design start as a standalone library?
   - **Article VII** — Does it add minimal complexity?
   - **Article VIII** — Does it use framework features directly, one model per concept?
   - **Article IX** — Will tests use real dependencies?
   - Flag any violation as a blocker; redesign before proceeding.
4. Produce these artifacts alongside `plan.md`:
   - `data-model.md` — Schema definitions, entity relationships, type contracts
   - `contracts/` — API specs, event definitions, function signatures
   - `research.md` — Technical investigation findings, evaluated alternatives
   - `quickstart.md` — Key validation scenarios (smoke tests confirming the feature works end-to-end)
5. Flag any requirement that cannot be satisfied — surface as a blocker

```markdown
# Implementation Plan: <Feature Name>

## Architecture Overview
High-level component diagram or description.

## Requirement Mapping
| Req # | Decision | Rationale | Trade-offs |
|-------|----------|-----------|------------|
| 1     | ...      | ...       | ...        |

## Pre-Implementation Gates
- [ ] Simplicity: fewest moving parts that satisfy the spec?
- [ ] Anti-Abstraction: using framework features directly?
- [ ] Integration-First: tests hit real dependencies?

## Dependencies
New libraries or services, with justification.

## Open Questions
Items needing resolution before implementation begins.
```

6. **STOP** — Present plan to user. Do not proceed to Phase 3 until user approves.

---

## Phase 3: Tasks

**Goal:** Produce `specs/<feature-slug>/tasks.md` with an executable, parallelism-annotated task list.

1. Read `specs/<feature-slug>/plan.md`
2. Derive tasks from:
   - Data model definitions
   - API contracts
   - Module boundaries
   - Test requirements (one test task per requirement)
3. Annotate each task:
   - `[parallel]` — can run concurrently with other parallel tasks
   - `[sequential]` — depends on a prior task (list the dependency)
   - `[test]` — test task (must precede the implementation task it validates)

```markdown
# Tasks: <Feature Name>

## Wave 1 — Foundation (parallel)
- [ ] [parallel] Define data models and types
- [ ] [parallel] Write contract tests for all interfaces
- [ ] [parallel] Scaffold module structure

## Wave 2 — Implementation (sequential after Wave 1)
- [ ] [sequential: Wave 1] Implement core domain logic
- [ ] [sequential: Wave 1] Implement API handlers/controllers

## Wave 3 — Integration (sequential after Wave 2)
- [ ] [sequential: Wave 2] Wire dependencies and entry point
- [ ] [sequential: Wave 2] Integration tests end-to-end

## Wave 4 — Validation
- [ ] Run full test suite with coverage check (>80%)
- [ ] Security review: inputs, secrets, path access
- [ ] Performance baseline: measure against constraints
```

4. Every requirement from the spec must map to at least one task.
5. Output the final task file and summarize the wave structure.

---

## Stopping Rules

- **STOP after Specify** — wait for user approval before generating the plan
- **STOP after Plan** — wait for user approval before deriving tasks
- **STOP on blockers** — if a requirement cannot be satisfied, surface it immediately rather than designing around it
- **CONTINUE** — only after explicit user sign-off at each gate
