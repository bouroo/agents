# Self-Organized Agent Configuration

[![Last commit](https://img.shields.io/github/last-commit/bouroo/agents?logo=github)](https://github.com/bouroo/agents)
[![Stars](https://img.shields.io/github/stars/bouroo/agents?logo=github)](https://github.com/bouroo/agents)
[![skills.sh](https://skills.sh/b/bouroo/agents)](https://skills.sh/b/bouroo/agents)
![Type](https://img.shields.io/badge/type-AI%20agent%20config-blue)
![Tools](https://img.shields.io/badge/tools-8-success)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](./LICENSE.md)

> Installable via the open Agent Skills ecosystem -- `npx skills add bouroo/agents` (see [skills.sh](https://skills.sh/b/bouroo/agents)) -- and via the bundled `adapters/install.sh` for filesystem-symlink installs.

A shared setup for AI coding assistants that is **agnostic of programming languages, agent frameworks, and host tools**. Drop one folder into your machine and eight different tools -- Gemini, Claude, OpenCode, Kilo, Codex, Qwen, and more -- pick up the same autonomous, self-improving coder-agent squad. The doctrine and its structure follow the [bmad-method](https://github.com/bmad-code-org/bmad-method) standards (persona agents, modular skills, reusable commands, single-source registries). No per-tool copy-paste, no drift between projects.

## Why use it

- **Agnostic core.** `AGENTS.md`, `agents/`, `command/`, and `skills/` contain no host-binding tokens and no language-bias doctrine. The `G17_agnostic_core` gate enforces it.
- **One squad, many tools.** A three-role coder squad (conductor / coder / discover) drives the THINK-ACT-PROVE-GROW loop; link it everywhere via one data-driven installer.
- **bmad-method structure.** Agents are persona artifacts; commands are reusable workflows; skills are modular capabilities; everything is declarative Markdown + frontmatter.
- **Hosts are data, not code.** Adding a tool is one entry in `registries/hosts.json` -- never a code change to the core.
- **Self-improving.** Every recurring failure becomes a deterministic gate (GROW); learnings persist on disk, not in the chat.

## Quick Start

Pick an install path. All three land the same artifacts.

### A. Agent Skills install (skills.sh)

The recommended cross-tool path: works with any Agent-Skills-compatible runtime (Claude Code, Cursor, Codex, OpenCode, Kilo, Gemini, Cline, Antigravity, AMP, Copilot, and 30+ others).

```bash
npx skills add bouroo/agents            # project-local (skills land in ./<agent>/skills/)
npx skills add bouroo/agents -g         # global (skills land in ~/<agent>/skills/)
npx skills add bouroo/agents --skill code-craft --skill harness-engineering
npx skills add bouroo/agents --list     # see everything the repo ships
```

Discovery is via the `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` manifests (Claude Code plugin marketplace format; honored by the `skills` CLI and any compatible runtime).

### B. Host plugin marketplaces

```bash
# Cursor
cursor plugin marketplace add bouroo/agents
cursor plugin install coder-agents@bouroo-coder-agents

# Gemini CLI
gemini extensions install https://github.com/bouroo/agents
```

Discovery is via `.cursor-plugin/*` (Cursor) and `gemini-extension.json` (Gemini) at the repo root.

### C. Symlink install (`adapters/install.sh`)

For the eight explicitly-targeted tools, the bundled installer symlinks `AGENTS.md`, `commands/`, `skills/`, and (where the host supports it) `agents/` into each tool's config directory. No Node.js required. The installer reads `registries/hosts.json` -- the host list is data, not code.

```bash
adapters/install.sh install            # link into every adapter (default)
adapters/install.sh status             # show linkage state
adapters/install.sh uninstall          # remove symlinks
adapters/install.sh list               # list adapters + target paths from the registry
adapters/install.sh install kilo       # filter to one adapter
adapters/install.sh install --dry-run  # preview without writing
adapters/install.sh install --force    # replace STALE links (use after a v2 -> v3 upgrade)

# Windows
./adapters/install.ps1 -Action install
./adapters/install.ps1 -Action status

# Backward-compat shim (link/unlink verbs)
adapters/link.sh            # = install.sh install
adapters/link.sh unlink     # = install.sh uninstall
```

Then restart your coding tool so it picks up the new config.

## What's inside

```
.
├── AGENTS.md                # Primary global governance agent: doctrine root + squad navigator
├── VERSION                  # Single version source (read by gen-manifests.py)
├── registries/              # Single-source-of-truth registries
│   ├── modules.json         # Module registry (core squad + optional domain adapters)
│   └── hosts.json           # Host-adapter registry (abstract contract + adapter instances)
├── agents/                  # Squad agent definitions -- flat <name>.md (native discovery)
│   ├── conductor.md         # primary orchestrator (read-only on source)
│   ├── coder.md             # subagent, mutating (implement/fix/verify/judge)
│   ├── discover.md          # subagent, read-only (explore/lookup/review)
│   └── <name>/references/   # progressive-disclosure depth per agent
├── commands/                # Standardized reusable workflows -- flat <name>.md
│   ├── document.md          # ACT/GROW -- bootstrap/sync a docs tree
│   ├── judge.md             # PROVE -- adversarial verification of "done"
│   ├── openapi.md           # ACT -- generate/validate an OpenAPI 3.2 contract
│   ├── refactor.md          # ACT -- analyze/plan/baseline/execute/verify a refactor
│   ├── review.md            # PROVE -- code review (MUST/SHOULD/NIT/SUGGESTION)
│   └── verify.md            # PROVE -- format/lint/type/test gate pipeline
├── skills/                  # Modular capability definitions -- nested <name>/SKILL.md
│   ├── code-craft/          # ten commandments + INTENT/TWINS/AUTH/PENDING gates
│   ├── harness-engineering/ # L1/L2/L3 termination, mutation testing, GROW
│   ├── memory-engineering/  # instruction vs learning memory
│   ├── spec-driven-development/
│   ├── performance-patterns/
│   ├── repo-documentation/
│   ├── commit-message/
│   ├── go-essential/        # domain adapter -- Go language doctrine
│   ├── openapi-spec/        # domain adapter -- OpenAPI 3.2 (backs commands/openapi)
│   └── confluence/          # domain adapter -- Atlassian Confluence via mcp-atlassian
├── adapters/                # Distribution layer (segregated from the agnostic core)
│   ├── install.sh           # reads registries/hosts.json; no hardcoded tool list
│   ├── install.ps1          # Windows companion
│   ├── link.sh              # backward-compat shim -> install.sh
│   └── manifests/           # generated per-host plugin manifests (source of truth)
│       ├── claude/  cursor/  gemini/  legacy/
├── .claude-plugin/          # discovery symlinks -> adapters/manifests/claude/
├── .cursor-plugin/          # discovery symlinks -> adapters/manifests/cursor/
├── gemini-extension.json    # discovery symlink -> adapters/manifests/gemini/
├── plugin.json              # discovery symlink -> adapters/manifests/legacy/plugin.json
├── marketplace.json         # discovery symlink -> adapters/manifests/legacy/marketplace.json
├── scripts/
│   ├── checks.py            # 17 deterministic gates (count via `checks.py --list`)
│   ├── gen-manifests.py     # generates adapters/manifests/ from VERSION + inventory + registries
│   ├── resolve-customization.py  # three-tier customize.toml merge (optional)
│   └── validate-agents.sh   # thin shim -> checks.py
├── docs/                    # Repo-local docs (systems, flows, ADRs, glossary)
│   └── README.md            # index: explains the layout
└── eval/                    # Honesty layer: scenario seeds + null-committed results
```

> **Manifest layout.** Host plugin manifests live canonically under `adapters/manifests/<host>/` and are surfaced at their tool-discovery paths (`.claude-plugin/`, `.cursor-plugin/`, `gemini-extension.json`, root `plugin.json`/`marketplace.json`) via symlinks. `G13_plugin_symlinks` enforces the contract; `G15_manifests_generated` regenerates from `VERSION` + inventory + registries and fails on drift. The host list itself comes from `registries/hosts.json` -- `G16_registries_parse` validates both registries.

### The squad

The governance `AGENTS.md` routes to a three-role **coder squad**:

| Agent | Mode | Role |
|---|---|---|
| [conductor](agents/conductor.md) | primary | Orchestrator. Decomposes work into a unit graph, delegates complete packets, audits evidence, converges, and self-improves the harness. Read-only on source. |
| [coder](agents/coder.md) | subagent | Mutating worker. Modes: implement / fix / verify / judge. Edits within SCOPE, runs the toolchain, captures executable evidence, adversarially judges claims. |
| [discover](agents/discover.md) | subagent | Read-only worker. Modes: explore / lookup / review. Never mutates source, never runs the toolchain. |

The load-bearing safety split is **mutating vs read-only**: only `coder` touches source. Each agent file carries a cross-host frontmatter superset -- `name`, `description`, `mode`, plus `tools` (name-gated hosts) and `permission` (capability-gated hosts) -- so the read-only/mutating boundary is enforced on every host.

### Commands

Six phase commands drive the THINK-ACT-PROVE-GROW loop: [document](commands/document.md) (ACT/GROW), [judge](commands/judge.md) (PROVE), [openapi](commands/openapi.md) (ACT), [refactor](commands/refactor.md) (ACT), [review](commands/review.md) (PROVE), [verify](commands/verify.md) (PROVE). Each carries `description` + `agent` (the worker it binds to) + `phase` frontmatter, When/Inputs/Steps, and executable Success/Failure metrics.

### Skills

| Skill | Use when |
|---|---|
| [code-craft](skills/code-craft/SKILL.md) | Writing, reviewing, or refactoring code for clarity, safety, testability, efficiency; artifact gates |
| [harness-engineering](skills/harness-engineering/SKILL.md) | Configuring agent controls, verifying work, establishing reliability; L1/L2/L3, mutation testing, GROW |
| [memory-engineering](skills/memory-engineering/SKILL.md) | Persisting cross-session learnings, configuring agent memory |
| [spec-driven-development](skills/spec-driven-development/SKILL.md) | Starting a feature, drafting requirements, resolving ambiguity |
| [performance-patterns](skills/performance-patterns/SKILL.md) | Profiling, optimizing a measured hot path |
| [repo-documentation](skills/repo-documentation/SKILL.md) | A behavior/interface/invariant/domain-term change needs documenting |
| [commit-message](skills/commit-message/SKILL.md) | Writing a commit message from staged changes |
| [go-essential](skills/go-essential/SKILL.md) | Writing, refactoring, or reviewing Go code |
| [openapi-spec](skills/openapi-spec/SKILL.md) | Producing or repairing an OpenAPI 3.2 contract |
| [confluence](skills/confluence/SKILL.md) | Operating Confluence via the mcp-atlassian bridge |

### Native harness compatibility

The artifacts ship in each harness's **native** discovery format, verified against the official docs:

| Artifact | Format | Compatible harnesses |
|---|---|---|
| **Agents** `agents/<name>.md` | flat `<name>.md`; frontmatter superset (`name`, `description`, `mode`, `tools`, `permission`) | opencode, Claude Code (`.claude/agents/`), kilo (`agent/`) |
| **Commands** `commands/<name>.md` | flat `<name>.md`; `description` + `agent` binding | opencode, kilo (`.kilo/commands/`), Claude Code |
| **Skills** `skills/<name>/SKILL.md` | nested per the Agent Skills standard; `name` + `description` | skills.md / opencode / Claude Code |
| **AGENTS.md** | root Markdown, nearest-wins | the open AGENTS.md standard (Codex, Cursor, Gemini, opencode, kilo, and 20+ others) |

The installer (`adapters/install.sh`, reads `registries/hosts.json`) symlinks the doctrine as each host's config file and links `agents/` + `commands/` where the host surfaces them.

### Verification

`scripts/checks.py` runs 17 deterministic gates (`--list` to see them; `--all` to run every gate). CI runs `python3 scripts/checks.py --all` on every push. Notable gates: `G13_plugin_symlinks`, `G15_manifests_generated`, `G16_registries_parse`, `G17_agnostic_core`.

## Upgrading from v2

v3 is a **breaking** restructure for filesystem consumers; the doctrine is continuous. Key changes:

- Artifacts now ship in **native harness format**: flat `agents/<name>.md` and `commands/<name>.md` (was nested `*/SKILL.md`). Run `adapters/install.sh install --force` to refresh links -- the installer detects STALE v2 symlinks and refuses to clobber real files without `--force`.
- `effective-code-craft` -> `code-craft`. The three language/tool skills are top-level: `skills/go-essential`, `skills/openapi-spec`, `skills/confluence` (was under `skills/adapters/`).
- `.agents/plugins/` -> `adapters/manifests/`; root installer -> `adapters/`.
- Agent frontmatter gained `tools` + `permission` so the read-only/mutating boundary is enforced on every host.

See [CHANGELOG.md](./CHANGELOG.md) for the full v3.0.0 entry. v2 content is preserved in git history.

## References

- [bmad-method](https://github.com/bmad-code-org/bmad-method) -- the structural standards this repo adheres to (persona agents, modular skills, reusable commands, single-source registries).
- [Agent Skills Specification](https://agentskills.io/specification) -- the open `SKILL.md` format this repo conforms to.
- [skills.sh](https://skills.sh) -- open skills leaderboard and `npx skills` CLI.
- [Claude Code Plugin Marketplace](https://code.claude.com/docs/en/plugin-marketplaces) -- `.claude-plugin/` format.
- [Cursor Plugin Specification](https://github.com/cursor/plugins) -- `.cursor-plugin/` schema.
- [Gemini CLI Extensions](https://geminicli.com/docs/extensions/reference/) -- `gemini-extension.json` format.
