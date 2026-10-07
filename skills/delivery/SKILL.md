---
name: delivery
description: "Delivery doctrine for plan-shaped agent work, in four faces. Lifecycle: the seven stages (intent, spec, plan, build, test, release, operate), their canonical back-edges, the collapsible seven seats, and the handoff, approval, and reopen rules between them. Artifacts: the deterministic shapes intent.md, spec.md, and PLAN.md with its sibling STATUS.md ledger, WPn work packages, a DONE_WHEN checklist of executable checks, and a grounded mermaid diagram. Grilling: plan-first interviews that walk a design tree in numbered frontier rounds, facts looked up by the agent and decisions put to the user. Wayfinder: a map of decision tickets (label wayfinder:map) resolved one per session until the fog clears. Use when deciding where work belongs in the delivery loop, what artifact a stage owes, who owns an approval, how to interview for a decision, or how to chart an effort too big for one session or shared across agents."
---

# Delivery

Four faces of one doctrine for plan-shaped agent work, merged because they are one loop, not four topics: **Lifecycle** names where work belongs and what each stage commits; **Artifacts** fixes the deterministic shapes those stages write; **Grilling** settles a decision in one session; **Wayfinder** runs that same interview across sessions as a map when the effort outgrows one.

> **Override.** A project-level process spec that explicitly supersedes this skill wins.

## Lifecycle

Code stopped being the bottleneck once agents could write it faster than humans could plan, review, and ship around it, so the constraint moved outward — to intent, review, governance. The job is a **loop**, not a phase sequence: each stage commits a readable artifact the next begins from, and that artifact chain *is* the audit trail; seven stages, and `Operate` reopens `Intent`.

| Stage | Commits | Seat | Exit check |
| --- | --- | --- | --- |
| **Intent** | `intent.md` — problem, affected parties, desired outcome, constraints, exclusions, open questions | Originator | acceptance recorded |
| **Spec** | `spec.md` + ADRs — requirements, design, risks, contradictions, unresolved decisions | Steward / Architect | spec accepted; an ADR per hard-to-reverse choice |
| **Plan** | `PLAN.md` + `STATUS.md` — work packages, `DONE_WHEN`, ledger | Steward | every `WPn` names its files and its verify command |
| **Build** | diff + tests | Implementer | L1 green; a failing regression test precedes a fix |
| **Test** | evidence (L1/L2/L3) + review findings | Verifier | evidence audit passes; verdict issued |
| **Release** | release record + `AUTH:` | Approver | explicit human authorization for the outward step |
| **Operate** | incident record -> new `intent.md` | Operator | the loop reopens |

A stage exits only on its check; "the agent finished" is not an exit. Stages may be **re-entered** through two **canonical back-edges** — `Test -> Build` (a refuted verdict returns to the implementer with findings, the ordinary review cycle, capped by the 3-failed-cycles rule) and `Operate -> Intent` (a production anomaly becomes a *new* `intent.md`). Skipping a stage is allowed only by naming why in the artifact that follows; silent skipping is the failure.

Seven **seats**, not seven people — one actor may hold several: Originator (files the intent, owns acceptance), Steward (owns spec and domain language), Architect (reviews higher-risk design; ADR routing), Implementer (executes the plan), Verifier (re-derives against anchors in a **fresh context**; judges, never writes), Approver (human gate on outward, destructive, or release steps; the `AUTH:` quote is theirs), Operator (maintains, triages, reopens the loop). Two constraints never bend: **the Implementer never approves its own work**, and **the Verifier is independent of what it judges**. Org roles collapse into these — release manager is the Approver, auditor a Verifier, on-call the Operator.

Verification attaches at every stage exit (L1/L2/L3, evidence audit, mutation probe). Distinct from that, the lifecycle itself is configuration an agent executes, so evals regression-test the process across runs and block a change that lowers the pass rate — evals test the process, verification tests one unit of work. Inside a stage, work is shaped as an execution graph (nodes, typed edges, caps, the minimal-harness ladder); the stage says what is committed, the graph how.

Implementation is the agent's; approval is not. Human judgment concentrates at the seams — accepted intent, agreed spec, authorized release — and policies are applied while artifacts are produced, not discovered in a later review: a policy that must always hold is backed by a deterministic gate, not an instruction to remember it, and automation stops at the production boundary so approval happens above it.

## Artifacts

An artifact an execution session must **resume from** needs a **deterministic shape**: same sections in the same order, same vocabulary for the same things. Plans only humans read may stay prose. Three durable shapes belong to Intent, Spec, and Plan — `intent.md`, `spec.md`, and `PLAN.md` + its sibling `STATUS.md` ledger; `<plans-root>/<feature-slug>/` (kebab-case) holds the chain, and the filename is invariant.

The templates, the shared vocabulary (`WPn`, `DONE_WHEN`, `PENDING`, the §0 `INTENT` gate), the `STATUS.md` ledger rules, and the drift sweep for an existing plan live in [artifact-shapes](references/artifact-shapes.md). The failure modes all four faces prevent are tabulated in [common-mistakes](references/common-mistakes.md).

## Grilling

Interview the user until you reach shared understanding of a plan, decision, or idea — the technique behind the manifesto's plan-first intake route, ambiguity drained through conversation and never through guessing. Map the decision space as a **design tree** and work it in **rounds**: each round asks the whole **frontier** — every question whose prerequisites are settled — numbering each question and giving a recommended answer, then stops and waits. Facts are the agent's to look up; only decisions reach the user.

The round template, the fact-versus-decision dispatch, and the completion rule: [grilling](references/grilling.md).

## Wayfinder

A loose idea too big for one agent session becomes a **map** — one issue labelled **`wayfinder:map`** whose child **decision tickets** are questions resolved one per session until the route is clear.

The map anatomy, ticket types (Research / Prototype / Grilling / Task, AFK / HITL), the fog-of-war rules, and the resolver and charting invocation halves: [wayfinder](references/wayfinder.md).
