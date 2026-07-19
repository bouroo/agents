---
name: go-essential
description: >
  Essential Go (Golang) production-readiness rules: code style, naming, error handling, safety,
  structs and interfaces, concurrency, context, testing, project & design, design patterns,
  observability, documentation, performance, and safe refactoring. Use when writing, reviewing,
  or refactoring Go code; starting a new Go project; profiling a hot path; restructuring code;
  instrumenting a service; or asked about idiomatic Go. Covers the high-density core; load the
  references for depth.
---

# Go Essential

Non-negotiable rules that distinguish production Go from "code that compiles." Linters handle
formatting; this skill handles judgment.

> **Override.** A project-level style guide or company skill that explicitly supersedes this
> skill takes precedence; project convention beats personal taste.

> "Clear is better than clever." - Go Proverbs

**Stance:** Every swallowed error, untyped `any`, leaked goroutine, and untagged struct field
is a defect waiting to ship. Clear beats clever; the next reader is the customer.

**Modes:**

- **Write** - new Go code; walk §1-§9 in order as a pre-flight checklist.
- **Refactor** - walk §13 in order: plan → safety net → small tool-driven step → verify →
  atomic single-category commit. Never mix structural and behavioral changes.
- **Review** - read only the diff; check against the rules most relevant to the change (errors,
  concurrency, safety, tags, structural-vs-behavioral separation).
- **Audit** - launch up to 5 parallel sub-agents: (1) errors and single-handling rule,
  (2) concurrency and goroutine lifecycle, (3) nil/aliasing/numeric safety, (4) interface and
  struct design, (5) test posture. For performance audits, swap in the three-way split in
  [Performance](./references/performance.md).

When ignoring a rule, add a code comment explaining why.

---

## 1. Code Style - Clarity Over Cleverness

- **MixedCaps everywhere.** Exported = `MixedCaps`; unexported = `mixedCaps`. No underscores
  (test subcases, generated code, cgo are the only exceptions). Capitalization controls
  visibility - `MaxRetries`, not `MAX_RETRIES`.
- **Break long lines at semantic boundaries** beyond ~120 chars; one arg per line for 4+ args.
- **`:=` for non-zero values, `var` for zero-value init** - the form signals intent.
- **Always init slices and maps.** Nil maps panic on write; nil slices serialize to JSON
  `null`. Preallocate (`make([]T, 0, n)`) only when capacity is known.
- **Composite literals use field names** - positional breaks on field add/reorder.
- **Early-return on errors and edge cases; happy path at minimal indent.** Drop `else` after a
  terminating `if`. `switch` over if-else chains on the same variable.
- **Extract named booleans** when an `if` has 3+ operands.
- **Functions: ≤4 params (else an options struct), one job.** Order: `ctx`, inputs, outputs.
- **Prefer `range` (and `range n` Go 1.22+) over index loops.**
- **Small types by value; pointers to mutate, for ~128B+ structs, or when `nil` is meaningful.**
- **`strconv` for simple conversions; `fmt.Sprintf` for complex formatting.** `%q` in errors
  shows string boundaries. `strings.Builder` for concat loops; `+` for trivial.
- **Avoid `reflect`.** Prefer generics over `any` when a concrete type will do.
- **Minimize public surface.** Unexport aggressively; blank/dot imports only in `main`/tests.

→ Depth: [Code Style](./references/code-style.md).

---

## 2. Naming - Names Are the Architecture

- **Avoid stutter.** `http.Client` not `http.HTTPClient`; `user.New()` not `user.NewUser()`.
- **Constructor: `New` for one type, `NewTypeName` for multiple.**
- **Booleans/predicates: `is`/`has`/`can`** (`IsHealthy()`, `hasPermission`). Go omits `Get`
  (`user.Name()`) but keeps `Is`/`Has`/`Can`.
- **Acronyms: all caps or all lower** - `URL`, `HTTPServer`, `xmlParser`. Never `Url`, `Http`.
- **Error variable: `Err` prefix (`ErrNotFound`). Error type: `Error` suffix (`PathError`).**
- **Error strings fully lowercase, no trailing punctuation, including acronyms** -
  `"invalid message id"`, not `"Invalid message ID"`. Sentinels include the package name:
  `"mypackage: not found"`.
