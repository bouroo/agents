---
description: Refactor and optimize Go code feature-by-feature in parallel without breaking public API
agent: code
subtask: true
---

# Go Refactor & Optimize Workflow

You are performing a long-term, self-organized refactoring pass on a complex Go project. The invariant is: **public API must not break**. Every change must be backward-compatible, tested, and verified before advancing.

## Constraints

- **Never** modify exported function/type signatures. Add new APIs; deprecate old ones.
- **Never** remove exported identifiers. Mark with `// Deprecated:` comments if superseded.
- Run `go vet`, `staticcheck`, and the full test suite after every wave. Fix failures before advancing.
- Trigger context compaction (`<leader>c`) when context grows large. Preserve goals, discoveries, and completed work.

## Phase 0 — Inventory

1. Map the module: `glob` for `**/*.go`, `grep` for exported identifiers, `read` key files.
2. Identify packages with the highest coupling: count import graph depth and cross-package references.
3. Catalogue violations against the Go standards below. Group findings by package.
4. Produce a prioritised backlog using `todowrite` — highest-impact, lowest-risk items first.

### Go Standards (enforce throughout)

**Naming** (ref: Alex Edwards, Go naming conventions):
- `camelCase` for unexported, `PascalCase` for exported identifiers. No `snake_case`.
- Acronyms stay consistent: `APIKey` not `ApiKey`, `userID` not `userId`.
- Short names for narrow scope (`i`, `err`, `buf`); descriptive names for wide scope.
- Receiver names: 1–3 chars, consistent across all methods on the same type. No `this`/`self`.
- Getters: `Address()` not `GetAddress()`. Setters: `SetAddress()`.
- Single-method interfaces: method name + `-er` suffix (`Reader`, `Authorizer`).
- Avoid chattery names: `customer.New()` not `customer.NewCustomer()`.
- Package names: lowercase, one word, no `util`/`helpers`/`common`.

