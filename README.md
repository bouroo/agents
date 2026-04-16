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
│   └── conductor.md       # Autonomous conductor — decomposes tasks, delegates to subagents
├── commands/              # Slash commands
│   ├── refactor.md        # /refactor — readability, safety, performance, maintainability
│   ├── verify-project.md  # /verify-project — format, lint, vulnerability scan, tests
│   └── vb-review.md       # /vb-review — VB Mobile Backend review checklist
└── skills/                # Conditional skill modules loaded by context
    ├── code-quality/      # Readability, clean code, naming
    ├── context-management/ # Long sessions, context limits, compaction
    ├── error-design/      # Error types, wrapping, actionable messages
    ├── go-excellence/     # Go naming, performance, concurrency, security
    ├── go-performance/    # Go memory, CPU, and throughput optimization
    ├── incremental-delivery/ # Feature flags, small PRs, progressive rollout
    ├── library-first/     # Architecture design, new feature structure
    ├── security-by-default/ # Input handling, auth, file access, secrets
    ├── self-organized-coder/ # Task decomposition, subagent delegation, iterative delivery
    ├── simplify/          # Refactoring, reducing technical debt, unnecessary complexity
    ├── spec-driven-dev/   # Planning features, writing specs, PRDs
    └── test-first/        # TDD workflow, writing tests before implementation
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

- **Execution loop** — Understand → Research → Plan → Test First → Implement → Verify → Iterate
- **Specification-Driven Development** — Specs are the source of truth; code serves specs
- **Library-First Architecture** — Features begin as standalone, reusable packages
- **Test-First** — Tests written before implementation (red-green-refactor)
- **Code Standards** — Readability, naming, performance, security, error handling
- **Performance Awareness** — Preallocation, zero-copy, buffered I/O, benchmarking
- **Concurrency** — Structured concurrency, confinement over sharing, no mutable globals

### Named Agents

Agents available for delegation via the `task` tool:

| Agent | Purpose |
|-------|---------|
| `conductor` | Decomposes complex tasks, delegates to subagents, validates outputs, delivers working increments |

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
| `context-management` | Long sessions, context limits, compaction |
| `error-design` | Error types, wrapping, actionable messages |
| `go-excellence` | Go codebases — naming, performance, concurrency, security |
| `go-performance` | Go memory, CPU, and throughput optimization |
| `incremental-delivery` | Feature flags, small PRs, progressive rollout |
| `library-first` | Architecture design, new feature structure |
| `security-by-default` | Input handling, auth, file access, secrets |
| `self-organized-coder` | Task decomposition, subagent delegation, iterative delivery |
| `simplify` | Refactoring, reducing technical debt, unnecessary complexity |
| `spec-driven-dev` | Planning features, writing specs, PRDs |
| `test-first` | TDD workflow, writing tests before implementation |

## Spec Artifacts

Non-trivial features produce a structured spec under `specs/<feature-slug>/`:

| File | Purpose |
|------|---------|
| `spec.md` | Requirements, constraints, interfaces, error cases, out-of-scope |
| `plan.md` | Architecture overview, requirement-to-decision mapping, rationale |
| `data-model.md` | Schema definitions, entity relationships, type contracts |
| `contracts/` | API specs, event definitions, function signatures |
| `research.md` | Technical investigation findings, library evaluations |
| `tasks.md` | Executable task list with parallelism annotations |
| `quickstart.md` | Key validation scenarios confirming the feature works end-to-end |
