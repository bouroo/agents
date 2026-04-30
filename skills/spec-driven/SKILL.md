---
name: spec-driven
description: Structured Prompt-Driven Development (SPDD) workflows — REASONS Canvas for spec creation, prompt-code bidirectional sync, alignment before implementation, and iterative review. Use for planning features, writing specs, or any task where specifications drive code generation.
---

# Structured Prompt-Driven Development (SPDD)

Specifications and structured prompts are first-class delivery artifacts — version controlled, reviewed, reusable, and kept synchronized with code. Code is merely the generated output of a well-defined specification.

## Core Principle

When reality diverges from the spec, fix the spec first — then update the code. Never let spec and code silently diverge.

## The REASONS Canvas

A seven-part structure for generating comprehensive specifications. Organize specs along these dimensions:

### Abstract Parts (Intent & Design)

- **R — Requirements**: What problem are we solving? What is the definition of done?
- **E — Entities**: Domain objects, their attributes, and relationships.
- **A — Approach**: The strategy for meeting requirements. Design decisions and rationale.
- **S — Structure**: Where the change fits in the system. Components and dependencies.

### Specific Part (Execution)

- **O — Operations**: Concrete, ordered, testable implementation steps. Precise down to method signatures and parameter types.

### Governance Parts

- **N — Norms**: Cross-cutting engineering standards (naming, error handling, observability, patterns).
- **S — Safeguards**: Non-negotiable boundaries (invariants, performance limits, security rules, backward compatibility constraints).

## Three Core Skills

### 1. Abstraction First
Design before you generate. Before writing any code:
- Clarify what objects exist and their lifecycle
- Define how objects collaborate (interfaces, data flow, contracts)
- Establish boundaries between modules and responsibilities
- Without this, AI sprints on implementation while structure falls apart

### 2. Alignment
Lock intent before writing code:
- Make "what we will do" and "what we won't do" explicit
- Agree on standards and hard constraints up front
- Define acceptance criteria in concrete, testable terms (Given/When/Then)
- Fast output with wrong intent produces slow rework

### 3. Iterative Review
Turn output into a controlled loop:
- Review intent alignment before reviewing code details
- Categorize changes: logic corrections (behavior changes) vs. refactoring (clean code)
- Logic corrections: update spec first, then regenerate code
- Refactoring: update code first, then sync back to spec
- Repeat until both spec and code are aligned

## Workflow Phases

1. **Story**: Break requirements into independent, deliverable user stories (INVEST principle)
2. **Analysis**: Extract domain keywords, scan codebase, identify risks and gaps
3. **Canvas**: Generate the REASONS Canvas — the executable blueprint
4. **Generate**: Produce code task-by-task, strictly following Operations, Norms, Safeguards
5. **Test**: Generate tests from acceptance criteria. Verify coverage against spec
6. **Review**: Check alignment between spec and code. Categorize adjustments. Sync both directions as needed

## Spec-Code Sync Rules

| Change Type | Direction | Strategy |
|---|---|---|
| New feature | Spec → Code | Write spec first, generate code from it |
| Logic correction | Spec → Code | Fix spec first, then regenerate affected code |
| Bug fix (behavior change) | Spec → Code | Update spec with correct behavior, then fix code |
| Refactoring (no behavior change) | Code → Spec | Refactor code, then sync changes back to spec |
| Performance optimization | Code → Spec | Optimize code, update spec with new constraints |

## Fitness Assessment

SPDD pays off most for:
- ★★★★★ Scaled, standardized delivery with high-repeat business logic
- ★★★★★ High compliance environments with hard constraints
- ★★★★☆ Team collaboration requiring auditability
- ★★★★☆ Cross-cutting consistency work across services

SPDD overhead may not be worth it for:
- ★★☆☆☆ Firefighting hotfixes where speed matters most
- ★★☆☆☆ Exploratory spikes validating ideas quickly
- ★★☆☆☆ One-off scripts with low reuse potential