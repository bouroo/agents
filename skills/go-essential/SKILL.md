---
name: go-essential
description: Language-specific instructions for writing robust, high-performance, and idiomatic Go code. Emphasizes error handling, readability, concurrency, and memory optimization. Use this skill whenever you are writing, refactoring, or reviewing Go (Golang) code.
---

# Go Essential Code Craft & Performance (go-essential)

Language-specific operating doctrine for writing robust, high-performance, idiomatic Go  --  architecture, naming, safety, error craft, concurrency, memory, and networking. External sources are consolidated in the repo README.

Use this skill whenever you are writing, refactoring, or reviewing Go code. Detail lives in the reference files under `./references/`; load only what the current task needs.

## 0. Prime Directive

Correctness is verified by executable evidence (L1/L2/L3), never by reading code. Performance work begins with profiling, never intuition. Treat your own certainty about Go correctness or speed as the least trustworthy signal.

## 1. Architecture & Package Design

- **Write packages, not programs.** Library/domain packages return data instead of printing and return errors instead of calling `panic` or `os.Exit`.
- **Isolate `main`.** Its only job is parsing flags/arguments, wiring dependencies, handling outer-loop errors, and graceful exit. The real work lives in imported domain packages.
- **Keep the module structure simple.** Default to a single package; avoid premature package explosion. Use `internal/` for code not intended for import.
- **Decouple code from the environment.** Do not call `os.Getenv` or `os.Args` deep inside packages  --  accept config structurally at the boundary. Do not assume `$HOME`, disk writability, or root privileges.
- **Bundle static assets** with `//go:embed`; do not require external config files at runtime. Distribute single binaries.

## 2. Naming, Readability & Line of Sight

- **Glanceability via conventional short names:** `err` errors, `data` arbitrary `[]byte`, `buf` buffers, `file` `*os.File`, `path` pathnames, `i` index, `req`/`resp` request/response, `ctx` contexts, `w` `http.ResponseWriter`, `r` `*http.Request`.
- **Test names are sentences:** `TestUserService_ReturnsErrorWhenIDIsEmpty`. Test small units of user-visible behaviour; add integration tests for end-to-end paths.
- **Semantic line breaking.** Lines past ~120 characters MUST break at semantic boundaries. Calls with 4+ arguments MUST use one argument per line.
- **Flat flow.** Return early via guard clauses. Avoid `else` after a `return`. Use `continue` inside loops to keep the happy path on the left edge.
- **Extract paperwork.** Move low-level prep (`createRequest`, `parseResponse`) into named helpers so the top-level function reads like prose.
- **MixedCaps, never underscores.** Use MixedCaps (`MaxRetries`, `parseHTTPResponse`); casing controls export. No `ALL_CAPS`, `snake_case`, or Hungarian notation (`kMax`).
- **Avoid stutter.** Call sites include the package name: write `http.Client` not `http.HTTPClient`, `user.New()` not `user.NewUser()`. Names MUST NOT repeat package or type context.
- **Lowercase error strings, including acronyms.** Write `"invalid message id"`, not `"invalid message ID"`; package-prefixed sentinels use `errors.New("apiclient: not found")`.
- **godoc is the doc convention -- `//` only, begin with the name.** Every exported identifier (function, type, constant, variable) takes a `//` comment directly above it that opens with the identifier name as a complete sentence: `// UserByID returns the user with the given id, or ErrNotFound.` Unexported code takes no comment unless a *why* is non-obvious; a performance *why* cites the benchmark. Use `//`, never `/* */`; one `// Package name ...` comment on exactly one file per package. Banners (`// ===== helpers =====`) and code-restating comments (`// loop over users`) are noise -- omit them.
- **Make enum zero values sentinels.** Put `StatusUnknown`/`StatusInvalid` at `iota` 0 so an uninitialized value is not a real state.
- **Boolean fields ask a question.** Use `is`/`has`/`can` (`isConnected`, `hasPermission`); exported getters keep the prefix (`IsConnected()`).
- **Signal initialization intent.** Use `:=` for non-zero values (`name := "default"`) and `var` for zero-value initialization (`var count int`).

### Declarations

