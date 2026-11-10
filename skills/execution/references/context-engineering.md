# Context Engineering

> Load on demand from [execution](../SKILL.md): what goes into the window and what stays out, why a longer context is a worse one, and what a compaction must preserve. Distilled from published context-engineering guidance, generalized away from any one host.

## The window is an attention budget, not a container

Recall degrades as the window grows. Every token introduced spends attention that would otherwise have gone to the tokens that matter, so the marginal value of context falls while its marginal cost rises. Two consequences the setup already half-states: the smallest set of high-signal tokens maximizes the chance of the desired outcome, and "keep the window small" is an **accuracy** rule, not a cost rule. A window that is merely affordable can still be wrong.

The always-loaded surface is the one every task pays for, so it is the surface that must earn its place. The host loads a skill's description to decide what applies, so a description is a routing decision rather than documentation, and a rule that never changes a decision is dead weight in the most expensive slot in the window.

## Instruction altitude

Every instruction sits on a line between two failures. **Too low**: brittle hardcoded logic — a branch for every case the author imagined, fragile, and expensive to maintain as the world moves. **Too high**: vague guidance that assumes shared context the run does not have, so the gap gets filled with something plausible. The right altitude is specific about the outcome and the check, and leaves the method to the model: name what must be true when the instruction is satisfied, not the steps that might produce it.

Two questions tell an instruction where it sits. Could two competent readers satisfy this rule by different routes? If not, it is too low. Could a reader with no other context satisfy it? If not, it is too high.

## An example teaches what a rule cannot

Some behaviors are checks and are best written as checks. Others are a shape of behavior that no check names, and a list of every edge case is a poor substitute for one: it is long, it is not weighted by likelihood, and it reads as a rule list rather than a demonstration. A small set of diverse, canonical examples carries the behavior in a fraction of the tokens, so prefer three good examples to twenty enumerated cases, and let a check govern whatever a reader can verify.

Worked example: the `unslop` skill's three before-and-after rewrites teach residue faster than its rule list does, and its scanner supplies the check.

## Compaction is a first lever, and it is lossy

When a window nears its limit, the cheapest continuation is to summarize it and continue from the summary; the alternative is a run that simply stops. Compaction is lossy in the dangerous direction — what it drops may look redundant at the time and matter later. So the policy is explicit about what survives:

- **decisions and their reasons**, architectural or otherwise;
- **open questions** and the requirements still owed;
- **the current position** — where the work is, what was tried, what the next action is;
- **the anchors and evidence pointers** the next step will cite.

And what goes: repeated tool output whose result is recorded elsewhere, superseded intermediate output, and anything the run can re-derive from disk. The lightest touch that helps is clearing old tool results — once a result is deep in the history, the raw form is rarely needed again — before discarding anything the run reasoned about.

This is about *using* compaction when a window fills, not about building a compaction subsystem. The first is a lever every run may pull; the second is machinery the setup still refuses to add speculatively, because a feature is a bet that expires.

## Just-in-time retrieval beats up-front loading

A run that carries the whole corpus in its window pays for it on every turn and recalls less as it grows. Keep a lightweight identifier instead — a path, a stored query, a link — and load the body at the moment it is needed. This is what the setup already does with skills and references: the manifest is a map, and a reference loads on a stated condition.

Identifiers carry meaning the body does not. A name and a location say what the material is for and when it was written, so the map stays useful without the body.

## A small always-on core, an explored remainder

Both ends are needed and they fail differently. **Up front**, a small core: the rules every task obeys, the environment facts, the routing information. **On demand**, exploration: the agent navigates its own information landscape, and each result informs the next step. The hybrid beats either extreme — retrieve up front for speed on stable material, explore where the path is not knowable in advance.

The cost of exploration is dead ends: a run that misuses its tools, chases a stale pointer, or misses the key file spends the very window it was trying to save. The cure is a scoped tool surface and a stated load condition on every deferred pointer, not more up-front context.

## What this does not change

The tool-surface rules stay where they are ([harness-design](harness-design.md)); the memory layers and the instruction/learning split stay where they are ([memory](memory.md)); the isolation move — a worker with a clean window — stays where it is ([topologies](topologies.md)). This file adds the budget and the compaction policy that those rules did not state.

## Cross-references

- [harness-design](harness-design.md) — the tool surface, the deterministic-injection rule, and the two sizing axes.
- [memory](memory.md) — what survives a session boundary, and how a rule is authored so it survives.
- [execution](../SKILL.md) — the loop whose continuity a compaction has to preserve.
