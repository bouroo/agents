---
name: incremental-delivery
description: Patterns for shipping software incrementally — feature flags, small PRs, phased rollouts, and backward-compatible deployments.
---

# Incremental Delivery

## Core Principle

Ship working slices, one step at a time. Each increment should be independently verifiable and deployable.

## Practices

### Small Batches
- Each change should be reviewable in under 15 minutes
- One concern per PR/commit — don't bundle refactoring with features
- If a change touches >10 files, split it

### Feature Flags
- Gate new features behind flags for safe rollout
- Flags should be simple booleans, not complex conditional trees
- Remove flags promptly after rollout completes
- Never use flags for authorization logic

### Backward Compatibility
- Additive changes first: new fields, new endpoints, new parameters
- Deprecation period for removals
- Version APIs explicitly when breaking changes are unavoidable
- Dual-write during migrations: write both old and new, read from old, then switch

### Phased Rollout
1. **Implement** behind flag — deploy without exposing
2. **Internal testing** — enable for team
3. **Beta** — enable for subset of users
4. **General availability** — enable for all
5. **Cleanup** — remove flag and old code path

### Integration Points
- Contract tests between services before deployment
- Smoke tests after deployment
- Rollback plan documented before each release

## Anti-patterns

- Big-bang releases that require coordinated deployment
- Long-lived feature branches that diverge from main
- Flags that stay in the codebase indefinitely
- Skipping rollback planning
