---
name: graph-engineering
description: "The doctrine's execution-graph grammar: nodes, six execution edge types, caps, anchor routing, knowledge edge types, the four shapes (linear, staged, fan-out, graph) with the concision ladder, the minimal-harness ladder (prompt or fixed workflow before an agent loop), fan-out's two rationales (sectioning vs. voting), tool-surface (ACI) design, three-graph organization (task, coordination, state), query routing by question type, and cost-per-successful-completion discipline. Use when designing or reviewing how a job executes — choosing between shapes, entering at the least agency that works, typing edges and routes, deciding when parallel steps beat a sequence, or costing feedback cycles."
---

# Graph Engineering

The grammar of the execution graph (§4.2) — the doctrine's canonical language for how work is shaped *inside* a lifecycle stage. Hosts express graphs through different mechanisms (spawns, parallel workers, scripted pipelines); enabling them is host configuration, out of doctrine scope. This skill governs the shape: nodes, edges, caps, anchors, and the cost of each.

> **Override.** A project-level orchestration spec that explicitly supersedes this skill wins.

## Nodes

A node is a bounded step that **closes on evidence**: command + exit code + output, or a resolved decision with its source. A node whose exit condition is "I feel done" is not a node — it is where a run goes to lie. THINK / ACT / PROVE / GROW are role-nodes most jobs need; a specific job's nodes name its own units ("baseline captured", "module migrated", "probe failed and reverted").

## The six execution edges

The edge type is the knowledge: an untyped edge ("goes next") is a missing decision — type it or delete it.

| Edge | Means |
| --- | --- |
| `PRODUCES` | this hands its output to that (plan -> unit; measurement -> verdict) |
| `VERIFIES` | that re-derives this against an anchor (probe -> change; judge -> report) |
| `ROUTES` | a conditional branch — diamond, named conditions, exactly one edge taken |
| `RETURNS` | feedback carrying a payload (findings, not a bare "failed") along a named back-path |
| `FAN_OUT` | this splits into concurrent branches (per-lens reviews, per-file migrations) |
| `JOINS` | concurrent branches re-synchronize here (synthesis, aggregate verdict) |

## Caps

Every cycle is bounded by a named cap, inherited from verification's hard bound: 3 failed cycles on one issue. A `RETURNS` edge without a cap is an unbounded loop wearing a graph costume — price the all-reviewers-fail path before building it.

## Anchors

An **anchor** is a fixed external node the machinery may read but never rewrite: a spec clause, the user's own words, a red test, captured command output. Every `VERIFIES` edge must terminate in an anchor; work citing only its own outputs is a loop validating itself — an echo chamber with more nodes. The authority rank (§0) is the anchor ordering. **Goodhart's law** is the standing threat: a system drilled on its own measurements optimizes the measurement, not the goal. Two structural guards follow:

- **Owned references.** A fast check may not set its own target: DONE_WHEN comes from the prompt or spec, not from what the diff made easy to assert. Pair every metric with its counter-metric (tests green *and* mutation probe catches).
- **Read-only anchors.** An anchor that a later step may rewrite is not an anchor. If the target must change, that is a decision routed to the anchor's owner (the spec's author, the user) — never a silent edit at the step that benefits from it.

## The four shapes

Concurrency x complexity — enter at the smallest shape that works; climb only on a measured bottleneck. The concision ladder binds: less mechanism wins.

| Complexity ↓ · Concurrency → | Low | High |
| --- | --- | --- |
| Simple | **linear** — THINK -> ACT -> PROVE, no branch | **fan-out** — independent jobs at once; within one turn this is §4.2 batching |
| Complex | **staged** — the sequence with checkpoints between stages | **graph** — concurrent branches, conditional routing, designed back-edges |

Climb signals: three or more concurrent verification steps **and** branching decision routing. Descend signals: sequential steps, same-file edits, heavy inter-step dependencies. Step down the moment the reason for the climb disappears.

## Enter at the least-agency rung

Three rungs, least first: a **prompt or retrieval**, a **fixed workflow** (linear / staged, routes designed ahead of time), an **agent loop** (routes chosen at run time). Enter at the lowest rung that closes on evidence — an agent loop buys adaptability only where the path genuinely cannot be known in advance, and costs a decision it must re-make every turn. Build the smallest loop that closes end-to-end first, then add a control only on an observed failure (the Kirby Effect at harness level). Full ladder, walking-skeleton build order, and the pattern catalogue: [harness-design](references/harness-design.md).

## Fan-out has two rationales