**Error Handling** (ref: JetBrains 10x Commandments #5):
- Define named sentinel errors: `var ErrNotFound = errors.New("not found")`.
- Wrap with `fmt.Errorf("context: %w", err)`. Never flatten to strings.
- Match with `errors.Is` / `errors.As`. Never compare with `==` or type-assert.
- Check every error. Never discard with `_`.

**Safety** (ref: JetBrains 10x Commandments #4, #6):
- Make zero values useful. Provide validating constructors returning guaranteed-valid objects.
- Configuration via `WithX` method chain: `NewWidget().WithTimeout(time.Second)`.
- Named constants over magic values. Use `iota` for enumerations.
- Use `os.Root` for filesystem access to prevent path traversal.
- Eliminate mutable global state. Inject dependencies. No `http.DefaultServeMux` or `http.DefaultClient`.

**Concurrency** (ref: JetBrains 10x Commandments #7, goperf.dev):
- Use structured concurrency. Goroutines must not escape their creator's scope.
- Ensure all goroutines terminate: `sync.WaitGroup`, `context` cancellation, or `errgroup.Group`.
- Channel direction: take `chan<- T` or `<-chan T`, never both.
- Worker pools to cap resource usage. `sync.Once` for lazy init.
- Share immutable data; avoid shared mutable state.

**Escape Analysis & Stack Allocation** (ref: goperf.dev stack-alloc, compiler flags):
- Run `go build -gcflags="-m -m" ./<pkg>... 2>&1` to identify heap escapes.
- Prioritize keeping values on the stack: avoid returning pointers to locals, capturing variables in closures that outlive the frame, and storing pointers in interface values.
- Strict rule: if a value does not escape its declaring function, it **must** stay on the stack. Refactor any unnecessary `&x` or `new(T)` that causes escape where a value copy suffices.
- Use `go build -gcflags="-S" ./<pkg>... 2>&1 | grep 'leak\|escape'` to verify stack frames after fixes.
- Re-run escape analysis after every perf-related change. Document each eliminated escape with a comment: `// NOESCAPE: <reason>`.

**Performance** (ref: goperf.dev common patterns):
- Pre-allocate slices/maps when size is known: `make([]T, 0, n)`.
- Object pooling (`sync.Pool`) for high-churn allocations.
- Struct field alignment: order fields from largest to smallest type.
- Avoid interface boxing where not needed. Use concrete types in hot paths.
- Zero-copy: prefer slices/views over `[]byte` duplication.
- Buffered I/O: `bufio.NewReader` / `bufio.NewWriter`. Batch small writes.
- Run `go test -bench=. -benchmem` before and after perf changes. Require measurable improvement.

**Architecture** (ref: JetBrains 10x Commandments #1, #3, #8):
- Write packages, not programs. `main` should only wire dependencies and handle errors.
- Decouple from environment: no `os.Getenv` or `os.Args` outside `main`. Pass config downward.
- Use `go:embed` for static assets. Use `xdg` for paths. Never assume writable storage.
- Log only actionable information with `slog`. Use structured JSON. Never log secrets or PII.

## Phase 1 — Test Fortification

For each package targeted for refactoring, **before any production code changes**:

1. `bash`: Run `go test -race -count=1 ./...` to establish a green baseline.
2. `bash`: Run `go test -coverprofile=baseline_coverage.out ./...` and identify uncovered critical paths.
3. `bash`: Run `go test -bench=. -benchmem -count=3 ./... 2>&1 | tee baseline_bench.txt` to capture baseline benchmark numbers.
4. `bash`: Run `go build -gcflags="-m -m" ./... 2>&1 | tee baseline_escape.txt` to capture baseline heap escape report. Count total escapes per package.
5. If coverage < 80% on a target package, write additional tests first (Red-Green-Refactor).
6. Use `task` with `subagent_type: go-tester` to write table-driven tests in parallel across packages.

**Gate**: All tests pass with `-race` before proceeding. Store `baseline_coverage.out`, `baseline_bench.txt`, and `baseline_escape.txt` — these are the immutable comparison baseline.

## Phase 2 — Parallel Refactoring Waves

Execute refactoring as a series of parallel waves. Each wave touches independent packages.

### Wave Execution Pattern

For each wave:

1. **Select** 2–4 independent packages from the backlog (no shared imports between them).
2. **Launch** parallel `task` agents (one per package) with `subagent_type: go-engineer`.
3. Each agent receives:
   - The specific package path and findings from Phase 0.
   - The applicable Go standards to enforce.
   - Instruction to run `go vet ./<pkg>...`, `staticcheck ./<pkg>...`, and `go test -race ./<pkg>...` after changes.
   - Instruction to return: files modified, tests added/changed, any issues encountered.
4. **Verify** all agent results. Run the full test suite: `bash` `go test -race ./...`.
5. **Advance** only after the full suite passes.

### Refactoring Checklist Per Package

Apply these transformations in order. Skip items that don't apply.

- [ ] **Naming**: Fix all identifier naming violations per the standards above.
- [ ] **Error handling**: Introduce sentinel errors. Wrap all error returns with context. Remove `==` comparisons.
- [ ] **Safety**: Add validating constructors. Replace magic numbers with named constants. Eliminate global state.
- [ ] **Concurrency**: Scope goroutines. Add `context` propagation. Replace shared mutable state with channels or immutable data.
- [ ] **Escape analysis**: Run `go build -gcflags="-m -m" ./<pkg>... 2>&1`. For each heap escape, determine if the value can stay on the stack by: using value receivers, returning structs instead of pointers, avoiding closure captures of pointer-typed variables. Add `// NOESCAPE: <reason>` comments for confirmed eliminations. Re-verify escapes after each fix.
- [ ] **Performance**: Pre-allocate known-size collections. Optimize struct field order. Add `sync.Pool` for hot allocations. Use buffered I/O.
- [ ] **Decoupling**: Move environment/OS access out of library packages. Accept interfaces, return structs.
- [ ] **Logging**: Replace `fmt.Println` / `log.Printf` with `slog` or structure log. Remove non-actionable log statements.
- [ ] **Dead code**: Remove unused exports (verify no references via `grep`). Simplify overly abstracted interfaces.

## Phase 3 — Verification & Benchmarks

After all refactoring waves complete:

1. `bash`: `go vet ./...` — must be clean.
2. `bash`: `staticcheck ./...` — must be clean.
3. `bash`: `go test -race -count=1 ./...` — all pass.
4. `bash`: `go test -coverprofile=final_coverage.out ./...`
5. `bash`: `go test -bench=. -benchmem -count=3 ./... 2>&1 | tee final_bench.txt`
6. `bash`: `go build -gcflags="-m -m" ./... 2>&1 | tee final_escape.txt` — count total escapes per package.
7. `bash`: `gofmt -l .` — no unformatted files.
8. `bash`: `go mod tidy` — clean module graph.

### Baseline vs Final Comparison

Run a strict comparison between `baseline_*` and `final_*` artifacts. **All deltas must be non-negative (improvement or neutral).**

| Metric | Baseline File | Final File | Requirement |
|---|---|---|---|
| Test coverage % | `baseline_coverage.out` | `final_coverage.out` | Must not decrease. Compute per-package delta via `go tool cover -func`. |
| Heap escapes | `baseline_escape.txt` | `final_escape.txt` | Total escape count must decrease. Per-package: `grep -c 'escapes to heap'` must be ≤ baseline. |
| Benchmark ns/op | `baseline_bench.txt` | `final_bench.txt` | No regression > 5%. Use `benchstat` for statistically significant comparison. |
| Benchmark allocs/op | `baseline_bench.txt` | `final_bench.txt` | Must not increase. |

**Gate**: All comparisons pass. If any metric regresses:
1. Identify the regressing package and metric.
2. Revert only that package's changes: `git checkout -- <pkg-path>/`.
3. Re-run the full comparison suite.
4. If still regressing after revert, flag in the summary for manual review.
5. Document any accepted neutral deltas (no improvement but no regression) with rationale.

## Phase 4 — Summary

Produce a structured summary:

- Packages refactored and changes per package.
- Tests added (count) and coverage delta (`go tool cover -func` baseline vs final).
- Escape analysis delta: baseline escape count vs final, per package. List each eliminated escape with its `// NOESCAPE` rationale.
- Benchmark results: `benchstat baseline_bench.txt final_bench.txt` — ns/op and allocs/op delta per benchmark.
- Verdict: **PASS** (all metrics improved or neutral) or **REGRESSION** (list specific failures).
- Remaining backlog items (if any) for future passes.
- Any API additions (new exported identifiers) — list them for review.

## Context Management

- After each wave, trigger compaction (`<leader>c`) if context is large.
- The `todowrite` backlog persists across compactions — use it as the single source of truth for progress.
- Each `task` subagent operates with fresh context. Pass only the relevant package findings, not the entire conversation history.

## Failure Protocol

- **Test failure**: Fix immediately in the same wave. Do not advance.
- **2 consecutive fix failures on same package**: Stop. Report the package and error. Move to next package.
- **Race condition detected**: Quarantine the package. Add to backlog for dedicated concurrent fix pass.
- **Build breakage**: Revert via `git checkout -- <files>`. Re-analyze and retry once. Stop after second failure.
