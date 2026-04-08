---
description: Review code for quality, security, and performance issues
agent: code
subtask: true
---

# Code Review

Perform a structured review of `$ARGUMENTS` (or the current diff if no target is provided).

## Steps

1. **Scope** — Determine review target:
   - If `$ARGUMENTS` is provided, review those files/paths.
   - Otherwise, run `git diff --name-only HEAD~1` to find changed files.
   - If no git history, review all tracked source files.

2. **Read** — Read every file in scope. Understand intent, context, and conventions before judging.

3. **Analyze** — Evaluate against these dimensions (use `task` with `code-reviewer` subagent for large scopes):

   | Dimension | Checks |
   |---|---|
   | **Correctness** | Logic errors, off-by-one, unhandled edge cases, race conditions |
   | **Security** | Input validation, rooted path traversal prevention, least-privilege, no secrets logged or hardcoded |
   | **Performance** | Memory pre-allocation, object pooling, zero-copy, buffered I/O, lazy initialization |
   | **Readability** | Clarity over writeability, cyclomatic complexity <10, explicit names, flat control flow |
   | **Simplicity** | Least mechanism, core language features over wrappers (anti-abstraction), no speculative features |
   | **Error handling** | Validated system boundaries, errors wrapped with context, sentinel errors for matching |
   | **Consistency** | Naming conventions, export patterns, file organization match project norms |
   | **Test coverage** | Test-first approach, error paths covered, descriptive test names, no change-detector tests |

4. **Report** — Output a structured review with severity ratings:

   ```
   ## [CRITICAL] <file>:<line> — <summary>
   <explanation and suggested fix>

   ## [WARNING] <file>:<line> — <summary>
   <explanation and suggested fix>

   ## [INFO] <file>:<line> — <suggestion>
   ```

5. **Summarize** — End with a brief verdict: approve, request changes, or blocking issues.

## Principles

- Review for the reader, not the writer — code is read far more than written.
- Prefer idiomatic patterns in the project's language.
- Flag *why* something is wrong, not just *that* it is wrong.
- Do not nit-pick style that `gofmt`/`prettier`/formatters would fix automatically.
- Distinguish canonical rules (must fix) from best-practice suggestions (nice to have).
