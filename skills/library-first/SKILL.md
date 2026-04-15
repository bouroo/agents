---
name: library-first
description: Use when designing new functionality or extracting features from existing code.
---

# Library-First Architecture

## Core Principle
Every feature begins as a standalone, reusable library before becoming an application.

## Rules

1. **Isolate domain logic** — Extract packages that others can use; `main()` only parses flags
2. **Clear API surfaces** — Libraries expose explicit interfaces with structured output
3. **Return data and errors** — Don't print or panic from library code
4. **Decouple from environment** — No `os.Getenv`, `os.Args`, or filesystem paths in library code
5. **Use `go:embed`** for static data; `xdg` for paths when environment integration is needed

## Single Responsibility
A library does one thing well. If a package needs CLI printing, inject a `Logger` interface.

## Testability
Libraries must be testable without mocks. Design for constructor injection.

```
Package: validation → returns (Result, error)
Application: main → parses flags → calls validation → formats output
```