- **Enum zero value is an explicit Unknown/Invalid sentinel.** A `var s Status` becomes `0`
  silently - if `0` maps to `StatusReady`, code behaves as if a state was chosen when it wasn't.
- **Receiver: 1-2 letter abbreviation, consistent across all methods** (`s *Server`). Never
  `this`/`self`.
- **Functional options: `With` + field name.** Variants: `Must` for panicking constructors,
  `f` suffix for format funcs (`Errorf`), `In` for in-place mutation (`SortIn`).
- **No `util`/`helper`/`common` packages** - pick a name that describes the abstraction.
- **Name length matches scope** - `i` for a 3-line loop; longer for package-level scope.

→ Depth: [Naming](./references/naming.md).

---

## 3. Error Handling - Every Error Is an Event

1. **Returned errors MUST be checked.** NEVER discard with `_`.
2. **Wrap with context: `fmt.Errorf("doing X: %w", err)`.** `%w` preserves the chain; `%v`
   flattens. Use `%w` internally, `%v` at system boundaries.
3. **Inspect with `errors.Is` (sentinel) and `errors.As` (typed).** Go 1.26+: prefer
   `errors.AsType[T]`. NEVER branch on error strings.
4. **`errors.Join` (Go 1.20+) for independent errors.**
5. **Single handling rule: log XOR return, NEVER both.** Logging-then-returning is the #1 cause
   of duplicate log noise in aggregators.
6. **Sentinels for expected conditions; custom types for carrying data.**
7. **`panic` only for truly unrecoverable bugs** - never expected conditions. `recover` only at
   goroutine boundaries or top-level handlers.
8. **`slog` (Go 1.21+) for structured logging at error sites.** Stable, low-cardinality message
   templates; IDs/paths/counts as structured attributes.
9. **Never expose technical errors to end users.** Translate at the boundary; log technical
   detail separately.
10. **For stack traces, tenant/user context, and APM integration**, wrap with a typed error
    carrying that metadata, or an error-structuring library.

→ Depth: [Error Handling](./references/error-handling.md).

---

## 4. Safety - Defend Against Yourself

Prevents programmer mistakes (bugs, panics, silent corruption). Security handles attackers;
safety handles ourselves.

- **Typed-nil-interface trap.** An interface is `nil` only when type AND value are nil. Returning
  a typed nil pointer from an interface-returning function yields a non-nil interface - return
  untyped `nil` for the nil case.
- **Nil map panics on write.** Always `make` or lazy-init.
- **`append` may alias the backing array.** Use `a[:len(a):len(a)]` to force a fresh copy when
  retaining both slices.
- **Return defensive copies** of internal slices/maps from exported functions - otherwise
  callers mutate your internals.
- **`defer` runs at function exit, not loop iteration.** Extract loop bodies to a function.
- **Integer conversions truncate silently** - check bounds before `int64`→`int32`.
- **Floats are not exact** - compare with `math.Abs(a-b) < epsilon` or `math/big`.
- **Integer division by zero panics** - guard `if divisor == 0`.
- **Safe type assertions always:** `v, ok := x.(T)` - the bare form panics.
- **Make the zero value useful.** Nil map fields panic on first write - lazy-init with
  `sync.Once`.
- **`noCopy` sentinel** on structs holding mutexes/channels so `go vet` catches copies.

→ Depth: [Safety](./references/safety.md).

---

## 5. Structs & Interfaces - Small, Composed, Discovered

> "The bigger the interface, the weaker the abstraction." - Go Proverbs
> "Don't design with interfaces, discover them."

- **Interfaces have 1-3 methods.** Compose larger ones
  (`type ReadWriter interface { io.Reader; io.Writer }`).
- **Define interfaces where consumed, not where implemented.** The consumer owns the contract;
  the implementor exports a concrete type.
- **Accept interfaces, return structs.** NEVER return interfaces from constructors - callers
  lose concrete access for no benefit.
