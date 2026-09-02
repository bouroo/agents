# Architecture Modeling

Models are communication tools, not art. Every diagram owes its reader a question answered; a diagram with no audience is deleted, not filed.

## C4 — the default zoom ladder

Zoom from the whole system to a class; pick the level matching the audience:

| Level | Shows | Audience |
|---|---|---|
| 1 · System context | system + users + external systems | executives, sponsors, everyone |
| 2 · Containers | deployable units, tech choices, inter-communication | delivery team, architects |
| 3 · Components | inside one container: responsibilities + tech | implementers |
| 4 · Code | classes/interfaces | rarely drawn — the code already shows it |

## Other notations, by job

| Job | Notation |
|---|---|
| Interactions over time, API contracts | sequence diagram |
| Domain events, bounded contexts discovery | event storming (workshop, not a diagram) |
| Business process, handoffs | BPMN (events/activities/gateways, pools = orgs, lanes = roles) |
| State machines (lifecycle, protocol) | state diagram |
| Deployment topology | deployment diagram |
| Enterprise layers (business/application/technology) | ArchiMate |

UML is fine where teams already read it; consistency within a diagram beats notation purity across them.

## Views beyond structure

The **4+1 model** keeps you honest that structure alone is not architecture: logical (function) · process (concurrency, runtime) · physical (deployment) · development (code organization) · use-case scenarios tying them together. A structural diagram that ignores runtime behavior hides the interesting decisions.

## Drawing practice

- One notation per diagram; legend when anything is non-obvious.
- Consistent direction (top-to-bottom, left-to-right); group related elements; label every arrow with what flows.
- Audience-first detail: executives get context diagrams, not swim lanes.
- Version-control the source (Mermaid/PlantUML/C4-DSL in-repo beats screenshot tools); stale diagrams mislead worse than none — keep current or delete.
- Accessibility: don't encode meaning in color alone.

## Pitfalls

Over-modeling (detail no reader needs) · under-modeling (one box labeled "system") · mixed notations in one diagram · pet vases (beautiful, outdated) · tool-first thinking — pick the practice, then the smallest tool that supports it.
