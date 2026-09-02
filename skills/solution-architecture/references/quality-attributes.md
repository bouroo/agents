# Quality Attributes

Quality attributes are the real requirements of architecture: users never complain that a system has clean code, they complain when it is slow, down, or breached. Each attribute has named **tactics** (design decisions that achieve it) and predictable **trade-offs** against the others.

## Catalog

| Attribute | Sub-characteristics | Measured by |
|---|---|---|
| **Performance** | time behavior, resource utilization, capacity | response time (p95/p99), throughput, utilization |
| **Reliability** | maturity, availability, fault tolerance, recoverability | MTBF, MTTR, uptime %, RTO/RPO |
| **Security** | confidentiality, integrity, non-repudiation, accountability, authenticity | incidents, detection time, control coverage |
| **Usability** | learnability, operability, error protection, accessibility | task completion, satisfaction, error rate |
| **Maintainability** | modularity, reusability, analysability, modifiability, testability | change lead time, coupling metrics, coverage |
| **Scalability** | horizontal, vertical, elastic | load-test ceilings, cost per unit of load |

Specify each as an SEI scenario (see [requirements](requirements.md)).

## Tactics

| Attribute | Tactics |
|---|---|
| Performance | control demand (reduce overhead, manage event rate, sample) · manage resources (increase, concurrency, replicas) · bound usage (execution time, queue sizes, allocations) |
| Reliability | prevent (transactions, removal from service) · detect (ping/echo, heartbeat, exceptions, checksums) · recover (active/passive redundancy, rollback, retry) |
| Security | detect attacks (IDS, integrity checks) · resist (authenticate, authorize, encrypt, limit exposure) · react (revoke, lock, notify) · recover (audit trail, restore) |
| Usability | support user initiative (cancel, undo, multiple views) · support system initiative (task/user/system models) |
| Maintainability | localize change (semantic coherence, anticipate change) · prevent ripple (hide information, stable interfaces, intermediaries) · defer binding (config, runtime registration, polymorphism) |
| Scalability | distribute load (balancing) · replicate (data, cache copies) · partition (functional, data sharding) |

## Trade-offs

Attributes never improve together; pick your conflicts deliberately.

| Pair | Coupling |
|---|---|
| Security ↔ performance | encryption/CORS/auth add latency; caching can help both |
| Consistency ↔ availability | CAP: partitions force a choice; sagas/eventual consistency buy availability |
| Performance ↔ maintainability | clever optimizations obscure code; good modularity serves both |
| Availability ↔ cost | every extra nine multiplies infrastructure and operational complexity |
| Security ↔ usability | MFA/complex policies add friction; SSO improves both |

## Testing map

| Attribute | Tests |
|---|---|
| Performance | load (expected), stress (beyond), spike (sudden), volume (data), endurance (leaks over time) |
| Security | SAST, DAST, dependency scanning, penetration test, compliance check |
| Usability | user tests, A/B, accessibility audit, heuristic review |
| Reliability/availability | chaos/failure injection, DR drill, failover test |
| Maintainability | fitness functions, architecture-conformance tests, static analysis |

**Fitness functions**: encode scenarios as automated checks in CI — `assert p95_latency < 200ms`, dependency-direction tests, policy-as-code on IaC. A quality attribute without at least one executable check is a hope.

## Pitfalls

Ignoring NFRs until production · vague quality requirements · unexamined trade-offs · testing quality only at the end · one-size-fits-all targets (a prototype does not need five nines).