- **Don't create interfaces prematurely** - wait for a second implementation or a test mock.
- **Compile-time interface check:** `var _ io.ReadWriter = (*MyBuffer)(nil)` near the type def.
  Free at runtime; build breaks if the contract drifts.
- **Honor canonical method names:** `String()`, `Read(p []byte) (n int, err error)`,
  `ServeHTTP(http.ResponseWriter, *http.Request)`.
- **Embed to promote an API; named field to keep a dependency private.**
- **Field tags on every exported field of a marshaled struct.** `json:"id,omitempty"`,
  `db:"id"`, `json:"-"` to exclude.
- **Receiver consistency:** if any method uses a pointer receiver, all do. Pointer to mutate,
  when the struct holds a mutex, or for large structs; value for small immutable types.
- **Prefer generics over `any`** when the type set is known - the compiler catches mismatches
  instead of the runtime panicking.

→ Depth: [Types and Interfaces](./references/types-interfaces.md).

---

## 6. Concurrency - Every Goroutine Has an Owner

Structured concurrency: every goroutine has a clear owner, a predictable exit, and proper error
propagation. Goroutines are cheap but not free.

1. **Every goroutine MUST have a clear exit** - context, done channel, or WaitGroup. Without
   one, it leaks until the process crashes.
2. **Share memory by communicating.** Channels transfer ownership explicitly; mutexes make
   ownership implicit.
3. **Send copies, not pointers** on channels - pointers create invisible shared memory.
4. **Only the sender closes a channel** - closing from the receiver panics on later send.
5. **Specify channel direction** (`chan<-`, `<-chan`) - the compiler prevents misuse.
6. **Default to unbuffered channels** - buffers mask backpressure; use with measured reason.
7. **Always include `ctx.Done()` in `select`** - without it, goroutines leak after cancellation.
8. **Avoid `time.After` in hot loops** - it allocates a timer per call. Reuse
   `time.NewTimer` + `Reset`.
9. **Track leaks in tests** with `go.uber.org/goleak`.
10. **Run `go test -race ./...` always in CI.**

**Quick pick:**

| Scenario                                | Use                            |
| --------------------------------------- | ------------------------------ |
| Passing data between goroutines         | Channel                        |
| Coordinating goroutine lifecycle        | Channel + context              |
| Protecting shared struct fields         | `sync.Mutex` / `sync.RWMutex`  |
| Simple counters, flags                  | `sync/atomic` (typed, 1.19+)   |
| Many readers, few writers on a map      | `sync.Map`                     |
| Deduplicate concurrent identical calls  | `x/sync/singleflight`          |

**Group needs:** no errors → `sync.WaitGroup`; first error → `errgroup.Group`; cancel siblings
on error → `errgroup.WithContext`; bound concurrency → `errgroup.SetLimit(n)`.

**Before spawning:** how will it exit? Can I signal it? Can I wait for it? Who owns the
channels? Should this just be synchronous?

→ Depth: [Concurrency](./references/concurrency.md).

---

## 7. Context - One Request, One Chain

`context.Context` is the "session" of a request - it ties every operation in the same unit of
work and carries cancellation, deadlines, and request-scoped values across boundaries.

1. **Propagate the same context through the whole call chain** (HTTP → service → DB → external
   API). Breaking the chain defeats cancellation and trace propagation.
2. **`ctx context.Context` is always the first parameter.**
3. **NEVER store a context in a struct; NEVER pass `nil`.** Use `context.TODO()` as placeholder.
4. **`context.Background()` only at the top level** (main, init, tests).
5. **Call `cancel()` on every path** for `WithCancel`/`WithTimeout`/`WithDeadline` - usually
   via `defer cancel()`.
6. **`context.WithoutCancel` (Go 1.21+)** for background work outliving the parent request
   (audit logs, cleanup).
7. **Value keys are unexported types.** Values carry only request-scoped metadata (request ID,
   user ID) - never function parameters.
8. **Always use `*Context` variants** (`QueryContext`, `ExecContext`,
   `NewRequestWithContext`) - unstarred forms break trace propagation and deadlines.

→ Depth: [Context](./references/context.md).

---

