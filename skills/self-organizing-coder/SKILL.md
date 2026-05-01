---
name: self-organizing-coder
description: Autonomous workflow for building complex features, refactoring codebases, multi-step planning. Integrates abstraction-first design, intent alignment, iterative review from SPDD methodology.
---

# Self-Organizing Coder

## SPDD Workflow

| Phase | Activity |
|-------|----------|
| **Analysis** | Understand specification comprehensively |
| **REASONS Canvas** | Clarify objects, collaborations, boundaries |
| **Generate** | Implement based on plan |
| **Test** | Validate against acceptance criteria |
| **Prompt Update/Sync** | Logic correction: spec→code. Refactoring: code→spec |

## 1. Decompose and Plan
- **Analyze Goal**: Understand specification. No speculative features.
- **Abstraction First**: Clarify objects, collaborations, boundaries before tasks
- **Task Breakdown**: Small, actionable, testable tasks. Explicit implementation plan.
- **Parallel Execution**: Identify independent tasks, execute concurrently.

## 2. Align Intent
- **Lock Intent**: Confirm what/not done. Explicit scope boundaries.
- **Standards Up Front**: Naming, error handling, coding standards agreed before coding.
- **Acceptance Criteria**: Concrete, testable. Given/When/Then format when possible.
- **Explicit Uncertainty**: Vague requirement → halt, ask user, mark `[NEEDS CLARIFICATION]`.

## 3. Manage Context and Focus
- **Context Condensing**: Proactively summarize progress, discoveries, modified files.
  - **When**: Before delegating new subtasks, when approaching token limits
  - **What**: Goal, discoveries, accomplishments, modified files, remaining tasks
- **Bounded Subagent Prompts**: Tight scope, exact files, clear acceptance criteria, defined deliverables.

## 4. Implement and Iterate
- **Test-First**: Write tests validating spec before functional code. Tests fail first.
- **Incremental Delivery**: Working slices, one step at a time.
- **Anti-Abstraction**: Use existing frameworks directly. No unnecessary layers.

## 5. Iterative Review
- **Intent before details**: Output matches spec before code quality review.
- **Categorize changes**: Logic correction (behavior change) vs refactoring (structural). Apply correct sync.
- **Controlled loops**: Each iteration deliberate. Drift = realign spec before regenerating.
- **Review and Refine**: Run validators, linters, tests. Fix autonomously before proceeding.

## 6. Large Project Workflow

| Phase | Subagent | Output |
|-------|----------|--------|
| 1. Explore | explorer | Project structure, module boundaries, entry points |
| 2. Plan | planner | REASONS Canvas, task breakdown, dependencies |
| 3. Implement | implementer (parallel) | Modified files per module |
| 4. Validate | tester | Full test suite, regression check |
| 5. Sync | — | Spec↔code aligned. Spec→code for logic, code→spec for refactoring |

## Tools

| Purpose | Tool |
|---------|------|
| File discovery | `glob` |
| Content search | `grep`, `semantic_search` |
| Read files | `read` |
| Edit files | `edit`, `write`, `apply_patch` |
| Execute | `bash` |
| Analyze | `lsp` |
| Track progress | `todowrite` |
| Fetch URLs | `webfetch` |
| Web search | `websearch` |
| Load skill | `skill` |
| Ask user | `question` |

## Context Condensing

- **Auto-compaction**: Enabled via `compaction.auto`. Triggers at ~20K token headroom.
- **Pruning**: `compaction.prune` removes old outputs beyond recency window → `[Old tool result content cleared]`
- **Reserved**: `compaction.reserved` buffer preserved for continuity
- **Manual**: `/compact` command
- **Post-compaction**: Re-read modified files to avoid stale assumptions.