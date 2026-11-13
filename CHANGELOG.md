# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The current line is carried in full; closed lines are retired below, one line
each. The full history lives in git tags and log (`v1.0.0` through `v3.11.0`,
and `git show v8.0.0-beta.6:CHANGELOG.md` for the retired detail).

## [8.0.0] - 2026-11-14

Stable cut of the 8.0.0 line, unchanged in behavior since
`v8.0.0-beta.10`: the setup is rewritten on the AI-native SDLC spine and
made agnostic of programming language, agent framework, and host harness.

- **A six-stage loop replaces the phase sequence.** Plan, Design, Build,
  Test, Deploy, and Maintain each commit a readable artifact the next stage
  begins from, the accepted artifact fires the next gate, and the chain of
  commits is the audit trail. Sizing is part of the loop: the compact path
  is the default, and the full path is owed only when the work is large,
  irreversible, outward-facing, cross-session, or multi-agent.
- **Rules name roles, not stacks.** Every rule in the manifesto is stated
  so it survives a change of language, framework, or harness, and the
  `agnostic` and `portable` gates reject a host-binding or stack-specific
  token that creeps back in.
- **A loop declares when to stop.** Terminal conditions, the requirements
  still owed, and a failure route chosen from the evidence replace the
  default of retry; escalation stops and asks rather than resolving a human
  decision by inference.
- **Context is an attention budget.** The window is kept small because
  recall degrades as it grows, instructions sit at the altitude that states
  the outcome and the check, and a compaction preserves the decisions, the
  owed requirements, the position, and the anchors while dropping what disk
  can re-derive.
- **The harness is sized on two named axes.** Action complexity and context
  complexity price different machinery, so the harness is specified per job
  rather than as the union of what every kind of agent needs; every harness
  feature is a bet that expires when the model no longer needs it.
- **Claims about a structure are measured.** The nine system-level
  properties are scored from a run trace by an instrument that passes an
  organized run and fails a degraded one, so a property that cannot fail is
  not a property.
- **The doctrine freezes no measurement and settles no re-check.** A
  statistic asserted in prose is true of one setup on one day, so each rule
  names the mechanism and leaves the number to the reader; a check that has
  already answered is recorded and read back rather than re-run.
- **The changelog is a map.** Closed lines retire to one line each with the
  full text in git history, held by the `changelog` gate, so the release a
  reader wants is not buried under the archive.

Gates: 46, `python3 scripts/check.py --all` green.

## [8.0.0-beta.10] - 2026-11-12

The always-on surface is measured, not assumed, and a settled fact stays settled.

- **The doctrine freezes no measurement.** A statistic asserted in prose — a
  token count from one turn, a failure rate from one run, a speed multiplier
  from one benchmark — is true of one setup on one day, cannot be re-derived by
  the reader, and goes stale without anyone noticing. The doctrine stated
  several: intuition about the bottleneck is wrong most of the time, typed
  comparison beats reflection by a fixed multiple, a container's memory limit
  belongs at a fixed share of its ceiling, a re-searched concept was searched a
  fixed number of ways. Each now names the mechanism and leaves the number to
  the reader's own measurement. The new `measured` gate holds the line, and the
  manifesto's hard constraints carry it on both installed surfaces.

- **A tool's schema is prompt the agent reads on every turn.** A connected
  server's catalogue is not a capability the agent pays for only when it calls
  it — the schemas sit in the window before the job starts and stay there for
  every turn, so breadth has a price beyond confusion. The rule is now in
  `execution/references/harness-design.md`: scope a server's surface where it
  is cheapest, and measure the schema cost before connecting it. The count
  itself stays out of the doctrine — a catalogue's size is a property of one
  server on one day, and a rule that names it as a number goes stale the
  moment that server changes. The `catalogue` gate holds that line.
- **A settled fact is settled.** When a check has already returned its answer,
  re-running it costs a round trip and buys nothing. Re-deriving a known result
  is the most common form of wasted work in a long run, and it looks like
  diligence because each individual re-check is fast. The rule now sits beside
  the bounded-evidence clause in the manifesto: record the result and read it
  back.
