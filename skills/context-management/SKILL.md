---
name: context-management
description: Strategies for managing AI context in long sessions, handling context limits, compaction, and maintaining context quality for large projects.
version: 1.0.0
triggers:
  - long sessions
  - context limits
  - large codebase work
  - context quality degradation
---

# Context Management

Strategies for maintaining high-quality context throughout long AI sessions.

## Principles

### Context Hygiene
- Summarize completed work before moving to the next task.
- Remove resolved context that is no longer relevant.
- Keep active context focused on the current task.
- Document decisions made so you don't re-derive them.

### Progressive Detail
- Start with high-level understanding before diving into details.
- Load file content only when needed, not preemptively.
- Use search tools first, read files second, edit files third.
- Batch related reads together to minimize context switches.

### Session Management
- Break large tasks into sessions with clear boundaries.
- At session start: load project context, review recent changes.
- At session end: summarize progress, note next steps in AGENTS.md.
- Use git history to reconstruct context across sessions.

### Context Window Budget
- Reserve 20% of context for tool output during implementation.
- If context exceeds 70%, summarize before continuing.
- Prefer targeted searches over reading entire files.
- Use file references (path:line) instead of quoting large blocks.

## Checklist

- [ ] Active context is relevant to current task
- [ ] Stale context summarized or removed
- [ ] Decisions documented for future reference
- [ ] Context budget monitored
