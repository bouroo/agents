---
name: spec-driven
description: A workflow where specifications act as the absolute source of truth, and code is merely the generated output.
---
# Specification-Driven Development (SDD)

A workflow where specifications act as the absolute source of truth, and code is merely the generated output.

## 1. Specifications as the Source of Truth
- **Power Inversion**: Code serves the specification. The Product Requirements Document (PRD) is the source that generates the implementation plan, which in turn generates the code.
- **Executable Specs**: Specifications must be precise, complete, and unambiguous enough to drive development without needing developer guesswork.

## 2. Test-First Imperative
- **Strict TDD**: Write unit and integration tests before writing implementation code. Tests define the expected behavior as outlined in the spec.
- **Real-world testing**: Prioritize integration-first testing using realistic environments (real databases instead of mocks) when validating contracts.

## 3. Structured Automation & Templates
- **Clarify Uncertainty**: Never guess missing requirements. Explicitly mark ambiguities in specs with markers like `[NEEDS CLARIFICATION]`.
- **Constraint-driven**: Use checklists and phase gates to ensure architectural principles are met before moving to implementation.

## 4. Modularity and Simplicity
- **Library-First Principle**: Every feature should be built as a modular, reusable library component with clear boundaries, rather than intertwined application logic.
- **CLI / Text-based Interfaces**: Build components so they can be interacted with and tested via clear, text-based APIs or CLIs.
- **Anti-Abstraction**: Use framework features directly. Do not over-engineer or add premature wrappers. Start simple and only add complexity when rigorously justified.

## 5. Continuous Refinement
- **Iterative Evolution**: If requirements pivot, update the specification first, then regenerate the implementation plan, and finally refactor the code.
- **Bidirectional Feedback**: Learnings from production, performance bottlenecks, and security reviews must flow back into updating the specification.