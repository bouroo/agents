# Self-Organized Agent Configuration

Shared, language-agnostic agent configuration for AI coding assistants. Contains global coding standards (AGENTS.md), reusable slash commands, domain-specific skills, and an orchestrator agent. Symlinked into each supported tool's config directory via `link.sh`.

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
├── AGENTS.md                  # Global coding standards and workflow principles
├── README.md                  # This file
├── link.sh                    # Symlink manager for supported tools
├── agents/                    # Agent definitions (mode, permissions, system prompts)
│   └── conductor.md           # Master orchestrator — decomposes, delegates, validates
├── commands/                  # Slash commands (reusable prompt workflows)
│   ├── code-review.md         # Review code for correctness, safety, and performance
│   ├── refactor-codebase.md   # Performance refactoring — analyze, plan, baseline, execute, verify
│   ├── spdd-workflow.md       # SPDD end-to-end — canvas → spec → code → sync
│   └── verify-codebase.md     # Full verification — format, lint, type-check, scan, test, githook
├── skills/                    # Domain-specific skill modules
│   ├── effective-code-craft/      # Clean, maintainable, production-ready code practices
│   ├── performance-patterns/      # High-performance software patterns (memory, concurrency, I/O)
│   └── spec-driven-development/   # Specification-first workflow with REASONS canvas
└── .agents/                   # Runtime directory (created by conductor agent at runtime)
    └── plans/                 # Spec drafts, REASONS canvases, plan trackers
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

| Agent        | Mode    | Purpose                                                  |
|--------------|---------|----------------------------------------------------------|
| `conductor`  | primary | Self-organizing orchestrator — decomposes, delegates, senses, self-corrects, steers |

## Commands

| Command            | Description                                                          |
|--------------------|----------------------------------------------------------------------|
| `code-review`        | Review code changes for correctness, safety, and performance       |
| `refactor-codebase`  | Performance refactoring — analyze, plan, baseline, execute, verify |
| `spdd-workflow`      | Structured prompt-driven development — canvas → spec → code → sync |
| `verify-codebase`    | Full verification pass — format, lint, type-check, scan, test, githook gate |

## Skills

| Skill                       | Trigger                                                                                  |
|-----------------------------|------------------------------------------------------------------------------------------|
| `effective-code-craft`      | Writing, reviewing, or refactoring code for clarity, safety, testability, or efficiency  |
| `performance-patterns`      | Optimizing for speed, throughput, latency, or memory after correctness is proven          |
| `spec-driven-development`   | Starting new features, resolving ambiguous requirements, bridging intent to implementation |

## SPDD Methodology

```
Story → Analysis → Canvas → Generate → Test → Review → Sync
  ↑                                                      |
  └────────────── repeat until aligned ──────────────────┘
```

## References

- [Structured Prompt-Driven Development (SPDD)](https://martinfowler.com/articles/structured-prompt-driven/) — REASONS Canvas, prompt-code bidirectional sync
- [GitHub Spec-Kit — Spec-driven Development](https://github.com/github/spec-kit/blob/main/spec-driven.md) — Spec-as-truth, executable specs, constitutional gates
- [10x Commandments of Highly Effective Go](https://blog.jetbrains.com/go/2025/10/16/the-10x-commandments-of-highly-effective-go/) — Code quality and readability principles
- [Go Performance Patterns](https://goperf.dev/01-common-patterns/) — Memory, concurrency, I/O, compiler optimization patterns
- [Kilo Docs — Customize](https://kilo.ai/docs/customize/) — Config at `~/.config/kilo/AGENTS.md`, agents dir `agent/`
- [OpenCode Docs](https://opencode.ai/docs/) — Config at `~/.config/opencode/AGENTS.md`, agents dir `agents/`
