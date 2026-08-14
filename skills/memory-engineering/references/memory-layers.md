# Memory Layers Type x Scope Map

> Load on demand. The short pointer lives in [memory-engineering](../SKILL.md); this file is the full grid.

Two axes decide where a fact lives and whether it is committed. State both before you write a fact. A fact without a type and a scope has no home.

## The Type Axis

What *kind* of thing the fact is:

| Type | What it holds | Example | Typical on-disk form |
|---|---|---|---|
| **semantic** | facts and conventions | "this repo uses tabs", "the API gateway is at `:8080`" | `MEMORY.md` index + one fact per file |
| **episodic** | what happened | a debugging root cause, a strategy that worked, a failed attempt + remedy | `.agents/plans/{slug}/retro.md`, handoff summaries, one fact per file |
| **procedural** | how to do something | how to run the verify gate, how to roll a release | skills, runbooks, `MEMORY.md` one fact per file |

## The Scope Axis

Where it applies: **local** (this machine) -> **project** (this repo) -> **user** (all this user's projects). More specific wins.

## Instruction vs. Learning axis

Whether it is a human directive (instruction, stable) or an agent correction (learning, forgettable).

| Fact | Type | Scope | Axis | Home |
|---|---|---|---|---|
| "the API gateway is at `:8080`" | semantic | project | learning | `.agents/memory/` |
| "user prefers tabs" | semantic | user | learning | user memory |
| a debugging root cause from last task | episodic | project | learning | `.agents/memory/` then forget when stale |
| "never push to main" (a governing rule) | semantic | project | **instruction** | `AGENTS.md`. Never learning memory |
| how to run the verify gate | procedural | project | instruction | `commands/cmd-verify.md` |

If a fact could go in two places, prefer the more specific scope and the non-instruction axis. Learning memory is auditable and forgettable; instruction memory is not.

## retro.md vs. memory/

`retro.md` is plan-scoped, not a second learning-memory home. A per-task failure analysis is captured first in `.agents/plans/{slug}/retro.md` and is transient with that plan. Graduate a lesson that must survive the task to `.agents/memory/` (one fact per file plus a `MEMORY.md` line) so the *durable* subset is auditable and forgettable while the plan-scoped working notes are not.

## Cross-References

- [memory-engineering](../SKILL.md) instruction vs. learning, the workflow, fallback layout, hygiene.
- [harness-engineering](../../harness-engineering/SKILL.md) state-on-disk, compaction resilience.
