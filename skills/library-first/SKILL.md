---
name: library-first
description: Library-first architecture patterns — every feature begins as a reusable library/module with clean interfaces. Use when designing architecture, creating new features, structuring packages, or when the user mentions library-first, modular design, or package architecture.
---

# Library-First Architecture

## Core Principle

Every feature begins as a standalone, reusable library/module with clean interfaces. **The entry point is last, not first.**

## Architecture Layers

Build bottom-up. Each layer depends only on layers below it.

1. **Domain/Library** — Pure logic, no I/O, no framework dependencies. Does the real work.
2. **Infrastructure** — Adapters for external systems (DB, HTTP, filesystem). Implements domain interfaces.
3. **Entry Point** — Parses arguments, handles errors, wires dependencies, orchestrates. Thin and minimal.

**Dependency direction:** Entry Point → Infrastructure → Domain. Never upward.

## Module Design

- Keep modules under 400 lines; extract when larger
- Single, clear responsibility per module
- Define clean interfaces at module boundaries
- Prefer composition over inheritance
- No circular dependencies between modules

## Interface Design

- Define interfaces where the **consumer** needs them, not where the implementation lives
- Keep interfaces small — favor single-method interfaces where practical
- Accept interfaces, return concrete types
- Hide implementation details behind interfaces only when they provide sufficient benefit

## Dependency Injection

- Domain packages receive configuration, not fetch it
- Only entry points access env vars, CLI args, or OS details
- Don't assume filesystem paths, writable storage, or `$HOME`
- Pass dependencies as constructor parameters, not global state

## Package Naming

- Name packages by what they **provide**, not what they contain
- Avoid generic names: `util`, `helper`, `common`, `misc`
- Use lowercase, concise, single-word names where possible
- Optimize for the call site: `csv.NewReader()` over `helper.NewCSVReader()`

## Checklist

Before writing an entry point:
- [ ] Domain logic exists as a standalone, testable library
- [ ] All external dependencies are behind interfaces
- [ ] Configuration is injected, not fetched
- [ ] No business logic in the entry point
- [ ] Module is under 400 lines
