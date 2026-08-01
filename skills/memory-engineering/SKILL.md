---
name: memory-engineering
description: "Memory-engineering norms: separate instruction memory (human directives) from learning memory (agent-accumulated corrections), the retrieve/construct/update workflow, the project/user/local scope hierarchy, file hygiene (one fact per file, scoped loading, a sub-200-line index), and the .agents/memory/ fallback for harnesses without native memory. Use when persisting cross-session learnings, configuring agent memory, or deciding where memory artifacts live."
---

# Memory Engineering -- Agent-Loadable Norms

`AGENTS.md` §7 makes the repository the system of record and the conversation window a cache that
resets. This skill extends that principle to *cross-session learning memory* -- the corrections,
preferences, and hard-won facts an agent accumulates across tasks -- and answers the two questions
§7 leaves open: **what kind** of memory is this, and **where** does it live when no one told you.

> **Override.** A project-level memory spec that explicitly supersedes this skill takes precedence.

**Stance:** You treat memory as engineering, not an afterthought. Memory that is never written is
forgotten at compaction; memory written into the wrong place drifts behavior silently. The goal is
the smallest high-signal memory that survives a restart and never corrupts the instructions that
govern the next session.

## 1. Two Axes of Memory

Every fact sits on two axes. State both before you write:

- **Type** -- *semantic* (facts and conventions), *episodic* (what happened: a debugging
  root cause, a strategy that worked), *procedural* (skills and routines). These are §7's three
  layers; most learning memory is *semantic* or *episodic*.
- **Scope** -- *project* (shared, lives in the repo), *user* (personal, lives in the user config
  dir, never committed), *local* (this machine only, `.local.md`, never committed).

The full Type x Scope grid with on-disk homes and commit rules is in
[memory-layers](./references/memory-layers.md). Load it when deciding where a specific fact belongs.

## 2. Instruction vs. Learning Memory (the core rule)

This is the distinction most agents get wrong, and it is the one that causes silent behavioral
drift.

- **Instruction memory** is human-authored directives: coding standards, build commands, the
  `AGENTS.md`/`CLAUDE.md` router, decision logs, hard constraints. It governs *how the agent
  behaves*. It is owned by humans and **never auto-mutated by the agent**.
- **Learning memory** is agent-accumulated: a correction the user made, a preference, a failed
  attempt and its remedy, a recurring command. It records *what the agent learned*. It lives in its
  own files, never inside instruction files.

**Why:** Writing a learning ("user prefers tabs") into `AGENTS.md` works once -- then it is
indistinguishable from a deliberate standard, survives long after it stops being true, and drifts
behavior in ways no human reviewed. Learning memory must be auditable, versionable, and *forgettable*
on its own; instruction memory must not.

**Rules:**

- Never write an agent-learned correction or preference into an instruction file
  (`AGENTS.md`, `CLAUDE.md`, build docs, decision logs). Route it to learning memory instead.
- Never edit an instruction file to "fix" a rule you disagree with -- surface the conflict to the
  human. Instruction files are read-only to the agent unless a human delegates the change.
- Keep the two in separate trees so a reviewer can tell at a glance which is which.

## 3. The Workflow: Retrieve -> Construct -> Update

Memory is a loop, not a write-only bin:

1. **Retrieve before the task.** Before acting, check learning memory for facts relevant to this
   repo, user, or task type. Do not dump all of it -- pull only what matches.
2. **Construct context.** Assemble the retrieved facts plus the instruction files into the smallest
   window that lets you act correctly. Redundant or stale memory costs tokens for worse results.
3. **Update after the task.** When you learn something durable (a confirmed preference, a root
   cause, a working command), write it. And **forget**: when a fact is contradicted or stale, delete
   or correct it in the same pass -- never leave a stale fact beside a newer one.

A fact you only held in conversation is gone after compaction. If it will matter next session,
write it in step 3.

## 4. Where Memory Lives: Native vs. Fallback

