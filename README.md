# Agent Configuration

Shared agent configuration for AI coding assistants. Language-agnostic, tool-agnostic instructions for autonomous coding work. One source of truth, symlinked to each tool's expected location.

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
├── agents/                # Named agent modes (for delegation via task tool)
│   ├── conductor.md       # Master orchestrator — decomposes tasks, delegates to subagents
│   ├── explorer.md        # Read-only project exploration
│   ├── implementer.md      # Full-capability implementation — writes code, runs commands
│   ├── planner.md         # Analysis and planning — designs solutions, creates plans
│   ├── reviewer.md         # Read-only code review — quality, security, performance
│   └── tester.md          # Test engineering — writes and runs tests
├── commands/              # Slash commands
│   ├── refactor.md        # /refactor — readability, safety, performance, maintainability
│   └── verify-project.md  # /verify-project — format, lint, vulnerability scan, tests
└── skills/                # Conditional skill modules loaded by context
    ├── code-quality/      # Readability, clean code, naming
    ├── context-management/ # Long sessions, context limits, compaction, quality maintenance
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
- **Architecture** — Modular by default, test first, simple (≤3 top-level modules), no speculative features

### Named Agents

Agents available for delegation via the `task` tool. All agents are language-agnostic and operate on generic code structures (files, functions, classes, modules, interfaces, data structures, collections).

| Agent | Mode | Purpose | Permissions |
|-------|------|---------|-------------|
| `conductor` | primary | Master orchestrator — decomposes tasks, delegates to subagents, validates outputs | No edits, no shell commands |
| `explorer` | subagent | Read-only project exploration — finds files, searches content, maps architecture | No edits, no shell commands |
| `implementer` | subagent | Full-capability implementation — writes code, edits files, runs commands | Full edit, write, shell commands |
| `planner` | subagent | Analysis and planning — designs solutions, creates implementation plans, estimates scope | Read-only for production code; can write plan files to `plans/` |
| `reviewer` | subagent | Code review — quality, security, performance, best practices | Read-only (+ git diff/log) |
| `tester` | subagent | Test engineering — writes and runs tests, validates against acceptance criteria | Edit/write (test files), full shell access |

### Slash Commands

| Command | Description |
|---------|-------------|
| `/refactor` | Refactor code for readability, safety, performance, and maintainability |
| `/verify-project` | Format, lint (auto-fix), vulnerability scan, static analysis, and run tests |

### Skills

Conditional rule modules loaded when context matches. Each skill is a `SKILL.md` file in `skills/<name>/`.

| Skill | Trigger Context |
|-------|-----------------|
| `code-quality` | Readability, clean code, naming discussions |
| `context-management` | Long sessions, context limits, compaction, context quality |
| `naming-conventions` | Writing or reviewing identifier names |
| `performance` | Performance optimization discussions |
| `self-organizing-coder` | Task decomposition, subagent delegation, iterative delivery |
| `spec-driven` | Planning features, writing specs, spec-first workflows |

## Context Condensing

For complex projects, context management is critical. Kilo Code provides automatic compaction:

- **Auto-compaction** triggers when the conversation approaches the model's token limit (default: ~20K headroom reserved).
- **Pruning** clears old tool outputs beyond a ~40K recency window between turns.
- **Manual compaction** via `/compact` slash command (also searchable as `smol` or `condense`).

### Configuration Reference

Kilo `kilo.jsonc` settings:

```jsonc
{
  "compaction": {
    "auto": true,      // Enable/disable automatic compaction
    "prune": true,     // Clear old tool outputs beyond recency window
    "reserved": 20000  // Token buffer for next turn
  }
}
```

Optional dedicated compaction agent:

```jsonc
{
  "agent": {
    "compaction": {
      "model": "anthropic/claude-haiku-4-5"
    }
  }
}
```

Environment overrides:

| Variable | Effect |
|----------|--------|
| `KILO_DISABLE_AUTOCOMPACT=1` | Forces `compaction.auto = false` |
| `KILO_DISABLE_PRUNE=1` | Forces `compaction.prune = false` |

### Best Practices

- Compact **before major transitions** (exploration → planning → implementation → validation).
- Compact **after completing significant milestones**.
- Be **specific in initial task descriptions** — this feeds better summaries.
- Use **subdirectory `AGENTS.md`** for domain-specific context that doesn't need to be compacted.
- After compaction, **re-read modified files** to avoid stale assumptions.
- Use **`todowrite`** for progress tracking — external tracking survives context compaction.

## Large Project Strategies

When working with large, complex projects:

- **Navigation** — Use `glob` and `grep` to find files by pattern, locate patterns across the project. Build mental model of module boundaries before making changes.
- **Incremental Changes** — Work within modular boundaries. Small, verifiable changes over broad refactoring. Ship each step. Update shared interfaces across all callers together.
- **Context Efficiency** — Reference specific files with paths. Break large tasks into smaller subtasks. Summarize large code sections in prompts rather than including full content. Use `/compact` manually before major transitions.
- **Working with Unfamiliar Code** — Read the module's public interface first. Trace call chains to understand data flow. Identify core domain types and relationships. Look for tests to understand expected behavior.

## Planned Skills (Not Yet Implemented)

The following skills are described in the desired-state but not yet implemented:

| Skill | Purpose |
|-------|---------|
| `error-design` | Error types, wrapping, actionable messages |
| `incremental-delivery` | Feature flags, small PRs, progressive rollout |
| `library-first` | Architecture design, new feature structure |
| `security-by-default` | Input handling, auth, file access, secrets |
| `simplify` | Refactoring, reducing technical debt, unnecessary complexity |
| `test-first` | TDD workflow, writing tests before implementation |

## References

- Kilo customize: https://kilo.ai/docs/customize
- Kilo context condensing: https://kilo.ai/docs/customize/context/context-condensing
- OpenCode tools: https://opencode.ai/docs/tools/
