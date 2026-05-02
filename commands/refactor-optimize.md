---
description: Refactor and optimize code — measure, analyze, refactor, verify, sync
agent: implementer
---

Refactor and optimize the specified code. Execute the full workflow below without stopping for confirmation between steps.

$ARGUMENTS

## Workflow

1. **Establish baseline** — Run benchmarks, profiling, or performance tests to capture current characteristics. If none exist, write them first. Record numbers — no optimization without measurement.
2. **Analyze** — Identify bottlenecks, code smells, unnecessary allocations, and structural issues using the analysis checklists below.
3. **Plan** — Describe the refactoring or optimization approach before making changes. State the expected improvement and risk.
4. **Refactor** — Make one small, incremental change at a time. Verify each step before proceeding.
5. **Verify** — Re-run benchmarks/tests after each change to confirm improvement without regressions. If results are ambiguous, revert.
6. **Sync** — Update spec/plan to reflect structural changes. Logic corrections: spec first, then code. Refactoring: code first, then spec.

**Do not stop after analysis.** Proceed through all six steps autonomously. Only pause if tests fail and you cannot resolve the failure — in that case, report what happened and revert the last change.

## Analysis Checklists

### Memory & Allocation

- [ ] Pre-allocate collections (arrays, lists, maps) when size is known or estimable to avoid costly resizes and rehashes
- [ ] Reuse objects and buffers instead of creating new ones in hot paths (object pools, buffer recycling)
- [ ] Minimize data copying — prefer references, slices, or views over full duplication
- [ ] Check data layout alignment — order fields by descending size to reduce padding waste
- [ ] Avoid hidden allocations from unnecessary boxing, wrapping, or interface conversions
- [ ] Keep hot-path data on the stack where possible — pass by value for small structs, avoid escaping to heap
- [ ] Be frugal with memory — process data in chunks rather than loading everything at once; reuse buffers across iterations
- [ ] Reduce garbage collection pressure by minimizing short-lived heap allocations in tight loops

### Concurrency & Synchronization

- [ ] Use concurrency sparingly — only introduce when the problem demands it, not by default
- [ ] Keep concurrent workers confined — control lifetime explicitly; ensure all workers terminate before the enclosing scope exits
- [ ] Use fixed-size worker pools to bound resource usage instead of unbounded spawning
- [ ] Prefer atomic operations and lightweight locks over heavy synchronization primitives
- [ ] Share immutable data between threads without locks; make defensive copies for mutation
- [ ] Delay expensive initialization until actually needed (lazy initialization)
- [ ] Propagate cancellation and timeouts through context or equivalent signal mechanism

### I/O & Throughput

- [ ] Use buffered I/O to batch system calls and reduce per-operation overhead
- [ ] Batch small operations together to reduce round trips and improve throughput
- [ ] Prefer sequential reads over random access where possible — optimize for disk/cache locality
- [ ] Close and release resources promptly; use deterministic cleanup (try-with-resources, defer, using, etc.)

### Structure & Readability

- [ ] Write packages, not programs — keep entry points thin; push logic into importable, testable modules
- [ ] Flatten cognitive speed-bumps — extract low-level "paperwork" into named helper functions with informative names
- [ ] Use consistent, conventional naming (`err` for errors, `ctx` for contexts, `req`/`resp` for requests, `buf` for buffers, etc.)
- [ ] Write code for reading, not writing — ask a reviewer to read it line by line; their stumbles reveal your speed-bumps
- [ ] Decouple code from environment — only entry points should access env vars, CLI args, or OS details; inject configuration explicitly
- [ ] Avoid mutable global state — use explicit dependency injection; no package-level mutable variables

### Safety & Error Handling

- [ ] Design types so invalid states are unrepresentable — use "always valid values" and validating constructors
- [ ] Use named constants instead of magic values
- [ ] Validate all inputs at boundaries; reject early
- [ ] Always check errors — handle when possible, retry when appropriate, report otherwise
- [ ] Wrap errors with context; don't flatten them into strings. Preserve the error chain for callers
- [ ] Define named sentinel errors users can match against
- [ ] Reserve panics/exceptions for internal program errors only; show usage hints for bad input instead of crashing
- [ ] Never log secrets or personal data

## Rules

- **One change at a time.** Verify before proceeding.
- **Never change observable behavior during refactoring** — only structure.
- If a refactoring requires behavior change, treat it as a logic correction (fix spec first).
- Always run tests before and after each change.
- If no tests or benchmarks exist, write them first.
- Never break existing public APIs.
- Make it work first, then make it right. Optimize only after correctness is proven.
- Summary of changes and verification results should be included in the report.
- **Execute the full workflow.** Do not stop after analysis to ask what to do. Analyze, plan, refactor, verify, and sync in sequence.
- If analysis finds nothing to improve, say so and stop — no refactoring needed.
