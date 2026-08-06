# docs/

Explains how this repo's shipped configuration works, for a reader who has never seen it before. Source (`AGENTS.md`, `agents/`, `commands/`, `skills/`, `registries/`, `adapters/`, `scripts/`) is the implementation source of truth; this tree explains *why* it's shaped this way, *when* each piece applies, and *what can go wrong*. See [repo-documentation](../skills/repo-documentation/SKILL.md) for the doctrine that governs this tree.

## Layout

| Directory | Holds |
|---|---|
| `systems/` | One doc per system -- a cohesive piece of runtime behavior (e.g. the coder squad, the multi-host distribution layer) |
| `flows/` | One doc per flow that crosses systems (e.g. installing into a host, generating manifests) |
| `architecture/decisions/` | ADRs -- durable decisions and the alternatives considered |
| `templates/` | Copies of the `repo-documentation` skill's templates, customizable per this repo |
| `glossary.md` | Title Case terms used across this repo's docs |

**Granularity rule:** start with a system doc; promote to a flow doc only once the behavior genuinely crosses systems (e.g. "install into a host" touches the host-adapter registry, the installer, and the target host's config dir).

## Current docs

- **Systems:** [Coder Squad Core](systems/coder-squad-core.md)
- **Flows:** [Multi-Host Install and Discovery](flows/multi-host-install-and-discovery.md)
- **ADRs:** [0001 -- Ship Agents and Commands in Native Per-Host Format](architecture/decisions/0001-native-per-host-artifact-format.md)
- **Glossary:** [glossary.md](glossary.md)

## Keeping this tree in sync

Docs are part of the diff. A change touching system behavior, the artifact contract, host discovery, or a glossary term updates the affected doc in the same change -- see the [document](../commands/document.md) command. A stale doc is a bug, not a nice-to-have.
