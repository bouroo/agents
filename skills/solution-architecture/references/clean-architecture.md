# Clean Architecture

Organize code in concentric layers with one absolute rule: **all dependencies point inward**. Inner circles know nothing of outer ones — business logic never imports a framework, a database driver, or an HTTP concern. The outer layers are plugins to the core, replaceable without touching business rules. (Same family: hexagonal / ports-and-adapters, onion architecture.)

## The four layers

| Layer | Owns | May depend on | Examples |
|---|---|---|---|
| **Entities** (domain) | enterprise business rules: entities, value objects, domain services, domain events | nothing | `Order.ApplyDiscount()`, invariants |
| **Use Cases** (application) | application-specific rules: orchestrate entities, define transaction boundaries | entities | `ProcessOrderUseCase` |
| **Interface Adapters** | translate data between use-case format and external format | use cases, entities | controllers, presenters, repository implementations |
| **Frameworks & Drivers** | delivery mechanisms and tools | all inner layers | web framework, ORM, UI, external APIs |

Dependencies invert at the boundary: the use case defines a repository *interface*; the adapter layer *implements* it against the real database. The core owns the abstraction; infrastructure conforms to it.

## Principles at work

- **Dependency inversion** — high-level policy and low-level detail both depend on abstractions owned by the high-level side.
- **Separation of concerns** — one responsibility per layer; UI logic, business rules, and persistence never mix.
- **Testability** — run use cases in tests with in-memory fakes; no database, no HTTP, no container.
- **Independence** — swap framework, database, UI, or external agencies without rewriting business rules.

## When to use

✅ Complex business domains with lasting rules · long-lived systems expecting framework churn · high testability demands · multiple teams sharing one core · DDD practice.
❌ Simple CRUD · prototypes and spikes · performance-critical hot paths (mapping overhead) · small teams on throwaway scope — the layer tax buys nothing there.

## Pitfalls

| Pitfall | Correction |
|---|---|
| Anemic domain model — entities are data bags, logic leaks into services | behavior lives on entities; `user.CalculateAge()`, not a service call |
| Leaking infrastructure — `DbContext`/ORM types appear in use cases | core defines interfaces; adapters implement them |
| Interface sprawl — one interface per trivial service | abstract only at real substitution or test seams |
| Fat controllers — business rules in handlers | controllers parse HTTP, call a use case, format the response |
| Cross-layer entity passing — domain entities as API payloads | DTOs at the boundary; mapping is the cost of isolation |
| Circular dependencies | break with interfaces or domain events; never patch the dependency rule |

**Relation to system-level styles:** clean architecture governs the *inside* of a service; monolith/microservices/event-driven govern deployment and communication ([patterns](patterns.md)). A well-bounded modular monolith with clean internals is usually the right monolith — and the cheapest extraction path if services ever split.
