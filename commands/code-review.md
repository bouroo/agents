---
description: Review code changes for quality, security, and performance issues
---

# Code Review

Check every change against these lenses:

- **Correctness** — does it satisfy the spec's acceptance criteria? Edge cases handled? Tests cover happy, error, and boundary paths? Tests fail with clear messages: input, actual, expected.
- **Safety** — invalid states unrepresentable? Errors wrapped with context and propagated, never discarded silently? No panics for normal control flow, no mutable globals? Prefer synchronous APIs; if concurrent, make lifetimes obvious. Beware accidental aliasing from shallow copies.
- **Performance** — allocations, copies, and locks justified? Hot paths preallocated, pooled, or stack-allocated where applicable? No N+1 I/O, no unbounded buffering? Pass small, immutable values by value, not by reference.
- **Readability** — names match scope (short local, long global) and casing conventions; functions short; no dead code or speculative features. Keep the normal path at minimal indentation; handle errors first and return early. Break lines by semantics, not width. Every public API has a doc comment and a usage example.
- **Spec alignment** — every change is traceable to a REASONS canvas section; orphans in either direction are flagged. Define abstractions (interfaces) on the consumer side; return concrete types.
