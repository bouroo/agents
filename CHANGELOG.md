# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Pre-4.0 entries were retired in the v4 fresh start; detailed entries for 4.0.0
through 6.8.0-beta.1 are retired below, one line each. The full history lives in
git tags and log (`v1.0.0` through `v3.11.0`, and `git show
v6.8.0:CHANGELOG.md` for the retired detail).

## [8.0.0-beta.1] - 2026-11-05

The spine is rewritten on the AI-native SDLC: a six-stage loop — **Plan,
Design, Build, Test, Deploy, Maintain** — replacing the previous seven
stages (Intent, Spec, Plan, Build, Test, Release, Operate). The stage
sequence now mirrors the one teams actually run when agents write the code:
intent is captured as `intent.md` in the Plan stage, requirements and design
compress into one session in the Design stage, the plan and the diff are the
Build stage's output, review and governance land in Deploy, and the loop
closes in Maintain when a breached control band is written back as a new
`intent.md`.

Four rules were added because the loop needs them to work, and each one is
now asserted by a gate:

- **The accepted artifact fires the next gate.** A committed `intent.md`
  triggers the design pass, an approved `spec.md` triggers planning, and a
  merged change triggers the pipeline. The handoff is the commit, so a
  person holds the gate rather than the handoff.
- **One source of truth per artifact.** Where a legacy system already holds
  the record — a tracker, a requirements tool, a wiki — name it the source of
  truth and keep the committed artifact as a linked working copy. Two copies
  with no link are two truths.
- **Advisory controls make violations rare; deterministic controls make them
  close to impossible.** A skill shapes the work while it is written; a
  policy that must always hold needs a hook or a check behind it.
- **Autonomy stops at the gate.** The agent acts up to the production gate
  and nothing past it, tiered per environment, so the human gate sits above
  the automation rather than inside it.

The `delivery` skill grows a **Plays** section and a
`references/plays.md` that carries the per-stage practices: capture as
`intent.md`, requirements and design in one session, plan-then-implement, the
project context file, skills as institutional knowledge, hooks as build-time
guardrails, parallel sessions and subagents, the feedback loop, continuous
evals, agentic review in both directions, hooks as approval gates, CI/CD
integration with tiered autonomy, closing the loop from a control-band
breach, and recurring codebase scans. Each play names what it changes, how
to start, the steps, the governance, and a leading and a lagging indicator.

Autonomy is also tiered by **guardrail maturity**, not only by environment: a
session may run unattended once the context file, the skills encoding
policy, the hooks blocking unsafe actions, and a runnable test suite have
earned it — a tight spec, a small blast radius, and code the tests already
cover. The ladder is earned rather than assumed, so a session that shows it
is not ready gets the per-edit prompt back.

Two gates join the set: `stages` holds the six-stage spine and each stage's
artifact on both installed surfaces, and `playbook` holds the four rules
above wherever they are stated. The gate count is twenty-seven, and the
eval suite grows three evals over the new material (95 checks, all green).

The always-on token budget moves from 8000 to 9000 (the manifesto from 6500
to 7500, the standalone copy from 5000 to 5500). The rewrite added four
always-loaded rules, so the footprint grew by design, and the old ceiling
left 16 tokens of headroom — a ceiling that sits at 99% of the footprint
turns the next legitimate rule into a red gate, which is how a budget stops
bounding cost and starts blocking the work.

## [7.9.0-beta.5] - 2026-11-05

