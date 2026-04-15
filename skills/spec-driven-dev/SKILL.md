---
name: spec-driven-dev
description: Use when building new features, APIs, or systems. Transforms vague ideas into executable specifications before any code is written.
---

# Spec-Driven Development

## Core Principle
**Specs are truth — code serves specifications, not the reverse.**

## Workflow

1. **Specify** — Dialogue to transform requirements into PRDs with user stories and acceptance criteria
2. **Plan** — Generate implementation plan mapping requirements to technical decisions with documented rationale
3. **Tasks** — Convert plans to executable task lists with parallelization markers

## Marking Ambiguity
Always mark gaps with `[NEEDS CLARIFICATION: question]`. Never speculate.

## Constitutional Constraints
- **Library-First**: Every feature begins as a standalone, reusable library
- **CLI Interface**: All libraries expose text-based interfaces
- **Test-First**: No implementation before tests fail correctly
- **Simplicity**: Maximum 3 projects per feature; use framework features directly
- **Integration-First**: Prefer real databases/services over mocks when safe

## Templates
Use templates to constrain output with:
- Explicit uncertainty markers
- Pre-implementation gates
- Structured checklists for completeness
- Test-first file creation ordering
- Prohibition on speculative features
