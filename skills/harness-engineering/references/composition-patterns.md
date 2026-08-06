# Composition Patterns -- Choosing the Delegation Topology

> Load on demand. The short pointer lives in `AGENTS.md` §3 (The Squad) and the [conductor](../../../agents/conductor.md) agent; this file is the menu for deciding *how* to break work across sub-agents once you have decided *that* you will delegate.

Delegating is not one pattern -- it is a choice among five. Pick the **smallest topology the job can hold**: every fan-out costs latency, tokens, and a round-trip, and most tasks need none of them. The Conductor's unit graph is already the orchestrator-workers pattern; reach for the others only when the work refuses that shape.

**Scope.** This covers *delegation topology* -- how sub-agents compose. Designing each worker's *tools* is [agent-computer-interface](./agent-computer-interface.md); deciding *how many verification layers* a delegated unit needs is [right-sizing](./right-sizing.md).

---

## The pattern menu

| Pattern | Shape | When it fits | Repo instance |
|---|---|---|---|
| **Prompt chaining** | Fixed sequence; each step feeds the next | Steps are known and ordered; each gates the next | THINK -> ACT -> PROVE -> GROW itself; `canvas.md` -> `state.json` -> verdict |
| **Routing** | Classify once, dispatch to one specialist | Inputs sort into disjoint types needing different handling | Conductor pre-flight classification (delegate to `coder` vs. `discover` vs. direct check) |
| **Parallelization -- sectioning** | N independent subtasks run at once, then aggregate | Subtasks share no data and no order | `discover (explore)` fanned across separate subsystems; independent `coder` units with `deps: []` |
| **Parallelization -- voting** | Same task N times, divergent lenses, then reconcile | One good pass is riskier than diverse perspectives; correctness/coverage is the bottleneck | Adversarial judge (§10) -- N skeptics, majority refutes to kill a plausible-wrong claim |
| **Orchestrator-workers** | Central planner decomposes dynamically, delegates, synthesizes | Subtasks **cannot** be predicted upfront | Conductor Plan Mode -- the unit graph (default) |
| **Evaluator-optimizer** | Generate, critique against a rubric, re-generate | A clear grading rubric exists and iteration measurably helps | `coder (judge)` -> `REFUTED` -> `coder (fix)` loop |

**Default to orchestrator-workers** (you are already in it). Reach right for routing or sectioning only when decomposition produces independent units that would serialize for no reason. Reach for voting or evaluator-optimizer only when a single pass has demonstrably failed or the task is correctness-critical -- both multiply cost.

## Right-size the topology

Two anti-patterns to refuse (full statement in [right-sizing](./right-sizing.md)):

- **Average Answer Trap** -- fanning out because the hardest job does. A two-step, single-module fix needs no sectioning and no voting; serial delegation of one `coder` unit is correct.
- **Kirby Effect** -- a topology that exists only because the current model cannot hold a context a stronger one will. If parallelizing exists solely to dodge context rot, revisit it when the model improves; the fan-out may be removable.

Add a fan-out only when a real failure (serialization latency, a wrong-but-plausible verdict, an unreached code path) demands it. Measure that it helps before keeping it.

## Clean-context delegation

- **Each subagent gets a complete, unambiguous packet** -- goal, scope, done condition, and the evidence it must return. Vague instructions cause subagent failure; the Conductor owns packet quality (see `conductor.md`).
- **Fresh window per subagent.** A subagent starts with a clean turn context -- that isolation *is* the value of delegating, not an inconvenience to route around by re-inlining its work. Do not pre-load a worker with context it can fetch itself -- context engineering, `AGENTS.md` §7.
- **Synthesize at one boundary.** Workers return structured verdicts; the orchestrator reconciles once. Re-reconciling after every worker is a hidden serial bottleneck.

## Stopping conditions and transparency

- **Every loop carries a bound.** The 3-cycle hard verify bound (`AGENTS.md` §6) is the existing instance; an evaluator-optimizer or orchestrator loop needs its own iteration cap, never open-ended delegation. State the cap before the first iteration.
- **Show the decomposition before executing.** Emit the unit graph / plan artifact first (Plan Mode, `canvas.md`); a topology the user cannot see is a decision they cannot correct. This is the transparency principle: planning steps are explicit, never implicit.

---

## Cross-References

- [harness-engineering](../SKILL.md) -- §10 (Adversarial Judge, the voting instance), §6 (Three-Layer Termination, the bound on loops).
- [Right-sizing the harness](./right-sizing.md) -- when a topology's cost is justified, and the Average Answer Trap / Kirby Effect.
- [agent-computer-interface](./agent-computer-interface.md) -- the workers are only as good as the tools they drive.
