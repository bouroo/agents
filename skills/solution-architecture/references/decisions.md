# Decision Records

ADRs are the "why" log of the codebase: what was decided, what was considered and rejected, and what it costs. The neglected alternative is usually more valuable than the rationale — it prevents relitigating and shows today's reviewer the exit ramps.

## When to write one

Write when: multiple viable options existed · the choice binds future work · teams disagreed · the effect crosses teams or systems.
Skip when: a standard or policy already covers it · the choice is temporary/experimental · scope, cost, and risk are trivially small.

## MADR-style template

```markdown
# ADR-007: Choose PostgreSQL over MongoDB for order data

## Status
Accepted (2026-08-30) — supersedes ADR-003

## Context
High-volume transactions, need horizontal scaling; team has SQL depth.

## Decision drivers
Sub-100ms queries · 1M+ users · consistency requirements · team expertise · cost

## Considered options
- PostgreSQL — ACID, team expertise, complex-query performance
- MongoDB — flexible schema, weaker cross-document transactions
- Cassandra — write scale, no ad-hoc queries

## Decision
PostgreSQL; scale via read replicas, shard by tenant if needed.

## Consequences
Positive: ACID, SQL ecosystem, existing skills.
Negative: schema discipline up front; sharding is a future project.

## Links
Related: ADR-003 (previous data store choice)
```

Lightweight alternative — **Y-statement** (one line, big decisions in flight):

> In context X, facing requirement Y, we decided Z, neglecting A and B, to achieve C, accepting D.

## Practices

- **One decision per record**; title as imperative verb phrase, kebab-case (`choose-database.md`), stored in-repo (e.g. `docs/adr/`).
- **Immutable**: never edit a superseded record — new status + new ADR pointing back. History is the asset.
- **Write during the decision**, not archaeology afterward; context decays in weeks.
- **Include business context** so non-engineers can audit the reasoning.
- Keep statuses moving (`proposed → accepted → superseded`); a stale "proposed" pile means the process is theater.
- Link related records — decisions form a graph, not a list.

## Pitfalls

Only the winner documented (no alternatives) · after-the-fact records with lost context · records so technical the business cannot audit them · statuses never updated · one template regardless of decision size.
