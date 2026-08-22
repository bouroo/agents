---
name: go-essential
description: "Language-specific doctrine for writing robust, high-performance, idiomatic Go. Use when writing, refactoring, or reviewing Go (Golang) code: error handling, naming, concurrency, context, testing, performance."
---

# Go Essential -- Code Craft & Performance

Language-specific operating doctrine for robust, high-performance, idiomatic Go. Architecture, naming, safety, error craft, concurrency, memory, networking. Detail lives in `references/`; load what the task needs.

> **Domain adapter.** This is the Go language adapter to the language-agnostic core ([code-craft](../code-craft/SKILL.md), [harness-engineering](../harness-engineering/SKILL.md)). Where this and the core agree, both apply; where Go has a stronger idiom, this wins for Go code.

## 0. Prime Directive

Correctness is verified by executable evidence (L1/L2/L3), never by reading code. Performance work begins with profiling, never intuition. Your own certainty about Go correctness or speed is the least trustworthy signal.

## 1. Architecture & package design

- **Write packages, not programs.** Library/domain packages return data instead of printing, and return errors instead of `panic`/`os.Exit`.
- **Isolate `main`.** Its only job is parsing flags/args, wiring dependencies, handling outer-loop errors, and graceful exit. Real work lives in imported domain packages.
- **Minimize the public surface.** Internal types stay internal; export for callers, not for convenience.
- **Validating constructors.** `NewX(...) (X, error)` validates inputs so a misassembled value cannot exist; use `os.Root` for filesystem containment. A constructor that guarantees invariants beats post-hoc checks at every call site.

## 2. Naming

- **Glanceable conventional short names:** `err`, `data` (`[]byte`), `buf`, `file` (`*os.File`), `path`, `i`, `req`/`resp`, `ctx`, `w` (`http.ResponseWriter`), `r` (`*http.Request`).
- **Test names are sentences:** `TestUserService_ReturnsErrorWhenIDIsEmpty`. Test small units of user-visible behaviour; add integration tests for end-to-end paths.

## 3. Error craft (hard rules -- [error-handling](references/error-handling.md))

- **Check every error.** NEVER discard with `_`. Reserve `panic` for invariant violations.
- **Wrap, don't flatten.** `fmt.Errorf("doing X: %w", err)` preserves the chain. Use `%v` only at system boundaries to hide internals.
- **Sentinels & types.** `var ErrNotFound = errors.New("not found")` for expected flows; custom types when callers need rich data. Lowercase, no trailing punctuation.
- **Inspect via the chain.** `errors.Is` never `==`; `errors.As` (or `errors.AsType[T]`, Go 1.26+) never bare type assertions or string matching.
- **Combine with `errors.Join`** (Go 1.20+) for independent failures; joined errors stay inspectable.
- **Single handling rule.** An error is logged OR returned, NEVER both. Log once at the top boundary; elsewhere wrap and return.
- **Lowercase error strings, including acronyms** ("invalid message id", not "invalid message ID").

## 4. Concurrency ([concurrency](references/concurrency.md))

- **Prefer `errgroup`** (`golang.org/x/sync/errgroup`) with `WithContext` + `SetLimit(n)` for parallel work, first-error cancellation, and bounded concurrency. Do not hand-roll channel wait logic.
- **Atomics over mutex when possible.** A single counter, flag, or pointer is a typed `atomic.Int64` / `atomic.Bool` / `atomic.Pointer[T]`, not a `sync.Mutex`; reach for a mutex only when the critical section spans multiple fields or guards an invariant.
- **Prefer `wg.Go`** (Go 1.25+) for fire-and-wait; call `wg.Add(1)` before `go`, never inside.
- **Channels: one owner.** The writer closes; readers never close. Pre-spawn checklist: who writes, who closes, what happens on close.
- **Avoid `panic`/`recover` as control flow.** Panic allocates a stack trace and unwinds; use error returns.

## 5. Memory & performance ([performance](references/performance.md))

- **Preallocate** slices when the size is known (`make([]T, 0, n)`) to avoid reallocation.
- **Escape analysis first.** Profile before optimizing; `go build -gcflags="-m"`.
- **`sync.Pool`** for reusable scratch buffers; avoid interface boxing on hot paths.
- **Iterators** (`iter.Seq`, Go 1.24+) for lazy/streaming; `b.Loop()` in benchmarks.

## 6. Logging & observability

- **Structured logging** (`log/slog`). Stable message templates (`slog.Error("db connection failed")`); high-cardinality data (IDs, counts) as attributes, never formatted into the message.
- **Never log secrets.**

## 7. Testing

- **Table-driven tests:** `[]struct{ name string; in input; want output; wantErr error }`. Test names are sentences.
- Cover happy, error, and edge paths; at least one integration test for end-to-end.

## 8. Modernize

- `sync.OnceFunc`/`OnceValue`/`OnceValues` (Go 1.21+); `wg.Go` (Go 1.25+); iterators (Go 1.24+); `slices.SortFunc` over `sort.Slice`; `math/rand/v2`; PGO (`-pgo=auto`).
- `govulncheck` in CI; `golangci-lint` v2 with `modernize`. Migrate with `gopls` rename; run `go vet` + `golangci-lint` after each step.

## Common mistakes

| Smell | Fix |
|---|---|
| `err == sql.ErrNoRows` | `errors.Is(err, sql.ErrNoRows)` |
| `err.(*MyError)` bare assertion | `errors.As(err, &target)` / `errors.AsType[T]` |
| `panic(err)` for expected failure | Return the error |
| Unbounded goroutines | `errgroup` + `SetLimit(n)` |
| `append` in a loop without prealloc | `make([]T, 0, n)` |

## References

- [error-handling](references/error-handling.md) sentinels vs types, `%w` vs `%v`, `errors.Is`/`As`/`Join`, single handling rule.
- [concurrency](references/concurrency.md) channel ownership, channel vs mutex vs atomic, sync primitives, pipelines, `goleak`.
- [performance](references/performance.md) escape analysis, preallocation, `sync.Pool`, pprof workflow.
- [networking](references/networking.md) client/server timeouts, transport tuning, resilience, `httptrace`.
