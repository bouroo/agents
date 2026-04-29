---
name: abstraction-first
description: Design before you generate. Clarify what objects exist, how they collaborate, and where boundaries are before implementation.
---
# Abstraction-First

Design before you generate. Clarify what objects exist, how they collaborate, and where boundaries are before implementation.

## 1. Purpose

Without clear abstractions, AI sprints on implementation details while structure falls apart. Invest in design up front so generated code aligns with the intended architecture.

## 2. Principles

- **Define domain entities first**: Identify the core objects, their attributes, and relationships before writing any code.
- **Clarify collaboration**: Map who calls whom, how data flows between components, and where state lives.
- **Establish boundaries**: Draw module boundaries and expose minimal, stable interfaces.
- **Choose patterns deliberately**: Apply design patterns (Strategy, Factory, Adapter, etc.) only when they reduce complexity, not for ceremony.

## 3. Practices

- **Start with Entities and Structure**: Begin with the Entities (E) and Structure (S) sections of the REASONS Canvas.
- **Sketch interfaces early**: Write method signatures and type contracts before implementations.
- **Validate against Requirements**: Check that the proposed abstractions solve the stated problem by mapping back to Requirements (R).
- **Review coupling and cohesion**: Ensure modules are highly cohesive and loosely coupled before generating code.

## 4. Anti-patterns

- **Jumping to implementation**: Writing code before defining what it is supposed to model.
- **Unclear responsibilities**: Multiple modules doing similar work, leading to duplicated logic and drift.
- **Inconsistent interfaces**: Each module inventing its own calling conventions, making the system hard to compose.
