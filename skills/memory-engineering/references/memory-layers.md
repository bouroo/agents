# Memory Layers -- Type x Scope Map

> Load on demand. The short pointer lives in [memory-engineering](../SKILL.md) §1 (two axes) and §4
> (fallback layout); this file is the full grid.

Two axes decide where a fact lives and whether it is committed. State both axes before you write a
fact -- a fact without a type and a scope has no home.

## The Type Axis

What *kind* of thing the fact is (§7's three layers):

| Type | What it holds | Example | Typical on-disk form |
|---|---|---|---|
| **semantic** | facts and conventions | "this repo uses tabs", "the API gateway is at `:8080`" | `MEMORY.md` index + one fact per file |
| **episodic** | what happened | a debugging root cause, a strategy that worked, a failed attempt + remedy | `retro.md`, handoff summaries, one fact per file |
| **procedural** | skills and routines | how to run a verification gate, a reusable workflow | `skills/<name>/SKILL.md` |

Most *learning* memory is semantic or episodic. Procedural memory is already served by the `skills/`
tree -- do not duplicate a skill into learning memory.

## The Scope Axis

*Who* the fact applies to and *where* it is stored:

| Scope | Applies to | Home | Committed? |
|---|---|---|---|
| **project** | everyone in this repo | `.agents/memory/` (or native store) | yes -- shared, version-controlled |
| **user** | one person, across repos | user-level config dir (`~/.config/...`) | never |
| **local** | this machine only | `.agents/memory/*.local.md` | never -- gitignored |

- **Project** is the most valuable layer: shared, version-controlled, survives for the next agent or
  human. Default to project scope unless the fact is genuinely personal or machine-specific.
- **User** scope (personal preferences, individual corrections) never goes in the repo -- it would
  impose one person's habits on every collaborator.
- **Local** scope (machine-specific paths, local tokens, scratch) uses the `.local.md` suffix and is
  gitignored. Never commit a secret or a path that only exists on your machine.

## The Orthogonal Axis: Instruction vs. Learning

Independent of type and scope, every fact is one of:

| Axis | Owner | Where it lives | Mutability |
|---|---|---|---|
| **instruction** | human | `AGENTS.md`, `CLAUDE.md`, decision logs, build docs | human-only; agent never auto-edits |
| **learning** | agent | learning-memory files (this skill) | agent writes/updates/forgets |

A fact's type and scope do **not** determine its instruction/learning axis. "The build command is
`make test`" can be instruction (a human wrote it in `AGENTS.md`) or learning (the agent discovered
the command and recorded it). The axis is about *authority*, not content. See SKILL.md §2 for why the
two must never be mixed.

## Combined Guidance

Pick the home from both axes together:

| Fact | Type | Scope | Axis | Where |
|---|---|---|---|---|
| repo uses tabs; gateway on `:8080` | semantic | project | learning | `.agents/memory/` (+ `MEMORY.md` line) |
| user prefers commit messages under 72 chars | semantic | user | learning | user config dir (uncommitted) |
| a machine-local scratch path | semantic | local | learning | `.agents/memory/*.local.md` |
| root cause of last week's build break | episodic | project | learning | `.agents/memory/` or `retro.md` |
| "never push to main" (a governing rule) | semantic | project | **instruction** | `AGENTS.md` -- never learning memory |
| how to run the verify gate | procedural | project | instruction | `skills/verify-phase/...` |

If a fact could go in two places, prefer the more specific scope and the non-instruction axis --
learning memory is auditable and forgettable; instruction memory is not.

## Cross-References

- [memory-engineering](../SKILL.md) -- §2 (Instruction vs. Learning), §4 (fallback layout), §5 (hygiene)
- [harness-engineering](../../harness-engineering/SKILL.md) -- §7 state-on-disk, compaction resilience

## Reference

- Z.ai -- Devpack Memory Mechanism: https://docs.z.ai/devpack/resources/memory-mechanism.md
