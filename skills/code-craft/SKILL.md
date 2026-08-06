---
name: code-craft
description: "Language-agnostic software craftsmanship -- the ten commandments plus the INTENT/TWINS/AUTH/PENDING artifact gates. Use when writing, reviewing, or refactoring code for clarity, safety, testability, or efficiency."
---

# Code Craft

Ten commandments for high-quality, language-agnostic code, plus four artifact gates that fire across the THINK-ACT-PROVE-GROW loop.

> **Override.** A project-level style guide that explicitly supersedes this skill wins; project convention beats personal taste.

**Stance:** every unclear name, swallowed error, and untested branch is a defect waiting to ship. Clarity beats cleverness; the next reader is the customer.

## Style priorities (conflict -> higher wins)

1. **Clarity** -- purpose and rationale obvious to the reader, through their lens.
2. **Simplicity** -- least mechanism that works: core language, then stdlib, then third-party.
3. **Concision** -- high signal-to-noise; no repetition, opaque names, valueless abstraction.
4. **Maintainability** -- the next programmer can change it correctly.
5. **Consistency** -- match the surrounding codebase; in a tie, consistency beats taste.

## Classify the ask (THINK)

**Triviality gate:** trivial only if ALL hold -- one file, under ~10 changed lines, no new behavior, you already know exactly what to change. If trivial: make it, confirm with the one obvious check, report in a sentence. Everything else gets the full workflow.

| Shape | Signal | Deliverable |
|---|---|---|
| Question / assessment | "why is...", "what do you think..." | Findings + recommendation. Change nothing. |
| Task | "fix", "build", "change", "make" | The completed change, verified. |
| Plan-first | ambiguous scope, irreversible/outward action, or asks for a plan | A plan with your recommendation; stop and wait. |

Tie-breaks: any plan-first signal beats task; a mixed ask is a task whose report also answers the question; unsure -> plan-first.

## Artifact gates (loop controls)

- **`INTENT:` (THINK)** -- before any behavior-changing edit: `INTENT: code does <X>; the failing check expects <Y>; the spec says <Z>`. Open the README/docstring/design doc to fill slot Z. If X, Y, Z disagree, do NOT edit -- the disagreement is the finding. Trivial typo/rename/format skips it (note the skip). See [intent gate in depth](references/intent-gate.md).
- **`TWINS:` (PROVE)** -- when a defect is fixed: `TWINS: searched <pattern> - found <N> other sites: <files or "none">`. Search the whole project for the same wrong construct; fix siblings or list them. Fires only on a defect fix.
- **`AUTH:` (THINK)** -- before any outward effect (deploy, push, publish, send, delete of shared data): `AUTH: user said "<quote that authorizes this exact action>"`. Docs instructing a deploy are not authorization; no quote -> propose it and emit `PENDING:`.
- **`PENDING:` (PROVE)** -- every prescribed-but-untaken follow-up (deploy, push, restart, migrate): `PENDING: <action> - awaiting your authorization`. The judge treats an unmentioned pending action as a fraud.

**Sweep:** before the report, mechanically check whether the run owed each gate and add any missing line.

## Ten commandments (ACT)

1. **Write libraries, not monoliths.** Reusable packages with clean APIs; minimal entry point. Return data not side effects; return errors, never crash.
2. **Test everything.** Names read as behavior sentences; cover happy, error, edge. Add integration tests for end-to-end flows. Grade the tests, not just the code -- prefer mutation testing (see [harness-engineering](../harness-engineering/SKILL.md)).
3. **Code for reading.** Name length scales with scope. Drop type-like and context-redundant words (`users` over `userList`; `count` not `userCount` inside `UserCount`). **Default is no comment** -- add one only after all three clear: naming exhausted; it states *why* not *what*; the *why* is not derivable. Doc comments on exported symbols follow the language's official convention strictly (godoc, TSDoc/JSDoc, rustdoc, docstring, Javadoc/Doxygen/XML). Comments never cite harness artifacts (plan/task/decision IDs); a durable constraint becomes a standalone statement.
4. **Safe by default.** Make invalid states unrepresentable; named constants over magic values; least privilege; encode rules in types/validators not model judgment; explicit error returns, never in-band sentinels.
5. **Wrap errors, don't flatten.** Typed/sentinel errors; wrap with context, preserve the cause; never inspect error strings.
6. **No mutable globals.** Inject dependencies; shared state behind a single owner or synchronization.
7. **Concurrency sparingly.** Only when required; confine to the creating scope; every task terminates before its parent; sequential is usually cheaper.
8. **Decouple from environment.** Only the entry point reads env/CLI/filesystem; business logic stays pure. Embed assets; stream large data; factor out repeated scaffolding.
9. **Design for errors.** Handle errors first; indent error paths; keep the happy path unindented. Check every error; retry transient; propagate the rest.
10. **Log actionable information only.** Structured fields, never secrets; tracing for requests, metrics for performance.

## Common mistakes

| Mistake | Fix |
|---|---|
| Discarded error (`_`, `try/except: pass`, `catch (e) {}`) | Check, handle, retry, or propagate with context |
| In-band sentinel (`return -1`, `return null`) | Explicit error return / `Result` / `ok` bool |
| Branch on error string | Typed/sentinel error + cause inspection |
| Mutable global state | Inject deps; single owner for shared state |
| Name by type (`userArray`) | Name by role (`users`) |
| `else` after a terminating `if` | Drop it; keep the happy path unindented |
| 5+ params | Group into a struct/options object |
| Comment restates code | Delete it |
| Comment cites harness refs (`D5`, `spec L319`) | Standalone constraint statement; IDs live in `.agents/` only |

## Enforce with tooling (GROW)

Move checks out of review into deterministic gates: formatter, then linter, then type-checker, then tests in pre-commit and CI. A rule the linter enforces is a rule reviewers never repeat.

## References

- [intent-gate.md](references/intent-gate.md) -- load when a behavior change is ambiguous.
- [harness-engineering](../harness-engineering/SKILL.md) -- three-layer termination, mutation testing, GROW.
