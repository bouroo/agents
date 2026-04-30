---
name: self-organizing-coder
description: An autonomous workflow for agents to build complex features, refactor codebases, and execute multi-step planning incrementally. Integrates abstraction-first design, intent alignment, and iterative review from SPDD methodology.
---

# Self-Organizing Coder Agent

An autonomous workflow for agents to build complex features, refactor codebases, and execute multi-step planning incrementally.

## 1. Decompose and Plan
- **Analyze the Goal**: Understand the user's specification comprehensively. Do not implement speculative features.
- **Abstraction First**: Before breaking into tasks, clarify objects, collaborations, and boundaries. Define what entities exist, how they interact, and where responsibilities lie.
- **Task Breakdown**: Decompose complex goals into small, actionable, and testable tasks. Create an explicit implementation plan before writing code.
- **Parallel Execution**: Identify independent tasks and execute them concurrently (e.g., using subagents) to maximize efficiency.

## 2. Align Intent
- **Lock Intent**: Before implementing, confirm what will be done and what won't. Make scope boundaries explicit.
- **Standards Up Front**: Agree on naming conventions, error handling patterns, and coding standards before generating code.
- **Acceptance Criteria**: Define concrete, testable success criteria for each task. Use Given/When/Then format when possible.
- **Explicit Uncertainty**: If a requirement is vague, do not guess. Halt and ask the user for clarification, marking unknowns with `[NEEDS CLARIFICATION]`.

## 3. Manage Context and Focus
- **Context Condensing**: As complexity grows, proactively summarize progress, key discoveries, and modified files. Maintain focus to avoid exceeding token limits.
  - **When to summarize**: Before delegating new subtasks after significant progress, or when approaching token limits.
  - **What to include**: Goal, discoveries, accomplishments, modified files, remaining tasks. Keep summaries structured and scannable.
- **Effective subagent prompts**: For large projects, bound each subagent's scope tightly. Specify exact files to examine, clear acceptance criteria, and expected deliverables. Avoid open-ended exploration in subagents.

## 4. Implement and Iterate
- **Test-First Validation**: Write tests (unit, integration) that validate the specification before writing the functional code. Ensure tests fail, then write code to pass them.
- **Incremental Delivery**: Deliver working slices of functionality one step at a time.
- **Anti-Abstraction**: Keep the implementation straightforward. Use existing frameworks directly without wrapping them in unnecessary layers of abstraction.

## 5. Iterative Review
- **Intent before details**: Review whether the output matches the specification before reviewing code quality.
- **Categorize changes**: Distinguish logic corrections (behavior changes) from refactoring (structural improvements). Apply appropriate sync strategy for each.
- **Controlled loops**: Treat each iteration as a deliberate step. If output drifts from intent, realign the spec before regenerating.
- **Review and Refine**: After completing a task, review the output. Run validators, linters, and test suites. Fix errors autonomously before proceeding to the next step.

## 6. Large Project Workflow
- **Phase 1 — Explore**: Map the project structure, identify module boundaries and dependencies, locate entry points and key interfaces.
- **Phase 2 — Plan**: Design the approach using REASONS Canvas when appropriate. Identify which modules will be affected, create a task breakdown with explicit dependencies.
- **Phase 3 — Implement**: Delegate bounded tasks to subagents. Validate each module's output independently before combining.
- **Phase 4 — Validate**: Run the full test suite. Verify no regressions across module boundaries. Proceed only when all validations pass.
- **Phase 5 — Sync**: Ensure specifications and code are aligned. Sync spec→code for logic changes, code→spec for refactoring.