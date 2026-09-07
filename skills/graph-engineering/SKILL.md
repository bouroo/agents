---
name: graph-engineering
description: "Graph engineering for agent workflows: the loop-vs-graph decision matrix, the five-stage method (audit, identify, design, implement, type), the canonical 3-5-node topology with explicit edge conditions, six typed edges, and cost-per-successful-completion discipline. Use when a job needs three or more concurrent verification steps or branching decision routing, when a workflow loop shows recurring bottlenecks or retry churn, or when deciding whether parallel steps beat a single loop."
---

# Graph Engineering

An agent job's execution shaped as an explicit graph: nodes (steps) joined by typed, conditional edges (handoffs), independent nodes run concurrently, feedback routed along named paths instead of a flat retry. Hosts express graphs through different mechanisms (team spawns, parallel workers, scripted pipelines); enabling them is host configuration, out of doctrine scope — this skill governs choosing the shape and designing its edges.

**Stance:** a graph is an escalation bought with tokens and coordination, never a prestige move. The single loop of §4 stays the default; reshape a job only when the matrix below says so. The method is distilled from a 2026 industry guide whose benchmark figures are claims — none are adopted as fact; measurement is the only verdict here.

> **Override.** A project-level orchestration spec that explicitly supersedes this skill wins.

## When a graph pays

| Complexity ↓ · Concurrency → | Low | High |
| --- | --- | --- |
| Simple | single loop | parallel loop — independent jobs at once; within one turn this is §4 batching |
| Complex | staged loop — the loop with checkpoints between stages | **graph** — concurrent branches, conditional routing |

Rule of thumb: three or more concurrent verification steps **and** branching decision routing. Below that bar a loop — batched within the turn (§4) — is the least mechanism that works. Sequential steps, same-file edits, and heavy inter-step dependencies are counter-signals: stay on teamwork's lower rungs.

## The five stages

1. **AUDIT** — inventory every workflow the job runs: steps, retry clusters, wall-clock and token cost per task. Artifact: a loop inventory with bottleneck annotations.
2. **IDENTIFY** — steps with no data dependency on each other are parallelization candidates; rank by impact.
3. **DESIGN** — draft the topology: three to five nodes, every edge condition written (what happens when a reviewer fails? where does feedback route?). Canonical shape and worked patterns: [topologies](references/topologies.md).
4. **IMPLEMENT** — build the smallest shape that honors the design; measure wall-clock **and** cost per successful completion against the audited loop.
5. **TYPE** — upgrade bare handoffs to typed edges.

## Typed edges

The edge type is the knowledge: an untyped edge ("relates to") is a missing decision — type it or delete it.

| Edge | Means |
| --- | --- |
| `SUPERSEDES` | this replaces that; the target is no longer current |
| `DEPENDS_ON` | this needs that; breaking the target breaks this |
| `DECIDED_BY` | this exists because that was chosen |
| `CAUSED` | this created that |
| `IMPLEMENTS` | this realizes that |
| `REFERENCES` | this mentions that |

Auto-derived edges carry creation and verification dates — facts expire, they do not die; a graph without dates routes on stale knowledge.

## The cost gate

Parallel fan-out re-pays its token cost on every failed cycle, so it amortizes only when most branches pass: the guide claims a ~50% per-cycle pass-rate breakeven, and ~3x tokens for the same result at ~30%. Treat those as arithmetic to re-derive on your own runs, not constants to cite. Judge by **cost per successful completion**, never wall-clock alone, and price the all-reviewers-fail path before building it — it can cost more than the loop it replaced. A graph that loses the cost gate is stepped back down to a staged loop.

## Common mistakes

| Mistake | Fix |
| --- | --- |
| Engineering a graph the job has not earned | Start at three to five nodes; grow only on a measured bottleneck |
| Bare edges ("relates to") | Name the relationship from the table above, or delete the edge |
| Citing the guide's benchmarks as expected gains | Adopt the method; re-measure locally before claiming any number |
| Trusting an auto-generated graph | Entity resolution compounds per hop (the guide's illustration: 85% per hop ≈ 44% over five) — dedupe and validate |
| An unpriced feedback loop | Cost the all-reviewers-fail path up front; cap it like verification caps retries |
| Edges that never expire | Timestamp creation and last verification; stale edges misroute |
| A graph where §4 batching would do | Batch within the turn first; graph only what survives the matrix |

## Cross-references

- [teamwork](../teamwork/SKILL.md) is the substrate: the graph decides shape (nodes, edges, gates); teamwork's ladder, ledger, and adversarial roles govern conduct at each node.
- [verification](../verification/SKILL.md) bounds every gate: graph routing inherits the loop caps — routing changes where failure goes, never how many retries exist.
- [wayfinder](../wayfinder/SKILL.md) when the graph outgrows one session: persist it as a map of decision tickets, not a longer diagram.
- [performance](../performance/SKILL.md) owns the measurement: AUDIT is the measure-first cycle applied to workflows; cost per successful completion is the benchmark it judges by.
- [system-diagramming](../system-diagramming/SKILL.md) renders the designed topology when it must be read by humans.

Distilled from flowtivity's graph-engineering guide (2026); its benchmark figures are deliberately not adopted — measure locally.
