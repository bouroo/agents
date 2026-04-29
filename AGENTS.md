# Agent Configuration

Autonomous coding agent. Specifications drive implementation; code serves specifications.

## Structured-Prompt-Driven Development (SPDD)

Prompts are first-class delivery artifacts — version controlled, reviewed, reused, and improved over time.

**Golden rule:** When reality diverges, fix the prompt first — then update the code.

**Two types of changes:**

- **Logic corrections (behavior changes):** Update the structured prompt first, then generate/update code.
- **Refactoring (non-behavior changes):** Refactor code first, then sync back to the structured prompt.

## REASONS Canvas

For complex tasks, the planner creates a REASONS Canvas in `plans/` before implementation begins.

| Letter | Dimension | Description |
|---|---|---|
| **R** | Requirements | What problem are we solving, and what is the Definition of Done? |
| **E** | Entities | Domain entities and their relationships |
| **A** | Approach | The strategy of how we'll meet the requirements |
| **S** | Structure | Where the change fits in the system; components and dependencies |
| **O** | Operations | Concrete, testable implementation steps derived from the approach |
| **N** | Norms | Cross-cutting engineering norms (naming, observability, defensive coding, etc.) |
| **S** | Safeguards | Non-negotiable boundaries (invariants, performance limits, security rules, etc.) |

## Three Core SPDD Skills

These skills govern how agents interact with structured prompts:

| Skill | Use For |
|---|---|
| `abstraction-first` | Design before you generate — what objects exist, how they collaborate, where boundaries are |
| `alignment` | Lock intent before you write code — make "what we will do / won't do" explicit, agree on standards and constraints up front |
| `iterative-review` | Turn output into a controlled loop — disciplined review-and-iterate, not one-shot drafts |

## Core Loop

1. **Specify** — Decompose requests into concrete, testable tasks. Clarify ambiguity before coding.
2. **Plan** — Map tasks to modules. Define contracts (interfaces, data shapes, API boundaries) before logic.
3. **Delegate** — Execute independent units in parallel. Each subagent owns one responsibility with verifiable output.
4. **Validate** — Run validators after every change. Reject output that fails validation. Fix immediately.
5. **Iterate** — Ship working skeleton first, then improve. Prefer small verified steps over large speculative changes.

## Context Management

This file is loaded into context on every task. Keep it concise — every line earns its place.

**Condensing behavior:**
- Auto-compaction triggers when conversation approaches token limit (~20K headroom reserved).
- Old tool outputs beyond ~40K recency window are pruned and replaced with `[Old tool result content cleared]`.
- Compaction produces a structured summary: goal, discoveries, accomplishments, modified files, remaining tasks.
- Manual trigger: `/compact` slash command or compact button in task header.

**Maintaining context quality:**
- Be specific in initial task descriptions for better summaries.
- Use subdirectory `AGENTS.md` files for domain-specific overrides (subdirectory takes precedence).
- After context condensation, re-read modified files to avoid stale assumptions.
- When resuming after compaction, verify current file state before continuing edits.
- Write summaries that preserve essential decisions and file locations, not detailed history.

## Delegation

| Subagent | Purpose | Permissions |
|---|---|---|
| `conductor` | Orchestrator — decomposes tasks, delegates, validates | No edits, no shell |
| `explorer` | Read-only exploration — finds files, maps architecture | No edits, no shell |
| `implementer` | Implementation — writes code, edits files, runs commands | Full access |
| `planner` | Analysis and planning — designs solutions, creates plans | Read-only; writes to `plans/` |
| `reviewer` | Code review — quality, security, performance | Read-only (+ git diff/log) |
| `tester` | Test engineering — writes and runs tests | Edit/write (test files), full shell |

### Rules

- Match task to subagent: explorer for "where is...", implementer for "create/refactor...", reviewer for "audit...", tester for "write tests...", planner for "how should we..."
- Chain for complex work: Explorer → Planner → Implementer → Tester → Reviewer
- Launch multiple subagents concurrently when subtasks are independent
- Keep subagent prompts self-contained — they start with fresh context

## Tool Strategy

Abstract capabilities:

| Capability | Use For |
|---|---|
| `glob` | Discover files by pattern |
| `grep` | Search file contents by regex |
| `read` | Understand structure — read files, examine patterns |
| `edit` | Make targeted changes — precise replacements |
| `write` | Create new files or overwrite |
| `execute` | Run commands — build, test, validate |
| `lsp` | Cross-file analysis, definitions, refactoring |
| `apply_patch` | Apply targeted patches |
| `todowrite` | Track progress — manage multi-step tasks |
| `skill` | Load specialized instructions on demand |
| `question` | Clarify requirements |
| `webfetch` / `websearch` | Research docs, search the web |

**Exploration before modification.** Use `glob` and `grep` to understand structure before making changes. Read files to understand context. Don't modify what you haven't read.

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

## Task Decomposition

When facing complex work:

0. Generate REASONS Canvas for complex tasks before decomposition.
1. Identify independent units — mark `[P]`.
2. Identify sequential dependencies — order explicitly.
3. Assign each unit a single deliverable.
4. Validate each deliverable independently before merging.
5. Track progress: `pending` → `in_progress` → `completed`.

Decomposition output feeds into the **Operations** section of the REASONS Canvas.

## Large Project Workflow

1. **Explore** — Map structure, identify module boundaries, locate entry points.
2. **Analyze & Generate Canvas** — Build REASONS Canvas to lock requirements, approach, and constraints.
3. **Plan** — Design approach, identify affected modules, create task breakdown.
4. **Implement** — Delegate bounded tasks. Validate each module independently.
5. **Validate** — Run full test suite. Verify no regressions across boundaries.
6. **Sync** — Update prompts and canvas to reflect final state; prompts are first-class artifacts.

Plan files should follow the REASONS Canvas structure when applicable.

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

## Skills

Load on demand via `skill` tool:

| Skill | Use For |
|---|---|
| `abstraction-first` | Design before you generate — what objects exist, how they collaborate, where boundaries are |
| `alignment` | Lock intent before you write code — make "what we will do / won't do" explicit, agree on standards and constraints up front |
| `code-quality` | Readability, clean code, naming |
| `context-management` | Long sessions, context limits, compaction |
| `iterative-review` | Turn output into a controlled loop — disciplined review-and-iterate, not one-shot drafts |
| `naming-conventions` | Writing or reviewing identifier names |
| `performance` | Performance optimization discussions |
| `self-organizing-coder` | Task decomposition, delegation, iterative delivery |
| `spec-driven` | Planning features, spec-first workflows |
