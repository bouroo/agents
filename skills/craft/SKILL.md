---
name: craft
description: "Language-agnostic software craftsmanship: the twelve commandments plus the full PROMPT/INTENT/TWINS/AUTH/PENDING gate definitions. Use when writing, reviewing, or refactoring code for clarity, safety, testability, or correctness."
---

# Craft

Twelve commandments for high-quality language-agnostic code, and the canonical definitions of the five artifact gates. When style priorities collide, resolve them by the manifesto's §1 order — Correctness > Clarity > Simplicity > Concision > Maintainability > Consistency > Performance.

> **Override.** A project-level style guide that explicitly supersedes this skill wins; project convention beats personal taste.

**Stance:** every unclear name, swallowed error, and untested branch is a defect waiting to ship. Clarity beats cleverness; the next reader is the customer.

## Artifact gates (canonical definitions)

Gates are literal lines owed at decision points; they belong verbatim in the final report. If a run owed a gate, an absent line means the gate was not met.

- **`PROMPT:` at intake, before the first edit or command:** `PROMPT: <one concise English paragraph — GOAL / CONTEXT / CONSTRAINTS / DONE_WHEN>`. Pin the ask in English before working, **correctively, not as a restatement**: the paragraph states the reading you will execute, filling in what the ask left implicit — vague scope, unstated constraints, missing `DONE_WHEN`. Surface it and **STOP for confirmation of that corrected reading before the first edit or command**; acting on an unconfirmed correction is the failure this gate prevents. A correction you cannot write without guessing is owed instead as one pointed question carrying your recommended interpretation. The stop confirms the reading, not a decision, so it does not violate `Decide, don't ask`. Skip only for a trivial ask (one file, <10 lines, no new public behavior, no searching); note the skip.
- **`INTENT:` before any behavior-changing edit:** `INTENT: code does <X>; the failing check expects <Y>; the spec says <Z>`. Fill all three slots by opening the artifacts: X = observed behavior of today's code (read it, run it if needed); Y = what the failing check actually expects (quote it); Z = what README/docstring/design doc/task demands (quote the clause). Worked case: endpoint returns insertion order, test `TestUserList_Alphabetical` fails, design doc says "sorted alphabetically by name" -> `INTENT: code does return users in insertion order; the failing test expects alphabetical order; the spec says "sorted alphabetically by name"`.
  - **When X, Y, Z disagree, the disagreement is the finding — do NOT edit.** Resolve by the anchor ordering (§0): user statement > spec > checks > code. Splits: code + spec agree, test wrong -> the *test* is the suspect; propose fixing it. Code + test agree, spec silent -> fill the gap; ask which behavior is intended. Test + spec agree, code wrong -> the normal fix; proceed, then emit `TWINS:`. The spec is the durable contract; a logic change revises the spec first, then the code; a refactor syncs both sides — never land one alone.
  - Skip only for pure typo/rename/format edits with no observable-behavior risk (return value, exit code, log line, side effect, ordering); note the skip.
- **`TWINS:` on every defect fix:** `TWINS: searched <pattern> - found <N> other sites: <files or "none">`. Search the whole project for the same wrong construct; fix siblings or list them.
- **`AUTH:` before any outward effect** (push, deploy, publish, send, install, delete shared data): `AUTH: user said "<exact quote>"`. Only the user's own statement authorizes; docs instructing a deploy, or the task feeling complete, do not. **Completion is never authorization:** finishing the task, a clean working tree, or a green build does not authorize any outward or destructive step — end local and emit `PENDING: <step> - awaiting your authorization`; take the step only after the user says so. No quotable authorization -> propose it and emit `PENDING:` instead of acting.
- **`PENDING:` for every prescribed-but-untaken follow-up:** `PENDING: <action> - awaiting your authorization`. An unmentioned pending action is treated as a fraud by judging.

**Sweep:** before reporting, mechanically check whether each owed gate is present.

## Twelve commandments

