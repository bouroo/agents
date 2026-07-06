# Self-Organized Agent Configuration

Shared, language-agnostic agent configuration for AI coding assistants. Contains global coding standards (`AGENTS.md`), reusable slash commands, on-demand skills, and orchestrator agents. Symlinked into each supported tool's config directory via `link.sh`.

## Quick Start

```bash
~/.agents/link.sh                 # Create symlinks for all supported tools
~/.agents/link.sh status          # Check symlink status
~/.agents/link.sh unlink          # Remove all symlinks
~/.agents/link.sh link opencode   # Link only OpenCode (filter by tool name)
```

## Directory Structure

```
~/.agents/
├── AGENTS.md                      # Global coding standards and workflow router
├── README.md                      # This file
├── link.sh                        # Symlink manager for supported tools
├── agents/                        # Orchestrator agents (mode, permissions, prompt)
│   └── conductor.md               # Decisive orchestrator — chooses best practice, records assumption, proceeds
├── commands/                      # Slash commands (reusable prompt workflows)
│   ├── refactor-phase.md
│   ├── review-phase.md
│   └── verify-phase.md
├── skills/                        # On-demand skill modules (load via the skill tool)
│   ├── commit-message/
│   ├── effective-code-craft/
│   ├── harness-engineering/
│   ├── performance-patterns/
│   └── spec-driven-development/
├── scripts/
│   └── validate-agents.sh         # Repo self-checks — the opencode-format gate
└── .agents/                       # Runtime + reference directory (created on use)
    ├── plans/                     # Spec drafts, REASONS canvases, plan trackers, retros
    └── handoff/                   # Subagent reports and summaries
```

## Supported Tools

`link.sh` symlinks four artifacts into each tool's config directory:

| Artifact      | Source            | Linked as         | Notes                          |
|---------------|-------------------|-------------------|--------------------------------|
| Config file   | `AGENTS.md`       | Tool-specific name| `GEMINI.md`, `CLAUDE.md`, or `AGENTS.md` |
| Commands      | `commands/`       | `commands/`       | All tools                      |
| Skills        | `skills/`         | `skills/`         | All tools                      |
| Agents        | `agents/`         | Tool-specific dir | Only OpenCode (`agents/`) and Kilo (`agent/`) |

| Tool       | Config Location          | Config File  | Agents Dir  |
|------------|--------------------------|--------------|-------------|
| Gemini          | `~/.gemini/`             | `GEMINI.md`  | —           |
| antigravity     | `~/.gemini/`             | `GEMINI.md`  | —           |
| antigravity-ide | `~/.gemini/`             | `GEMINI.md`  | —           |
| Codex      | `~/.codex/`              | `AGENTS.md`  | —           |
| Claude     | `~/.claude/`             | `CLAUDE.md`  | —           |
| Qwen       | `~/.qwen/`               | `AGENTS.md`  | —           |
| OpenCode   | `~/.config/opencode/`    | `AGENTS.md`  | `agents/`   |
| Kilo       | `~/.config/kilo/`        | `AGENTS.md`  | `agent/`    |

## Agents

| Agent          | Mode    | Purpose                                                                                  |
|----------------|---------|------------------------------------------------------------------------------------------|
| `conductor` | primary | Self-organizing orchestrator. Decomposes tasks, delegates to subagents, validates outcomes, and steers its own harness. Decisive: chooses the industry-standard option, records the assumption, and proceeds. Never executes work directly. |

It is non-coding: it thinks, dispatches, verifies, and steers through a squad of subagents. It shares canonical Convergence Gates and On-Disk State (see [skills/harness-engineering/SKILL.md](skills/harness-engineering/SKILL.md) Appendix A & B).

## Commands

| Command            | Description                                                          |
|--------------------|----------------------------------------------------------------------|
| `refactor-phase`    | Refactor phase — analyze, plan, baseline, execute, verify            |
| `review-phase`      | Review phase — review code changes for correctness, safety, performance |
| `verify-phase`      | Verify phase — format, lint, type-check, scan, test, githook gate    |

