# Agent Configuration

Specifications drive implementation; code serves specifications.

## Agent & Tool Discovery

Available subagent types and tools are declared in each agent's system prompt. When delegating tasks, select agents and tools based on their described capabilities at runtime rather than relying on hardcoded names. Each agent definition specifies what it can do and what tools it has available.

## SPDD Core Loop

1. **Specify** → Decompose into concrete, testable tasks
2. **Align** → Lock intent: what/what-not done, constraints, definition of done
3. **Plan** → Design abstractions. Use REASONS Canvas for complex features
4. **Delegate** → Execute independent units in parallel
5. **Validate** → Run validators after every change. Fix immediately
6. **Sync** → Logic corrections: spec→code. Refactoring: code→spec

## REASONS Canvas

| Letter | Dimension | Content |
|--------|-----------|---------|
| R | Requirements | Problem, definition of done |
| E | Entities | Domain objects & relationships |
| A | Approach | Strategy, design decisions |
| S | Structure | Where change fits in system |
| O | Operations | Ordered, testable steps |
| N | Norms | Standards, naming, patterns |
| S | Safeguards | Constraints, invariants |

## Spec-Code Sync

| Change Type | Strategy |
|-------------|----------|
| New feature | Spec → Code |
| Logic correction | Spec → Code (fix spec first) |
| Refactoring | Code → Spec (refactor first, then sync) |

## Context Condensing

- **Auto-compaction**: Triggers at ~20K token headroom; `compaction.auto` enabled
- **Pruning**: Old outputs beyond ~40K recency → `[Old tool result content cleared]`; `compaction.prune`
- **Reserved buffer**: `compaction.reserved` tokens kept for context continuity
- **Manual trigger**: `/compact` slash command
- After compaction: re-read modified files to avoid stale assumptions

## Task Decomposition

1. Identify independent units — mark `[P]`
2. Order sequential dependencies explicitly
3. Assign each unit single deliverable
4. Validate independently before merging
5. Sync: fix spec first for logic changes
6. Track: `pending` → `in_progress` → `completed`

Decomposition output feeds into the **Operations** section of the REASONS Canvas.

## Large Project Workflow

1. **Explore** — Map structure, identify boundaries, locate entry points
2. **Plan** — Design via REASONS Canvas. Identify affected modules
3. **Implement** — Delegate bounded tasks. Validate each independently
4. **Validate** — Run full test suite. Verify no regressions

Context efficiency: reference specific files, break into subtasks, use `/compact` before major transitions.
