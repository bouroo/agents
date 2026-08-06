# Glossary

Title Case terms used across this repo's docs, agents, commands, and skills. Add a term here the first time it is introduced in a doc.

## Terms

**Coder Squad** -- the three-role agent team this repo governs: [conductor](../agents/conductor.md) (primary, read-only orchestrator), [coder](../agents/coder.md) (mutating worker), [discover](../agents/discover.md) (read-only worker). See [Coder Squad Core](systems/coder-squad-core.md).

**Governance Agent** -- the role `AGENTS.md` plays: doctrine root and squad navigator, loaded by every host as its global system prompt.

**Host Adapter** -- a self-describing entry in `registries/hosts.json` (e.g. `claude`, `opencode`, `kilo`) that tells the installer where and how to link this repo's artifacts into one AI coding tool's config directory. See [Multi-Host Install and Discovery](flows/multi-host-install-and-discovery.md).

**Native Discovery Format** -- the exact file layout and frontmatter shape a given host scans for on disk (e.g. flat `agents/<name>.md` for opencode/Claude Code, nested `skills/<name>/SKILL.md` for the Agent Skills standard). See [ADR: Ship Agents and Commands in Native Per-Host Format](architecture/decisions/0001-native-per-host-artifact-format.md).

**Domain Adapter** -- an optional, non-agnostic skill that names a specific language or tool (`go-essential`, `openapi-spec`, `confluence`), excluded from the `G17_agnostic_core` gate.

**Artifact Gates** -- the four forced report lines owed at decision points: `INTENT:`, `TWINS:`, `AUTH:`, `PENDING:`. Defined in [code-craft](../skills/code-craft/SKILL.md).

**THINK-ACT-PROVE-GROW Loop** -- the four-phase operating loop every squad task moves through, defined in `AGENTS.md` §4.
