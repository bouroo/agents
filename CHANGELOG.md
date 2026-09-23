# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Pre-4.0 entries were retired in the v4 fresh start; detailed entries for 4.0.0
through 6.3.0 were retired in the 6.6.0 compaction. The full history lives in
git tags and log (`v1.0.0` through `v3.11.0`, and `git show
v6.3.0:CHANGELOG.md` for the retired detail).

## [6.6.0-beta.2] - 2026-09-23

The beta.1 role definitions absorb a round of hardening, mostly borrowed
from what the doctrine already knows. The **orchestrator** now draws a
task graph before dispatching: nodes are units, edges exist only where a
unit consumes another unit's result, and fake edges — steps that never
read the prior output — are deleted so independent units actually run in
parallel. A stop rule bounds the shape: sequential pieces become a chain
of units dispatched one at a time, and one sequential piece runs as a
single unit. The written graph is the plan, fan-out is capped at what
can actually be verified, and the orchestrator is the single owner of
the merge. The blanket "never run destructive actions" becomes gate
placement: route irreversible actions through explicit approval where a
mistake is expensive to undo. The **worker** becomes a full loop —
classify the brief before acting, treat the DONE check as the only done
criterion, orient before editing (primary sources beat memory), act
surgically behind an `INTENT:` line, hold the standing prohibitions,
verify by observation with a verbatim `TWINS:` search, and report
outcome-first.

### Changed

- **`agents/common/`, `agents/codex/`** — all orchestrator and worker
  variants (markdown, `.plain.md`, Codex TOML) rewritten to the shapes
  above; the worker now carries the doctrine's ACT/PROVE discipline
  (INTENT gate, TWINS search, three-cycle bound, outcome-first report)
  instead of a bare "run the DONE check and report".

### Fixed

- **`scripts/install.sh`** — a legacy dir-level symlink into the repo at
  the declared agents subdir is migrated to per-file placement on
  install; a foreign symlink is skipped with a warning instead of being
  deleted. Stale links at the sibling `agent`/`agents` spelling are
  removed on install and uninstall, and status reports `agents=legacy`
  while one is present.

## [6.6.0-beta.1] - 2026-09-23

The orchestrator-worker shape stops being prose and becomes installable
machinery. Teamwork described the lead's dispatch-and-verify loop, but nothing
a host could load enacted it — every host rolled its own lead/worker prompts.
`agents/` now ships the two definitions: an **orchestrator** that decomposes
into units with explicit file ownership and executable DONE checks, dispatches
each to a worker, re-verifies every returned unit itself (a worker's report is
testimony, not proof), and stops after three failed cycles on one unit; and a
**worker** that executes exactly one unit and returns files changed plus
exit-code evidence. `scripts/install.sh` grows a fourth surface column that
distributes them per host: common markdown for most, a `.plain` variant (no
`name:` frontmatter — the host derives the agent id from the filename) for
OpenCode and Kilo, copied TOML for Codex, and no agents surface for OpenClaw,
Hermes, and MiniMax. A host-specific file under `agents/<code>/` wins over the
common one by installed basename.

The confluence skill absorbs one day's write-side failures and one discipline.
Three guards, each paid for 2026-09-23: never copy a collapsed macro's rendered
signature line back as markdown (three sample blocks corrupted that way —
re-fence every sample instead); section updates are boundary-blind past the
headings the matcher recognizes, so on unfamiliar pages always diff (n-1)→n
after a section write and restore from the removed lines when the replacement
swallowed to EOF; and MCP writes go out sequentially, one call per message —
parallel write calls fused into a single garbled ~100 KB payload once, and
size was never the trigger, batching was. The discipline: a page *update* must
make the delta visible in the page itself — fetch a pre-change baseline
version, mark every changed row with a `C#` ref and bold field name, record
removals as `Removed` rows in one per-page Change Log table, and prove after
publish that every `C#` resolves bidirectionally.

### Added

- **`agents/common/`, `agents/codex/`** — the orchestrator and worker agent
  files in three encodings: common markdown, `.plain.md` for hosts that reject
  a `name:` key, and Codex TOML (`developer_instructions`, plus a note on
  raising `agents.max_depth` when spawning fails).
- **The `agents` surface in `scripts/install.sh`** — a sixth host-table column
  (`<subdir>[:<fmt>...][:copy]`, `-` for none) that installs per-file agent
  definitions with the format rules above; the file-level precedence and the
  `md` vs `md-plain` consumption rule are documented in the script's `--help`.
- **`skills/confluence/references/page-template.md` — the `[changelog]`
  section**: the baseline-diff workflow, storage-form snippets for the
  Change column and the Change Log table, the change-type and numbering rules,
  and the bidirectional `C#` integrity gate with its three documented
  relaxations, added as item 7 of the publish proof.

### Changed

- **`skills/teamwork`** — a new "The lead's dispatch loop" section: one unit
  per worker with a self-contained brief, re-run the failing worker rather
  than re-dispatching (re-dispatch only on mis-specification), stop after
  three failed cycles, and synthesize the final report outcome-first.
