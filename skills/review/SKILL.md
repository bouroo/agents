---
name: review
description: Use when a change is written and someone must decide whether it merges — a diff must be judged for correctness, safety, tests, security, and structure, reported by severity with one verdict. Read-only; trusts the author's evidence (re-running claims is the verify skill).
---

# Review a Change

Review the current changes by severity and end at one verdict. This pass is read-only and trusts the author's evidence; adversarial re-running is the verify skill's job.

## 1. Read-only pass

- Review the current changes; a clean tree with nothing to diff means report there is nothing to review and stop.
- Never fabricate a diff to review.

## 2. Rubric — one read pass over the diff plus touched neighbors

- Correctness and spec parity: off-by-one, null and edge handling, races, leaks.
- Safety and error handling: none swallowed, no branching on error strings.
- Tests: happy, error, and boundary paths, asserting behavior rather than implementation details.
- Security: input validation, authorization, and no logged or committed secrets.
- Performance: flag only with measurement or a clear algorithmic concern.
- Readability and consistency with the surrounding convention.
- Simplicity: flag only where you can name what it buys.
- Structure and reuse: duplicated logic that will drift, and a module needing "and" to describe itself.

## 3. AI-residue tells

- Placeholder bodies, stubs, and swallowed errors.
- Comments that restate the code, and prose that says nothing about this project.

## 4. Severity

- MUST FIX (correctness bugs, security holes, data loss, broken builds) blocks merge.
- SHOULD FIX (missing tests, material maintainability gaps) earns its place by naming the concrete harm.
- NIT (style, optional) and SUGGESTION (an optional alternative) never block.
- Every finding carries a location and a suggested resolution.

## 5. Chase only correctness

- A reviewer asked to find problems always finds something, so report the full list and block only on MUST FIX.
- Pursuing every NIT manufactures over-engineering, so treat NIT and SUGGESTION as optional by definition.

## 6. Verdict

- One verdict — APPROVE / REQUEST CHANGES / BLOCKED — with a one-line justification, in this fixed template.

```
### MUST FIX
- [ ] [file:line] issue -> suggested resolution
### SHOULD FIX
- [ ] [file:line] issue -> suggested resolution
### NIT
- [ ] [file:line] nit
### SUGGESTION
- [ ] [file:line] optional idea

## Verdict
APPROVE | REQUEST CHANGES | BLOCKED - one-line justification
```

## 7. Gotchas

- Reviewing from the author's reasoning instead of the diff.
- Findings without a location or a resolution.
- Style findings blocking a merge.