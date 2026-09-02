# Governance & Assessment

Governance is guardrails, not roadblocks: enough structure that fifty teams make compatible decisions, not so much that innovation queues behind a board. Assess maturity before prescribing process — controls a Level 1 org cannot operate are decoration.

## Operating models

| Model | Shape | Fits |
|---|---|---|
| Centralized | one authority decides | regulated industries, small orgs |
| Decentralized | domains decide | fast-moving, high-autonomy cultures |
| **Federated** | central principles, domain execution | most large enterprises |

## Machinery

- **Standards hierarchy**: principles (few, durable) → standards (mandated: security, data, APIs) → guidelines (recommended patterns) → emerging (experimental, time-boxed). Every mandated standard needs a stated rationale and an exception path.
- **Architecture review board**: cross-functional (chief architect, domain architects, senior engineers, security, ops, business). Triage reviews by risk: simple → automated checks; moderate → peer review; complex/high-risk → board. If the queue is weeks long, the board is a bottleneck — push more decisions to automated conformance.
- **Exception management**: an exception request names the standard, justification, risk assessment, alternatives tried, mitigation, and an expiry date. Expired exceptions are compliance failures, not paperwork.
- **Compliance metrics**: standards adherence %, security-control coverage, documentation currency, review completion, exception rate (target <10% — more means the standards, not the teams, are wrong).

## Automated conformance over meetings

Prefer executable governance: architecture-conformance tests (dependency rules), policy-as-code on IaC, SAST/dependency scanning, fitness functions in CI (see [quality attributes](quality-attributes.md)). A review board should judge what cannot be automated — trade-offs, context, strategy.

## Maturity levels

| Level | Name | Signature |
|---|---|---|
| 0–1 | None / Initial | ad hoc, no documentation, reactive |
| 2 | Developing | basic standards, project-level reviews, informal governance |
| 3 | Defined | formal process, documented standards, governance body |
| 4 | Managed | metrics-driven decisions, compliance measured |
| 5 | Optimizing | adaptive, innovation budget, industry leadership |

Assessment = current state → target state → gap analysis → roadmap → (crucially) implementation. Annual deep assessment + quarterly health checks on key metrics; an assessment that produces no resourced actions is shelfware.

## Technology portfolio

Classify each technology; act accordingly:

| Stage | Action |
|---|---|
| Emerging | experiment, time-boxed, low investment |
| Strategic | invest, set standards, grow skills |
| Utility | maintain efficiently, standardize |
| Legacy | strict governance, sunset plan, no new features |

Track vendor support status, vulnerability exposure, maintenance-cost trend, skill availability — health, not age, decides sunset.

## Anti-patterns

Ivory tower (governance without practitioners) · standards for their own sake (no rationale, no measurement) · bureaucracy (weeks-long approval for reversible decisions) · exception creep (standards dissolve one waiver at a time) · assessment theater (measurement without follow-through).