Resolve the home once, the first time you need memory in a project:

- **If the running harness has native memory** (a built-in recall/store feature), **prefer it.** It
  is already wired into retrieve/construct and survives compaction correctly. Use the native store
  and stop here.
- **If the harness has no native memory** (the common case for a caller harness that just runs
  `AGENTS.md`), fall back to the project root: **`.agents/memory/`**, alongside the existing
  `.agents/plans/` and `.agents/handoff/` runtime state.

**Fallback layout** (host-neutral; compatible with the index-plus-fact-file pattern native stores
use, so an upgrade to a native store carries over cleanly):

```
.agents/memory/
├── MEMORY.md            # index/router: one line per fact, < 200 lines
└── <slug>.md            # one fact per file (scoped by topic or scope)
```

- `MEMORY.md` is the only file loaded eagerly -- a one-line pointer per fact ("what" + "where").
  Keep it under 200 lines; split into topic sub-files when it grows.
- One fact per file so each can be retrieved, updated, and forgotten independently. Frontmatter
  tags the type and scope (see [memory-layers](./references/memory-layers.md)).
- **Commit rules by scope:** *project* facts may be committed (they are shared, like Z.ai's
  version-controlled project memory); *user* facts go to the user-level config dir and are never
  committed; *local* (machine-specific paths, tokens) use a `.local.md` suffix and are gitignored.

Do not invent a third location. Two homes cover everything: native (if present) else
`.agents/memory/`.

## 5. File Hygiene & Pitfalls

- **Sub-200-line index.** An oversized memory file consumes the context window and *reduces*
  adherence to instructions -- the model spends attention on memory instead of the task. Split early.
- **One owner per fact.** Before writing, check for an existing fact that covers it; update that one
  rather than adding a duplicate. Conflicting rules across files make the agent pick one
  *arbitrably* -- resolve the conflict explicitly and delete the loser.
- **Dedupe / update / forget on every write.** Writing is also the garbage-collection moment: if the
  new fact supersedes an old one, retire the old one in the same change.
- **Scoped loading.** Load a fact only when its scope is active (working in the matching repo, for
  the matching task type). Eagerly loading all memory recreates the bloat you split files to avoid.
- **Signal over volume.** Do not record what the repo already records (code structure, git history,
  `CLAUDE.md`/`AGENTS.md` content). Record only what is non-obvious and not re-derivable: the *why*
  behind a preference, the root cause a future you would re-discover the hard way.

## 6. Anti-patterns

- **Learning leakage.** A correction written into `AGENTS.md`/`CLAUDE.md`. The flagship mistake --
  it drifts behavior and resists removal.
- **Self-mutating instructions.** Editing an instruction rule because the agent "knows better."
  Surface the conflict instead.
- **Unbounded growth.** Memory that is only ever appended to. Forgetting is a first-class operation.
- **Duplicate / conflicting facts.** Two files assert opposite rules; the model guesses. One owner.
- **Eager full-load.** Reading the entire memory tree into every turn. Load by scope.
- **Conversation-only.** A durable fact left in chat, lost at compaction.

## Cross-References

- [harness-engineering](../harness-engineering/SKILL.md) -- repository as system of record (§1-2),
  compaction resilience, state-on-disk
- [effective-code-craft](../effective-code-craft/SKILL.md) -- signal over volume, clarity norms
- [repo-documentation](../repo-documentation/SKILL.md) -- `docs/` as the *system-explanation* layer
  (distinct from learning memory, which records *agent experience*)

---

## References

- Z.ai -- Devpack Memory Mechanism: https://docs.z.ai/devpack/resources/memory-mechanism.md (layered
  memory, instruction vs. learning separation, scope hierarchy, file hygiene, fallback conventions)
- Anthropic -- Effective Harnesses for Long-Running Agents: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- OpenAI -- Harness Engineering: https://openai.com/index/harness-engineering/
