# Testing — Depth

Loaded on demand from [go-essential](../SKILL.md) §8. The core rules live there; this file
covers structure, table-driven tests, goleak, synctest, fuzzing, and benchmarks.

## File Conventions

```go
// package_test.go    — same package (white-box, access to unexported)
package mypackage

// mypackage_test.go  — external test package (black-box, public API only)
package mypackage_test
```

Use the external `_test` package by default so tests exercise the real public surface; drop into
the internal package only when an unexported field or helper must be reached.

## Naming

```go
func TestAdd(t *testing.T) { ... }                  // function test
func TestMyStruct_MyMethod(t *testing.T) { ... }    // method test
func BenchmarkAdd(b *testing.B) { ... }             // benchmark
func ExampleAdd() { ... }                           // executable doc
func FuzzAdd(f *testing.F) { ... }                  // fuzz test
```

Subtests in `t.Run` use lowercase descriptive phrases: `"valid id"`, `"empty input"` — not
`"Valid ID"` or `"valid_ID"`.

## Table-Driven Tests

Every case has a `name` passed to `t.Run`, so failures identify the scenario.

```go
func TestCalculatePrice(t *testing.T) {
    tests := []struct {
        name      string
        quantity  int
        unitPrice float64
        expected  float64
    }{
        {name: "single item",         quantity: 1,   unitPrice: 10.0, expected: 10.0},
        {name: "bulk discount - 100", quantity: 100, unitPrice: 10.0, expected: 900.0},
        {name: "zero quantity",       quantity: 0,   unitPrice: 10.0, expected: 0.0},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got := CalculatePrice(tt.quantity, tt.unitPrice)
            if got != tt.expected {
                t.Errorf("CalculatePrice(%d, %.2f) = %.2f, want %.2f",
                    tt.quantity, tt.unitPrice, got, tt.expected)
            }
        })
    }
}
```

Scaffold with `gotests`:

```bash
go install github.com/cweill/gotests/gotests@latest
gotests -all -w handler.go
```

## Parallel Tests

Mark independent tests and subtests for concurrent execution:

```go
for _, tt := range tests {
    tt := tt   // capture (Go 1.22+ loop variable scoping makes this optional, still safe)
    t.Run(tt.name, func(t *testing.T) {
        t.Parallel()
        // ... assertions ...
    })
}
```

In Go 1.22+ the loop variable is per-iteration, so the `tt := tt` defensive copy is no longer
required — but it is harmless and documents intent for readers on older toolchains.

## Goroutine Leak Detection (goleak)

```go
import (
    "testing"
    "go.uber.org/goleak"
)

func TestMain(m *testing.M) {
    goleak.VerifyTestMain(m)
}
```

Per-test or with exclusions for known background goroutines:

```go
func TestWorkerPool(t *testing.T) { defer goleak.VerifyNone(t) /* ... */ }

func TestMain(m *testing.M) {
    goleak.VerifyTestMain(m, goleak.IgnoreCurrent())
}
```

## `testing/synctest` (Go 1.25+)

Deterministic tests for goroutines, timers, deadlines, and context cancellation. Synthetic time
advances only when all goroutines are blocked.

```go
import (
    "context"
    "testing"
    "testing/synctest"
    "time"
)

func TestContextTimeout(t *testing.T) {
    synctest.Test(t, func(t *testing.T) {
        const timeout = 5 * time.Second
        ctx, cancel := context.WithTimeout(t.Context(), timeout)
        defer cancel()

        time.Sleep(timeout - time.Nanosecond)
        synctest.Wait()
        if err := ctx.Err(); err != nil { t.Fatalf("before timeout: %v", err) }

        time.Sleep(time.Nanosecond)
        synctest.Wait()
        if err := ctx.Err(); err != context.DeadlineExceeded {
            t.Fatalf("after timeout: got %v, want DeadlineExceeded", err)
        }
    })
}
```

Use `synctest.Test` in Go 1.25+ / 1.26+. Do not use the Go 1.24 experimental `synctest.Run` API
in 1.25+ code; reserve it only as a compatibility fallback for modules targeting Go 1.24 with
`GOEXPERIMENT=synctest`.

## Fuzzing

Seed with `f.Add(...)`, then assert an invariant inside `f.Fuzz`.

