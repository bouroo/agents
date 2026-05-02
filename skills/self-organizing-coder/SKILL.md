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

- Analyze goal, understand spec, no speculative features
- Abstraction first: objects, collaborations, boundaries before tasks
- Task breakdown: small, actionable, testable tasks with explicit plan
- Parallel execution: identify independent tasks, execute concurrently

## 2. Align Intent

- Lock intent: confirm what/not done. Explicit scope boundaries
- Standards up front: naming, error handling, coding standards before coding
- Acceptance criteria: concrete, testable. Given/When/Then when possible
- Explicit uncertainty: vague requirement → halt, ask, mark `[NEEDS CLARIFICATION]`

## 3. Manage Context

- Proactively summarize progress, discoveries, modified files
- Before delegating new subtasks or when approaching token limits
- Bounded subagent prompts: tight scope, exact files, clear deliverables

## 4. Implement and Iterate

- Test-first: tests validating spec before functional code
- Incremental delivery: working slices, one step at a time
- Anti-abstraction: use existing frameworks directly

## 5. Iterative Review

- Intent before details: output matches spec before code quality review
- Categorize: logic correction (behavior) vs refactoring (structural)
- Controlled loops: drift = realign spec before regenerating

## 6. Large Project Workflow

| Phase | Agent | Output |
|-------|-------|--------|
| Explore | explorer | Structure, boundaries, entry points |
| Plan | planner | REASONS Canvas, task breakdown |
| Implement | implementer (parallel) | Modified files per module |
| Validate | tester | Full test suite, regression check |
| Sync | — | Spec↔code aligned |

## Context Condensing

- Auto-compaction: `compaction.auto`, triggers at ~20K token headroom
- Pruning: `compaction.prune` removes old outputs
- Reserved: `compaction.reserved` buffer for continuity
- Post-compaction: re-read modified files
