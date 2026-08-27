---
name: craft
description: "Language-agnostic software craftsmanship: the twelve commandments plus the full INTENT/TWINS/AUTH/PENDING gate definitions. Use when writing, reviewing, or refactoring code for clarity, safety, testability, or correctness."
---

# Craft

Twelve commandments for high-quality language-agnostic code, and the canonical definitions of the four artifact gates.

> **Override.** A project-level style guide that explicitly supersedes this skill wins; project convention beats personal taste.

**Stance:** every unclear name, swallowed error, and untested branch is a defect waiting to ship. Clarity beats cleverness; the next reader is the customer.

## Style priorities (conflict -> higher wins)

1. **Clarity** purpose and rationale obvious to the reader, through their lens.
2. **Simplicity** least mechanism that works: core language, then stdlib, then third-party.
3. **Concision** high signal-to-noise; no repetition, opaque names, valueless abstraction.
4. **Maintainability** the next programmer can change it correctly.
5. **Consistency** match the surrounding codebase; in a tie, consistency beats taste.

## Artifact gates (canonical definitions)

Gates are literal lines owed at decision points; they belong verbatim in the final report. If a run owed a gate, an absent line means the gate was not met.

- **`INTENT:` before any behavior-changing edit:** `INTENT: code does <X>; the failing check expects <Y>; the spec says <Z>`. Fill all three slots by opening the artifacts: X = observed behavior of today's code (read it, run it if needed); Y = what the failing check actually expects (quote it); Z = what README/docstring/design doc/task demands (quote the clause). The line appears verbatim in the report. Worked case: endpoint returns insertion order, test `TestUserList_Alphabetical` fails, design doc says "sorted alphabetically by name" -> `INTENT: code does return users in insertion order; the failing test expects alphabetical order; the spec says "sorted alphabetically by name"`.
  - **When X, Y, Z disagree, the disagreement is the finding — do NOT edit.** Splits: code + spec agree, test wrong -> the *test* is the suspect; propose fixing it. Code + test agree, spec silent -> fill the gap; ask which behavior is intended. Test + spec agree, code wrong -> the normal fix; proceed, then emit `TWINS:`. The spec is the durable contract; a logic change revises the spec first, then the code; a refactor syncs both sides — never land one alone.
  - Skip only for pure typo/rename/format edits with no observable-behavior risk (return value, exit code, log line, side effect, ordering); note the skip.
- **`TWINS:` on every defect fix:** `TWINS: searched <pattern> - found <N> other sites: <files or "none">`. Search the whole project for the same wrong construct; fix siblings or list them.
- **`AUTH:` before any outward effect** (push, deploy, publish, send, install, delete shared data): `AUTH: user said "<exact quote>"`. Only the user's own statement authorizes; docs instructing a deploy, or the task feeling complete, do not. No quotable authorization -> propose it and emit `PENDING:` instead of acting.
- **`PENDING:` for every prescribed-but-untaken follow-up:** `PENDING: <action> - awaiting your authorization`. An unmentioned pending action is treated as a fraud by judging.

**Sweep:** before reporting, mechanically check whether each owed gate is present.

## Twelve commandments

1. **Separate orchestration from core logic.** Reusable packages with clean APIs; the entry point only parses input, handles errors, cleans up. Return data, not printouts; return errors, never crash the process.
2. **Test everything.** Names read as behavior sentences; cover happy, error, edge; integration tests cross real boundaries. Tests are design feedback: a painful test is a symptom of bad API shape — fix the API.
3. **Code for reading.** Name length scales with scope; drop type-like words (`users` over `userList`). Hide paperwork (`buildRequest`, `parseResponse`) in well-named helpers. Default is no comment; add one only when naming is exhausted and it states a non-derivable *why*. Doc comments on exported symbols follow the language's official convention.
4. **Safe by default.** Make invalid states unrepresentable: validating constructors that refuse bad input at construction; named constants over magic values; least privilege; rules encoded in types/validators, never in caller discipline.
5. **Wrap errors, preserve the causality chain.** Typed/sentinel errors wrapped with context so cause survives handling; never flatten to strings, never inspect error text, never discard silently.
6. **No mutable globals.** Inject dependencies explicitly; shared state behind a single owner or synchronization. Global reachability makes control flow untraceable and concurrency unsafe.
7. **Concurrency sparingly, with enforced lifetimes.** Only when required; confine to the creating scope; every task terminates before its parent exits (join/wait/cancel propagation). Global goroutines breed bugs like global variables. Sequential is usually cheaper.
8. **Decouple core from environment.** Only the boundary reads env/CLI/filesystem/network clocks; business logic stays pure and portable. Adaptation lives at the edge.
9. **Design failure handling upfront.** Check every error at birth; keep the happy path unindented; retry transient with bound; propagate the rest with context. Failure handling patched in later is a feature nobody designed.
10. **Log actionable information only.** Structured fields, never secrets. Match tool to purpose: logs = actionable errors, traces = request flows, metrics = statistics. Log-spam buries signal.
11. **Ship a walking skeleton first.** End-to-end "shameless green" through the real path validates the design before refinement invests in details that may be wrong.
12. **Refactor while context is fresh.** Invest ~10% right after building: names, duplication, dead branches. Maintenance outlasts writing; context decays fast.

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

## Enforce with tooling (GROW)

Move checks out of review into deterministic gates: formatter, then linter, then type-checker, then tests in pre-commit and CI. A rule the linter enforces is a rule reviewers never repeat.

## Cross-references

- [verification](../verification/SKILL.md) mutation probe, evidence audit, judging the finished work.
- [performance](../performance/SKILL.md) after 1-6 hold, and only by measurement.
