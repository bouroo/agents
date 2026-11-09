# The Three Views

> Load on demand from [execution](../SKILL.md): the task, coordination, and state graphs worked out as one structure — what a unit is, who holds it, what flows between holders, and how the run is scored. Read it when a job spans several workers and the three views have to be made explicit, or when a finished run must be scored for effectiveness, efficiency, robustness, structural fidelity, operational correctness, and evolution governance.

## Why three views

A job beyond the trivial needs three answers kept in one structure: **what** is being done, **who** is doing it, and **how it actually went**. The views are coupled, not a list — a unit's DONE_WHEN names the check that closes it, that check names the capability that must hold it, the capability names the worker who carries it, and the state graph records what happened there. Change any one and the other two need re-reading.

Adding workers to a job that has no three views buys nothing. The cost goes up, the structure stays invisible, and the failures surface exactly where they did before — in the handoffs. Organize first, then add capacity.

## The task graph (what)

The goal decomposes into explicit subgoals joined by dependency edges; the workflow compiles into executable operations; intermediate results refine the decomposition.

- **Unit** — a bounded piece of work with one DONE_WHEN, stated as an observable condition plus the check that proves it. The check is external to the unit's own output: a check that the unit also writes proves whatever it likes.
- **Dependency edge** — typed, and typed because the type decides what blocks what: `DEPENDS_ON` (blocks), `PRODUCES` (feeds forward), `VERIFIES` (re-derives against an anchor), `RETURNS` (feedback with a payload), `ROUTES` (a named condition choosing one successor).
- **Dynamic refinement** — when a unit returns, its evidence may make the next unit unnecessary, change its scope, or split it. The plan is compiled from the goal, then re-compiled from intermediate results. A plan that survives contact with the first result unchanged was never refined, only written down.
- **Anchor** — the fixed external node every `VERIFIES` edge terminates in: a spec clause, the user's words, a failing test, captured output.

The task graph is what crosses a session boundary (the wayfinder map) and what crosses agents (the team ledger). One writer per ledger, so no two agents hold divergent copies of the same graph.

## The coordination graph (who)

Three views of the same coordination graph, each answering a different question.

### Capability view

What each worker **can** do and **holds**. The relations are explicit, not assumed from the worker's name:

| Relation | Meaning |
| --- | --- |
| Skills | the techniques the worker can apply |
| Tools | the interfaces the worker may call |
| Resources | the artifacts, quotas, environments, or services it holds |
| Permissions | the actions it is authorized to take, and the scope of each |
| Reliability | what the worker is observed to do well, on what kind of unit |

Two properties follow, and both are the point: a unit can be **held** by any worker holding the capability, and a worker that **loses** a resource — a revoked permission, an unavailable tool, a consumed quota — leaves its units reassignable rather than stuck. Routing runs by capability, not by name. "The one who did it last time" is an assignment that survives only until that worker is unavailable.

### Team view

Who is accountable for what, and who supervises whom. One lead owns decomposition, assignment, synthesis, and monitoring; workers own units; workers do not nest. Assignment edges carry the brief; supervision edges carry the check-in; verification edges carry the evidence.

### Communication view

Runtime information flow, kept separate from the stable team structure — the team structure is fixed at design time, the communication graph is what actually happened at run time.

- **Exchange point** — where in the execution an exchange happens: at a handoff, at a fan-out join, at a gate, at a clarification stop. An exchange with no point in the execution has no consequence and is cost without information.
- **What the exchange changes** — the recipient's permission to act afterwards, the edge it opens or closes, the claim it licenses. If the answer is "nothing", the relation carries no decision and gets removed. More connections do not improve collaboration by default; a graph that connects everyone to everyone buys context cost and no coordination.
- **Humans as participants** — a human appears in the view with explicit edges: **clarification** (an answer that unblocks a unit), **feedback** (a correction that redirects the work), **approval** (a sign-off that closes a gate), **escalation** (a blocked unit handed up). The human is a participant in the flow, not only the final evaluator standing outside it.

## The state graph (how)

What actually happened, recorded rather than remembered. Its four properties — structured representation, governed updation, scoped visibility, consistency management — and the transition cycle (propose, validate, commit) are owned by [runtime-state](runtime-state.md); this file states why the three views close together.

State is the join point of the other two graphs: the task graph says what should have happened, the coordination graph says who should have done it, and the state graph says what did. A gap between the three is the finding — a unit closed without its check, a worker committed a result no capability covered, an exchange happened that no unit recorded.

## Scoring a run

End-task success is one dimension, not a verdict. Report six:

| Dimension | Question |
| --- | --- |
| Effectiveness | did it finish the job? |
| Efficiency | cost per successful completion, not wall-clock alone |
| Robustness | does it survive a failed unit, a lost capability, a contradictory finding? |
| Structural fidelity | does the structure match the work — units at the right granularity, dependencies where the work really couples? |
| Operational correctness | were the graph operations executed as intended — typed edges, named caps, exclusive ownership, evidence gates? |
| Evolution governance | are structural changes traceable and controllable — credit assignment, validation, commit or rollback? |

The last two are what separate a working system from a lucky one. A run that succeeded with a coarse task graph, an unrouted fan-out, and a claim closed on testimony has high effectiveness and low structural fidelity and operational correctness — the next run will not repeat the success.

## Ablation: separating the structure from the model

A better model produces the same numbers as a better structure. To tell them apart, hold the budget fixed and ablate the structural change: run the job with the structure, and run it again without it at equal cost — same model, same token budget, same task. Attribute only the difference the structure explains.

- If the structural version wins at equal cost, the structure is carrying the gain.
- If both versions move together with the model, the model is carrying it.
- If the structural version wins only with a larger budget, the win is a budget win, and the cost per successful completion says so.

Ablate one structural element at a time where the graph is large: the typed edges, the capability routing, the communication view, the evidence gates. Each ablation names which dimension it moves.

## Cross-references

- [execution](../SKILL.md) the grammar and the faces these views belong to.
- [runtime-state](runtime-state.md) the governed transition cycle, provenance, fault localization, and recovery boundary that make the state graph trustworthy.
- [topologies](topologies.md) the cost arithmetic behind the shapes these views pick.
- the verification standard in the `quality` skill — what counts as evidence and what bounds every `RETURNS`.
