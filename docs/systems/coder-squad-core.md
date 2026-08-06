# Coder Squad Core

## Purpose

This repo ships a shared, language- and host-agnostic configuration for AI coding assistants: one **Coder Squad** (three agent roles), six **Commands** (reusable phase workflows), and a set of **Skills** (modular capability doctrine), all governed by a root `AGENTS.md`. Drop the repo's artifacts into a supported host and that host's coding agent inherits the same THINK-ACT-PROVE-GROW loop, the same safety boundaries, and the same verification discipline as every other supported host.

## Questions this doc answers

- What are the three squad roles and what can each one touch?
- How does a task move through THINK-ACT-PROVE-GROW?
- What is the load-bearing safety split, and where is it enforced?
- How do Commands and Skills relate to the squad?

## Scope

The squad's three agent role definitions (`agents/conductor.md`, `agents/coder.md`, `agents/discover.md`), the root governance doctrine (`AGENTS.md`), the six phase Commands (`commands/*.md`), and the core Skills (`skills/*/SKILL.md`) that the squad loads on demand.

## Non-scope

Multi-host distribution (symlinking these artifacts into a specific tool's config directory) is a separate system -- see [Multi-Host Install and Discovery](../flows/multi-host-install-and-discovery.md). Domain-specific doctrine (Go, OpenAPI, Confluence) lives in domain-adapter skills and is loaded only when that domain applies.

## Key concepts

**The squad.** Three roles, split by a single load-bearing boundary -- **mutating vs. read-only**:

| Agent | Mode | Touches source? | Runs toolchain? |
|---|---|---|---|
| [conductor](../../agents/conductor.md) | `primary` | No | No |
| [coder](../../agents/coder.md) | `subagent` | Yes | Yes |
| [discover](../../agents/discover.md) | `subagent` | No | No |

`conductor` decomposes work into a unit graph, delegates complete packets to `coder`/`discover`, audits returned evidence, and converges. `coder` is the only role that edits files or runs commands -- it implements, fixes, verifies (L1/L2/L3 + a mutation probe), and adversarially judges. `discover` explores unfamiliar code, does version-sensitive lookups, and reviews diffs against a fixed rubric -- writing only under `.agents/`.

**The loop.** Every task moves through THINK (classify, gather evidence) -> ACT (one bounded change, delegated to `coder`) -> PROVE (executable evidence at L1/L2/L3, a mutation probe, adversarial review) -> GROW (catalog failure modes into `.agents/plans/{slug}/retro.md`, convert recurring failures into gates). Defined in `AGENTS.md` §4.

**Commands.** Six reusable phase workflows -- `document`, `judge`, `openapi`, `refactor`, `review`, `verify` -- each bound to a squad agent via its `agent:` frontmatter field and tagged with the loop `phase:` it belongs to.

**Skills.** Progressive-disclosure capability doctrine, loaded only when a task's shape matches a skill's trigger. Seven core skills (`code-craft`, `harness-engineering`, `memory-engineering`, `spec-driven-development`, `performance-patterns`, `repo-documentation`, `commit-message`) are language- and host-agnostic; three domain-adapter skills (`go-essential`, `openapi-spec`, `confluence`) name a specific domain and are excluded from the agnostic-core gate.

**Artifact gates.** Four forced report lines fire at decision points regardless of host: `INTENT:` (before a behavior-changing edit), `TWINS:` (after fixing a defect -- did you search for siblings?), `AUTH:` (before an outward action), `PENDING:` (a prescribed follow-up left untaken). Defined in [code-craft](../../skills/code-craft/SKILL.md).

## Error handling

Hard rules enforced across the squad, independent of host: never swallow an error, never branch on error strings, never leave a dirty checkout, never declare done without executable evidence. See `AGENTS.md` §5 and §9.

## Testing notes

`scripts/checks.py` runs 17 deterministic gates over every artifact in this system (frontmatter shape, line budgets, link integrity via manifest cross-refs, and -- new in this system's current form -- `G17_agnostic_core`, which fails if any core file names a specific host). Run `python3 scripts/checks.py --all`.

## Common pitfalls

- Assuming the conductor can make a quick edit "just this once" -- it is read-only on source by design; even trivial edits route through the escape hatch documented in `agents/conductor.md`, not a silent exception.
- Treating a Skill's trigger description as optional detail -- on hosts that auto-invoke skills by description, a vague trigger means the skill never loads when it should.
- Adding host-specific language to a core agent, command, or core skill file -- this trips `G17_agnostic_core`. Host-specific detail belongs in `registries/hosts.json` or `adapters/`.

## Source map

- [`AGENTS.md`](../../AGENTS.md) -- governance doctrine and squad navigator.
- [`agents/conductor.md`](../../agents/conductor.md), [`agents/coder.md`](../../agents/coder.md), [`agents/discover.md`](../../agents/discover.md) -- the three role definitions.
- [`commands/`](../../commands/) -- the six phase workflows.
- [`skills/code-craft/SKILL.md`](../../skills/code-craft/SKILL.md), [`skills/harness-engineering/SKILL.md`](../../skills/harness-engineering/SKILL.md) -- the two most load-bearing core skills.
- [`scripts/checks.py`](../../scripts/checks.py) -- the 17 deterministic gates.

## Related docs

- [Multi-Host Install and Discovery](../flows/multi-host-install-and-discovery.md) -- how this system's artifacts reach a specific host.
- [ADR 0001 -- Native Per-Host Artifact Format](../architecture/decisions/0001-native-per-host-artifact-format.md) -- why agents/commands ship flat and skills ship nested.
- [Glossary](../glossary.md)
