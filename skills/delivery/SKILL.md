---
name: delivery
description: "Use when deciding where a piece of agent work belongs and what artifact it owes: the six-stage AI-native delivery loop (plan, design, build, test, deploy, maintain), the per-stage plays, the artifact chain whose accepted artifact fires the next gate, advisory versus deterministic controls, autonomy tiers, and closing the loop from a breached control band back to a new intent.md. Also the intent.md / spec.md / PLAN.md / STATUS.md shapes with WPn work packages and a DONE_WHEN checklist, grilling a decision in numbered frontier rounds, and a wayfinder map of decision tickets for an effort too large for one session. Reach for it when a task needs a plan before code, when work spans sessions or agents, when a decision must be interviewed out of the user, or when someone asks which stage or document a change needs. Not for the mechanics of running a stage (execution) or for proving output correct (quality)."
---

# Delivery

One doctrine for plan-shaped agent work, merged because it is one loop, not a list of topics: **Lifecycle** names where work belongs and what each stage commits; **Plays** turns each stage into steps a team can run; **Artifacts** fixes the deterministic shapes those stages write; **Controls** separates advice from enforcement; **Automation** tiers what may act unattended; **Grilling** settles a decision in one session; **Wayfinder** runs that same interview across sessions as a map when the effort outgrows one.

> **Override.** A project-level process spec that explicitly supersedes this skill wins.

## Lifecycle

Code stopped being the bottleneck once agents could write it faster than humans could plan, review, and ship around it, so the constraint moves to the steps around it — plan, review, deploy — which still run at human speed. Controls sized for human output stop matching reality, and governance costs rise because exceptions still route through committees.

The job is a **loop**, not a phase sequence: each stage commits a readable artifact the next begins from, and that artifact chain *is* the audit trail; six stages, and `Maintain` reopens `Plan`. The old control objectives stay — accountability, control, audit — and only the enforcement changes: AI is embedded at every point, and the handover between stages is automated rather than negotiated. The loop keeps running; human judgement stays above it.

| Stage | Commits | Seat | Exit check |
| --- | --- | --- | --- |
| **Plan** | `intent.md` — problem, affected parties, desired outcome, constraints, exclusions, open questions | Originator | acceptance recorded |
| **Design** | `spec.md` + ADRs — requirements and design together, risks, contradictions, unresolved decisions | Steward / Architect | spec accepted; an ADR per hard-to-reverse choice |
| **Build** | `PLAN.md` + `STATUS.md`, then the diff and its tests | Implementer | plan approved before code; L1 green; a failing regression test precedes a fix |
| **Test** | evidence (L1/L2/L3) + review findings | Verifier | evidence audit passes; verdict issued |
| **Deploy** | the PR with its review findings, the release record + `AUTH:` | Approver | explicit human authorization for the outward step |
| **Maintain** | incident record -> new `intent.md` | Operator | the loop reopens |

A stage exits only on its check; "the agent finished" is not an exit. Stages are **re-entered** through two **canonical back-edges** — `Test -> Build` (a refuted verdict returns to the implementer with findings, the ordinary review cycle, capped by the 3-failed-cycles rule) and `Maintain -> Plan` (a production anomaly becomes a *new* `intent.md`). Skipping a stage is allowed only by naming why in the artifact that follows; silent skipping is the failure.

**Size the path to the job.** The artifact chain is an audit trail for work big enough to need one, not a per-task tax. A small, local, reversible change takes the **compact path**: one THINK, one ACT, one PROVE, held in the conversation, with no `intent.md` / `spec.md` / `PLAN.md` chain and no state checkpoint. The full six-stage path is owed when the work is large, irreversible, outward-facing, cross-session, or multi-agent; taking the compact path *is* the recorded reason for the stages it skips.

**Accepted artifacts fire the next gate.** A stage begins from the artifact the previous one committed, so the handoff is the commit itself: a committed `intent.md` can trigger the design pass, an approved `spec.md` triggers planning, and a merged PR triggers the pipeline. Human attention concentrates at the gates — reviewing what the agent flagged — rather than at the start of each stage.

**One source of truth per artifact.** Where a legacy system already holds the record — a tracker, a requirements tool, a wiki — name it the source of truth and keep the committed artifact as a linked working copy; otherwise the committed artifact is the record. Every artifact notes the record id, and every legacy record carries the commit id of the artifact. Two copies with no link are two truths, and both drift.

Seven **seats**, not seven people — one actor may hold several: Originator (files the intent, owns acceptance), Steward (owns spec and domain language), Architect (reviews higher-risk design; ADR routing), Implementer (executes the plan), Verifier (re-derives against anchors in a **fresh context**; judges, never writes), Approver (human gate on outward, destructive, or deploy steps; the `AUTH:` quote is theirs), Operator (maintains, triages, reopens the loop). Two constraints never bend: **the Implementer never approves its own work**, and **the Verifier is independent of what it judges**. Org roles collapse into these — release manager is the Approver, auditor a Verifier, on-call the Operator.

Verification attaches at every stage exit (L1/L2/L3, evidence audit; the mutation probe on high-risk work). Distinct from that, the lifecycle itself is configuration an agent executes, so evals regression-test the process across runs and block a change that lowers the pass rate — evals test the process, verification tests one unit of work. Inside a stage, work is shaped as an execution graph (nodes, typed edges, caps, the minimal-harness ladder); the stage says what is committed, the graph how.

## Plays

