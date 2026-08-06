---
status: Accepted
date: "2026-08-06"
---

# Ship Agents and Commands in Native Per-Host Format

## Context

The v3 rewrite needed to be compatible with popular coder-agent harnesses -- opencode, Claude Code, and kilo -- while staying agnostic of any single one of them. Research against each host's own docs (opencode agents/commands/skills, Claude Code sub-agents, kilo workflows, the skills.md standard, and the agents.md standard) surfaced a hard conflict:

- **opencode** discovers agents as **flat** `agents/<name>.md`; the filename *is* the identifier, and there is no `name`-field-based identity.
- **Claude Code** discovers agents as `<name>.md` (subdirectories are allowed but `name` in frontmatter is authoritative, not the path).
- **kilo** discovers commands ("workflows") as **flat** `commands/<name>.md` in its own commands dir, with no nested-file convention.
- The Agent Skills standard (skills.md) and both opencode and Claude Code agree that **skills** are **nested** `skills/<name>/SKILL.md`, one level deep.

The v3 draft initially shipped agents and commands as nested `<id>/SKILL.md` (matching skills' own shape, for internal consistency). That form is invisible to opencode's and kilo's flat scanners.

Capability gating also differs by host: Claude Code gates by a `tools` allowlist (tool names); opencode gates by a `permission` object (capability names, each `allow`/`ask`/`deny`). Neither host reads the other's field.

## Decision

Ship **agents/** and **commands/** flat -- `agents/<name>.md` and `commands/<name>.md` -- matching every researched host's native scan. Ship **skills/** nested -- `skills/<name>/SKILL.md` -- matching the Agent Skills standard and both hosts that implement it. Give every agent file a **cross-host frontmatter superset**: `name`, `description`, `mode`, plus both `tools` (for name-gated hosts) and `permission` (for capability-gated hosts) in the same file, so the read-only-vs-mutating boundary (`conductor`/`discover` vs `coder`) is enforced regardless of which field the host actually reads. Give every command file an `agent:` field binding it to the squad role it runs on. Keep `AGENTS.md` as plain, unadorned root Markdown -- the agents.md standard defines no schema, so no compatibility work was needed there.

Move the three domain-adapter skills (`go-essential`, `openapi-spec`, `confluence`) from a nested `skills/adapters/<id>/` location to top-level `skills/<id>/`, so every skill is exactly one level deep -- both opencode's and Claude Code's skill scanners only look one level deep, and the nested adapters location was invisible to them.

Keep the host list itself out of the core entirely: `registries/hosts.json` is the single source of truth for which hosts exist and what each surfaces, and the installer reads it rather than hardcoding a host table.

## Consequences

**Benefits:** every artifact is discoverable by its target host without a translation step at install time; no generator has to reshape files per host. The installer stays a thin symlink operation. Adding a ninth host is a registry entry, not a code or file-layout change.

**Costs:** agents and commands lost the internal-consistency benefit of matching skills' nested shape -- the repo now has two different artifact shapes (flat for agents/commands, nested for skills) rather than one uniform one. Agent frontmatter carries two capability-gating fields instead of one, which is redundant on any single host and must be kept in sync by hand.

**Risk accepted:** a host not yet researched (e.g. one of the "existing eight" adapters without a public agent/command schema -- codex, qwen, gemini, antigravity) gets the doctrine file via `AGENTS.md` but may not surface `agents/`/`commands/` natively; those hosts' `surfaces.agents` stays `false` in the registry until their schemas are confirmed.

## Alternatives considered

- **Keep bmad-style nested `<id>/SKILL.md` for agents and commands too**, and add a generator that flattens/reshapes per host at install time. Rejected: adds a second generator and a translation layer between source and what a host actually reads, for no benefit once flat is already native everywhere it needs to be.
- **Pick one host's format as canonical and treat the others as degraded.** Rejected: the ask was explicit compatibility with opencode, Claude Code, and kilo as first-class, not one as primary.
- **Single capability-gating field, host-specific translation at install time.** Rejected: adds install-time logic to reshape frontmatter per host; a static superset in the source file is simpler and lets any host read the file directly (e.g. via the marketplace/manifest path, which bypasses the installer).

## Related code

- [`agents/conductor.md`](../../../agents/conductor.md), [`agents/coder.md`](../../../agents/coder.md), [`agents/discover.md`](../../../agents/discover.md) -- `tools` + `permission` superset frontmatter.
- [`commands/`](../../../commands/) -- flat `<name>.md` files with `agent:` binding.
- [`skills/`](../../../skills/) -- nested `<name>/SKILL.md`, all ten skills one level deep.
- [`scripts/checks.py`](../../../scripts/checks.py) -- `G3`-`G5` validate the native shapes; `G17_agnostic_core` excludes the three domain adapters by design.

## Related docs

- [Coder Squad Core](../../systems/coder-squad-core.md)
- [Multi-Host Install and Discovery](../../flows/multi-host-install-and-discovery.md)
- [Glossary](../../glossary.md)
