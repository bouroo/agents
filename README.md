# Self-Organized Agent Configuration

Shared, language-agnostic agent configuration for AI coding assistants. Symlinked to each tool's expected location via `link.sh`.

Based on [Structured Prompt-Driven Development (SPDD)](https://martinfowler.com/articles/structured-prompt-driven/), [GitHub Spec-Kit](https://github.com/github/spec-kit), and [10x Commandments of Highly Effective Go](https://blog.jetbrains.com/go/2025/10/16/the-10x-commandments-of-highly-effective-go/).

## Quick Start

```bash
~/.agents/link.sh          # Create symlinks for all supported tools
~/.agents/link.sh status   # Check symlink status
~/.agents/link.sh unlink   # Remove all symlinks
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
│   ├── refactor.md        # /refactor — refactor and optimize code
│   ├── generate-agents-md.md # /generate-agents-md — generate AGENTS.md for project
│   └── verify-project.md  # /verify-project — format, lint, scan, test
└── skills/                # Conditional modules loaded by context
    ├── abstraction-first/ # Design before you generate
    ├── alignment/         # Lock intent before coding
    ├── code-quality/      # Readability, clean code, naming
    ├── context-management/# Context limits, compaction, quality
    ├── error-design/      # Error types, wrapping, actionable messages
    ├── incremental-delivery/ # Feature flags, small PRs, rollout
    ├── iterative-review/  # Controlled review-and-iterate loops
    ├── naming-conventions/# Language-agnostic naming
    ├── performance/       # Optimization patterns
    ├── safe-by-default/   # Always-valid values, input validation, security
    ├── self-organizing-coder/ # Task decomposition, delegation, SPDD workflow
    ├── spec-driven/       # SPDD methodology and REASONS Canvas
    └── test-first/        # TDD workflow, Red-Green-Refactor
```

## Supported Tools

| Tool | Config Location | Agent File | Agents Dir |
|------|-----------------|------------|------------|
| Claude Code | `~/.claude/` | `CLAUDE.md` | — |
| Gemini | `~/.gemini/` | `GEMINI.md` | — |
| Kilo | `~/.config/kilo/` | `AGENTS.md` | `agent/` |
| OpenCode | `~/.config/opencode/` | `AGENTS.md` | `agents/` |
| Qwen | `~/.qwen/` | `AGENTS.md` | — |

## Agents

| Agent | Mode | Purpose | Permissions |
|-------|------|---------|-------------|
| `conductor` | primary | Orchestrates — decomposes tasks, delegates, validates | task only |
| `explorer` | subagent | Project exploration — finds files, maps architecture | read-only |
| `implementer` | subagent | Implementation — writes code, edits, runs commands | full access |
| `planner` | subagent | Analysis — designs solutions, generates REASONS Canvas | read + plans/ |
| `reviewer` | subagent | Code review — quality, security, performance, intent alignment | read-only |
| `tester` | subagent | Test engineering — writes and runs tests | test files + shell |

## Slash Commands

| Command | Description |
|---------|-------------|
| `/refactor` | Refactor and optimize — measure, refactor, optimize, sync |
| `/generate-agents-md` | Generate AGENTS.md — codebase analysis (no args) or from brief (with args) |
| `/verify-project` | Format, lint, type-check, scan, test |

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

SPDD (Structured Prompt-Driven Development) is embedded as foundational knowledge in `skills/spec-driven/`, `skills/self-organizing-coder/`, and all agents — not exposed as commands. The workflow is:

```
Story → Analysis → Canvas → Generate → Test → Review → Sync
  ↑                                                    |
  └────────────── repeat until aligned ────────────────┘
```

Agents apply SPDD automatically when tasks match the methodology's fitness criteria.

## Context Condensing

- **Auto-compaction**: Triggers at ~20K token headroom
- **Pruning**: Clears tool outputs beyond ~40K recency
- **Manual**: `/compact` command
- **Post-compaction**: Re-read modified files

## References

- [Structured Prompt-Driven Development (SPDD)](https://martinfowler.com/articles/structured-prompt-driven/)
- [GitHub Spec-Kit](https://github.com/github/spec-kit/blob/main/spec-driven.md)
- [10x Commandments of Highly Effective Go](https://blog.jetbrains.com/go/2025/10/16/the-10x-commandments-of-highly-effective-go/)
- [Kilo Docs — AGENTS.md](https://kilo.ai/docs/customize/agents-md)
- [Kilo Docs — Skills](https://kilo.ai/docs/customize/skills)
- [Kilo Docs — Workflows](https://kilo.ai/docs/customize/workflows)
- [Kilo Docs — Custom Subagents](https://kilo.ai/docs/customize/custom-subagents)
- [Kilo Docs — Context Condensing](https://kilo.ai/docs/customize/context/context-condensing)
- [OpenCode Tools](https://opencode.ai/docs/tools/)
- [OpenCode Docs — Commands](https://opencode.ai/docs/commands/)
- [Agent Skills Specification](https://agentskills.io/home)
