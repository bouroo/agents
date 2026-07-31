# Self-Organized Agent Configuration

[![Last commit](https://img.shields.io/github/last-commit/bouroo/agents?logo=github)](https://github.com/bouroo/agents)
[![Stars](https://img.shields.io/github/stars/bouroo/agents?logo=github)](https://github.com/bouroo/agents)
[![skills.sh](https://skills.sh/b/bouroo/agents)](https://skills.sh/bouroo/agents)
![Type](https://img.shields.io/badge/type-AI%20agent%20config-blue)
![Tools](https://img.shields.io/badge/tools-8-success)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](./LICENSE.md)

> Installable via the open Agent Skills ecosystem -- `npx skills add bouroo/agents` (see [skills.sh](https://skills.sh/bouroo/agents)) -- and via the bundled `link.sh` / `install.sh` for filesystem-symlink installs.

A shared, language-agnostic setup for AI coding assistants. Drop one folder into your machine and eight different tools  --  Gemini, Claude, OpenCode, Kilo, Codex, Qwen, and more  --  pick up the same global coding standards, slash commands, and reusable skills. No per-tool copy-paste, no drift between projects.

## Why use it

- **One config, many tools**  --  write the rules once; link it everywhere via a single script.
- **Coding standards baked in**  --  global guidelines live in `AGENTS.md` and are followed by every tool.
- **On-demand skills**  --  focused modules (commit messages, code craft, performance, harness design, specs) load only when you need them.
- **Slash commands**  --  run repeatable workflows like refactor / review / verify with one command.
- **One-command install**  --  `link.sh` handles the symlinks; `link.sh status` tells you what's linked.

## Quick Start

Pick one of the two install paths. Both land the same artifacts.

### A. Agent Skills install (skills.sh / Claude Code plugin format)

The recommended cross-tool path: works with any Agent-Skills-compatible runtime (Claude Code, Cursor, Codex, OpenCode, Kilo, Gemini, Cline, Antigravity, AMP, Copilot, and 30+ others).

```bash
# Project-local install (default): skills land in ./<agent>/skills/
npx skills add bouroo/agents

# Global install: skills land in ~/<agent>/skills/
npx skills add bouroo/agents -g

# Pick specific skills
npx skills add bouroo/agents --skill effective-code-craft --skill harness-engineering

# Install specific skills to specific agents only
npx skills add bouroo/agents -a claude-code -a opencode --skill harness-engineering -y

# List everything the repo ships before installing
npx skills add bouroo/agents --list
```

Discovery is via the `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` manifests in this repo (the Claude Code plugin marketplace format; honored by the `skills` CLI and any compatible runtime).

### B. Cursor plugin marketplace install

```bash
# Add the marketplace (one-time)
cursor plugin marketplace add bouroo/agents

# Install the plugin
cursor plugin install coder-agents@bouroo-coder-agents
```

Discovery is via `.cursor-plugin/plugin.json` and `.cursor-plugin/marketplace.json` per the [cursor/plugins](https://github.com/cursor/plugins) schema.

### C. Gemini CLI extension install

```bash
gemini extensions install https://github.com/bouroo/agents
```

Discovery is via `gemini-extension.json` at the repo root. Skills load from `skills/`, slash commands from `commands/`, and the conductor sub-agent from `agents/`. Update with `gemini extensions update coder-agents`.

### D. Symlink install (`link.sh` / `install.sh`)

For the eight explicitly-targeted tools (Gemini, antigravity, Codex, Claude, Qwen, OpenCode, Kilo), the bundled installer symlinks `AGENTS.md`, `commands/`, `skills/`, and `agents/` into each tool's config directory. No Node.js required. `link.sh` is now a thin backward-compat shim that execs `install.sh` -- the only thing it does is translate the legacy verbs (`link` -> `install`, `unlink` -> `uninstall`) and forward everything else (tool filters, `--dry-run`, `--force`, `--help`) verbatim. The two are interchangeable; pick whichever verb set you remember.

```bash
# install.sh vocabulary (canonical)
~/.agents/install.sh install           # link into every detected tool (default)
~/.agents/install.sh status            # show linkage state
~/.agents/install.sh uninstall         # remove symlinks
~/.agents/install.sh list              # list detected tools + target paths
~/.agents/install.sh install kilo      # filter to a single tool
~/.agents/install.sh install --dry-run # preview without writing

# link.sh vocabulary (shim, backward-compat)
~/.agents/link.sh                      # = install.sh install
~/.agents/link.sh status               # = install.sh status
~/.agents/link.sh unlink               # = install.sh uninstall
~/.agents/link.sh link opencode        # = install.sh install opencode
```

Then restart your coding tool so it picks up the new config.

## What's inside

```
~/.agents/
├── AGENTS.md                # Global coding standards and workflow router
├── README.md                # This file
├── link.sh                  # Backward-compat shim that execs install.sh (verb translation only)
├── install.sh               # The installer: links AGENTS.md, commands/, skills/, agents/ into every supported tool
├── .agents/plugins/         # Source-of-truth plugin manifests (one subdir per tool)
│   ├── claude/
│   │   ├── plugin.json      # Claude Code plugin manifest (skills.sh discovery)
│   │   └── marketplace.json # Multi-plugin catalog (skills.sh discovery)
│   ├── cursor/
│   │   ├── plugin.json      # Cursor plugin manifest (Cursor marketplace)
│   │   └── marketplace.json # Cursor marketplace catalog
│   ├── gemini/
│   │   └── gemini-extension.json  # Gemini CLI extension manifest
│   └── legacy/
│       ├── plugin.json      # OpenCode/Kilo plugin manifest (legacy path)
│       └── marketplace.json # OpenCode/Kilo marketplace (legacy path)
├── .claude-plugin/          # Symlinks -> .agents/plugins/claude/* (Claude Code auto-discovery)
├── .cursor-plugin/          # Symlinks -> .agents/plugins/cursor/* (Cursor auto-discovery)
├── gemini-extension.json   # Symlink -> .agents/plugins/gemini/gemini-extension.json
├── plugin.json              # Symlink -> .agents/plugins/legacy/plugin.json
├── marketplace.json         # Symlink -> .agents/plugins/legacy/marketplace.json
├── agents/                  # Orchestrator agents (mode, permissions, prompt)
│   ├── coder.md             # Mutating subagent -- implements, fixes, verifies, and judges
│   ├── conductor.md         # Decisive orchestrator -- chooses best practice, records assumption, proceeds
│   └── discover.md          # Read-only subagent -- plans, explores, looks up, and reviews
├── commands/                # Slash commands (reusable prompt workflows)
│   ├── document-phase.md
│   ├── judge-phase.md
│   ├── openapi-phase.md
│   ├── refactor-phase.md
│   ├── review-phase.md
│   └── verify-phase.md
├── skills/                  # On-demand skill modules (load via the skill tool)
│   ├── commit-message/
│   ├── effective-code-craft/
│   ├── go-essential/
│   ├── harness-engineering/
│   ├── openapi-spec/
│   ├── performance-patterns/
│   ├── repo-documentation/
│   └── spec-driven-development/
├── scripts/
│   ├── checks.py            # Repo validator (deterministic gates; count via `checks.py --help`)
│   ├── gen-manifests.py     # Generates host manifests from VERSION + disk inventory (single source of truth)
│   └── validate-agents.sh   # Thin shim that execs checks.py (preserves the documented entrypoint)
└── .agents/                 # Per-project runtime dir (plans/, handoff/ created on use IN THE TARGET
                             # PROJECT, never in this repo; gitignored here except .agents/plugins/)
    ├── plans/               # Spec drafts, REASONS canvases, plan trackers, retros
    └── handoff/             # Subagent reports and summaries
```

> **Manifest layout.** Tool-specific plugin manifests live canonically under `.agents/plugins/<tool>/` and are surfaced at their tool-discovery paths (`.claude-plugin/`, `.cursor-plugin/`, `gemini-extension.json`, root `plugin.json`/`marketplace.json`) via symlinks. The `G13_plugin_symlinks` gate in `scripts/checks.py` enforces this contract so a future edit at the discovery path cannot silently fork from the source of truth. The manifests themselves are generated from `VERSION` plus the on-disk skill/command/agent inventory by `scripts/gen-manifests.py`; the `G15_manifests_generated` gate fails if any checked-in manifest drifts from generated output, so the inventory and version can never drift across the four host formats.

### Agents

Orchestrators that think, dispatch, and verify  --  they delegate code edits by default (a narrow trivial-work escape hatch lets the conductor fix a typo or rename directly).

| Agent | Mode | Purpose |
|----------------|---------|------------------------------------------------------------------------------------------|
| `conductor` | primary | Self-organizing orchestrator. Owns Plan Mode (unit-graph decomposition, `done_cmd`, `INTENT:` gate, writes `canvas.md`/`state.json` under `.agents/`), delegates to subagents, validates outcomes, and steers its own harness. Decisive: chooses the industry-standard option, records the assumption, and proceeds. Delegates execution by default; a narrow trivial-work escape hatch lets it apply a one-line fix (typo, rename) directly when self-verification still holds. |
| `coder` | subagent | Mutating specialist. Implements source changes, fixes narrow bugs with a repro, runs L1/L2/L3 verification and the mutation probe, and delivers adversarial VERIFIED / CAVEATS / REFUTED judgments. Owns its own permissive `edit`/`bash` permission block. |
| `discover` | subagent | Read-only specialist. Consolidates Explorer / Scout / Reviewer into explore, lookup, and review modes. Never edits source or runs the toolchain; writes only under `.agents/**`. Issues the fixed seven-grade review rubric. |

The conductor is non-coding by default: it plans, dispatches, verifies, and steers through the two named subagents (`coder` for mutation and toolchain, `discover` for exploration, external lookup, and read-only review). A narrow trivial-work escape hatch lets it apply a one-line fix (typo, rename) directly when self-verification still holds. It shares canonical Convergence Gates and On-Disk State (see [skills/harness-engineering/SKILL.md](skills/harness-engineering/SKILL.md) Appendix A & B).

### Commands

Reusable prompt workflows you trigger with a slash command.

| Command | Description |
|--------------------|----------------------------------------------------------------------|
| `document-phase` | Document phase  --  bootstrap repo docs or sync docs/ with code changes |
| `openapi-phase` | OpenAPI phase  --  generate or update docs/openapi.yaml (OpenAPI 3.2) from API code or requirements and validate it against the canonical OAS meta-schema |
| `refactor-phase` | Refactor phase  --  analyze, plan, baseline, execute, verify |
| `review-phase` | Review phase  --  review code changes for correctness, safety, performance |
| `verify-phase` | Verify phase  --  format, lint, type-check, scan, test, githook gate |
| `judge-phase` | Judge phase  --  adversarial verification of finished work; treats "done" as claims, re-runs verifications, hunts frauds, delivers VERIFIED / CAVEATS / REFUTED |

### Skills

Focused modules the agent loads on demand when a task matches. Each ships a terse `SKILL.md` and, where depth is needed, a sibling `references/` tree loaded lazily by explicit "load when" hints (progressive disclosure per the [Agent Skills best-practices](https://agentskills.io/skill-creation/best-practices)).

| Skill | Trigger |
|-----------------------------|------------------------------------------------------------------------------------------|
| `effective-code-craft` | Writing, reviewing, or refactoring code for clarity, safety, testability, or efficiency  |
| `go-essential` | Writing, refactoring, or reviewing Go (Golang) code: error handling, naming, concurrency, context, testing, performance  |
| `harness-engineering` | Designing agent workflows, checkpoints, verification rules, or orchestrator agents; lifecycle controls; preventing overreach, premature victory, or context loss |
| `memory-engineering` | Persisting cross-session learnings, configuring agent memory, or deciding where memory artifacts live (Instruction vs. Learning separation; the `.agents/memory/` fallback) |
| `openapi-spec` | Generating or repairing an OpenAPI 3.2 contract into docs/openapi.yaml and validating it against the canonical OAS meta-schema |
| `performance-patterns` | Optimizing for speed, throughput, latency, or memory after correctness is proven |
| `repo-documentation` | Repo keeps a `docs/` tree and a behavior/interface/invariant/domain-term change must update the affected doc in the same change |
| `spec-driven-development` | Starting new features, resolving ambiguous requirements, bridging intent to implementation |
| `commit-message` | Generating a conventional commit message from staged changes |

## Compatibility

This repo is installable through three ecosystems that share the same [Agent Skills](https://agentskills.io/specification) format. All plugin manifests live canonically under `.agents/plugins/<tool>/` and are surfaced at their tool-discovery paths via symlinks (enforced by the `G13_plugin_symlinks` gate).

| Install path | Mechanism | Tools reached |
|---|---|---|
| **`npx skills add bouroo/agents`** ([skills.sh](https://skills.sh)) | `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` (the Claude Code plugin marketplace format, honored by the `skills` CLI) | Claude Code, Cursor, Codex, OpenCode, Kilo Code, Cline, GitHub Copilot, Antigravity, AMP, Gemini CLI, Roo, Goose, Continue, and 30+ more. Full list at [skills.sh/docs/cli](https://skills.sh/docs/cli). |
| **Cursor plugin marketplace** | `.cursor-plugin/plugin.json` + `.cursor-plugin/marketplace.json` per the [cursor/plugins](https://github.com/cursor/plugins) schema | Cursor (IDE + CLI). |
| **Gemini CLI extension** | `gemini-extension.json` at repo root, installed via `gemini extensions install https://github.com/bouroo/agents` | Gemini CLI (and Antigravity CLI). Skills load from `skills/`; commands from `commands/`; sub-agents from `agents/`. |
| **`link.sh` / `install.sh`** (this repo) | Symlink `AGENTS.md`, `commands/`, `skills/`, `agents/` into each tool's config dir | Gemini + antigravity (`~/.gemini/`), Codex (`~/.codex/`), Claude (`~/.claude/`), Qwen (`~/.qwen/`), OpenCode (`~/.config/opencode/`), Kilo (`~/.config/kilo/`). |
| **Manual copy** | Copy `skills/<name>/` into the target tool's skill discovery path | Any Agent-Skills-compatible runtime. See [skill discovery paths](https://skills.sh/docs/cli). |

The skills themselves are pure markdown (`SKILL.md` + optional `references/`) with YAML frontmatter -- they load in any compliant runtime. The `conductor` agent and `commands/` are OpenCode/Kilo-native and only land when the runtime has an agents concept.

## Supported Tools (symlink install)

`link.sh` / `install.sh` symlink four artifacts into each tool's config directory.

| Artifact | Source | Linked as | Notes |
|---------------|-------------------|-------------------|--------------------------------|
| Config file | `AGENTS.md` | Tool-specific name| `GEMINI.md`, `CLAUDE.md`, or `AGENTS.md` |
| Commands | `commands/` | `commands/` | All tools |
| Skills | `skills/` | `skills/` | All tools |
| Agents | `agents/` | Tool-specific dir | Only OpenCode (`agents/`) and Kilo (`agent/`) |

| Tool | Config Location | Config File  | Agents Dir  |
|------------|--------------------------|--------------|-------------|
| Gemini | `~/.gemini/` | `GEMINI.md`  |  -- |
| antigravity | `~/.gemini/` | `GEMINI.md`  |  -- |
| antigravity-ide | `~/.gemini/` | `GEMINI.md`  |  -- |
| Codex | `~/.codex/` | `AGENTS.md`  |  -- |
| Claude | `~/.claude/` | `CLAUDE.md`  |  -- |
| Qwen | `~/.qwen/` | `AGENTS.md`  |  -- |
| OpenCode | `~/.config/opencode/` | `AGENTS.md`  | `agents/` |
| Kilo | `~/.config/kilo/` | `AGENTS.md`  | `agent/` |

## How it works

Everything in this repo is plain markdown  --  the symlinks make it look like each tool's own config directory contains the same rules, commands, and skills. `AGENTS.md` is intentionally short: it's a router that points the agent at the right skill or command on demand instead of dumping every rule into one giant prompt. Adding a new tool is a matter of adding a target to `link.sh`; updating the rules means editing one file, and every linked tool picks up the change.

## Methodology

### THINK→ACT→PROVE→GROW Loop

The core operational loop is grounded in the Fable Method:
- **THINK (discover):** Classify the ask, define done conditions, gather context and executable evidence, plan testable units.
- **ACT (coder):** Surgical implementation within explicit SCOPE bounds, one unit at a time.
- **PROVE (coder verify + discover review):** Three-layer verification (L1 static, L2 runtime, L3 end-to-end), mutation test probe, and adversarial judgment  --  **dialed to job complexity** via the [right-sizing map](skills/harness-engineering/references/right-sizing.md) (a typo does not need the full apparatus).
- **GROW (self-improving harness):** Catalog failure modes in retro logs, build deterministic gates from recurring failures, and continuously improve the surrounding harness system.

### Harness Engineering

These configs embody the harness-engineering canon, not merely reference it: the repo is the operational record of truth; instructions are split into focused, agent-loadable modules; WIP is one verified task at a time; completion requires executable evidence; verification is dialed to the task's complexity  --  right-sized, not universal (see the right-sizing map); and state persists across sessions via explicit clock-in/out checklists.

The `harness-engineering` skill adds the design vocabulary for *building* these controls  --  feedforward **guides** vs feedback **sensors**, **computational** vs **inferential** controls  --  and the disciplines that keep agent output trustworthy: **gates enforce**, **separate reasoning from computation**, **grade the tests** (mutation testing  --  an agent-authored green suite is a signal, not proof), and **engineer the whole lifecycle** (improve the harness, not the prompt; deliberate friction is leverage). It also carries the **right-sizing** discipline  --  dial controls to the job's complexity, and refuse the Average Answer Trap (every control on every task) and the Kirby Effect (controls that encode obsolete model limits). Norms + clock-in/out checklist: [skills/harness-engineering/SKILL.md](skills/harness-engineering/SKILL.md).

### SPDD Methodology

```
Story → Analysis → Canvas → Generate → Test → Review → Sync
  ↑                                                      |
  └────────────── repeat until aligned ──────────────────┘
```

The workflow is phased to keep each review checkpoint small enough to engage with (cognitive load, not ceremony): validate behavior at the system boundary early, review code only once it works, and generate unit tests last as a regression net. See [skills/spec-driven-development/SKILL.md](skills/spec-driven-development/SKILL.md) for the fitness table  --  when to spec, and when not to.

## OpenCode Format Mapping

> **Reference for contributors and portability.** This section explains how the repo's artifacts map to the [opencode](https://opencode.ai/docs/) format so the config loads natively across tools.

This repo follows the [opencode](https://opencode.ai/docs/) artifact format so it loads natively when `link.sh` symlinks `commands/`, `skills/`, and `agents/` into `~/.config/opencode/`. OpenCode auto-discovers all three directories; no `opencode.json` is required.

| Artifact | File | Recognized frontmatter | Notes |
|---|---|---|---|
| Rules | `AGENTS.md` | (none  --  plain markdown) | Read as global rules from `~/.config/opencode/AGENTS.md`. Keep it a router; load detail from skills. |
| Agent | `agents/*.md` | `description` (req), `mode`, `temperature`, `steps`, `model`, `prompt`, `permission`, `hidden`, `color`, `top_p` | `permission` keys: `read edit glob grep list bash task external_directory todowrite webfetch websearch lsp skill question doom_loop`  --  each `allow\|ask\|deny` or a glob→action object. `tools` is deprecated; use `permission`. |
| Command | `commands/*.md` | `description` (req), `agent`, `subtask`, `model` | Body is the prompt template. Supports `$ARGUMENTS`, `$1`/`$2`/…, `` !`cmd` `` shell injection, `@file` references. |
| Skill | `skills/<name>/SKILL.md` | `name` (req, must equal dir, `^[a-z0-9]+(-[a-z0-9]+)*$`), `description` (req, 1-1024 chars), `license`, `compatibility`, `metadata` | Unknown fields (e.g. Kilo's `disable-model-invocation`) are ignored by opencode and kept for portability. Loaded on demand via the `skill` tool. |

**Discovery paths (global):** `~/.config/opencode/{AGENTS.md, agents/, commands/, skills/}`. Claude-compatible fallbacks (`CLAUDE.md`, `~/.claude/skills/`, `.agents/skills/`) are also honored. Skills are also discovered from `~/.agents/skills/*/SKILL.md`.

**Optional `opencode.json`** (not shipped  --  the repo stays tool-neutral):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": ["docs/guidelines.md", ".cursor/rules/*.md"],
  "references": {
 "sdk": { "repository": "owner/repo", "description": "Use for SDK implementation details" }
  },
  "compaction": {
 "auto": true,
 "prune": false,
 "reserved": 10000
  },
  "agent": {
 "conductor": { "model": "anthropic/claude-sonnet-4-5" }
  },
  "provider": {
 "anthropic": { "options": { "apiKey": "{env:ANTHROPIC_API_KEY}" } }
  }
}
```

- `instructions`  --  array of paths/globs to instruction files; lazily loaded, not eagerly expanded.
- `references`  --  map of named reference repos the agent can consult for external context.
- `compaction`  --  `{ auto, prune, reserved }`; controls context compaction behavior (auto-compact when full, prune old tool outputs, reserve a token buffer).
- `agent`  --  per-agent model/permission overrides; custom agents also load from `agents/*.md`.
- `provider`  --  provider config; supports `{env:VAR}` and `{file:path}` variable substitution.

### Context Management

**AGENTS.md is a router, not a dump.** Keep global rules terse; load detail from skills on demand (Kilo: "Keep custom instructions concise and actionable"; OpenCode: lazy-load instructions). **Semantic codebase index.** When the host tool offers semantic/code search (e.g. Kilo "Codebase Indexing"), prefer it over broad string-search fan-out for unfamiliar surfaces -- but route by capability, never by a tool name borrowed from another host. **Context condensing discipline.** Long sessions auto-compact; put the next executable action and current blocker in the latest turn or a tracked file, because the verbatim tail is what survives (Kilo: "Context Condensing"; OpenCode: `compaction` config). **Memory discipline.** Keep instruction memory (human-authored `AGENTS.md`/`CLAUDE.md`) separate from learning memory (agent-accumulated corrections); learning that leaks into instruction files drifts behavior silently. Harnesses with no native recall store fall back to `.agents/memory/` (a `MEMORY.md` index plus one fact per file)  --  see `skills/memory-engineering`. **Variable substitution for secrets.** Use `{env:VAR}` / `{file:path}` so keys never live in config files (OpenCode config doc). See `AGENTS.md` §7 and `skills/harness-engineering` for the full doctrine  --  this section summarizes, does not duplicate.

Validate the repo's artifacts at any time with `python3 scripts/checks.py --all` (the `./scripts/validate-agents.sh` shim execs it).

## Kilo/Opencode config example

Model names are examples; substitute your provider/model IDs.

```json
{
  ...
  "model": "anthropic/claude-sonnet",
  "small_model": "anthropic/claude-haiku",
  "subagent_model": "anthropic/claude-sonnet",
  "default_agent": "conductor",
  "agent": {
    "conductor": {
      "model": "anthropic/claude-opus"
    },
    "orchestrator": {
      "model": "anthropic/claude-opus"
    },
    "plan": {
      "model": "anthropic/claude-opus"
    },
    "debug": {
      "model": "anthropic/claude-sonnet"
    },
    "code": {
      "model": "anthropic/claude-sonnet"
    },
    "ask": {
      "model": "anthropic/claude-haiku"
    },
    "explore": {
      "model": "anthropic/claude-haiku"
    },
    "compaction": {
      "model": "anthropic/claude-haiku"
    },
    "coder": {
      "model": "anthropic/claude-sonnet"
    },
    "discover": {
      "model": "anthropic/claude-haiku"
    }
  },
  ...
}
```

## References

### Methodology
- [Structured Prompt-Driven Development (SPDD)  --  Martin Fowler](https://martinfowler.com/articles/structured-prompt-driven/)  --  REASONS Canvas, prompt-code bidirectional sync, phased-review rationale
- [GitHub Spec-Kit  --  Spec-driven Development](https://github.com/github/spec-kit/blob/main/spec-driven.md)  --  Spec-as-truth, executable specs, constitutional gates
- [Lost in the Middle (Liu et al., 2023)](https://arxiv.org/abs/2307.03172)  --  Why instructions must be split, not bloated

### Harness engineering canon
- [Learn Harness Engineering (12 lectures)](https://walkinglabs.github.io/learn-harness-engineering/en/)  --  Synthesized canon these configs are grounded in
- [Harness Engineering  --  Martin Fowler](https://martinfowler.com/articles/harness-engineering.html)  --  Guides vs sensors; computational vs inferential controls
- [Harness Engineering  --  OpenAI](https://openai.com/index/harness-engineering/)  --  Repo as operational record; harness-driven reliability
- [Effective Harnesses for Long-Running Agents  --  Anthropic](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)  --  Small next steps, handoff files, context anxiety
- [Harness Design for Long-Running Application Development  --  Anthropic](https://www.anthropic.com/engineering/harness-design-long-running-apps)  --  Worker/checker separation, premature-victory prevention
- [Unrolling the Codex agent loop  --  OpenAI](https://openai.com/index/unrolling-the-codex-agent-loop/)  --  Agent loop structure and intervention points
- [Demystifying evals for AI agents  --  Anthropic](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)  --  Evaluator rubrics and self-judgment calibration
- [Improving Deep Agents with harness engineering  --  LangChain](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering)  --  Guides/sensors and lifecycle controls for deep agents
- [Continually improving our agent harness  --  Cursor](https://cursor.com/blog/continually-improving-agent-harness)  --  Iterate the harness as models improve; simplify over accrete
- [Decision-Time Guidance: Keeping Replit Agent Reliable  --  Replit](https://blog.replit.com/decision-time-guidance)  --  Situational guidance at the decision point
- [Maintaining Code Quality at Agent Speed  --  Salesforce](https://engineering.salesforce.com/maintaining-code-quality-at-agent-speed-7-patterns-for-agentic-engineering/)  --  Gates over prompts, grade-the-tests, mutation testing
- [How to Build Reliable AI Agents  --  Salesforce](https://engineering.salesforce.com/how-to-build-reliable-ai-agents-5-engineering-patterns-from-a-production-system/)  --  Separate reasoning from computation; explanations≠evidence

### Language & performance
- [10x Commandments of Highly Effective Go  --  JetBrains](https://blog.jetbrains.com/go/2025/10/16/the-10x-commandments-of-highly-effective-go/)  --  Code quality and readability principles
- [Go Performance Patterns  --  goperf.dev](https://goperf.dev/01-common-patterns/)  --  Memory, concurrency, I/O, compiler optimization patterns

### Tool documentation
- [Kilo Docs](https://kilo.ai/docs/customize/)  --  [Customize](https://kilo.ai/docs/customize/), [Prompt Engineering](https://kilo.ai/docs/customize/prompt-engineering), [Context Condensing](https://kilo.ai/docs/customize/context/context-condensing), [Codebase Indexing](https://kilo.ai/docs/customize/context/codebase-indexing)
- [OpenCode Docs](https://opencode.ai/docs/)  --  Config at `~/.config/opencode/AGENTS.md`, agents dir `agents/`

### Agent Skills ecosystem
- [Agent Skills Specification](https://agentskills.io/specification)  --  The open `SKILL.md` format this repo conforms to
- [Agent Skills  --  Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)  --  Progressive disclosure via "load when X" hints
- [Agent Skills  --  Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)  --  Train/validation split for triggering accuracy
- [skills.sh](https://skills.sh)  --  Open skills leaderboard and `npx skills` CLI powering `npx skills add bouroo/agents`
- [Claude Code Plugin Marketplace](https://code.claude.com/docs/en/plugin-marketplaces)  --  `.claude-plugin/plugin.json` + `marketplace.json` format
- [Cursor Plugin Specification](https://github.com/cursor/plugins)  --  `.cursor-plugin/plugin.json` + `marketplace.json` schema
- [Gemini CLI Extensions  --  Reference](https://geminicli.com/docs/extensions/reference/)  --  `gemini-extension.json` manifest format
