---
name: context-management
description: Strategies for managing AI context in long sessions, handling context limits, compaction, and maintaining context quality for large projects.
---

# Context Management Skill

Strategies for managing AI context in long sessions, handling context limits, compaction, and maintaining context quality for large projects.

## Context Window Awareness

- Every AI model has a context window limit
- As conversations grow, responses slow down and eventually hit limits
- The agent should proactively manage context before hitting limits

## Auto-Compaction

- Compaction automatically summarizes conversation history when approaching limits
- Reserved buffer: ~20K tokens kept free for the next response
- Pruning: old tool outputs beyond ~40K recency window are replaced with placeholder text
- The agent should trigger manual compaction before auto-compaction when appropriate

## When to Compact Manually

- Before major phase transitions (exploration → planning → implementation → validation)
- After completing a significant milestone
- When the conversation feels unwieldy or context feels stale
- When approaching ~70-80% of estimated context usage

## Writing Effective Summaries

A good summary preserves:

- **Goal**: What the user originally asked for
- **Decisions**: Key design choices and their rationale
- **Discoveries**: Important findings about the codebase
- **Accomplished**: What has been completed, including file paths
- **Modified Files**: List of files changed with brief descriptions
- **Remaining**: Outstanding tasks and their status

A bad summary is vague, omits rationale, or loses file references.

Be specific — "refactored auth module in src/auth/" not "did some refactoring"

## Context Quality Best Practices

- Be specific in initial task descriptions — this feeds better summaries
- Use AGENTS.md for persistent project context that doesn't need to be repeated
- Use subdirectory AGENTS.md files for domain-specific context
- After compaction, re-read modified files to avoid stale assumptions
- Reference specific file paths in prompts, not vague descriptions
- Break large tasks into smaller subtasks — keeps context focused

## Large Project Context Management

- Don't load entire modules into context — read only what's needed
- Use exploration agents to map boundaries before deep diving
- Keep subagent prompts bounded — specify which files/directories to work on
- Use grep and glob strategically instead of reading everything
- Maintain a mental map of module relationships, not individual implementations
- When context condenses, verify module boundary assumptions haven't changed

## Tool-Specific Context Tips

- `read`: Read specific line ranges for large files, not entire files
- `grep`: Use targeted patterns, not broad searches that return thousands of results
- `glob`: Map directory structure first, then drill down
- `todowrite`: Track progress externally so it survives context compaction
- `skill`: Load skills on-demand rather than keeping all context loaded