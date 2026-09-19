# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Pre-4.0 entries were retired in the v4 fresh start; the full history lives in git
tags and log (`v1.0.0` through `v3.11.0`).

## [6.4.0] - 2026-09-19

Stable promotion of the 6.4.0 series. `beta.1` through `beta.3` shipped the craft
simplicity rule, the modernize-coding re-scope with four language adapters, and
the security-audit skill; those sections are kept below as their own record, and
this release adds the MiniMax Code host and plugin route.

MiniMax Code (`mcode`) joined the distribution layer, and it is the first host
with no global instruction file. Every other host installs the manifesto into a
config directory (`CLAUDE.md`, `SOUL.md`, `AGENTS.md`); MiniMax Code reads
`AGENTS.md` from the workspace root and documents no user-level rules path, so a
global install for it links **skills only**. Rather than invent a
`~/.minimax/AGENTS.md` the host does not read, the installer models the absence:
a host row may leave its instruction field empty, install and uninstall skip that
surface, and the README states the workspace contract.

The second surface is the plugin route. MiniMax consumes plugins from a public
GitHub repo whose root carries `.minimax-plugin/plugin.json` — a shape this
repository already satisfies, since that manifest sits at the canonical path
beside the existing plugin/extension families. Its `skills` array names each
`SKILL.md` as a file path rather than a directory, and `schemaVersion` is the
integer `1`.

Compatibility was checked against MiniMax's own tooling rather than assumed. All
seventeen skills pass the bundled `lint-skill.js` on every rule it enforces
except one, where the linter strips a link's `../` prefix and resolves the
remainder against the skill's own directory — so a legitimate cross-skill link
such as `../verification/references/evolution.md` is misread as a missing
same-skill `references/evolution.md`. The files exist and this repository's
`links` gate, which resolves the path correctly, passes. The skills are
unmodified; the false positive is recorded here rather than worked around.

### Added

- **`.minimax-plugin/plugin.json`** — MiniMax Code plugin metadata at the host's
  canonical path, making the repository root directly installable as a MiniMax
  plugin from GitHub. Registered in the `manifests` gate, which now holds six
  manifests to a single version.
- **MiniMax host row** in `scripts/install.sh` — links `skills/` into
  `~/.minimax/skills`, the user-scope skill root MiniMax's own `skill-creator`
  documents.

### Changed

- **`scripts/install.sh`** — a host may now declare no global instruction file:
  the row's instruction field is empty, install/uninstall skip that surface, and
  `status`/`list` report it as project-level instead of printing an empty name.
- **`scripts/check.py`** — the `manifests` gate covers the sixth manifest, and
  the `agnostic` gate forbids `minimax`/`mcode`/`mavis` tokens in core doctrine.

## [6.4.0-beta.3] - 2026-09-18

The doctrine had no security discipline of its own. `cmd-review`'s Security row
was one line — input validation, authorization, no logged secrets, dependency
sanity — and `cmd-verify`'s Scan stage said never to auto-fix a security finding
without saying what one *is*. The missing piece was not detection; it was the
test that separates a real boundary violation from a best-practice deviation. A
review without that test produces a list of "add a rate limit" and "consider
rotating keys", which costs an owner more to triage than it is worth, and buries
the one real defect underneath it.

`skills/security-audit` is that test. Its load-bearing rule is the **candidate
gate**: a finding must name the lower-trust principal, the input or action it
controls, the intended control, the boundary crossed, the affected principal or
resource, and the concrete result — all six, or it is not a finding. This is the
manifesto's §0 anchor discipline aimed at security: the chain has to terminate
in a real victim and a real effect rather than in a missing practice, a guessed
deployment, or self-impact.

Two structural borrows. A **`needs_validation`** state, distinct from confirmed
and from rejected, carrying one exact missing fact — a proxy, identity provider,
or deployment behavior absent from the repository — and explicitly **no
severity**, because a blocked hypothesis is not a low-confidence finding. And
**coverage units** of entry surface × boundary × attack class rather than files,
with `references/attack-classes.md` carrying the classes and per-domain hunter
rules. Severity is calibrated to demonstrated impact, with the discriminator
made explicit: does the result fully defeat an explicit control, or only weaken
it?

**What was deliberately not ported.** The source skill enforces its execution
safety with an OS sandbox, a descriptor-based artifact-promotion ladder, and a
budget ledger — machinery that is correct where an agent runs hostile target
code and is unpayable here, where the audit reads a repository that is already
the user's own. The skill states the gap rather than inheriting the promise:
here the execution boundary rests on the `AUTH:` gate and §10, and it says so.
The audit is read-only and describes fixes; it does not edit the target.

### Added

- **`skills/security-audit`** — a 76-line skill plus a 96-line attack-class
  reference, loading [craft](skills/craft/SKILL.md), [verification](skills/
  verification/SKILL.md), [teamwork](skills/teamwork/SKILL.md), and the
  lifecycle rather than restating them. Guidance is the default mode: a security
  question, a focused review, or triage of a reported finding writes no files.
  The full audit workflow — and a `REPORT.md` — runs only on explicit request.
- **Skill count 16 → 17** across all five manifest descriptions and their three
  skill arrays, plus the README tree and the manifesto's §11 repository map.

### Fixed

- **The `modernize` gate no longer fails on an older toolchain** (`668cc3f`,
  carried into this release). Its first CI run failed because GitHub's runners
  ship older Go and JDK than a developer machine: their `GOROOT/api` has no
  record of a symbol added after it, and the gate read that absence as a false
  claim. An older toolchain having no record of a later feature is evidence that
  host cannot judge it, not that the claim is wrong — and a gate that is red on
  CI only is the worst place to discover a verdict that cannot be trusted.
  Claims above the detected toolchain are now counted and reported as not
  judgeable on that host, while every claim the host *can* judge is still
  verified and a wrong one still fails.

## [6.4.0-beta.2] - 2026-09-18

Modernization stops being a language fact and becomes a project fact. Users
reported generated code and patterns coming out outdated; the cause was a wrong
fact in the doctrine, not model drift, and it was wrong in the direction that
produces the complaint. Told `maps.Copy` needs Go 1.23, an agent on a `go 1.21`
module believes it is unavailable and hand-writes the legacy loop the skill
exists to retire.

`skills/go-modernize` becomes `skills/modernize-coding`, and "modern" is now
defined by the project you are working in rather than by a language release. The
skill derives a ceiling from what the project declares (`go.mod`,
`package.json` `engines`, `tsconfig` `target`, `requires-python`), what its
tooling actually runs, and what its neighbours do — then modernizes toward that
ceiling and never past it. Go becomes the first of five language adapters.