```go
func FuzzReverse(f *testing.F) {
    f.Add("hello"); f.Add(""); f.Add("a")
    f.Fuzz(func(t *testing.T, input string) {
        reversed := Reverse(input)
        double := Reverse(reversed)
        if input != double {
            t.Errorf("Reverse(Reverse(%q)) = %q, want %q", input, double, input)
        }
    })
}
```

Run with `go test -fuzz=FuzzReverse -fuzztime=30s ./...`. Corpus failures are saved under
`testdata/fuzz/` and become regression tests automatically.

## Benchmarks

Use `b.Loop()` (Go 1.24+) — it handles warmup and reports stable timings. The legacy
`for i := 0; i < b.N; i++` form is reserved for modules targeting Go <1.24.

```go
func BenchmarkConcat(b *testing.B) {
    b.Run("plus", func(b *testing.B) {
        for b.Loop() { _ = "a" + "b" + "c" }
    })
    b.Run("builder", func(b *testing.B) {
        for b.Loop() {
            var sb strings.Builder
            sb.WriteString("a"); sb.WriteString("b"); sb.WriteString("c")
            _ = sb.String()
        }
    })
}
```

```bash
go test -bench=. -benchmem ./...             # run all benchmarks
go test -bench=. -count=10 ./... | tee old.txt
# ... make a change ...
go test -bench=. -count=10 ./... | tee new.txt
benchstat old.txt new.txt                    # statistical comparison
```

For deeper profiling (CPU, memory, block, mutex, trace, flame graphs, continuous profiling) see
[Performance](./performance.md) and [Observability](./observability.md).

## HTTP Handler Tests

Use `httptest`:

```go
func TestHandler(t *testing.T) {
    req := httptest.NewRequest(http.MethodPost, "/users", strings.NewReader(`{"name":"ada"}`))
    rec := httptest.NewRecorder()

    handler(rec, req)

    resp := rec.Result(); defer resp.Body.Close()
    if resp.StatusCode != http.StatusCreated { t.Fatalf("got %d", resp.StatusCode) }
}
```

## Integration Tests

Build tags separate them from unit tests:

```go
//go:build integration

package mypackage_test

func TestDatabaseIntegration(t *testing.T) { /* ... */ }
```

```bash
go test ./...                  # unit only
go test -tags=integration ./... # include integration
```

## Mocking

- Mock interfaces, never concrete types.
- Define the interface where the consumer lives.
- Prefer [`github.com/stretchr/testify/mock`](https://github.com/stretchr/testify) or generated
  mocks (`mockgen`, `moq`) over hand-rolled stubs when the contract has many calls.

## Examples as Documentation

Examples prefixed with `Output:` comments are executed by `go test`:

```go
func ExampleCalculatePrice() {
    fmt.Printf("%.2f\n", CalculatePrice(100, 10.0))
    // Output: 900.00
}
```

`ExampleCalculatePrice_bulkDiscount` becomes a subexample in godoc.

## Go 1.26+: Test Artifacts

When a test must persist a file for inspection, use `t.ArtifactDir()` instead of ad-hoc paths:

```go
func TestRender(t *testing.T) {
    out := filepath.Join(t.ArtifactDir(), "rendered.json")
    if err := os.WriteFile(out, payload, 0o644); err != nil { t.Fatal(err) }
    t.Logf("artifact: %s", out)
}
```

Available on `*testing.T`, `*testing.B`, `*testing.F`.

## Quick Reference

```bash
go test ./...                          # all tests
go test -race ./...                    # race detection (always in CI)
go test -run 'TestName/subtest' ./...  # specific subtest (regexp)
go test -coverprofile=c.out ./...      # coverage
go tool cover -html=c.out              # browse coverage
go test -tags=integration ./...        # integration only
go test -bench=. -benchmem ./...       # benchmarks
go test -fuzz=FuzzName ./...           # fuzzing
```

## Audit Sub-Agents (Parallel)

When auditing a test suite, split into 3 parallel sub-agents:

1. **Unit test quality** — coverage gaps, table-driven structure, assertion quality, no
   implementation-detail coupling.
2. **Integration test isolation** — build tags, fixtures, no shared mutable state, no order
   dependency.
3. **Concurrency hygiene** — `t.Parallel()` where safe, `goleak` in `TestMain` for goroutine-
   spawning packages, no `time.After`-based sleeps that flake.
