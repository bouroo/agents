---
name: context-management
description: Strategies for managing AI context in long sessions, handling context limits, compaction, and maintaining context quality for large projects.
---

# Context Management

## Auto-Compaction

- Triggers at ~20K token headroom via `compaction.auto`
- Produces anchored summary: goal, constraints, progress, decisions, modified files
- Keeps most recent turns verbatim when they fit
- Updates previous summary rather than starting over

## Pruning

- Old tool outputs beyond ~40K recency → `[Old tool result content cleared]`
- Runs incrementally between turns
- `compaction.prune` enabled by default

## Reserved Buffer

- `compaction.reserved` tokens kept free for next turn
- Default: `min(20,000, model_max_output_tokens)`
- Lower value → compaction triggers later, risk of overflow
- Higher value → compaction triggers earlier, fewer overflow errors

## Manual Compaction

- `/compact` slash command
- Use before major transitions or phase changes
- Use after reaching significant milestones

## Post-Compaction Recovery

After compaction fires, re-read modified files to avoid stale assumptions. The summary may omit details from earlier turns.

## Configuration

```jsonc
{
  "compaction": {
    "auto": true,
    "prune": true,
    "tail_turns": 2,
    "preserve_recent_tokens": 8000,
    "reserved": 20000
  }
}
```

## Environment Overrides

| Variable | Effect |
|----------|--------|
| `KILO_DISABLE_AUTOCOMPACT=1` | Disable auto-compaction |
| `KILO_DISABLE_PRUNE=1` | Disable pruning |

## Best Practices

- Be specific in initial task descriptions for better summaries
- Use `AGENTS.md` for persistent project context that doesn't need compaction
- Use `todowrite` for external progress tracking that survives compaction
- Compact before switching to a different aspect of the project
- Review the summary after compaction for accuracy

## Large Project Strategies

- Navigate with `glob` and `grep` — find files, locate patterns, build mental model
- Change incrementally — work within modular boundaries
- Be context-efficient — reference specific files, break tasks into subtasks
- Understand unfamiliar code by reading public interfaces first, then tracing call chains
