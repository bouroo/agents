---
name: solution-architecture
description: "Design and document solution architectures: distill architecturally significant requirements, pin quality attributes as measurable SEI scenarios, choose patterns by context and tradeoff, record decisions as ADRs, model in C4 views, and size/govern the delivery. Use when designing or reviewing a system's architecture, writing ADRs/HLDs/proposals, choosing between architectural patterns, or defining non-functional requirements."
---

# Solution Architecture

Architecture is the set of trade-offs you can defend. Requirements → architecture → technology, never in reverse; every significant choice names what it neglected; every quality claim carries a measure. There is no perfect architecture, only one fit to its context.

**When to load:** designing a system or a structure-changing evolution, writing ADRs / HLDs / SADs / proposals, choosing patterns, or defining NFRs. Not for code-level design — [craft](../craft/SKILL.md); measured hot paths — [performance](../performance/SKILL.md); proving the build — [verification](../verification/SKILL.md).

## 1. Frame: requirements before shapes

1. Separate **ASRs** from ordinary requirements — high business impact, cross-cutting, quality-attribute-focused ([requirements](references/requirements.md)).
2. Pin every NFR as an SEI scenario; "fast" and "scalable" are not requirements:

   > When a user submits a search under normal load, the search system shall return results within 2 s for 95% of requests at 1,000 concurrent users.

3. Prioritize (MoSCoW / value-vs-effort) and keep the traceability chain: business goal → requirement → decision → test.

## 2. Design: context picks the pattern

Start with the simplest style that meets the ASRs and evolve on evidence. Defaults by context:

| Context | Default architecture |
|---|---|
| Small team (<10), simple domain | Modular monolith, layered |
| Complex domain, long-lived | Clean/hexagonal + DDD bounded contexts |
| Multiple teams, independent scaling | Microservices + API gateway |
| Integration-heavy, async at scale | Event-driven (queue/bus, sagas) |
| Audit, temporal queries | Event sourcing (+ CQRS) |
| Prototype / MVP | Monolith on a familiar stack |

Pattern catalog with trade-offs: [patterns](references/patterns.md); the code-level dependency-inward discipline for complex domains: [clean architecture](references/clean-architecture.md). Quality-attribute tactics and their conflicts (e.g. security ↔ performance, availability ↔ consistency): [quality attributes](references/quality-attributes.md).

## 3. Decide: one ADR per significant choice

Write an ADR when options were weighed and the choice binds future work; skip it for standards-covered or throwaway calls. The value is the neglected alternative:

> In context X, facing Y, we decided Z, neglecting A and B, to achieve C, accepting D.

Keep records immutable — supersede, never rewrite. Templates, naming, lifecycle: [decisions](references/decisions.md).

## 4. Model for the audience

Diagrams are communication, not decoration. Zoom with C4: system context for executives and sponsors, containers for the delivery team, components for implementers; sequence diagrams for interactions; BPMN for process. One notation per diagram, current or deleted. Notation choices and drawing practice: [modeling](references/modeling.md); presenting it per audience and keeping the design alive in agile delivery: [communication](references/communication.md). To render one of these views as an explorable, self-contained system map, hand it to [system-diagramming](../system-diagramming/SKILL.md).

## 5. Size and govern the delivery

- **Estimate in ranges**: E = (O + 4M + P)/6, σ = (P − O)/6 — give E ± 2σ, never a point. Name the bias you are correcting (optimism, anchoring, scope creep).
- **Map stakeholders** on power × interest; manage closely only the top quadrant.
- **Govern with guardrails**: federated model, tiered standards, exceptions with expiry; assess maturity L0–L5 before prescribing process.
- Business capability/value-stream framing, estimation techniques, presales (RFP/HLD/pricing), cloud & DR choices: [delivery contexts](references/delivery-contexts.md). Governance models, review boards, portfolio, assessment checklists: [governance](references/governance.md).

**Termination:** an architecture deliverable is done when every ASR has a measurable scenario, every significant decision has an ADR naming rejected alternatives, the C4 context + container diagrams render at their audience's zoom level, and each scenario that can be automated is encoded as a fitness function or test — an architecture review yielding no executable check is a narrative, not a design (§7 of the manifesto).