## Skills

| Skill                       | Trigger                                                                                  |
|-----------------------------|------------------------------------------------------------------------------------------|
| `effective-code-craft`      | Writing, reviewing, or refactoring code for clarity, safety, testability, or efficiency  |
| `harness-engineering`       | Designing agent workflows, checkpoints, verification rules, or orchestrator agents; lifecycle controls; preventing overreach, premature victory, or context loss |
| `performance-patterns`      | Optimizing for speed, throughput, latency, or memory after correctness is proven          |
| `spec-driven-development`   | Starting new features, resolving ambiguous requirements, bridging intent to implementation |
| `commit-message`            | Generating a conventional commit message from staged changes                              |

## OpenCode Format Mapping

This repo follows the [opencode](https://opencode.ai/docs/) artifact format so it loads natively when `link.sh` symlinks `commands/`, `skills/`, and `agents/` into `~/.config/opencode/`. OpenCode auto-discovers all three directories; no `opencode.json` is required.

| Artifact | File | Recognized frontmatter | Notes |
|---|---|---|---|
| Rules | `AGENTS.md` | (none — plain markdown) | Read as global rules from `~/.config/opencode/AGENTS.md`. Keep it a router; load detail from skills. |
| Agent | `agents/*.md` | `description` (req), `mode`, `temperature`, `steps`, `model`, `prompt`, `permission`, `hidden`, `color`, `top_p` | `permission` keys: `read edit glob grep list bash task external_directory todowrite webfetch websearch lsp skill question doom_loop` — each `allow\|ask\|deny` or a glob→action object. `tools` is deprecated; use `permission`. |
| Command | `commands/*.md` | `description` (req), `agent`, `subtask`, `model` | Body is the prompt template. Supports `$ARGUMENTS`, `$1`/`$2`/…, `` !`cmd` `` shell injection, `@file` references. |
| Skill | `skills/<name>/SKILL.md` | `name` (req, must equal dir, `^[a-z0-9]+(-[a-z0-9]+)*$`), `description` (req, 1–1024 chars), `license`, `compatibility`, `metadata` | Unknown fields (e.g. Kilo's `disable-model-invocation`) are ignored by opencode and kept for portability. Loaded on demand via the `skill` tool. |

**Discovery paths (global):** `~/.config/opencode/{AGENTS.md, agents/, commands/, skills/}`. Claude-compatible fallbacks (`CLAUDE.md`, `~/.claude/skills/`, `.agents/skills/`) are also honored. Skills are also discovered from `~/.agents/skills/*/SKILL.md`.

**Optional `opencode.json`** (not shipped — the repo stays tool-neutral):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": ["docs/guidelines.md"],
  "references": {
    "sdk": { "repository": "owner/repo", "description": "Use for SDK implementation details" }
  }
}
```

Validate the repo's artifacts at any time with `./scripts/validate-agents.sh`.

## Harness Engineering

These configs embody the harness-engineering canon, not merely reference it: the repo is the operational record of truth; instructions are split into focused, agent-loadable modules; WIP is one verified task at a time; completion requires executable evidence; every task runs static + runtime + end-to-end verification; and state persists across sessions via explicit clock-in/out checklists.

The `harness-engineering` skill adds the design vocabulary for *building* these controls — feedforward **guides** vs feedback **sensors**, **computational** vs **inferential** controls — and the disciplines that keep agent output trustworthy: **gates enforce**, **separate reasoning from computation**, **grade the tests** (mutation testing — an agent-authored green suite is a signal, not proof), and **engineer the whole lifecycle** (improve the harness, not the prompt; deliberate friction is leverage). Norms + clock-in/out checklist: [skills/harness-engineering/SKILL.md](skills/harness-engineering/SKILL.md).

## SPDD Methodology

```
Story → Analysis → Canvas → Generate → Test → Review → Sync
  ↑                                                      |
  └────────────── repeat until aligned ──────────────────┘
```

The workflow is phased to keep each review checkpoint small enough to engage with (cognitive load, not ceremony): validate behavior at the system boundary early, review code only once it works, and generate unit tests last as a regression net. See [skills/spec-driven-development/SKILL.md](skills/spec-driven-development/SKILL.md) for the fitness table — when to spec, and when not to.

## References

- [Structured Prompt-Driven Development (SPDD) — Martin Fowler](https://martinfowler.com/articles/structured-prompt-driven/) — REASONS Canvas, prompt-code bidirectional sync, phased-review rationale
- [GitHub Spec-Kit — Spec-driven Development](https://github.com/github/spec-kit/blob/main/spec-driven.md) — Spec-as-truth, executable specs, constitutional gates
- [Harness Engineering — Martin Fowler](https://martinfowler.com/articles/harness-engineering.html) — Guides vs sensors; computational vs inferential controls; shift quality left
- [Maintaining Code Quality at Agent Speed — Salesforce](https://engineering.salesforce.com/maintaining-code-quality-at-agent-speed-7-patterns-for-agentic-engineering/) — Gates over prompts, grade-the-tests, mutation testing, lifecycle engineering
- [How to Build Reliable AI Agents — Salesforce](https://engineering.salesforce.com/how-to-build-reliable-ai-agents-5-engineering-patterns-from-a-production-system/) — Separate reasoning from computation, explanations≠evidence, improve the harness
- [10x Commandments of Highly Effective Go — JetBrains](https://blog.jetbrains.com/go/2025/10/16/the-10x-commandments-of-highly-effective-go/) — Code quality and readability principles
- [Go Performance Patterns — goperf.dev](https://goperf.dev/01-common-patterns/) — Memory, concurrency, I/O, compiler optimization patterns
- [Kilo Docs — Customize](https://kilo.ai/docs/customize/) — Config at `~/.config/kilo/AGENTS.md`, agents dir `agent/`
- [OpenCode Docs](https://opencode.ai/docs/) — Config at `~/.config/opencode/AGENTS.md`, agents dir `agents/`
- [Harness Engineering — OpenAI](https://openai.com/index/harness-engineering/) — Repo as operational record; harness-driven agent reliability
- [Effective Harnesses for Long-Running Agents — Anthropic](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — Small next steps, handoff files, context anxiety
- [Harness Design for Long-Running Application Development — Anthropic](https://www.anthropic.com/engineering/harness-design-long-running-apps) — Worker/checker separation, premature-victory prevention
- [Learn Harness Engineering (12 lectures)](https://walkinglabs.github.io/learn-harness-engineering/en/) — Synthesized canon these configs are grounded in
- [Unrolling the Codex agent loop — OpenAI](https://openai.com/index/unrolling-the-codex-agent-loop/) — Agent loop structure and harness intervention points
- [Demystifying evals for AI agents — Anthropic](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) — Evaluator rubrics and agent self-judgment calibration
- [Improving Deep Agents with harness engineering — LangChain](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering) — Applying guides/sensors and lifecycle controls to deep agents
- [Continually improving our agent harness — Cursor](https://cursor.com/blog/continually-improving-agent-harness) — Iterate the harness as models improve; simplification over accretion
- [Decision-Time Guidance: Keeping Replit Agent Reliable — Replit](https://blog.replit.com/decision-time-guidance) — Situational guidance at the decision point, not prompt-stuffing
- [Lost in the Middle (Liu et al., 2023)](https://arxiv.org/abs/2307.03172) — Why instructions must be split, not bloated
- [Kilo Docs — Prompt Engineering](https://kilo.ai/docs/customize/prompt-engineering) — Think-then-do loop; clarity, context, output format
- [Kilo Docs — Context Condensing](https://kilo.ai/docs/customize/context/context-condensing) — AGENTS.md as router; compaction discipline
