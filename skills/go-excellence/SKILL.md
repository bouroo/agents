---
name: go-excellence
description: Go-specific excellence patterns — naming conventions, 15 performance patterns, concurrency primitives, error design, structured logging, and security. Use when writing, reviewing, or optimizing Go code.
---

# Go Excellence

Language-specific guidance for writing idiomatic, high-performance, production-ready Go. Load this skill when working in Go codebases.

---

## Style Hierarchy

When principles conflict, resolve in this priority order:

1. **Clarity** — Purpose and rationale obvious to the reader; explain non-obvious choices
2. **Simplicity** — Most straightforward path; prefer core language constructs → stdlib → google libs → external deps ("least mechanism")
3. **Concision** — High signal-to-noise; relevant details surfaced, noise buried
4. **Maintainability** — Structure enables safe future modification; test coverage validates changes
5. **Consistency** — Matches broader codebase; local style cannot justify diverging from the guide or hiding bugs

All Go files must pass `gofmt`. Never commit unformatted code. Use `gofmt -w .` or `goimports -w .` before every commit.

---

## Packages, Not Programs

- Keep `main` minimal: flag parsing, error printing, and `os.Exit` only
- Domain logic lives in importable packages that return data, never print or call `panic`
- Packages are the unit of reuse; design them to be importable first
- Return errors to callers; let entry points decide how to surface them

## Naming: MixedCaps Only

Go uses `MixedCaps` for all multi-word identifiers — never underscores in Go identifiers:
- Exported: `MaxLength`, `HTTPServer`, `UserID`
- Unexported: `maxLength`, `httpServer`, `userID`
- Never: `max_length`, `HTTP_SERVER`, `Max_Length`

Acronyms use consistent case: `APIKey`, `userID`, `HTTPClient`, `urlStr`.

---

## Naming Conventions

### Packages
- Lowercase, single word, no underscores or camelCase: `auth`, `httputil`, `pgstore`
- Avoid stutter: `auth.Client` not `auth.AuthClient`
- Avoid generic names: `util`, `common`, `misc` carry no meaning

### Types and Interfaces
- Exported types: `PascalCase`
- Single-method interfaces: `-er` suffix (`Reader`, `Writer`, `Stringer`, `Flusher`)
- Multi-method interfaces: describe the role (`Store`, `Handler`, `Executor`)

### Functions and Methods
- Receiver name: short abbreviation of the type name (`c` for `Client`, `s` for `Server`)
- Keep receiver names consistent across all methods of a type
- Constructor pattern: `New<Type>` returns `(*Type, error)`

### Variables
| Name | Use |
|------|-----|
| `err` | errors |
| `ctx` | `context.Context` |
| `buf` | buffers |
| `n` | counts / byte lengths |
| `ok` | boolean existence checks |
| `req` / `resp` | request / response |
| `r` / `w` | `io.Reader` / `io.Writer` |
| `i`, `j`, `k` | loop indices (narrow scope only) |

- Short names for narrow scope; descriptive names for wide scope
- No type in the name: `count` not `intCount`, `users` not `userList`
- Acronyms keep consistent casing: `APIKey`, `userID`, `HTTPServer`

---

## Error Design

- Define sentinel errors as package-level `var`: `var ErrNotFound = errors.New("not found")`
- Match with `errors.Is(err, ErrNotFound)` — never compare error strings
- Wrap with `fmt.Errorf("operation failed: %w", err)` to preserve identity
- Unwrap with `errors.As` to extract typed errors from wrapped chains
- Add context at each layer: what operation failed, with what input
- Never ignore errors with `_`; never swallow with empty `catch`/`recover`

```go
// Bad
if err != nil {
    return err  // no context
}

// Good
if err != nil {
    return fmt.Errorf("fetch user %d: %w", id, err)
}
```

---

## Concurrency

- Introduce goroutines only when necessary; don't parallelize for its own sake
- All goroutines must terminate before the enclosing function returns
- Use `sync.WaitGroup` or `golang.org/x/sync/errgroup` for fan-out/fan-in
- Propagate cancellation via `context.Context`; check `ctx.Done()` in loops
- Type channel parameters directionally: `chan<- T` (send-only), `<-chan T` (receive-only)
- No mutable package-level variables; guard shared state with `sync.Mutex` or a single owner goroutine
- Avoid `init()` functions that modify global state

```go
// Directional channels prevent misuse at compile time
func producer(out chan<- int) { ... }
func consumer(in <-chan int) { ... }
```

---

## Performance Patterns

Profile before optimizing (`go tool pprof`). Apply these patterns only where measurement shows a bottleneck.

### 1. Object Pooling — `sync.Pool`
Reuse allocated objects to reduce GC pressure on high-churn types.
```go
var pool = sync.Pool{New: func() any { return &bytes.Buffer{} }}
buf := pool.Get().(*bytes.Buffer)
buf.Reset()
defer pool.Put(buf)
```

### 2. Memory Preallocation
Allocate with known capacity to avoid repeated resizes.
```go
out := make([]Item, 0, len(input))
index := make(map[string]int, len(keys))
```

