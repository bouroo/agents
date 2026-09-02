# Requirements Analysis

Requirements → architecture → technology, in that order. The architect's job is not to collect all requirements but to find the few that shape the structure — **Architecturally Significant Requirements (ASRs)** — and make the rest traceable.

## Functional vs non-functional

- **Functional**: what the system does — behaviors, features, business rules.
- **Non-functional (quality attributes)**: how well it does it — the primary drivers of architecture and the usual cause of failed projects when left implicit.

## ASR criteria

A requirement is architecturally significant when it has:

1. **High business impact** — critical to success, not a nicety.
2. **Technical complexity** — forces real design consideration.
3. **Cross-cutting scope** — touches multiple components or teams.
4. **Quality-attribute focus** — mostly non-functional.
5. **Stakeholder priority** — named as important by decision holders.

ASR card:

```
ID: ASR-007                Title: Response time under peak load
Description: respond within 2 s for 95% of transactions at peak
Quality attribute: performance
Business justification: checkout abandonment
Stakeholders: end users, business owner        Priority: High
Acceptance: p95 ≤ 2 s under 3,000 concurrent users, incl. network latency
```

## SEI quality-attribute scenarios

Non-functional requirements are only testable in scenario form — six parts:

```
When <source> <stimulus> under <environment>,
the <artifact> shall <response>, measured by <response measure>.
```

| Attribute | Example scenario |
|---|---|
| Performance | user submits search / normal load / search system / returns results / ≤ 2 s for 95% at 1k concurrent users |
| Availability | server fails / normal operations / system / keeps processing / failover ≤ 30 s, 99.9% uptime |
| Security | unauthorized user requests data / normal ops / API / denies + logs / 100% of attempts logged within 1 s |

Anti-requirement: "the system shall be fast." If no response measure, it is not a requirement — it is a wish.

## Elicitation

Interviews (per stakeholder group) · workshops · observation of real work · document/system analysis · prototypes to force reactions. Combine at least two; single-technique elicitation reproduces one stakeholder's blind spots.

## Prioritization

- **MoSCoW** — Must / Should / Could / Won't (this release). Simplest contract with the business.
- **Value vs effort** — quick wins (high/low) first, then major projects (high/high); avoid-question anything low value regardless of effort.
- **Kano** — basics (expected), performance (linear), excitement (delighters); excitement features decay into basics.

## Traceability

Maintain the chain business goal → requirement → decision (ADR) → test. Uses: impact analysis on change, coverage proof, audit compliance. A requirement with no test and no decision is decoration.

## Pitfalls

- Functional-only analysis — quality attributes surface at the first peak load, too late.
- Vague NFRs ("user-friendly", "fast") — convert to scenarios or drop.
- Requirements creep without change control — route additions through impact analysis.
- Missing stakeholders — map power × interest first (see [governance](governance.md)).