- **Initialize slices and maps explicitly.** Nil maps panic on write; nil slices serialize as `null` rather than `[]`. Use `[]T{}`, `map[K]V{}`, or `make` when capacity is known.
- **Name composite literal fields.** `&http.Server{Addr: ":8080"}` survives added or reordered fields; positional literals do not.
- **Switch over repeated comparisons.** Prefer `switch` for one variable; use `switch {}` with default-then-override for mutually exclusive assignments.
- **Keep functions to ≤4 parameters.** Beyond that, group inputs into an options struct. Order `ctx`, inputs, then outputs.
- **Prefer `range` over index loops.** Use `range n` (Go 1.22+) for simple counting.

## 3. Safety by Default

- **Make zero values useful.** Prefer `var items []string` over `items := []string{}` when no init logic is needed. A zero-value `sync.Mutex`, `bytes.Buffer`, `http.Server` must be ready to use.
- **Validating constructors.** When a struct has invariants, expose an unexported zero value and a `NewX()` constructor that validates. Add configuration via `WithX` builders: `NewWidget().WithTimeout(time.Second)`.
- **Named constants, not magic values.** `http.StatusOK` is self-explanatory; `200` is not. Use `iota` for enumerated constants.
- **Prevent path traversal.** Use `os.Root` / `os.OpenRoot` for filesystem access scoped to a directory; reject code that `os.Open`'s user-supplied paths.
- **No mutable globals.** Package-level variables cause data races. Inject dependencies explicitly; never reach for `http.DefaultServeMux` or `http.DefaultClient` in libraries  --  instantiate and configure your own.
- **Race detector by default.** Run `go test -race ./...` in CI; the data races it catches are bugs that escape unit tests.
- **Typed nil in an interface is not `nil`.** A typed nil pointer returned through an interface is non-nil; return untyped `nil` explicitly for the nil case.
- **Beware `append` aliasing.** `append` may reuse the backing array; use `s[:len(s):len(s)]` before appending when shared mutation is unsafe.
- **Scope `defer` to resource lifetime.** `defer` runs at function exit, not loop iteration; extract loop bodies into named functions.
- **Check narrowing conversions.** Integer conversions truncate silently; bounds-check against `math.MaxInt32`/`math.MinInt32` before converting.
- **Compare floats with epsilon.** Never use `==` for IEEE 754 values; use `math.Abs(a-b) < epsilon`.
- **Use safe type assertions.** Prefer `v, ok := x.(T)`; in Go 1.25+ reflection, use `reflect.TypeAssert[T]` over `value.Interface().(T)`.

## 4. Error Craft

Hard rules  --  full detail in `references/error-handling.md`.

- **Check every error.** NEVER discard with `_`. Report runtime errors and exit gracefully; reserve `panic` for invariant violations and internal program errors.
- **Wrap, don't flatten.** Use `fmt.Errorf("doing X: %w", err)` to preserve the chain. Use `%v` only at system boundaries (HTTP, gRPC) to hide internals.
- **Sentinels & types.** Define `var ErrNotFound = errors.New("not found")` for expected logic flows; define custom error types when callers need rich data. Sentinels MUST be lowercase, no trailing punctuation.
- **Inspect via the chain.** MUST use `errors.Is(err, sentinel)`  --  never `==`. MUST use `errors.As(err, &target)` or `errors.AsType[T](err)` (Go 1.26+)  --  never bare type assertions or string matching.
- **Combine with `errors.Join`** (Go 1.20+) for independent failures (parallel tasks, multi-field validation). Joined errors remain inspectable by `errors.Is`/`errors.As`.
- **Single handling rule.** An error MUST be either logged OR returned, NEVER both. Log once at the top boundary (HTTP middleware, `main`); everywhere else wrap and return.
- **`recover` at goroutine boundaries.** Wrap HTTP handlers and worker goroutines with deferred `recover()` that logs the panic + `debug.Stack()` and returns a 500.

## 5. Context & Concurrency

