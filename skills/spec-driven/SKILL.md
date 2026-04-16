---
name: spec-driven
description: Specification-Driven Development (SDD) workflow: specs as source of truth, executable specs, PRD-first development, implementation plans, task decomposition. Use when building features from requirements, creating specs, generating implementation plans, or following spec-driven methodology.
license: MIT
metadata:
  author: kilo-config
  version: 1.0.0
  source: github/spec-kit
---

# Specification-Driven Development (SDD)

Code serves specifications. Specifications are the source of truth.

## Core Principles

### Power Inversion

- Specifications don't serve code—code serves specifications
- PRD generates implementation, not guides it
- Maintaining software means evolving specifications
- Debugging means fixing specifications
- Refactoring means restructuring specs for clarity

### Executable Specifications

Specifications must be precise, complete, and unambiguous enough to generate working systems.

### Continuous Refinement

- Consistency validation happens continuously
- Analyze specs for ambiguity, contradictions, gaps
- Production metrics inform specification evolution

## Workflow

### Phase 1: Specify

Transform idea into comprehensive PRD through iterative dialogue:

1. Define user stories with acceptance criteria
2. Mark ambiguities: `[NEEDS CLARIFICATION: specific question]`
3. Don't guess—if prompt doesn't specify, mark it
4. Focus on WHAT users need and WHY, not HOW to implement
5. Include non-functional requirements

### Phase 2: Plan

Generate implementation plan from specification:

1. Read and understand feature requirements
2. Ensure alignment with project constitution and architectural principles
3. Convert business requirements into technical architecture
4. Document technology choices with rationale
5. Generate data models, API contracts, test scenarios
6. Produce quickstart validation guide

### Phase 3: Task

Analyze plan and generate executable task list:

1. Read `plan.md` and supporting documents
2. Convert contracts, entities, scenarios into specific tasks
3. Mark independent tasks `[P]` for parallel execution
4. Output `tasks.md` ready for execution

## Specification Template

### Feature Specification Structure

```
# Feature: [name]

## User Stories
- As a [role], I want [goal] so that [benefit]
  Acceptance: [measurable criteria]

## Requirements
### Functional
- [testable requirement]

### Non-Functional
- Performance: [measurable target]
- Security: [constraint]
- Scalability: [constraint]

## Out of Scope
- [explicitly excluded]

## Open Questions
- [NEEDS CLARIFICATION: specific question]
```

### Implementation Plan Structure

```
# Implementation Plan: [feature]

## Architecture
- [high-level design tracing to requirements]

## Technology Choices
- [choice]: [rationale linking to requirement]

## Data Model
- [entities and relationships]

## API Contracts
- [endpoints, inputs, outputs]

## Test Scenarios
- [acceptance scenarios mapping to user stories]

## Phases
1. [phase] - [deliverables]
2. [phase] - [deliverables]

## Complexity Tracking
- [any deviations from simplicity principles with justification]
```

## Quality Gates

### Pre-Implementation Gates

- [ ] No `[NEEDS CLARIFICATION]` markers remain
- [ ] Requirements are testable and unambiguous
- [ ] Success criteria are measurable
- [ ] No speculative or "might need" features
- [ ] All phases have clear prerequisites

### Constitutional Compliance

- [ ] Library-first: feature as standalone library
- [ ] Simplicity: ≤3 projects for initial implementation
- [ ] No future-proofing without documented justification
- [ ] Test-first: tests before implementation
- [ ] Integration-first: realistic environments over mocks

## Bidirectional Feedback

- Production incidents update specifications
- Performance bottlenecks become non-functional requirements
- Security vulnerabilities become constraints for future generations
- Change requirements → regenerate plans → iterate

## When to Use

- Building new features from requirements
- Creating implementation plans from specs
- Decomposing complex tasks into executable steps
- Maintaining alignment between intent and implementation
- Pivoting based on user feedback or market changes
