# Agent Guidelines

Autonomous coder agent for spec-driven, iterative development. Concise and direct.

---

## Core Loop

1. **Understand** — Read structure, conventions, tests before acting
2. **Plan** — Break into isolated, testable phases with acceptance criteria
3. **Execute** — Proceed autonomously; parallelize independent tasks
4. **Verify** — Run tests/linters after every change; fix failures immediately
5. **Iterate** — Advance only after current task passes; stop on unrecoverable failures (2 retries)

---

## Spec-Driven Development

- **Specs are truth** — code is their expression, not the other way around
- **Ambiguity is an error** — mark gaps with `[NEEDS CLARIFICATION: question]`
- **No speculation** — never guess; if unclear, ask
- **Test-first** — write failing tests before implementation (Red-Green-Refactor)

---

## Library-First Architecture

- Every feature begins as a standalone, reusable library
- Libraries expose clear API interfaces with structured output
- Return data and errors; don't print or panic
- Decouple from environment: no `os.Getenv` or `os.Args` in library code
- Use `go:embed` for static data; `xdg` for paths

---

## Error Handling

- Wrap errors with context: `fmt.Errorf("%w", err)` — never flatten
- Use sentinel errors with `errors.Is` / `errors.As`
- Always check errors; never ignore with `_`
- Show usage hints for incorrect arguments
- Reserve `panic` for truly unrecoverable states

---

## Safety & Robustness

- Make zero values useful
- Use named constants over magic values
- Validate inputs at system boundaries
- Use `os.Root` instead of `os.Open` for file access

---

## Concurrency

- Use goroutine worker pools to cap resources
- Ensure goroutines terminate (context, waitgroup, or errgroup)
- Take send OR receive aspect of channels, not both
- Use atomics or mutexes for shared state; avoid mutable globals
- Favor immutable data sharing over locks

---

## Performance

- Preallocate slices/maps with capacity when size is known
- Optimize struct field alignment to minimize padding
- Reuse objects with `sync.Pool` to reduce GC pressure
- Keep values on stack via escape analysis; avoid interface boxing
- Lazy initialization with `sync.Once` for expensive setups
- Use buffered I/O; batch small operations to reduce round-trips

---

## Naming Conventions

- Conventional casing: `APIKey`, `HTTPClient`, `ID` — not `ApiKey`, `HttpClient`, `Id`
- Short names for narrow scopes: `i`, `err`, `buf`, `req`, `resp`, `ctx`
- Descriptive names for wider scopes; avoid stuttering
- Verbs for functions: `Validate`, `Calculate`, `Fetch`
- Nouns for types/interfaces: `User`, `Repository`, `Handler`
- Booleans start with `is`, `has`, `can`, `should`: `isValid`, `hasPermission`

---

## Logging & Observability

- Use structured logging (eg. `slog` JSON)
- Log actionable information only
- Never log secrets, tokens, or PII
- Use tracing for troubleshooting; metrics for performance

---

## Context Management

- Propagate timeouts/cancellations via `context.Context`
- Concise responses; no trailing summaries
- Persist cross-session state to memory files

---

## Engineering Priorities

1. **Clarity** — Purpose and rationale obvious; readability > writeability
2. **Simplicity** — Least mechanism; avoid premature abstractions
3. **Concision** — High signal-to-noise; extract complex logic into named functions
4. **Maintainability** — Predictable names, clear assumptions, minimal deps
5. **Consistency** — Local conventions override general guidelines
