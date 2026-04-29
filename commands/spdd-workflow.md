---
description: Structured-Prompt-Driven Development workflow — analyze requirements, generate REASONS Canvas, implement, verify, and sync
---

# SPDD Workflow

Execute the full Structured-Prompt-Driven Development workflow for $ARGUMENTS (requirements description or path to requirements file).

> **Conductor note**: You do NOT execute steps directly. Decompose this command into the subtasks below, delegate each to the correct subagent, and validate every deliverable before proceeding.

## Constraints

- The Canvas is the single source of truth. Do not generate code that deviates from it.
- Logic corrections (behavior changes) require updating the Canvas first, then regenerating code.
- Refactoring (no behavior change) is done on code first, then synced back to the Canvas.
- The workflow is complete only when the Canvas and code are synchronized.

## Phase 1 — Requirements & Story

### 1.1 Clarify requirements
- **Agent**: `planner` or `conductor`
- **Task**:
  - If $ARGUMENTS is a file path, read it.
  - Decompose the input into a clear problem statement and goals.
  - Ensure acceptance criteria use Given/When/Then format with concrete examples.
  - Identify stakeholders and business value.
- **Deliverable**: Consolidated user story document containing:
  - **Background**: Context and motivation
  - **Business Value**: Why this matters
  - **Scope In**: What is included
  - **Scope Out**: What is explicitly excluded
  - **Acceptance Criteria**: Given/When/Then scenarios with concrete examples

## Phase 2 — Analysis

Delegate the following in parallel where possible:

### 2.1 Extract domain keywords
- **Agent**: `planner`
- **Task**: Identify domain-specific terms, actors, actions, and boundaries from the requirements.
- **Deliverable**: Domain keyword glossary.

### 2.2 Scan codebase
- **Agent**: `explorer`
- **Task**: Scan relevant parts of the codebase (not all of it). Identify existing concepts, analogous implementations, and extension points.
- **Deliverable**: Relevant file paths and concept mappings.

### 2.3 Identify risks and gaps
- **Agent**: `planner`
- **Task**: Synthesize findings from 2.1 and 2.2. Identify new concepts, business rules, technical risks, and dependencies.
- **Deliverable**: Analysis context document in `plans/` covering:
  - Domain concepts (existing vs new)
  - Strategic direction (where this feature fits)
  - Risks & gaps (uncertainty, dependencies, technical debt)

## Phase 3 — Generate REASONS Canvas

### 3.1 Draft structured prompt
- **Agent**: `planner`
- **Task**: Generate the full structured prompt following the REASONS Canvas:
  - **R** — Requirements: Problem definition, Definition of Done, acceptance criteria
  - **E** — Entities: Domain model, existing vs new entities, relationships
  - **A** — Approach: Design strategy, patterns, trade-offs, rationale
  - **S** — Structure: System components, files affected, dependencies
  - **O** — Operations: Concrete implementation steps, method signatures, execution order
  - **N** — Norms: Engineering standards, naming conventions, error handling, observability
  - **S** — Safeguards: Invariants, performance limits, security rules, scope exclusions
- **Deliverable**: Structured prompt file in `plans/` (e.g., `plans/<id>-[Feat]-<feature-name>.md`)

### 3.2 Review Canvas
- **Agent**: `conductor` (you)
- **Task**: Review the Canvas for intent alignment against the consolidated user story (Phase 1). Check:
  - Acceptance criteria are represented in Requirements (R)
  - Domain model is complete in Entities (E)
  - Approach is feasible and trade-offs are documented (A)
  - Operations are concrete and ordered (O)
  - Norms and Safeguards are actionable (N, S)
- **Deliverable**: Review notes or approval.
- **Gate**: Do NOT proceed to Phase 4 until the Canvas is reviewed and aligned. Do not generate code from a misaligned Canvas.

## Phase 4 — Generate Code

### 4.1 Implement from Canvas
- **Agent**: `implementer`
- **Task**:
  - Read the approved Canvas.
  - Generate code task by task following Operations (O).
  - Strictly adhere to Norms (N) and Safeguards (S).
  - No improvisation beyond the spec.
  - Validate each deliverable independently before moving to the next operation.
- **Deliverable**: Implemented code with verification passing.

## Phase 5 — Verify

Delegate the following in parallel where possible:

### 5.1 Run tests
- **Agent**: `tester`
- **Task**: Run unit tests and integration tests. Generate API test scripts if applicable.
- **Deliverable**: Test results. Must be green.
- **Gate**: If tests fail, return to `implementer` to fix. Do NOT proceed until green.

### 5.2 Validate against acceptance criteria
- **Agent**: `tester`
- **Task**: Cross-check test coverage against the acceptance criteria in the Canvas (R). Ensure every Given/When/Then scenario is exercised.
- **Deliverable**: Acceptance criteria coverage report.

## Phase 6 — Review & Iterate

### 6.1 Review code against Canvas
- **Agent**: `reviewer`
- **Task**: Review the implemented code against the Canvas. Categorize every finding:
  - **Logic corrections** (behavior changes): Code deviates from Canvas intent → Update Canvas first, then regenerate code.
  - **Refactoring** (no behavior change): Code quality or structure improvement → Refactor code, then sync Canvas.
- **Deliverable**: Review report with categorized findings.

### 6.2 Apply corrections or refactoring
- **Agent**: `implementer` or `planner` (depending on finding category)
- **Task**: Process findings from 6.1:
  - For logic corrections: `planner` updates Canvas, then `implementer` regenerates affected code.
  - For refactoring: `implementer` refactors code, then `planner` updates Canvas to match.
- **Deliverable**: Updated code and/or Canvas.
- **Gate**: Re-run Phase 5 (Verify) after any changes. Iterate until review report is empty.

## Phase 7 — Sync

### 7.1 Final Canvas sync
- **Agent**: `planner`
- **Task**: Ensure the Canvas accurately reflects the final code state. Update any sections that drifted during implementation or refactoring:
  - Update Entities (E) if the domain model evolved.
  - Update Structure (S) if files changed from the original plan.
  - Update Operations (O) if the execution order or signatures changed.
  - Update Safeguards (S) if new invariants or limits emerged.
- **Deliverable**: Synchronized Canvas.

### 7.2 Archive deliverables
- **Agent**: `conductor` (you)
- **Task**: Ensure all deliverables are in their expected locations:
  - Consolidated user story (Phase 1)
  - Analysis context document (Phase 2)
  - REASONS Canvas (Phase 3, 7)
  - Review report (Phase 6)
- **Deliverable**: Confirmation of artifact locations.

## Completion Criteria

The SPDD workflow is complete ONLY when:
1. Requirements are clarified and documented (Phase 1).
2. Analysis context is produced (Phase 2).
3. REASONS Canvas is generated and reviewed for intent alignment (Phase 3).
4. Code is generated from the Canvas, not ad hoc (Phase 4).
5. Tests pass against acceptance criteria (Phase 5).
6. Review findings are resolved and categorized correctly (Phase 6).
7. Canvas and code are synchronized (Phase 7).

(End of file - total 127 lines)
