---
name: self-organizing-coder
description: Autonomous workflow for building complex features, refactoring codebases, multi-step planning. Integrates abstraction-first design, intent alignment, and iterative review from the SPDD methodology.
version: 1.0.0
triggers:
  - complex multi-step tasks
  - autonomous feature building
  - codebase refactoring
  - multi-agent orchestration
---

# Self-Organizing Coder

Autonomous workflow for complex, multi-step engineering tasks.

## Workflow

### 1. Understand
- Read the task. Identify ambiguity. Ask clarifying questions if needed.
- Explore the codebase: structure, conventions, patterns, dependencies.
- Identify the scope: what's changing, what's affected, what's out of scope.

### 2. Plan
- Apply **alignment**: define scope in/out, acceptance criteria, constraints.
- Apply **abstraction-first**: identify objects, collaborations, boundaries.
- Break the task into ordered, testable steps.
- Use the todo list for 3+ steps. Mark in_progress one at a time.

### 3. Implement
- Follow the plan step-by-step. One task at a time.
- For each step:
  1. Write/edit code following the plan.
  2. Run relevant tests.
  3. Verify the step is complete before moving on.
- Delegate to subagents when appropriate:
  - **explorer**: search and understand code
  - **implementer**: write code, run commands
  - **tester**: write and run tests

### 4. Review
- Apply **iterative-review**: compare output against intent.
- Run lint, typecheck, and tests.
- If reality diverged from the plan, update the plan first.
- Classify fixes: logic → fix spec then code; style → fix code then sync.

### 5. Deliver
- Verify all acceptance criteria pass.
- Run final lint, typecheck, and test suite.
- Summarize changes. Note anything deferred or noteworthy.

## Rules

- Never skip the plan. Even a 30-second plan prevents rework.
- Never implement more than one task at a time.
- When stuck, re-read the plan. If the plan is wrong, fix the plan.
- After each task, verify before starting the next.

## Checklist

- [ ] Task understood, ambiguity resolved
- [ ] Plan created with scope and acceptance criteria
- [ ] Tasks decomposed and ordered
- [ ] Each task implemented and verified individually
- [ ] Final review against acceptance criteria
- [ ] Lint, typecheck, and tests pass
