# Design Patterns & Idioms - Depth

Loaded on demand from [go-essential](../SKILL.md) §10. The short rules live there; this file is
the why, the worked code, and the decision tables.

Guiding test: a pattern earns its place by solving a real problem in *this* codebase, not by
demonstrating sophistication. "A little copying is better than a little dependency."

## Constructor Patterns: Functional Options vs Builder

Functional options are the Go default. They scale with API evolution without breaking callers,
compose naturally, and read well at the call site. Reach for a builder only when validation
crosses configuration steps (e.g., "if A is set, B must be > 0" and the order matters).

```go
type Server struct {
    addr         string
    readTimeout  time.Duration
    writeTimeout time.Duration
    maxConns     int
}

type Option func(*Server) error // returns error so validation can fail

func WithReadTimeout(d time.Duration) Option {
    return func(s *Server) error {
        if d < 0 {
            return fmt.Errorf("read timeout must be non-negative, got %s", d)
        }
        s.readTimeout = d
        return nil
    }
}

func NewServer(addr string, opts ...Option) (*Server, error) {
    s := &Server{
        addr:         addr,
        readTimeout:  5 * time.Second,
        writeTimeout: 10 * time.Second,
        maxConns:     100,
    }
    for _, opt := range opts {
        if err := opt(s); err != nil {
            return nil, fmt.Errorf("invalid server option: %w", err)
        }
    }
    return s, nil
}

srv, err := NewServer(":8080",
    WithReadTimeout(30*time.Second),
    WithMaxConns(500),
)
```

**Rules:**

- One `Option` type per constructor family; one setter function per option.
- Defaults live in the constructor, not in the struct field tags.
- Options that can fail return an error. Catch bad config at construction, not at runtime.
- Reserve `MustX` constructors (`MustParse`) for package-level initialization where a failure
  means the program cannot start - never in library code called by users.

## Enums and Zero Values

Go has no first-class enums; `iota` produces untyped or typed integer constants. The trap: the
zero value silently passes as the first declared member.

```go
// ✗ Bad - StatusActive is the zero value, so an uninitialized Status is Active
type Status int
const (
    StatusActive Status = iota
    StatusInactive
)

// ✓ Good - Unknown sentinel at 0; real values start at 1
type Status int
const (
    StatusUnknown Status = iota // 0
    StatusActive                // 1
    StatusInactive              // 2
)
```

## Make Illegal States Unrepresentable

Use the type system to enforce invariants. If a transition is impossible, make it impossible to
construct a value that would require it.

```go
// ✗ Bad - every method must re-check state
type Order struct {
    Status string // "open" | "closed" | "shipped"
    Items  []Item
}

// ✓ Good - closed orders are a different type; the compiler enforces the rule
type OpenOrder struct{ items []Item }
type ClosedOrder struct{ items []Item; total int64 }

func (o OpenOrder) Close() ClosedOrder { return ClosedOrder{items: o.items, total: sum(o.items)} }
// CloseOrder has no method to mutate items - the state is locked at construction.
```

Other techniques:

- **Newtype pattern**: `type UserID string`, `type TenantID string` - prevents mixing IDs at
  call sites without runtime cost.
- **Non-empty slices**: a `func NonEmpty[T any](xs []T) ([]T, error)` constructor that rejects
  empty inputs; the empty case is handled once, not in every consumer.
- **Sealed interfaces**: a private method on an interface makes it impossible to implement
  outside the defining package - the set of implementations is closed.

## Resource Management

`defer Close()` immediately after opening. Not 50 lines later, not conditionally, not after some
setup step that might return early.

```go
f, err := os.Open(path)
if err != nil {
    return err
}
defer f.Close() // right here

rows, err := db.QueryContext(ctx, query)
if err != nil {
    return err
}
defer rows.Close()
```

**Close-error nuance:** read-only resources (a file opened for read, an HTTP response body) can
use a bare `defer f.Close()`. Write/flush resources (databases, file writers, buffered writers)
MUST surface close or flush errors when durability matters:

```go
// For a write resource where durability matters
defer func() {
    cerr := w.Close()
    if err == nil {
        err = cerr
    }
}()
```

**`runtime.AddCleanup` over `runtime.SetFinalizer`** (Go 1.24+). Finalizers run at unpredictable
times, can resurrect objects, and have ordering issues. `AddCleanup` is a more predictable
mechanism for resource cleanup tied to object lifetime. For most resources, an explicit `Close()`
or `defer` is still the right answer - cleanup hooks are for cases where the caller may forget.

