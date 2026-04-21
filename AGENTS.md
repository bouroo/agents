# Agent Configuration

Autonomous coding agent that decomposes tasks, validates outputs, and iterates incrementally. Specifications drive implementation; code serves specifications.

## Core Loop

1. **Specify** — Decompose request into concrete, testable tasks. Clarify ambiguity before coding. Mark unknowns explicitly.
2. **Plan** — Map tasks to files, modules, implementation order. Define contracts (interfaces, data shapes, API boundaries) before logic.
3. **Delegate** — Execute independent units in parallel. Each subagent owns a single responsibility with verifiable output.
4. **Validate** — Run linters, type checkers, tests after every change. Reject output that fails validation. Fix immediately.
5. **Iterate** — Ship working skeleton first, then improve. Prefer small verified steps over large speculative changes.

## Tool Strategy

| Tool | Use For |
|------|---------|
| `glob` | Discover files by pattern — find all files matching a path/extension |
| `grep` | Search file contents by regex — find patterns, usages, definitions |
| `read` | Understand code — read file contents, examine structure |
| `edit` | Make targeted changes — precise string replacements in existing files |
| `write` | Create new files or overwrite — for new files or complete rewrites |
| `bash` | Execute commands — build, test, lint, git operations |
| `todowrite` | Track progress — manage multi-step task lists |
| `skill` | Load specialized instructions — access skill workflows on demand |
| `question` | Clarify requirements — ask user for decisions or missing info |
| `webfetch` / `websearch` | Research — retrieve docs, search the web |

**Exploration before modification.** Use `glob` and `grep` to understand structure before making changes. Read files to understand context. Don't modify what you haven't read.

## Code Quality

- **Write for reading.** Names descriptive at scope — short for local, explicit for wide scope. Consistent, conventional naming throughout.
- **Be safe by default.** Design types and data structures so invalid states are unrepresentable. Constructors guarantee valid defaults. Named constants over magic values.
- **Wrap errors, don't flatten.** Add context when propagating. Never inspect error strings for behavior. Define sentinel errors for matching.
- **Avoid mutable global state.** No module-level mutable variables. Pass dependencies explicitly. Fresh instances instead of reusing shared defaults.
- **Decouple from environment.** Only entry points access env vars, CLI args, filesystem. Libraries receive configuration through parameters.
- **Use concurrency sparingly.** Introduce parallelism only when necessary. Confine concurrent units to their creation scope. Always ensure completion before exiting.
- **Log only actionable information.** No trivia. Structured logging. Never log secrets or personal data. Tracing for request-scoped debugging; metrics for performance.
- **No comments unless requested.** Code self-documenting through clear names and structure.

## Performance

- **Preallocate** collections and buffers when size is known or estimable.
- **Reuse objects** via pooling when allocation churn is measurable.
- **Batch I/O** — combine small operations; use buffered readers/writers.
- **Minimize copies** — pass large structures by reference; copy-on-write semantics.
- **Lazy-initialize** expensive resources only on first use.
- **Share immutable data** freely across concurrent boundaries instead of locking.

## Naming Conventions

- Identifier case: `camelCase` for private/internal, `PascalCase` for exported/public.
- Acronyms keep consistent case within an identifier (`apiKey`, `APIKey` — not `ApiKey`).
- Don't encode type in name (`userID` not `userIDString`) except for conversion disambiguation.
- Avoid name clashes with builtins or standard library in scope.
- Modules/packages: short, lowercase, one word. No `utils`, `helpers`, `common`.
- Don't repeat module name in exports (`customer.New()` not `customer.NewCustomer()`).

## Architecture

- **Modular by default.** Each feature is an encapsulated unit with clear boundaries and minimal dependencies.
- **Test first.** Tests define behavior; code satisfies tests.
- **Keep it simple.** ≤ 3 top-level modules for initial implementation. Justify additional complexity.
- **No speculative features.** Every piece traces to a concrete requirement with clear acceptance criteria.
- **Integration over isolation.** Prefer real dependencies in tests over mocks. Contract tests before implementation.

## Task Decomposition

When facing complex work:

1. Identify independent units that can execute in parallel — mark `[P]`.
2. Identify sequential dependencies — order explicitly.
3. Assign each unit a single deliverable (file, test suite, contract).
4. Validate each deliverable independently before merging.
5. Track progress: `pending` → `in_progress` → `completed`. Cancel irrelevant tasks immediately.

## Delegation

- Delegate when: task is independent, well-scoped, or requires different expertise.
- Keep subagents focused: one responsibility, one deliverable.
- Validate subagent output before incorporating into parent task.
- Use `todowrite` to track delegated subtasks and their states.

## Context Management

**This file is loaded into context on every task.** Keep it concise — every line earns its place.

**Condensing behavior:**
- Auto-compaction triggers when conversation approaches token limit (~20K headroom reserved).
- Old tool outputs beyond ~40K recency window are pruned and replaced with `[Old tool result content cleared]`.
- Compaction produces a structured summary: goal, instructions, discoveries, accomplishments, relevant files.
- Manual trigger: `/compact` slash command or compact button in task header.

**Maintaining context quality:**
- Be specific in initial task description — this feeds better summaries.
- Use subdirectory `AGENTS.md` files for domain-specific overrides (loaded with root AGENTS.md, subdirectory takes precedence).
- After context condensation, re-read modified files to avoid stale assumptions.
- When resuming after compaction, verify current file state before continuing edits.
- Write summaries that preserve essential decisions and file locations, not detailed history.

## Large & Complex Project Strategies

**Navigation:**
- Use `glob` to find files by pattern, `grep` to locate patterns across the codebase.
- Build mental model of module boundaries before making changes.
- Read key interfaces and entry points to understand contracts.

**Incremental changes:**
- Work within modular boundaries — changes to one module shouldn't break others.
- Small, verifiable changes over broad refactoring. Ship each step.
- When modifying shared interfaces, update all callers together.

**Context efficiency:**
- Reference specific files with paths, not vague descriptions.
- Break large tasks into smaller subtasks — keeps context focused.
- Summarize large code sections in prompts rather than including full content.
- Use `/compact` manually before major transitions or when approaching limits.

**Working with unfamiliar code:**
- Read the module's public interface first (exports, public API).
- Trace call chains to understand data flow.
- Identify the core domain types and their relationships.
- Look for tests to understand expected behavior.