## 8. Testing - Tests Are Executable Specifications

Write tests to constrain behavior, not to hit coverage targets.

1. **Table-driven tests with named subtests** - every case has a `name` field for `t.Run`.
2. **Independence:** each test runs on its own; no order dependency. `t.Parallel()` when safe.
3. **Integration tests behind build tags** (`//go:build integration`), separate from unit tests.
4. **Test observable behavior, not implementation details** - implementation-coupled tests
   break on every refactor.
5. **`goleak.VerifyTestMain(m)`** in packages that spawn goroutines.
6. **testify as helpers, not a stdlib replacement.** Mock interfaces, not concrete types.
7. **`Example_xxx` functions are executable documentation** verified by `go test`.
8. **Benchmarks use `b.Loop()` (Go 1.24+)**, not legacy `for i := 0; i < b.N; i++`.
9. **Fuzzing** seeds with `f.Add(...)` to find edge cases via invariants
   (e.g., `Reverse(Reverse(s)) == s`).
10. **`testing/synctest` (Go 1.25+)** for deterministic time-based tests - time advances only
    when all goroutines are blocked.

```bash
go test ./...                          # all tests
go test -race ./...                    # race detection (always in CI)
go test -run 'TestName/subtest' ./...  # specific subtest (regexp)
go test -coverprofile=c.out ./... && go tool cover -html=c.out
go test -tags=integration ./...        # integration only
go test -bench=. -benchmem ./...       # benchmarks
go test -fuzz=FuzzName ./...           # fuzzing
```

→ Depth: [Testing](./references/testing.md).

---

## 9. Project, Design & Idioms - Right-Size Everything

- **Ask first.** When starting a project, ask the developer about architecture (clean,
  hexagonal, DDD, flat) and DI approach (manual, wire, dig/fx). Never impose complex structure
  on a small project.
- **Module path matches repo URL**, lowercase, hyphens for multi-word:
  `github.com/jdoe/payment-processor`.
- **`cmd/{name}/main.go` is minimal:** parse flags, wire deps, call `Run()`. Business logic in
  `internal/` (private) or `pkg/` (exportable). Packages are lowercase, singular, match their
  directory.
- **Follow 12-Factor** for services: env-var config, stdout logs, stateless processes, graceful
  shutdown, backing services as attached resources, admin tasks as `cmd/migrate/` one-offs.
- **Avoid `init()`.** It runs implicitly, can't return errors, and runs before tests -
  unpredictable. Use explicit constructors.
- **Constructors use functional options** - one `Option` type, one setter per option, defaults
  in the constructor. Options that validate return an error. Use builder only when validation
  crosses configuration steps.
- **Make illegal states unrepresentable.** Use the type system to enforce invariants: a
  `ClosedOrder` is a different type from an `OpenOrder`; a `NonEmpty[T]` cannot be constructed
  empty.
- **`defer Close()` immediately after opening** - read-only resources can use bare
  `defer f.Close()`; write/flush resources must surface close errors when durability matters.
- **Timeout every external call.** Limit everything (pools, queues, buffers, retry counts) -
  unbounded resources grow until they crash.
- **Retry loops check `ctx.Err()` between attempts** with exponential backoff + jitter.
- **`string` for keys/display, `[]byte` for I/O/mutation, `[]rune` for character ops.** Stay
  in one type - each conversion allocates.
- **Iterators (Go 1.23+) for lazy evaluation.** Stream large transfers (DB rows → HTTP) to
  keep memory constant regardless of dataset size.
- **Compile regexp once at package level.** `//go:embed` for static assets (compile-time, no
  runtime I/O errors).
- **`crypto/rand` for keys/tokens/nonces** - `math/rand` is predictable.
- **`runtime.AddCleanup` over `runtime.SetFinalizer`** (Go 1.24+) - finalizers are
  unpredictable and can resurrect objects.
- **A little recode > a big dependency.** Reach for stdlib first, then `golang.org/x/...`, then
  external. Each dep adds attack surface and an upgrade treadmill.
- **Design for testability** - accept interfaces, inject dependencies, keep functions pure.

