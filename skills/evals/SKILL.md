---
name: evals
description: "The harness regression suite: a set of realistic tasks, each a prompt plus objective checks, run on a schedule and whenever the manifesto, a skill, a hook, or the model changes, blocking a merge that lowers the pass rate. Use when changing the doctrine itself, converting an incident into a permanent regression, judging whether a GROW evolution helped, or setting up a suite for a repo whose instruction files agents execute."
---

# Evals

The doctrine is **configuration an agent executes** — the manifesto, the skills, the commands, the hooks, the gates. That is exactly the definition of code, and it gets the same treatment: whatever steers the agent is versioned, reviewed, and **regression-tested**. An eval is one realistic task plus objective checks; the suite is the set of them. Its pass rate over time is the only honest answer to "did that change make the agent better or worse?" — because a doctrine edit that reads well and degrades behavior is indistinguishable from a good one until it is run.

> **Override.** A project-level eval suite that explicitly supersedes this skill wins.

## An eval is a prompt plus objective checks

Two parts, and the second is what makes it an eval rather than an example:

- **The task** — a realistic request of the kind the agent actually receives, specific enough to have a right answer. "Refactor the config loader" is not an eval; "the loader duplicates env parsing in three places; consolidate it and keep the CLI flags identical" is.
- **The checks** — executable conditions, run against the agent's output, that yield pass or fail without a human reading the transcript. A named command and its expected observable: exit 0, a query count, a response body, a file that now exists with a given shape.

A check that needs a human to judge whether it passed is not objective, and an eval made of them drifts with whoever is reading. Keep the checks mechanical ([verification](../verification/SKILL.md) owns the evidence standard they invoke).

## Size it to the harness, not to completeness

A suite is not a coverage exercise. Twenty to fifty realistic tasks spanning the behaviors the doctrine actually governs — intake routing, gate emission, verification discipline, context handling — is enough to catch a regression, and small enough to run often. A suite of three hundred nobody runs has a pass rate of zero in practice. Start with the failures you have already seen; grow on incident, not on ambition.

**Prefer tasks drawn from real runs.** A task that extracts from an actual episode — a gate that went unemitted, a check that got narrated instead of run — is a regression test with a proven failure mode behind it. Invented tasks test what you imagined; extracted ones test what happened.

## When it runs

- **On schedule** — a standing cadence, so drift from a model change is caught without anyone remembering to look.
- **On any change to the harness** — the manifesto, any `SKILL.md`, a command, a hook, a gate, or the pinned model. This is the load-bearing trigger: a doctrine edit's whole claim is that it improves behavior, and the suite is where that claim is tested instead of asserted.
- **On incident** — every production incident whose cause was agent behavior becomes a permanent eval *after the fix ships*, so the class cannot return silently.

## What a regression means

A change that lowers the pass rate **blocks the merge** until it is fixed or the eval is deliberately retired with a reason. Two honest outcomes and one dishonest one:

- **Fix the change** — the regression is real and the edit was wrong.
- **Retire the eval, with a reason** — the behavior it asserted was itself wrong, and the doctrine deliberately moved. Retiring is legitimate; retiring *because it failed* is the doctrine grading its own homework, which is the failure [verification](../verification/SKILL.md) hunts under other names.
- **The dishonest one** — loosen the check until it passes. That is a metric edited by the party it measures, and the anchor rank forbids it: the eval's target is set by the harness's intent, not by what the change made easy to assert.

Never let the agent that wrote the change write the check that judges it. Same independence rule as any verifier ([lifecycle](../lifecycle/SKILL.md)).

## Evals are how GROW proves itself

GROW's whole cycle — instrument, propose, validate, commit — has one weak joint: *validate*. A new gate or a sharpened rule is a hypothesis that the harness will fail less often; the suite is where the hypothesis meets evidence. Run it before and after an evolution: a change that passes the gates and holds the suite is one you can commit with a rationale; one that regresses it is a change to revert, not to reconcile ([evolution](../verification/references/evolution.md)).

Pair evals with the **Kirby Effect** discipline: when a model upgrade lands, run the suite *with a control removed* before assuming the control is still needed. A component the suite passes without is dead weight, and evals are the measurement that tells you so — the harness shrinks by evidence, not by taste.

## Common mistakes

| Mistake | Fix |
| --- | --- |
| Checks a human must judge | Make them mechanical: a command plus its expected observable |
| A suite too large to actually run | 20-50 realistic tasks; grow on incident, not ambition |
| Invented tasks only | Extract from real runs; a proven failure mode beats an imagined one |
| Running only on a schedule | Trigger on harness change too — that is the load-bearing case |
| Loosening a check so a change passes | Block the merge; the change is wrong or the eval is deliberately retired |
| The change author writing its checks | Same independence rule as any verifier — separate the actors |
| An incident fixed and forgotten | Convert it to a permanent eval after the fix ships |
| Assuming a control is still needed | Run the suite with it removed on each model upgrade |

## Cross-references

- [verification](../verification/SKILL.md) the evidence standard each eval's checks invoke; the mutation probe is the same idea applied to one change.
- [lifecycle](../lifecycle/SKILL.md) evals test the process; verification tests a unit of work. Both attach to every stage.
- [evolution](../verification/references/evolution.md) the governed GROW cycle evals exist to validate.
- [artifacts](../artifacts/SKILL.md) the eval suite is itself a committed artifact with a shape, not ad-hoc.

Distilled from Anthropic's *AI-native SDLC playbook*: continuous evals as the AI-native equivalent of a QA stage gate — a maintained task set with objective checks, re-run on schedule and on any change to the agent's configuration, blocking merges that lower the pass rate, with every incident becoming a permanent regression.
