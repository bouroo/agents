# Runtime State

> Load on demand from [execution](../SKILL.md): the state graph — what a run records, who may commit it, how a failure is localized, and where recovery resumes. Structure only; the repository stays the system of record.

## Recording

State is what a fresh context needs to resume deterministically, not the transcript. Record the ledger fields and nothing else: unit, status, evidence pointer, owner, open edges, gates owed, scope.

- **Structured.** Fields in a file, never a prose narrative that only the writing context can parse.
- **Governed update.** A state change is proposed, validated against the check that proves it, then committed. A finding no check has confirmed is written as tentative, so a later reader cannot mistake a hypothesis for a fact.
- **Scoped visibility.** A role reads the projection it needs. Every worker reading the whole ledger is a window cost with no decision behind it.
- **One writer per file.** The lead owns the ledger; workers report and never write it. Two writers on one state file lose updates with no error.
- **Append-only history, derived views.** Commit transitions to a log and regenerate summaries from it. A summary edited in place loses provenance, and the next run cannot tell which claim was ever checked.

## Fault localization

Recorded dependencies narrow the search for a cause; they never prove one. Temporal adjacency and a graph edge are correlation, and the fault usually surfaces downstream of where it started. So the cause is a hypothesis, tested against evidence outside the failing path: re-run the check, read the upstream output, diff the file.

Keep what attribution needs, since final output alone cannot support it: the actor, the transition, the dependency edge, and the validation evidence at each step.

## Recovery

Name the recovery boundary before repairing — the last state whose evidence still holds — and resume from there instead of restarting the run. Sort the work either side of it:

- **Replayable.** A pure computation, a local edit, a test run: re-execute it.
- **Outward.** An effect on a system outside the repository — a push, a post, a deploy, a paid call: it cannot be replayed, only compensated or reported, and re-running it is a new outward effect that needs `AUTH:`.

Record the boundary, the corrective action, and the resulting state. A recovery with no boundary written down is an untracked restart wearing the word "fix".

## Adaptation is not evolution

Adapting inside a run — retry, reroute, re-split a unit — changes one trajectory. Evolution changes the machinery future runs execute, and only a validated, versioned change counts; the governed cycle lives in the `quality` skill's [evolution](../../quality/references/evolution.md).

Structural changes to one graph move the others: reshaping the task graph changes the capabilities the units need, which changes the team topology, which changes what the ledger must record. Validate the coupled change and check that it generalizes to the recorded failures; an unvalidated structural edit is churn with a diagram.
