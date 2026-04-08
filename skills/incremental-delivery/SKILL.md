---
name: incremental-delivery
description: Shipping small vertical slices, feature flags, and progressive rollout strategies. Use when the user mentions incremental delivery, feature flags, small PRs, or iterative development.
---

# Incremental Delivery

Ship small, working, verified increments. Each increment is a vertical slice that delivers end-to-end value.

## Vertical Slice Strategy

- Each PR/change is a complete, reviewable, deployable unit
- Slice by use case, not by layer — not "all models" then "all APIs"
- Every slice must pass all tests and lint checks independently
- Prefer 5-10 small PRs over 1 large PR

## Feature Flags

- Wrap new features behind flags for safe rollout
- Flags allow merging incomplete work without exposing it to users
- Remove flags after full rollout — don't accumulate technical debt
- Flag naming: descriptive, tied to the feature (e.g., `enable-new-checkout-flow`)

## Progressive Rollout

1. Develop behind a flag — off by default
2. Enable for internal testing (dogfood)
3. Enable for a small percentage of users (canary)
4. Gradually increase to 100%
5. Remove the flag

## PR Discipline

- One logical change per PR
- PR description explains **what** and **why**, not how
- Include a test plan in the PR description
- Keep PRs under 400 lines changed for thorough review
- If a PR needs "Part N" in the title, consider merging incrementally instead

## Branching Strategy

- Short-lived feature branches merged frequently into main
- Avoid long-running branches that diverge from main
- Rebase or merge from main daily to minimize integration conflicts
