# Task graph — search and diagnosis efficiency (GROW cycle 1)

## Origin

A real production run (2026-11-10, orch-mbf netPrice fix, VBG-78478) was measured
against its own transcript. The measurement is the evidence this cycle is built on.

### Measured baseline (298 tool calls, 270 bash)

| Signal | Count | Cost |
| --- | --- | --- |
| Tool calls before the first root-cause statement | 81 | 27% of the run |
| Tool calls before the fix unit was dispatched | 194 | 65% of the run |
| Bash calls returning nothing usable, discarded silently | ~137 | 51% of bash |
| `rg -rn` calls (silently wrong: `-r` is `--replace`, not `--recursive`) | 21 | 7% of bash |
| One-off python heredocs parsing the same trace files | 37 | 21% of bash |
| Write-to-`/tmp`-then-read-back round trips | 13 | pure overhead |
| Re-searches of one concept under different flags/spellings | ~104 (`voucher`), 78 (`installment`), 34 (`netPrice`) | the bulk of the empty calls |
| Root-cause narrations ("pinned"/"confirmed") | 33 | narration, not evidence |
| Files re-read after already being read | `installmentation.go` 15x, `utils.go` 9x | window churn |

The dominant cost was **not** the reasoning. It was re-searching one concept until
a query returned something, with no termination rule, plus a search-tool flag
(`rg -r`) that fails silently so a wrong result looks like a right one.

## Why the current doctrine does not catch this

- **§2 "Bounded evidence"** caps *identical* retries ("two fruitless lookups on
  one source"). The observed waste was *non-identical* re-searches of one
  concept under different flags and spellings. Nothing bounded that.
- **§2 "Tool routing"** says "known string -> search" but never says *how* to
  search once: no rule that a search tool's flags are themselves a failure mode.
- **`indexed-search` skill** owns the search mechanics and documents the engine
  ladder, but it is scoped to *slow or repeated* searches in *large* trees. The
  run's tree was small, so the skill never fired, and the one place that could
  have taught correct search mechanics stayed unloaded.
- No gate asserts any of this. Every gate in the repo checks that a rule is
  *present on a surface*; none checks that the rule is *loadable when needed*.

## Graph

Two independent units; no edge (neither reads the other's result). They own
disjoint files, so they may run in parallel.

### Unit A — doctrine surface

- **Owns**: `AGENTS.md`, `standalone/AGENTS.md`
- **Goal**: state the two rules that would have cut this run, in the intake
  section, on both installed surfaces.
- **Rule 1 (search discipline)**: a search that returns nothing changes the
  query, not the tool's flags, and a repeated concept is re-searched under one
  canonical form until a miss is established.
- **Rule 2 (diagnosis closure)**: a diagnosis is closed by a named check, not
  by a restatement; re-narration is not new evidence.
- **DONE**: `python3 scripts/check.py budget cost standalone` exits 0, and
  `AGENTS.md` stays within the 250-line budget and the token ceilings.

### Unit B — skill + gate surface

- **Owns**: `skills/indexed-search/SKILL.md`, `scripts/check.py`,
  `evals/suite.json`
- **Goal**: put the search mechanics where a run that searches will load them,
  and make the trigger fire on the *actual* trigger condition, not only on
  large trees.
- **B1**: extend the `indexed-search` skill with a short "search discipline"
  section: canonical form, one-query-one-concept, silent-flag-failure
  awareness, and a "write to stdout, not a temp file" rule for structured
  output.
- **B2**: widen the `indexed-search` trigger clause so it fires on *repeated
  searching* and *a search that returned nothing*, which are the conditions
  this run met and the skill did not.
- **B3**: add a deterministic gate `searchdiscipline` asserting the rule is
  present on the canonical surfaces, and add one eval that draws on the real
  run.
- **DONE**: `python3 scripts/check.py --all` exits 0; the eval suite reports
  `RATE 103/103` or better.

## Constraints

- KISS: the doctrine change is at most two clauses in §2 on each surface. No
  new section, no new skill, no config knob.
- The `indexed-search` skill is on-demand; its trigger clause is the only thing
  that decides whether it loads. Fixing the body without fixing the trigger is
  the failure this cycle is correcting, so the trigger change is in scope.
- The `portable` and `agnostic` gates forbid stack- and host-specific tokens.
  A rule that names a specific search tool's flag syntax violates `portable`.
  The rule must name the *capability* (a search tool that silently rewrites
  its output), with the concrete flag only inside the `indexed-search` skill,
  which is the surface that owns engine specifics.
- Every new gate must follow the repo's own conventions: a `RULE_SURFACES`
  entry, a `g_<name>()` function, registration in `GATES`, and a docstring that
  states the failure it prevents (the existing gates all do this).
- No change to `check.py`'s existing gate semantics.
- Budgets: `AGENTS.md` 250 lines / 7500 tokens; always-on 9000; standalone
  5500; skill body 500 lines / 5000 tokens; command 120 lines.

## Verification

The lead re-runs, independently of the units' own reports:
`python3 scripts/check.py --all` (34 gates green), the eval suite rate, the
`git diff` against `origin/develop`, and the budget numbers.

## Not in scope

- Changing the release-tooling skill that lives in the consuming repo.
- Any claim that the doctrine change alone fixes the run: the measurement is of
  one run, and the doctrine states the rule, not the outcome. The eval locks
  the rule's presence, not the run's duration.
