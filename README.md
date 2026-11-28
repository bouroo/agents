# coder-agents

A lean shared setup for autonomous coding agents — agnostic of programming languages, agent frameworks, and host tools. One entry point ([`AGENTS.md`](AGENTS.md)) carries the working loop and four decision-point gates; six skills load on demand.

## How it works

- **One source of truth.** `AGENTS.md` holds the doctrine: intake, the work loop, checks, parallelism, memory discipline, sessions, unattended runs. Host-specific files (e.g. `CLAUDE.md`) just point at it.
- **Four forced lines at decision points.** `ASK:` before the first edit, `INTENT:` before a behavior-changing edit, `AUTH:` before any outward/irreversible effect, `OWED:` closing every report.
- **Skills load on demand.** Names and triggers live in the entry point; bodies load only when the trigger holds, so procedures stay out of the always-loaded context.
- **Scope precedence.** Organization → project → personal: the closest instruction file wins on conflict.

## Repository layout

```
AGENTS.md                  # the entry point (doctrine)
CLAUDE.md                  # pointer: @AGENTS.md
skills/                    # on-demand skills, one directory each
  plan/  verify/  review/  refactor/  skill-creation/  swe/
scripts/install.sh         # host-aware installer (the only host-specific code)
.claude-plugin/            # Claude Code plugin + marketplace manifests
.cursor-plugin/            # Cursor plugin + marketplace manifests
.minimax-plugin/           # MiniMax plugin manifest
gemini-extension.json      # Gemini CLI extension manifest
```

## Skills

| Skill | Trigger |
| --- | --- |
| `plan` | Scope is ambiguous, an action is irreversible or outward-facing, or a plan was requested. Interviews the user, writes the plan artifact, stops for approval. |
| `verify` | Before claiming work done, or judging any completion claim. Runs checks and reads outputs; never trusts a report alone. |
| `review` | A diff is written and someone must decide whether it merges. Read-only judgment by severity, one verdict. |
| `refactor` | Behavior-preserving restructuring of correct-but-unclear, unsafe, or slow code. Not for new features. |
| `skill-creation` | Creating a new skill or revising an existing one after real runs expose gaps. |
| `swe` | Craft best practices for writing/reviewing/refactoring code in any language: clarity, errors, security, resources, concurrency, tests, idiom currency, and unslopping AI-generated code/text/UI. |

## Install

### Script (any supported host)

```sh
git clone https://github.com/bouroo/agents.git
cd agents
./scripts/install.sh detect     # show compatible tools found on this machine
./scripts/install.sh install    # install into every detected tool
```

The installer symlinks `AGENTS.md` (renamed per host) and each skill directory into the host's config dir, so updates in this repo propagate to every tool. Real files are never clobbered.

| Command | Effect |
| --- | --- |
| `detect` | List detected tools |
| `list` | List every supported tool |
| `install [<code>...]` | Install (default: all detected tools) |
| `uninstall [<code>...]` | Remove installed symlinks (real files need `--force`) |
| `status` | State of every artifact on every tool |

Options: `--all` (include undetected tools), `--copy` (copy instead of symlink), `--force` (replace foreign links / refresh copies), `--dry-run`.

Supported hosts: `gemini`, `codex`, `claude`, `qwen`, `opencode`, `kilo`, `openclaw`, `hermes`, `pi`, `omp`, `minimax`. Adding a harness is one line in the script's `HOSTS` table.

### Plugin / extension

- **Claude Code:** `/plugin marketplace add bouroo/agents`, then `/plugin install coder-agents@bouroo-agents`
- **Gemini CLI:** `gemini extensions install https://github.com/bouroo/agents`
- **Cursor / MiniMax:** manifests ship in `.cursor-plugin/` and `.minimax-plugin/`

## License

[Apache-2.0](LICENSE.md)
