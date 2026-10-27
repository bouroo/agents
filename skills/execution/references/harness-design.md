# Harness Design

> Load on demand from [execution](../SKILL.md): the minimal-harness ladder, the pattern catalogue mapped onto the graph grammar, and tool-surface design. Distilled from Anthropic's *Building effective agents* and Hugo Bowne-Anderson's *Stop overengineering your agent harness* — adopted as method, numbers re-derived locally.

## The minimal-harness ladder

Start at the least agency that closes on evidence, and climb only on a measured need. Three rungs:

1. **Prompt or retrieval** — one model call plus context. Enough when the answer is already in the window or fetchable in one step; no loop, no tools beyond a lookup.
2. **Fixed workflow (linear / staged)** — a designed sequence of calls with known routes, composed ahead of time. Deterministic control flow means the model cannot wander, and the graph is inspectable.
3. **Agent loop** — the model chooses its route at run time, iterating until it closes. The most capable rung and the most expensive; it buys adaptability only where the path genuinely cannot be known in advance.

This is the shape ladder viewed from the **agency axis**: the four shapes say how a job's nodes connect, the ladder says how much of that connection the model decides. Both bind to one rule — enter low, climb on a bottleneck, step down when the reason for the climb disappears.

**Walking-skeleton build order.** Build the smallest loop that closes end-to-end on evidence first — one prompt, or the linear sequence — then add a control only when an observed failure demands it. This is the Kirby Effect at harness level: every routing rule, retry, and sub-agent is a bet on a limitation, placed on evidence, not speculation. A harness accreted control-by-control from the start is the framework the next section warns against, wearing the doctrine's own vocabulary.

## The pattern catalogue → the grammar

The industry's agent patterns are the doctrine's shape vocabulary under other names. Map, do not memorize:

| Catalogue pattern | Grammar |
| --- | --- |
| Augmented LLM | a node with tools |
| Prompt chaining | linear / staged |
| Routing | `ROUTES` (diamond, named conditions, exactly one edge taken) |
| Parallelization — sectioning | `FAN_OUT` to independent subtasks, `JOINS` at the synthesis |
| Orchestrator-workers | the coordination graph ([teamwork](../SKILL.md) rungs) |
| Evaluator-optimizer | the canonical review graph's `VERIFIES` + gated `RETURNS` |
| Agent | the graph itself |

The composition follows: a real job is several of these nested, and the entry point is the least complex pattern that fits — a chained workflow often suffices where an agent was assumed. Read a catalogue entry as a shape you already have, not a new mechanism to import.

## Fan-out has two rationales

The `FAN_OUT` edge carries one of two intents, designed differently:

- **Sectioning** — the job splits into *independent subtasks* (per-file migrations, per-lens reviews). The branches differ; each does its own work; the `JOINS` merges distinct results.
- **Voting** — the *same* task runs N times and the outputs are aggregated for confidence (majority answer, union of findings). The branches are nominally identical; the `JOINS` decides by agreement.

Sectioning pays when the parts are genuinely disjoint. Voting pays only when the N runs are plausibly **decorrelated** — different sampling, different context, or different lens. Correlated runs fail together, so the aggregate carries no more confidence than one run and the N-fold premium becomes a tax. This is teamwork's **correlated-lens** hazard: reviewers sharing one blind spot buy nothing by multiplying windows. Never cite "ensemble" or "N runs" as free confidence — state why the runs decorrelate, or do not vote.

## Design the tool surface (ACI)

Tool definitions are as load-bearing as the prompt: they are the interface the model actually reads, so they are designed *for the model*, not written for the implementer.

- **Document what, when, and how.** For each tool state what it does, when to use it (and when not), the input format, the returned fields, and its error behavior.
- **Poka-yoke the arguments.** Make the wrong call hard to express — constrain enums, require the identifying field, remove the ambiguous optional. A misuse-prone signature is an interface defect, not a prompting problem.
- **Use natural, model-friendly formats.** Plain structured text the model reads fluently beats a clever encoding it must decode.
- **Boundary against neighbours.** Say how this tool differs from the similar one, or the model will pick the wrong sibling by name resemblance.
- **Iterate on observed misuse.** When traces show a tool used wrongly, fix the interface first — tighten the description, the signature, the return — before adding a prompt instruction. The prompt compensates for a bad surface; the surface removes the failure class.

