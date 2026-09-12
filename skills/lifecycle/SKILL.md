---
name: lifecycle
description: "The AI-native delivery lifecycle: seven stages (intent, spec, plan, build, test, release, operate) that form a loop rather than a waterfall, the artifact each stage commits, the seven seats that own them, and the handoff and reopen rules between stages. Use when deciding where a piece of work belongs in the delivery loop, what artifact a stage owes, who owns an approval, or how an incident reopens the lifecycle."
---

# The Delivery Lifecycle

Code stopped being the bottleneck the moment agents could write it faster than humans could plan, review, and ship around it. The constraint moved outward — to intent, review, and governance — so the job is a **loop**, not a phase sequence: each stage commits a readable artifact that the next stage begins from, and the chain of artifacts *is* the audit trail. Seven stages; `Operate` reopens `Intent`.

> **Override.** A project-level process spec that explicitly supersedes this skill wins.

## The seven stages

| Stage | Commits | Seat | Exit check |
| --- | --- | --- | --- |
| **Intent** | `intent.md` — problem, affected parties, desired outcome, constraints, exclusions, open questions | Originator | acceptance recorded |
| **Spec** | `spec.md` + ADRs — requirements, design, risks, contradictions, unresolved decisions | Steward / Architect | spec accepted; an ADR per hard-to-reverse choice |
| **Plan** | `PLAN.md` + `STATUS.md` — work packages, `DONE_WHEN`, ledger | Steward | every `WPn` names its files and its verify command |
| **Build** | diff + tests | Implementer | L1 green; a failing regression test precedes a fix |
| **Test** | evidence (L1/L2/L3) + review findings | Verifier | evidence audit passes; verdict issued |
| **Release** | release record + `AUTH:` | Approver | explicit human authorization for the outward step |
| **Operate** | incident record -> new `intent.md` | Operator | the loop reopens |

A stage exits only on its check. "The agent finished" is not an exit; the artifact and its check are. Artifact shapes are owned by [artifacts](../artifacts/SKILL.md); this skill owns the stage map.

## It is a loop, not a waterfall

Phase-gated delivery was a response to a bottleneck (hand-written code) that no longer exists; keeping the gates after removing the bottleneck leaves planning, review, and release running at human speed while build collapses to hours. So stages may be **re-entered**, and two back-edges are canonical:

- **`Test -> Build`** — a refuted verdict returns to the implementer with findings, not a flag. This is the ordinary review cycle, bounded by the 3-failed-cycles rule ([verification](../verification/SKILL.md)).
- **`Operate -> Intent`** — an anomaly observed in production becomes a *new* `intent.md`, and the lifecycle runs again. Maintenance is not a terminal stage; it is the loop closing.

A stage may be skipped, but only by naming why in the artifact that follows — a hotfix that never had a spec says so in its incident record. Skipping silently is the failure.

## The seats

Seven seats, not seven people — one agent or person may hold several at once, and small jobs compress them:

- **Originator** — files the intent; owns the problem statement and its acceptance.
- **Steward** — owns the spec and the domain language; keeps `CONTEXT.md` honest ([domain-modeling](../domain-modeling/SKILL.md)).
- **Architect** — reviews higher-risk design; the seat the ADR trigger routes to ([solution-architecture](../solution-architecture/SKILL.md)).
- **Implementer** — executes the plan; the agent at the keyboard.
- **Verifier** — re-derives the work against anchors in a **fresh context**; judges, never writes.
- **Approver** — the human gate on outward, destructive, or release steps; the `AUTH:` quote is theirs.
- **Operator** — maintains the running system, triages anomalies, reopens the loop.

Two constraints never bend, however the seats collapse: **the Implementer never approves its own work**, and **the Verifier is independent of what it judges** — a different context, not the author's memory of writing it.

Org-specific machinery collapses into these seats rather than adding more: a release manager is the Approver, an auditor is a Verifier, on-call is the Operator, a product or policy owner is a Steward. Adding a seat duplicating an existing one is the enterprise-ceremony failure this cast exists to prevent.

## Human judgment concentrates at the seams

Implementation is the agent's; approval is not. Every artifact requiring judgment — accepted intent, agreed spec, authorized release — stays human-accountable, and the audit trail is those artifacts in the repository, not a narration about them. Policies are applied *while* artifacts are produced, not discovered in a later review; a policy that must always hold is backed by a deterministic gate rather than by an instruction to remember it. Automation stops at the production gate — approval happens above that boundary.

## Where verification and evals attach

Every stage's exit is a verification event: the three layers (L1 static / L2 runtime / L3 end-to-end), the evidence audit, and the mutation probe live in [verification](../verification/SKILL.md). Distinct from that, the lifecycle itself is configuration an agent executes, so it is regression-tested like production code: the [evals](../evals/SKILL.md) suite runs realistic tasks against the manifesto and skills and blocks a change that lowers the pass rate. Evals test *the process*; verification tests *a unit of work*.

## Within a stage, the execution graph

The lifecycle says *which stage and what it commits*; it does not say how a stage's work is shaped inside. That is the execution graph — nodes, typed edges, caps, shapes, and the minimal-harness ladder that enters at the least agency that closes on evidence ([graph-engineering](../graph-engineering/SKILL.md)). A stage is a container of one or more graphs; the two compose, and neither replaces the other.

## Common mistakes

| Mistake | Fix |
| --- | --- |
| Running the stages as a waterfall | Re-enter on evidence; `Test -> Build` and `Operate -> Intent` are canonical back-edges |
| Skipping a stage silently | Name the skip in the artifact that follows |
| Exiting a stage on "the agent finished" | Exit on the stage's check — the artifact plus its evidence |
| The implementer approving its own work | Split the seats; approval is a different actor from authorship |
| Verifying in the author's context | Re-derive in a fresh context; a report is testimony, not evidence |
| Adding a seat for every org role | Collapse into the seven; a duplicated seat is ceremony |
| Treating evals as verification | Evals test the process across runs; verification tests one unit of work |

## Cross-references

- [artifacts](../artifacts/SKILL.md) the deterministic shapes each stage commits: `intent`, `spec`, `PLAN.md`, the records.
- [verification](../verification/SKILL.md) the evidence standard every stage exit owes.
- [evals](../evals/SKILL.md) the harness regression suite that gates changes to the process itself.
- [graph-engineering](../graph-engineering/SKILL.md) how work is shaped *inside* a stage.
- [craft](../craft/SKILL.md) the artifact gates (`INTENT:` / `TWINS:` / `AUTH:` / `PENDING:`) that surface at stage seams.
- [wayfinder](../wayfinder/SKILL.md) when the effort outgrows one session, the lifecycle runs across a map of decision tickets.

Distilled from Anthropic's *AI-native SDLC playbook* as method: the non-linear artifact-driven loop, the artifact chain as audit trail, human judgment at the approval seams, and evals as a standing regression control. The org-specific apparatus and host product mechanisms are deliberately not adopted; the seats are the collapsible, host-agnostic form.
