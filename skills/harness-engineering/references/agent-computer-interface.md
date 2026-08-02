# Agent-Computer Interface (ACI) -- Tool & MCP Design

> Load on demand. The short pointer lives in `AGENTS.md` §2 (tool routing) and [harness-engineering](../SKILL.md) Cross-References; this file is the design checklist for when you *build* a tool, slash command, or MCP rather than merely call one.

The model is only as good as the interface it drives. Invest in the agent-computer interface (ACI) the effort you would give a human-facing one: a tool a model misuses is a tool whose spec failed, not a model that failed.

**Scope.** This covers *designing* tools and MCPs. Picking which *existing* capability to call is routing -- see `AGENTS.md` §2. Right-sizing the *verification* a tool's output triggers is [right-sizing](./right-sizing.md).

---

## Stance

A tool is a contract, not a convenience wrapper. Every argument the model must guess at, every output field it must reverse-engineer, every overlapping responsibility between two tools is a failure mode you built in on purpose. The goal is the smallest, most self-evident contract that makes correct use the path of least resistance and misuse harder than correct use.

## Design checklist

- **Self-contained.** A caller holding only the tool's description can use it correctly -- no tribal context, no "you also need to know." State the input shape, the output shape, and the side effects in the spec itself.
- **Non-overlapping.** Two tools must not answer the same call. If `search_code` and `find_symbol` both return matches for a name, the model is forced to guess; either merge them or draw a boundary the spec states ("string vs. symbol," "broad vs. precise"). One capability, one tool.
- **Poka-yoke arguments -- make misuse harder than correct use.**
  - Require **absolute paths**, never relative. A model mid-context loses the cwd; an absolute path cannot be silently wrong.
  - Prefer **typed enums** over free strings where the value set is closed (`"strict" | "loose"` beats `string`).
  - Make an argument **required** when ambiguity is the failure mode; optional only when the default is genuinely always-safe.
  - Accept the **most constrained shape** that still works (a structured object over a prose blob).
- **Token-efficient returns.** Return the decision, not the dump. Surface structure first -- counts, paths, headers, a summary -- and gate large bodies behind pagination or a follow-up call. A tool that returns 4,000 lines "to be safe" forces the model to re-read noise every turn and rots the context window -- context rot, `AGENTS.md` §7.
- **Complete spec contents.** One-line purpose; input shape with edge cases (empty, missing, very large); output shape; at least one worked example; and explicit **boundaries** -- what the tool will *not* do. Writing the spec is writing a docstring for a careful junior developer who has no other documentation.
- **Minimal formatting overhead.** Keep the description close to natural prose the model has seen at scale. Avoid gimmicks the model must parse -- mandatory line-counting, custom escaping schemes, positional flags dressed as tokens. Cognitive overhead spent decoding the format is overhead spent not solving the task.

## The feedback loop

A tool's spec is a hypothesis about how the model will use it. Validate it the way you validate code:

1. **Watch real usage.** Run the tool through representative turns; log where the model passes the wrong argument, the wrong shape, or calls the wrong sibling tool.
2. **Repeated misuse is a spec bug, not a model bug.** If the model reliably misuses an argument, fix the argument -- rename it, constrain its type, make it required, or fold it into another tool. Do not add a prose warning and ship.
3. **Convert recurring misuse into a gate.** A misuse you cannot design out becomes a deterministic check (a validator, a type constraint, a pre-flight assertion). This is the §13 [Failure-Mode -> Control Map](../SKILL.md) applied to interfaces: the control lives in the harness, not in a reminder.

> **Kirby check.** A poka-yoke constraint that exists only because the current model cannot read a flat description is a bet against model improvement. Revisit each constraint when a stronger model arrives; yesterday's guardrail is tomorrow's dead weight (see [right-sizing](./right-sizing.md)).

---

## Cross-References

- [harness-engineering](../SKILL.md) -- §13 (Failure-Mode -> Control Map), where recurring tool misuse becomes a deterministic gate.
- [Right-sizing the harness](./right-sizing.md) -- the Average Answer Trap and the Kirby Effect; applies to interface constraints too.
- [composition-patterns](./composition-patterns.md) -- how designed tools compose into delegation topologies.
