---
description: "Review phase (PROVE) -- review current code changes for quality, safety, and performance, grouped by severity with a verdict. Use to review a diff (trusts the author; for adversarial re-verification use judge)."
agent: discover
phase: PROVE
---

# Review -- Code Review

A thorough, language-agnostic code review of the current changes, reported by severity. Part of the **PROVE** phase. (Review trusts the author's evidence; the [judge](judge.md) command trusts nothing and re-runs.)

> **Agent:** run on a reviewing worker ([discover](../agents/discover.md), review mode) or any read-only reviewer.

**Target** (optional): **$ARGUMENTS**. Otherwise review the current uncommitted changes (`git diff` / `git diff --cached`).

## Workflow

1. **Understand the change.** Read the message/PR/summary. Does it make sense? Should it exist? Identify scope: bug fix, feature, refactor, cleanup.
2. **Read the diff plus neighbors.** Do not review in isolation; read enough surrounding code to judge coupling and convention.
3. **Check against the rubric** (below).
4. **Group findings** by severity; every finding names `[file:line]` and a suggested resolution.

## Review rubric

- **Correctness & spec parity:** does the change do what it claims? Does it match DONE_WHEN? Any off-by-one, wrong null/edge handling, race, or resource leak?
- **Safety & error handling:** all errors checked and propagated with context; none silently discarded. No swallowed errors, no branching on error strings. ([code-craft](../skills/code-craft/SKILL.md) hard rules.)
- **Tests:** appropriate unit/integration/e2e covering happy, error, and boundary paths? Tests assert behavior, not implementation.
- **Security:** input validation, authz, no secrets logged or committed, dependency sanity.
- **Performance:** only flag with measurement or a clear algorithmic concern; do not micro-optimize.
- **Readability & consistency:** short single-purpose functions; happy path at minimal indent; errors handled first; matches surrounding convention.

## Severity

- **MUST FIX** -- correctness bugs, security holes, data loss, broken builds. Block merge.
- **SHOULD FIX** -- design issues, missing tests, performance/error-handling gaps that materially affect maintainability. Strongly recommend before merge.
- **NIT** -- style, naming, minor clarity. Optional.
- **SUGGESTION** -- optional improvement, alternative approach.

## Output

```
### MUST FIX
- [ ] [file:line] issue + suggested resolution
### SHOULD FIX
- [ ] [file:line] issue + suggested resolution
### NIT
- [ ] [file:line] nit: ...
### SUGGESTION
- [ ] [file:line] optional: ...

## Verdict
[APPROVE / REQUEST CHANGES / BLOCKED -- one-line justification]
```

## Success metrics

- Every rubric row considered; every finding names a location and a fix.
- Verdict is one of the three with a one-line justification.

## Failure metrics

- Findings without `[file:line]` or without a suggested resolution -> incomplete review.

## References

- [code-craft](../skills/code-craft/SKILL.md) -- hard rules, the review checklist.
- [judge](judge.md) -- when you need adversarial re-verification, not author-trusting review.