### 3. Struct Field Alignment
Order fields largest → smallest to minimize padding bytes.
```go
// Bad: wastes padding between bool and int64
type Bad struct { flag bool; value int64; id int32 }

// Good: no wasted padding
type Good struct { value int64; id int32; flag bool }
```
Use `go vet -fieldalignment` to detect misaligned structs.

### 4. Avoid Interface Boxing
Interface conversions in hot paths cause heap allocations. Use concrete types where performance matters.
```go
// Hot path: use concrete type, not interface
func sum(nums []int64) int64 { ... }  // not []any
```

### 5. Zero-Copy Techniques
Slice into existing buffers instead of copying.
```go
// Avoid: allocates new slice
copy := append([]byte{}, src[start:end]...)

// Prefer: zero-copy view (read-only safe)
view := src[start:end]
```
Use `strings.Builder` for string concatenation; `io.Reader` chains for streaming.

### 6. GC Pressure Reduction
- Reuse buffers; avoid short-lived allocations in loops
- Use value types (structs) over pointers where the struct is small
- Batch allocations: allocate a slice of structs rather than many individual pointers

### 7. Escape Analysis
Inspect what escapes to the heap:
```
go build -gcflags="-m" ./...
```
Values that escape unexpectedly often indicate unnecessary interface conversions or pointer returns.

### 8. Goroutine Worker Pools
Cap concurrency with a fixed-size pool to bound memory and CPU.
```go
const workers = runtime.NumCPU()
jobs := make(chan Job, len(input))
var wg sync.WaitGroup
for range workers {
    wg.Add(1)
    go func() {
        defer wg.Done()
        for job := range jobs { process(job) }
    }()
}
for _, job := range input { jobs <- job }
close(jobs)
wg.Wait()
```

### 9. Atomic Operations
Prefer `sync/atomic` over mutex for simple counters and flags.
```go
var count atomic.Int64
count.Add(1)
n := count.Load()
```

### 10. Lazy Initialization — `sync.Once`
Delay expensive setup until first use.
```go
var (
    instance *Client
    once     sync.Once
)
func getClient() *Client {
    once.Do(func() { instance = newExpensiveClient() })
    return instance
}
```

### 11. Immutable Data Sharing
Pass values between goroutines by value or via read-only interfaces to avoid locking.
```go
type Config struct { ... }  // value type, copied on pass
// Goroutines read cfg without mutex — it never changes
go worker(cfg)
```

### 12. Context Propagation
Attach deadlines and cancellation at the call site; propagate via `context.Context`.
```go
ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
defer cancel()
result, err := store.Fetch(ctx, id)
```

### 13. Buffered I/O
Wrap unbuffered readers/writers to reduce syscall frequency.
```go
r := bufio.NewReaderSize(conn, 64*1024)
w := bufio.NewWriterSize(conn, 64*1024)
defer w.Flush()
```

### 14. Batching
Aggregate small operations to reduce round trips.
```go
// Instead of N individual inserts, batch:
stmt := `INSERT INTO items (id, val) VALUES ` + placeholders
db.ExecContext(ctx, stmt, args...)
```

### 15. Compiler Flags for Benchmarking
```
# Disable inlining to isolate function cost
go test -bench=. -gcflags="-l"

# Build with optimizations for production measurement
go build -ldflags="-s -w"
```

---

## Logging

- Use `log/slog` (stdlib, structured, zero-dep):
```go
slog.Info("user created", "id", user.ID, "email", user.Email)
slog.Error("fetch failed", "err", err, "userID", id)
```
- Libraries must never call `log.Fatal`, `log.Panic`, or `fmt.Println`; return errors instead
- Log at action boundaries, not inside implementation helpers
- Never log passwords, tokens, PII, or raw request bodies

---

## Security

- Use `os.Root` (Go 1.23+) for rooted filesystem access to prevent path traversal:
```go
root, err := os.OpenRoot("/var/data")
f, err := root.Open(userProvidedPath)  // cannot escape /var/data
```
- Never pass user input directly to `os.Open`, `exec.Command`, or SQL queries
- Use `crypto/rand` for all random values needing security properties
- Parameterize all database queries; never interpolate user strings into SQL
- Constant-time comparison for secrets: `subtle.ConstantTimeCompare`

---

## Static Assets

- Bundle static files with `//go:embed` — no runtime path assumptions:
```go
//go:embed templates/* static/*
var assets embed.FS
```
- Never construct paths with `filepath.Join(os.Getenv("HOME"), ...)` in library code

---

## Testing

- Table-driven tests for multiple scenarios:
```go
tests := []struct {
    name    string
    input   string
    want    int
    wantErr bool
}{
    {"empty input", "", 0, true},
    {"valid input", "42", 42, false},
}
for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) { ... })
}
```
- Always run with `-race` flag: `go test -race ./...`
- Place fixtures in `testdata/` directory (ignored by `go build`)
- Use real implementations over mocks; mock only at external service boundaries
- Benchmark with `testing.B`; profile with `go test -cpuprofile/memprofile`
