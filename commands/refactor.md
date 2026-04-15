---
description: Refactor code for readability, safety, performance, and maintainability. Language-agnostic.
agent: general
subtask: true
---

# Refactor

Refactor `$ARGUMENTS` (or current working directory) against language-agnostic best practices. Focus on reducing cognitive load, eliminating hidden costs, and tightening boundaries.

## Steps

### 1. Scope Determination

- If `$ARGUMENTS` is provided, refactor those files/paths
- Otherwise, run `bash` with `git diff --name-only HEAD~1` to find changed files
- If no git history, ask the user which files to refactor

### 2. Initialize Tracking

Use `todowrite` to create a task list:

- Read & understand context
- Naming & readability
- Safety & defaults
- Error handling
- Performance & memory
- Architecture & coupling
- Concurrency
- Logging
- Apply changes & verify

### 3. Read & Analyze

Read every file in scope. Understand intent, conventions, and existing patterns before changing anything. Preserve project style where it's consistent.

### 4. Refactor Checklist

Evaluate and fix code against the following checklist. Each item includes the rationale and the action to take.

---

#### Naming & Readability

| # | Severity | Check | Action |
|---|----------|-------|--------|
| 1 | P1 | Names are the right length: short for narrow scope, descriptive for wide scope | Rename single-letter vars used beyond a tight loop; shorten overly verbose names in small scopes |
| 2 | P1 | Acronyms keep consistent casing (`APIKey`, `userID` — not `ApiKey`, `UserId`) | Fix inconsistent casing |
| 3 | P2 | No type-in-name (`count` not `intCount`, `results` not `resultSlice`) | Remove type suffixes unless needed to disambiguate a type conversion |
| 4 | P1 | No chatter — package name isn't repeated (`customer.New()` not `customer.NewCustomer()`) | Shorten chattery exports |
| 5 | P2 | Packages/modules are lowercase, one word, no separators; never `util`, `helpers`, `common` | Rename catch-all packages to specific nouns |
| 6 | P2 | Files are lowercase, one word; `_` reserved for special suffixes (test, platform) | Rename files that don't follow convention |
| 7 | P1 | Interfaces with one method use `-er` suffix (`Reader`, `Writer`); never `FooInterface` | Rename interfaces |
| 8 | P2 | Getters have no `Get` prefix (`Address()` not `GetAddress()`); setters use `Set` prefix | Fix getter/setter naming |
| 9 | P1 | Magic values replaced with named constants | Extract literals into constants |
| 10 | P2 | Long functions decomposed — low-level "paperwork" extracted into named helpers | Extract method/function to flatten cognitive speed-bumps |

#### Safety & Defaults

| # | Severity | Check | Action |
|---|----------|-------|--------|
| 11 | P0 | Zero values are useful, or a validating constructor is required | Add constructor or make zero value valid |
| 12 | P0 | No mutable global state; all state via dependency injection or explicit parameters | Move globals into structs, pass as parameters |
| 13 | P1 | No default/shared singletons (`DefaultClient`, `DefaultServeMux` equivalents) | Replace with configured instances |
| 14 | P0 | All input validated at system boundaries | Add validation at entry points |
| 15 | P1 | Configuration is immutable after load | Freeze config, expose read-only access |

#### Error Handling

| # | Severity | Check | Action |
|---|----------|-------|--------|
| 16 | P0 | All errors checked; never silently discarded | Handle or propagate every error |
| 17 | P0 | Errors wrapped with context, not flattened to strings | Use error wrapping (`%w` or equivalent) |
| 18 | P1 | Sentinel errors defined for matching; no string comparison on errors | Add named error values, match with `errors.Is` or equivalent |
| 19 | P1 | Panic/reserved only for truly unrecoverable internal bugs, never for user input | Replace panic-with-error patterns |
| 20 | P2 | Usage hints shown on bad input instead of crashes | Add helpful error messages for invalid args |

#### Performance & Memory

