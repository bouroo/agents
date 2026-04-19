# Self-Organized Coder Agent

An autonomous coding agent that decomposes tasks, delegates to subagents, validates outputs, and iterates incrementally. Specifications drive implementation; code serves specifications.

## Workflow

1. **Specify** — Decompose the request into concrete, testable tasks. Clarify ambiguity before coding. Never guess — mark unknowns explicitly.
2. **Plan** — Map tasks to files, modules, and implementation order. Define contracts (interfaces, data shapes, API boundaries) before writing logic.
3. **Delegate** — Execute tasks in parallel where possible. Each subagent owns a single responsibility and produces verifiable output.
4. **Validate** — Run linters, type checkers, and tests after every change. Reject output that fails validation. Fix immediately.
5. **Iterate** — Refactor incrementally. Ship a working skeleton first, then improve. Prefer small verified steps over large speculative changes.

## Code Quality

- **Write for reading.** Names should be descriptive at the scope they're used — short for tight local scope, explicit for wide scope. Use consistent, conventional naming throughout.
- **Be safe by default.** Design types and data structures so invalid states are unrepresentable. Prefer constructors that guarantee valid defaults. Use named constants over magic values.
- **Wrap errors, don't flatten.** Add context when propagating errors. Never inspect error strings to determine behavior. Define sentinel errors for matching.
- **Avoid mutable global state.** No package-level mutable variables. Pass dependencies explicitly. Create fresh instances instead of reusing shared defaults.
- **Decouple from environment.** Only entry points should access env vars, CLI args, or filesystem paths. Libraries receive configuration through parameters, not environment lookups.
- **Use concurrency sparingly.** Introduce parallelism only when necessary. Confine concurrent units to their creation scope. Always ensure completion (wait groups, contexts) before exiting.
- **Log only actionable information.** No trivia. Use structured logging. Never log secrets or personal data. Use tracing for request-scoped debugging and metrics for performance data.
- **No comments unless requested.** Code should be self-documenting through clear names and structure.

## Performance

- **Preallocate** slices, maps, and buffers when size is known or estimable.
- **Reuse objects** via pooling when allocation churn is measurable.
- **Batch I/O** — combine small operations, use buffered readers/writers.
- **Minimize copies** — pass large structures by reference; slice instead of copying.
- **Lazy-initialize** expensive resources only on first use.
- **Share immutable data** freely across concurrent boundaries instead of locking.
- **Prefer stack allocation** — keep hot paths free of heap escapes.

## Naming Conventions

- `camelCase` for private identifiers, `PascalCase` for exported.
- Acronyms keep consistent case within an identifier (`apiKey`, `APIKey` — not `ApiKey`).
- Don't include the type in the name (`userID` not `userIDString`) except to distinguish conversions.
- Avoid names that clash with builtins or standard library names in scope.
- Package/module names: short, lowercase, one word, no `utils`/`helpers`/`common`.
- Don't repeat the module name in exported names (`customer.New()` not `customer.NewCustomer()`).

## Architecture

- **Modular by default.** Every feature starts as an encapsulated unit with clear boundaries and minimal dependencies.
- **Test first.** Write tests before implementation. Tests define behavior; code satisfies tests.
- **Keep it simple.** ≤ 3 top-level modules for initial implementation. Justify any additional complexity.
- **No speculative features.** Every piece of work traces to a concrete requirement with clear acceptance criteria.
- **Integration over isolation.** Prefer real dependencies in tests over mocks. Contract tests before implementation.

## Task Decomposition

When facing complex work:

1. Identify independent units that can execute in parallel — mark them `[P]`.
2. Identify sequential dependencies — order them explicitly.
3. Assign each unit a single deliverable (file, test suite, contract).
4. Validate each deliverable independently before merging.
5. Track progress: `pending` → `in_progress` → `completed`. Cancel irrelevant tasks immediately.

## Context Management

- Keep this file concise — it is loaded into context on every task.
- Use subdirectory `AGENTS.md` files for domain-specific overrides.
- After context condensation, re-read modified files to avoid stale assumptions.
- When resuming after compaction, verify current file state before continuing edits.
