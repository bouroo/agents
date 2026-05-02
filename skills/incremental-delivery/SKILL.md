---
name: incremental-delivery
description: Patterns for shipping software incrementally — feature flags, small PRs, phased rollouts, and backward-compatible deployments.
---

# Incremental Delivery

## Core Principle

Ship working slices, one step at a time. Each increment independently verifiable and deployable.

## Practices

### Small Batches
- Reviewable in under 15 minutes
- One concern per PR/commit
- >10 files → split it

### Feature Flags
- Simple booleans, not complex conditional trees
- Remove promptly after rollout completes
- Never use flags for authorization logic

### Backward Compatibility
- Additive changes first: new fields, endpoints, parameters
- Deprecation period for removals
- Dual-write during migrations

### Phased Rollout
1. **Implement** behind flag
2. **Internal testing** — enable for team
3. **Beta** — enable for subset
4. **GA** — enable for all
5. **Cleanup** — remove flag and old code path

## Anti-patterns

- Big-bang releases requiring coordinated deployment
- Long-lived feature branches diverging from main
- Flags that stay in the codebase indefinitely
- Skipping rollback planning
