# Automation

> Load on demand from [execution](../SKILL.md): how a proven workflow keeps running without a human in the conversation, and where it stops so a human still holds the authority. Method distilled from the general coding-agent practice of layering a run-time trigger over a reusable workflow.

## Why this layer exists

A **Skill** captures a workflow so it runs the same way every time; an **Automation** keeps that workflow running when nobody is watching. The pair completes the fourth noun of the practice — prompts carry the task, plans carry the intent, skills carry the method, workflows carry the repetition.

Automation is the last layer to earn, not the first: automate a workflow that has already proven itself interactively, run twice by hand with the same result. A timer over a workflow nobody has run is a broken procedure on a schedule.

It also completes the development loop: the same stages that run during a session (implement, test, run the checks, review) can run unattended on the same gates, so the loop keeps turning between human sessions.

## The workflow stays a workflow

Automating does not change what the workflow does, only who calls it. Three properties carry over unchanged:

- **The same gates.** The check that gated the interactive run gates the automated one — same command, same expected exit code.
- **The same artifacts.** The output of an automated run is the artifact the interactive run produced: a diff, a report, a ledger entry. A different output shape means a different workflow, and a workflow that changed is one that has not proven itself.
- **The same scope.** The automated run touches what the interactive run touched. Scope growth is a deliberate change, made once, reviewed.

## The unattended contract

An automated run has no conversation, so the gates that depend on attention become the run's own obligations:

- **The scope is pre-declared.** The automation states what it may touch before it starts; a run that needs more scope ends local and reports the gap rather than widening its own permissions.
- **The check gates the stop.** A run ends on its own evidence — the command and exit code captured, nothing narrated from memory.
- **Authority still terminates in a human.** An automated run never performs an outward or destructive effect on its own authority: it ends local and emits `PENDING:` naming the action it would take. An automation that posts, publishes, merges, or deletes without a human in the loop is an unreviewed release path.
- **The report is the output.** A scheduled run's deliverable is a report with commands, exit codes, and findings — never a silent change to a branch nobody reviewed.

## What fires the run

The trigger is the least interesting part of the design and the easiest to get wrong; the workflow it calls is the work. Three shapes cover nearly every case, and none is preferred by default:

- **Event** — a release is published, a CI run completes, a review is requested. Fires once per event; the state that decides whether to fire lives outside the run.
- **Condition** — a threshold crossed, a check failed, an anomaly detected. Fires on something the agent can observe.
- **Schedule** — daily, weekly, hourly. The simplest to write and the one that needs a rule for overlap: what happens when the previous run is still going.

Pick the trigger that matches how the work arises; when none of the three fits, the workflow probably does not run unattended yet.

## The template

Reuse this shape for a new automation; fill the bracketed parts and delete the rest.

```markdown
# Automation: <workflow name>

- **Workflow:** <the skill or command this calls>
- **Fires on:** <event | condition | schedule> — <what fires it>
- **Runs:** <where it runs, on whose machine, with what credentials>
- **Scope:** <files, systems, and commands this run may touch>
- **May not:** <outward, destructive, or irreversible effects — always ends local and emits PENDING:>
- **Check that gates the stop:** <command> — exit <code> means done
- **Report:** <where the report lands, what it carries>
- **Owner:** <who reads the reports, and how often>

## Steps

1. <step> — verify: <command>
2. <step> — verify: <command>

## Failure

- On a failed check: stop, report the failing command and output, propose the next action, do not retry the same arguments.
- On an unexpected result: treat it as a surprise — re-read before acting.
```

## Failure modes

- **Automation over an unstable workflow** — the trigger publishes a bug on a schedule. Fix the workflow first.
- **Unbounded retries** — a failing run that retries forever hides the failure. Bound the retries; a deterministic failure is terminal.
- **Overlapping runs** — two instances of the same run writing the same state. Make the run idempotent or serialize it with a lock.
- **Silent scope growth** — the automation was allowed one repository and now touches three. Scope creep is a design change, made deliberately, not a side effect.
- **Authority creep** — the first version read CI logs, the second merged the fix. Every authority increase is a separate, explicit decision.
- **No owner** — nobody watches the reports, so a run can fail for months unnoticed. Name the owner and the review cadence.
- **The trigger became the job** — the workflow is now written around one schedule and no longer usable by hand. If a person cannot run it on demand, it is not a workflow with an automation; it is a script.
