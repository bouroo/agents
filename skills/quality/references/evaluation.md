# Structural and Multi-Agent Evaluation

> Load on demand from [quality](../SKILL.md): the working detail behind the six evaluation dimensions — when the correctness of the work depends on the organization doing the work (several agents, a graph of steps, a division of labor), a green suite is not the verdict.

## Why a green suite is not enough

End-task success shows that the outcome held once, on the tasks the suite happens to run. It does not show that the system is better organized. The same curve comes from a stronger model, a longer context window, more samples, or more compute. A structure claim judged only on the end task is therefore unfalsifiable — the gain and the purchase look identical.

So work whose correctness depends on a structure is judged on six dimensions, each of which must be observable rather than asserted.

| Dimension | Question | Observable |
| --- | --- | --- |
| **Effectiveness** | Did the outcome hold? | pass rate and task success across the task set in scope, not on one task |
| **Efficiency** | What did a successful completion cost? | cost per successful completion — tokens, tool calls, retries, wall clock — where wall clock alone never qualifies: waiting is not working |
| **Robustness** | Does it survive disturbance? | behavior under a changed input, a failed dependency, a removed worker |
| **Structural fidelity** | Does the organization match the work? | whether the division of labor, the graph shape, and the node granularity fit the task's actual structure |
| **Operational correctness** | Were the graph's operations executed as intended? | every node ran as intended, every edge carried what its type carries, every cap held, no silently skipped step |
| **Evolution and governance** | Are structural changes traceable and controllable? | a proposal names its evidence and its author; a bad proposal is revertible and was reverted |

A structure that improves only one of these is not better; it is differently expensive.

## The budget-fixed discipline

The rule the Evals section owns: **hold the budget fixed and ablate the claimed structural change.** The mechanics:

1. **Fix the budget.** Same model, same token ceiling, same retry ceiling, same concurrency ceiling. A budget that moves makes every comparison meaningless.
2. **Ablate one structure.** Remove the claimed change and nothing else — no second improvement in the same run, or the delta is unattributable.
3. **Require the delta to disappear.** The structure earns its place only if removing it costs the measured gain.
4. **Read the verdict honestly.** A gain that survives only at a larger budget is a purchase, not an improvement — the system bought compute, it did not get better.

## What the evaluation needs as evidence

Without these, a structure claim is a narrative:

- **Matched execution budgets** — every arm of the comparison runs under the same ceiling.
- **Versioned artifacts** — the exact inputs, outputs, and configuration each arm ran against, recoverable later.
- **Complete traces and state snapshots** — the whole run, including the state transitions, so a claim about what happened can be re-derived rather than believed.
- **Controlled structural perturbations** — deliberately changed inputs, failed dependencies, removed workers, so robustness is exercised rather than assumed.
- **Repeated evaluation across tasks and over time** — a single run is noise, and a single day is one point on a curve.

Evaluation therefore combines three kinds of study: **intervention studies** (change one thing, measure), **structural ablations** (remove one thing, measure), and **execution-trace analysis** (read what actually happened, not what was reported).

## Independent verification is a structural role

A writer evaluating its own output is role confusion: the same context that produced the defect also argues against it, and confirmation bias makes the argument cheap. Verification is therefore a **separate role**, given the artifact, the pinned ask, and fresh context — never the writer's reasoning. Where the surrounding machinery grants roles, independence is a structural property of the graph (a verifier node that cannot be the writer node), not an instruction to the writer to be careful.

## Failure modes

| Mode | Looks like | Fix |
| --- | --- | --- |
| Green-suite worship | one passing run reported as proof the structure works | judge the six dimensions, at minimum robustness under a perturbation |
| Budget drift | the "with structure" arm ran more tokens, more retries, more time | fix the budget before comparing, or the gain is unattributable |
| Wall-clock worship | faster wall clock read as more efficient | efficiency is cost per successful completion |
| Robustness by assumption | no perturbation was ever applied | a perturbation per claimed improvement |
| Writer judges self | the author re-reads its own output and approves | a separate verifying role with fresh context |
| Structure described, not measured | a diagram offered as evidence of fitness | structural fidelity needs a match against the work's real shape |

## Cross-references

- [quality](../SKILL.md) — the Verification section that calls this file for the six dimensions, the Evals section that owns the budget-fixed ablation rule, and [measurement](measurement.md) for the cost-per-completion measurement.