Tagged as a **beta**: continuing the open 6.4.0 series, whose beta.1 is already
published. The skill rename is breaking under semver, but 6.4.0 has only ever
existed as a beta, so no stable consumer contract breaks here — that question
properly belongs to the 6.4.0 → stable promotion.

### Fixed

- **Four wrong version claims in the Go table**, corrected against `GOROOT/api`,
  the toolchain's own record of when each stdlib symbol landed: `maps.Copy` and
  `maps.Clone` are 1.21 (not 1.23); `fmt.Appendf` is 1.19 (not 1.20);
  `plusbuild`'s `//go:build` is 1.17 (not 1.18). Compile probes cannot settle
  this — the `go` directive gates language features, not stdlib availability —
  so `GOROOT/api` is the anchor that decides, and the tests that would have
  "confirmed" the wrong versions actually prove nothing.
- **`.cursor-plugin/marketplace.json` was two major versions stale** (found by
  the `TWINS:` sweep): it advertised "fourteen on-demand skills", listed
  `plan-authoring` (the pre-v6 name of `artifacts`), and omitted `artifacts`,
  `evals`, and `lifecycle`. All five manifests now agree.

### Added

- **Four language adapters**, each verified against a real toolchain rather than
  recalled: **Java** (API claims anchored to the JDK's own `src.zip` `@since`
  tags — Java's `GOROOT/api` analogue — and language features pinned by
  compiling each against `javac --release N` and taking the first release that
  accepts it: records 16, switch expressions 14, pattern-matching switch 21);
  **Rust** (verified in a scratch crate — `clippy --fix` genuinely rewrote
  source, `cargo fix --edition` migrates both `Cargo.toml` and source, and cargo
  enforces `rust-version`); **Python** (anchored to the library reference's
  structured "Added in version" notes and the what's-new page announcing each
  PEP, runtime-verified on 3.14.7); **TypeScript/JS** (editions anchored to
  TC39's finished-proposals publication years).
- **A `verify.md` per doc-anchored adapter** recording how to re-derive its
  table, including the two traps hit and corrected while building them:
  windowing over flattened prose attributes the *next* entry's version note to
  the symbol (this reported the dict-union operator as 3.8 and
  `typing.override` as 3.11 — both wrong), and a keyword scan over what's-new
  finds the first page that *mentions* a feature, not the one that introduced
  it.

### Changed

- **The `modernize` gate covers all five adapters**: every claim must be
  version-pinned, and Go and Java are cross-checked against two independent
  local anchors. Where an ecosystem ships no local machine-readable index, the
  gate says so in its own output rather than letting a uniform `PASS` imply
  uniform rigor.
- **The cross-check is version-aware.** A toolchain older than a claim's
  feature has no record of it — an older `GOROOT/api` lacks the symbol, an older
  JDK lacks the `src.zip` entry — and that absence is not evidence the claim is
  wrong. Counting it as failure made the gate machine-dependent and red only on
  CI, whose runners ship older Go and JDK than a developer machine; the first
  push of this very release failed that way. Claims above the detected toolchain
  are now counted and reported as not judgeable on this host, while every claim
  the host *can* judge is still verified and a wrong one still fails. The JDK
  version is read from the `release` file that sits beside the `src.zip` being
  read, so the version always matches the source actually examined.
- **`AGENTS.md` §11, `README`, and the adapter table** re-point at the renamed
  skill and its adapter set.

## [6.4.0-beta.1] - 2026-09-18

The simplicity rule stops being a ranking. §1 put Simplicity third and §10
banned speculative features, but nothing was actionable: no clause told an agent
to prefer the least mechanism, no rubric row let a reviewer reject an
unnecessary abstraction, and no gate failed when the rule was diluted. Users saw
the result as code too complex to read and maintain. The rule is now sharp:
decidable tests for when structure has earned its place, and a counterweight so
that "simpler" never means "smaller diff."

Tagged as a **beta**: this is the same additive shape as v6.3.0, cut ahead of a
stable patch so the release path runs end-to-end before the change is advertised
as the latest download.

### Added

- **`skills/craft` — a `Simplicity` section** (loaded on demand): the default is
  the least mechanism that works — the standard library before a dependency, a
  plain function before a class, a direct call before a layer. Four named classes
  of unintended complexity, each a defect: speculative abstraction (extract on
  the second concrete caller, never the first imagined one), dead configurability
  (a knob nobody turns), indirection the reader must decode (a wrapper that only
  forwards), and a dependency for the trivial. Flagged in review with the cost
  named — "this serves one caller and adds a file every change must cross" is a
  finding; "this feels complex" is not.
- **A `simplicity` gate** in `scripts/check.py`: the rule must be present on both
  canonical surfaces (the always-loaded manifesto clause and `skills/craft`), so
  neither can silently drop it. It shares a rule-presence helper with the
  `comments` gate rather than duplicating it, so a third such rule costs one
  dict entry.
- **An eval case** — `simplicity-rule-survives-doctrine-edits` — so a doctrine
  edit that drops the rule from either surface fails the suite.

### Changed

- **`AGENTS.md` §5** carries the always-loaded clause in place: least mechanism,
  complexity pays its way, no abstraction before a second real caller, no flag
  nobody sets, no forwarding wrapper, no dependency for what the standard library
  does — and simplicity never overrides correctness.
- **`AGENTS.md` §10** extends the speculative-feature ban to a layer, flag,
  wrapper, or dependency that has not earned its cost.
- **`cmd-review`** gains a Simplicity rubric row: a finding must name a concrete
  cost or it is taste, not a defect, and a needed error path or clarifying name
  is never traded for a smaller diff.
- **Doc drift swept**: the gate count on the README verification table and
  `validate.yml`'s gate list now include `simplicity`.

## [6.3.0] - 2026-09-18

The comment rule stops being inert. "Default is no comment, add one only for the
*why*" was already true and already written down — it sat mid-paragraph in §10
with no language named, no length bound, and no check, so it lost to the model's
prior of commenting everything. Users saw the result as comment spam in code the
agents wrote. The rule is now sharp: it names the noise classes, points at each
language's own convention, and bounds length by the code rather than the shape.

### Added

- **`skills/craft` — a `Comments` section** (loaded on demand): default is no
  comment, earned only by a non-derivable *why*; four named noise classes deleted
  on sight (restates the code or signature, narrates the change, banners inside a
  short function, a doc block longer than the code it documents). The governing
  line is that **language conventions set the form, the code's complexity sets
  the length** — a one-line function gets a one-line doc — with a pre-emit test:
  if a correct refactor would make the comment wrong, it was noise.
- **A `comments` gate** in `scripts/check.py`: the rule must be present on both
  canonical surfaces (the always-loaded manifesto clause and `skills/craft`), so
  neither can silently drop it. The gate asserts presence, not wording — prose
  cannot be linted for meaning — so rewording either surface means updating its
  marker. That is the deliberate cost of gating prose rather than code.
- **An eval case** — `comment-rule-survives-doctrine-edits` — so a doctrine edit
  that drops the rule from either surface fails the suite.

### Changed

- **`AGENTS.md` §10** carries the sharpened clause in place, same line: three
  named spam modes, the per-language conventions (GoDoc, TSDoc, PEP 257,
  rustdoc, Javadoc), and "at that convention's minimum length."
- **`cmd-review`** makes comment noise flaggable in the readability rubric rather
  than tolerated; **`cmd-refactor`** deletes restating comments during Execute
  instead of porting them to the new shape.
- **Doc drift swept**: the gate count on the README verification table and
  `validate.yml`'s gate list now include `comments`; a stale README line still
  crediting `craft` with four artifact gates rather than five was corrected;
  the stray space in the README's "sixteen on-demand skills" was fixed and the
  skill-tree description realigned.

## [6.2.0] - 2026-09-15

The intake gate: an agent now surfaces its **corrected reading** of an ask and
waits for confirmation before acting on it. A restatement recites the ask; a
correction states the reading the run will execute, filling in what the ask left
implicit — vague scope, unstated constraints, missing `DONE_WHEN` — and a wrong
correction silently steers everything downstream, costing more to undo than it
costs to confirm.

### Added

- **`PROMPT:` — the fifth decision-point gate.** One concise English paragraph,
  GOAL / CONTEXT / CONSTRAINTS / DONE_WHEN (§4.2), owed at intake before the
  first edit or command, joining `INTENT:` / `TWINS:` / `AUTH:` / `PENDING:` in
  the `craft` gate definitions. Deliberately **corrective, not a restatement**:
  the agent resolves the ask's implicit content, surfaces that reading, and
  **stops for confirmation of the reading** before acting. The stop confirms a
  reading, not a decision, so it does not reopen any lookupable fact and does not
  collide with `Decide, don't ask`; a trivial ask is the only exemption.
- **The unguessable correction is itself the question.** When the wording is
  ambiguous or self-contradictory, a detail would be guessed rather than read, or
  no one is present to answer, the correction is owed as one pointed question
  carrying the recommended interpretation instead of an action taken on a guess.

### Changed

- **Every surface that enumerates the gate set** now carries `PROMPT:`: the
  README one-line doctrine, `AGENTS.md` §2 (intake prose, the class-exit
  condition, and the §3 gate block), `skills/craft` (canonical definition),
  `skills/lifecycle` (stage-seam list), `skills/verification` (artifact-line
  check), `commands/cmd-verify` (artifact-gate sweep), and the intake flowchart
  in `skills/verification/references/flowcharts.md`, which now routes
  *not trivial* → pin the corrected reading → confirm (cap: 2 rounds) → fit gate
  rather than pinning before the trivial test. The confirmation loop is capped at
  two rounds, so the gate cannot stall a run indefinitely.

### Motivation

- Measured across the change: **7 files, +18 / −10 lines**, +8 net, roughly 440
  added words carried by the always-loaded manifesto and the on-demand docs. No
  new skill, no new mechanism: the gate is a paragraph in files that already own
  intake, plus one node in the existing flowchart. `AGENTS.md` holds at 150/250
  lines, inside the budget gate.
- `python3 scripts/check.py --all` → `OK (7 gate(s))`: budget, frontmatter,
  links, agnostic, manifests, privacy, evals all pass on the released commit.

## [6.1.0] - 2026-09-14

Harness hygiene: five load-bearing ideas the doctrine lacked, drawn from a gap
analysis against Anthropic's Claude Code best-practices guide. Each folds into a
skill that already owns the territory — no new skill, no new gate. The v6
lifecycle's pending stable-`6.0.0` promotion is superseded by this release.

### Added

- **`skills/verification` — how hard a check grips the stop.** Four rungs, each
  trading setup for attention: in-prompt iteration, a standing cross-turn
  condition, a deterministic gate or hook, and an independent verifier. The
  governing rule: *a check that must always run becomes a gate; a check that
  only guides stays a sentence.* This is the minimal-harness ladder applied to
  verification, and the reason the repository's own gates exist.
- **`skills/craft` — instruction-file hygiene.** The prune test (*would removing
  this line cause the agent to err?*), what to include versus what the agent can
  read for itself, and two diagnostics: a rule that keeps being ignored means the
  file is too long — cut, don't re-emphasize; a question the file already answers
  means the phrasing is ambiguous.
- **`skills/evals` — running unattended.** Three conditions for a run with no
  human reading the transcript: the check gates the stop, the tool surface is
  pre-scoped, and authority still terminates in a human. Autonomy is a degree of
  attention, never a degree of authority.
- **`commands/cmd-review`** and the `verification` failure table — the
  over-reporting reviewer: a gap hunt always finds gaps, so chase only what
  affects correctness or a stated requirement; the rest is optional.

### Changed

- **`AGENTS.md`** — four pointer clauses, no added lines (147/250 throughout):
  §2 prefers an installed CLI to a hand-rolled API call; §4.2 hands the artifact
  rather than describing it; §7 names the grip ladder; §8 adds the two-correction
  reset and the compaction directive.

### Motivation

- Measured, not asserted: the doctrine held at **+26 lines** across five files,
  with `AGENTS.md` flat because the new material is inline clauses rather than
  new sections. `python3 scripts/check.py --all` → `OK (7 gate(s))`; the
  `agnostic` gate was driven red on a host token and restored green; all five
  eval checks were executed directly rather than merely validated.

## [6.0.0-beta.2] - 2026-09-12

Second beta of the v6 lifecycle foundation: a context-reduction pass over the
always-loaded manifesto and the workflow docs. **No behavior changed** — every
rule survives, verified by a rule-token sweep across all nine files.

### Changed

- **`AGENTS.md`** (166 -> 147 lines): §4's stage table — a verbatim copy of the
  lifecycle skill's — becomes a one-line artifact chain that keeps every
  stage -> artifact -> **seat** mapping; §2's tool-routing and built-in-preference
  paragraphs merge into one; §7's L1/L2/L3 bullets collapse inline; §4's
  duplicated "human judgment" paragraph folds into the seats section. The Shape
  gate gains an explicit exit condition.
- **`commands/`**: `cmd-verify` states its three-iteration cap once and folds the
  hook gate and reporting into the pipeline; `cmd-review` collapses the severity
  list to one line and gives the stale-tree case an explicit stop; `cmd-refactor`
  and `cmd-document` group their hand-back conditions under `Done =`.
- **`skills/craft`** (72 -> 64 lines): the "Style priorities" list — 5 of the
  manifesto's §1 entries — is deleted; the skill now points at §1 as the single
  owner.
- **`skills/performance`**, **`skills/domain-modeling`**: gain an explicit exit
  condition — the only two skills in the set that lacked one. Performance's
  external-bottleneck section now points at its reference.
- **`skills/graph-engineering`**: section references corrected to §4.2 and a
  lifecycle cross-reference added.

### Motivation

- The manifesto and its docs load on every run, so their line count is a
  recurring context cost. A measured duplication sweep first: one duplicated
  sentence across 16 skills, so the reduction is concentrated where it pays —
  `AGENTS.md`, the always-loaded file. Three files (`cmd-refactor`,
  `cmd-document`, `graph-engineering`) were restructured for cohesion at zero
  line change; that is recorded here rather than claimed as a saving.

## [6.0.0-beta.1] - 2026-09-12

First published form of the v6 lifecycle foundation. Tagged as a **beta**: the
publish flows that ship the release are new this cycle and have not yet run
end-to-end in CI, so the tag is marked prerelease and does not become the
"latest" download for consumers until a stable tag is cut.

### Added

- **`scripts/release_notes.py`**: prints one version's CHANGELOG section
  verbatim, so a release body is the committed bytes rather than a
  paraphrase. Exits non-zero when a tag has no matching section, failing the
  release instead of publishing an empty body.
- **`.github/workflows/release.yml`**: on a pushed `v<major>.<minor>.<patch>`
  tag, re-runs the gates on the tagged commit, extracts the release body, and
  publishes the GitHub Release. A tag carrying a prerelease suffix (`-beta.1`,
  `-rc.1`) is marked `prerelease: true` and never becomes "latest"; promoting a
  beta to stable is a new tag on the merge commit, never a re-point of the tag
  already published.
- **`skills/lifecycle/`**: the doctrine's new spine — the AI-native delivery
  lifecycle. Seven stages (intent, spec, plan, build, test, release, operate),
  the artifact each commits, its exit check, and the seven **seats** that own
  them (Originator, Steward, Architect, Implementer, Verifier, Approver,
  Operator). The loop is explicitly non-linear: `Test -> Build` is the canonical
  review back-edge and `Operate -> Intent` reopens the lifecycle. Two
  constraints never bend however the seats collapse — the Implementer never
  approves its own work, and the Verifier is independent of what it judges.
  Org-specific roles collapse into the seven (release manager -> Approver,
  auditor -> Verifier, on-call -> Operator). Distilled from Anthropic's
  *AI-native SDLC playbook* as method; its org apparatus and host product
  mechanisms are deliberately not adopted.
- **`skills/evals/`** and **`evals/suite.json`**: continuous evals as a named
  control — a harness regression suite of realistic tasks, each a prompt plus
  objective checks, run on schedule and on any change to the manifesto, a
  skill, a hook, or the pinned model. A change that lowers the pass rate blocks
  the merge. Evals are how GROW proves an evolution helped rather than merely
  shipped.
- **`evals` gate** in `scripts/check.py`: validates that `evals/suite.json`
  exists and every eval is well-formed (non-empty id, prompt, and mechanical
  checks carrying a `cmd` and an `expect_exit`). The suite is now seven gates.

### Changed

- **`AGENTS.md`**: re-authored onto the lifecycle spine. §4 becomes **The
  Delivery Lifecycle** (stage/artifact/seat/exit-check table, the loop's
  back-edges, the seat cast, human judgment at the seams, evals as the
  process regression control); the execution graph moves to §4.2 as the engine
  that shapes work *inside* a stage. §7 gains the evals-regression rule; §11's
  map lists the three new skills. Budget raised 200 -> 250 lines; the manifesto
  is 166.
- **`skills/plan-authoring` -> `skills/artifacts`**: generalized from one
  artifact to the chain — deterministic `intent.md` and `spec.md` shapes added
  alongside `PLAN.md` and its `STATUS.md` ledger, one artifact per lifecycle
  stage. All live referrers updated (`AGENTS.md`, `README.md`, `grilling`,
  `verification`, `wayfinder`); historical CHANGELOG entries are not rewritten.
- **`skills/graph-engineering`**: reframed as the grammar of work *inside* a
  stage, composing with the lifecycle rather than being the top level;
  section references now point at §4.2.
- **Commands** re-pointed at their stages: `cmd-verify` and `cmd-review` ->
  Test, `cmd-refactor` -> Build, `cmd-document` -> Spec.
- **`README.md`**: rewritten around the lifecycle foundation; skill tree,
  execution-graph section, one-line doctrine, and the gate table updated.
- Version fields bumped to 6.0.0 across the four versioned manifests, and each
  manifest's skill list expanded from fourteen to sixteen.

### Motivation

- v5 answered *how one job runs* (the execution graph) but had no answer for
  *where a job sits in the delivery loop, what artifact it commits, or who owns
  an approval* — the foundation-level absence the SDLC playbook names. Its
  thesis, that code stopped being the bottleneck once agents could write it
  faster than humans could plan and ship around it, reorganizes the doctrine
  around a non-linear artifact-driven loop with human judgment concentrated at
  the approval seams. The other three researched sources (Bowne-Anderson's
  harness article, the flowtivity graph-engineering guide, the z.ai devpack
  best-practice page) were audited and found already distilled as of 5.7.0 or
  carrying no adoptable delta; their material stays where it is.

## [5.7.0] - 2026-09-12

### Added

- **`skills/graph-engineering/references/harness-design.md`**: the harness-design
  reference the execution-graph grammar lacked — the minimal-harness ladder
  (prompt/retrieval -> fixed workflow -> agent loop) with the walking-skeleton
  build order; the pattern catalogue (augmented LLM, prompt chaining, routing,
  parallelization, orchestrator-workers, evaluator-optimizer, agent) mapped onto
  the grammar's shapes and edges; voting vs. sectioning with the decorrelation
  caveat; tool-surface (ACI) design — document for the model, poka-yoke the
  arguments, iterate on observed misuse; scoping the tool surface; server-side
  context injection; layer attribution for failures; and the anti-framework
  stance. Distilled from Anthropic's *Building effective agents* and Hugo
  Bowne-Anderson's *Stop overengineering your agent harness*, adopted as method
  with numbers re-derived locally.

### Changed

- **`skills/graph-engineering`**: the description, three new short sections
  (enter at the least-agency rung; fan-out's two rationales; design the tool
  surface), three new common-mistake rows, and the reference linked. The agency
  ladder is named as the shape ladder viewed from the agency axis.
- **`AGENTS.md`**: §4 routes to the minimal-harness ladder — enter at the least
  agency that closes on evidence, a prompt or fixed workflow before an agent
  loop, the smallest shape before a graph; §11's graph-engineering row lists the
  new reference.
- **`skills/teamwork`**: the spawn-brief contract now scopes the worker's tool
  surface to its task — a narrower surface means less confusion, misuse, and
  injection exposure.
- **`skills/verification`**: Diagnosis attributes a failure to its layer —
  reasoning, tool interface, context, or control flow — before patching, since a
  wrong-layer fix is a symptom patch by construction.
- **`README.md`**: the skills tree lists the harness-design reference.
- Version fields bumped to 5.7.0 across the four versioned manifests.

### Motivation

- The doctrine governed how one job runs (shapes, typed edges, caps, anchors,
  cost) but said little about designing the harness that runs it. A coverage
  sweep against the two sources found the workflow-vs-agent ladder,
  voting-vs-sectioning, tool-surface (ACI) design, scoped tool access,
  server-side context injection, layer-attribution diagnosis, and the
  anti-framework stance absent, with the correlated-lens hazard present but
  voting unnamed. The reference adds the missing method without restating what
  the "Right-size, don't overengineer" banner and the Kirby Effect already
  encode — those are sharpened, not duplicated.

## [5.6.0] - 2026-09-11

### Changed

- **`AGENTS.md`**: the completion-non-authorization rule generalized to all
  destructive and outward-reaching commands, example-free — finishing a task,
  a clean tree, or a green build authorizes nothing beyond it; §3's AUTH gate
  and §10's hard constraint both state the general form, with outward steps
  named in `PENDING:` until the user approves.
- **`skills/craft`**: the AUTH gate definition carries the same generalization,
  with the concrete `PENDING: <step> - awaiting your authorization` pattern.
- Version fields bumped to 5.6.0 across the four versioned manifests.

### Motivation

- Review feedback on v5.5.0: naming `git push` alone was too narrow — the same
  completion-non-authorization logic covers every outward or irreversible step
  (pushes, releases, deletes, publishes). v5.5.0 had shipped an hour earlier
  in the same day; the generalization replaces the narrow rule before any
  dependent procedure could anchor on it.

## [5.5.0] - 2026-09-11

### Changed

- **`AGENTS.md`**: `git push` is now named as the canonical AUTH case (§3) —
  finishing a task, a clean tree, or a green build never authorizes reaching the
  remote; agents end at local commits and report. §10 gains the matching hard
  constraint: never `git push` without the user's explicit go-ahead; ending at
  local commits with the push named in `PENDING:` is a clean exit.
- **`skills/craft`**: the AUTH gate definition carries the same weave — the
  completed-task/clean-tree/green-build non-authorization and the concrete
  `PENDING: push - awaiting your authorization` pattern.

### Motivation

- Users reported agents pushing to the remote as a side effect of finishing a
  task. The doctrine's AUTH gate spoke of outward effects only in the abstract,
  and nothing said "done ≠ pushed". The rule is now named at every surface that
  enforces AUTH, with host-side enforcement (permission ask-rules / hooks)
  remaining a per-machine, per-host concern — the doctrine portable layer
  states the rule; the deterministic layer is owned by each harness config.
- Version fields bumped to 5.5.0 across the four versioned manifests.

## [5.4.0] - 2026-09-11

### Added

- **`skills/confluence`**: the read-collapse playbook — when page-body reads return
  `<<ccr:…>>` pointers instead of content, the pointer is a *deterministic* cached
  result (identical retries are futile; cap two per variable change), with read
  fallbacks (title-scoped `siteSearch` probes — `ancestor` excludes the parent
  itself; adjacent-version `page_diff` as both read oracle and post-edit recovery
  for section edits) and write discipline while reads are down: schema-bounded
  sections only, no changelog/dictionary rewrites, no full-body reconstruction from
  excerpts; park gaps in a dated footer comment.

### Changed

- **`AGENTS.md`**: §2 bounded evidence now treats pointer/ref results as
  deterministic — cap identical retries at two, then vary one variable or hand the
  blocker back; §10 gains two hard constraints — never loop a failed call on
  identical arguments (transient transport faults excepted), and never overwrite
  content unread in-session (append-only or schema-bounded fallbacks + PENDING;
  a body rebuilt from excerpts/memory and pushed over an unread original is
  fabrication).
- Motivation: the 2026-09-11 MBF-wiki sync hit a collapsed-read retry loop, then a
  near-miss pair of fabricated full-body rewrites (caught before push, originals
  intact). The recovered techniques — diff-as-recovery-oracle, schema-bounded
  section edits, footer-comment checklists — are promoted from episode to doctrine.
- Version fields bumped to 5.4.0 across the four versioned manifests.

## [5.3.0] - 2026-09-10

### Changed

- **`skills/plan-authoring`**: the execution ledger is no longer a plan section —
  PLAN.md is a planning-phase artifact, and execution state lives in a sibling
  `<slug>/STATUS.md` (dated, newest on top, cite-don't-narrate, probe-before-write
  unchanged). Plans-root index rows gain a STATUS.md link; the drift sweep now hunts
  `Execution status` inside PLAN.md; nine sections become eight;
  [verification](skills/verification/SKILL.md)'s judgment-contract cross-reference
  follows the ledger.
- Version fields bumped to 5.3.0 across the four versioned manifests.

## [5.2.0] - 2026-09-10

### Added

- **`skills/indexed-search`**: drive a trigram-indexed search tool when the host
  has one — probe first, drive the index/serve lifecycle when present, fall back
  to ripgrep then the built-in Grep; no install steps. Covers the index-earns-keep
  decision, staleness rules (`--no-index` for fresh edits; a stale-index miss is
  not evidence of absence), `--` pattern discipline, machine output (`--json`,
  `--vimgrep`, `-q` exit codes), and the flags that silently degrade to a full scan.

### Changed

- **Skill count 13 -> 14** across all discovery surfaces: AGENTS.md §11 repository
  map and §2 tool routing, README, and the five marketplace manifests. Version
  fields bumped to 5.2.0.

## [5.1.0] - 2026-09-10

### Added

- **`skills/plan-authoring`**: the deterministic plan-document pattern — one `PLAN.md`
  per effort with a fixed nine-section order, work packages as `WPn`, a DONE_WHEN
  checklist of executable checks, a dated status ledger, and a grounded mermaid
  diagram; deterministic alignment/drift sweep included. Grilling's approved plan,
  wayfinder's graduated decisions, and verification's judgment contract now all
  route through it.

### Changed

- **Skill count 12 -> 13** across all discovery surfaces: AGENTS.md §11 repository
  map, README, and the five marketplace manifests (`.claude-plugin`,
  `.cursor-plugin`, `gemini-extension.json`), whose descriptions now list
  plan-authoring. Version fields bumped to 5.1.0.
- **README verification section drift fixed**: documents the six gates (the v5.0.1
  `privacy` gate was missing) and the `plan-authoring` tree entry.

## [5.0.1] - 2026-09-09

### Added

- **`skills/confluence` storage-form template anchor**: decoded a live family
  page (v5; its identity lives in machine-local memory, never in the
  doctrine) and recorded it as
  the mcp-atlassian surface of the "BFF API Specification" family in
  [references/page-template.md](skills/confluence/references/page-template.md) — H2/H3 ladder and `<hr>` rhythm, editor-v2 table attributes (`ac:local-id` / `data-table-width` / `data-highlight-colour`), status/expand/code macro forms, M/O span syntax, changed-row `#fffae6` shading, sample-wrapper captions, and both table column sets. The template-match workflow now graduates decoded anchors into instance-variant records, and the publish checklist (now six gates) validates against the matched anchor.

### Changed

- **`skills/confluence` SKILL.md diagram and prove rules tightened**: the `data` param must be encoded by the reference's **gated encoder** (percent-encode `safe="/"` → raw deflate level 6 → padded base64; pure base64, no `%`) with its `GATE OK` line obtained **before** any publish; publish-then-prove now names the `<<ccr:…>>` collapsed-read-back failure mode and routes it to the diff/version/search probe ladder.

## [5.0.0] - 2026-09-09

v5 re-authors the doctrine's execution model from a cycle to an **execution graph**, absorbing four graph-engineering sources — flowtivity's 2026 guide, Eigent's graph-engineering and self-evolved-agents essays, and the arXiv survey 2608.21156 — while keeping v4's gates, verification layers, and budgets intact. Section numbering unchanged (§2 intake … §11 map).

### Added

- **Anchors (§0, §10)**: every proof chain terminates in a fixed external node — a spec clause, the user's own words, a red test, captured command output — the machinery may read but never rewrite; the authority rank is restated as the anchor ordering (user statement > spec > checks > code).
- **`skills/verification/references/evolution.md`**: governed self-evolution — GROW formalized as instrument -> propose -> validate -> commit, with intra-/inter-episode cadence, read-only anchors and evidence standard, adversarial validation, and the Kirby audit at model upgrades.
- **`skills/graph-engineering` knowledge edges**: `SUPERSEDES`, `DEPENDS_ON`, `DECIDED_BY`, `CAUSED`, `IMPLEMENTS`, `REFERENCES` — dated like facts.

### Changed

- **`AGENTS.md` §4 "The Execution Graph"** replaces the loop as the execution model: THINK -> ACT -> PROVE -> GROW are role-nodes; edges are typed and conditional; every cycle is capped; the forbidden shape is the unrouted cycle. §8/§9 name the three graphs (task / coordination / state).
- **`skills/graph-engineering`** re-based from escalation matrix to the doctrine's graph grammar: nodes closing on evidence, six execution edges (`PRODUCES`, `VERIFIES`, `ROUTES`, `RETURNS`, `FAN_OUT`, `JOINS`), caps, anchor routing, four shapes on a concision ladder, three-graph organization, query routing, cost gate; the v4 five-stage method (audit, identify, design, implement, type) is retained as the loop-to-graph conversion path — now from the v4 loop rather than a legacy build; [topologies](skills/graph-engineering/references/topologies.md) reworked around the canonical review graph.
- **`skills/verification`** re-anchored: executable evidence as the anchor class of last resort; GROW as the governed evolution operator.
- **`skills/teamwork`** re-anchored as the coordination graph: topology ladder, ledger as task graph, spawn briefs as node contracts.
- Flowcharts, `cmd-document`, craft, wayfinder, and README synchronized to the graph ontology.
- `skills/go-modernize` gopls MCP guidance rewritten: the shared `serve -mcp.listen` singleton, port probing, and supervisor/bridge setup replaced by gopls's official headless MCP mode.

### Not adopted

- Benchmark figures from all four sources (claims, not facts — re-derive locally); host-specific tooling and tool names; free-running self-modification (evolution stays governed).

## [4.7.0] - 2026-09-08

### Added

- **`skills/graph-engineering` query routing**: route retrieval by question type, distilled from the same [flowtivity guide](https://flowtivity.ai/blog/graph-engineering-2026-guide-openclaw-codex/) — similarity search answers lookups ("what does X do?"), graph traversal answers multi-hop questions ("why did X change, what is downstream"); graphs lose on simple lookups, high-volume retrieval, and low entity resolution; keep a cheap index for lookups beside the typed edges for the multi-hop path. New pitfall row: traversal where a lookup would do.

## [4.6.0] - 2026-09-08

### Added

- **`skills/graph-engineering`**: graph engineering for agent workflows, distilled from [flowtivity's graph-engineering guide](https://flowtivity.ai/blog/graph-engineering-2026-guide-openclaw-codex/) — whose benchmark figures are claims and are deliberately not adopted (measure locally): the loop-vs-graph decision matrix (simple/complex × low/high concurrency → single, parallel, or staged loop, or an explicit graph, entered only on three or more concurrent verification steps plus branching decision routing), the five-stage method (audit the loops → identify concurrency → design a 3-5-node topology with every edge condition written → implement and measure → type the edges), six typed edges (`SUPERSEDES`, `DEPENDS_ON`, `DECIDED_BY`, `CAUSED`, `IMPLEMENTS`, `REFERENCES` — an untyped edge is a missing decision, and facts expire), the cost gate (judge by cost per successful completion, never wall-clock alone; the guide's claimed ~50% pass-rate breakeven is re-derived, not cited; a graph that loses the gate steps back down to a staged loop), and `references/topologies.md` with the canonical Planner→Worker→parallel Reviewers→Synthesizer→gate topology, edge-condition routing patterns, the cost arithmetic, and temporal-validity rules.

### Changed

- **AGENTS.md §4 "The Loop"** routes jobs that need three or more concurrent verification steps or branching decision routing to shape execution as an explicit graph via `skills/graph-engineering` (batching stays within-turn; teamwork stays the substrate); the Repository Map gains the skill row, and README plus the five discovery manifests count twelve on-demand skills and list `graph-engineering`.

## [4.5.0] - 2026-09-07

### Added

- **`skills/grilling`**: the plan-first interview method, distilled from [mattpocock/skills](https://github.com/mattpocock/skills) (`grilling`, MIT): decisions mapped as a design tree and worked in numbered frontier rounds — every question whose prerequisites are settled, each with a recommended answer — facts dispatched to sub-agents while only decisions reach the user, done when the frontier is empty: one-recommendation plan, then STOP for approval.
- **`skills/domain-modeling`**: the active domain-language discipline, adapted from the same source (MIT): five habits (challenge terms against the glossary, sharpen fuzzy language to canonical ones, stress-test relationships with edge-case scenarios, cross-reference code claims, update `CONTEXT.md` inline), `CONTEXT.md` at the repo root as a glossary and nothing else (opinionated `_Avoid_` entries, lazy creation, `CONTEXT-MAP.md` for multi-context repos), and the ADR trigger triad — offered only when hard to reverse, surprising without context, and a real trade-off; format reference in `references/context-format.md`.

### Changed

- **AGENTS.md §2 "Decide, don't ask"** now states the fact/decision split: facts are the agent's to look up; only decisions reach a human. The plan-first Shape line links `skills/grilling` for the full method; §5 routes design work touching domain terms, the glossary, or a decision record to `skills/domain-modeling`; the Repository Map gains both rows.
- **Glossary unified on `CONTEXT.md`** at the repo root: `cmd-document`'s `--type=glossary` and its bootstrap layout retarget from `docs/glossary.md`, with format owned by `skills/domain-modeling`; README's tree follows. One language, one source of truth.
- **Scoping cross-references**: wayfinder's Grilling tickets route to `skills/grilling` for technique, with "frontier" disambiguated (map tickets across sessions vs open questions within one session); solution-architecture §3 notes domain-modeling owns the conversation-time ADR trigger while format and lifecycle stay canonical there.
- **`skills/confluence`**: three hard-won publish lessons from one day of blank-diagram debugging. (1) The `plantumlcloud` `data` encoding is not standard PlantUML base64 and varies between pages on the same instance — prove an encoder against the `data` param of a page that demonstrably renders in a browser (a sibling's mere existence proves nothing), re-encoding byte-for-byte before trusting it; recipe pinned as percent-encode → raw deflate (level 6) → standard base64 with padding kept. (2) A collapsible raw-source expand must use the native `expand` macro in storage format — Confluence silently strips an HTML `<details>` element from the stored body. (3) Multi-KB write payloads can be silently corrupted in the MCP client→server hop (`InputValidationError … could not be parsed as JSON`, reported bytes ~3× the payload) — a transport defect, not an authoring mistake: switch transport via smaller `confluence_update_page_section` or full-body `confluence_update_page` with `content_file`; and read-backs now rank probes by descending strength, led by `confluence_get_page_diff` (with the caveat that search indexes lag and never index macro parameters).

## [4.4.0] - 2026-09-06

### Added

- **`skills/wayfinder`**: plan an effort too big for one agent session as a shared map of decision tickets on the repo's issue tracker — destination named first, map as index (not store), HITL/AFK ticket types (research, prototype, grilling, task), fog of war graduated into tickets as the frontier advances, out-of-scope recorded where ruled out, claim-before-work for concurrent sessions, at most one ticket resolved per session; the map is done when nothing is left to decide before someone goes and does the thing. AGENTS.md routes plan-first efforts too big or foggy for one session to it and scopes it against teamwork: teamwork parallelizes one job across contexts, wayfinder persists one effort across sessions.

## [4.3.0] - 2026-09-03

### Added

- **`skills/system-diagramming`**: self-contained system diagramming — turn a
  codebase or system description into one interactive HTML artifact (inline
  SVG, dark/light themes, pan/zoom, hover tracing, search) with no installs
  and no network. Author a small typed JSON IR inside the bundled template
  (five kinds: architecture, workflow, sequence, dataflow, lifecycle; the
  renderer draws it deterministically), then gate it with the bundled stdlib
  validator (`E_*`/`W_*` diagnostics) before handoff. Exports, motion, and
  share cards are out of scope.

### Changed

- **`skills/confluence`**: both supported MCP servers are now first-class -
  the official Rovo remote server (OAuth; read/search/Teamwork-Graph surface)
  and mcp-atlassian (open-source; hosted, e.g. mcp-atlassian.soomiles.com, or
  local stdio with an API token; full page CRUD). Adds tool-shape detection
  (server names are arbitrary; camelCase-with-cloudId vs snake_case-pinned-to-
  one-site), a per-operation routing table with write-defaults-to-mcp-atlassian
  when both are connected, mcp-atlassian transport rules (storage-format macros
  first-class, `confluence_update_page_section` as the low-blast-radius path,
  `version_comment` on updates, read-back via `convert_to_markdown: false`),
  and hosted-endpoint setup. Retracts the wrong claim that the local stdio
  fallback shared Rovo's tool surface.

## [4.2.0] - 2026-09-02

### Added

- **`skills/go-modernize`**: Go modernization discipline keyed to the module's
  declared version (`go` directive in go.mod, toolchain fallback): run `go fix`
  (Go ≥ 1.26) or the standalone `modernize` analyzer with `-diff`-then-apply
  review, plus a write-modern-from-the-start idiom table. A reference file
  maps every fixer (evidence: go1.26.7's fixer set vs current
  `modernize@latest` — overlapping but non-identical; `bloop`, `fmtappendf`,
  `appendclipped`, `slicesdelete` documented upstream but not in either yet).
  A second reference encodes the one-shared-`gopls serve -mcp.listen` MCP
  singleton pattern (login-time supervisor + held-open stdin; legacy
  HTTP+SSE transport; per-host wiring by client transport class, stdio-only
  hosts via a bridge) verified end-to-end on this machine. Ports are
  discovered, not fixed: probe for a live instance, else bind a free high
  port (49152–65535) and publish it (`~/.local/state/gopls-mcp.port`) for
  hosts/bridges to resolve at connect time.

- **`skills/solution-architecture`**: solution-architecture discipline distilled
  from the Awesome AI Architect knowledge base (15 topics): frame ASRs as SEI
  quality-attribute scenarios, choose patterns/styles by context and trade-off,
  record significant decisions as ADRs (Y-statement core, MADR template),
  model in C4 zoom levels, size with three-point estimates, and govern with
  federated standards plus automated conformance. Eight references carry the
  depth (requirements, quality attributes, patterns, decisions, modeling,
  delivery contexts, governance, communication); descriptions across the five
  discovery manifests now say seven on-demand skills.

## [4.1.0] - 2026-08-29

### Added

- **Agent-agnostic teamwork doctrine**: `skills/teamwork` plus a new AGENTS.md
  §9. Distilled from current multi-agent team guides across hosts and expressed
  capability-first per the agnosticism charter: the solo-to-delegation-to-team
  escalation ladder with counter-signals, shared task ledger with
  dependency-gated claiming (3-5 workers, 5-6 tasks each), exclusive file
  ownership, self-contained spawn briefs, milestone rotation to fresh contexts,
  adversarial verification roles (reviewer / challenger / auditor) treating
  worker reports as testimony and inter-agent messages as untrusted input, and
  a failure-mode table (anchoring, lead-grabs-work, facade delivery, ledger
  lag, orphaned workers, token blowout). The right-sizing header and §8 now
  name team escalation as the sanctioned response to window strain on
  parallelizable work. Verified end-to-end in a throwaway sandbox run (ledger
  with dependency-gated claiming, four exclusive-ownership workers, lead
  re-verification, mutation probe); that run surfaced and the brief rule now
  encodes: on a conflict inside a brief, the worker flags and stops — spec
  outranks checks, never implement past an unresolved conflict.

## [4.0.0] - 2026-08-29

### Added

- **Execution-efficiency doctrine upgrades**, absorbed from current coding-agent
  engineering guidance: session hygiene (one task per session; fresh session per
  investigation thread); environment-first triage for inconsistent outputs
  (directory/permissions/tool surface/integrations before reasoning); deliberate
  knowledge placement (instruction vs learning memory; procedures -> skills;
  episodes -> retros; facts -> repo docs or retrieval) under memory-scope
  precedence organization > project > personal > machine-local, with role-scoped
  memory for delegated workers; GROW promotes battle-proven procedures into
  scheduled or triggered automation; authoring rules for instruction files
  themselves (verifiable-rule phrasing, topic-modular on-demand loading).

### Changed (BREAKING)

Ground-up restructure: the four-role distribution (governance file + role sheets +
commands + registries + installers) becomes a single concise shared setup for AI
coding assistants, agnostic of programming languages, agent frameworks, and host
tools. Tracked volume drops from ~5,000 lines to under ~800.

- **`AGENTS.md`** rewritten as the v4 manifesto: intake route (trivial / fit / shape),
  decision-point gates with authority rank (user statement > spec > checks > code),
  THINK-ACT-PROVE-GROW loop with backward planning and single-turn batched execution,
  three-layer verification with the hard verify bound, context/state austerity.
- **Three consolidated skills** replace the ten-skill surface:
  `skills/craft` (twelve commandments, canonical artifact-gate definitions),
  `skills/performance` (measure-first cycle; tactics organized by the four runtime-
  overhead sources: allocation churn, lock contention, syscall count, data copying),
  `skills/verification` (right-sizing dial, evidence audit, mutation probe, adversarial
  judging) — plus `references/measurement.md`, `references/tactics.md`, and
  `references/flowcharts.md`.
- **Routine-task commands** restored lean for every-project reuse:
  `cmd-verify` (quality-gate pipeline), `cmd-review` (severity-grouped review),
  `cmd-refactor` (behavior-preserving restructure), `cmd-document` (docs/ tree
  bootstrap/sync). Deliberately not restored: cmd-judge (protocol lives in the
  verification skill) and cmd-openapi (tool-chain-specific, breaks agnosticism).
- **Marketplace compatibility**: plugin/extension discovery manifests ship at
  their canonical paths (`.claude-plugin/`, `.cursor-plugin/`,
  `gemini-extension.json`) as plain versioned files - no generator step and no
  root-symlink indirection - so Agent-Skills-compatible CLIs can add the repo
  directly from GitHub. A fifth gate (`manifests`) parses them and asserts
  cross-file version agreement.
- **`scripts/install.sh`**: detection-driven local installer; discovers
  installed harnesses by config directory, then links (or copies) the manifesto
  under each tool's expected instruction filename plus its skills/commands
  directories where supported. Never clobbers real files; uninstall only
  touches links resolving back to this repository unless `--force`.
  Host-agnostic doctrine stays token-free - concrete hosts are known only to
  this script and the manifests (the distribution layer, excluded from the
  agnostic scan).
- **`scripts/check.py`** replaces `checks.py`: four gates (budget, frontmatter, links,
  agnostic). The GitHub workflow calls it from the same change; consumers invoking
  `checks.py` gate names must migrate.

### Removed

- Squad surface: `agents/*.md`, `commands/*.md`, `references/**`.
- Distribution machinery: `registries/`, `adapters/`, `.claude-plugin/`,
  `.cursor-plugin/`, root plugin/marketplace/gemini-extension discovery files,
  `VERSION` (git tags are now the sole version source).
- Superseded skills: `memory-engineering` (one-line sliver survives in AGENTS.md §8)
  and `spec-driven-development` (spec-sync rule survives in craft's intent gate);
  dropped as out of scope for a language-/host-agnostic core: `commit-message`,
  `repo-documentation`, `go-essential`, `openapi-spec`, `confluence`
  (reinstated below once the Rovo remote MCP server removed its local-machinery
  dependency).
- `eval/` scenario suite (graded deleted surfaces; a replacement suite seeds from the
  first real post-v4 retros instead of stubs).

Removed artifacts remain recoverable from git history.
