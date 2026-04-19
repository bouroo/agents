---
description: Refactor & optimize code for quality and performance without breaking public API
---
# Refactor & Optimize

Refactor the specified target `$ARGUMENTS` (or current working directory if not specified) for readability, quality, and performance while preserving the public API contract (exported symbols, signatures, behavior, and tests must remain compatible). benchmark results must not regress beyond noise threshold.

## Step 1 — Analyze

1. Read the target file(s) or module identified by `$ARGUMENTS`. If `$ARGUMENTS` is empty, use the current working directory (`.`) as the target.
2. Identify the public API surface: exported functions, types, methods, constants, and their call sites across the codebase (use `grep` to find usages).
3. Run existing tests to establish a green baseline (use `bash`). Record the test command for re-validation.
4. If no tests exist for the target code, write essential valid tests covering core functionality before making any refactoring changes. Tests must verify current behavior so refactoring can be validated against them.
5. Run pprof and heap profilers to identify performance bottlenecks.

## Step 2 — Apply Refactoring Principles

Apply the following language-agnostic rules. Only refactor what improves the code — do not make changes for the sake of change.

### Naming & Readability
- **Casing**: camelCase for local, PascalCase for exported. Acronyms keep uniform case (`HTTPClient`, `userID` — not `HttpClient`, `userId`).
- **Length**: Short for narrow scope (loop vars, lambdas); descriptive for broad scope (public functions, types).
- **Avoid repetition**: Don't repeat package/type context at call site (`customer.New()`, not `customer.NewCustomer()`).
- **No type encoding**: `count` not `countInt`. Exception: type-conversion disambiguation.
- **No shadowing**: Avoid names that clash with standard library or built-ins.

### Code Structure
- **Minimal visibility**: Write shy code — only expose what consumers need; prefer unexported helpers.
- **Extract helpers**: Break long routines into small, named functions to reduce cognitive load.
- **Valid initial state**: Constructors/factories must guarantee usable defaults; use With-style configurators for optional params.
- **Named constants**: Prefer constants over magic values.

### Error Handling
- **Always propagate**: Never silently ignore errors.
- **Wrap with context**: Add source, operation, and key values so call chains are traceable.
- **Sentinel errors**: Define public sentinel errors for matching; never compare error strings.

### State & Concurrency
- **Explicit dependencies**: Avoid mutable global state; pass dependencies as parameters.
- **Structured concurrency**: Ensure all async work terminates before the enclosing scope exits.
- **Immutable sharing**: Share immutable data across concurrent boundaries; use atomics for simple shared counters.

### Performance — Memory
- **Preallocate**: Allocate collections with capacity upfront when size is known to avoid dynamic resizes.
- **Pool high-churn objects**: Reuse objects via pooling to reduce GC pressure.
- **Minimize padding**: Order struct fields by descending alignment size (pointers/large scalars first).
- **Avoid interface boxing**: Keep concrete types on hot paths to prevent hidden heap allocations.
- **Zero-copy**: Use sub-slicing, buffer reuse, and reference passing instead of copying large data.
- **Stack over heap**: Keep values local, pass by value when small, avoid escaping pointers to locals.

### Performance — Concurrency
- **Worker pools**: Use fixed-size pools to cap resource usage; avoid unbounded goroutine/thread spawning.
- **Atomics over locks**: Use atomic primitives for simple shared state; reserve mutexes for complex state.
- **Lazy init**: Delay expensive setup (pools, caches, configs) until first use.
- **Propagate cancellation**: Pass timeouts, deadlines, and cancel signals through all concurrent work.

### Performance — I/O
- **Buffered I/O**: Wrap readers/writers with buffered equivalents to minimize syscalls.
- **Batch operations**: Combine small writes, DB inserts, or network sends into batches.

### Performance — Compiler
- **Leverage inlining**: Enable inlining for hot paths; use inline hints where supported.
- **Respect escape analysis**: Keep hot values on the stack; avoid capturing loop vars in closures or storing refs in interfaces.

### Verification — Before & After
- **Benchmark before**: Run the project's benchmark suite (or write one if none exists) and record baseline results (throughput, latency, memory allocations, GC pauses).
- **Measure before**: Capture baseline metrics (complexity, performance, memory, line count) before refactoring.
- **Benchmark after**: Re-run the same benchmark suite under identical conditions and compare results against baseline.
- **Compare results**: Present a before/after table showing key metrics (ns/op, B/op, allocs/op, throughput, p99 latency). Result must be strictly better or neutral — never worse.
- **Quality gates**: Refactor is only acceptable if it reduces complexity, improves performance, or enhances readability without degrading any other metric.
- **Reject regression**: If any metric worsens, revert or iterate until metrics improve or stay neutral.

### Observability
- **Actionable logs only**: Never log secrets or personal data.
- **Structured logging**: Use key-value pairs or JSON for machine readability.
- **Tracing over logs**: Use tracing for request-scoped debugging, metrics for performance data.

## Step 3 — Validate

1. Re-run the test command from Step 1. All tests must pass.
2. Run the project's linter (use `bash` to run the appropriate lint command for the ecosystem).
3. Verify no public API symbols were removed or had their signatures changed (use `grep` to confirm call sites still compile/resolve).
4. Run benchmarks and compare before & after results. Display a comparison table (ns/op, B/op, allocs/op, throughput). If any metric regresses beyond noise threshold, investigate and fix before proceeding.

If any step fails, fix the issue and re-validate until all checks pass.
