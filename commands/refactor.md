---
description: Refactor & optimize code for quality and performance without breaking public API
agent: code
---
# Refactor & Optimize

Refactor the specified target `$ARGUMENTS` for readability, quality, and performance while preserving the public API contract (exported symbols, signatures, behavior, and tests must remain compatible).

## Step 1 — Analyze

1. Read the target file(s) or module identified by `$ARGUMENTS`. If `$ARGUMENTS` is empty, use `question` to ask which file(s) or module to refactor.
2. Identify the public API surface: exported functions, types, methods, constants, and their call sites across the codebase (use `grep` to find usages).
3. Run existing tests to establish a green baseline (use `bash`). Record the test command for re-validation.

## Step 2 — Apply Refactoring Principles

Apply the following language-agnostic rules. Only refactor what improves the code — do not make changes for the sake of change.

### Naming & Readability
- Use consistent casing conventions (camelCase for local, PascalCase for exported). Acronyms keep uniform case (e.g., `HTTPClient`, not `HttpClient`; `userID`, not `userId`).
- Scope-appropriate length: short names for narrow scope (loop variables, lambdas), descriptive names for broad scope (public functions, types, constants).
- Eliminate chattery names — avoid repeating the package or type context at the call site (e.g., `customer.New()` not `customer.NewCustomer()`).
- Do not encode types in identifiers (e.g., `count` not `countInt`). Exception: type-conversion disambiguation.
- Avoid identifiers that clash with standard library or built-in names.

### Code Structure
- Write shy code: default to minimal visibility. Only expose what consumers need; prefer unexported/internal helpers.
- Extract small, named helper functions from long routines to reduce cognitive load and document intent through function names.
- Initialize objects in a valid state. Constructors or factory functions should guarantee usable defaults; use With-style configurators for optional parameters.
- Prefer named constants over magic values.

### Error Handling
- Always check and propagate errors — never silently ignore them.
- Wrap errors with context (source, operation, key values) so the call chain is traceable.
- Define sentinel errors for public matching; do not compare error strings.

### State & Concurrency
- Avoid mutable global state. Pass dependencies explicitly as parameters.
- When concurrency is needed, use structured patterns: ensure all async work terminates before the enclosing scope exits.
- Share immutable data across concurrent boundaries; use atomic operations for simple shared counters.

### Performance — Memory Management & Efficiency
- **Object Pooling**: Reuse objects via pooling for high-churn allocations to reduce GC pressure and allocation overhead.
- **Memory Preallocation**: Allocate collections (slices, maps, lists, buffers) with capacity upfront when the size is known or estimable to avoid costly dynamic resizes.
- **Struct/Record Field Alignment**: Order fields by descending alignment size (pointers and large scalars first) to minimize padding, reduce struct size, and improve cache locality.
- **Avoid Interface Boxing**: Prevent hidden heap allocations by avoiding unnecessary interface/abstract conversions on hot paths — keep concrete types where the indirection isn't needed.
- **Zero-Copy Techniques**: Minimize data copying with sub-slicing, buffer reuse, and reference passing instead of copying byte slices, strings, or large records.
- **Reduce Heap Usage**: Minimize heap allocations to reduce GC overhead. Reuse memory buffers across iterations rather than allocating fresh ones.
- **Stack Over Heap**: Favor stack allocation by keeping values local, passing by value when small, and avoiding escapes (e.g., don't return pointers to locals, don't store references in heap-escaped closures). Prefer value receivers for small structs.

### Performance — Concurrency & Synchronization
- **Worker Pools**: Control concurrency with a fixed-size pool to cap resource usage; avoid unbounded spawning of goroutines/threads.
- **Atomic Operations**: Use atomic primitives or lightweight locks for shared counters and flags — avoid heavy mutexes for simple state.
- **Lazy Initialization**: Delay expensive setup (connection pools, caches, parsed configs) until first use using once-style initialization primitives.
- **Immutable Data Sharing**: Share data safely across concurrent boundaries without locks by making it immutable (copy-on-write, frozen collections).
- **Context/Cancellation Propagation**: Propagate timeouts, deadlines, and cancel signals through all concurrent work to prevent leaked goroutines/threads.

### Performance — I/O Optimization & Throughput
- **Buffered I/O**: Wrap raw readers/writers with buffered equivalents to minimize syscalls and I/O round-trips.
- **Batching**: Combine multiple small operations (writes, DB inserts, network sends) into batches to reduce per-call overhead and improve throughput.

### Performance — Compiler & Build Tuning
- **Compiler Flags**: Where applicable, leverage optimization flags (e.g., inlining thresholds, dead-code elimination, size optimizations) for hot packages/modules.
- **Escape Analysis**: Analyze which values escape to the heap and restructure code to keep them on the stack (avoid returning pointers to locals, capturing loop variables in closures, storing references in interface values).

### Logging & Observability
- Log only actionable information. Never log secrets or personal data.
- Use structured logging (key-value pairs or JSON) for machine readability.
- Prefer tracing for request-scoped debugging, metrics for performance data — not logs.

## Step 3 — Validate

1. Re-run the test command from Step 1. All tests must pass.
2. Run the project's linter (use `bash` to run the appropriate lint command for the ecosystem).
3. Verify no public API symbols were removed or had their signatures changed (use `grep` to confirm call sites still compile/resolve).

If any step fails, fix the issue and re-validate until all checks pass.
