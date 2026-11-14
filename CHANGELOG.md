# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The current line is carried in full; closed lines are retired below, one line
each. The full history lives in git tags and log (`v1.0.0` through `v3.11.0`,
and `git show v8.0.0-beta.10:CHANGELOG.md` for the retired detail).

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

## Retired detail (4.0.0 – 8.0.0-beta.10)

Detailed notes for these releases are retired; the full text lives in git
history (`git show v8.0.0-beta.10:CHANGELOG.md` for 7.0.0-beta.1 through
8.0.0-beta.10, and `git show v6.8.0:CHANGELOG.md` for 4.0.0 through
6.8.0-beta.1). One line each, newest first:

- [8.0.0-beta.10] - 2026-11-12 — the always-on surface is measured rather than assumed: the doctrine freezes no measurement, a tool's schema is priced before its server is connected, a settled fact stays settled, a read and a search go through the tool built for each, and the lead dispatches once the graph is written.
- [8.0.0-beta.9] - 2026-11-11 — the unslop skill gains the half it was missing: preservation. A rewrite may not invent the fact, a hit is not a verdict, the project outranks the rule lists, and the scanner reports without changing anything.
- [8.0.0-beta.8] - 2026-11-10 — context becomes a budget rather than a container: the window is an attention budget, an instruction has an altitude, a compaction is lossy in the dangerous direction, a bundled reference shares its skill's ceiling, and the changelog becomes a readable map.
- [8.0.0-beta.7] - 2026-11-10 — the loop gains a controller: the terminal conditions are declared and every failure takes a route chosen from the evidence, the nine system-level properties are measured by an instrument that can fail, and the harness is sized on the two named axes.
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
