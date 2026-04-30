# Agent Configuration

Autonomous coding agent. Specifications drive implementation; code serves specifications.

## Core Loop

1. **Specify** — Decompose requests into concrete, testable tasks. Clarify ambiguity before coding.
2. **Align** — Lock intent: define what will be done, what won't be done, standards, and hard constraints. Ensure spec and understanding are synchronized before implementation.
3. **Plan** — Map tasks to modules. Define contracts (interfaces, data shapes, API boundaries) before logic. Design abstractions before generating code.
4. **Delegate** — Execute independent units in parallel. Each subagent owns one responsibility with verifiable output.
5. **Validate** — Run validators after every change. Reject output that fails validation. Fix immediately.
6. **Sync** — When implementation diverges from spec, fix the spec first for logic changes, then regenerate. For refactoring, update code then sync spec. Keep prompt assets and code synchronized.

## SPDD Principles

Structured Prompt-Driven Development treats specifications and prompts as first-class delivery artifacts — version controlled, reviewed, reusable.

- **Abstraction-first**: Design objects, collaborations, and boundaries before generating code. Unclear responsibilities lead to duplicated logic and inconsistent interfaces.
- **Alignment before implementation**: Make "what we will do / what we won't do" explicit. Agree on standards and hard constraints up front. Fast output with wrong intent produces slow rework.
- **Iterative review**: Treat AI output as a controlled loop, not a one-shot draft. Review intent alignment before reviewing code details.
- **Prompt-code sync**: Logic corrections update the spec first, then code. Refactoring updates code first, then syncs back to spec. Neither side silently diverges.
- **Accumulated context**: Successful patterns and decisions compound across iterations, reducing variability and building team expertise.

## Context Management

This file is loaded into context on every task. Keep it concise — every line earns its place.

**Condensing behavior:**
- Auto-compaction triggers when total tokens fill the context window minus a reserved buffer (~20K tokens or model max output, whichever is smaller).
- Pruning replaces old tool outputs beyond a 40K-token recency window with `[Old tool result content cleared]`.
- Compaction keeps the most recent user turns verbatim (default: 2 turns, within a token budget of 25% usable context clamped to 2K–8K tokens).
- Manual trigger: `/compact` slash command or compact button in task header.
- Can configure a dedicated compaction model via `agent.compaction.model` in kilo.jsonc.

**Maintaining context quality:**
- Be specific in initial task descriptions for better summaries.
- Use subdirectory `AGENTS.md` files for domain-specific overrides (subdirectory takes precedence).
- After context condensation, re-read modified files to avoid stale assumptions.
- When resuming after compaction, verify current file state before continuing edits.
- Write summaries that preserve essential decisions and file locations, not detailed history.

## Delegation

Identify available subagents from your environment. Delegate based on purpose:

| Purpose | Delegate to |
|---|---|
| Read-only exploration — find files, map architecture | Exploration-capable subagent |
| Implementation — write code, edit files, run commands | Implementation-capable subagent |
| Code review — quality, security, performance | Review-capable subagent |
| Test engineering — write and run tests | Testing-capable subagent |
| Analysis and planning — design solutions, create plans | Planning-capable subagent |

### Rules

- Match task to subagent by capability, not by name.
- Chain subagents for complex work: exploration → planning → implementation → testing → review.
- Launch multiple subagents concurrently when subtasks are independent.
- Keep subagent prompts self-contained — they start with fresh context.

## Tool Strategy

Discover available tools from your environment. Use tools by purpose:

| Purpose | Tool Category |
|---|---|
| Discover files by pattern | File search |
| Search file contents by pattern | Content search |
| Read files and directories | File reading |
| Make targeted changes | File editing |
| Create new files | File writing |
| Run commands — build, test, validate | Command execution |
| Cross-file analysis, definitions, references | Language server |
| Apply targeted patches | Patch application |
| Track progress on multi-step tasks | Task tracking |
| Load specialized instructions | Skill loading |
| Clarify requirements from user | User interaction |
| Fetch content from URLs | Web fetching |
| Search the web for information | Web search |

**Exploration before modification.** Understand structure before making changes. Read files to understand context. Don't modify what you haven't read.

## Code Quality

- **Write for reading.** Descriptive names at wide scope, short at local scope.
- **Be safe by default.** Invalid states should be unrepresentable. Constructors guarantee valid defaults.
- **Wrap errors, don't flatten.** Add context when propagating. Define sentinel errors for matching.
- **Avoid mutable global state.** Pass dependencies explicitly.
- **Decouple from environment.** Only entry points access env vars, CLI args, filesystem.
- **Use concurrency sparingly.** Confine concurrent units to their creation scope.
- **Log only actionable information.** Structured logging. Never log secrets.
- **No comments unless requested.** Code self-documenting through clear names.

## Performance

- **Preallocate** collections when size is known.
- **Reuse objects** via pooling when allocation churn is measurable.
- **Batch I/O** — combine small operations.
- **Minimize copies** — pass large structures by reference.
- **Lazy-initialize** expensive resources only on first use.
- **Share immutable data** freely across concurrent boundaries.
- **Escape Analysis** avoiding unnecessary heap allocation.

## Architecture

- **Modular by default.** Clear boundaries, minimal dependencies.
- **Test first.** Tests define behavior; code satisfies tests.
- **Keep it simple.** ≤ 3 top-level modules for initial implementation.
- **No speculative features.** Every piece traces to a concrete requirement.
- **Integration over isolation.** Prefer real dependencies in tests over mocks.
- **Design before generate.** Clarify objects, collaborations, and boundaries before writing code. Abstraction-first prevents structural debt.

## Task Decomposition

When facing complex work:

1. Identify independent units — mark `[P]`.
2. Identify sequential dependencies — order explicitly.
3. Align on intent: what will be done, what won't be done, constraints.
4. Assign each unit a single deliverable.
5. Validate each deliverable independently before merging.
6. Sync: if implementation diverges from spec, fix spec first for logic changes.
7. Track progress: `pending` → `in_progress` → `completed`.

## Large Project Workflow

1. **Explore** — Map structure, identify module boundaries, locate entry points.
2. **Plan** — Design approach, identify affected modules, create task breakdown.
3. **Implement** — Delegate bounded tasks. Validate each module independently.
4. **Validate** — Run full test suite. Verify no regressions across boundaries.

**Context efficiency:**
- Reference specific files with paths, not vague descriptions.
- Break large tasks into smaller subtasks — keeps context focused.
- Summarize large code sections in prompts rather than including full content.
- Use `/compact` manually before major transitions or when approaching limits.

**Working with unfamiliar code:**
- Read the module's public interface first (exports, public API).
- Trace call chains to understand data flow.
- Identify core domain types and relationships.
- Look for tests to understand expected behavior.
