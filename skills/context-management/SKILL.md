---
name: context-management
description: Strategies for managing AI context in long sessions, handling context limits, compaction, and maintaining context quality for large projects.
---

# Context Management Skill

Strategies for managing AI context in long sessions, handling context limits, compaction, and maintaining context quality for large projects.

## Context Window Awareness

- Every AI model has a context window limit — a maximum amount of text it can process at once
- As conversations grow with file contents, code snippets, and discussion history, responses slow down and eventually hit limits
- The agent should proactively manage context before limits are reached to maintain responsiveness and avoid session interruption

## The Compaction System

Kilo Code uses an automatic compaction system to manage context efficiently:

### Auto-Compaction Triggers

- **Trigger point**: Compaction runs when total token count fills the window minus a reserved buffer (~20K tokens by default)
- **Buffer rationale**: The reserved buffer ensures there's always room for the next response without overflow
- **Trackable models**: Auto-compaction only runs for models that declare a context window; custom models without declarations are not tracked
- **Configuration**: Adjust via `compaction.auto` in kilo.jsonc (default: true)

### Context Pruning

- **Recency window**: Old tool outputs beyond ~40K tokens are pruned and replaced with `"[Old tool result content cleared]"`
- **Incremental behavior**: Pruning runs between turns so large outputs don't accumulate space indefinitely, even before full compaction triggers
- **Configuration**: Toggle via `compaction.prune` in kilo.jsonc (default: true)

### Reserved Buffer Configuration

| Setting | Default | Effect |
|---------|---------|--------|
| `compaction.reserved` | `min(20,000, model_max_output)` | Token headroom for next turn; smaller = later trigger, larger = earlier trigger |

**Trade-off guidance**: Lower values (e.g., 10K) give more raw window turns but risk mid-turn overflow on large responses. Higher values (e.g., 40K) trigger earlier with fewer overflow errors but shorter effective conversations between summaries.

## Manual Compaction

Trigger compaction at any time using:
- **Slash command**: type `/compact` in chat (searchable by typing `smol` or `condense`)
- **Task header button**: click the compact icon in the active task header
- **Settings**: toggle auto-compaction in **Settings → Context**

## When to Compact Manually

- **Before major phase transitions**: exploration → planning → implementation → validation
- **After completing significant milestones**: When a meaningful chunk of work is done
- **When context feels unwieldy**: Conversation has grown long and hard to follow
- **At ~70-80% estimated context usage**: Proactively, before automatic trigger

## Writing Effective Summaries

A good summary preserves all of the following:

- **Goal**: What the user originally asked for
- **Decisions**: Key design choices and their rationale
- **Discoveries**: Important findings about the codebase or requirements
- **Accomplished**: What has been completed, including file paths
- **Modified Files**: List of files changed with brief descriptions
- **Remaining**: Outstanding tasks and their status

A bad summary is vague, omits rationale, or loses file references.

**Quality criteria**: Summaries must be specific — "refactored auth module in src/auth/" not "did some refactoring". Include actual file paths and concrete outcomes, not abstract descriptions.

## Using Subdirectory AGENTS.md

For domain-specific context that applies to particular areas:

- Place an `AGENTS.md` file in relevant subdirectories
- It loads alongside the root AGENTS.md, with subdirectory version taking precedence
- Use this for module-specific conventions, architectural decisions, or team-specific workflows
- Keeps main context focused while ensuring domain knowledge is available when working in that area

## Context Quality Best Practices

- **Be specific in initial task descriptions**: This feeds better summaries when compaction occurs
- **Reference specific file paths**: Not vague descriptions — "examine src/auth/" not "look at the auth code"
- **Break large tasks into smaller subtasks**: Keeps context focused and boundaries clear
- **After compaction, re-read modified files**: Verify assumptions haven't become stale
- **Use todowrite for progress tracking**: External tracking survives context compaction

## Large Project Context Management

- **Read only what's needed**: Don't load entire modules into context
- **Use exploration agents to map boundaries**: Before deep diving into complex areas
- **Keep subagent prompts bounded**: Specify exact files, clear acceptance criteria, expected deliverables
- **Use grep and glob strategically**: Instead of reading everything to find patterns
- **Maintain mental map of relationships**: Between modules, not individual implementations
- **Verify assumptions after condensing**: Module boundary assumptions may change during context condensation

## Tool-Specific Context Tips

- `read`: Read specific line ranges for large files, not entire files
- `grep`: Use targeted patterns, not broad searches that return thousands of results
- `glob`: Map directory structure first, then drill down
- `todowrite`: Track progress externally so it survives context compaction
- `skill`: Load skills on-demand rather than keeping all context loaded

## Configuration Reference

Compaction settings in kilo.jsonc:

```jsonc
{
  "compaction": {
    "auto": true,     // Enable/disable automatic compaction
    "prune": true,    // Clear old tool outputs beyond recency window
    "reserved": 20000 // Token buffer for next turn
  }
}
```

Dedicated compaction agent (optional):

```jsonc
{
  "agent": {
    "compaction": {
      "model": "anthropic/claude-haiku-4-5"  // Use cheaper/larger-context model for summarization
    }
  }
}
```

Environment overrides:

| Variable | Effect |
|----------|--------|
| `KILO_DISABLE_AUTOCOMPACT=1` | Forces `compaction.auto = false` |
| `KILO_DISABLE_PRUNE=1` | Forces `compaction.prune = false` |
| `KILO_EXPERIMENTAL_OUTPUT_TOKEN_MAX` | Overrides the 32,000 default output-token ceiling |