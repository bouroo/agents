---
name: abstraction-first
description: Design before you generate. Clarify what objects exist, how they collaborate, and where boundaries are before implementation.
version: 1.0.0
triggers:
  - designing before implementing
  - creating new modules or packages
  - architectural decisions
  - greenfield features
---

# Abstraction First

Design the structure before generating code. Clarify objects, collaborations, and boundaries first.

## When to Use

- Starting a new feature or module
- Before generating any significant code
- When responsibilities are unclear
- During architectural decisions

## Steps

1. **Identify Objects**: List the core domain objects and their responsibilities.
2. **Define Collaborations**: Map how objects interact — messages, data flow, dependencies.
3. **Draw Boundaries**: Establish clear interfaces between components. What's internal vs. public.
4. **Name Components**: Give every object a precise, intention-revealing name.
5. **Validate**: Walk through the design with a concrete scenario before writing code.

## Rules

- No implementation code until the design is reviewed and approved.
- Every object must have a single, clear responsibility.
- Dependencies point inward (domain has no external deps).
- If you can't name it clearly, the abstraction is wrong.

## Checklist

- [ ] Core objects identified and named
- [ ] Responsibilities assigned (one per object)
- [ ] Interfaces defined between components
- [ ] Data flow documented
- [ ] Edge cases considered in design
- [ ] Design reviewed before code generation
