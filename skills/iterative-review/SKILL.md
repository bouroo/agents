---
name: iterative-review
description: Turn AI output into a controlled loop. Review output against intent, fix the prompt first, then regenerate.
---
# Iterative Review

Turn AI output into a controlled loop. Review output against intent, fix the prompt first, then regenerate.

## 1. Purpose

Without disciplined review-and-iterate, teams either force patches until solutions drift, or restart repeatedly and lose control. A structured loop keeps intent and output aligned.

## 2. Principles

- **Prompt captures intent**: The structured prompt is the source of truth; code is its implementation.
- **Fix the prompt first**: When behavior diverges from intent, update the prompt before regenerating code.
- **Sync after refactoring**: When refactoring (no behavior change), refactor the code first, then sync back to the prompt.
- **Review intent, not just bugs**: Reviews shift from spotting individual bugs to verifying that the code matches the stated intent.

## 3. Practices

- **Map to Operations**: After generating code, verify it maps one-to-one to Operations (O) in the REASONS Canvas.
- **Logic corrections**: Identify the gap, input new intent into the prompt, update the Canvas, and regenerate targeted code.
- **Refactoring sync**: Refactor code, then use a sync command to update the Canvas so it remains accurate.
- **Regression tests after every iteration**: Run tests after each cycle to catch unintended side effects.

## 4. Workflow

1. Review generated code against the Canvas.
2. Categorize issues: logic mismatch vs. structural or style concerns.
3. Logic mismatch → update the prompt → regenerate.
4. Structural or style → refactor code → sync prompt.
5. Re-run tests.
6. Repeat until aligned.
