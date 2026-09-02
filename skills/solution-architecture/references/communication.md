# Communication & Practice

Architecture that is not communicated does not exist. Same design, different altitude per audience — and the delivery practice (agile architecture, documentation, tooling) decides whether the design survives contact with the codebase.

## Presentations by audience

**Executive (15–20 min)**: business context → solution overview (one diagram, key decisions) → plan & risks → investment/ROI → Q&A. Business value first; no component names.

**Technical (45–60 min)**: context & requirements (functional + NFRs + constraints) → C4 context/container overview → detailed design (interactions, data, integration, security) → implementation approach → open questions. Decisions and trade-offs on screen, not buried in an appendix.

Tailor by stakeholder role: executives get strategic impact and risk, users get workflow impact, engineers get specifications, ops gets runbooks and failure modes.

## Architecture document skeleton

Executive summary → context & requirements (incl. ASR scenarios) → architecture overview (context + container diagrams) → detailed design (components, data, integration, security) → quality attributes (scenarios + tactics chosen) → implementation considerations → risks & mitigations → decisions (ADR index) → appendices.

Keep it thin: the doc indexes and links (ADRs, diagrams, fitness tests); it does not duplicate them. Documentation-as-code — Markdown/diagrams-in-repo, reviewed in PRs, versioned with the system.

## Agile architecture

- **Just enough, just in time**: frame the load-bearing decisions early (boundaries, data ownership, NFR tactics), defer the rest until the requirement is real.
- **Walking skeleton**: first milestone is the thinnest end-to-end slice through every layer — it proves the architecture, pipeline, and integration assumptions, not a feature.
- **Architecture stories / NFRs in the backlog**: quality work gets scheduled, not wished for.
- **Evolutionary design with guardrails**: fitness functions + conformance tests enforce the invariant parts so refactoring can move the rest (see [quality attributes](quality-attributes.md)).
- Refactoring cadence to pay architecture debt before it compounds.

## Workshops

- **Event storming**: domain experts + engineers, orange sticky notes for domain events in time order, then commands, then bounded contexts. Fastest route to a defensible domain model.
- **Decision workshops**: options pre-read → structured trade-off discussion → ADR drafted in the room, not after.
- Every workshop produces an artifact (map, ADR, decision list) or it was a meeting.

## Tool selection

Pick practices first, tools second. Weighted-matrix discipline for any consequential pick:

| Criterion (example weights) | What it captures |
|---|---|
| Functionality (30%) | does it do the job at your scale |
| Team fit (25%) | skills, learning curve, ops burden |
| Integration (20%) | fits the existing toolchain, SSO, API |
| Cost (15%) | license + implementation + training |
| Vendor health/support (10%) | will it exist and answer tickets |

Score independently, sanity-check the winner against the team that will live with it. Diagram/doc tooling: prefer in-repo, text-source tools (Mermaid/PlantUML/ADR markdown) so models version with code; heavier EA suites only when regulatory or portfolio demands require them.

## Pitfalls

One deck for every audience · documentation that duplicates instead of links · big design up front (BDUF) after the requirements stopped being real · tool shopping as a substitute for practice decisions · workshops without artifacts.
