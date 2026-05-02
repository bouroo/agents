---
name: context-management
description: Strategies for managing AI context in long sessions, handling context limits, compaction, and maintaining context quality for large projects.
---

# Context Management

## Auto-Compaction

- Triggers at ~20K token headroom via `compaction.auto`
- Produces anchored summary: goal, constraints, progress, decisions, modified files
- Updates previous summary rather than starting over

## Pruning

- Old tool outputs beyond ~40K recency → `[Old tool result content cleared]`
- `compaction.prune` enabled by default

## Reserved Buffer

- `compaction.reserved` tokens kept free for next turn
- Lower value → compaction triggers later, risk of overflow
- Higher value → compaction triggers earlier, fewer overflow errors

## Post-Compaction Recovery

Re-read modified files to avoid stale assumptions. The summary may omit details from earlier turns.

## Best Practices

- Be specific in initial task descriptions for better summaries
- Use `AGENTS.md` for persistent project context that survives compaction
- Use `todowrite` for external progress tracking
- Compact before switching to a different project aspect
- Review the summary after compaction for accuracy

## Large Project Strategies

- Navigate with `glob` and `grep` — find files, locate patterns, build mental model
- Change incrementally — work within modular boundaries
- Be context-efficient — reference specific files, break tasks into subtasks
- Understand unfamiliar code by reading public interfaces first, then tracing call chains