- **Propagate one context end-to-end.** `ctx context.Context` MUST be the first parameter of any blocking or long-running function. Same `ctx` flows HTTP handler → service → DB → outbound HTTP/gRPC.
- **Keep context keys private.** Use an unexported key type to avoid cross-package collisions; context values carry request metadata (trace ID, user ID), never function parameters.
- **Always `defer cancel()`.** For `WithCancel`/`WithTimeout`/`WithDeadline`, call `cancel()` on every control-flow path unless ownership is explicitly transferred. Never pass `nil`; use `context.TODO()` if unsure.
- **Use `context.WithoutCancel`** (Go 1.21+) for background work that must outlive the parent request (audit logs, async dispatch) while preserving request-scoped values.
- **Every goroutine has an exit.** Never start a goroutine without a shutdown mechanism (context cancellation, done channel, or WaitGroup). "Fire-and-forget" goroutines leak.
- **Prefer `wg.Go`** (Go 1.25+) for fire-and-wait tasks without panic or error propagation; call `wg.Add(1)` before `go`, never inside it. Use `errgroup` for errors, cancellation, or limits.
- **Modernize sync primitives.** Use `sync.OnceFunc`/`OnceValue`/`OnceValues` (Go 1.21+) and typed `atomic.Int64`/`atomic.Bool` (Go 1.19+) over manual boilerplate.
- **Channel ownership.** Only the sender closes. Specify direction (`chan<-`, `<-chan`). Default to unbuffered; buffers mask backpressure and need measured justification. Send copies, not pointers.
- **Always include `ctx.Done()` in `select`.** Avoid repeated `time.After` in hot loops  --  each call allocates; reuse `time.NewTimer` + `Reset`.
- **Prefer `errgroup`.** Use `golang.org/x/sync/errgroup` with `WithContext` and `SetLimit(n)` for parallel work, first-error cancellation, and bounded concurrency. Do not hand-roll channel-based wait logic.
- **Pick the right primitive.** Channel = ownership transfer/lifecycle; `sync.Mutex`/`RWMutex` = shared fields (never across I/O or upgrade `RLock` → `Lock`); `sync/atomic` = counters/flags; `sync.Map` = read-heavy map; `singleflight` = deduplicate calls; `sync.Pool` = short-lived object reuse (see §6).
- **Structured concurrency.** Confine goroutines to the scope that created them. Track leaks in tests with `go.uber.org/goleak`.

## 6. Performance & Memory

Full detail in `references/performance.md`. **Profile before optimizing**  --  intuition is wrong ~80% of the time.

- **Rule out external bottlenecks first.** If traces show 90% of latency in a DB or upstream API, allocation tuning will not help. Fix the upstream first.
- **Preallocate.** `make([]T, 0, n)` and `make(map[K]V, n)` whenever the target size is known or estimable. Avoids repeated growth + copy.
- **Prefer stack over heap.** Return small structs by value; use pointers only when mutation is required or the struct is large. Inspect with `go build -gcflags="-m"`.
- **`sync.Pool` for hot paths only.** Reuse `*bytes.Buffer`, `[]byte` working arrays, or struct graphs in high-throughput code. ALWAYS `Reset()` before `Put()`. Skip pooling when objects are long-lived, shared, or rarely reused.
- **Avoid interface boxing in hot loops.** Passing a concrete value to an `any`/`interface{}` parameter forces an allocation. Use `slog.LogAttrs` (not `slog.Info`) in hot paths to avoid boxing arguments.
- **Avoid `reflect.DeepEqual` in production.** 50 -- 200× slower than typed comparison. Use `slices.Equal`, `maps.Equal`, `bytes.Equal`.
- **Avoid `panic`/`recover` as control flow.** Panic allocates a stack trace and unwinds; use error returns.
- **Measure with the iterative cycle.** Define metric → baseline benchmark (`-benchmem -count=6`) → diagnose (pprof) → ONE change with explanatory comment → compare with `benchstat`. Commit `benchstat` output in the commit body.
- **Tune the runtime in containers.** Set `GOMEMLIMIT` to 80 -- 90% of container memory; consider PGO (`-pgo=auto`) once benchmarks are stable.

## 7. Networking & I/O

Full detail in `references/networking.md`.

