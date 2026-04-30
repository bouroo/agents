# Agent Configuration

Shared agent instructions for AI coding assistants. Language-agnostic, tool-agnostic configuration symlinked to each tool's expected location.

## Quick Start

```bash
~/.agents/link.sh
```

Creates symlinks for all supported tools. Run once after cloning or updating.

## Directory Structure

```
~/.agents/
├── AGENTS.md              # Core agent instructions (symlinked)
├── README.md              # This file
├── link.sh                # Bootstrap script
├── agents/                # Named agent modes for delegation
│   ├── conductor.md       # Master orchestrator — decomposes and delegates tasks
│   ├── explorer.md        # Read-only project exploration
│   ├── implementer.md     # Full implementation — writes code, runs commands
│   ├── planner.md         # Analysis and planning
│   ├── reviewer.md        # Code review — quality, security, performance
│   └── tester.md          # Test engineering
├── commands/              # Slash commands
│   ├── refactor.md        # /refactor
│   ├── vb-review.md       # /vb-review — mobile backend checklist
│   └── verify-project.md  # /verify-project — format, lint, scan, test
└── skills/                # Conditional modules loaded by context
    ├── code-quality/      # Readability, clean code, naming
    ├── context-management/ # Context limits, compaction, quality
    ├── naming-conventions/ # Language-agnostic naming
    ├── performance/       # Optimization patterns
    ├── self-organizing-coder/ # Task decomposition, delegation
    └── spec-driven/       # Spec-driven development workflow
```

## Supported Tools

| Tool | Config Location | Agent File |
|------|-----------------|------------|
| Claude Code | `~/.claude/` | `CLAUDE.md` |
| Gemini | `~/.gemini/` | `GEMINI.md` |
| Kilo | `~/.config/kilo/` | `AGENTS.md` |
| OpenCode | `~/.config/opencode/` | `AGENTS.md` |
| Qwen | `~/.qwen/` | `AGENTS.md` |

The `link.sh` script symlinks `AGENTS.md`, `commands/`, `skills/`, and `agents/` to each tool's directory.

## Agents

Delegatable agents available via the `task` tool:

| Agent | Role | Purpose | Permissions |
|-------|------|---------|-------------|
| `conductor` | primary | Orchestrates — decomposes tasks, delegates, validates | read-only |
| `explorer` | subagent | Project exploration — finds files, maps architecture | read-only |
| `implementer` | subagent | Implementation — writes code, edits, runs commands | full access |
| `planner` | subagent | Analysis — designs solutions, estimates scope | read-only |
| `reviewer` | subagent | Code review — quality, security, performance | read-only |
| `tester` | subagent | Test engineering — writes and runs tests | test files + shell |

## Slash Commands

| Command | Description |
|---------|-------------|
| `/refactor` | Refactor for readability, safety, performance |
| `/vb-review` | Mobile backend review checklist |
| `/verify-project` | Format, lint, scan, test |

## Skills

Conditional modules loaded when context matches:

| Skill | Trigger |
|-------|---------|
| `code-quality` | Readability, naming discussions |
| `context-management` | Long sessions, compaction |
| `naming-conventions` | Writing identifier names |
| `performance` | Performance optimization |
| `self-organizing-coder` | Task decomposition, delegation |
| `spec-driven` | Planning, spec-first workflows |

## Context Condensing

### Auto-Compaction

- **Triggers** at ~20K token headroom (configurable)
- **Pruning** clears tool outputs beyond ~40K recency
- **Manual** via `/compact` command

### Configuration

```jsonc
{
  "compaction": {
    "auto": true,
    "prune": true,
    "reserved": 20000
  }
}
```

### Environment Overrides

| Variable | Effect |
|----------|--------|
| `KILO_DISABLE_AUTOCOMPACT=1` | Disable auto-compaction |
| `KILO_DISABLE_PRUNE=1` | Disable pruning |

### Best Practices

- Compact before major transitions
- Compact after milestones
- Be specific in task descriptions
- Use `todowrite` for external progress tracking
- Re-read modified files after compaction

## Large Project Strategies

- **Navigate** with `glob` and `grep` — find files, locate patterns, build mental model of boundaries
- **Change incrementally** — work within modular boundaries, ship each step
- **Be context-efficient** — reference specific files, break tasks into subtasks, summarize large code
- **Understand unfamiliar code** — read public interface first, trace call chains, find tests

## Planned Skills

| Skill | Purpose |
|-------|---------|
| `error-design` | Error types, wrapping, actionable messages |
| `incremental-delivery` | Feature flags, small PRs, rollout |
| `library-first` | Architecture design, new features |
| `security-by-default` | Input handling, auth, secrets |
| `simplify` | Refactoring, technical debt |
| `test-first` | TDD workflow |

## References

- [Kilo Docs](https://kilo.ai/docs/)
- [OpenCode Tools](https://opencode.ai/docs/tools/)
- [Structured Prompt Driven](https://martinfowler.com/articles/structured-prompt-driven/)