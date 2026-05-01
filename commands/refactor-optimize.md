---
description: Refactor and optimize code — improve readability, performance, safety, and maintainability
---

# Refactor & Optimize

Improve code for readability, performance, maintainability, and safety.

## Phase 1: Measure

1. **Profile** — run existing benchmarks or write new ones to establish baselines
2. **Identify bottlenecks** — use profiling tools or instrumentation to find hot paths
3. **Read the code** — understand current behavior, tests, and architecture

## Phase 2: Refactor (no behavior change)

4. **Identify improvement areas**:
   - Long functions that need extraction
   - Duplicated logic across files
   - Magic values that need named constants
   - Unclear names that need renaming
   - Deep nesting that needs flattening
   - Missing error handling
5. **Refactor incrementally** — one change at a time, verify after each:
   - Run tests after each change
   - Keep changes small and reviewable

## Phase 3: Optimize (may change internal behavior, preserve external behavior)

6. **Apply optimization patterns**:
   - Memory preallocation and object pooling
   - Avoiding unnecessary allocations
   - Algorithmic improvements (better data structures, early termination)
   - I/O reduction (batching, connection pooling, streaming)
   - Concurrency (worker pools, lock-free patterns) — only when justified by profiling
   - Caching with explicit invalidation
7. **Benchmark after each optimization** — compare against baselines
8. **Verify** — all existing tests still pass; no regressions

## Phase 4: Sync

9. **Update spec** — if a Canvas exists in `plans/`, sync structural and performance changes back (Code → Spec)

## Rules

- **External behavior preservation**: Observable external behavior must not change
- **Benchmark first**: Never optimize without measuring — guesswork wastes time
- **Small steps**: Each change independently verifiable
- **Test between steps**: Run tests after each change
- **No new features**: Don't add functionality during refactoring
- **Document trade-offs**: Note what was optimized and what was sacrificed (readability, memory, etc.)
