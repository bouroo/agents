---
name: alignment
description: Lock intent before you write code. Make what we will do and won't do explicit, and agree on standards and constraints up front.
---

# Alignment

Lock intent before you write code. Make what we will do and won't do explicit, and agree on standards and constraints up front.

## 1. Purpose

Without explicit alignment, fast output leads to slow rework. Clarifying intent early prevents thrashing and ensures the generated code matches expectations.

## 2. Principles

- **Clear, testable requirements**: Requirements must be precise and agreed upon before implementation begins.
- **Explicit scope boundaries**: Define Scope In and Scope Out so the team knows exactly what is being built.
- **Definition of Done**: Establish the DoD upfront so everyone agrees when work is complete.
- **Non-negotiable constraints**: Engineering norms and safeguards are treated as hard constraints, not suggestions.

## 3. Practices

- **Write R and S first**: Complete the Requirements (R) and Safeguards (S) sections of the REASONS Canvas before any code is generated.
- **Given/When/Then criteria**: Use concrete acceptance criteria with explicit examples to remove ambiguity.
- **Mark gaps, don't guess**: Identify ambiguities and mark them `[NEEDS CLARIFICATION]` rather than assuming.
- **Review the prompt for intent**: Before generating code, re-read the structured prompt to confirm alignment.

## 4. Checklist

- Are requirements precise enough to generate tests?
- Are scope boundaries (in and out) explicit?
- Are all acceptance criteria testable?
- Are norms and safeguards defined and agreed upon?