- **A read, a search, and a listing go through the tool built for each.** A
  measured run reached through the shell for all three, so a file printed whole
  into the window instead of a bounded slice, and one turn carried the largest
  input the run ever paid. The rule now names the purpose-built tool in both
  doctrines and in the reference that designs the tool surface, and the shell
  keeps the commands only it can run. The `toolrouting` gate holds it on every
  surface that states it.
- **The lead dispatches once the graph is written.** The lead owns the graph,
  the briefs, the verification, and the merge, and exploration before dispatch
  duplicates work the first unit will redo: a measured run spent its opening
  phase reading before any unit existed. The rule now sits on every lead role
  surface, and the `leadorientation` gate keeps a trim from dropping it from
  one variant alone.

Gates: 40 -> 46.

## [8.0.0-beta.9] - 2026-11-11

The unslop skill gains the half it was missing: preservation.

- **Preservation outranks polish.** The skill could cut residue, but nothing
  in it said what a rewrite must not touch. Facts, units, dates, names, paths,
  identifiers, quotes, citations, and code now survive a rewrite exactly, and
  so do scope, negation, and force-bearing words in a security or legal rule.
  With no finding, the source returns unchanged: a no-op beats an uncertain
  edit.
- **A rewrite may not invent the fact.** "Robust retry logic" becomes "three
  attempts over 500ms" only when the repository says so. Otherwise the sentence
  is cut, or the hit is missing work and carries a `PENDING:` line.
- **A hit is not a verdict.** Quoted examples, fenced demonstrations, domain
  terms, and attributed quotes are protected, so the scanner stops flagging the
  rule lists that name the residue and the documents that cite it.
- **The project outranks the lists.** A declared design system, component
  library, or glossary is read before judging; its choice beats a default here.
- **Audit only.** "Just flag it" stops after the split, reports every hit with
  its rule id, and changes nothing.
- **Three prose rules added:** the throat-clearing opener (P51), the model
  talking about itself instead of reading the source (P52), and the anti-slop
  overshoot that swaps one machine register for another (P53).
- **The interface surface gains its preconditions:** size the job honestly
  before running nine passes, read the project's tokens before inventing a
  palette, and write the five-line direction before touching a value.

## [8.0.0-beta.8] - 2026-11-10

Context becomes a budget rather than a container.

- **The window is an attention budget, not a container.** The setup already
  said to keep the window small, but framed it as cost: fewer tokens, less
  spend. That is the weaker half of the truth. Recall degrades as the context
  grows, so a window that is merely affordable can still be the wrong one —
  the tokens that matter are harder to retrieve out of a large context than
  out of a small one. Keeping the window small is an *accuracy* rule, and the
  smallest set of high-signal tokens is what maximizes the chance of the
  desired outcome.
- **An instruction has an altitude.** Too low is brittle hardcoded logic —
  a branch for every case the author imagined, fragile and expensive to
  maintain as the world moves. Too high is vague guidance that assumes
  shared context the run does not have, so the gap gets filled with something
  plausible. The right altitude is specific about the outcome and the check
  and leaves the method to the model: state what must be true when the
  instruction is satisfied, not the steps that might produce it.
- **An example teaches what a rule cannot.** Some behaviors are checks and
  belong in a check. Others are a shape of behavior no check names, and an
  enumerated list of every edge case is a poor substitute for one: long,
  unweighted by likelihood, and reading like a rule list rather than a
  demonstration. A few diverse, canonical examples carry the behavior in a
  fraction of the tokens.
- **A compaction is lossy in the dangerous direction.** What it drops may
  look redundant at the time and matter later, so the policy is explicit
  about what survives: the decisions and their reasons, the requirements
  still owed, the current position, and the anchors. What goes is what the
  run can re-derive from disk. The lightest touch that helps is clearing old
  tool results before discarding anything the run reasoned about. This is
  about *using* compaction when a window fills — not about building a
  compaction subsystem, which the setup still refuses to add speculatively.
