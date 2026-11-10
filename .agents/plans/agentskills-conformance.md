# Task graph — agentskills.io conformance for skills/

## OUTCOME (2026-11-10) — shipped as v8.0.0-beta.4

All units landed. PR #105 (feat -> develop) merged; PR #106 (develop -> main)
merged; tag `v8.0.0-beta.4` pushed; GitHub Release published as a prerelease
with a body identical to the CHANGELOG section followed by one trailing
newline (`scripts/release_notes.py --tag v8.0.0-beta.4` + `\n` == release
body, 3140 bytes).

- Gates 31 -> 34 (`layout`, `skillvoice`, `thirdparty` added).
- Always-on context ~8590 -> ~8159 tokens of a 9000 ceiling.
- Eval suite 103/103. `python3 scripts/check.py --all` -> exit 0 on the
  merged branch, on a fresh CI-style clone, and on a fresh recursive clone
  with the submodule materialized.
- The vendored draw.io skill: 6701 -> 1646 tokens, 279 -> 67 lines, valid
  single-line quoted description, identity off the activation surface. Token
  counts are the repo's own counter, `len(text.encode()) // 4`. The repo's
  gates reach it through `thirdparty` (pointer untracked, resolvable,
  documented); with the symlink present all 34 pass and the content stays
  outside the other gates by design, which is the boundary DONE_WHEN 6 asks
  for.
- The submodule pin (`fec9567`) was published to `bouroo/ai-skill` as
  `improve/conformance`; without it a fresh `--recursive` clone failed to
  resolve the pin.
- The pin lives on `improve/conformance` (`fec9567`), which is **not** an
  ancestor of `improve/layout-quality` (merge base `7b7c448`). That branch
  still carries the folded `description: >-` and the layout work; read the
  quoted description from the pin, not from `improve/layout-quality`.

### DONE_WHEN status

| # | criterion | status | evidence |
|---|---|---|---|
| 1 | `check.py --all` exits 0 | met | `OK (34 gate(s))` on the merged branch, on a fresh `--depth 1` clone, and on a fresh `--recursive` clone with the submodule at `fec9567` |
| 2 | new gate enforces the spec's content rules | met | `layout`, `skillvoice`, `thirdparty` added; 31 -> 34 |
| 3 | every description follows the description rules | met | `descriptions` + `skillvoice` pass; 10/10 open with `Use`, longest 662 chars (limit 1024), always-on ~8159 of 9000 |
| 4 | trigger set matches the spec's query shape | met | 8/8 to 10/10 per skill, train and validation both mixed; `triggers` gate passes |
| 5 | per-skill train rate reported, edits guided by train | **partly met** | the table below has all ten rows, but nine predate `4b292fc`; see its provenance note |
| 6 | vendored skill conformant, gates reach it | met, pointer sense | description is one quoted line, 760 chars, with a boundary; gates reach the pointer via `thirdparty`, not the content |
| 7 | beta release | met | PR #105 and #106 merged, annotated tag, prerelease published |

### Measured trigger rate (train split, `--model haiku`, 3 runs/query)

| skill | train | skill | train |
|---|---|---|---|
| architecture | 7/10 = 0.70 | modernize-coding | 6/10 = 0.60 |
| confluence | 6/10 = 0.60 | problem-details | 7/10 = 0.70 |
| delivery | 8/12 = 0.67 | quality | 5/10 = 0.50 |
| execution | 6/13 = 0.46 | security-audit | 7/10 = 0.70 |
| indexed-search | 6/10 = 0.60 | unslop | 6/13 = 0.46 |

Source: `/tmp/kilo/probe/meas-<skill>.log`, 07:22-08:05 on 2026-11-10, i.e.
**before** the final description commit `4b292fc` (10:23). Only `architecture`
was re-measured after it (`/tmp/kilo/measure/architecture.train.log`, 11:38,
7/10 unchanged). Nine of the ten rows therefore score the description as it
stood before the last body-and-description pass: the numbers satisfy DONE_WHEN
5 as a measurement, not as evidence about the shipped descriptions, and a
re-measure is owed before any such claim. Every `should-not-trigger` row scored
0.00 except one (`problem-details`, which over-triggers a single negative), so
the shortfall sits on the trigger side: a description that names the user's
situation rather than the skill.

