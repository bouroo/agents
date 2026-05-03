---
name: iterative-review
description: Turn AI output into a controlled loop. Review output against intent, fix the prompt first, then regenerate.
version: 1.0.0
triggers:
  - review loops
  - spec-code alignment
  - quality gates
  - output not matching intent
---

# Iterative Review

Turn AI output into a controlled review-and-iterate loop.

## Core Rule

When output doesn't match intent, fix the prompt or plan first — then regenerate. Never patch endlessly against a drifting solution.

## Workflow

1. **Generate**: Produce output from the spec or prompt.
2. **Review**: Compare output against intent, not just correctness.
3. **Classify**: Is the gap a logic issue or a refactoring issue?
4. **Fix the source**:
   - Logic mismatch → update the spec/prompt, then regenerate code.
   - Style/cleanup → refactor code directly, then sync back to spec.
5. **Verify**: Run tests. Confirm behavior matches acceptance criteria.
6. **Sync**: Keep spec and code aligned. Neither side silently diverges.

## Classification Guide

| Issue Type | Strategy | Direction |
|-----------|----------|-----------|
| Wrong business logic | Update prompt, regenerate | Spec → Code |
| Missing feature | Update scope, regenerate | Spec → Code |
| Code smell | Refactor code, sync back | Code → Spec |
| Magic numbers | Extract constants, sync | Code → Spec |
| Naming issue | Rename in code, sync | Code → Spec |

## Rules

- Never manually edit generated code to fix logic — fix the prompt.
- Never manually edit the spec for style — fix the code.
- Each iteration must have a clear review focus.
- Stop when output matches intent and tests pass.

## Checklist

- [ ] Output reviewed against intent (not just correctness)
- [ ] Issues classified as logic vs. style
- [ ] Source fixed before target
- [ ] Tests pass after fix
- [ ] Spec and code synchronized