- **Just-in-time retrieval beats up-front loading.** A run that carries the
  whole corpus pays for it every turn and recalls less as it grows; keeping
  a lightweight identifier and loading the body at the moment it is needed
  is the trade the setup already makes with skills and references. The
  identifiers carry meaning too: a name and a location say what the
  material is for and when it was written.
- **The working detail lives in a new reference.** `execution/references/
  context-engineering.md` carries the budget, the altitude, the
  examples-over-edge-case-lists rule, the compaction policy, and the
  retrieval trade. The `execution` skill gains a `## Context` section, and
  its Runtime State paragraphs were compressed so the section fits inside
  the loadable-whole budget rather than exceeding it.
- **The rule is a gate, not a habit.** The new `context` gate asserts the
  budget, the altitude, and the compaction policy survive on the manifesto,
  the standalone copy, the execution skill, and the reference that owns them.
  The harness regression suite gains an eval exercising the same checks.
- **A reference is read whole when it is read, so it carries the same
  ceiling a skill body does.** One bundled reference — the endpoint page
  template — had grown to roughly 6,150 tokens, larger than any loadable
  skill, so the run either truncated it or spent more context on one
  deferred file than on the whole skill that points at it. It is now split
  into the template, the change-log and round-marker discipline, and the
  recorded page-family variants, each named from its skill on a stated load
  condition. The `skillbudget` gate now checks every bundled reference, so
  the next oversized file fails the build rather than the run.
- **The changelog becomes a readable map rather than an archive.** It had
  grown to roughly 17,800 tokens because every release kept its full text
  forever, so the releases a reader actually wants were buried under the
  ones nobody rereads. The repo already solved this for the 6.x line in
  v7.8.1 — a closed line retires to one line each, with the full text
  reachable in git history — and 25 closed versions now carry that shape,
  so the file reads at roughly 5,400 tokens. No version was dropped: all 65
  remain, each one saying what changed.
- **The discipline is a gate, not a habit.** The new `changelog` gate holds
  the file within a line and token ceiling, so the next release cannot
  quietly restore the archive. The suite gains an eval that checks the
  ceiling, the links, and the release contract together — the published
  body still reads verbatim from the changelog section.

Gates: 38 -> 40.

## [8.0.0-beta.7] - 2026-11-10

The loop gains a controller: it declares when to stop, and a failure gets a
route chosen from the evidence rather than a default of retry.

- **A loop declares its terminal conditions and owes a route for every
  failure.** A run that cannot name the states from which continuing is no
  longer justified continues on hope, and a failure with no route other than
  retry is a spin wearing a progress report. The new rule states the goal,
  the acceptance criteria that close it, and the stop states up front; tracks
  the requirements still owed, so a step advances the run by closing one
  rather than by finishing; and picks the route from the evidence — revise,
  take another capability, recover an earlier state, escalate to a human, or
  terminate — with escalation meaning the run stops and asks, never resolving
  a human decision by inference.
- **The working detail lives in a new reference.** `execution/references/
  loop-control.md` carries the terminal conditions, the five routes and what
  each costs, the continuity that binds one iteration to the next through the
  recorded state, the fact that feedback is intermediate rather than only
  terminal, and the capability record — the relations that say what each
  worker can do, kept as a versioned record so the next assignment is a
  lookup rather than a guess, and so a worker that loses a resource leaves
  its units reassignable rather than stuck.
- **The rule is a gate, not a habit.** The new `loop` gate asserts the rule
  survives on the manifesto, the standalone copy, the execution skill, and
  the reference that owns the detail, so one surface cannot silently lose it.
  The harness regression suite gains an eval that exercises the same four
  checks.
- **The always-on footprint is unchanged in kind.** The rule is one
  paragraph on each installed surface; the standalone copy stays inside its
  token ceiling, and the execution skill's body was condensed to make room
  for the new section rather than exceeding its loadable-whole budget.
- **The skills are validated against the published specification.** The
  validation pipeline now runs the Agent Skills reference library's own
  validator over every shipped skill, so conformance with the specification
  is checked by the specification's tool rather than by a local reading of
  it. The reference library's command is stable enough to name; a rename
  upstream breaks this step loudly, which is the correct failure mode for a
  gate that claims conformance.