- **Timeouts are mandatory.** Never ship `&http.Client{}` or `&http.Server{}` with zero values  --  they have no timeouts and will leak file descriptors under slow clients.
  - Server: set `ReadHeaderTimeout` (or `ReadTimeout`), `WriteTimeout`, `IdleTimeout`.
  - Client: set `Timeout` (total) and tune the `Transport` (`MaxIdleConns`, `MaxIdleConnsPerHost`  --  default is only 2).
- **Drain and close response bodies.** ALWAYS `defer resp.Body.Close()`. To allow TCP connection reuse, drain the remainder first: `io.Copy(io.Discard, resp.Body)` before close.
- **Bound long-lived connections.** For TCP/WebSocket/gRPC streams, call `SetReadDeadline` / `SetWriteDeadline` per operation; a blocked read holds a goroutine and its stack forever.
- **Buffer small I/O.** Wrap repeated small reads/writes in `bufio.Reader`/`bufio.Writer`; flush the writer explicitly. Keep buffers bounded and reuse them across chunks.
- **Propagate cancellation.** Pass `r.Context()` from inbound requests to DB (`QueryContext`/`ExecContext`) and outbound HTTP/gRPC so client disconnects halt upstream work.
- **Build for resilience.** Use circuit breakers (Closed / Open / Half-Open), load shedding (bounded queues + `errgroup.SetLimit`), backpressure, and graceful degradation (`503` + `Retry-After`) under overload.
- **Observe the connection lifecycle.** Use `net/http/httptrace` to capture DNS, dial, TLS, and GotConn spans for slow-client debugging; integrate with `slog` and OpenTelemetry tracing.

## 8. Logging & Observability

- **Use `log/slog` (Go 1.21+).** Never `fmt.Println` or `log.Printf` for telemetry. Prefer `slog.LogAttrs` in hot paths to avoid `any` boxing allocations.
- **Actionable, not chatty.** Log only events someone must act on. Do not log routine trivia; for request-scoped flow use tracing, not logging; for performance data use metrics, not logs.
- **Low-cardinality grouping.** Keep message templates stable (`slog.Error("db connection failed")`). Attach high-cardinality data (IDs, paths, counts) as structured key-value attributes  --  never by formatting into the message.
- **Never log secrets or PII.** Sanitize tokens, passwords, and personal data before they reach a handler; implement `slog.LogValuer` for secret-bearing types.

## 9. Verification & Testing

- **Table-driven tests.** `[]struct{ name string; in input; want output; wantErr error }` covers many scenarios in one function. Test names are sentences.
- **Parallelize independent tests.** Call `t.Parallel()` at the top of tests and subtests that do not share mutable state; it speeds suites and surfaces races.
- **Scope testify assertions per subtest.** Never reuse `assert.New(t)` across `t.Run`; it captures the parent `*testing.T`. Pass `tt` into the closure and call `assert.New(tt)`.
- **Detect goroutine leaks.** Add `defer goleak.VerifyNone(t)` (or use `TestMain`) with `go.uber.org/goleak`.
- **Fuzz parsers and decoders.** Use `func FuzzParse(f *testing.F)` with seed cases to catch malformed-input panics hand-written cases miss.
- **Use `b.Loop()`** (Go 1.24+) in benchmarks instead of manual `b.N` loops; it adjusts iterations and keeps the body live.
- **Three-layer evidence (L1/L2/L3).** L1 `go vet` + `golangci-lint`; L2 `go test -race -cover`; L3 at least one path across real boundaries (`httptest.Server`, real DB transaction).
- **Mock boundaries, not internals.** Mock external network/system I/O; do not mock internal types  --  that couples tests to implementation.
- **Benchmarks gate performance claims.** `go test -bench=... -benchmem -count=6 | tee /tmp/report-1.txt`; compare with `benchstat`. No benchmark → no perf claim.
- **Lint config in CI.** `govet`, `staticcheck`, `errcheck`, `gosec`, `gocritic` minimum; `-race` always on.

## 10. Anti-Cheat Sheet (DO NOT)

