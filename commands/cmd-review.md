---
name: cmd-review
description: "Review phase (PROVE): review current code changes for correctness, safety, tests, security, performance, and readability, grouped by severity with one verdict. Use to review a diff while trusting the author; for adversarial re-verification use the judge protocol."
---

# Review Code Changes

A thorough, language-agnostic review of the current changes, reported by severity. Review trusts the author's evidence; adversarial re-running is the judge protocol's job ([verification](../skills/verification/SKILL.md)). Right-size: a trivial diff (one file, <10 lines, no behavior change) narrows to correctness + safety and reports in two sentences.

Flag any owed artifact line the author skipped as SHOULD FIX: an outward action without `AUTH:`, a behavior change without `INTENT:`, a defect fix without `TWINS:` ([craft](../skills/craft/SKILL.md)). Full fraud hunting is out of scope here.

## Target

Default: the current uncommitted changes (`git diff` / `git diff --cached`). Options: `--against=<ref>` diffs against a ref; `--focus=<security|performance|correctness|tests>` reviews one dimension only. Clean tree with no `--against`: report that there is nothing to review and stop - never fabricate a diff.

## Rubric

Consider every row; synthesize in one read pass over the diff plus touched neighbors.

- **Correctness & spec parity:** does the change do what it claims and match DONE_WHEN? Off-by-one, wrong edge/null handling, races, leaks.
- **Safety & error handling:** every error checked and propagated with context; none swallowed; no branching on error strings.
- **Tests:** cover happy, error, boundary paths; assert behavior, not implementation details.
- **Security:** input validation, authorization, no logged or committed secrets, dependency sanity.
- **Performance:** flag only with measurement or a clear algorithmic concern; never micro-optimize in review.
- **Readability & consistency:** single-purpose functions, happy path minimally indented, errors handled first, matches surrounding convention.

## Severity

- **MUST FIX** correctness bugs, security holes, data loss, broken builds - blocks merge.
- **SHOULD FIX** missing tests, design or error-handling gaps that materially hurt maintainability.
- **NIT** style, naming, minor clarity - optional.
- **SUGGESTION** optional improvement or alternative approach.

## Output

```
### MUST FIX
- [ ] [file:line] issue -> suggested resolution
### SHOULD FIX
- [ ] [file:line] issue -> suggested resolution
### NIT
- [ ] [file:line] nit
### SUGGESTION
- [ ] [file:line] optional idea

## Verdict
APPROVE | REQUEST CHANGES | BLOCKED - one-line justification
```

## Done =

Every rubric row considered; every finding carries `[file:line]` and a resolution; exactly one verdict with justification. A finding lacking location or resolution makes the review incomplete.
