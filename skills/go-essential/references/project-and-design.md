# Project and Design - Depth

Loaded on demand from [go-essential](../SKILL.md) §9. The headline rules live there; this file
covers project layout, functional options, constructors, architecture, and resource lifecycle.

## Ask First

When starting a project, ask the developer (in order):

1. **Software architecture** - clean, hexagonal, DDD, flat? Never impose complex structure on a
   small project.
2. **Dependency injection approach** - manual constructor injection, or a DI library
   (wire, dig/fx), or none at all. The choice affects wiring,
   lifecycle (health checks, graceful shutdown), and project structure.

Right-size structure to scope. A 100-line CLI tool needs no layers of abstraction.

## Module Naming

`go.mod` module path:

- **MUST match the repository URL**: `github.com/username/project-name`
- **Lowercase only**: `github.com/you/my-app`, not `MyApp`
- **Hyphens for multi-word**: `user-auth`, not `user_auth` or `userAuth`
- **Semantic**: name expresses purpose

## Directory Layout

```
project/
  cmd/
    {name}/main.go      # entry point; minimal (parse, wire, Run)
  internal/             # private packages - not importable externally
  pkg/                  # public, exportable packages (omit if none)
  api/                  # OpenAPI/protobuf schemas (services)
  web/                  # frontend assets (services)
  testdata/             # test fixtures
  go.mod
  Makefile
  .gitignore
  .golangci.yml
```

- **`cmd/{name}/main.go`** does flag parsing, dependency wiring, and calls `Run()`. Business
  logic lives in `internal/` or `pkg/`.
- **`internal/`** is enforced by the toolchain - packages here cannot be imported from outside
  the module. Use it for everything proprietary.
- **`pkg/`** only when code is genuinely reusable by external consumers. Don't create it
  speculatively.
- **Packages are lowercase, singular, match the directory name.**

### Project-type quick picks

| Project Type | Use When                           | Key Directories                          |
| ------------ | ---------------------------------- | ---------------------------------------- |
| CLI Tool     | Command-line application           | `cmd/{name}/`, `internal/`, optional `pkg/` |
| Library      | Reusable code for others           | `pkg/{name}/`, `internal/`               |
| Service      | HTTP API, microservice, web app    | `cmd/{service}/`, `internal/`, `api/`, `web/` |
| Monorepo    | Multiple related modules           | `go.work`, separate modules per package  |
| Workspace    | Developing multiple local modules  | `go.work`, replace directives            |

## 12-Factor