## Scope the tool surface

Give the agent only the tools its job needs: a narrower surface means less confusion, fewer misuses, and less exposure to injected instructions arriving through tool output. Breadth is not capability — it is surface area. A worker's spawn brief scopes its tools to its task for the same reason ([teamwork](../SKILL.md)); the node contract names what the worker may touch, not just what it owes.

## Inject known context; do not ask the model for it

Anything the system already knows — the date, the file path, the schema, the project's conventions — is supplied deterministically into the context, never inferred by the model or requested through a tool. Asking the model to recall or fetch a known fact spends a round-trip and adds a failure mode to information the harness already holds. This is §10's *never put deterministic logic in the model* applied at the context boundary: retrieval is for what the system does not know.

## External systems extend the context boundary

Context the job needs often lives outside the repository — issue trackers, CI results, database schemas, API references, internal automation — and a protocol that exposes those systems as resources or tools (MCP being the common one) is how it arrives. Prefer the connected retrieval to a pasted excerpt: the boundary stays explicit, the retrieval is repeatable, and the trace shows what the agent actually read. This changes what the agent can do, so treat each connection as authority and exposure rather than free capability: scope it to the systems the job reads, keep write access narrower than read, and keep every result in the untrusted-input class the tool-surface rules above already bind — a fetched document or tool response is a claim to verify, never consent.

## The execution environment defines what the agent can do

Behavior is not the model's alone: the same agent produces different results under a different working directory, permission set, or command surface. Four categories decide what a run can do at all, and each is a design decision rather than a default to accept:

- **Where the agent runs** — the project root it resolves paths against, and whether that root is the repository, a subproject, or a container. A wrong root produces a run that looks at the right files in the wrong place.
- **What it may touch** — read and write permissions, the files it may modify, and the paths it must not. Narrow by default and widen deliberately; a permission widened "for this run" becomes the next run's inherited default.
- **Which commands it may run** — the build, test, and lint surface. The check the agent must run is part of its environment: if the test command is not reachable, "run the tests" is an instruction the agent cannot obey.
- **What it is connected to** — external tools and data sources (below). A connection is capability, exposure, and authority at once.

Diagnose these before the model when a run behaves inconsistently: an agent that cannot locate the project directory, cannot read a file, or cannot run the test command is reporting the environment's limits, not its own.

## The automation layer

A skill says how a workflow runs; an automation says when it runs and how it keeps running. Automate only a workflow that has proven itself interactively, and keep the unattended run inside the same gates: pre-declared scope, the check that gates the stop, and a human holding the authority — an automated run ends local and emits `PENDING:` rather than acting outward on its own. The template and the failure modes: [automation](automation.md).

## Attribute the failure to its layer

When a step fails, name the layer before patching: **reasoning** (the model decided wrongly), **tool interface** (it reached for the right action through a bad signature or description), **context** (the fact was absent, stale, or buried), or **control flow** (the graph routed wrongly, or a cap was too tight). The wrong-layer fix is a symptom patch — rewriting the prompt when the interface was ambiguous, or relaxing a check when the routing was wrong, leaves the cause in place. Diagnose per the verification standard, then patch the layer the evidence points to.

## Do not surrender design to a framework

An SDK, an MCP server, or an orchestration library is an **implementation mechanism**, not a substitute for deciding what the agent needs. The design decisions — rungs, shapes, tool surface, what is injected — are yours and are made before any framework is chosen; a framework that hides the prompts, the raw responses, and the execution flow also hides the evidence you debug with. Use the abstraction when it carries a decision you have already made, and understand what lies beneath it well enough to read the trace when it fails.

## Cross-references

- [execution](../SKILL.md) the grammar these rules configure; the shape ladder and this agency ladder are the same entry discipline.
- [teamwork](../SKILL.md) the coordination graph and spawn briefs that scope a worker's surface.
- the verification standard: the evidence standard, the diagnosis discipline, and the caps that bound every `RETURNS`.
- [topologies](topologies.md) the canonical review graph and shape cost arithmetic these patterns resolve to.
- [memory](memory.md) what survives a session boundary, and why a rule that lives only in the conversation does not.
