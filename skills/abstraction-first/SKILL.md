---
name: abstraction-first
description: Design before you generate. Clarify what objects exist, how they collaborate, and where boundaries are before implementation.
---

# Abstraction-First

Design before you generate. Clarify what objects exist, how they collaborate, and where boundaries are before implementation.

## Principles

- **Define domain entities first**: Core objects, attributes, relationships before any code.
- **Clarify collaboration**: Who calls whom, data flow, where state lives.
- **Establish boundaries**: Module boundaries with minimal, stable interfaces.
- **Choose patterns deliberately**: Apply design patterns only when they reduce complexity.

## Practices

- Start with Entities (E) and Structure (S) of the REASONS Canvas.
- Sketch interfaces early: method signatures and type contracts before implementations.
- Validate against Requirements (R): map abstractions back to stated problem.
- Review coupling and cohesion: highly cohesive, loosely coupled modules.

## Anti-patterns

- Jumping to implementation before defining what it models.
- Unclear responsibilities causing duplicated logic and drift.
- Inconsistent interfaces making the system hard to compose.