- **The nine system-level properties are measured, not asserted.** The
  doctrine claimed nine properties of a multi-agent structure — goal
  formation, semantic consistency, parallel execution efficiency,
  heterogeneous capability allocation, collective decision quality, state
  consistency, failure recovery, transfer across tasks, runtime overhead —
  and said a claim with no measurement is a narrative. That left the claim
  itself as the narrative. The new instrument reads a run trace and scores
  each property against a stated threshold, so a report can now answer
  whether a structure delivered what it claimed.
- **The measurement can fail.** Two traces under `evals/fixtures/` disagree
  on every property, and the `properties` gate requires the instrument to
  pass the organized one and fail the degraded one. A property that cannot
  fail is not a property, and a measurement that passes both directions
  measures nothing. The suite gains nine evals, one per property, each
  checking both directions.
- **An unexercised property does not score as a pass.** A run with no
  failures has nothing to recover and a team with no decisions has nothing
  to merge; the instrument scores those 0.0 rather than 1.0, so a structure
  cannot earn a property by not having the situation that exercises it.
- **The harness is sized on two named axes.** The setup said to size each
  job and pointed at action and context complexity, but neither axis was
  defined anywhere — a promise with no definition behind it, on the surface
  every task reads. The two are now defined: action complexity is how many
  tools, decisions, dependencies, and handoffs a job coordinates; context
  complexity is how much it must gather, retain, and retrieve. They move
  independently, so a job can route widely while carrying little or carry a
  lot while routing little, and each axis prices different machinery — action
  complexity buys routing and tool surface, context complexity buys state and
  retrieval. The average job is not the job: the union of what every kind of
  agent needs describes almost no one, so the harness is specified per job
  from its own axes.
- **The three strain moves are defined, in the order they apply.** Reduce
  (do fewer things), Offload (move what remains out of the window, onto disk
  read on demand), Isolate (split the concern into its own context). Isolate
  comes last because it adds the machinery the other two avoid. A team is
  warranted only when the strain survives all three.
- **Every harness feature is a bet that expires.** Each one encodes an
  assumption that the model cannot do the thing on its own, so when the model
  improves the feature becomes dead weight constraining the model it was
  built for. A feature is a bet, and a bet is re-examined when the model
  changes. The new `harnessaxes` gate asserts both axes survive on both
  installed surfaces, the execution skill, and the reference that owns the
  derivation.

Gates: 35 -> 38.

## Retired detail (7.0.0-beta.1 – 8.0.0-beta.6)

Detailed notes for these releases are retired; the full text lives in git
history (`git show v8.0.0-beta.6:CHANGELOG.md` for 7.0.0-beta.1 through
8.0.0-beta.6, and `git log -p v7.0.0-beta.1..v8.0.0-beta.6 -- CHANGELOG.md`).
One line each, newest first:

