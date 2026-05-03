---
name: context-management
description: Strategies for managing AI context in long sessions, handling context limits, compaction, and maintaining context quality for large projects.
version: 2.0.0
triggers:
  - long sessions
  - context limits
  - large codebase work
  - context quality degradation
  - compaction
  - context pruning
---

# Context Management

Strategies for maintaining high-quality context throughout long AI sessions.

## Kilo Compaction Mechanics

### Auto-Compaction
- Triggers when total tokens (input + output + cached reads/writes) fill the context window minus a reserved buffer (~20K tokens for models with separate input limits).
- Produces an **anchored summary**: goal, constraints, progress, decisions, next steps, critical context, relevant files.
- Replaces older conversation history while keeping the most recent turns verbatim (default: 2 user turns).
- On re-compaction, updates the previous summary — preserves still-relevant details, removes stale ones.

### Pruning
- Between turns, a lighter **prune** pass replaces completed tool outputs outside a 40K-token recency window with `"[Old tool result content cleared]"`.
- Runs incrementally — large tool outputs don't consume space forever, even before full compaction.

### Manual Compaction
- Use `/compact` (also findable via `smol` or `condense`) to trigger compaction on demand.
- Trigger before major task transitions for control over when the summary is produced.

## Writing Compactable Output

### Survive Pruning
- Use **file:line references** (`path/to/file.go:42`) instead of quoting large code blocks inline.
- Record decisions in **AGENTS.md** — it's write-protected and persists across compaction.
- Summarize completed work before starting the next task.

### Survive Compaction
- Structure output with clear headings and lists — summaries extract structured content better.
- State the current goal, constraints, and progress explicitly at each milestone.
- Document "why" decisions, not just "what" — the "why" is what compaction loses first.

### Avoid Context Waste
- Don't re-read files already in the recent tail (last 2 turns).
- Batch related reads together to minimize context switches.
- Use search tools first, read files second, edit files third.
- Reserve ~20% of context for tool output during implementation.

## Configuration (kilo.jsonc)

```jsonc
{
  "compaction": {
    "auto": true,                    // Enable auto-compaction
    "prune": true,                   // Prune old tool outputs beyond 40K window
    "tail_turns": 2,                 // Recent turns kept verbatim
    "preserve_recent_tokens": 8000,  // Max token budget for recent tail
    "reserved": 20000,               // Buffer kept free; triggers compaction
  },
  "agent": {
    "compaction": {
      "model": "anthropic/claude-haiku-4-5",  // Cheaper model for summarization
    },
  },
}
```

### Tuning `compaction.reserved`
- **Lower** (e.g., 10K): compaction triggers later, more raw turns, risk of mid-turn overflow.
- **Higher** (e.g., 40K): compaction triggers earlier, fewer overflow errors, shorter raw conversations.

## Checklist

- [ ] Decisions documented in AGENTS.md (persists across compaction)
- [ ] File:line references used instead of inline code blocks
- [ ] Completed work summarized before transitioning tasks
- [ ] `/compact` triggered manually before major transitions
- [ ] Context budget monitored (trigger compaction before auto-trigger if needed)