Each stage carries **plays** — a named practice with what it changes, how to start, the steps, the governance, and how to measure it. The steps are modular: adopt the stages you need in the order that suits you, and let a play with no prerequisites be a starting point. Read [plays](references/plays.md) when you are choosing a practice for a stage, or when you need the per-stage measurement pairs (a leading indicator and a lagging indicator) that say whether the practice worked.

The shifts the plays produce, stage by stage:

| Stage | Traditional | AI-native |
| --- | --- | --- |
| Plan | requirements gathered by committee, distilled through workshops and sign-offs, written up by hand | intent synthesized from the source in the originator's own words and captured in `intent.md`, human readable and machine actionable |
| Design | spec written by analysts, parsed by designers | requirements and design compressed into one working session, guided by standards encoded as skills and versioned in git |
| Build | tests and code handwritten, documentation written after the work | code and tests generated, institutional knowledge maintained as versioned machine-readable context files and skills |
| Test | QA gates at stage boundaries | continuous evals woven through implementation, and every session checks its own work before a human sees it |
| Deploy | humans review every line, governance in review cycles | layered agentic review with human review reserved for regulated and critical code; governance enforced as the agent acts |
| Maintain | humans watch production for bugs | agents monitor live deployments; a breached control band is diagnosed and written back into the loop as a new `intent.md` |

## Artifacts

An artifact an execution session must **resume from** needs a **deterministic shape**: same sections in the same order, same vocabulary for the same things. Plans only humans read may stay prose. Three durable shapes belong to the first three stages — `intent.md` (Plan), `spec.md` (Design), and `PLAN.md` + its sibling `STATUS.md` ledger (Build).

The templates, the shared vocabulary (`WPn`, `DONE_WHEN`, `PENDING`, the §0 `INTENT` gate), the `STATUS.md` ledger rules, and the drift sweep for an existing plan live in [artifact-shapes](references/artifact-shapes.md) — read it when you are about to write or resume an `intent.md`, `spec.md`, `PLAN.md`, or `STATUS.md`. When a plan, spec, or handoff feels wrong but you cannot name why, the failure modes the other faces prevent are tabulated in [common-mistakes](references/common-mistakes.md).

## Controls

A control is only as strong as the thing that enforces it, and there are two kinds, and confusing them is the defect.

**Advisory controls** shape the work while it is produced: a skill encoding a policy, a project context file carrying conventions and commands, a prompt stating the constraint. They make a violation rare, because the agent applies the policy as it writes rather than discovering it in a review weeks later. They cannot guarantee anything, because nothing forces a session to comply.

**Deterministic controls** are what make a policy that must always hold actually hold: a hook that blocks the action, a check that exits non-zero, a branch rule that demands a named approval, a sandbox that refuses the command. The rule is simple — **a skill makes violations rare; a hook makes them close to impossible.** Anything a policy declares absolute needs a deterministic control behind it, and anything that merely guides gets an advisory one.

**Enforcement belongs where the action happens.** Controls fire where the work happens, so a control that must apply to every session lives in the repository, not in one operator's setup: version-controlled hooks and settings, shared permission rules, a review pass that re-checks the policy at the merge. A control an engineer can switch off is not a control.

**Separation of duties survives automation.** The agent that wrote the code has no route to approve it: findings rank by severity, a human owns the approval, and the merge gate stays with the code owner. **Autonomy is tiered per environment** — free in development, prepared and authorized in production — so the human gate sits above the automation, never inside it.

**Rollback is rehearsed before it is needed.** The path that closes the loop is the one most likely to be used under pressure, so it is exercised regularly in a lower environment rather than discovered during an incident.

## Automation

Automation is the layer above a skill — it decides when a workflow runs, not how. Automate only a workflow that has proven itself interactively: declare the unattended run's scope, let the check gate its stop, and keep the authority with a human — an automated run ends local and emits `PENDING:` rather than posting, publishing, merging, or deleting on its own.

**The loop closes at Maintain.** A trigger invokes the agent with no person in the invocation path — a breached control band, a ticket, a channel message, a schedule. Detection stays deterministic: a script watches a rolling baseline and decides the tier; no model is involved in deciding that something happened. The tier then sets what the agent may do: log it, diagnose it read-only, or propose through the review gate. The finding re-enters the loop as a new `intent.md` in the Plan format, so the same stages run again. A confidence gate sits between stages — a deterministic check or an adversarial reviewing agent — deciding whether the previous stage's output continues or escalates to a human.

**The report is the output.** An unattended run's deliverable is a report carrying commands, exit codes, and findings, never a silent change to a branch nobody reviewed. Template, failure modes, and the per-run scope declaration live in the `execution` skill's automation reference.

## Grilling

Interview the user until you reach shared understanding of a plan, decision, or idea — the technique behind the manifesto's plan-first intake route, ambiguity drained through conversation and never through guessing. Map the decision space as a **design tree** and work it in **rounds**: each round asks the whole **frontier** — every question whose prerequisites are settled — numbering each question and giving a recommended answer, then stops and waits. Facts are the agent's to look up; only decisions reach the user.

Read [grilling](references/grilling.md) when a round needs its template, the fact-versus-decision dispatch, or the completion rule.

## Wayfinder

A loose idea too big for one agent session becomes a **map** — one issue labelled **`wayfinder:map`** whose child **decision tickets** are questions resolved one per session until the route is clear.

Read [wayfinder](references/wayfinder.md) when an effort outgrows one session and needs the map anatomy, ticket types (Research / Prototype / Grilling / Task, AFK / HITL), the fog-of-war rules, and the resolver and charting invocation halves.
