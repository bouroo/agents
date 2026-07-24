# Right-Sizing the Harness to the Job

> Load on demand. The short pointer lives in [harness-engineering](../SKILL.md) §7 (termination) and `AGENTS.md` §6 (verification); this file is the two-axis map and the control dial.

The right harness depends on the job. Every control in this skill -- three-layer termination, mutation probes, adversarial judging, GROW retros -- exists because some failure once demanded it. Applying all of them to every task is the **Average Answer Trap**: assuming you need the full apparatus just because the hardest jobs do. The cost is real -- token spend, latency, and delegation round-trips on work that never needed them.

Two anti-patterns to refuse:

- **Average Answer Trap** -- turning high-complexity controls into defaults. A one-line typo does not need L3 end-to-end, a mutation probe, an adversarial judge, and a GROW retro.
- **Kirby Effect** -- a component that encodes an assumption about something the model cannot yet do. Every such component is a bet that goes wrong as models improve. Revisit each addition when a stronger model arrives; yesterday's workaround is tomorrow's dead weight.

## The Two Axes

- **Action Complexity** -- how many tools, decisions, file handoffs, and outward side effects the task coordinates.
- **Context Complexity** -- how much code and state must be gathered and retained to finish it.

Plot the task on both axes. Pick the dial.

## Control Dial

| Complexity | Examples | L1 / L2 / L3 | Mutation probe | Adversarial judge | Artifact lines | GROW retro |
|---|---|---|---|---|---|---|
| Low / Low | typo, rename, format-only, one-file read-only question | L1 only (if the change is linted/compiled) | no | no | note the skip | no |
| Mid / Mid | feature or fix within one module; runtime behavior | L1 + L2 (tests for the touched behavior) | on behavior-bearing lines | on demand | `INTENT:` / `TWINS:` owed | only if a failure recurred |
| High / High | cross-boundary, infra, security-sensitive, multi-module | full L1 + L2 + L3 | yes | on demand | full, + decision log | yes |

Rules of thumb:

- **Executable evidence is never optional** -- whatever layer you run, capture command + exit code + actual output. The dial chooses *which* layers; it never lowers the evidence standard.
- **`n/a` is allowed** for any layer, with a one-line reason naming why the change cannot reach that layer.
- **Add a control only when a real failure demands it**, not because the hardest job uses it. Remove it when a stronger model makes it redundant.
- **Coding-agent doctrine only.** This is calibrated for source work. Support, sales, Q&A, and other low-complexity agents should not inherit this loop at all -- build the minimum viable harness for that job.

## Cross-References

- [harness-engineering](../SKILL.md) -- §7 (Three-Layer Termination), §8 (Mutation Testing), §10 (Adversarial Judge)
- [verification-theater](./verification-theater.md) -- when a Mid/High task's tests look theatrical

## Reference

- O'Reilly Radar: *Stop Overengineering Your Agent Harness* -- https://www.oreilly.com/radar/stop-overengineering-your-agent-harness/
