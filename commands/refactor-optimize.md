---
description: Refactor and optimize code feature-by-feature without breaking public API
agent: code
subtask: true
---

# Refactor & Optimize

Refactor `$ARGUMENTS` while preserving public API contracts and passing all existing tests.

## Pre-conditions

Before any changes, establish the baseline:

1. **Green baseline** — Run the full test suite (add missing if nessesary). If tests fail, stop and report — refactoring on a red baseline is undefined behavior.
2. **Map surface area** — Use `grep` to find all exported/public symbols in target files. These are the API contract — do not change signatures, behavior, or exported types without explicit instruction.
3. **Identify callers** — Use `grep` to find all call sites of exported symbols. This is the blast radius.

## Execution Loop

For each refactoring target (one at a time):

1. **Describe** — State the change and why. Write it as a comment or in the commit message.
2. **Edit** — Make the minimal change. Prefer `edit` over `write`.
3. **Verify** — Run tests after every change. If red, fix and re-run until green.
4. **Lint** — Run linter/type-checker. Fix violations and re-run until clean.

**CONTINUE** automatically after each verification passes. Only stop when all identified improvements are complete or at diminishing returns.

## Refactoring Catalog

Apply these patterns when applicable:

| Pattern | When |
|---|---|
| **Extract function** | Cyclomatic complexity >10 or >3 levels of nesting |
| **Name constants** | Magic numbers or unexplained string literals |
| **Reduce scope** | Variables declared far from usage or scope too wide |
| **Simplify control flow** | Early returns, guard clauses, eliminate flag variables |
| **Remove duplication** | Same logic in 2+ places (but avoid premature abstraction) |
| **Tighten types** | Replace `any`/`interface{}` with concrete types; prevent invalid states by design |
| **Pre-allocate** | Known-size slices/maps without `make` with capacity |
| **Error context** | Bare errors wrapped with `fmt.Errorf("doing X: %w", err)` or equivalent |

## Constraints

- **One concern per step** — Never mix refactoring with feature changes.
- **No public API breakage** — Signatures, behavior, and exported types stay the same.
- **Preserve test intent** — Do not change test expectations to match new implementation.
- **Module size** — Keep modules under 400 lines. Extract when larger.
- **Stop at diminishing returns** — Not every function needs to be perfect.

## Final Verification

After all refactorings:
1. Run full test suite — must pass.
2. Run linter — zero errors.
3. Run type-checker (if applicable) — zero errors.
4. Summarize all changes made with file names and rationale.