## Resilience and Limits

Every external call has a timeout. Every pool, queue, and buffer has a bound. Every retry loop
checks context cancellation between attempts.

```go
ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
defer cancel()

resp, err := httpClient.Do(req.WithContext(ctx))
```

**Retry checklist:**

- Check `ctx.Err()` before each attempt; abort if cancelled.
- Use exponential backoff with jitter - fixed intervals thunder-herd downstream.
- Bound the retry count; unbounded retries amplify an outage into a self-DoS.
- After exhausting retries, surface the last error; do not silently swallow it.

**Limit everything:** `errgroup.SetLimit(n)` for bounded concurrency; `semaphore.NewWeighted(n)`
for non-uniform work; bounded channels for backpressure; `sync.Pool` for reusable buffers.

## Data Handling: string vs []byte vs []rune

| Type     | Default for | Use when                                            |
| -------- | ----------- | --------------------------------------------------- |
| `string` | Everything  | Immutable, safe, UTF-8, hashable, map keys           |
| `[]byte` | I/O         | Writing to `io.Writer`, building strings, mutations |
| `[]rune` | Unicode ops | `len()` must mean characters, not bytes             |

Each conversion allocates. Stay in one representation until you need the other.

## Iterators and Streaming (Go 1.23+)

Iterators (`iter.Seq[T]`, `iter.Seq2[K, V]`) let consumers drive iteration - the producer does
not materialize a collection. Use them when:

- The dataset is large and the consumer may exit early (`break` after the first match).
- The producer would otherwise allocate a slice it doesn't need to keep.
- The consumer only scans once (multiple passes warrant a slice).

```go
// Produces a lazy iterator over DB rows - memory stays constant regardless of result size
func Rows(ctx context.Context, db *sql.DB, q string, args ...any) iter.Seq2[Row, error] {
    return func(yield func(Row, error) bool) {
        rows, err := db.QueryContext(ctx, q, args...)
        if err != nil {
            yield(Row{}, err)
            return
        }
        defer rows.Close()
        for rows.Next() {
            r, err := scanRow(rows)
            if !yield(r, err) {
                return
            }
        }
    }
}
```

**Stream large transfers** (DB rows → HTTP, file → S3): wire `io.Reader`/`io.Writer` together
with a fixed-size buffer; never materialize the whole payload in memory.

## Compile-Time Checks

```go
// Interface satisfaction - free at runtime, breaks the build on contract drift
var _ io.Reader = (*MyBuffer)(nil)

// Struct tag validity
var _ = reflect.TypeOf(MyStruct{}).Field(0).Tag
```

## Architecture: Ask First

Ask the developer about architecture preference (clean / hexagonal / DDD / flat) and DI approach
before proposing structure. Don't impose complex architecture on a small project.

Core principles regardless of architecture:

- **Keep the domain pure.** No framework or DB imports in the domain layer.
- **Fail fast at boundaries.** Validate input at the entry point; trust internal code.
- **Respect 12-Factor** for services: env-var config, stdout logs, stateless processes, backing
  services as attached resources.
- **A little recode > a big dependency.** Each dep adds attack surface and an upgrade treadmill.

## Common Mistakes

```go
// ✗ Bad - init() with hidden global state, cannot return errors
var db *sql.DB
func init() {
    var err error
    db, err = sql.Open("postgres", os.Getenv("DATABASE_URL"))
    if err != nil { log.Fatal(err) }
}

// ✓ Good - explicit constructor, injectable
func NewUserRepository(db *sql.DB) *UserRepository {
    return &UserRepository{db: db}
}
```

```go
// ✗ Bad - regexp compiled per call
func ValidEmail(s string) bool {
    re := regexp.MustCompile(`^[^@]+@[^@]+\.[^@]+$`) // O(n) compile, allocates
    return re.MatchString(s)
}

// ✓ Good - compiled once at package level
var emailRE = regexp.MustCompile(`^[^@]+@[^@]+\.[^@]+$`)
func ValidEmail(s string) bool { return emailRE.MatchString(s) }
```

```go
// ✗ Bad - unbounded retry with no cancellation
for {
    if err := doCall(); err == nil { break }
    time.Sleep(time.Second)
}

// ✓ Good - bounded retry, backoff, context-aware
for attempt := 0; attempt < maxAttempts; attempt++ {
    if err := doCall(ctx); err == nil { return nil }
    if ctx.Err() != nil { return ctx.Err() }
    sleepWithJitter(ctx, backoff(attempt))
}
return ErrMaxAttempts
```
