# Plays

> Load on demand from [delivery](../SKILL.md): the five-part shape every play shares, how the plays are ordered by dependency, and how the measurement pairs are read.

A **play** is a named practice with five parts: **what it changes**, **how to start**, **the steps**, **the governance**, and **how to measure it**. The five parts are the contract: the first says the shift, the second says the smallest entry point, the third is the work, the fourth says what is enforced and who owns it, and the fifth says how anyone would know it worked.

The plays are **modular and ordered by dependency, not by stage**. A play with no prerequisites is a valid starting point, and an organization adopts the stages it needs in its own order. Nothing in a play presumes the play above it ran first, except where the play says what it builds on.

## The per-stage plays

- Plan and Design — [plays-plan-design](plays-plan-design.md) — read when an intent needs capturing or a spec needs writing.
- Build — [plays-build](plays-build.md) — read when a change needs a plan, a project context file, a skill, a pre-action check, or parallel sessions.
- Test — [plays-test](plays-test.md) — read when a session needs its own feedback loop, or when the agent's configuration needs regression tests.
- Deploy — [plays-deploy](plays-deploy.md) — read when a change needs review passes, an approval gate, or a pipeline run.
- Maintain — [plays-maintain](plays-maintain.md) — read when a control band is breached, a scan needs a schedule, or an incident arrives from outside the monitoring path.

## How to start is the smallest honest entry point

**Getting started** names the least setup that makes the play real, and the infrastructure it assumes. It is where a play admits what it needs from the organization: a repository, a product owner with agent access, a place to put a pre-action check script, a metrics store, a continuous-integration pipeline. A play that says "none" is a claim that the play needs nothing bought before it starts — hold it to that claim.

## The governance part says four things

Every play answers the same four questions, and a play that leaves one unanswered has not finished its design:

- **What is enforced** — the rule, and the mechanism that makes it hold: a pre-action check that can allow, ask, or block, a check that exits non-zero, a branch rule demanding a named approval.
- **What the evidence is** — the artifact, the log, the check output, the review finding. Evidence comes from the system, not from the agent's account of it.
- **Where it is logged** — the store a later reader can query, so the play's own practice is measurable.
- **Who approves** — the seat, never "the team", and never the actor whose work is being judged.

## Measure the loop, not the tasks

Each play names a **leading indicator** — something that moves before the outcome — and a **lagging indicator** — the outcome itself. Read both together: a leading indicator that improves while the lagging one does not means the practice measures activity, not progress. A leading indicator that improves is a reason to keep going and check the lagging one, never a reason to declare success.

The unit of measurement is the **loop**, not the task. One change travelling Plan, Design, Build, Test, Deploy, Maintain is one journey: its cycle time, its rework count, and how many times it re-entered a stage are the numbers that say whether the practice worked. Counting tasks completed says only that work was typed.

## Choosing where to start

The dependency is not the same as the order:

1. **Plan** — capture as `intent.md` needs nothing. It is the cheapest change with the largest effect on the stages to its left.
2. **Design** — needs an `intent.md` and the policies written as skills.
3. **Build** — the project context file, the skills, and the pre-action checks each need the one before; the context file needs only a repository.
4. **Test** — the feedback loop needs the context file's commands; the evals need the feedback loop.
5. **Deploy** — the review policy needs the context file; the approval gates need the written list of approvals; the pipeline needs both.
6. **Maintain** — closing the loop needs the `intent.md` format, the approval gates, and a rehearsed rollback path.