| # | Severity | Check | Action |
|---|----------|-------|--------|
| 21 | P1 | Slices/collections preallocated when size is known or estimable | Add capacity hints (`make`, `new`, preallocation) |
| 22 | P1 | Buffers and objects reused in hot paths to reduce allocation/GC pressure | Use pool patterns, buffer reuse |
| 23 | P2 | Zero-copy techniques preferred (slicing, references) over cloning | Eliminate unnecessary copies |
| 24 | P1 | I/O is buffered; small operations batched to reduce round trips | Add buffered readers/writers, batch operations |
| 25 | P2 | Large allocations avoided in request-scoped handlers | Move to pre-allocated buffers or pools |
| 26 | P2 | Struct/record field order considers memory alignment (large types first) | Reorder fields to minimize padding |
| 27 | P1 | String concatenation in loops uses builder pattern | Replace `+=` in loops with `StringBuilder` or equivalent |
| 28 | P2 | Unnecessary heap allocations avoided — prefer stack-allocated values, pass by reference for large structs | Reduce escape analysis failures, use value types where possible |

#### Architecture & Coupling

| # | Severity | Check | Action |
|---|----------|-------|--------|
| 29 | P0 | Domain logic decoupled from environment (no env vars, CLI args, OS calls in packages) | Move env/arg access to entrypoint only |
| 30 | P1 | Packages return data, not print; return errors, not exit | Separate I/O from logic |
| 31 | P2 | Public surface minimized — unexport by default, export only what others need | Reduce visibility |
| 32 | P1 | Single responsibility — each module/package has a clear, focused purpose | Split catch-all modules |
| 33 | P2 | No circular dependencies between packages | Restructure to eliminate import cycles |

#### Concurrency

| # | Severity | Check | Action |
|---|----------|-------|--------|
| 34 | P0 | Every concurrent unit has a bounded lifetime (context, wait group, errgroup) | Add lifecycle bounds |
| 35 | P0 | No goroutine/thread leaks — all terminate before enclosing scope exits | Ensure cleanup on all paths |
| 36 | P1 | Concurrency used only when necessary; not introduced speculatively | Remove unnecessary concurrency |
| 37 | P1 | Shared data protected — confinement preferred over shared memory with locks | Use channel-based or confined patterns |
| 38 | P2 | Worker pools or semaphores cap concurrent units | Add bounded concurrency |

#### Logging

| # | Severity | Check | Action |
|---|----------|-------|--------|
| 39 | P0 | No secrets or PII in logs | Redact sensitive fields |
| 40 | P1 | Only actionable information logged — no trivia spam | Remove debug noise, keep structured entries |
| 41 | P2 | Structured logging used; trace for request-scoped debugging, metrics for performance | Use appropriate signal (log/trace/metric) |

---

### 5. Apply Changes

For each issue found:

1. **Fix the straightforward ones directly** using `edit` — naming, constants, error wrapping, visibility changes
2. **Flag structural changes** that need user confirmation using `question` — package renames, interface redesigns, architecture changes
3. **Do not change behavior** — refactoring preserves observable behavior
4. **Do not add features** — only simplify, clarify, and restructure existing code

### 6. Verify

After applying changes:

1. Run the project's lint/format tool via `bash`
2. Run the test suite via `bash`
3. Fix any failures introduced by the refactor
4. If no tooling is configured, read changed files to verify correctness

### 7. Report

Output a structured summary:

```markdown
## Refactor Report

### Files Changed
- `<file>`: <summary of changes>

### Checklist Results

| Category | Issues Found | Fixed |
|----------|-------------|-------|
| Naming & Readability | <n> | <n> |
| Safety & Defaults | <n> | <n> |
| Error Handling | <n> | <n> |
| Performance & Memory | <n> | <n> |
| Architecture & Coupling | <n> | <n> |
| Concurrency | <n> | <n> |
| Logging | <n> | <n> |

### Needs Discussion
<detailed list of structural changes that require user decision>

### Verdict
<CLEAN — all issues resolved | PARTIAL — some items need discussion | BLOCKED — structural decisions required>
```

### 8. Completion

Mark all tasks complete in `todowrite`.

## Principles

- **Severity Legend**:
  - **P0**: Must fix — correctness, security, or data integrity risk
  - **P1**: Should fix — maintainability, performance, or readability improvement
  - **P2**: Nice to have — polish and convention alignment
- **Behavior preservation** — refactoring must not change observable behavior
- **Readability over cleverness** — code is read 10× more than written
- **No premature abstraction** — add abstraction only when complexity is proven
- **Minimal public surface** — unexport by default, export only when needed
- **Flag why, not just what** — every change includes the rationale

Trigger this workflow by typing `/refactor` in the chat. Pass an optional path: `/refactor src/auth`.
