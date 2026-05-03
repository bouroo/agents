---
name: incremental-delivery
description: Patterns for shipping software incrementally — feature flags, small PRs, phased rollouts, and backward-compatible deployments.
version: 1.0.0
triggers:
  - shipping incrementally
  - feature flag design
  - phased rollouts
  - breaking changes
---

# Incremental Delivery

Patterns for shipping software in small, safe increments.

## Principles

### Small PRs
- Each PR does one thing. If you need "and" to describe it, split it.
- PRs should be reviewable in under 30 minutes.
- Prefer 5 small PRs over 1 large one.
- Every PR must leave the codebase in a working state.

### Feature Flags
- Gate new features behind flags. Deploy disabled, enable incrementally.
- Flags are temporary. Remove them once the feature is fully rolled out.
- Flag names describe the feature, not the implementation.

### Backward Compatibility
- Additive changes first. Deprecation second. Removal last.
- Never break the public API in a single commit.
- Provide migration paths with versioned endpoints or adapters.

### Phased Rollout
1. **Develop**: Behind a flag, in a feature branch.
2. **Test**: Integration tests pass. Staging validated.
3. **Release**: Deploy to production, flag disabled.
4. **Enable**: Turn on for internal users, then percentage, then all.
5. **Clean up**: Remove the flag and old code paths.

## Checklist

- [ ] Change broken into smallest reviewable units
- [ ] Feature flag used for risky or incomplete changes
- [ ] Backward compatibility maintained
- [ ] Rollback plan defined
