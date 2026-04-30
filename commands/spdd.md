---
description: Structured Prompt-Driven Development — guide a feature from requirements through specification, code generation, testing, and review using the SPDD workflow
---

# SPDD Workflow

Execute the Structured Prompt-Driven Development workflow for $ARGUMENTS (a feature description, requirements document, or user story).

> **Conductor note**: You do NOT execute steps directly. Decompose this command into the subtasks below, delegate each to the correct subagent, and validate every deliverable before proceeding.

## Constraints

- Specifications are first-class artifacts. They must be created, reviewed, and maintained alongside code.
- Code is generated from specifications — never the reverse for new features.
- When reality diverges from spec, fix the spec first for logic changes, then regenerate code.
- Every acceptance criterion must have at least one corresponding test.

## Phase 1 — Requirements & Analysis

Delegate the following in parallel where possible:

### 1.1 Create or refine user story
- **Delegate to**: planning-capable subagent
- **Task**: If $ARGUMENTS is a raw idea or enhancement description, break it into structured user stories following INVEST principles. If it's already a user story, validate and refine it.
- **Deliverable**: Structured user story with Background, Business Value, Scope In, Scope Out, and Acceptance Criteria in Given/When/Then format.

### 1.2 Domain analysis
- **Delegate to**: exploration-capable subagent
- **Task**: Extract domain keywords from the requirements. Scan the codebase for related concepts, existing patterns, and potential conflicts. Identify:
  - Existing domain entities that the feature touches
  - New entities or relationships introduced
  - Technical risks and edge cases
- **Deliverable**: Analysis context document with domain concepts, risks, and design direction.

### 1.3 Review analysis
- **Owner**: conductor (you)
- **Task**: Review the analysis against your understanding of the requirements. Identify:
  - Gaps between business intent and AI interpretation
  - Edge cases the analysis surfaced that weren't anticipated
  - Design decisions that need stakeholder input
- **Gate**: Do NOT proceed until analysis aligns with intent. Ask the user for clarification if ambiguity remains.

## Phase 2 — Specification (REASONS Canvas)

### 2.1 Generate REASONS Canvas
- **Delegate to**: planning-capable subagent
- **Task**: Create a comprehensive specification using the REASONS Canvas structure. Write to a plan file (e.g., `plans/spdd-<feature-name>.md`):
  - **R**equirements: Problem statement, definition of done
  - **E**ntities: Domain objects, attributes, relationships
  - **A**pproach: Strategy, design decisions, trade-offs
  - **S**tructure: Where changes fit in the system, components, dependencies
  - **O**perations: Ordered, testable implementation steps with method-level detail
  - **N**orms: Naming, error handling, observability, patterns to follow
  - **S**afeguards: Non-negotiable constraints, invariants, limits
- **Deliverable**: REASONS Canvas plan file.

### 2.2 Review and refine Canvas
- **Owner**: conductor (you)
- **Task**: Review the Canvas for:
  - Completeness of each REASONS dimension
  - Consistency between Requirements and Operations
  - Coverage of all acceptance criteria in Operations
  - Reasonableness of Safeguards
- **Gate**: Do NOT proceed to code generation until the Canvas passes review. Iterate with the planning subagent if gaps exist.

## Phase 3 — Code Generation

### 3.1 Generate code task by task
- **Delegate to**: implementation-capable subagent
- **Scope**: Files identified in the Canvas Structure section
- **Task**: Read the REASONS Canvas plan file. Generate code following the Operations section step by step. Strictly adhere to Norms and Safeguards. Do not improvise features beyond the spec.
- **Deliverable**: Generated code files matching the Canvas Operations.

### 3.2 Generate tests from acceptance criteria
- **Delegate to**: testing-capable subagent
- **Task**: Read the Canvas Requirements and Operations. Generate tests that:
  - Cover every acceptance criterion from the user story
  - Cover normal, boundary, and error scenarios
  - Follow project test conventions
- **Deliverable**: Test files with mapped acceptance criteria coverage.

### 3.3 Run tests
- **Delegate to**: testing-capable subagent
- **Task**: Run all tests (existing + new). Record results.
- **Deliverable**: Test results. Must be green.
- **Gate**: If tests fail, classify: logic error → fix Canvas first (3.1). Test error → fix test. Do NOT proceed until green.

## Phase 4 — Review & Sync

Delegate the following in parallel:

### 4.1 Code review
- **Delegate to**: review-capable subagent
- **Task**: Review generated code against the REASONS Canvas. Check:
  - Intent alignment: does code match spec?
  - Scope compliance: no features beyond spec?
  - Norms compliance: naming, error handling, patterns followed?
  - Safeguards respected: no constraint violations?
- **Deliverable**: Review report with findings categorized by severity.

### 4.2 Classify and address findings
- **Owner**: conductor (you)
- **Task**: For each finding, classify as:
  - **Logic correction** (changes observable behavior): Update Canvas first → regenerate code (return to Phase 3)
  - **Refactoring** (no behavior change): Fix code directly → sync Canvas later
  - **Test gap**: Add tests (return to Phase 3.2)
- **Gate**: Do NOT proceed until all P0 findings are resolved.

### 4.3 Sync specifications
- **Delegate to**: implementation-capable subagent
- **Task**: Update the REASONS Canvas plan file to reflect:
  - Any refactoring performed during review
  - Any structural changes made to the codebase
  - Final state of all generated files
- **Deliverable**: Updated Canvas file synchronized with final code state.

## Phase 5 — Final Validation

### 5.1 Regression test
- **Delegate to**: testing-capable subagent
- **Task**: Run the full test suite. Verify no regressions.
- **Deliverable**: Test results. Must be green.

### 5.2 Final alignment check
- **Delegate to**: review-capable subagent
- **Task**: Quick verification that the final Canvas matches the final code state.
- **Deliverable**: Confirmation or list of remaining mismatches.

## Completion Criteria

SPDD workflow is complete ONLY when:
1. User story has structured acceptance criteria (1.1).
2. Domain analysis is aligned with intent (1.3).
3. REASONS Canvas exists and is reviewed (2.2).
4. Code is generated from the Canvas (3.1).
5. All tests pass, covering every acceptance criterion (3.3).
6. Code review shows no P0 issues (4.2).
7. Canvas is synchronized with final code state (4.3).
8. Full test suite passes with no regressions (5.1).
9. Canvas and code are aligned (5.2).

## Deliverables

At completion, the following artifacts should exist:
- `plans/spdd-<feature-name>.md` — The REASONS Canvas (version controlled)
- Generated source files — Matching Canvas Operations
- Test files — Covering all acceptance criteria
- Review report — Documenting findings and resolutions
