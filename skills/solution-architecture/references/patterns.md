# Architectural Patterns

Patterns are the trade-off catalog: each buys some quality attributes at the price of others. Choose by context and ASRs, not fashion; start simple and evolve on evidence.

## Styles

| Style | Buys | Costs | Choose when |
|---|---|---|---|
| **Monolith** | simplicity, atomic deploys, easy debugging | scales only as a unit, tech lock-in | small teams, simple domain, prototypes |
| **Layered** | familiar separation (UI/business/data) | anemic domains, change ripples through layers | traditional business apps, green teams |
| **Modular monolith** | monolith simplicity + module boundaries ready for extraction | discipline required to keep modules honest | default for most new products |
| **Microservices** | independent scaling/deploys, team autonomy, fault isolation | distributed-systems tax: latency, eventual consistency, ops burden | many teams, divergent scaling needs |
| **Event-driven** | loose coupling, async throughput, real-time reaction | eventual consistency, hard debugging, ordering concerns | integrations, high-volume streams, audit trails |

**Clean / hexagonal** (any style, at code level): dependencies point inward, business logic independent of frameworks and databases — full treatment in [clean-architecture](clean-architecture.md); use for complex domains and long-lived systems, skip for CRUD and prototypes.

**CQRS + event sourcing**: separate write model (normalized) from read models (denormalized, projected from the event log). Buys optimized reads/writes, perfect audit, time travel; costs eventual consistency and real complexity. Only for rich domains with audit or temporal needs — not a default.

## Data & scaling

- **Caching**: cache-aside (simple, read-heavy, eventually consistent) · write-through (consistent, slower writes) · write-behind (fast writes, data-loss window). Always name the invalidation strategy.
- **Sharding**: range / hash / directory / geographic; buys scale, costs cross-shard queries and rebalancing.
- **Load balancing**: round-robin, least-connections (long requests), weighted (heterogeneous capacity), session affinity (stateful — a smell; prefer stateless).

## Resilience

- **Circuit breaker**: closed → open (fail fast past threshold) → half-open (probe recovery). Stops cascade failures.
- **Retry with exponential backoff + jitter**: for transient faults only; idempotent operations only.
- **Bulkhead**: separate pools per criticality so one flood cannot sink the ship.
- **Health checks + graceful degradation**: know it is broken before the users tell you.

## Integration

- **API gateway**: single entry — routing, authn/authz, rate limiting, observability.
- **Messaging**: point-to-point queue (one consumer) vs publish-subscribe (fan-out); at-least-once delivery means consumers must be idempotent.
- **Saga** (distributed transactions): choreography (events, no coordinator — simple, hard to see) or orchestration (central coordinator — visible, a coupling point). Compensating actions replace rollback.
- **Strangler fig**: route traffic incrementally from legacy to new behind a facade; migrate by capability, delete legacy last.
- **Anti-corruption layer**: translate a legacy/external model at the boundary so it cannot infect your domain.
- **ETL vs ELT**: transform-before-load (traditional DW) vs load-raw-then-transform (lake, schema-on-read).

## API styles

| Style | Best for | Cost |
|---|---|---|
| REST | public/web APIs, CRUD, cacheability | over/under-fetch, chatty UIs |
| GraphQL | client-driven aggregation, many viewports | caching complexity, N+1 on the server |
| gRPC | internal service-to-service, streaming | browser/HTTP/2 friction, non-human-readable |

Version deliberately (URL path is the least surprising); never break a published contract without a version bump.

## Release patterns

Blue-green (two environments, instant switch/rollback) · canary (gradual traffic shift with metrics gates) · feature flags (decouple deploy from release, kill switches). All three assume observability good enough to judge the rollout.

## Security

- **Defense in depth**: perimeter (WAF, DDoS) → network (segmentation) → application (authn/z, input validation) → data (encryption at rest/in transit, key management) → audit.
- **Zero trust**: verify explicitly, least privilege, assume breach — identity per request, not per network location.
- **Authorization models**: RBAC (roles, simple), ABAC (attributes/policies, flexible, harder to audit).

## Anti-patterns

Golden hammer (one pattern for every problem) · architecture astronautics (building for imaginary scale) · copy-paste architecture (pattern without its context) · big ball of mud (no enforced boundaries) · premature optimization (complexity before measurement).

**Selection discipline**: name the ASRs the pattern serves, the attributes it degrades, and the team's ability to operate it — then pick the simplest survivor, and record it as an ADR (see [decisions](decisions.md)).
