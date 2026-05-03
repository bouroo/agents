# Self-Organized Agent Configuration

Shared, language-agnostic agent configuration for AI coding assistants. Symlinked to each tool's expected location via `link.sh`.

Based on [SPDD](https://martinfowler.com/articles/structured-prompt-driven/), [GitHub Spec-Kit](https://github.com/github/spec-kit), [10x Commandments of Highly Effective Go](https://blog.jetbrains.com/go/2025/10/16/the-10x-commandments-of-highly-effective-go/), [Go Performance Patterns](https://goperf.dev/01-common-patterns/), [Kilo Docs](https://kilo.ai/docs/customize/), and [OpenCode Docs](https://opencode.ai/docs/).

## Quick Start

```bash
~/.agents/link.sh              # Create symlinks for all supported tools
~/.agents/link.sh status       # Check symlink status
~/.agents/link.sh unlink       # Remove all symlinks
~/.agents/link.sh link opencode # Link only OpenCode
```

## Directory Structure

```
~/.agents/
├── AGENTS.md              # Core agent instructions (symlinked to each tool)
├── README.md              # This file
├── link.sh                # Symlink manager (link/unlink/status)
├── agents/                # Named agent modes for delegation
│   ├── conductor.md       # Orchestrator — decomposes and delegates tasks
│   ├── explorer.md        # Read-only project exploration
│   ├── implementer.md     # Full implementation — writes code, runs commands
│   ├── planner.md         # Analysis and planning with REASONS Canvas
│   ├── reviewer.md        # Code review — quality, security, performance
│   └── tester.md          # Test engineering
├── commands/              # Slash commands
│   ├── generate-agents-md.md  # Generate AGENTS.md for a project
│   ├── refactor-codebase.md   # Refactor and optimize code
│   └── verify-codebase.md     # Format, lint, scan, test
└── skills/                # Conditional modules loaded by context
    ├── abstraction-first/     # Design before you generate
    ├── alignment/             # Lock intent before coding
    ├── code-quality/          # Readability, clean code, naming
    ├── context-management/    # Context limits, compaction, quality
    ├── error-design/          # Error types, wrapping, actionable messages
    ├── incremental-delivery/  # Feature flags, small PRs, rollout
    ├── iterative-review/      # Controlled review-and-iterate loops
    ├── naming-conventions/    # Language-agnostic naming
    ├── performance/           # Optimization patterns
    ├── safe-by-default/       # Always-valid values, input validation, security
    ├── self-organizing-coder/ # Task decomposition, delegation, SPDD workflow
    ├── spec-driven/           # SPDD methodology and REASONS Canvas
    └── test-first/            # TDD workflow, Red-Green-Refactor
```

## Supported Tools

| Tool | Config Location | Agent File | Agents Dir |
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

| Agent | Mode | Purpose | Permissions |
|-------|------|---------|-------------|
| `conductor` | primary | Orchestrates — decomposes, delegates, validates | task only |
| `explorer` | subagent | Read-only exploration — files, architecture | read-only |
| `implementer` | subagent | Implementation — writes code, runs commands | full access |
| `planner` | subagent | Planning — REASONS Canvas, implementation plans | read + write plans |
| `reviewer` | subagent | Code review — quality, security, performance | read + read-only git |
| `tester` | subagent | Test engineering — writes and runs tests | test files + shell |

## Slash Commands

| Command | Description |
|---------|-------------|
| `/generate-agents-md` | Generate AGENTS.md — codebase analysis or from brief |
| `/refactor-codebase` | Refactor and optimize — measure, refactor, verify, sync |
| `/verify-codebase` | Format, lint, type-check, scan, test |

## Skills

| Skill | Trigger |
|-------|---------|
| `abstraction-first` | Designing before implementing |
| `alignment` | Locking intent, scoping features |
| `code-quality` | Code quality discussions, reviews |
| `context-management` | Long sessions, compaction, context limits |
| `error-design` | Error handling, error types |
| `incremental-delivery` | Shipping incrementally, feature flags |
| `iterative-review` | Review loops, spec-code alignment |
| `naming-conventions` | Writing identifier names |
| `performance` | Performance optimization |
| `safe-by-default` | Safety patterns, input validation, security |
| `self-organizing-coder` | Autonomous multi-step workflows |
| `spec-driven` | SPDD methodology, REASONS Canvas |
| `test-first` | TDD, test writing |

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
- [OpenCode Docs](https://opencode.ai/docs/) — OpenCode config format
