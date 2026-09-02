# Delivery Contexts

The same architecture discipline wears different hats per engagement stage: business framing, estimation, presales, cloud/infrastructure.

## Business framing

- **Capabilities = what, stable** ("expense management") vs **processes = how, volatile** ("submit expense report"). Anchor the target architecture to capabilities; processes change faster than systems.
- **Capability map** (3–4 levels deep) × maturity (1 ad-hoc → 5 optimizing) × strategic importance → heat map → investment priority. Gaps between maturity and importance are the roadmap.
- **Value streams**: end-to-end request→delivery; measure lead time vs process time — the ratio is process efficiency; handoff waits, not work, are usually the bottleneck.
- **Transformation**: strangler fig over big-bang replacement (incremental value, reversible); API-first wrapper around legacy buys integration while replacement proceeds.
- **Stakeholder power × interest grid**: manage closely (high/high) · keep satisfied (power, low interest) · keep informed (interest, low power) · monitor. Tailor altitude per audience.

## Estimation

Units: story points (relative, team-velocity conversion) · ideal days · t-shirt sizes (low-ceremony triage) · hours (contracts).

Techniques:

| Technique | Shape | Use when |
|---|---|---|
| Three-point (PERT) | E = (O+4M+P)/6, σ=(P−O)/6, quote E±2σ | always, as the base |
| Analogous | scale from a similar past project | historical data exists |
| Planning poker / Wideband Delphi | independent estimates, discuss spread, converge | team scoping; anonymity counters anchoring |
| Parametric (COCOMO, function points) | model from size drivers | contract-grade defensibility |

Biases to name and counter: optimism/planning fallacy (three-point), anchoring (independent-first estimates), Parkinson's law (effort not calendar padding), scope creep (assumptions + change process in the estimate). Give ranges, never points.

## Presales architecture

- **Qualify**: budget/authority/need/timeline/competition, plus technical fit (complexity, integrations, performance/security asks).
- **RFI** (capability survey) ≠ **RFP** (full solution proposal — comply with every requirement, differentiate on value) ≠ **RFQ** (price-led).
- **HLD** skeleton: executive summary → system overview → components → integration points → tech stack → deployment → security → performance → risks. WBS decomposes it to estimable work packages.
- **Pricing models**: fixed price (client gets certainty, vendor carries risk — needs airtight scope), T&M (flexibility, client carries budget risk), hybrid (fixed core + T&M for change), outcome/value-based (shared risk, requires measurable outcomes). Scope assumptions and change process belong in the proposal, not in hallway agreements.
- Credibility is the product: honest risks in the proposal beat an optimistic bid that fails delivery.

## Cloud & infrastructure

- **Service models**: IaaS (max control) · PaaS (managed runtime) · SaaS (buy the capability) — buy at the highest level that meets the requirements.
- **Deployment models**: public (elastic, cheapest start) · private (control/compliance) · hybrid (regulatory data local, burst elastic) · multi-cloud (leverage/bargaining power — pay for it in duplicated ops skills).
- **Compute**: VMs → containers/K8s → serverless (event-driven, pay-per-use, cold starts and vendor coupling).
- **Resilience ladder (RTO/RPO vs cost)**: backup/restore (hours/hours, cheapest) → pilot light (minutes) → warm standby → active-active multi-region (seconds/near-zero, expensive).
- **Cost discipline**: right-size, autoscale, reserved for steady load, spot for fault-tolerant work, tag for allocation, review continuously.
- **Security**: least-privilege IAM, encryption at rest/in transit, defense in depth, zero trust posture.
- **IaC**: declarative desired state (Terraform/CloudFormation/Bicep) over imperative scripts — reviewable, repeatable, auditable. Lift-and-shift without refactoring forfeits most cloud value.

## Further reading

Bass, Clements, Kazman — *Software Architecture in Practice* · Fowler — *Patterns of Enterprise Application Architecture* · Kleppmann — *Designing Data-Intensive Applications* · Newman — *Building Microservices* · Ford et al. — *Building Evolutionary Architectures* · Evans — *Domain-Driven Design* · McConnell — *Software Estimation*.
