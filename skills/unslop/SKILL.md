---
name: unslop
description: "Detect and remove AI residue from the artifacts a SWE task delivers: prose that says nothing about this project (commit messages, PR descriptions, docs, error and log strings), code that shows model residue (placeholder bodies, stubs, erased types, near-duplicate blocks, swallowed errors, speculative seams), and screens carrying the usual generated-UI tells. Use when output looks AI-generated, when polishing or reviewing a change before it ships, or when a message, comment, or document reads generic - even if nobody says 'unslop'. Not for general code quality, test coverage, or design taste (quality owns those), and not for adding features or restructuring working code."
license: Apache-2.0
---

# Unslop

**Stance:** a deliverable that reads as machine output carries its own defect class: it says things that are true of no project in particular. "Handles errors gracefully", "improves performance", "ensures a seamless experience", a `util` module holding one function, a handler returning `[]`. The reader cannot tell which statements are load-bearing, so none of them are. The fix is never a synonym swap. It is one specific fact: name the actor, the mechanism, the number, the file.

**The one test.** Swap this project for a different one. Does the line still read as true? If yes, it carries no information about *this* project, so it is residue: cut it, or replace it with the concrete fact it was standing in for.

**A tell marks unfinished work.** "Handles errors gracefully" beside a `catch` that swallows is a symptom. Rewording it hides the defect. Treat every prose claim as a specification to check against the code: where the code does not do what the sentence says, the code is what changes. Rewriting prose to agree with a defect is the one wrong move this skill can make.

**Scope:** this skill owns the residue, not the craft. The `quality` skill owns craft, verification, and the comment rule; `architecture` owns structure and domain language; `modernize-coding` owns idiom. Where this skill touches those, it points at them rather than restating them. It adds nothing: it removes residue from artifacts the task already touches, and reports residue found outside that scope without rewriting it.

## 1. Route the surface

| Surface | Artifacts | Rule list |
| --- | --- | --- |
| Prose | commit messages, PR descriptions, docs, READMEs, issue and ticket text, error strings, log messages, user-facing copy | [`references/prose.md`](references/prose.md), read when the task writes or edits prose |
| Code | source, tests, migrations, config, generated files | [`references/code.md`](references/code.md), read when the task writes or edits source |
| UI | rendered surfaces: pages, components, styles, images | [`references/ui.md`](references/ui.md), read when the task touches a rendered screen |

Read the matching reference when the task touches that surface, and load one surface at a time: three lists in one window is three times the cost for one fix. A task can touch several surfaces, and each surface keeps its own rule list. A string inside a source file (a docstring, an error message, a log line) belongs to the **code** surface and is judged by the code rules; the prose surface owns prose that ships as prose (a README, a commit message, an issue).

**The report format.** Every finding carries `file:line`, the rule id, the quote, and one of two labels: `residue` (rewritten here) or `missing work` (not rewritten here, carried into the build queue). Work left undone is listed as `PENDING:` with the file, the rule id, and what it would take — a claim with no referent is never quietly dropped.

## 2. Run it

1. **Scope.** List the artifacts in the task's scope, one per surface. Everything else is report-only.
2. **Collect.** Walk each artifact against its rule list and record every hit as `file:line` plus the rule id (`P3`, `C7`, `U2`). Rule ids are stable, so a report can cite them and a later pass can compare against them.
3. **Split.** Mark each hit as **residue** (the wording or the shape is wrong, the behaviour is right) or **missing work** (the claim exceeds the implementation). Missing work goes to the build queue, never to the rewrite queue, and is reported as `PENDING:`.
4. **Rewrite.** Apply the fix the rule names. Preserve meaning, preserve the project's own voice, and keep the tone the author intended. A rewrite that changes behaviour is not a rewrite.
5. **Verify.** Run the project's own gates. Prose claims must still be true of the code, code must still pass its tests, and a changed screen must still render. A rewrite that breaks the build is a regression, not a cleanup.
6. **Report.** Per surface: what was found, what changed, what was deliberately kept, and what is left as `PENDING:`.

`scripts/scan.py` flags the machine-detectable residue in a path (words, phrases, placeholder markers, leftover debug output) with the rule id attached. It finds candidates, not verdicts: every hit is judged before it is rewritten. Run `python3 skills/unslop/scripts/scan.py --self-test` to check the scanner itself.

## 3. Rules of the rewrite

- **Specificity beats style.** "The retry budget is three attempts over 500ms" beats "robust retry logic", because the first can be checked and the second cannot.
- **An adjective is a claim.** Cite the measurement or cut the adjective. "Significantly improves" with no number is residue.
- **Fixing a defect is not adding mechanism.** "Do not add" forbids new helpers, abstractions, dependencies, and features. It does not forbid the smallest change that makes the code match its own claim: wrapping a swallowed error with its cause (C13) or deleting a catch that only re-raises (C37) changes behaviour on purpose, and both are repairs the task's own claim already promised. Where a fix would invent behaviour that nothing in the repository supports, that is missing work, and it goes to the build queue.
- **One term per concept.** "User", "customer" and "account" for the same entity is a synonym cycle, and the reader has to work out which one the code means.
- **Keep the project's voice.** The residue is the machine's voice, not the house's. A house that swears in its commits keeps swearing.
- **Do not add.** A cleanup that introduces a helper, a config flag, a dependency, or a paragraph of explanation is a second change wearing the first one's clothes.
- **Do not restructure.** Moving code to make it read better is a refactor with its own risk and its own review. Report it instead.
- **Do not tidy the neighbouring line.** A file you were asked to change is not a licence to reformat the file next to it.

## 4. Worked example

A PR that added a retry path with a bounded budget, and the residue around it.

```text
- This method implements a robust retry mechanism that ensures transient failures are handled gracefully.
+ retryBudget(3, 500*time.Millisecond) in retry.go retries the three transient
+ errors the client reports: connection reset, 503, and 429.
```

```text
- TODO: implement proper error handling here
+ return fmt.Errorf("parse config %s: %w", path, err)
```

```text
- def process_data(data):
-     # This function processes the input data and returns the result
-     ...
+ def process_data(data):
+     raise NotImplementedError
```

The first is `P3` plus `P40`: hype plus a claim with no actor and no number. The second is `C1` plus `C13`: a placeholder body, and the swallowed exception it hides. The third is `C2`: a signature that promises a result and a body that promises nothing. The last one is *missing work* under step 3: it goes to the build queue, and the honest report says the function has no implementation yet.

## 5. What this skill does not do

- It does not rewrite code that is correct but written differently. That is `modernize-coding`'s job, and it applies only when the project itself declares the newer idiom.
- It does not judge architecture, and it does not propose a pattern. That is `architecture`'s job.
- It does not rewrite the project to sound better. It removes residue from what the task already produced.
- It does not replace `quality`'s craft rules: table-driven tests, typed doubles, wrapped errors, and the rest stay where they are. This skill finds the residue those rules do not cover.
- It does not run on a surface the task did not touch, unless the user asks for a sweep of that surface.
