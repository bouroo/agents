---
name: delivery
description: "Delivery doctrine for plan-shaped agent work, in four faces. Lifecycle: the seven stages (intent, spec, plan, build, test, release, operate), their canonical back-edges, the collapsible seven seats, and the handoff, approval, and reopen rules between them. Artifacts: the deterministic shapes intent.md, spec.md, and PLAN.md with its sibling STATUS.md ledger, WPn work packages, a DONE_WHEN checklist of executable checks, and a grounded mermaid diagram. Grilling: plan-first interviews that walk a design tree in numbered frontier rounds, facts looked up by the agent and decisions put to the user. Wayfinder: a map of decision tickets (label wayfinder:map) resolved one per session until the fog clears. Use when deciding where work belongs in the delivery loop, what artifact a stage owes, who owns an approval, how to interview for a decision, or how to chart an effort too big for one session or shared across agents."
---

# Delivery

Four faces of one doctrine for plan-shaped agent work, merged because they are one loop, not four topics: [Lifecycle](#lifecycle) names where work belongs and what each stage commits; [Artifacts](#artifacts) fixes the deterministic shapes those stages write; [Grilling](#grilling) settles a decision in one session; [Wayfinder](#wayfinder) runs that same interview across sessions as a map when the effort outgrows one.

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

An artifact an execution session must **resume from** needs a **deterministic shape**: same sections in the same order, same vocabulary for the same things. Plans only humans read may stay prose. Three durable shapes belong to the lifecycle stages — `intent.md` (Intent), `spec.md` (Spec), `PLAN.md` + `STATUS.md` (Plan).

`<plans-root>/<feature-slug>/` (kebab-case) holds the chain: `PLAN.md`, the sibling `STATUS.md` ledger, and `retro.md` when done; render artifacts live in `<slug>/wiki/`. The filename is invariant — `PLAN.md`, never `plan.md` or `PLAN-<topic>.md`. The plans-root carries a `README.md` index, one row per plan. `intent.md` and `spec.md` live beside the code they govern (an `intent/` directory) or inside the effort directory, each a single named, version-controlled file.

**intent.md** — the originator's own words, problem as experienced not diagnosed:

```markdown
# <Title> — intent
Date: YYYY-MM-DD · Status: DRAFT | ACCEPTED · Originator: <who>
## Problem
## Affected parties
## Desired outcome
## Constraints
## Exclusions
## Open questions
```

**Exclusions** is load-bearing: what this does *not* attempt is the boundary the spec later respects. Unresolved **Open questions** stay listed rather than silently answered.

**spec.md** — requirements and design produced together, not as analyst/designer handoffs:

```markdown
# <Title> — spec
Date: YYYY-MM-DD · Status: DRAFT | ACCEPTED · Steward: <who>
## Requirements
## Design
## Risks and contradictions
## Unresolved decisions
```

**Risks and contradictions** names where the intent fights itself. A spec that pretends to have decided everything has hidden the decisions, not made them. A hard-to-reverse choice graduates to an ADR.

**PLAN.md** — the deterministic execution shape:

```markdown
# <Title> — plan
Date: YYYY-MM-DD · Status: DRAFT | APPROVED | IN PROGRESS | DONE · Scope: <repos touched>
## INTENT
## Current state (verified facts)
## Decisions (user-confirmed YYYY-MM-DD)
## Design
## Work packages
## Risks
## DONE_WHEN (executable evidence)
## PENDING (prescribed but untaken)
```

**One vocabulary, everywhere**: work packages are **`WPn`** (WP0 allowed as baseline/migration), never "phase", "step", or bare `Pn`. Section by section: **INTENT** is the §0 gate as prose — what the code will do and its driver; if code, check, and spec disagree, the disagreement is the finding, resolved by anchor rank before any work package. **Current state** is the repository as observed, every claim anchored (file:line, command output). **Decisions** are numbered, dated, naming who confirmed them. **Design** leads with one `mermaid` diagram grounded in facts already recorded. **Work packages** run in execution order, `### WPn — <repo/slice>: <deliverable>`, each naming files to touch, mechanics, and its own verify command; one WP is one reviewable unit. **Risks** include accepted risks and why. **DONE_WHEN** is the anchor every execution session cites — one checkbox per terminal check, naming command plus expected observable; a check that cannot name its command does not belong. **PENDING** lists follow-ups deliberately not taken (write "None recorded." if empty); an unlisted pending action reads as fraud.

**STATUS.md** is the sibling ledger, not a section: the plan stays a planning artifact, and execution progress never leaks into it. Newest on top, cite-don't-narrate: what landed where (branch/commit/tag, merged or not), what is blocked and on what. Probe before writing it — run the cheapest observable check rather than trusting the transcript — and name the branch, because working-tree evidence can contradict the default branch.

Drift sweep for an existing plan: heading order matches the fixed sequence; one status line under the title; every in-text label resolves to a heading; `DONE_WHEN` count matches the checkbox count; diagrams parse. Mechanical checks: `grep -n '^## ' <slug>/PLAN.md` for order, `grep -rn 'Phase\|phase\|Backlog\|plan\.md\|Execution status' <slug>/PLAN.md` for orphan tokens (expect zero), `grep -c '^\- \[ \]' <slug>/PLAN.md` so every `DONE_WHEN` item is a check.

## Grilling

Interview the user until you reach shared understanding of a plan, decision, or idea — the technique behind the manifesto's plan-first intake route. Ambiguity drains through conversation, never through guessing. Map the decision space as a **design tree**: every decision branches into the decisions that hang off it; settling a node unblocks its children.

Work the tree in **rounds**. The **frontier** is every question whose prerequisites are settled — what you can ask now without guessing at answers you have not heard. Ask the whole frontier in one round: number each question, give your recommended answer, then stop and wait. A question depending on one still open belongs to a later round; each round's answers push the frontier outward, so recompute it and ask the next.

```markdown
❓ **Q1** - **<question title>**: <question body; may offer choices>

➡️ <recommended answer>

---

❓ **Q2** - **<question title>**: <question body>

➡️ <recommended answer>
```

Facts are yours, decisions are theirs. Finding a _fact_ is your job: when a frontier question needs one from the environment, dispatch a sub-agent to look it up rather than asking the user. Do not block the round on it — only questions downstream of the lookup wait; ask the rest now. Put each _decision_ to the user in the round and wait: a decision made without the user is fabricated, not resolved.

Completion: the frontier is empty when every branch is visited and nothing is left silently assumed. Then produce the plan with one recommendation and **STOP** for approval — never act on the interview's outcome on your own authority. The `intent` / `spec` / `PLAN.md` shapes carry the approval. The grilling method is adapted from [mattpocock/skills](https://github.com/mattpocock/skills) (`grilling`, MIT).

## Wayfinder

A loose idea arrives, too big for one agent session, wrapped in fog: the way to the destination is not visible yet. Wayfinding is finding the way, not charging at it. Chart the effort as a **map** on the issue tracker, then work its **decision tickets** — questions whose resolution is a decision, not build slices — until the route is clear. Naming the destination (a spec to hand off, decisions locked before build planning, or a change made in place) is the first act of charting, because it shapes every ticket.

Wayfinder is **planning** by default: each ticket resolves a decision, and the map is done when the way is clear; the urge to just do the work usually means you have reached the edge of the map and it is time to hand off. An effort may override this in its **Notes** and carry execution into the map.

The map is a single issue labelled **`wayfinder:map`** — the canonical artifact, with tickets as child issues. It is an **index, not a store**: it lists decisions made and points at the tickets holding the detail, so a decision lives in exactly one place and the map never restates it, only gists it with a link. Every ticket is referred to **by name** (its title), never a bare id or number; the id rides inside the name link. Blocking uses the tracker's native dependency relationship when it has one; fall back to `Blocked-by:` lines only when it does not. Where map, tickets, and blocking live is tracker-specific; if none was provided, default to a local markdown tracker (one file per issue, labels in frontmatter) and say so.

The map body holds: **Destination** (the end of the map, one or two lines, oriented against first); **Notes**; **Decisions so far** (index: one line per closed ticket); **Not yet specified** (the fog); **Out of scope** (work consciously ruled out, closed, never graduates). Open tickets are found by query, not listed.

Each ticket is a child issue whose body is a question sized for one session, carrying a `wayfinder:<type>` label. A session **claims** a ticket by self-assigning **first**, before any work — an open, unassigned ticket is unclaimed, so concurrent sessions skip it. A ticket is **unblocked** when every ticket blocking it is closed; the **frontier** is the open, unblocked, unclaimed children — the edge of the known. The answer is recorded on resolution, never in the body.

Ticket types: **Research** (AFK) reads docs or APIs to surface a fact a decision waits on, fanned out one scoped worker per ticket. **Prototype** (HITL) resolves a "how should it look or behave" question by raising fidelity to a rough, concrete artifact the human reacts to. **Grilling** (HITL) is conversation to pin down a decision — the default type whenever the open question is about intent, preference, or scope. **Task** (AFK) does work that must happen so a decision can be made, and earns its place only by unblocking one. A HITL ticket resolves only through live exchange; the agent never stands in for the human's side, and answering your own grilling questions breaks the same gate as self-granted `AUTH:`.

**Fog of war**: the map is deliberately incomplete — don't chart what you can't yet see. Resolving a ticket clears fog ahead of it, graduating what is now specifiable into fresh tickets, one at a time, never in advance. **Fog or ticket?** Test whether you can state the question sharply now, not whether you can answer it: sharp-but-blocked is a ticket, unstateable is fog. Fog gathers only toward the destination; work beyond it is **out of scope**, which never graduates and returns only if the destination is redrawn.

Invocation, resolver half: **load** the low-resolution map; **choose** a ticket (the named one, else the first frontier ticket) and **claim** it; **resolve** it, defaulting to a grilling conversation when in doubt; **record** the resolution (comment, close, append the one-line gist); **update the map's edges** (create newly surfaced tickets, graduate fog, rule out of scope, rewire what the decision invalidated); **stop**. Resolve at most **one ticket per session** — research fan-out is the exception — because the map carries the state, so no context has to. Charting, the other half, names the destination, maps the frontier breadth-first, creates the map and its specifiable tickets, fires research fan-outs, and stops; if no fog surfaces, the whole journey fits one session and there is no map to make.

## Common mistakes

| Mistake | Fix |
| --- | --- |
| Running the stages as a waterfall | Re-enter on evidence; `Test -> Build` and `Operate -> Intent` are canonical back-edges |
| Exiting a stage on "the agent finished" | Exit on the stage's check — the artifact plus its evidence |
| The implementer approving its own work | Split the seats; approval is a different actor from authorship |
| Verifying in the author's context | Re-derive in a fresh context; a report is testimony, not evidence |
| Adding a seat for every org role | Collapse into the seven; a duplicated seat is ceremony |
| Treating evals as verification | Evals test the process across runs; verification tests one unit of work |
| Mixing intent, spec, and plan into one document | One artifact per stage; each is a checkpoint the next resumes from |
| A spec with no Unresolved decisions | List what is open; a settled-looking spec hid the decisions |
| Execution progress leaking into PLAN.md | It belongs in the sibling STATUS.md |
| A WP with no verify command | Size it until it names one, or split it |
| A DONE_WHEN item that cannot name its command | Rewrite it as a check, or it is not terminal |
| `Phase` / `step` / bare `Pn` tokens | One vocabulary: `WPn` |
| One question at a time in a grilling round | Ask the whole settled frontier as one numbered round |
| Asking what you could look up | Dispatch a sub-agent for facts; only decisions reach the user |
| Acting when the questions run out | Frontier empty -> one-recommendation plan, then STOP for approval |
| Pre-slicing fog into ticket-sized pieces | Graduate one patch at a time as the frontier reaches it |
| An agent answering its own HITL ticket | Resolve HITL only through live exchange; a self-answer is fabricated |
| Charting past the destination | Rule it out of scope; it returns only if the destination is redrawn |
