# Harness Design

> Load on demand from [graph-engineering](../SKILL.md): the minimal-harness ladder, the pattern catalogue mapped onto the graph grammar, and tool-surface design. Distilled from Anthropic's *Building effective agents* and Hugo Bowne-Anderson's *Stop overengineering your agent harness* — adopted as method, numbers re-derived locally.

## The minimal-harness ladder

Start at the least agency that closes on evidence, and climb only on a measured need. Three rungs:

1. **Prompt or retrieval** — one model call plus context. Enough when the answer is already in the window or fetchable in one step; no loop, no tools beyond a lookup.
2. **Fixed workflow (linear / staged)** — a designed sequence of calls with known routes, composed ahead of time. Deterministic control flow means the model cannot wander, and the graph is inspectable.
3. **Agent loop** — the model chooses its route at run time, iterating until it closes. The most capable rung and the most expensive; it buys adaptability only where the path genuinely cannot be known in advance.

This is the shape ladder viewed from the **agency axis**: the four shapes say how a job's nodes connect, the ladder says how much of that connection the model decides. Both bind to the same rule — enter low, climb on a bottleneck, step down when the reason for the climb disappears.

**Walking-skeleton build order.** Build the smallest loop that closes end-to-end on evidence first — one prompt, or the linear sequence — then add a control only when an observed failure demands it. This is the Kirby Effect at harness level: every routing rule, retry, and sub-agent is a bet on a limitation, and bets are placed on evidence, not on speculation. A harness accreted control-by-control from the start is the framework the next section warns against, wearing the doctrine's own vocabulary.

## The pattern catalogue → the grammar

The industry's agent patterns are the doctrine's shape vocabulary under other names. Map, do not memorize:

| Catalogue pattern | Grammar |
| --- | --- |
| Augmented LLM | a node with tools |
| Prompt chaining | linear / staged |
| Routing | `ROUTES` (diamond, named conditions, exactly one edge taken) |
| Parallelization — sectioning | `FAN_OUT` to independent subtasks, `JOINS` at the synthesis |
| Orchestrator-workers | the coordination graph ([teamwork](../../teamwork/SKILL.md) rungs) |
| Evaluator-optimizer | the canonical review graph's `VERIFIES` + gated `RETURNS` |
| Agent | the graph itself |

The composition follows: a real job is several of these nested, and the entry point is the least complex pattern that fits — a chained workflow often suffices where an agent was assumed. Read a catalogue entry as a shape you already have, not a new mechanism to import.

## Fan-out has two rationales

The `FAN_OUT` edge carries one of two intents, and they are designed differently:

- **Sectioning** — the job splits into *independent subtasks* (per-file migrations, per-lens reviews). The branches differ; each does its own work; the `JOINS` merges distinct results.
- **Voting** — the *same* task runs N times and the outputs are aggregated for confidence (majority answer, union of findings). The branches are nominally identical; the `JOINS` decides by agreement.

Sectioning pays when the parts are genuinely disjoint. Voting pays only when the N runs are plausibly **decorrelated** — different sampling, different context, or different lens. Correlated runs fail together, so the aggregate carries no more confidence than one run and the N-fold premium becomes a tax. This is the same hazard as teamwork's **correlated lenses**: reviewers sharing one blind spot buy nothing by multiplying windows. Never cite "ensemble" or "N runs" as free confidence — state why the runs decorrelate, or do not vote.

## Design the tool surface (ACI)

The tool definitions are as load-bearing as the prompt: they are the interface the model actually reads, so they are designed *for the model*, not written for the implementer.

- **Document what, when, and how.** For each tool state what it does, when to use it (and when not), the input format, the returned fields, and its error behavior.
- **Poka-yoke the arguments.** Make the wrong call hard to express — constrain enums, require the identifying field, remove the ambiguous optional. A misuse-prone signature is an interface defect, not a prompting problem.
- **Use natural, model-friendly formats.** Plain structured text the model reads fluently beats a clever encoding it must decode.
- **Boundary against neighbours.** Say how this tool differs from the similar one, or the model will pick the wrong sibling by name resemblance.
- **Iterate on observed misuse.** When traces show a tool used wrongly, fix the interface first — tighten the description, the signature, the return — before adding an instruction to the prompt. The prompt compensates for a bad surface; the surface is what removes the failure class.

## Scope the tool surface

Give the agent only the tools its job needs: a narrower surface means less confusion, fewer misuses, and less exposure to injected instructions arriving through tool output. Breadth is not capability — it is surface area. A worker's spawn brief scopes its tools to its task for the same reason ([teamwork](../../teamwork/SKILL.md)); the node contract names what the worker may touch, not just what it owes.

## Inject known context; do not ask the model for it

Anything the system already knows — the date, the file path, the schema, the project's conventions — is supplied deterministically into the context, never inferred by the model or requested through a tool. Asking the model to recall or fetch a known fact spends a round-trip and adds a failure mode to information the harness already holds. This is §10's *never put deterministic logic in the model* applied at the context boundary: retrieval is for what the system does not know.

## Attribute the failure to its layer

When a step fails, name the layer before patching: **reasoning** (the model decided wrongly), **tool interface** (it reached for the right action through a bad signature or description), **context** (the fact was absent, stale, or buried), or **control flow** (the graph routed wrongly, or a cap was too tight). The wrong-layer fix is a symptom patch — rewriting the prompt when the interface was ambiguous, or relaxing a check when the routing was wrong, leaves the cause in place. Diagnose per [verification](../../verification/SKILL.md), then patch the layer the evidence points to.

## Do not surrender design to a framework

An SDK, an MCP server, or an orchestration library is an **implementation mechanism**, not a substitute for deciding what the agent needs. The design decisions — rungs, shapes, tool surface, what is injected — are yours and are made before any framework is chosen; a framework that hides the prompts, the raw responses, and the execution flow also hides the evidence you debug with. Use the abstraction when it carries a decision you have already made, and understand what lies beneath it well enough to read the trace when it fails.

## Cross-references

- [graph-engineering](../SKILL.md) the grammar these rules configure; the shape ladder and this agency ladder are the same entry discipline.
- [teamwork](../../teamwork/SKILL.md) the coordination graph and spawn briefs that scope a worker's surface.
- [verification](../../verification/SKILL.md) the evidence standard, the diagnosis discipline, and the caps that bound every `RETURNS`.
- [topologies](topologies.md) the canonical review graph and shape cost arithmetic these patterns resolve to.
