---
name: incremental-delivery
description: Use when planning features, sprints, or release milestones. Deliver value in small, verifiable increments.
---

# Incremental Delivery

## Core Principle
Ship small units of working software frequently. Each increment is:
- **Functional** — Adds measurable value
- **Verifiable** — Has clear acceptance criteria
- **Reversible** — Can be rolled back if needed

## Feature Breakdown
Break features along user-visible boundaries:
1. Identify minimum viable feature
2. Ship core path first with error handling
3. Add edge cases and optimizations later
4. Never merge incomplete error handling

## Ship Criteria
- Tests pass (unit + integration)
- Linter passes
- No hardcoded values that should be config
- Observability: logging, metrics, or tracing added

## Merge Strategy
- **Small, frequent merges** over large, infrequent ones
- **Trunk-based development** with feature flags when needed
- **Never merge broken builds** to main

## Review Checklist
- [ ] Feature works for the primary use case
- [ ] Error paths handled gracefully
- [ ] Tests cover core behavior
- [ ] No TODO comments or placeholder names