These are three-run samples on a host whose router is `combo-free`, so they
read as direction, not precision.

## PROMPT

GOAL: bring every skill under `skills/` (and the future vendored skill) into
alignment with the three agentskills.io documents named by the user —
`specification.md`, `skill-creation/best-practices.md`,
`skill-creation/optimizing-descriptions.md` — then cut a beta release from
`main` with a beta tag.

CONTEXT: The repo is `bouroo/agents` (governance doctrine + on-demand skills).
Branch `feat/agentskills-spec` already landed the spec's *structural* half
(`license: Apache-2.0` on every skill, architecture `scripts/`+`assets/`,
modernize-coding references flattened to one level). It is green under
`python3 scripts/check.py --all`. The remaining work is the *content* half the
spec and the two best-practice guides ask for, plus the deterministic gates
that keep the next skill conformant. `scripts/check.py` is the single
verification surface (31 gates); CI runs it on every push and PR.

CONSTRAINTS:
- English; em-dash only (no en-dash in prose); no host/vendor tokens in
  doctrine; no new third-party dependency; stdlib only.
- Never edit or commit on `main`/`develop`. Work lands on
  `feat/agentskills-conformance`, then merges to `develop`, then `main`.
- Only push after the user authorizes the outward action.
- Every gate must stay green; a new gate must be a *deterministic* check, not
  a model call.

DONE_WHEN:
1. `python3 scripts/check.py --all` exits 0 on the merged branch.
2. A new gate enforces the spec's *content* rules that the repo does not yet
   enforce (imperative + pushy + boundary description shape; spec directory
   layout; reference one-level-deep).
3. All 10 skills' descriptions satisfy the optimizing-descriptions rules
   (imperative voice, user-intent framing, pushy scope, ≤1024 chars) and
   still fit the always-on token budget.
4. `evals/trigger.json` matches the spec's query-set shape (8-10 positives,
   8-10 negatives per skill; train/validation split).
5. Trigger rate measured on the train split is reported per skill with the
   measured number, and description edits are guided by train only.
6. The vendored "future skill" (`vendor/ai-skill` → `skills/drawio-hla-architect`)
   is conformant by the same rules, and the repo's gates reach it.
7. Beta release: version bumped, CHANGELOG section written, PR merged to
   `main`, annotated tag pushed, GitHub Release published as prerelease.

## Unit graph

```
U1 gates (scripts/check.py)  ──┐
                               ├──> U3 integrate+verify ──> U4 release
U2 content (10 skills + evals)┘
```
U3 also consumes U2's measured trigger rates. U4 is sequential (only after
U3 passes).

### U1 — spec-conformance gates  (branch `feat/conformance-gates`)
Owned files: `scripts/check.py`, `evals/suite.json` (new eval entries only),
`.github/workflows/validate.yml` (gate list lines).
Adds deterministic gates for rules the spec states but the repo does not
enforce. Does NOT edit any SKILL.md.

### U2 — skill content conformance  (branch `feat/conformance-content`)
Owned files: the 10 `skills/*/SKILL.md`, `skills/*/references/*.md` (as needed),
`evals/trigger.json`, `evals/run_triggers.py` (if needed).
Rewrites descriptions to the optimizing-descriptions shape and aligns skill
bodies with best-practices (gotchas/checklists/templates/validation loops),
respecting the 500-line/5000-token budget.

### U3 — future skill (vendored drawio) conformance
Sequential after U1 (needs the new gates to know what "conformant" means).
Owned files: the vendored skill's `SKILL.md` inside the submodule
`vendor/ai-skill` + the parent repo's submodule pin + `vendor/README.md`.
Constraint: the parent repo stores only a pointer; content lives upstream or
in the submodule's local branch `improve/conformance`.

