---
name: architecture
description: "Design and document software architecture, domain language, and system diagrams: distill architecturally significant requirements, pin quality attributes as measurable SEI scenarios, choose patterns by context and tradeoff, record decisions as ADRs, model in C4 views, keep the CONTEXT.md glossary opinionated, select GoF design patterns with the no-pattern gate, and render systems as self-contained interactive HTML from a typed JSON IR with a bundled validator. Use when designing or reviewing architecture, writing ADRs/HLDs/proposals, defining non-functional requirements, shaping domain terms and bounded contexts, choosing a pattern (refactoring.guru / GoF) or making code extensible, or visualizing architecture, workflows, sequences, pipelines, and state machines."
---

# Architecture

Architecture is the set of trade-offs you can defend: requirements inform architecture inform technology, never in reverse; every significant choice names what it neglected, and every quality claim carries a measure. Domain language, design patterns, and diagrams are one discipline at different zoom levels.

**When to load:** designing or reviewing a system or a structure-changing evolution; writing ADRs / HLDs / SADs / proposals; framing ASRs and non-functional requirements; choosing a pattern; shaping a domain glossary; selecting a GoF pattern; or rendering a system map. **Not for:** code-level craftsmanship, measured hot paths, or proving a build ([quality](../quality/SKILL.md)); the delivery lifecycle itself ([delivery](../delivery/SKILL.md)).

## Solution Architecture

Requirements before shapes. Separate **Architecturally Significant Requirements (ASRs)** — high business impact, cross-cutting, quality-attribute-focused — from ordinary ones, and pin every non-functional requirement (quality attributes) as a six-part **SEI scenario**: `When <source> <stimulus> under <environment>, the <artifact> shall <response>, measured by <measure>`. "Fast" and "scalable" are wishes: no response measure means no requirement. Keep the traceability chain business goal → requirement → decision → test.

Start with the simplest style that meets the ASRs and evolve on evidence: modular monolith for most new products, clean/hexagonal inside a service for complex long-lived domains, microservices only for many teams with divergent scaling. Style catalog, quality-attribute tactics, predictable conflicts, and anti-patterns: [architecture patterns](references/architecture-patterns.md), [quality attributes](references/quality-attributes.md), [clean architecture](references/clean-architecture.md).

One **ADR** per significant choice, written when options were weighed and the choice binds future work; skip standards-covered or throwaway calls. The value is the neglected alternative: *In context X, facing requirement Y, we decided Z, neglecting A and B, to achieve C, accepting D.* Records are immutable — supersede, never rewrite. Trigger, MADR template, practices, pitfalls: [decisions](references/decisions.md).

Model for the audience with the **C4** zoom ladder (system context, container, component, code); one notation per diagram, current or deleted. Zoom ladder and drawing practice: [modeling](references/modeling.md). Federation, guardrails, and maturity: [governance](references/governance.md). Per-audience presentation: [communication](references/communication.md). ASRs, elicitation, and traceability: [requirements](references/requirements.md).

**Done** when every ASR has a measurable scenario, every significant decision has an ADR naming rejected alternatives, the C4 context and container views render at their audience's zoom, and each automatable scenario is encoded as a fitness function or test.

## Domain Modeling

The active discipline for a project's domain language — when you are changing the model, not consuming it. A project-level glossary or decision-record convention that explicitly supersedes these rules wins. Five habits: challenge terms against the glossary; sharpen fuzzy or overloaded language to one canonical term; stress-test relationships with concrete edge-case scenarios; cross-reference code claims (authority rank: user statement > spec > checks > code); update the glossary inline, never batched. End when every term under discussion is pinned or explicitly deferred — an unresolvable term is an open question, not a guess.

`CONTEXT.md` at the repo root is a glossary and nothing else — no implementation detail, not a spec or scratchpad. Be opinionated: pick the best term, list the rest under `_Avoid_`; keep definitions to one or two sentences and context-specific terms only. Create it lazily on the first resolved term; multi-context repos add a `CONTEXT-MAP.md` charting each context. Entry rules and the map template: [context format](references/context-format.md). Offer a decision record only when the choice is hard to reverse, surprising without context, and a real trade-off; format and lifecycle are the ADR rules above, never a second template.

## Design Pattern Selection

Catalog anchor: [refactoring.guru/design-patterns](https://refactoring.guru/design-patterns) — 22 GoF patterns. Decision-first: most requests need no pattern, and modern languages collapse several classics into plain idioms.

Pin the pain (a concrete symbol or file), the variation axis, and the language's existing idioms. Restate the pain as one variation sentence; then apply the **no-pattern gate** first — if the variation is hypothetical, the plain solution is under ~50 lines with no duplication, or a library already owns it, answer "no pattern" and give the plain code. Shortlist at most 2 candidates, look for the collapse (two pains, one mechanism), and check language reality: first-class functions absorb Strategy/Command-lite/Template Method, Observer needs a second subscriber, Singleton is usually stdlib or DI. Deliver: verdict (pattern name or "no pattern") → why (pain vs buy/cost) → minimal skeleton in the user's language → the change that should trigger revisiting. On a tie take the candidate with fewer new types; if the user insists on a named pattern with no pain, implement it and flag the cost. Pain→pattern table, per-pattern intent / use when / skip when / shape, example, and cross-cutting notes: [GoF patterns](references/gof-patterns.md).

## System Diagramming

One deliverable: a single self-contained HTML file — an inline-SVG system map drawn deterministically from a typed JSON **IR contract** embedded in the file, with dark/light themes, pan/zoom, hover tracing, and node search. Layout judgment is the agent's; drawing is the template's. Copy the [template](references/template.html) per run, author only its `ir` block, and gate with the stdlib [validator](references/validate.py) — execute it, never edit it. No installs, no network; exports, motion, and share cards are out of scope (the browser's screenshot/print covers them).

Choose the kind — `architecture`, `workflow`, `sequence`, `dataflow`, `lifecycle`. Author the IR first: ≤ 12 primary nodes, one obvious main path, roles as the palette (`frontend` `backend` `database` `cloud` `security` `messagebus` `external` `state` `participant`), semantic edge labels naming protocol/action/direction, exact product and protocol names preserved, at most 3–4 cards each visible in the diagram. Then copy the template and replace its `ir` block, writing `<slug>.html`.

Validate: `python3 skills/architecture/references/validate.py <slug>.html`. `E_*` lines are defects — fix the diagnosed subject and rerun (3-cycle cap); `W_*` lines are judgment calls to resolve or knowingly accept. Prove it renders with one real look (open it or take a headless-browser screenshot); no browser, say so and hand over the validated file. Iterate by editing the `ir` block in place — it is the source of truth — and never edit the renderer. Mermaid in: read it for topology and meaning, then author fresh IR (`flowchart`/`graph` → `workflow`, `sequenceDiagram` → `sequence`, `stateDiagram` → `lifecycle`); never carry Mermaid styling over. Report the artifact path, kind, and validator receipt (0 errors).

Load the reference the question at hand needs; each SKILL.md section links the one that answers it.