→ Depth: [Project and Design](./references/project-and-design.md) and
[Design Patterns](./references/design-patterns.md).

---

## 10. Observability - A Feature Isn't Done Until Observable

Five complementary signals, each answering a different question:

| Signal       | Question                  | Default tool         | Use for                                |
| ------------ | ------------------------- | -------------------- | -------------------------------------- |
| **Logs**     | What happened?            | `log/slog`           | Discrete events, errors, audit trails  |
| **Metrics**  | How much / how fast?      | Prometheus client    | Aggregated measurements, alerting      |
| **Traces**   | Where did time go?       | OpenTelemetry        | Request flow across services           |
| **Profiles** | Why slow / memory-hungry? | `pprof`, Pyroscope   | CPU hotspots, memory leaks, contention |
| **RUM**      | How do users experience?  | PostHog, Segment     | Product analytics, funnels, replay     |

1. **Structured logging with `log/slog`** (Go 1.21+) - production emits JSON, not freeform.
   Levels: Debug (dev), Info (normal), Warn (degraded), Error (needs attention).
2. **`slog.InfoContext(ctx, ...)` correlates logs with traces** - context carries `trace_id`
   and `span_id`. Go 1.26+: `slog.NewMultiHandler` for fan-out before adding a dependency.
3. **Prefer `Histogram` over `Summary` for latency** - aggregates across instances, supports
   `histogram_quantile()` in PromQL; summaries don't.
4. **Label cardinality low.** NEVER unbounded values (user IDs, full URLs, request IDs) as
   labels - one high-traffic endpoint can OOM Prometheus.
5. **Every HTTP endpoint has latency + error-rate metrics** - P50/P90/P99/P99.9 from a histogram.
6. **Set up OpenTelemetry tracing early.** Spans on every meaningful operation: service methods,
   DB queries, external API calls, queue sends/receives.
7. **Propagate context everywhere** (see §7). `trace_id` in logs via `otelslog` bridge;
   exemplars on histograms link P99 spikes to offending traces.
8. **Enable profiling via env vars** - toggle pprof/continuous profiling without redeploying.
   Protect pprof endpoints behind auth in production.
9. **Alert on the four golden signals** (latency, traffic, errors, saturation) with explicit
   `for:` durations to avoid flapping.
10. **Migrate legacy loggers (zap/logrus/zerolog) to `slog`** - bridge during, drop after.
11. **Never log secrets or PII.** Identity keys are `user_id`, not email. Check consent before
    server-side RUM tracking.

**Definition of done:** metrics declared (with PromQL queries and alert rules as comments above
the declaration), structured `slog` logging with context variants (errors logged XOR returned),
spans on every service method / DB query / external call (errors via `span.RecordError()`),
dashboards and alerts wired from the metric comments.

→ Depth: [Observability](./references/observability.md).

---

## 11. Documentation - Doc Comments First

Write for the reader who has never seen this codebase.

1. **Every exported identifier has a doc comment starting with its name.** Package comment
   (`// Package foo ...`) MUST exist on exactly one file.
2. **Intent over paraphrase.** Code shows *what*; the comment explains *why*, *when*, *what
   constraints apply*, and *what can go wrong*. Paraphrasing the signature wastes the reader's
   time.
3. **Concision.** Shortest version that carries the idea. Remove ornament, marketing
   vocabulary (`seamlessly`, `robust`, `enterprise-grade`), hollow transitions, groundless
   future claims.
4. **Preserve modality when editing.** `must`/`should`/`may` are different obligations; a
   cleaner sentence that silently changes them is wrong.
5. **Document parameters, returns, and error cases** on non-trivial functions. Name the
   sentinel errors returned (`// Returns ErrInvalidPrice if basePrice is negative.`).
6. **`Example_xxx` test functions are executable documentation** verified by `go test` - drift
   between docs and code becomes a build failure.
7. **`// Deprecated:`** markers surface at every callsite via `gopls` and linters.
8. **`// Play: https://go.dev/play/p/xxx`** renders as a "Run" button on pkg.go.dev.
9. **README order:** Title → Badges → Summary → Demo → Getting Started → Features →
   Contributing → Contributors → License.
