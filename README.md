# Self-Organized Agent Configuration

[![Last commit](https://img.shields.io/github/last-commit/bouroo/agents?logo=github)](https://github.com/bouroo/agents)
[![Stars](https://img.shields.io/github/stars/bouroo/agents?logo=github)](https://github.com/bouroo/agents)
![Type](https://img.shields.io/badge/type-AI%20agent%20config-blue)
![Tools](https://img.shields.io/badge/tools-8-success)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](./LICENSE.md)

A shared, language-agnostic setup for AI coding assistants. Drop one folder into your machine and eight different tools  --  Gemini, Claude, OpenCode, Kilo, Codex, Qwen, and more  --  pick up the same global coding standards, slash commands, and reusable skills. No per-tool copy-paste, no drift between projects.

## Why use it

- **One config, many tools**  --  write the rules once; link it everywhere via a single script.
- **Coding standards baked in**  --  global guidelines live in `AGENTS.md` and are followed by every tool.
- **On-demand skills**  --  focused modules (commit messages, code craft, performance, harness design, specs) load only when you need them.
- **Slash commands**  --  run repeatable workflows like refactor / review / verify with one command.
- **One-command install**  --  `link.sh` handles the symlinks; `link.sh status` tells you what's linked.

## Quick Start

```bash
~/.agents/link.sh # Create symlinks for all supported tools
~/.agents/link.sh status # Check symlink status
~/.agents/link.sh unlink # Remove all symlinks
~/.agents/link.sh link opencode # Link only OpenCode (filter by tool name)
```

Then restart your coding tool so it picks up the new config.

## What's inside

```
~/.agents/
├── AGENTS.md # Global coding standards and workflow router
├── README.md # This file
├── link.sh # Symlink manager for supported tools
├── agents/ # Orchestrator agents (mode, permissions, prompt)
│ └── conductor.md # Decisive orchestrator  --  chooses best practice, records assumption, proceeds
├── commands/ # Slash commands (reusable prompt workflows)
│ ├── document-phase.md
│ ├── refactor-phase.md
│ ├── review-phase.md
│ └── verify-phase.md
├── skills/ # On-demand skill modules (load via the skill tool)
│ ├── commit-message/
│ ├── effective-code-craft/
│ ├── harness-engineering/
│ ├── performance-patterns/
│ ├── repo-documentation/
│ └── spec-driven-development/
├── scripts/
│ └── validate-agents.sh # Repo self-checks  --  the opencode-format gate
└── .agents/ # Per-project runtime dir (created on use IN THE TARGET PROJECT, never in this repo; gitignored here)
 ├── plans/ # Spec drafts, REASONS canvases, plan trackers, retros
 └── handoff/ # Subagent reports and summaries
```

### Agents

Orchestrators that think, dispatch, and verify  --  they never edit code themselves.

| Agent | Mode | Purpose |
|----------------|---------|------------------------------------------------------------------------------------------|
| `conductor` | primary | Self-organizing orchestrator. Decomposes tasks, delegates to subagents, validates outcomes, and steers its own harness. Decisive: chooses the industry-standard option, records the assumption, and proceeds. Never executes work directly. |

It is non-coding: it thinks, dispatches, verifies, and steers through a squad of subagents. It shares canonical Convergence Gates and On-Disk State (see [skills/harness-engineering/SKILL.md](skills/harness-engineering/SKILL.md) Appendix A & B).

### Commands

Reusable prompt workflows you trigger with a slash command.

| Command | Description |
|--------------------|----------------------------------------------------------------------|
| `document-phase` | Document phase  --  bootstrap repo docs or sync docs/ with code changes |
| `refactor-phase` | Refactor phase  --  analyze, plan, baseline, execute, verify |
| `review-phase` | Review phase  --  review code changes for correctness, safety, performance |
| `verify-phase` | Verify phase  --  format, lint, type-check, scan, test, githook gate |

### Skills

Focused modules the agent loads on demand when a task matches.

| Skill | Trigger |
|-----------------------------|------------------------------------------------------------------------------------------|
| `effective-code-craft` | Writing, reviewing, or refactoring code for clarity, safety, testability, or efficiency  |
| `harness-engineering` | Designing agent workflows, checkpoints, verification rules, or orchestrator agents; lifecycle controls; preventing overreach, premature victory, or context loss |
| `performance-patterns` | Optimizing for speed, throughput, latency, or memory after correctness is proven |
| `repo-documentation` | Repo keeps a `docs/` tree and a behavior/interface/invariant/domain-term change must update the affected doc in the same change |
| `spec-driven-development` | Starting new features, resolving ambiguous requirements, bridging intent to implementation |
| `commit-message` | Generating a conventional commit message from staged changes |

## Supported Tools

`link.sh` symlinks four artifacts into each tool's config directory.

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

### Harness Engineering

These configs embody the harness-engineering canon, not merely reference it: the repo is the operational record of truth; instructions are split into focused, agent-loadable modules; WIP is one verified task at a time; completion requires executable evidence; every task runs static + runtime + end-to-end verification; and state persists across sessions via explicit clock-in/out checklists.

The `harness-engineering` skill adds the design vocabulary for *building* these controls  --  feedforward **guides** vs feedback **sensors**, **computational** vs **inferential** controls  --  and the disciplines that keep agent output trustworthy: **gates enforce**, **separate reasoning from computation**, **grade the tests** (mutation testing  --  an agent-authored green suite is a signal, not proof), and **engineer the whole lifecycle** (improve the harness, not the prompt; deliberate friction is leverage). Norms + clock-in/out checklist: [skills/harness-engineering/SKILL.md](skills/harness-engineering/SKILL.md).

### SPDD Methodology

```
Story → Analysis → Canvas → Generate → Test → Review → Sync
  ↑ |
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

**AGENTS.md is a router, not a dump.** Keep global rules terse; load detail from skills on demand (Kilo: "Keep custom instructions concise and actionable"; OpenCode: lazy-load instructions). **Semantic codebase index.** When the host tool offers it (Kilo: "Codebase Indexing"), prefer `semantic_search` over broad grep fan-out for unfamiliar surfaces. **Context condensing discipline.** Long sessions auto-compact; put the next executable action and current blocker in the latest turn or a tracked file, because the verbatim tail is what survives (Kilo: "Context Condensing"; OpenCode: `compaction` config). **Variable substitution for secrets.** Use `{env:VAR}` / `{file:path}` so keys never live in config files (OpenCode config doc). See `AGENTS.md` §7 and `skills/harness-engineering` for the full doctrine  --  this section summarizes, does not duplicate.

Validate the repo's artifacts at any time with `./scripts/validate-agents.sh`.

## Kilo/Opencode config example

Model names are examples; substitute your provider/model IDs.

```json
{
  ...
  "model": "<your-model-here>",
  "small_model": "<your-model-here>",
  "subagent_model": "<your-model-here>",
  "default_agent": "conductor",
  "agent": {
    "conductor": {
      "model": "<your-model-here>"
    },
    "orchestrator": {
      "model": "<your-model-here>"
    },
    "plan": {
      "model": "<your-model-here>"
    },
    "debug": {
      "model": "<your-model-here>"
    },
    "code": {
      "model": "<your-model-here>"
    },
    "ask": {
      "model": "<your-model-here>"
    },
    "explore": {
      "model": "<your-model-here>"
    },
    "compaction": {
      "model": "<your-model-here>"
    }
  },
  ...
}
```

## References

- [Structured Prompt-Driven Development (SPDD)  --  Martin Fowler](https://martinfowler.com/articles/structured-prompt-driven/)  --  REASONS Canvas, prompt-code bidirectional sync, phased-review rationale
- [GitHub Spec-Kit  --  Spec-driven Development](https://github.com/github/spec-kit/blob/main/spec-driven.md)  --  Spec-as-truth, executable specs, constitutional gates
- [Harness Engineering  --  Martin Fowler](https://martinfowler.com/articles/harness-engineering.html)  --  Guides vs sensors; computational vs inferential controls; shift quality left
- [Maintaining Code Quality at Agent Speed  --  Salesforce](https://engineering.salesforce.com/maintaining-code-quality-at-agent-speed-7-patterns-for-agentic-engineering/)  --  Gates over prompts, grade-the-tests, mutation testing, lifecycle engineering
- [How to Build Reliable AI Agents  --  Salesforce](https://engineering.salesforce.com/how-to-build-reliable-ai-agents-5-engineering-patterns-from-a-production-system/)  --  Separate reasoning from computation, explanations≠evidence, improve the harness
- [10x Commandments of Highly Effective Go  --  JetBrains](https://blog.jetbrains.com/go/2025/10/16/the-10x-commandments-of-highly-effective-go/)  --  Code quality and readability principles
- [Go Performance Patterns  --  goperf.dev](https://goperf.dev/01-common-patterns/)  --  Memory, concurrency, I/O, compiler optimization patterns
- [Kilo Docs  --  Customize](https://kilo.ai/docs/customize/)  --  Config at `~/.config/kilo/AGENTS.md`, agents dir `agent/`
- [OpenCode Docs](https://opencode.ai/docs/)  --  Config at `~/.config/opencode/AGENTS.md`, agents dir `agents/`
- [Harness Engineering  --  OpenAI](https://openai.com/index/harness-engineering/)  --  Repo as operational record; harness-driven agent reliability
- [Effective Harnesses for Long-Running Agents  --  Anthropic](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)  --  Small next steps, handoff files, context anxiety
- [Harness Design for Long-Running Application Development  --  Anthropic](https://www.anthropic.com/engineering/harness-design-long-running-apps)  --  Worker/checker separation, premature-victory prevention
- [Learn Harness Engineering (12 lectures)](https://walkinglabs.github.io/learn-harness-engineering/en/)  --  Synthesized canon these configs are grounded in
- [Unrolling the Codex agent loop  --  OpenAI](https://openai.com/index/unrolling-the-codex-agent-loop/)  --  Agent loop structure and harness intervention points
- [Demystifying evals for AI agents  --  Anthropic](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)  --  Evaluator rubrics and agent self-judgment calibration
- [Improving Deep Agents with harness engineering  --  LangChain](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering)  --  Applying guides/sensors and lifecycle controls to deep agents
- [Continually improving our agent harness  --  Cursor](https://cursor.com/blog/continually-improving-agent-harness)  --  Iterate the harness as models improve; simplification over accretion
- [Decision-Time Guidance: Keeping Replit Agent Reliable  --  Replit](https://blog.replit.com/decision-time-guidance)  --  Situational guidance at the decision point, not prompt-stuffing
- [Lost in the Middle (Liu et al., 2023)](https://arxiv.org/abs/2307.03172)  --  Why instructions must be split, not bloated
- [Kilo Docs  --  Prompt Engineering](https://kilo.ai/docs/customize/prompt-engineering)  --  Think-then-do loop; clarity, context, output format
- [Kilo Docs  --  Context Condensing](https://kilo.ai/docs/customize/context/context-condensing)  --  AGENTS.md as router; compaction discipline
- [Kilo Docs  --  Codebase Indexing](https://kilo.ai/docs/customize/context/codebase-indexing)  --  Semantic index for unfamiliar surfaces