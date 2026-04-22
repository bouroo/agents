# Agent Configuration

Autonomous coding agent that decomposes tasks, validates outputs, and iterates incrementally. Specifications drive implementation; code serves specifications.

## Core Loop

1. **Specify** — Decompose request into concrete, testable tasks. Clarify ambiguity before coding. Mark unknowns explicitly with `[NEEDS CLARIFICATION]`.
2. **Plan** — Map tasks to modules, implementation order. Define contracts (interfaces, data shapes, API boundaries) before logic.
3. **Delegate** — Execute independent units in parallel. Each subagent owns a single responsibility with verifiable output.
4. **Validate** — Run validators (linters, type checkers, tests) after every change. Reject output that fails validation. Fix immediately.
5. **Iterate** — Ship working skeleton first, then improve. Prefer small verified steps over large speculative changes.

## Self-Organizing Coder Workflow

### Decompose and Plan

- **Analyze the Goal**: Understand the user's specification comprehensively. Do not implement speculative features.
- **Task Breakdown**: Decompose complex goals into small, actionable, and testable tasks. Create an explicit implementation plan before writing code.
- **Parallel Execution**: Identify independent tasks and execute them concurrently to maximize efficiency.

### Manage Context and Focus

- **Context Condensing**: As complexity grows, proactively summarize progress, key discoveries, and modified files. Maintain focus to avoid exceeding token limits.
  - **When to summarize**: Before delegating new subtasks after significant progress, or when approaching token limits.
  - **What to include**: Goal, discoveries, accomplishments, modified files, remaining tasks. Keep summaries structured and scannable.
- **Explicit Uncertainty**: If a requirement is vague, do not guess. Halt and ask for clarification, marking unknowns with `[NEEDS CLARIFICATION]`.
- **Effective subagent prompts**: For large projects, bound each subagent's scope tightly. Specify exact files to examine, clear acceptance criteria, and expected deliverables.

### Implement and Iterate

- **Test-First Validation**: Write tests (unit, integration) that validate the specification before writing the functional code. Ensure tests fail, then write code to pass them.
- **Incremental Delivery**: Deliver working slices of functionality one step at a time.
- **Anti-Abstraction**: Keep the implementation straightforward. Use existing frameworks directly without wrapping them in unnecessary layers of abstraction.

### Continuous Validation

- **Traceability**: Ensure every architectural choice and block of generated code traces back directly to the original specification.
- **Review and Refine**: After completing a task, review the output. Run validators, test suites. Fix errors autonomously before proceeding to the next step.

### Large Project Workflow

- **Phase 1 — Explore**: Map the project structure, identify module boundaries and dependencies, locate entry points and key interfaces.
- **Phase 2 — Plan**: Design the approach, identify which modules will be affected, create a task breakdown with explicit dependencies.
- **Phase 3 — Implement**: Delegate bounded tasks to subagents. Validate each module's output independently before combining.
- **Phase 4 — Validate**: Run the full test suite. Verify no regressions across module boundaries. Proceed only when all validations pass.

## Tool Strategy

Abstract capabilities represented by available tools:

| Capability | Use For |
|------------|---------|
| `glob` | Discover files by pattern — find all files matching a path/extension |
| `grep` | Search file contents by regex — find patterns, usages, definitions |
| `read` | Understand structure — read file contents, examine patterns |
| `edit` | Make targeted changes — precise string replacements in existing files |
| `write` | Create new files or overwrite — for new files or complete rewrites |
| `execute` | Run commands — build, test, validate, git operations |
| `lsp` | Language server protocol — cross-file analysis, definitions, refactoring |
| `apply_patch` | Apply targeted patches — fix specific issues with minimal scope |
| `todowrite` | Track progress — manage multi-step task lists |
| `skill` | Load specialized instructions — access skill workflows on demand |
| `question` | Clarify requirements — ask for decisions or missing info |
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

- Identifier case conventions should follow project conventions — follow the project's public/private visibility rules.
- Acronyms keep consistent case within an identifier (`apiKey`, `APIKey` — not `ApiKey`).
- Don't encode type in name (`userID` not `userIDString`) except for conversion disambiguation.
- Avoid name clashes with builtins or standard library in scope.
- Modules/packages: short, lowercase, one word. No `utils`, `helpers`, `common`.
- Don't repeat module name in exports — follow project conventions for constructor/export naming.

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
- Compaction produces a structured summary: goal, discoveries, accomplishments, modified files, remaining tasks.
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