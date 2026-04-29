---
name: spec-driven
description: A workflow where specifications act as the absolute source of truth. Uses the REASONS Canvas to structure prompts as first-class, versioned, reviewable artifacts.
---
# Specification-Driven Development (SDD)

A workflow where specifications act as the absolute source of truth, and code is merely the generated output.

## 1. Specifications as the Source of Truth
- **Power Inversion**: Code serves the specification. The Product Requirements Document (PRD) is the source that generates the implementation plan, which in turn generates the code.
- **Executable Specs**: Specifications must be precise, complete, and unambiguous enough to drive development without needing developer guesswork.
- **Canonical Format**: The REASONS Canvas is the canonical format for structured prompts. It forces clarity across all seven dimensions before code generation.
- **Maintained Artifacts**: Prompts are version controlled, reviewed, and kept in sync with code.

## The REASONS Canvas

The canonical format for structured prompts in SPDD. It forces clarity across all seven dimensions before code generation.

| Letter | Dimension | Description |
|---|---|---|
| **R** | Requirements | What problem are we solving, and what is the Definition of Done? |
| **E** | Entities | Domain entities and their relationships |
| **A** | Approach | The strategy of how we'll meet the requirements |
| **S** | Structure | Where the change fits in the system; components and dependencies |
| **O** | Operations | Break the abstract strategy into concrete, testable implementation steps |
| **N** | Norms | Cross-cutting engineering norms (naming, observability, defensive coding, error handling, etc.) |
| **S** | Safeguards | Non-negotiable boundaries (invariants, performance limits, security rules, compliance requirements, etc.) |

The Canvas is split into three groups:
- **Abstract parts (R, E, A, S)**: intent & design
- **Specific parts (O)**: execution
- **Common standards (N, S)**: governance

For complex tasks, generate a Canvas in `plans/` before implementation begins.

## 2. Test-First Imperative
- **Strict TDD**: Write unit and integration tests before writing implementation code. Tests define the expected behavior as outlined in the spec.
- **Real-world testing**: Prioritize integration-first testing using realistic environments (real databases instead of mocks) when validating contracts.

## 3. Structured Automation & Templates
- **Clarify Uncertainty**: Never guess missing requirements. Explicitly mark ambiguities in specs with markers like `[NEEDS CLARIFICATION]`.
- **Constraint-driven**: Use checklists and phase gates to ensure architectural principles are met before moving to implementation.
- **Canvas Template**: Use the REASONS Canvas template for all complex feature prompts.
- **Safeguard Enforcement**: Safeguards (S) define non-negotiable boundaries that generated code must respect.

## 4. Modularity and Simplicity
- **Library-First Principle**: Every feature should be built as a modular, reusable library component with clear boundaries, rather than intertwined application logic.
- **CLI / Text-based Interfaces**: Build components so they can be interacted with and tested via clear, text-based APIs or CLIs.
- **Anti-Abstraction**: Use framework features directly. Do not over-engineer or add premature wrappers. Start simple and only add complexity when rigorously justified.

## 5. Continuous Refinement
- **Iterative Evolution**: If requirements pivot, update the specification first, then regenerate the implementation plan, and finally refactor the code.
- **Bidirectional Feedback**: Learnings from production, performance bottlenecks, and security reviews must flow back into updating the specification.
- **Bidirectional Sync**: When requirements pivot, update the Canvas first, then regenerate. When refactoring code, sync changes back to the Canvas so it stays an accurate design document.
- **Golden Rule**: When reality diverges, fix the prompt first — then update the code.