| Anti-pattern | Fix |
| --- | --- |
| `err == sql.ErrNoRows` | `errors.Is(err, sql.ErrNoRows)` |
| `err.(*MyError)` bare type assertion | `errors.As(err, &target)` / `errors.AsType[T](err)` |
| `if err != nil { log; return err }` | Either log OR return  --  never both |
| `&http.Client{}` / `&http.Server{}` | Always set timeouts + tune `Transport` |
| `resp.Body.Close()` without draining | `io.Copy(io.Discard, resp.Body)` then `Close` |
| `time.After` inside a hot loop | Reuse `time.NewTimer` + `Reset` |
| `go func(){ ... }()` with no exit | `ctx` + `errgroup` + `Wait`/`goleak` |
| `make([]T, 0)` then `append` in a loop | `make([]T, 0, knownLen)` |
| `reflect.DeepEqual` in hot path | `slices.Equal` / `maps.Equal` / `bytes.Equal` |
| `panic(err)` for expected failure | Return the error |
| `os.Open(userPath)` | `os.Root` / `os.OpenRoot` |
| `http.DefaultServeMux` in libraries | `http.NewServeMux()`, inject the mux |
| `return typedNil` from interface func | Return untyped `nil` for the nil case |
| `b := append(a, x)` then mutate `b[0]` | `a[:len(a):len(a)]` to force a copy |
| `defer f.Close()` inside a loop | Extract the loop body to a function |
| `int32(bigInt64)` without bounds check | Check `math.MaxInt32`/`math.MinInt32` first |
| `a + b == c` for floats | `math.Abs((a+b)-c) < epsilon` |
| `v := x.(T)` bare assertion | `v, ok := x.(T)` comma-ok |
| `wg.Add(1)` inside the goroutine | `Add` before `go`  --  `Wait` may return early |
| Unbounded goroutine spawning | `errgroup.SetLimit(n)` or semaphore |
| `assert.New(t)` reused in `t.Run` | `assert.New(tt)` per subtest |

## §11 Modernization (Go 1.21 -- 1.26)

Adopt these proactively when writing or reviewing Go; old-style equivalents are technical debt.

- **Use `log/slog`** (Go 1.21+) for structured key-value logging; prefer `slog.LogAttrs` in hot paths.
- **Use standard collections.** `slices.Sort`, `slices.Contains`, `maps.Clone`, and `maps.Equal` replace hand-rolled loops and `reflect.DeepEqual`.
- **Use range improvements.** `range n` (Go 1.22+) counts; range variables are per-iteration, avoiding closure capture bugs.
- **Use `context.WithoutCancel`** (Go 1.21+) for background work that outlives a request.
- **Use modern sync.** `sync.OnceFunc`/`OnceValue`/`OnceValues` (Go 1.21+) and `wg.Go` (Go 1.25+) replace manual Once/Add/Done boilerplate.
- **Use `errors.AsType[T]`** (Go 1.26+) for type-safe error-chain inspection.
- **Use iterators** (`iter.Seq`, `iter.Seq2`, and `strings.SplitSeq` in Go 1.24+) when they simplify lazy or streaming code.
- **Use `b.Loop()`** (Go 1.24+) in benchmarks; replace `sort.Slice` with `slices.SortFunc` (Go 1.21+).
- **Enable PGO** with `-pgo=auto` (Go 1.21+) after benchmarks stabilize; typical CPU gains are 2 -- 7%.
- **Modernize tooling.** Prefer `math/rand/v2` (Go 1.22+), `go.mod` tool directives (Go 1.24+), `govulncheck` in CI, and `golangci-lint` v2 with `modernize`.
- **Migrate safely.** Use `gopls` rename; run `go vet` and `golangci-lint` after each step.

## References

- `references/concurrency.md`  --  channel ownership, channel vs mutex vs atomic decision, sync primitives deep dive, goroutine pre-spawn checklist, pipelines, `goleak`.
- `references/error-handling.md`  --  sentinel vs custom types, `%w` vs `%v`, `errors.Is`/`As`/`Join`, single handling rule, panic/recover.
- `references/performance.md`  --  escape analysis, preallocation, `sync.Pool`, interface boxing, pprof workflow, iterative benchmarking.
- `references/networking.md`  --  client/server timeouts, transport tuning, long-lived connection deadlines, resilience patterns, `httptrace` observability.

