# Self-Organizing Coder Agent

Shared agent configuration for Claude Code, Gemini, OpenCode, and Kilo. One source of truth, symlinked to each tool's expected location.

## Structure

```
~/.agents/
├── AGENTS.md              # Core agent instructions (symlinked to each tool)
├── link.sh                # Bootstrap: creates symlinks for all supported tools
├── agents/                # Named agent modes (OpenCode/Kilo)
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

## Setup

```bash
~/.agents/link.sh
```

Creates symlinks for all supported tools:

| Tool | Config dir | Agent file |
|------|-----------|------------|
| Claude Code | `~/.claude/` | `CLAUDE.md` |
| Gemini | `~/.gemini/` | `GEMINI.md` |
| OpenCode | `~/.config/opencode/` | `AGENTS.md` |
| Kilo | `~/.config/kilo/` | `AGENTS.md` |
| Qwen | `~/.qwen/` | `AGENTS.md` |

The script also symlinks `commands/`, `skills/`, and `agents/` directories where the tool supports them.

## Agent Design

**AGENTS.md** is the top-level instruction file. It defines:

- **Execution loop** — Understand → Research → Plan → Test First → Implement → Verify → Iterate
- **Specification-Driven Development** — Specs are truth; code is their expression
- **Library-First Architecture** — Features begin as standalone libraries
- **Test-First** — Tests written before implementation, always
- **Code Standards** — Readability, naming, performance, security, error handling
- **Performance Awareness** — Preallocation, zero-copy, buffered I/O, benchmarking
- **Concurrency** — Structured concurrency, confinement over sharing, no globals

## Agents

Named agent modes available for delegation via the `task` tool:

| Agent | Mode | Purpose |
|-------|------|---------|
| `conductor` | Primary | Decomposes complex tasks, delegates to subagents, delivers working increments |

## Commands

Slash commands available in supported tools:

| Command | Description |
|---------|-------------|
| `/refactor` | Refactor code for readability, safety, performance, and maintainability |
| `/verify-project` | Format, lint (auto-fix), vulnerability scan, static analysis, and run tests |
| `/vb-review` | Virtual Banking Mobile Backend review — comprehensive Go/Kafka/Postgres/Mongo/Redis/K8s checks |

## Skills

Skills are conditional rule modules loaded when context matches. Each skill lives in `skills/<name>/SKILL.md`.

| Skill | Trigger |
|-------|---------|
| `code-quality` | Readability, clean code, naming |
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

Every non-trivial feature produces this structure under `specs/<feature-slug>/`:

| File | Purpose |
|------|---------|
| `spec.md` | Requirements, constraints, interfaces, error cases, out-of-scope |
| `plan.md` | Architecture overview, requirement-to-decision mapping, rationale |
| `data-model.md` | Schema definitions, entity relationships, type contracts |
| `contracts/` | API specs, event definitions, function signatures |
| `research.md` | Technical investigation findings, library evaluations |
| `tasks.md` | Executable task list with parallelism annotations |
| `quickstart.md` | Key validation scenarios confirming the feature works end-to-end |
