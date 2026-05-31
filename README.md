# Self-Organized Agent Configuration

Shared, language-agnostic agent configuration for AI coding assistants. Symlinked to each tool's expected location via `link.sh`.

## Quick Start

```bash
~/.agents/link.sh              # Create symlinks for all supported tools
~/.agents/link.sh status       # Check symlink status
~/.agents/link.sh unlink       # Remove all symlinks
~/.agents/link.sh link opencode # Link only OpenCode (filter by tool name)
```

## Directory Structure

```
~/.agents/
├── AGENTS.md                  # Global coding standards and workflow principles
├── README.md                  # This file
├── link.sh                    # Symlink manager for all supported tools
├── agents/                    # Agent definitions (mode, permissions, system prompts)
│   ├── conductor.md           # Master orchestrator — decomposes, delegates, validates
│   ├── explorer.md             # Fast read-only codebase explorer (glob, grep, read)
│   └── builder.md             # General-purpose autonomous agent with full tool access
├── commands/                  # Slash commands (reusable prompt workflows)
│   ├── generate-agents-md.md  # Generate or update project AGENTS.md from codebase analysis
│   ├── refactor-codebase.md   # Structured refactoring — test, measure, refactor, verify, sync
│   └── verify-codebase.md     # Full verification pass — format, lint, type-check, scan, test
└── skills/                    # Domain-specific skill modules
    ├── effective-code-craft/  # Clean, maintainable, production-ready code practices
    ├── performance-patterns/  # High-performance software patterns (memory, concurrency, I/O)
    └── spec-driven-development/ # Specification-first workflow with REASONS canvas
```

## Supported Tools

| Tool | Config Location | Config File | Agents Dir |
|------|-----------------|------------|------------|
| Aider | `~/.aider/` | `CONVENTIONS.md` | — |
| Claude Code | `~/.claude/` | `CLAUDE.md` | — |
| Cline | `~/.cline/` | `AGENTS.md` | — |
| Codex | `~/.codex/` | `AGENTS.md` | — |
| Copilot | `~/.copilot/` | `AGENTS.md` | — |
| Cursor | `~/.cursor/` | `CURSOR.md` | — |
| Gemini | `~/.gemini/` | `GEMINI.md` | — |
| Kilo | `~/.config/kilo/` | `AGENTS.md` | `agent/` |
| OpenCode | `~/.config/opencode/` | `AGENTS.md` | `agents/` |
| Qwen | `~/.qwen/` | `AGENTS.md` | — |
| Windsurf | `~/.windsurf/` | `AGENTS.md` | — |

## Agents

| Agent | Mode | Steps | Permissions | Purpose |
|------------|----------|-------|----------------------------------------|---------|
| `conductor` | primary | 30 | edit=limited to handoff only, bash=deny, task=allow | Master orchestrator — decomposes tasks, delegates to subagents, validates results |
| `explorer` | subagent | — | edit=deny, bash=deny | Fast read-only codebase explorer — glob, grep, read only |
| `builder` | subagent | — | all tools (full access) | General-purpose autonomous agent — multi-step execution, file changes, shell commands |

## Slash Commands

| Command | Description |
|---------|-------------|
| `generate-agents-md` | Generate or update project AGENTS.md from codebase analysis or a brief |
| `refactor-codebase` | Structured refactoring — test, measure, refactor, verify, sync |
| `verify-codebase` | Format, lint, type-check, security scan, and test the project |

## Skills

| Skill | Trigger |
|-------|---------|
| `effective-code-craft` | Writing new modules, designing APIs, handling errors, writing tests, managing concurrency, reviewing code |
| `performance-patterns` | Optimizing for speed, throughput, latency, or memory usage |
| `spec-driven-development` | Starting new features, resolving ambiguous requirements, bridging intent to implementation |

## SPDD Methodology

```
Story → Analysis → Canvas → Generate → Test → Review → Sync
  ↑                                                      |
  └────────────── repeat until aligned ──────────────────┘
```

## References

- [Structured Prompt-Driven Development (SPDD)](https://martinfowler.com/articles/structured-prompt-driven/) — REASONS Canvas, prompt-code bidirectional sync
- [GitHub Spec-Kit](https://github.com/github/spec-kit/blob/main/spec-driven.md) — Spec-driven development methodology
- [10x Commandments of Highly Effective Go](https://blog.jetbrains.com/go/2025/10/16/the-10x-commandments-of-highly-effective-go/) — Code quality and readability principles
- [Go Performance Patterns](https://goperf.dev/01-common-patterns/) — Performance optimization patterns
- [Kilo Docs — Customize](https://kilo.ai/docs/customize/) — Agent config structure
- [Kilo Docs — Context Condensing](https://kilo.ai/docs/customize/context/context-condensing) — Auto-compaction, pruning, context management
- [OpenCode Docs](https://opencode.ai/docs/) — OpenCode config format