- **`skills/confluence` write guards** — collapsed-macro copyback,
  boundary-blind section edits, and sequential (never parallel) MCP writes
  join the rules-paid-for-by-breakage list; the payload-corruption rule now
  names batching, not size, as the trigger.

## [6.5.1-beta.1] - 2026-09-23

### Changed

- **`AGENTS.md`, `skills/craft/SKILL.md`** — the `PROMPT:` intake gate states explicitly that an ask in any language is first rewritten as one concise, clear English paragraph before work begins; the confirm-the-reading stop is unchanged.

## [6.5.0] - 2026-09-20

Eighteenth skill: `design-pattern-selection`.

### Added

- **`skills/design-pattern-selection/`** decision-first GoF selection: restate the pain as a variation sentence, apply the no-pattern gate first (a plain solution under ~50 lines is the common, valid verdict), shortlist at most 2 candidates against the pain→pattern table, run language reality checks (function values, stdlib, duck typing collapse several classics), deliver verdict + why + minimal skeleton + revisit signal. Condensed 22-pattern catalog in `references/patterns.md` (intent / use when / skip when / shape).
- **`README.md`** skill count bumped to eighteen; tree lists the new skill.
- **`.claude-plugin/`, `.cursor-plugin/`, `.minimax-plugin/`, `gemini-extension.json`** manifests carry the new skill and the eighteen-skill description.

## [6.4.1] - 2026-09-20

The MiniMax host row was wrong about its own host. 6.4.0 modeled MiniMax Code
as having no user-level instruction file and installed skills only; the host
does take a global `AGENTS.md`, so the row now installs the manifesto to
`~/.minimax/AGENTS.md` like any other AGENTS.md host.

### Changed

- **`scripts/install.sh`** — the minimax row carries `AGENTS.md` again. The
  empty-instruction mechanism stays for any host that genuinely has no global
  rules path; no current host uses it.
- **`README.md`** — the "hosts without a global instruction file" bullet is
  gone, since nothing consumes the capability it described.

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

## Retired detail (4.0.0 – 6.3.0)

Detailed notes for these releases were retired in the 6.6.0 compaction; the
full text lives in git history (`git show v6.3.0:CHANGELOG.md`, or
`git log -p v4.0.0..v6.3.0 -- CHANGELOG.md`). One line each, newest first:

- [6.3.0] - 2026-09-18 — comment rule sharpened into `craft`'s Comments section, a `comments` gate, and an eval case.
- [6.2.0] - 2026-09-15 — the `PROMPT:` intake gate: corrected reading surfaced and confirmed before work.
- [6.1.0] - 2026-09-14 — harness hygiene: verification grip ladder, instruction-file hygiene, unattended evals, the over-reporting reviewer.
- [6.0.0-beta.2] - 2026-09-12 — context-reduction pass over the manifesto and workflow docs; no behavior change.
- [6.0.0-beta.1] - 2026-09-12 — v6 lifecycle foundation: the `lifecycle` and `evals` skills, release automation.
- [5.7.0] - 2026-09-12 — the harness-design reference for the execution-graph grammar.
- [5.6.0] - 2026-09-11 — completion-non-authorization generalized to all outward and destructive commands.
- [5.5.0] - 2026-09-11 — `git push` named as the canonical AUTH case.
- [5.4.0] - 2026-09-11 — the confluence read-collapse playbook; deterministic-failure and unread-overwrite hard constraints.
- [5.3.0] - 2026-09-10 — the STATUS.md execution ledger split out of PLAN.md.
- [5.2.0] - 2026-09-10 — `skills/indexed-search`: the trigram-indexed search lifecycle.
- [5.1.0] - 2026-09-10 — `skills/plan-authoring`: the deterministic plan pattern.
- [5.0.1] - 2026-09-09 — the confluence storage-form template anchor; gated-encoder publish rules.
- [5.0.0] - 2026-09-09 — v5 execution-graph re-authoring: anchors, knowledge edges, `graph-engineering` re-base.
- [4.7.0] - 2026-09-08 — graph-engineering query routing: similarity search for lookups, traversal for multi-hop.
- [4.6.0] - 2026-09-08 — `skills/graph-engineering` added: loop-vs-graph decision, typed edges, cost gate, topologies.
- [4.5.0] - 2026-09-07 — `skills/grilling` and `skills/domain-modeling`; `CONTEXT.md` unified at the root.
- [4.4.0] - 2026-09-06 — `skills/wayfinder`: the map of decision tickets.
- [4.3.0] - 2026-09-03 — `skills/system-diagramming`; confluence's dual-server support.
- [4.2.0] - 2026-09-02 — `skills/go-modernize` and `skills/solution-architecture`.
- [4.1.0] - 2026-08-29 — agent-agnostic teamwork doctrine (§9).
- [4.0.0] - 2026-08-29 — the v4 ground-up restructure: single manifesto, three consolidated skills, discovery manifests, installer, check gates.