A `FAN_OUT` edge carries one of two intents: **sectioning** splits the job into independent subtasks (per-file migrations, per-lens reviews), while **voting** runs the same task N times and aggregates for confidence. Sectioning pays on disjoint parts; voting pays only when the runs are plausibly **decorrelated** — correlated runs fail together and the premium becomes a tax (teamwork's correlated-lens hazard). Never cite "N runs" as free confidence without saying why they decorrelate: [harness-design](references/harness-design.md).

## Design the tool surface

Tool definitions are as load-bearing as the prompt: document each for the model (what it does, when to use it, input format, returned fields, error behavior, and how it differs from the similar tool), poka-yoke the arguments so misuse is hard to express, and scope the surface to the job — a narrower tool set means less confusion and less injection exposure. When traces show misuse, fix the interface before the instruction: [harness-design](references/harness-design.md).

## Three graphs over one job

Any job above trivial has three simultaneous graph structures; design them deliberately instead of letting them accrete:

- **Task graph (what):** units, dependencies, DONE_WHEN per unit. The wayfinder map is its cross-session form; the team ledger its cross-agent form.
- **Coordination graph (who):** solo -> delegation -> team, one rung per topology; teamwork owns the rungs and their law.
- **State graph (how it operates):** nodes read and write the repository as system of record — checkpoints, evidence pointers, retros; §8 is its law.

## Knowledge edges

The same typed-edge discipline records what was learned, not only what runs. Decision and knowledge graphs use their own six types: `SUPERSEDES` (this replaces that), `DEPENDS_ON` (breaking that breaks this), `DECIDED_BY` (this exists because that was chosen), `CAUSED` (this created that), `IMPLEMENTS` (this realizes that), `REFERENCES` (this mentions that). An untyped edge ("relates to") is a missing decision — type it or delete it. Auto-derived edges carry creation and verification dates: facts expire, they do not die; a graph without dates routes on stale knowledge.

## The five-stage method

Reshaping an existing loop-built job into a graph is itself a graph-shaped job; run it in five stages: **audit** the current execution (where are the cycles, which routes repeat, what evidence does each step close on), **identify** the nodes worth making explicit (bounded, evidence-closing, on a measured bottleneck), **design** edges and caps (typed per the tables above; every `RETURNS` payload-carrying and capped), **implement** at the smallest shape that works, and **type** the knowledge left behind (`SUPERSEDES`/`DEPENDS_ON`/... with dates) so the next audit starts from a map, not folklore.

## Route the query by its type

Reading a knowledge graph obeys the same routing discipline as building a work graph: a lookup ("what does X do?") rides similarity search — cheaper than traversal; a multi-hop question ("why did X change, and what is downstream of it?") rides graph traversal — similarity finds what sounds like the question, traversal finds what is connected to the answer. Simple lookups, high-volume retrieval, and low entity resolution are where graphs lose. Keep both: a cheap index for the lookups, the typed edges for the multi-hop path.

## The cost gate

Fan-out re-pays its token cost on every failed cycle, so it amortizes only when most branches pass: the industry guide claims a ~50% per-cycle pass-rate breakeven, and ~3x tokens for the same result at ~30%. Treat those as arithmetic to re-derive on your own runs, not constants to cite. Judge by **cost per successful completion**, never wall-clock alone. A shape that loses the cost gate is stepped back down the ladder.

## Common mistakes

| Mistake | Fix |
| --- | --- |
| A node that closes on narration | Re-derive its exit as evidence, or split it until one node = one proof |
| Bare edges ("goes next") | Name the relationship from the edge table, or delete the edge |
| `RETURNS` with no payload or no cap | Route findings, not flags; bind the cycle count |
| Citing the guide's benchmarks as expected gains | Adopt the method; re-measure locally before claiming any number |
| Trusting an auto-generated graph | Entity resolution compounds per hop — dedupe and validate |
| Traversal where a lookup would do | Route by question type: similarity answers "what", traversal answers "why and what downstream" |
| An anchor a step can rewrite | Route target changes to the anchor's owner; never silently |
| Graph where a sequence or a turn's batching would do | Enter at the smallest shape; graph only what survives the climb signals |
| Agent loop where a workflow or prompt would do | Enter at the least-agency rung; climb on a measured need |
| N identical runs cited as confidence | Voting pays only on decorrelated runs; say why they decorrelate |
| Tool definition written for the implementer | Document it for the model; iterate on observed misuse, fixing the interface first |

## Cross-references

- [harness-design](references/harness-design.md) the minimal-harness ladder, the pattern catalogue mapped onto the grammar, voting vs. sectioning, and tool-surface (ACI) design.
- [lifecycle](../lifecycle/SKILL.md) owns *which stage and what it commits*; this skill owns how work is shaped inside a stage. A stage contains one or more graphs — the two compose.
- [teamwork](../teamwork/SKILL.md) owns the coordination graph: this skill decides topology (shapes, edges, gates); teamwork's ladder, ledger, and adversarial roles govern conduct at each node.
- [verification](../verification/SKILL.md) owns the evidence standard at every node and the caps that bound every `RETURNS` edge; its [flowcharts](../verification/references/flowcharts.md) render the doctrine's own execution graph.
- [wayfinder](../wayfinder/SKILL.md) the task graph persisted across sessions: when the graph outgrows one session, it becomes a map of decision tickets, not a longer diagram.
- [performance](../performance/SKILL.md) owns the measurement: the cost gate is the measure-first cycle applied to shapes; cost per successful completion is the benchmark it judges by.
- [system-diagramming](../system-diagramming/SKILL.md) renders a designed graph when it must be read by humans.

Distilled from flowtivity's graph-engineering guide (2026) and Eigent's graph-engineering essays; their benchmark figures are deliberately not adopted — measure locally.