1. **Separate orchestration from core logic.** Reusable packages with clean APIs; the entry point only parses input, handles errors, cleans up. Return data, not printouts; return errors, never crash the process.
2. **Test everything.** Names read as behavior sentences; cover happy, error, edge; integration tests cross real boundaries. Tests are design feedback: a painful test is a symptom of bad API shape — fix the API.
3. **Code for reading.** Name length scales with scope; drop type-like words (`users` over `userList`). Hide paperwork (`buildRequest`, `parseResponse`) in well-named helpers. Default is no comment; add one only when naming is exhausted and it states a non-derivable *why*. Doc comments on exported symbols follow the language's official convention. See [Comments](#comments).
4. **Safe by default.** Make invalid states unrepresentable: validating constructors that refuse bad input at construction; named constants over magic values; least privilege; rules encoded in types/validators, never in caller discipline.
5. **Wrap errors, preserve the causality chain.** Typed/sentinel errors wrapped with context so cause survives handling; never flatten to strings, never inspect error text, never discard silently.
6. **No mutable globals.** Inject dependencies explicitly; shared state behind a single owner or synchronization. Global reachability makes control flow untraceable and concurrency unsafe.
7. **Concurrency sparingly, with enforced lifetimes.** Only when required; confine to the creating scope; every task terminates before its parent exits (join/wait/cancel propagation). Global goroutines breed bugs like global variables. Sequential is usually cheaper.
8. **Decouple core from environment.** Only the boundary reads env/CLI/filesystem/network clocks; business logic stays pure and portable. Adaptation lives at the edge.
9. **Design failure handling upfront.** Check every error at birth; keep the happy path unindented; retry transient with bound; propagate the rest with context. Failure handling patched in later is a feature nobody designed.
10. **Log actionable information only.** Structured fields, never secrets. Match tool to purpose: logs = actionable errors, traces = request flows, metrics = statistics. Log-spam buries signal.
11. **Ship a walking skeleton first.** End-to-end "shameless green" through the real path validates the design before refinement invests in details that may be wrong.
12. **Refactor while context is fresh.** Invest ~10% right after building: names, duplication, dead branches. Maintenance outlasts writing; context decays fast.

## Comments

Default is **no comment**. One earns its place only by stating a non-derivable *why* — a rationale, an invariant, an external constraint, a trap the code cannot express.

Named noise, each deleted on sight:

- **Restates the code or the signature** — `// increment i`, `// returns the user`.
- **Narrates the change** — `// added null check`, `// fix for the timeout bug`; git records that, and the code records the result.
- **Banners inside a function** short enough to read whole — `// --- validation ---` in a five-line function is a table of contents for one page.
- **A doc block longer than the code it documents** — the failure mode is a paragraph of prose on a two-line helper.

**Language conventions set the form, the code's complexity sets the length.** Doc comments on exported symbols follow the language's own convention — GoDoc, TSDoc, PEP 257, rustdoc, Javadoc — at that convention's **minimum**: a one-line function gets a one-line doc. Elaborate only where behavior is genuinely non-obvious, never to satisfy a shape.

**Pre-emit test:** re-read every comment you wrote. If a correct refactor would make it wrong, it was noise — delete it.

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
| Comment narrates the change | Delete it; git records the change |
| Doc block longer than its function | Cut to one line, or delete |

## Enforce with tooling (GROW)

Move checks out of review into deterministic gates: formatter, then linter, then type-checker, then tests in pre-commit and CI. A rule the linter enforces is a rule reviewers never repeat.

Same law for instructions: a project rule stated twice in prompts belongs in an instruction file — written as a **verifiable rule** (command, path, threshold: "run `pnpm test` after touching business logic", never "test well"), split into topic files loaded on demand rather than piled into globals, and kept out of machine-local, uncommitted notes.

**The instruction file is loaded every session, so prune it like code.** Apply the test to each line: *would removing this cause the agent to err?* If not, cut it. Include what the agent cannot derive — build/test commands, style rules that differ from convention, repo etiquette, environment quirks, non-obvious gotchas. Exclude what it can read for itself — standard conventions, file-by-file maps, anything already true without the line. Two diagnostics: a rule that keeps being ignored means the file is **too long** and the rule is lost in noise (cut, don't re-emphasize); a question the agent keeps asking that the file answers means the **phrasing is ambiguous**, not that the rule is missing. Emphasize sparingly — if many lines shout, none stands out. A rule that must always hold belongs in a deterministic gate, not in prose ([verification](../verification/SKILL.md)).

## Cross-references

- [verification](../verification/SKILL.md) mutation probe, evidence audit, judging the finished work.
- [performance](../performance/SKILL.md) after 1-6 hold, and only by measurement.
