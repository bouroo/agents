# Agent Configuration

Specifications drive implementation; code serves specifications. The spec is the primary artifact; code is its expression in a particular language and framework.

## Agent & Tool Discovery

Available subagent types and tools are declared in each agent's system prompt. When delegating tasks, select agents and tools based on their described capabilities at runtime rather than relying on hardcoded names.

## SPDD Core Loop

1. **Specify** → Decompose into concrete, testable tasks
2. **Align** → Lock intent: what/what-not done, constraints, definition of done
3. **Plan** → Design abstractions. Use REASONS Canvas for complex features
4. **Delegate** → Execute independent units in parallel
5. **Validate** → Run validators after every change. Fix immediately
6. **Sync** → Logic corrections: spec→code. Refactoring: code→spec

## REASONS Canvas

| Letter | Dimension | Content |
|--------|-----------|---------|
| R | Requirements | Problem, definition of done |
| E | Entities | Domain objects & relationships |
| A | Approach | Strategy, design decisions |
| S | Structure | Where change fits in system |
| O | Operations | Ordered, testable steps |
| N | Norms | Standards, naming, patterns |
| S | Safeguards | Constraints, invariants |

## Spec-Code Sync

| Change Type | Strategy |
|-------------|----------|
| New feature | Spec → Code |
| Logic correction | Spec → Code (fix spec first) |
| Bug fix (behavior change) | Spec → Code (fix spec first) |
| Refactoring | Code → Spec (refactor first, then sync) |
| Performance optimization | Code → Spec (optimize, update spec) |

## Constitutional Principles

### Library-First
Every feature begins as a standalone, reusable module with clear boundaries and minimal dependencies.

### Test-First Imperative
No implementation code before tests. Red → Green → Refactor.

### Simplicity
Max 3 projects/modules for initial implementation. No future-proofing. No speculative features.

### Anti-Abstraction
Use framework features directly. Single model representation. No abstraction layers until complexity justifies them.

### Integration-First Testing
Prefer real databases over mocks. Use actual service instances over stubs. Contract tests mandatory.

## Safe by Default

- Use "always valid values" — design types so invalid states are unrepresentable
- Use named constants instead of magic values
- Validate all inputs at boundaries; reject early
- Never require elevated privileges; let users configure minimal permissions
- Use sandboxed file access to prevent path traversal
- Never log secrets or personal data

## Error Design

- Always check errors. Handle when possible, retry when appropriate, report otherwise
- Wrap errors with context; don't flatten them into strings
- Define named sentinel errors users can match against
- Use structured error types that preserve the error chain
- Reserve panics for internal program errors only
- Show usage hints for incorrect arguments; don't crash

## Code Quality

- Write code for reading, not writing. Flatten cognitive speed-bumps
- Use consistent, conventional names: `err` for errors, `ctx` for contexts, `req`/`resp` for requests/responses
- Simplify wordy functions by extracting low-level paperwork into named helpers
- Decouple code from environment — only entry points access env vars, CLI args, or OS details
- Avoid mutable global state; use explicit dependency injection
- Use concurrency sparingly and keep it strictly confined
- Write packages, not programs — keep `main` thin, push logic into importable packages

## Context Condensing

- **Auto-compaction**: Triggers at ~20K token headroom; `compaction.auto` enabled
- **Pruning**: Old outputs beyond ~40K recency → `[Old tool result content cleared]`; `compaction.prune`
- **Reserved buffer**: `compaction.reserved` tokens kept for context continuity
- **Manual trigger**: `/compact` slash command
- After compaction: re-read modified files to avoid stale assumptions

## Task Decomposition

1. Identify independent units — mark `[P]`
2. Order sequential dependencies explicitly
3. Assign each unit single deliverable
4. Validate independently before merging
5. Sync: fix spec first for logic changes
6. Track: `pending` → `in_progress` → `completed`

## Large Project Workflow

1. **Explore** — Map structure, identify boundaries, locate entry points
2. **Plan** — Design via REASONS Canvas. Identify affected modules
3. **Implement** — Delegate bounded tasks. Validate each independently
4. **Validate** — Run full test suite. Verify no regressions