### U4 — release
Sequential after U3. Owns version files, `CHANGELOG.md`, tag, GitHub Release.

## Verified facts (measured, not assumed)

Pre-work numbers below; the OUTCOME block carries the shipped state (34 gates,
~8159 always-on tokens, vendored skill 67 lines / 1646 tokens).

- `scripts/check.py --all` = 31 gates, exit 0 on `feat/agentskills-spec`.
- Always-on budget: AGENTS.md ~6724 + descriptions ~1866 = ~8590 of 9000
  tokens → only ~410 tokens (~1640 chars) of headroom for all 10 descriptions.
- Skill body headroom to 5000 tokens at `ab00fd9`: execution +1 token (!),
  quality +17, delivery +599; the other seven have >2200 (confluence +2235 is
  the smallest of them).
- Description shapes after the rewrite: 10/10 open with `Use …` (or `Use for`,
  `Use before`), each carries a clause keeping it in scope when the domain is
  not named, and each keeps a boundary. Re-measured pre-work state at `ab00fd9`:
  7/10 opened with an imperative verb and 3/10 with `Use …` (delivery,
  execution, quality), 6/10 carried "even if"/"even when". The earlier "4/10
  imperative" reading was not reproducible and is corrected here.
- `evals/trigger.json` shipped shape: positives/negatives per skill = architecture 8/8, confluence 8/8,
delivery 10/8, execution 10/8, indexed-search 8/8, modernize-coding 8/8, problem-details 8/8,
quality 8/8, security-audit 8/8, unslop 10/10. Spec says 8-10 of each, so all ten
are inside it. Pre-rewrite it was execution 13 and unslop 15 positives, both over.
- Measurement mechanics: `claude -p <q> --model haiku --output-format
  stream-json --verbose` emits `tool_use` `{"name":"Skill","input":{"skill":
  "<name>"}}` → the repo runner's default marker matches. Measured again on
  the merged branch: 30-80 s/run, and the cost driver is the init payload, not
  the prompt. `--strict-mcp-config` alone leaves ~$0.25-0.35/run, mostly MCP
  tool schemas; adding `--tools Skill,Bash,Read,Edit,Write,Glob,Grep,Task`
  drops the surface from 60+ tools to 8 and the run to ~$0.10, with the Skill
  call still firing first. Calibrate the marker with `--tools` in place,
  because the trigger decision is what is being measured, not the follow-up.
- The host loads skill content from `~/.claude/skills` (a symlink to the
  repo's `skills/`), so a *worktree* edit does NOT change what triggers.
  Measurement must run against the checkout that `~/.claude/skills` points at.
- Gate reach over the vendored skill, re-measured on the merged branch: with
  `skills/drawio-hla-architect` symlinked, all 34 gates pass and `thirdparty`
  reports "1 symlinked skill pointer(s) untracked and documented". The earlier
  reading (symlinking breaks `descriptions`, `skillbudget`, `evals`) predates
  the `_skill_dirs` symlink exclusion and is withdrawn.
- What "reach" means, measured rather than asserted: copied to
  `skills/zz-vendored-test`, the same content fails `frontmatter` (directory
  name != frontmatter name), `portable` (framework tokens in seven files),
  `privacy` (a numeric real-work identifier in `references/style-strings.md`),
  and drags `evals` red with it. So the gates reach the *pointer*, and its
  content stays out by design; DONE_WHEN 6 is satisfied in the pointer sense
  its own last clause asks for, not in the sense of the content passing them.
- The vendored skill: 6701 tokens / 279 lines (over the 5000 budget),
  `description: >-` folded YAML (the repo's line-based frontmatter parser
  reads only the literal `>-`), and it carries real-work identity.
- CI does not check out submodules (`actions/checkout@v4`, no
  `submodules:` key), so a submodule-backed skill is invisible to CI.
