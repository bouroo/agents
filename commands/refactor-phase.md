---
description: Refactor phase  --  analyze, plan, baseline, execute, and verify with tests
---

# Refactor Phase

A language-agnostic refactoring workflow. Apply engineering norms and performance patterns **after** correctness is proven; measure before and after; keep only what the data supports.

> **Agent:** requires `edit` + `bash`  --  run on the implementing/build agent, not `plan` or `conductor`.

Target area (optional): **$ARGUMENTS**. If empty, ask the user which module/package/path to target before analyzing.

---

## 1. Analyze

Map the target area, its dependencies, and call sites. Identify the smell, not just the symptom.

**Structural smells** (top 3  --  full set in [effective-code-craft](../skills/effective-code-craft/SKILL.md) "Structure & Coupling"):

- Mutable global state mutated from multiple call sites.
- Tight coupling to environment (env vars, CLI args, FS paths deep in domain packages).
- Monolithic entry points doing real work instead of parsing, delegating, and handling errors.

**Performance smells** (top 3  --  full patterns in [performance-patterns](../skills/performance-patterns/SKILL.md)):

- Unnecessary allocations in hot loops; missing preallocation when final size is known.
- Unbuffered I/O; per-element syscalls or DB queries that should be batched.
- Heap escapes from pointers-to-locals, interface boxing, or large closure captures.

**Correctness smells** (top 3  --  full hard rules in [effective-code-craft](../skills/effective-code-craft/SKILL.md) "Hard rules"):

- Unchecked errors  --  discarded returns, ignored error channels, `_` assignments.
- In-band errors  --  sentinels like `-1`, `null`, empty string instead of explicit error returns.
- Error string inspection  --  comparing messages with `==`/`contains` instead of typed/sentinel matching.

Run CPU, memory, and I/O profilers. Identify the top contributors. Record heap profiles and allocation counts. These measurements form the basis for all subsequent decisions.

---

## 2. Plan

Write a REASONS canvas  --  see `AGENTS.md` "Workflow". Lock scope explicitly. Mark unknowns; tests and benchmarks are part of the plan, not an afterthought.

---

## 3. Baseline

Before touching production code, capture or write tests and benchmarks for the target area. The baseline must prove current behavior and, if performance is a goal, current metrics. No refactor proceeds without a reproducible before/after comparison.

- Write tests that read as sentences about behavior. Cover happy path, error path, and edge cases.
- Add integration tests for end-to-end flows.
- Record benchmark numbers: latency percentiles, throughput, allocation count, heap size.
- Commit the baseline. Every subsequent change must be measured against it.

---

## 4. Execute

Make small, atomic commits. Keep the build green at every step. Preserve public behavior. When principles conflict, clarity wins over concision, simplicity over concision, and maintainability over consistency.

**Apply engineering norms**  --  see `AGENTS.md` "Code Craft Norms" and [effective-code-craft](../skills/effective-code-craft/SKILL.md) (Architecture, Safety, State & Concurrency, Observability).

**Apply performance patterns**  --  see `AGENTS.md` "Performance Discipline" and [performance-patterns](../skills/performance-patterns/SKILL.md). Apply only after correctness is proven; measure before/after; revert regressions.

---

## 5. Verify

Run formatter, linter, type-checker, and full test suite. Re-profile and re-benchmark against the baseline to confirm improvement, not regression. If any metric regresses, revert and re-plan. Do not ship a refactor that trades correctness or performance for aesthetics.

---

## 6. Sync Spec

Update or create the spec to match the refactor; never leave the spec describing the old shape. When code and spec diverge, fix the spec first, then the code. A stale spec is a bug.

Sync also covers the repo-local `docs/` tree when one exists: **if the repo maintains a `docs/` tree**, and the refactor moves or renames the important source files a doc points to, update the affected system or flow doc **and its Source map** so links still resolve and the doc still points at the code it describes.
