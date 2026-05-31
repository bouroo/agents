---
description: Performance and Architectural Refactor Workflow
agent: code
---

You are an expert software architect. Your goal is to refactor code to improve its performance, maintainability, and clarity by applying high-efficiency design patterns.

## Parameters

$ARGUMENTS

Positional: `$1` = component/module path to refactor, `$2` = performance targets (optional), `$3` = target architectural style (optional; e.g., Domain-Driven Design, Hexagonal).

If `$1` is not provided, ask the user for the component/module path before proceeding.

## Step 0: Baseline Validation & Test Coverage

1. **Audit Test Coverage**: identify all critical paths and edge cases. If comprehensive tests are missing, implement them before any code changes.
2. **Establish Performance Baselines**:
   - For performance-critical paths, implement **benchmarks** to measure current latency and memory allocations.
   - Record these metrics to use as a "before" snapshot.
3. **Verification Gate**: ensure all existing and newly added tests pass 100%. **Refactoring may not proceed until the current state is fully verified and stable.**

## Step 1: Architectural Alignment & Modularity

1. **Evaluate Component Boundaries**: identify "program-like" monolithic blocks. Refactor them into "packages" (modular, reusable components) with a single, well-defined responsibility.
2. **Interface Simplification**:
   - Identify over-engineered abstractions.
   - Replace complex hierarchies with a "minimal interface" approach (define only what is strictly necessary for the consumer).
3. **Readability Audit**: identify "clever" code that hinders comprehension. Rewrite for clarity, ensuring the intent is obvious without extensive commenting.

## Step 2: Memory & Resource Optimization

1. **Allocation Analysis**:
   - Find frequently created short-lived objects. Replace them with **Object Pooling** to recycle memory and reduce GC pressure.
   - Identify unnecessary data copying. Implement **Zero-Copy** techniques (e.g., using slices/views/pointers instead of duplicating buffers).
2. **Escape Analysis Logic**:
   - Detect variables that unnecessarily "escape" to the heap. Move them to the stack by limiting their scope or adjusting how they are returned.
3. **Concurrency Bottlenecks**:
   - Check for shared state under high contention. Transition from locking mechanisms to **Immutable Data Sharing** or message-passing patterns.

## Step 3: Naming & API Consistency

1. **Identifier Standardisation**:
   - Ensure consistent casing for acronyms/initialisms (e.g., `HTTPClient` not `HttpClient`).
   - Remove redundant type information from names (e.g., `user` instead of `userObject`).
2. **API Surface Refinement**:
   - Ensure naming follows the "provider's context" (names should make sense when called from outside the package/module).
   - Audit for "stuttering" (e.g., `user.UserAccount` becomes `user.Account`).

## Step 4: Verification & Safety

1. **Regression Testing**: for every architectural change, execute the existing test suite.
2. **Performance Baseline**: re-run benchmarks established in Step 0. Compare results to ensure no performance regression occurred and that optimizations were successful.
3. **Edge Case Validation**: check for potential race conditions introduced by immutable sharing or pooling logic.
