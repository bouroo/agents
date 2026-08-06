---
name: memory-engineering
description: "Agent memory engineering: separate instruction memory (human directives) from learning memory (agent corrections), the retrieve/construct/update/forget workflow, scope hierarchy, file hygiene, and the .agents/memory fallback. Use when persisting cross-session learnings, configuring agent memory, or deciding where memory artifacts live."
---

# Memory Engineering

Treat cross-session memory as engineering, not an afterthought. The repository is the system of record; the conversation window is a cache that resets. This skill governs *learning memory* -- the corrections, preferences, and hard-won facts an agent accumulates across tasks.

Memory never written is forgotten at compaction; memory written into the wrong place drifts behavior silently. Goal: the smallest high-signal memory that survives a restart and never corrupts the instruction layer.

## Instruction vs. learning (the load-bearing split)

- **Instruction memory** is human-authored directives: `AGENTS.md`, build docs, style guides. Stable and predictable. **Never write corrections into it** -- they drift behavior silently and resist removal. Update only when the human changes a directive.
- **Learning memory** is agent-accumulated: a correction, a preference, a failed attempt and its remedy. Auditable and *forgettable*. Lives in its own files.

The split is the core invariant: instruction stays stable; learning is mutable. When a learned correction becomes durable policy, the *human* promotes it into instruction memory -- never the agent.

## The workflow: retrieve -> construct -> update -> forget

1. **Retrieve before.** Pull relevant learning memory scoped to the task before starting. Load by scope, never the whole tree.
2. **Construct during.** When a correction or hard-won fact appears, capture it -- one fact per file, frontmatter + one-line index entry.
3. **Update after.** Persist durable learnings at task end; update the index.
4. **Forget deliberately.** Forgetting is a first-class operation -- stale or superseded facts are deleted, not archived. Unbounded growth is a failure mode.

## Scope hierarchy (where a fact lives)

More specific scope wins; prefer the non-instruction axis.

| Scope | Home | Committed? |
|---|---|---|
| **local** (this machine/session) | `.agents/memory/local/` or harness-native memory | no |
| **project** (this repo, shared) | `.agents/memory/` (one fact per file + `MEMORY.md` index) | yes |
| **user** (all this user's projects) | harness-native user memory or `~/.agents/memory/` | as configured |

**`retro.md` is plan-scoped, not a learning-memory home.** A per-task failure analysis is captured first in `.agents/plans/{slug}/retro.md` and is transient with that plan. Graduate a lesson that must survive the task to `.agents/memory/` so the durable subset is auditable while the working notes are not.

## The Type x Scope grid

State both axes before you write a fact -- a fact without a type and a scope has no home.

- **semantic** -- facts and conventions (the repo uses tabs; the gateway is at `:8080`).
- **episodic** -- what happened (a root cause, a strategy that worked).
- **procedural** -- how to do something (a skill, a runbook).

See [memory-layers](references/memory-layers.md) for the full grid with homes and commit rules.

## File hygiene

- **One fact per file.** Frontmatter (`name`, `description`, `type`) + one fact. No mega-files.
- **One index line per fact** in `MEMORY.md`. Sub-200-line index.
- **Scoped loading.** Load only the scope the task needs; never eager full-load.
- **No duplicates.** One owner per fact; on conflict, resolve and delete the loser.

## Anti-patterns

- Writing a correction into instruction memory (drifts silently).
- Conversation-only durable fact (lost at compaction).
- Append-only memory without forgetting (unbounded growth).
- Duplicate/contradictory facts (agent guesses).
- Eager full-tree load every turn (taxes the window).

## References

- [memory-layers](references/memory-layers.md) -- the full Type x Scope grid with homes and commit rules.
- [harness-engineering](../harness-engineering/SKILL.md) -- repo-as-record, compaction resilience.
- [code-craft](../code-craft/SKILL.md) -- signal over volume.