A tenth on-demand skill: `unslop`, which removes AI residue from the
artifacts a SWE task delivers. Two upstream skills feed it — the
`unslop` prose rules from [cursor/plugins](https://github.com/cursor/plugins)
(MIT) and the interface passes from
[heydamir/unslop](https://github.com/heydamir/unslop) (CC BY 4.0) — and the
gap between them is closed for back-end work: prose rules cover commit
messages, PR descriptions, docs, error strings and log lines; code rules
cover placeholder bodies, swallowed errors, over-generated abstractions,
vague names and claims without a referent; interface rules cover spacing,
colour, icons, copy, type, layout, details, visuals and motion.

The skill's discriminator is one test: swap this project for a different
one, and any line that still reads as true carries no information about
this project, so it is residue. A second rule keeps it honest: a prose
claim that exceeds the implementation is *missing work*, which goes to the
build queue, never to the rewrite queue. Rewriting a sentence to agree with
a defect is the one move the skill forbids.

Rule ids are stable (`P3`, `C11`, `U2`), so a report cites them and a later
pass compares against them. `scripts/scan.py` flags the machine-detectable
residue in a path and carries a self-test; the scanner finds candidates,
not verdicts. Bundled references load one surface at a time: prose, code,
interface.

A forward-test on a slop artifact found five contradictions in the first
draft, all now closed: a string inside a source file belongs to the code
surface, so the docstring rule lost its duplicate id; "do not add" is
reconciled with the fix for a swallowed error, which is a repair the claim
already promised; the sample-data rule now names its three outcomes
(read the real source, replace with plausible data, or report missing work)
instead of leaving no middle path; the vague-name rule no longer fires on a
job-named class that the naming rule asks for; and the report format is
stated, with `PENDING:` carrying what was not rewritten. The scanner gained
the missing hype vocabulary, stopped double-reporting a swallowed `pass` as
a placeholder body, and takes several paths at once.

Applying the skill to this repository found residue the scanner could not see,
and two claims that no longer matched the code. The `quality` skill stated the
trigger set as "8-10 should-trigger and 6-8 should-not-trigger" per skill, but
the gate enforces a minimum and two skills carry more; the claim now states the
minimum and says why a broad scope carries more. The CI workflow headed its
gate list "the authoritative list" while listing 11 of 25 gates; it now lists
all 25 and names `scripts/check.py` as the registry. Three magic timeouts became
named constants with their reason, the three near-identical doctrine scan
loops in `check.py` became one helper, and the scanner learned that a
`-> str | None` return is a declared sentinel and that a comment block's
continuation line is not narration. The rule list now states the scanner's
remaining blind spots, so a manual pass still owes them attention.

## [7.9.0-beta.4] - 2026-11-03

Users consuming this repository as their agent configuration reported that
time per task grew with the setup itself. The setup is the configuration: the
doctrine's per-task cost *is* the product's cost, so the fix is to make that
cost proportional to the job instead of fixed.

- **The compact path is the default.** The seven-stage delivery lifecycle
  demanded an `intent.md` / `spec.md` / `PLAN.md` chain, a state checkpoint,
  and a separate verification report from every task, including a one-line
  fix. `AGENTS.md` section 4 and the `delivery` skill now state a **compact
  path**: a small, local, reversible change runs one THINK, one ACT, one
  PROVE, held in the conversation, with no artifact chain and no checkpoint.
  The full path is owed when the work is large, irreversible, outward-facing,
  cross-session, or multi-agent, and taking the compact path *is* the recorded
  reason for the stages it skips.
- **The confirmation stop is proportional.** The `PROMPT:` gate stopped the
  run for confirmation before the first edit, which spent a round trip on
  every task including unambiguous ones. It now stops only when the
  corrected reading could change the work materially — a genuine ambiguity, a
  competing reasonable interpretation, or an irreversible or outward action;
  a small, local, reversible, unambiguous reading proceeds and names the
  reading it acted on. The gate itself is unchanged: the ask is still pinned
  before the first edit.
- **The verification loop is sized, not skipped.** The Generate-Verify-Refine-Deliver
  loop stays owed on non-trivial work, and the mutation probe stays owed on
  high-risk work; a small, local, reversible change is verified in place
  (re-read the diff against the pinned ask, run the check, name the evidence)
  and the report says so in one line. The loop is skipped only by being sized
  down, never by being forgotten.
- **The per-turn checkpoint is no longer per-turn.** `ACT` checkpoints state
  under `.agents/` when the work spans turns or sessions, not on every turn
  of a compact change.
- **The always-on footprint is now measured.** A new `cost` gate holds the
  context every task pays before any work starts — the manifesto plus the
  skill descriptions the host loads to decide what applies — within a token
  budget, so the setup's per-task cost cannot grow silently. The standalone
  copy carries its own ceiling, since a host that installs it alone loads
  neither the manifesto nor the skills. Measured: ~7,300 tokens for the
  skills install, ~4,300 for the standalone one.
- **Gated.** A new `sizing` gate pins all three sizing rules (the compact
  path, the proportional confirmation stop, the sized verification loop) on
  every surface that carries them — both doctrines, the delivery skill, and
  the quality skill (suite now 25 gates), and two evals check that the
  sizing rule and the always-on budget survive a doctrine edit (suite now
  33 evals, 82 checks).

## [7.9.0-beta.3] - 2026-11-01

Skill-authoring conformance with the Agent-Skills best-practices guidance: the
gates now hold the shape the guidance describes, and the places where the
repository only appeared to follow it are fixed.

- **Bundled references must state their load condition.** The `references` gate
  already required every `references/` file to be named from its `SKILL.md`;
  naming alone defers nothing, because an unconditioned "details:
  references/x.md" is context the run either pays for every turn or never
  finds. The gate now requires the link's paragraph to carry the condition that
  sends the reader there, and 46 links across eight skills were rewritten to
  say *when* (plus one already-correct link preserved). `AGENTS.md` section 8
  and the `quality` skill's Evals section state the rule.
- **Frontmatter accepts the whole spec.** The gate whitelisted only `name` and
  `description`, so a spec-legal `compatibility`, `license`, or `metadata` key
  would fail it; all six spec keys are now accepted, `compatibility` is
  length-checked at 500, and the parser ignores indented map entries under
  `metadata:` instead of reading them as top-level fields.
- **Skills no longer repeat their description in the body.** `architecture`,
  `modernize-coding`, and `problem-details` each carried a `**When to load:**`
  paragraph restating the frontmatter the host already loaded; each is replaced
  by a one-line scope boundary against the neighbouring skill.
- **The installer stops publishing machine-local skills.** It linked the whole
  `skills/` directory into every host, which carried the untracked
  `skills/.system/` tree (a coding CLI's own runtime skills) into nine hosts'
  skill directories. Placement is now per shipped skill, dot-directories are
  skipped, a legacy whole-directory link is migrated, `uninstall` removes the
  per-skill links and only then the emptied directory, and `status` reports
  `skills=ok (9/9)` instead of a single link.
- **The `confluence` skill no longer hardcodes a third-party MCP host** as the
  default endpoint; it names the upstream project and takes the deployment's
  own URL.
- **A negated trigger no longer passes the `descriptions` gate.** "Do not use
  when X" matched the trigger regex while saying the opposite, so a description
  with no positive half read as valid; the gate now detects the negating words
  immediately before the clause.
- **New eval** `bundled-reference-states-its-load-condition` (suite: 31 evals,
  23 gates), and the four gates missing from `check.py`'s own docstring and the
  README table are documented.

## [7.9.0-beta.2] - 2026-10-29

Runtime state management, from the graph-engineering survey (arXiv:2608.21156):
tasks and agents were structured, but what a run *recorded*, how a fault was
*localized*, and where recovery *resumed* were left to memory and prose.

- **State is recorded, not remembered.** `AGENTS.md` section 8 and the
  standalone copy state that the state record carries evidence pointers and a
  version, is proposed-validated-committed rather than asserted (a worker's
  report stays a proposal until its check is re-run), is written by one owner
  per file, and keeps append-only history with derived summaries so provenance
  survives. The new `skills/execution/references/runtime-state.md`, named from
  the skill's `## Runtime state` section, owns the record fields and the
  visibility rule.
- **Fault localization is evidence, not adjacency.** A recorded dependency
  narrows the search and never proves a cause; the visible fault sits
  downstream of where it started, so the cause is stated as a hypothesis and
  tested outside the failing path, against the actor, transition, dependency,
  and validation evidence each step left behind.
- **Recovery names its boundary first.** Internal state replays; outward
  effects — pushed, posted, deployed, deleted — compensate or wait for `AUTH:`,
  and the boundary, corrective action, and resulting state are recorded.
  Adaptation inside a run is not evolution: only a validated, versioned change
  to the machinery is, and it is checked for generalization to the recorded
  failures.
- **Gated.** A new `state` gate pins the rule on both doctrines and the
  execution skill (suite now 23 gates), the execution description's trigger
  set gains three runtime-state prompts, and a new eval checks that the rule
  and its reference survive a doctrine edit.

Source: Feng et al., "Graph Engineering in the Era of LLM Agents: From
Individual Intelligence to System Intelligence", arXiv:2608.21156v2, sections
4.4 (runtime state), 4.5 (evolution), and 5.1 (evaluation confounds).


## [7.9.0-beta.1] - 2026-10-27

The shared setup adopts the general coding-agent practice for managing
prompts, plans, skills, and workflows, closing the three gaps it left open:
the execution environment, the automation layer, and session hygiene.

- **The execution environment is a design decision.** `AGENTS.md` section 8
  and the standalone copy now state that a run's capability — the root it
  resolves paths against, what it may read and write, the build/test/lint
  commands it can execute, the external systems it is connected to — is
  decided before the model acts. A run that cannot locate the project, reach
  a file, or run the check reports the environment's limits, not its own.
  The `execution` skill's harness-design reference carries the four
  categories and the diagnosis order.
- **Automation is the layer above a skill.** A skill says how a workflow
  runs; an automation says when it runs and how it keeps running. The new
  `skills/execution/references/automation.md` states the unattended contract
  (pre-declared scope, the check that gates the stop, the authority held by
  a human) and ships a reusable template plus the failure modes. Both
  doctrines carry the clause; an automated run ends local and emits
  `PENDING:` rather than acting outward on its own.
- **A session is a working context, not a transcript to keep growing.**
  One task per session, a new session for a new line of investigation, and
  a long session summarized rather than carried — stated in both doctrines.
- **The harness regression suite runs.** `evals/run_suite.py` executes every
  eval's objective checks and reports the pass rate, exiting non-zero when
  a check misses its expected exit code. The `evals` gate now requires the
  runner and a green suite, so a suite nobody runs cannot pass the gates.
- **Three gates added.** `environment`, `automation`, and `branch` hold the
  new clauses on every surface that carries them (manifesto, standalone copy,
  execution skill, role agents), so no surface can silently lose one.
- **Four evals added.** `environment-clause-survives-doctrine-edits`,
  `automation-layer-survives-doctrine-edits`,
  `work-lands-on-a-task-branch`, and `suite-runner-executes-the-evals` keep
  the above from drifting.
- **Work lands on a branch, never the trunk.** Users reported agents editing
  on the default branch, leaving nothing to review and no merge request to
  open. The hard constraints now forbid editing or committing on the branch
  `origin/HEAD` points at (or the trunk the repository names): a task branch
  is created first, unit worktrees are cut from it, and worktree branches
  merge back into it. The `lead` and `worker` role agents say the same, so a
  worker on the trunk stops and reports instead of editing. The `branch` gate
  and the `work-lands-on-a-task-branch` eval hold the rule on all five
  surfaces.

Gates: `python3 scripts/check.py --all` 22/22 PASS; `python3 evals/run_suite.py` 74/74 = 1.00.

## [7.8.1] - 2026-10-25

The changelog carries the current line in full and the closed lines as one line each, so it says what changed recently without burying it.

- **The 6.x line retires.** The 17 versions from `6.4.0-beta.1` to `6.8.0` move
  into the retired list, one line each; the full text stays reachable in git
  history (`git show v6.8.0:CHANGELOG.md`). The 7.x line keeps its detail,
  because each release there documents a load-bearing doctrine change.
- **The header states the boundary.** It names the new retirement range and
  the tag that still carries the retired detail, instead of pointing at the
  6.6.0 compaction that stopped at 6.3.0.
- **No release section lost.** `scripts/release_notes.py --tag v7.8.0` still
  extracts the stable release body verbatim from its kept section.

Gates: check.py --all 19/19 PASS.

## [7.8.0] - 2026-10-25

Skills ship stable: a skill is addressed by the name the runtime already
knows, so an agent never has to resolve a path it cannot see.

- **Skills are called by name.** Every skill reference in `AGENTS.md`, in the
  four command workflows, and in the skill bodies now names the skill ("the
  `quality` skill's Craft section") instead of linking `SKILL.md`. Some
  harnesses cannot resolve a skill's file path — the doctrine may be
  installed outside the repository, or the agent's working directory
  differs — while every harness that loads a skill knows its name, so a name
  is the only reference that always resolves.
- **A section is named, not linked.** The topic that used to be the link text
  (craft, verification, grilling, wayfinder, domain modeling) is now the
  skill's section: "the `delivery` skill's Grilling section". The Repository
  Map in `AGENTS.md` section 11 lists the nine skills by name, with their
  bundled references, and without directory paths.
- **The sibling construct is gone.** The 14 cross-skill path links inside the
  skill bodies and the 3 inside two bundled reference files are converted too,
  so no runtime-loaded file points at a skill by path.
- **Nothing else moved.** No rule, gate, description, or trigger set changed;
  `python3 scripts/check.py --all` stays green at 19/19.

## [7.7.0-beta.1] - 2026-10-24

Sessions are the default unit of forgetting, so the doctrine now says where
knowledge goes and what a connected system is allowed to mean.

- **Memory is a design decision, not a hope.** `skills/execution/SKILL.md` gains
  a `Memory` section and `skills/execution/references/memory.md` the detail:
  five layers (session, project, user, machine-local, role) under an
  organization ceiling, instruction memory (policy, written by a human) kept in
  a separate file from learning memory (corrections, written by the agent) so
  accumulated experience cannot quietly rewrite policy, and rules authored as
  checks rather than virtues, one topic per file, loaded by path, promoted on
  their second occurrence, and pruned like code. A troubleshooting ladder
  follows the failure from stale rule to wrong scope to a surface that never
  loaded.
- **External systems extend the context boundary.**
  `skills/execution/references/harness-design.md` adds the rule that issue
  trackers, CI results, schemas, and API docs arrive through a connected
  protocol (MCP being the common one), that connected retrieval beats a pasted
  excerpt, and that every connection carries authority and exposure at once:
  results are claims, not consent.
- **The always-loaded clause sharpened.** `AGENTS.md` section 8 states a fresh
  window as the default and disk as the only thing that reloads, ranks
  environment context above reasoning when identical input disagrees, and spells
  out where each kind of knowledge lives, in what precedence, scoped how, and
  pruned when. `standalone/AGENTS.md` carries the same clause so the two
  installed surfaces cannot drift.
- **New `memory` gate.** Both canonical surfaces must keep stating the rule;
  gates 18 -> 19.
- **Two new evals, two new trigger queries.** The suite (23 -> 25) covers the
  memory rule surviving a doctrine edit and the reference staying loadable; the
  execution trigger set gains a forgotten-rules query and a
  read-my-tracker-directly query (144 -> 146).

## [7.6.0-beta.1] - 2026-10-23

Skills, commands, and evals follow the Agentskills authoring guidance: a
description now carries the whole triggering decision, and it is measured
instead of argued.

- **Descriptions rewritten for triggering.** Every skill and command
  description now leads with an imperative trigger clause naming the user
  intents and phrasings that activate it (including asks that never name the
  domain) and closes with a boundary naming the near-miss another skill owns.
  The old descriptions led with internal mechanics ("the twelve commandments
  and artifact gates..."), which reads as documentation and both
  under-triggers and over-triggers.
- **Trigger evals.** `evals/trigger.json` adds a labelled prompt set — 144
  queries across 9 skills, 8-10 positives and 6-8 near-miss negatives each,
  split train/validation so a description tuned on train is scored on held-out
  queries. `evals/run_triggers.py` runs each query N times against a host
  command, matches a load marker, and reports trigger rate per split.
- **Four new gates.** `descriptions` (trigger clause + boundary present),
  `skillbudget` (skill body within 500 lines / 5000 tokens, command within 120
  lines, covering every skill so a new one cannot enter ungated), `references`
  (every bundled reference named from its SKILL.md), and `triggers` (the query
  set is well-formed and large enough to measure). Gates: 13 -> 18.
- **Eval suite deduplicated.** Eight near-identical
  `<skill>-structure-holds-under-edit` evals and eight
  `<skill>-progressive-disclosure` evals collapsed into two gate-backed evals
  covering every skill; 34 evals -> 21, with no coverage lost and new skills
  now covered on arrival. Two evals were added for the agent and standalone
  surfaces: 23 total.
- **The always-loaded surfaces follow the same rule.** Role agents
  (`agents/common/*`, `agents/codex/*`) are selected by description exactly as
  skills are, so their descriptions gained a trigger clause and a boundary, and
  the `descriptions` gate now reads TOML metadata too. `standalone/` and
  `agents/` joined the privacy and dash scans, and the new `standalone` gate
  asserts that every hard constraint in `AGENTS.md` is present in the compact
  copy (a rule had already gone missing there: the exported-symbol doc-comment
  rule). The repo map now names `agents/`, `standalone/`, and `evals/`.

Gates: check.py --all 18/18 PASS.

## [7.5.1-beta.1] - 2026-10-21

Fixes the stuck subagent loop users hit when the lead agent config is
installed. The lead prompt looped "until every unit passes its check"
with only a per-unit three-cycle cap, leaving three unbounded paths:
a failed subagent spawn was retried with identical arguments forever,
re-splitting a failed unit reset its cycle count, and the teamwork
skill licensed workers to spawn their own result-back workers —
nesting that deadlocks outright on hosts where a subagent cannot
spawn (omp subagent kernels, Codex depth 1). All three are now closed
in every shipped variant (md, plain-md, codex toml): a spawn error is
terminal for that route (vary the agent type once or stop), the job
carries a dispatch budget of twice the initial graph's units plus one
re-split per failed unit with failure history carried over, workers
are forbidden from spawning subagents, and a lead with no dispatch
surface at all stops and reports the host remedy — raise the nesting
or depth limit — instead of stalling.
Gates: check.py --all 13/13 PASS.

## [7.5.0] - 2026-10-19

Three features ship stable, consolidating the 7.5 pre-releases. First,
typed test doubles close the gap between production type discipline and
test code: tests and doubles obey the same type discipline as the code
under test — mocks, fakes, and stubs are typed against the real
interface, never loosened to `any` or an untyped map because "it's only
a test", an any-typed double making the test compile against a lie. The
rule is stated once on the language-agnostic surface (the quality
skill's second commandment) and idiom-specific on all five adapters:
typed `MagicMock(spec=...)`/`create_autospec` with `Protocol` or
`TypedDict` fixtures for Python, hand-written fakes implementing the
real interface and no `any`-parameter stubs for Go, records over
`Map<String, Object>` with typed captors and strict stubs for Java, no
`Box<dyn Any>` or `serde_json::Value` fixtures with trait-checked fakes
for Rust, and `satisfies`, `Partial<T>`, typed `vi.fn<Sut['save']>()`,
and a documented `as unknown as` last resort for TypeScript. Prefer
small in-memory fakes over deep stubs everywhere: interface changes
then break the fake at compile time instead of the test passing anyway.

Second, an agentic verification loop closes the gap between generating a
deliverable and delivering it. The workflow moves from
Generate-and-Deliver to **Generate-Verify-Refine-Deliver**: what the
model first produces for a non-trivial ask is a draft, never the
deliverable. An adversarial **Verifier** persona re-derives the user's
pinned `PROMPT:` constraints and checks the artifact against them
point-by-point, each explicit constraint earning its own Pass/Fail/Partial
verdict rather than a global impression; defect fixes return to
generation under the existing 3-failed-cycle bound and are re-verified
before the next pass, and the **Verification Report** (Requirement Check /
Logic Audit / Final Verdict) is emitted before the deliverable, never
after it. A trivial ask skips the loop exactly as it skips the `PROMPT:`
gate. The rule is stated on both canonical surfaces (AGENTS.md §7 and the
quality skill's `## Verification Loop`), and a deterministic
check.py gate (`veriloop`) pins it on both so neither surface can
silently lose it, bringing the suite to 13 gates.

Third, a ninth on-demand skill: `problem-details`, a plug-and-play RFC
9457 (Problem Details for HTTP APIs, superseding RFC 7807)
error-response guide, for targets with no existing error pattern and
for enforcing one on demand. The skill pins the shared contract — the
`application/problem+json` media type and the five standard members
(`type`, `title`, `status`, `detail`, `instance`) with their exact
semantics — and states the load-bearing rule plainly: `title` is fixed
per problem class, so per-request variability lives in `detail`,
`instance`, or an extension member, never in `title`. Two adoption
paths ship: greenfield (one handler, map errors to type/title/status,
verify with a DONE check) and retrofit (inventory shapes, define the
type URI scheme, wrap legacy payloads as an `errors` extension, enforce
with a schema-validating contract test). `references/blueprints.md`
carries a draft 2020-12 JSON Schema, idiomatic Express, FastAPI, and
Spring Boot (6+ native `ProblemDetail`) implementations, and the
contract test. The skill also covers a hybrid topology for clients that
already speak JSend: user-facing JSend over an internal 9457 record,
with the edge serializer generated rather than hand-built per handler.
Gates: check.py --all 13/13 PASS.

## [7.4.0] - 2026-10-09

Lint evidence becomes owed rather than remembered. Incident: users
reported agents claiming "done" while the generated code failed lint,
forcing manual fixes. Root cause: L1 lint was verification prose, the
role briefs said "build, lint, or tests" — an "or" that let lint be
skipped — and no owed report line carried it. Fix, per the grip ladder
(a rule that keeps being forgotten climbs a rung): the done report on
every source change now owes an `L1:` line — the project's own
lint/format/type-check commands, discovered from its manifests and
scripts (package scripts, Makefile, pyproject/tox, pre-commit, CI),
never assumed absent — each with literal command and exit code; still
red is not done. The gate is stated on all three doctrine surfaces
(manifesto, quality skill, standalone), the lead and worker briefs
demand lint always and report it as their `L1:` line, cmd-verify
discovers the project's own linters before claiming absence, and a new
deterministic check.py gate (`l1`) pins the rule on both canonical
surfaces so neither can silently lose it, with a permanent incident
eval (done-report-owes-l1-evidence). Gates: check.py --all 12/12 PASS;
a mutation probe stripping the rule fails the `l1` gate.

## [7.3.0] - 2026-10-08

The four command workflows now complete a uniform no-options autonomy
contract: invoked without options, each resolves every decision from the
repo's own signals, states its inferences in one line, and stops only at
its named bound. cmd-verify notes absent tooling and states its inference
rather than asking; cmd-review states the diff bounds it took; cmd-refactor
gains the fixed machine-scannable report shape (target, baseline, commits,
before/after, verdict) that cmd-verify and cmd-document already carry.
cmd-document already met the contract and is unchanged. Gates: check.py
--all 11/11 PASS.

## [7.2.0] - 2026-10-08

Stable cut of the 7.2.0 line, unchanged in content since v7.2.0-beta.1:
the doctrine now both teaches and obeys KISS, DRY, SOLID, and YAGNI. Craft
gains Reuse (DRY) and Structure (SOLID) as checkable rules; review and
refactor carry structure-and-reuse checks; the lead and worker role agents
carry the four-principle quality bar into every dispatch brief; standalone
carries the same tags as the root doctrine. The corpus itself was
de-duplicated and de-bloated: dead code out of check.py, duplicate
reference lists out of skills, off-mission presales content out of
architecture, confluence restructured, standalone realigned to root.
Gates: check.py --all 11/11 PASS; the eval suite's 70 mechanical checks
pass.

## [7.2.0-beta.1] - 2026-10-07

A principle-alignment release: the doctrine now both teaches and obeys
KISS, DRY, SOLID, and YAGNI. The manifesto's core principles carry their
classic names, its Hard Constraints section is one clause per line, and
every executing surface operationalizes the four.

The craft skill gains `## Reuse (DRY)` — one canonical owner per piece of
knowledge, extraction on the second real caller, copy-paste-with-edits as
the strongest duplication smell — and `## Structure (SOLID)` — one reason
to change per module, dependencies pointing inward, interfaces narrowed to
their callers, substitutes keeping the base contract. cmd-review adds a
Structure & reuse rubric row; cmd-refactor names the principle-driven moves
(consolidate, split along reasons to change, delete dead weight); the lead
and worker role agents carry the quality bar into every dispatch brief
across all three variants, kept in sync; standalone/AGENTS.md carries the
same tags as the root doctrine.

The corpus itself was brought under the same principles: check.py drops a
34-line dead duplicate of its Go claims table (SYMBOL_CLAIMS), a dead
allowlist constant, and a drifted docstring gate list; skills lose their
duplicated `## References` sections and reference-paraphrasing; the
architecture skill sheds its off-mission presales content
(delivery-contexts.md deleted) and its in-doctrine changelog line; the
confluence skill's 1,000-plus-character bullets move to a new
writing-failure-modes reference with em-dash typography throughout; the
commands lose their restatements of skill-owned detail; standalone is
realigned to the root doctrine (testimony-not-evidence, the wayfinder
escape route, and L1/L2/L3 parity restored). Gates: check.py --all 11/11
PASS; the eval suite's 70 mechanical checks pass.

## [7.1.0] - 2026-10-06

A minor release shipping the doctrine in standalone form. `standalone/AGENTS.md`
is a 94-line, fully self-contained edition of the manifesto plus its three
essential skills (quality, delivery, execution), carrying zero repo-internal
references so it can be dropped onto a host that has none of this repository.
`standalone/SOUL.md` is its identity twin: a 35-line soul document in the
soul.md convention (Core Truths, Boundaries, Vibe, Continuity), written in the
first person and host- and model-agnostic, carrying an explicit clause that it
evolves together with the doctrine it mirrors.

`scripts/install.sh` gains `--standalone`: it installs only the standalone
doctrine into each selected host's instruction-file slot, preferring
`standalone/<instruction basename>` when that file exists so a host whose
instruction file is SOUL.md receives `standalone/SOUL.md`, and falling back to
`standalone/AGENTS.md` otherwise. The flag composes with `--copy`, `--force`,
and `--dry-run`, and the default install is unchanged. README documents the
new tree and option. Gates: check.py --all 11/11 PASS.

## [7.0.0] - 2026-10-03

Stable cut of the 7.0.0 line. The major consolidates the skill set from
eighteen to eight: delivery, execution, and quality each absorb their
former satellites as router-style SKILL.md files whose deep detail moves
into bundled references (progressive disclosure), and architecture merges
solution-architecture, domain-modeling, design-pattern-selection, and
system-diagramming; confluence, security-audit, modernize-coding, and
indexed-search are unchanged. AGENTS.md is condensed with no rule dropped,
and the eval suite is regenerated from 63 to 33 cases against the new
layout (beta.1). Link hygiene lands across the doctrine: 97 anchor-bearing
relative links in 19 files drop their `#fragment`, because a host file
resolver reads the fragment as a literal path segment and fails the link,
and the `links` gate now rejects any relative target containing a `#`
(beta.2).

The stable cut additionally renames the repository's `orchestrator` role
agent to `lead`: Kilo Code ships a deprecated built-in agent named
`orchestrator`, and on hosts that derive the agent id from the
installed filename (kilo, opencode) the role agent of the same
name collided with the built-in. `lead` is the doctrine's own term
for the role, collides with no supported host's built-in agent,
and the agent body is unchanged. All artifacts move in lockstep:
`agents/common/orchestrator.md` becomes `agents/common/lead.md`,
`agents/common/orchestrator.plain.md` becomes
`agents/common/lead.plain.md`, `agents/codex/orchestrator.toml`
becomes `agents/codex/lead.toml`, the omp plugin-level root link
`agents/orchestrator.md` becomes `agents/lead.md`, and the marketplace
manifests and README point at the new paths. Consumers that dispatch
the agent by name must spawn `lead` instead of `orchestrator`, and
machines with a previous install should re-run
`./scripts/install.sh install` and remove the stale
`orchestrator.md` link left in their host agents directories. Gates:
check.py --all 11/11 PASS.

Per-beta detail in the sections below.

## [7.0.0-beta.2] - 2026-10-03

Link hygiene across the doctrine: 97 anchor-bearing relative links in 19
markdown files dropped their `#fragment`. Cross-file links keep the path
and drop the fragment; same-file navigation lists become plain text and
inline same-file links become prose or bold, since host file resolvers
treat the fragment as a literal path segment and fail the link. The
`links` gate (`g_links` in scripts/check.py) now rejects any relative
target containing a `#`, so a fragment cannot silently pass again. Fix
mutation-probed; gates: check.py --all 11/11 PASS.

## [7.0.0-beta.1] - 2026-10-03

Breaking consolidation of the skill set: eighteen skills become eight.
lifecycle + artifacts + grilling + wayfinder merge into delivery;
graph-engineering + teamwork into execution; craft + verification + evals +
performance into quality; solution-architecture + domain-modeling +
design-pattern-selection + system-diagramming into architecture. The
remaining four (confluence, security-audit, modernize-coding,
indexed-search) are unchanged. Each merged skill is now a router-style
SKILL.md whose deep detail lives in bundled references/, collapsing the
eight bodies from 1441 to 559 lines with no rule dropped. AGENTS.md is
condensed from 3575 to 2499 words, likewise losing no rule. check.py
repoints its rule-surface checks (comments, simplicity, typography) to
skills/quality/SKILL.md, and the eval suite is regenerated from 63 to 33
cases against the new layout. The marketplace manifests and README move to
the eight-skill layout. Consumers that reference the fourteen removed
skill paths must repoint; scripts/install.sh copies the skills directory
wholesale and needs no change.

## Retired detail (4.0.0 – 6.8.0-beta.1)

- [6.8.0] - 2026-10-01 — stable cut of the 6.8.0 line: omp host support (beta.1) and the lead's worktree isolation for parallel fan-out (beta.2), plus the `dashes` gate, the eleventh deterministic gate.
- [6.8.0-beta.2] - 2026-10-01 — parallel fan-out gains worktree isolation: one worktree and branch per unit, the lead owning the combine, and the exclusive-file-ownership law stated in the teamwork skill.
- [6.8.0-beta.1] - 2026-09-26 — omp (oh-my-pi) host support: an installer row for `~/.omp/agent`, with the role agents linked at the repository root for its plugin loader.
- [6.7.1] - 2026-09-25 — prose and structure release: the four-lever framing, the delivery lifecycle rewritten as control flow, and the fixed machine-scannable report templates.
- [6.7.0] - 2026-09-24 — the four command workflows stop asking on their no-options paths; every decision resolves from the repo's own signals, and the only stops left are best practices.
- [6.6.0] - 2026-09-24 — stable cut of the 6.6.0 line: the lead and worker role agents ship through every manifest route, and the lead dispatches by capability (beta.4).
- [6.6.0-beta.4] - 2026-09-24 — capability-based dispatch: the lead surveys the agent types its harness exposes and routes each unit to the best fit instead of a hard-coded target.
- [6.6.0-beta.3] - 2026-09-24 — the plugin `repository` field fixed to a plain URL string, unblocking Claude Code plugin installs and with them the skills and agents.
- [6.6.0-beta.2] - 2026-09-23 — the lead draws the task graph, scopes each unit, and owns the merge; the worker becomes a full act-and-prove loop.
- [6.6.0-beta.1] - 2026-09-23 — the `agents/` surface ships: the lead and worker definitions plus an installer column that distributes them per host.
- [6.5.1-beta.1] - 2026-09-23 — the `PROMPT:` intake gate states that an ask in any language is first rewritten as one concise English paragraph before work begins.
- [6.5.0] - 2026-09-20 — the eighteenth skill, `design-pattern-selection`: decision-first GoF selection behind a no-pattern gate.
- [6.4.1] - 2026-09-20 — the MiniMax host row corrected: the host does take a global `AGENTS.md`, so the row installs the manifesto again.
- [6.4.0] - 2026-09-19 — stable promotion of the 6.4.0 series: the craft simplicity rule, `modernize-coding` with five language adapters, and the `security-audit` skill; MiniMax Code joins the distribution layer.
- [6.4.0-beta.3] - 2026-09-18 — the `security-audit` skill: the candidate gate, the `needs_validation` state, and severity calibrated to demonstrated impact.
- [6.4.0-beta.2] - 2026-09-18 — `skills/modernize-coding` replaces the Go-only skill: modern means the ceiling the project declares, not a language release.
- [6.4.0-beta.1] - 2026-09-18 — the craft simplicity rule, pinned by a `simplicity` gate and an eval so neither canonical surface can lose it.
Detailed notes for these releases are retired; the full text lives in git
history (`git show v6.8.0:CHANGELOG.md` for 6.4.0 through 6.8.0-beta.1, and
`git log -p v4.0.0..v6.8.0-beta.1 -- CHANGELOG.md`). One line each, newest
first:

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
