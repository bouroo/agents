---
name: cmd-review
description: "Use to review the current diff for correctness, safety, tests, security, performance, readability, simplicity, and structure, reported by severity with one verdict. Reach for it when a change is written and someone must decide whether it merges, trusting the author's evidence. Not for adversarial re-verification that re-runs claims (the judge protocol in quality), for restructuring (cmd-refactor), or for gate mechanics (cmd-verify)."
---

# Review Code Changes

A thorough, language-agnostic review of the current changes, reported by severity. This is the **Test** stage's review pass (§4), run by the Verifier seat — never the Implementer. Review trusts the author's evidence; adversarial re-running is the judge protocol's job (the `quality` skill's Verification section). Right-size: a trivial diff (one file, <10 lines, no behavior change) narrows to correctness + safety and reports in two sentences. **No options: fully autonomous** — this pass is read-only, asks nothing, states any inference (e.g. which diff bounds it took) in one line rather than asking, and ends at its verdict; the only stop is the no-diff rule below. Everything mechanical — diff bounds, the output template's shape, the no-diff stop — is deterministic; the model judges only the findings. Flag any owed artifact line the author skipped — an outward action without `AUTH:`, a behavior change without `INTENT:`, a defect fix without `TWINS:` — as SHOULD FIX per the `quality` skill's Craft section; full fraud hunting is out of scope.

## Target

Default: the uncommitted changes (`git diff` / `git diff --cached`). `--against=<ref>` diffs against a ref; `--focus=<security|performance|correctness|tests>` reviews one dimension only. **Clean tree with no `--against`: report that there is nothing to review and stop** — never fabricate a diff.

## Rubric

Consider every row in one read pass over the diff plus touched neighbors:

- **Correctness & spec parity** — does it do what it claims and match DONE_WHEN? Off-by-one, wrong edge/null handling, races, leaks.
- **Safety & error handling** — every error checked and propagated with context; none swallowed; no branching on error strings.
- **Tests** — happy, error, and boundary paths; assert behavior, not implementation details.
- **Security** — input validation, authorization, no logged or committed secrets, dependency sanity. A suspected boundary violation goes to the `security-audit` skill's candidate gate; this pass does not run that hunt.
- **Performance** — flag only with measurement or a clear algorithmic concern; never micro-optimize in review.
- **Readability & consistency** — single-purpose functions, minimally indented happy path, errors handled first, matches surrounding convention; comments and simplicity per the `quality` skill's Craft section.
- **Simplicity** — the least mechanism that works; flag it only where the reviewer can name what it buys per the `quality` skill's Craft section.
- **Structure & reuse** — same logic knowledge in two places (diff copies: drifted sibling latent defect), module needing "and" describe itself, dependencies pointing outward into transport framework per the `quality` skill's Craft section.

## Severity

**MUST FIX** (correctness bugs, security holes, data loss, broken builds — blocks merge) · **SHOULD FIX** (missing tests, design or error-handling gaps that materially hurt maintainability) · **NIT** (style, naming, minor clarity — optional) · **SUGGESTION** (optional improvement or alternative approach).

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

Every rubric row considered; every finding carries `[file:line]` and a resolution; exactly one verdict with justification. A finding without location or resolution makes the review incomplete.

Reviewing is hunting gaps, and a hunt always finds some — a reviewer asked to look will report even when the work is sound. Chase only what affects **correctness or a stated requirement**; a NIT or SUGGESTION is optional by definition, and pursuing every one manufactures over-engineering — abstraction layers, defensive branches, tests for cases that cannot occur. Report the full list; treat only MUST FIX as blocking, and let a SHOULD FIX earn its place by naming the concrete harm.