For services and applications, follow [12-Factor](https://12factor.net/) conventions:

- Config via environment variables
- Logs to stdout (never to files inside the container)
- Stateless processes
- Graceful shutdown (SIGTERM → drain in-flight → exit)
- Backing services (DB, queue, cache) as attached resources
- Admin tasks as one-off commands: `cmd/migrate/`, `cmd/seed/`, etc.

## Functional Options

The idiomatic constructor pattern in Go. Scales without breaking changes as the API evolves.

```go
type Server struct {
    addr         string
    readTimeout  time.Duration
    writeTimeout time.Duration
    maxConns     int
}

type Option func(*Server) error   // return error if validation can fail

func WithReadTimeout(d time.Duration) Option {
    return func(s *Server) error {
        if d < 0 { return fmt.Errorf("read timeout must be non-negative, got %s", d) }
        s.readTimeout = d
        return nil
    }
}
func WithMaxConns(n int) Option {
    return func(s *Server) error {
        if n < 1 { return errors.New("max conns must be >= 1") }
        s.maxConns = n
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
        if err := opt(s); err != nil { return nil, fmt.Errorf("server option: %w", err) }
    }
    return s, nil
}

srv, err := NewServer(":8080",
    WithReadTimeout(30 * time.Second),
    WithMaxConns(500),
)
```

Options that validate MUST return an error - catch bad config at construction, not at runtime.
Use the builder pattern only when you need complex validation between configuration steps that
the functional-options form can't express cleanly.

## Avoid `init()` and Mutable Globals

`init()`:

- Runs implicitly before `main()` and before tests
- Cross-file order is filename-alphabetical - fragile
- Cannot return errors - failures must `panic` or `log.Fatal`
- Hidden side effects make tests unpredictable

```go
// ✗ Bad - hidden global state, untestable
var db *sql.DB
func init() {
    var err error
    db, err = sql.Open("postgres", os.Getenv("DATABASE_URL"))
    if err != nil { log.Fatal(err) }
}

// ✓ Good - explicit constructor, dependency injected
func NewUserRepository(db *sql.DB) *UserRepository { return &UserRepository{db: db} }
```

## Enums

Place an explicit Unknown/Invalid sentinel at iota 0:

```go
type Status int
const (
    StatusUnknown   Status = iota  // 0 - uninitialized sentinel
    StatusActive                    // 1
    StatusInactive                  // 2
    StatusSuspended                 // 3
)
```

A `var s Status` silently becomes `0` - if that maps to a real state like `StatusReady`, code can
behave as if a state was deliberately chosen when none was. The Unknown sentinel catches it.

## Resource Management

### `defer Close()` immediately

```go
f, err := os.Open(path)
if err != nil { return err }
defer f.Close()   // right here, not 50 lines later

rows, err := db.QueryContext(ctx, query)
if err != nil { return err }
defer rows.Close()
```

### `runtime.AddCleanup` over `runtime.SetFinalizer`

Finalizers are unpredictable, can resurrect objects, and run at unspecified times. Go 1.24+
`runtime.AddCleanup` is the safer alternative for tying cleanup to object lifetime. Better still:
explicit `Close()` via `defer`.

## Resilience

### Timeout every external call

```go
ctx, cancel := context.WithTimeout(ctx, 5 * time.Second)
defer cancel()
resp, err := httpClient.Do(req.WithContext(ctx))
```

### Retry with context awareness

```go
for attempt := 0; attempt < maxAttempts; attempt++ {
    if attempt > 0 {
        select {
        case <-ctx.Done(): return ctx.Err()
        case <-time.After(backoff(attempt)):   // or a reusable *time.Timer
        }
    }
    if err := call(ctx); err == nil { break }
}
```

- Retry logic MUST check `ctx.Err()` between attempts.
- Use exponential or linear backoff. Add jitter to avoid thundering-herd.
- Distinguish retryable (network, 5xx, timeout) from non-retryable (4xx, validation) errors.

### Limit everything

Pool sizes, queue depths, buffers, goroutine counts - unbounded resources grow until they crash.
Prefer `errgroup.SetLimit(n)` over unbounded `g.Go(...)`.

## Data Handling

### `string` vs `[]byte` vs `[]rune`

| Type     | Default for | Use when                                            |
| -------- | ----------- | --------------------------------------------------- |
| `string` | Everything  | Immutable, safe, UTF-8                              |
| `[]byte` | I/O         | Writing to `io.Writer`, building strings, mutations |
| `[]rune` | Unicode ops | `len()` must mean characters, not bytes             |

Avoid repeated conversions - each one allocates. Stay in one type until you need the other.

### Iterators and streaming

Go 1.23+ offers `iter.Seq[T]` and `iter.Seq2[K, V]`. Use them for lazy evaluation instead of
materializing collections.

For large transfers (1M DB rows → HTTP), stream to prevent OOM. Memory stays constant regardless
of dataset size.

### `//go:embed`

```go
import "embed"

//go:embed templates/*
var templateFS embed.FS

//go:embed version.txt
var version string
```

Embeds at compile time - eliminates runtime file-I/O errors and external file dependencies.

## Essential Root Files

Every Go project should have at the root:

- **Makefile** - `make build`, `make test`, `make lint`, `make cover`
- **.gitignore** - `/vendor/`, binary outputs, `.env`, `coverage.out`
- **.golangci.yml** - linter configuration
- **go.mod / go.sum** - module definition and checksums

## Initialization Checklist

When starting a new Go project:

- [ ] Ask the developer their preferred software architecture
- [ ] Ask the developer their preferred DI approach
- [ ] Decide project type (CLI, library, service, monorepo)
- [ ] Right-size the structure to scope
- [ ] Choose module name (matches repo URL, lowercase, hyphens)
- [ ] `go mod init github.com/user/project-name`
- [ ] `cmd/{name}/main.go` for the entry point
- [ ] `internal/` for private code
- [ ] `pkg/` only if you have public libraries
- [ ] For monorepos: `go work init` and add modules
- [ ] `gofmt -s -w .`
- [ ] `.gitignore` with `/vendor/` and binary patterns

## Architecture Principles (Regardless of Pattern)

- **Keep the domain pure** - no framework dependencies in the domain layer.
- **Fail fast** - validate at boundaries, trust internal code.
- **Make illegal states unrepresentable** - use types to enforce invariants.
- **Respect 12-Factor** - see above.
- **Minimize dependencies** - "a little recode > a big dependency."

For deep architecture guides (clean, hexagonal, DDD with file trees and code) see
[Design Patterns](./design-patterns.md).