- [8.0.0-beta.6] - 2026-11-10 — the trigger instrument stops waiting for one row at a time: rows of a split are independent, so `evals/run_triggers.py` measures them through a thread pool (`--workers`, default 8), with a check asserting the parallel run matches the serial run line for line.
- [8.0.0-beta.5] - 2026-11-10 — the search discipline and the diagnosis closure are stated where a search will load them: a measured run spent half its 270 shell calls on search waste, so two clauses now sit in the intake section of both doctrine surfaces, the trigger instrument covers the conditions the widened description claims (validation split 0.62 to 0.75), and the gate count stops drifting from the gates.
- [8.0.0-beta.4] - 2026-11-10 — the skills align with the Agent Skills specification and the two skill-authoring guides: every description opens imperatively and names its boundary, bundled references state their load condition, and the rules that keep them aligned become gates rather than habit.
- [8.0.0-beta.3] - 2026-11-09 — the graph structure closes three gaps and the vocabulary converges: *structured is not engineered* (typed edges, observed graphs, one term per concept), and the three claims about goals, grounding, and recovery gain a home.
- [8.0.0-beta.2] - 2026-11-09 — the doctrine is rewritten to be agnostic of programming language, agent framework, and agent harness: rules name roles, not stacks.
- [8.0.0-beta.1] - 2026-11-05 — the spine is rewritten on AI-native SDLC: a six-stage loop (Plan, Design, Build, Test, Deploy, Maintain) replacing the previous seven, where each stage commits a readable artifact the next begins from and the accepted artifact fires the next gate.
- [7.9.0-beta.5] - 2026-11-05 — a tenth on-demand skill, `unslop`, removes AI residue from the artifacts a task delivers: prose, code, and interface rules under one discriminator (swap this project for a different one — a line that still reads as true carries no information), with stable rule ids and a scanner that finds candidates, not verdicts.
- [7.9.0-beta.4] - 2026-11-03 — the per-task cost of the setup is made proportional to the job instead of fixed: the compact path is the default, the confirmation stop is proportional, the verification loop is sized rather than skipped, and a new `cost` gate holds the always-on footprint within a token budget.
- [7.9.0-beta.3] - 2026-11-01 — skill-authoring conformance with the Agent-Skills best-practices guidance: bundled references must state their load condition, and the places where the repository only appeared to follow the guidance are fixed.
- [7.9.0-beta.2] - 2026-10-29 — state is recorded, not remembered: the state record carries evidence pointers and a version, a transition is proposed, validated, then committed, and recovery names its boundary before repairing.
- [7.9.0-beta.1] - 2026-10-27 — the shared setup adopts the general coding-agent practice of managing prompts, plans, skills, and workflows, closing three gaps it left open: the execution environment, the automation layer, and session hygiene.
- [7.8.1] - 2026-10-25 — the 6.x line retires: 17 versions move into the retired list, one line each, with the full text still reachable in git history.
- [7.8.0] - 2026-10-25 — skills ship stable, addressed by name: every skill reference in the manifesto, the command workflows, and the skill bodies names the skill rather than linking a `SKILL.md` path the runtime may not resolve.
- [7.7.0-beta.1] - 2026-10-24 — sessions are the default unit of forgetting, so the doctrine now says where knowledge goes: memory is a design decision, not a hope, with five layers under organization and project memory.
- [7.6.0-beta.1] - 2026-10-23 — skills, commands, and evals follow the Agentskills authoring guidance: a description carries the whole triggering decision, and it is measured rather than argued.
- [7.5.1-beta.1] - 2026-10-21 — the stuck subagent loop is fixed in every shipped variant: a spawn error is terminal for that route, the job carries a dispatch budget, and workers never spawn workers.
- [7.5.0] - 2026-10-19 — three features ship stable: typed test doubles close the gap between production type discipline and test code, and the doctrine teaches and obeys KISS, DRY, SOLID, and YAGNI by name.
- [7.4.0] - 2026-10-09 — lint evidence becomes owed rather than remembered: the done report on every source change carries an `L1:` line with the project's own commands and exit codes, discovered from its manifests and never assumed absent.
- [7.3.0] - 2026-10-08 — the four command workflows complete a uniform no-options autonomy contract: each resolves every decision from the repo's own signals, states its inferences in one line, and stops only at its named bound.
- [7.2.0] - 2026-10-08 — stable cut of the 7.2.0 line: the doctrine both teaches and obeys KISS, DRY, SOLID, and YAGNI, with checkable rules in the craft surface.
- [7.2.0-beta.1] - 2026-10-07 — principle-alignment release: the core principles carry the classic names, the Hard Constraints section is one clause per line, and the executing surface operationalizes all four.
- [7.1.0] - 2026-10-06 — the doctrine ships in standalone form: a fully self-contained `AGENTS.md` carrying no repository-internal references, for a host with no repository.
- [7.0.0] - 2026-10-03 — stable cut of the 7.0.0 line: the skill set consolidates from eighteen to eight on the AI-native delivery spine.
- [7.0.0-beta.2] - 2026-10-03 — anchor-bearing links become prose or bold, since host file resolvers read a fragment as a literal path segment.
- [7.0.0-beta.1] - 2026-10-03 — the breaking skill-set consolidation: eighteen skills become eight, with the lifecycle, graph engineering, and craft material merged into the delivery, execution, and quality skills.
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
