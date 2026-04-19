# Self-Organizing Coder Agent

Shared agent configuration for Claude Code, Gemini, OpenCode, Kilo, and Qwen. One source of truth, symlinked to each tool's expected location.

## Quick Start

```bash
~/.agents/link.sh
```

This bootstraps symlinks for all supported tools. Run it once after cloning or updating.

## Directory Structure

```
~/.agents/
├── AGENTS.md              # Core agent instructions (symlinked to each tool)
├── README.md              # This file
├── link.sh                # Bootstrap script: creates symlinks
├── agents/                # Named agent modes (for delegation via `task` tool)
│   ├── conductor.md       # Master orchestrator — decomposes tasks, delegates to subagents
│   ├── explorer.md        # Read-only codebase exploration
│   ├── implementer.md     # Full-capability implementation — writes code, runs commands
│   ├── planner.md         # Analysis and planning — designs solutions, creates plans
│   ├── reviewer.md        # Read-only code review — quality, security, performance
│   └── tester.md          # Test engineering — writes and runs tests
├── commands/              # Slash commands
│   ├── refactor.md        # /refactor — readability, safety, performance, maintainability
│   ├── verify-project.md  # /verify-project — format, lint, vulnerability scan, tests
│   └── vb-review.md       # /vb-review — VB Mobile Backend review checklist
└── skills/                # Conditional skill modules loaded by context
    ├── code-quality/      # Readability, clean code, naming
    ├── naming-conventions/ # Language-agnostic naming conventions
    ├── performance/       # Language-agnostic performance optimization
    ├── self-organizing-coder/ # Task decomposition, subagent delegation, iterative delivery
    └── spec-driven/       # Spec-driven development workflow
```

## Supported Tools

| Tool | Config dir | Agent file |
|------|-----------|------------|
| Claude Code | `~/.claude/` | `CLAUDE.md` |
| Gemini | `~/.gemini/` | `GEMINI.md` |
| OpenCode | `~/.config/opencode/` | `AGENTS.md` |
| Kilo | `~/.config/kilo/` | `AGENTS.md` |
| Qwen | `~/.qwen/` | `AGENTS.md` |

The `link.sh` script creates symlinks for `AGENTS.md`, `commands/`, `skills/`, and `agents/` directories where the tool supports them.

## Agent Architecture

### AGENTS.md — Top-Level Instructions

Defines the core execution loop and coding standards:

- **Workflow** — Specify → Plan → Delegate → Validate → Iterate
- **Code Quality** — Readability, safe defaults, error wrapping, no mutable globals, decoupled from environment
- **Performance** — Preallocation, object reuse, batched I/O, minimized copies, lazy initialization
- **Naming Conventions** — camelCase/PascalCase, no type names in identifiers, short lowercase package names
- **Architecture** — Modular by default, test first, simple (≤3 top-level modules), no speculative features

### Named Agents

Agents available for delegation via the `task` tool:

| Agent | Mode | Purpose | Permissions |
|-------|------|---------|-------------|
| `conductor` | primary | Master orchestrator — decomposes tasks, delegates to subagents, validates outputs | No edits, no bash |
| `explorer` | subagent | Read-only codebase exploration — finds files, searches content, maps architecture | No edits, no bash |
| `implementer` | subagent | Full-capability implementation — writes code, edits files, runs commands | Full edit, write, bash |
| `planner` | subagent | Analysis and planning — designs solutions, creates implementation plans, estimates scope | Read-only |
| `reviewer` | subagent | Code review — quality, security, performance, best practices | Read-only (+ git diff/log) |
| `tester` | subagent | Test engineering — writes and runs tests, validates against acceptance criteria | Edit/write (test files), full bash |

### Slash Commands

| Command | Description |
|---------|-------------|
| `/refactor` | Refactor code for readability, safety, performance, and maintainability |
| `/verify-project` | Format, lint (auto-fix), vulnerability scan, static analysis, and run tests |
| `/vb-review` | Virtual Banking Mobile Backend review — comprehensive Go/Kafka/Postgres/Mongo/Redis/K8s checks |

### Skills

Conditional rule modules loaded when context matches. Each skill is a `SKILL.md` file in `skills/<name>/`.

| Skill | Trigger Context |
|-------|-----------------|
| `code-quality` | Readability, clean code, naming discussions |
| `naming-conventions` | Writing or reviewing identifier names |
| `performance` | Performance optimization discussions |
| `self-organizing-coder` | Task decomposition, subagent delegation, iterative delivery |
| `spec-driven` | Planning features, writing specs, spec-first workflows |

## Planned Skills (Not Yet Implemented)

The following skills are described in the desired-state but not yet implemented:

| Skill | Purpose |
|-------|---------|
| `context-management` | Long sessions, context limits, compaction |
| `error-design` | Error types, wrapping, actionable messages |
| `go-excellence` | Go naming, performance, concurrency, security |
| `go-performance` | Go memory, CPU, and throughput optimization |
| `incremental-delivery` | Feature flags, small PRs, progressive rollout |
| `library-first` | Architecture design, new feature structure |
| `security-by-default` | Input handling, auth, file access, secrets |
| `simplify` | Refactoring, reducing technical debt, unnecessary complexity |
| `test-first` | TDD workflow, writing tests before implementation |