10. **CONTRIBUTING.md gets a new contributor to a working build in under 10 minutes.** If it
    takes longer, fix the process (Makefile, docker-compose, devcontainer).
11. **CHANGELOG follows [Keep a Changelog](https://keepachangelog.com/) or GitHub Releases.**
    Entries answer *what changed for the reader* - internal refactors belong in commit history.
12. **`llms.txt` at repo root** for AI-friendly overview; machine-readable API specs
    (OpenAPI/AsyncAPI/protobuf) for any API-exposing project.

→ Depth: [Documentation](./references/documentation.md).

---

## 12. Performance - Measure, Then Optimize

Optimize only after correctness is proven, only with measurement. Intuition about bottlenecks
is wrong ~80% of the time.

1. **Profile before optimizing.** `pprof` finds actual hot spots; guessing does not.
2. **Rule out external bottlenecks first.** If 90% of latency is a slow DB or upstream,
   allocation tuning won't help. Use `fgprof` (off-CPU) or tracing to confirm before touching
   code.
3. **Allocation reduction has the biggest ROI** - Go's GC is fast but not free; allocations
   per request often matter more than micro-optimized CPU.
4. **Iterate:** define metric → baseline → diagnose → improve ONE thing → compare with
   `benchstat` on `-count=6` runs.
5. **Preallocate when size is known** - `make([]T, 0, len(ids))`. Never speculatively.
6. **`strings.Builder` for concat in loops; `+` for trivial.**
7. **`sync.Pool` for short-lived high-allocation objects** (buffers, decoded envelopes).
   Always `Reset()` before `Put()`.
8. **Tune the HTTP transport.** Default `MaxIdleConnsPerHost` is **2** - fatal under real
   concurrency. Reuse one `*http.Client` process-wide; never per request.
9. **Stream large transfers** instead of materializing.
10. **Avoid reflection in hot paths.** `reflect.DeepEqual` is 50-200× slower than typed
    comparison - use `slices.Equal`, `maps.Equal`, `bytes.Equal`.
11. **Compile regexp once at package level** - `regexp.MustCompile` is O(n) and allocates.
12. **Mind struct field alignment.** Reorder largest-to-smallest; run `fieldalignment`.
13. **PGO (Go 1.21+).** Drop a production CPU profile at `default.pgo` - typical 2-7% gains
    with no code change.
14. **Container runtime knobs:** `GOMEMLIMIT` at 80-90% of container memory (prevents OOM
    kills); `automaxprocs` so `GOMAXPROCS` sees the cgroup quota.
15. **`unsafe` only with benchmark proof** - justified only when >10% of a verified hot path.
    Isolate and document.
16. **Document optimizations** with benchmark numbers so a future reader doesn’t revert them
    as "unnecessary."
17. **Set read/write deadlines on every long-lived connection** (`SetReadDeadline` /
    `SetWriteDeadline` on `net.Conn`, `*http.Response.Body`, websockets) - no deadline means a
    stuck peer leaks a blocked goroutine forever. Use idle/timeouts via a `time.AfterFunc`
    heartbeat; do not depend on `KeepAlive` alone.

→ Depth: [Performance](./references/performance.md).

---

## 13. Refactoring - Safe Change at Scale

Refactoring (Fowler) changes internal structure to make code easier to understand or cheaper to
modify, **without changing observable behavior**. Go tooling can prove several transforms
behavior-preserving *by construction* - that guarantee is the leverage.

**Core loop:** understand → safety net → small tool-driven step → verify → atomic
single-category commit. Repeat.

1. **Never mix structural and behavioral changes in one commit or PR.** Reviewers need different
   postures for a rename vs. a feature.
2. **Map blast radius with `gopls` before touching anything** - references, call hierarchy,
   package API. Get explicit user sign-off before edits.
3. **Prefer `gopls` Rename/Inline/Extract over LLM hand-edits.** Rename refuses on shadowing
   or interface-satisfaction breakage; Inline substitutes side-effect-bearing arguments into
   `var` temporaries. Hand-edits across many call sites have no such guarantee.
4. **Recurring change across many sites → generate a rewrite tool.** Escalate `gofmt -r` →
   `eg` → `gopatch` → a `go/analysis` fixer. A generated tool is reviewable, re-runnable,
   testable against golden files.
5. **Build a coverage-adaptive safety net.** Gate on the blast radius's coverage, not global.
   Add characterization/golden tests for untested code before touching it.
6. **Type alias (`type A = B`) for every type moved across packages** - gradual-code-repair;
   old and new names stay interchangeable during migration.
7. **Break import cycles with a consumer-side interface first** - Go resolves interfaces
   implicitly; the producer never imports the consumer's interface. Cheapest, most surgical fix.
8. **Grep for tag and reflection references after any rename.** `gopls` Rename only guards
   *compilation* - it can't see struct tags, `text/template` field refs, or `reflect` dispatch.
9. **Pause for human sign-off before** any cross-package move/split, exported-API change or
   deprecation, any deletion, any new major version, or touching untested code.
10. **Atomic single-category commit, 100-500 lines per PR.** One coherent change per review.
11. **Start every step from a clean committed baseline; revert rather than debug forward when it
    goes red.** Version control is the safety net under the test safety net. Commit the moment
    a step goes green.
12. **Verify per step:** `go build ./... && go vet ./... && go test ./...`; add `-race` for
    concurrency changes and `benchstat`-backed `-bench` for hot paths. A "refactor" that
    regresses a benchmark is a behavior change - stop and revert or optimize.

**Risk stratification:**

| Risk       | Transforms                                                                                  | Safety                            |
| ---------- | ------------------------------------------------------------------------------------------- | --------------------------------- |
| **Low**    | gopls Rename, Extract Variable/Constant, Inline Variable, `gofmt -s`, organize imports      | Build/vet/test after step         |
| **Medium** | Extract Function/Method, Inline across packages, single-param add/remove, generics         | Targeted tests over blast radius  |
| **High**   | Signature change across many callers, cross-package type moves, package split/merge, import-cycle breaks, exported-API or major-version changes | Full safety net + human checkpoint |

**When NOT to refactor:** the code works and nothing planned will touch it again; it's critical
production code with no tests; the deadline is tight (staged review needs bandwidth between
PRs); or there's no clear purpose behind the ask.

→ Depth: [Refactoring](./references/refactoring.md).

---

## Enforce with Linters

Move rules out of review and into deterministic checks. In order of leverage:
`gofmt`/`gofumpt`/`goimports` → `golangci-lint` (`errcheck`, `govet`, `staticcheck`, `revive`,
`thelper`, `paralleltest`, `testifylint`, `errname`, `predeclared`, `misspell`, `nilerr`,
`forcetypeassert`) → `go test -race`. A rule the linter enforces is one reviewers never repeat.

---

## Cross-References

Depth files: [Code Style](./references/code-style.md) · [Naming](./references/naming.md) ·
[Error Handling](./references/error-handling.md) · [Safety](./references/safety.md) ·
[Concurrency](./references/concurrency.md) · [Types and Interfaces](./references/types-interfaces.md) ·
[Context](./references/context.md) · [Testing](./references/testing.md) ·
[Project and Design](./references/project-and-design.md) · [Design Patterns](./references/design-patterns.md) ·
[Observability](./references/observability.md) · [Documentation](./references/documentation.md) ·
[Performance](./references/performance.md) · [Refactoring](./references/refactoring.md).

Companion skills: [effective-code-craft](../effective-code-craft/SKILL.md) (language-agnostic
craft), [harness-engineering](../harness-engineering/SKILL.md) (three-layer termination and
verify bound), [performance-patterns](../performance-patterns/SKILL.md) (language-agnostic
performance depth).

Draws on [Effective Go](https://go.dev/doc/effective_go), the
[Go style guides](https://google.github.io/styleguide/go/guide),
[Uber's Go style guide](https://github.com/uber-go/guide/blob/master/style.md),
[100 Go Mistakes](https://100go.co/), the [Go proverbs](https://go-proverbs.github.io/), and
[Keep a Changelog](https://keepachangelog.com/).
