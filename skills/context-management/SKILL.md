---
name: context-management
description: Context window management, conversation condensing, and efficient prompt engineering for AI-assisted development. Use when sessions grow long, context approaches limits, or when the user mentions context, condensing, compaction, or token efficiency.
---

# Context Management

Context window is finite and expensive. Maximize signal density; minimize waste.

## Token Efficiency

- Prefer concise summaries over verbose logging
- Use structured, scannable formats (lists, tables) over prose paragraphs
- Subagent return values should be structured and scannable
- Avoid repeating information already in context

## When to Compact

Trigger condensation/compaction when conversation grows long.

**Preserve:**
- Session goal and active task
- Discoveries and decisions with rationale
- Completed work and its outcomes
- Pending tasks and acceptance criteria

**Discard:**
- Verbose exploration logs
- Intermediate failed attempts
- Repeated/duplicate context
- Full file contents after extracting relevant portions

## What to Keep in Context

- Current task and its acceptance criteria
- Relevant file paths and key code snippets
- Decisions made and their rationale
- Remaining work items

## What to Drop from Context

- Full file contents — extract relevant portions, then drop
- Exploration logs — keep only target files/patterns found
- Failed approaches — note "approach X failed because Y", drop details
- Redundant information from multiple sources

## Delegation Strategy

- Use subagents for read-heavy exploration to keep main context clean
- Tell subagents exactly what to return — structured summaries, not raw dumps
- Prefer "explore" agents for research; keep implementation in main context
- Use `todowrite` to externalize progress tracking instead of re-reading context

## Practical Patterns

- Read files with targeted offsets, not entire large files
- Use `grep` to find specific patterns before reading full sections
- Batch parallel reads when you know which files you need
- Summarize file contents after reading rather than keeping full content in context
- Chain narrow tool calls over broad exploratory ones
