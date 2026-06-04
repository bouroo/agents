# Self-Organized Agent Configuration

Shared, language-agnostic agent configuration for AI coding assistants. Symlinked to each tool's expected location via `link.sh`.

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
│   ├── code-review.md         # Structured code review — correctness, safety, performance
│   ├── refactor-codebase.md   # Structured refactoring — test, measure, refactor, verify, sync
│   ├── spdd-workflow.md       # SPDD canvas → spec → code → review → sync loop
│   └── verify-codebase.md     # Full verification pass — format, lint, type-check, scan, test
├── skills/                    # Domain-specific skill modules
│   ├── effective-code-craft/      # Clean, maintainable, production-ready code practices
│   ├── performance-patterns/      # High-performance software patterns (memory, concurrency, I/O)
│   └── spec-driven-development/   # Specification-first workflow with REASONS canvas
└── .agents/                   # Internal handoff directory (specs, canvases, progress trackers)
    └── plans/                 # Spec drafts, REASONS canvases, plan trackers
```

## Supported Tools

| Tool       | Config Location          | Config File  | Agents Dir  |
|------------|--------------------------|--------------|-------------|
| Gemini     | `~/.gemini/`             | `GEMINI.md`  | —           |
| Codex      | `~/.codex/`              | `AGENTS.md`  | —           |
| Claude     | `~/.claude/`             | `CLAUDE.md`  | —           |
| Qwen       | `~/.qwen/`               | `AGENTS.md`  | —           |
| OpenCode   | `~/.config/opencode/`    | `AGENTS.md`  | `agents/`   |
| Kilo       | `~/.config/kilo/`        | `AGENTS.md`  | `agent/`    |

## Agents

| Agent        | Mode    | Purpose                                                  |
|--------------|---------|----------------------------------------------------------|
| `conductor`  | primary | Master orchestrator — decomposes tasks, delegates, validates |

## Commands

| Command            | Description                                                          |
|--------------------|----------------------------------------------------------------------|
| `code-review`        | Review code changes for quality, security, and performance        |
| `refactor-codebase`  | Structured refactoring — test, measure, refactor, verify, sync    |
| `spdd-workflow`      | SPDD canvas → spec → code → review → sync loop                    |
| `verify-codebase`    | Format, lint, type-check, security scan, and test the project      |

## Skills

| Skill                       | Trigger                                                                                  |
|-----------------------------|------------------------------------------------------------------------------------------|
| `effective-code-craft`      | Writing modules, designing APIs, handling errors, tests, concurrency, code review        |
| `performance-patterns`      | Optimizing for speed, throughput, latency, or memory usage                               |
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
