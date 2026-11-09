# Runtime State

> Load on demand from [execution](../SKILL.md): the state graph — what a run records, who may commit it, how a failure is localized, and where recovery resumes. Structure only; the repository stays the system of record.

## Recording

State is what a fresh context needs to resume deterministically, not the transcript. Record the ledger fields and nothing else: unit, status, evidence pointer, owner, open edges, gates owed, scope.

Reliable state has four properties, and each one is a decision rather than a default:

- **Structured representation.** Fields in a file, never a prose narrative that only the writing context can parse.
- **Governed updation.** A state change is proposed, validated, then committed — see the transition cycle below.
- **Scoped visibility.** A role reads the projection it needs. Every worker reading the whole ledger is a window cost with no decision behind it.
- **Consistency management.** One writer per file. The lead owns the ledger; workers report and never write it. Two writers on one state file lose updates with no error.

History is append-only and summaries derive from it: commit transitions to a log and regenerate summaries from it. A summary edited in place loses provenance, and the next run cannot tell which claim was ever checked.

## The governed transition

Every state change — a unit opened, a claim made, a unit closed, a fault attributed — moves through the same cycle:

1. **Propose.** The proposer states the change and the check that will prove it. A proposal is a candidate, not a fact.
2. **Validate.** Four things are checked before the write commits:
   - **Schema** — the change has the fields the ledger defines, in the fields it belongs in.
   - **Permission** — the proposer may write this field, in this scope, at this level.
   - **Invariant** — the change does not break a rule the state must keep (a task with an open upstream edge is not claimable; a unit is not closed without its evidence).
   - **Conflict** — the change does not contradict the current state; a stale proposal loses to the newer committed one rather than overwriting it.
3. **Commit.** Only what passed is committed, and every committed transition carries its **provenance**: who proposed it, which check proved it, when, and against which prior state.

**Tentative is not committed belief.** A write no check has confirmed is marked tentative and stays tentative — it is never quoted downstream as fact, and a reader cannot mistake a hypothesis for a record. A committed belief that later proves wrong is **retracted and repaired**, with the retraction itself recorded: leaving it in place and letting it spread is how one wrong claim becomes the next run's premise.

## Fault localization

Recorded dependencies narrow the search for a cause; they never prove one. Temporal adjacency and a graph edge are correlation, and the fault usually surfaces downstream of where it started. So the cause is a **hypothesis, tested against externally observable evidence outside the failing path**: re-run the check, read the upstream output, diff the file, observe the resource.

Two rules follow:

- **Test outside the failing path.** Evidence produced by the path that already failed is downstream of the cause and cannot discriminate between candidates.
- **Record the diagnosis and its evidence.** The hypothesis, the evidence that tested it, and the verdict are written down, so recovery builds on the diagnosis instead of restarting the hunt — and so the next occurrence starts from a recorded answer rather than a fresh guess.

Keep what attribution needs, since final output alone cannot support it: the actor, the transition, the dependency edge, and the validation evidence at each step.

## Recovery

Name the recovery boundary before repairing — the last state whose evidence still holds — and resume from there instead of restarting the run. Sort the work either side of it:

- **Replayable.** Internal state — a pure computation, a local edit, a test run — replays: re-execute it.
- **Outward.** An effect on a system outside the repository — a push, a post, a deploy, a paid call — cannot be replayed, only compensated, and the compensation itself needs `AUTH:`. Wait for the resulting state to be recorded before continuing: an outward effect whose outcome is unknown leaves the state graph inconsistent, and everything downstream inherits the ambiguity.

Record the boundary, the corrective action, and the resulting state. A recovery with no boundary written down is an untracked restart wearing the word "fix".

## Adaptation is not evolution

Adapting inside a run — retry, reroute, re-split a unit — changes one trajectory. It costs nothing and leaves nothing behind, so it is the right response to a one-off.

**Evolution** changes the machinery future runs execute, and it is governed, because it outlives the run that proposed it:

1. **Credit assignment** — which recorded failure earns the change, and how much credit each candidate gets.
2. **Mutation** — the structural change itself: a new edge type, a new cap, a new capability relation, a new gate.
3. **Validation** — the change is run against the recorded failures; it must fail on the old evidence and pass on good runs.
4. **Commit or rollback** — committed with a version, or rolled back to the prior state. An unvalidated structural edit is churn with a diagram.

Structural changes to one graph move the others: reshaping the task graph changes the capabilities the units need, which changes the team topology, which changes what the ledger must record. A structural change therefore **names the other views it touches**, and the coupled change is validated together — a change that invalidates another graph without updating it is worse than no change. Validate the coupled change and check that it generalizes to the recorded failures.

## Cross-references

- [execution](../SKILL.md) the grammar and the three coupled views this state graph completes.
- [graphs](graphs.md) the task and coordination views the state graph is the join point for, and the scoring dimensions.
- the `quality` skill's [evolution](../../quality/references/evolution.md) — the governed change cycle at the level of the machinery itself.
- the verification standard — what counts as the evidence a transition commits against.
