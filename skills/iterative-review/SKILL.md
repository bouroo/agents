---
name: iterative-review
description: Turn AI output into a controlled loop. Review output against intent, fix the prompt first, then regenerate.
---

# Iterative Review

Turn AI output into a controlled loop. Review output against intent, fix the prompt first, then regenerate.

## Principles

- **Prompt captures intent**: The structured prompt is the source of truth; code is its implementation.
- **Fix the prompt first**: When behavior diverges, update the prompt before regenerating code.
- **Sync after refactoring**: Refactor code first, then sync back to the prompt.
- **Review intent, not just bugs**: Verify code matches stated intent.

## Workflow

1. Review generated code against the Canvas.
2. Categorize issues: logic mismatch vs. structural/style.
3. Logic mismatch → update prompt → regenerate.
4. Structural/style → refactor code → sync prompt.
5. Re-run tests.
6. Repeat until aligned.

## Practices

- After generating code, verify it maps one-to-one to Operations (O) in the REASONS Canvas.
- Logic corrections: identify gap, input new intent, update Canvas, regenerate targeted code.
- Refactoring sync: refactor code, then update Canvas.
- Regression tests after every iteration.
