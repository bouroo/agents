# Self-Organizing Coder Agent

Shared agent configuration for Claude Code, Gemini, OpenCode, and Kilo. One source of truth, symlinked to each tool's expected location.

## Structure

```
~/.agents/
├── AGENTS.md          # Core agent instructions (symlinked to each tool)
├── link.sh            # Bootstrap: creates symlinks for all supported tools
├── agents/            # Named agent modes (OpenCode/Kilo)
│   └── conductor.md   # Orchestrator — waves of parallel subagent work
├── commands/          # Slash commands (e.g. /spec, /code-review)
│   ├── spec.md
│   ├── code-review.md
│   ├── verify-project.md
│   └── refactor-optimize.md
└── skills/            # Conditional skill modules loaded by context
    ├── go-excellence/
    ├── spec-driven-dev/
    ├── test-first/
    ├── library-first/
    ├── security-by-default/
    ├── error-design/
    ├── code-quality/
    ├── context-management/
    ├── incremental-delivery/
    └── prompt-engineering/
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

## Agent Design

**AGENTS.md** is the top-level instruction file. It defines:

- **Execution loop** — Understand → Plan → Execute → Verify → Iterate
- **Specification-Driven Development** — Specs are truth; code is their expression
- **Constitutional Foundation** — Six non-negotiable implementation gates
- **Library-First Architecture** — Features begin as standalone libraries
- **Test-First** — Tests written before implementation, always
- **Code Standards** — Style hierarchy, naming, performance, security

### Constitutional Foundation

| Article | Rule |
|---------|------|
| I | Every feature begins as a standalone library with a clean interface |
| II | Libraries expose functionality through CLI/API interfaces producing structured output |
| III | Test-First: tests written and approved before any implementation code |
| VII | Simplicity: max 3 active projects; complexity requires documented justification |
| VIII | Anti-Abstraction: use framework features directly; one model per concept |
| IX | Integration-First Testing: real databases and actual services; no mocks at boundaries |

## Commands

Slash commands available in supported tools:

| Command | Description |
|---------|-------------|
| `/spec` | Transform a feature description into a gated spec → plan → tasks pipeline |
| `/code-review` | Review code for quality, security, and performance |
| `/verify-project` | Validate project health, deps, lint, security, and tests |
| `/refactor-optimize` | Refactor and optimize code feature-by-feature |

## Skills

Skills are conditional rule modules loaded when context matches. Each skill lives in `skills/<name>/SKILL.md`.

| Skill | Trigger |
|-------|---------|
| `go-excellence` | Go codebases — naming, performance, concurrency, security |
| `spec-driven-dev` | Planning features, writing specs, PRDs |
| `test-first` | TDD workflow, writing tests before implementation |
| `library-first` | Architecture design, new feature structure |
| `security-by-default` | Input handling, auth, file access, secrets |
| `error-design` | Error types, wrapping, actionable messages |
| `code-quality` | Readability, clean code, naming |
| `context-management` | Long sessions, context limits, compaction |
| `incremental-delivery` | Feature flags, small PRs, progressive rollout |
| `prompt-engineering` | AI prompting, few-shot examples, task decomposition |

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
