# Error Handling — Depth

Loaded on demand from [go-essential](../SKILL.md) §3. The short rules live there; this file is
the why, the worked code, and the inspection patterns.

## Error Creation

Error messages tell the story of *what happened*, lowercase, no trailing punctuation, no
prescribed action.

```go
// ✓ Good — describes what happened
errors.New("unexpected EOF")
fmt.Errorf("parsing token %q: %w", tok, err)

// ✗ Bad — capitalized, prescriptive, or contains an acronym
errors.New("Invalid ID, please check your input")
fmt.Errorf("Failed to connect to %s", host)
```

- **Sentinel errors** (`var ErrNotFound = errors.New("apiclient: not found")`) for expected
  conditions that callers branch on. Include the package name so the origin is identifiable in
  logs.
- **Custom error types** (`type PathError struct { Path string; Op string; Err error }`) when you
  need to carry structured data callers can inspect with `errors.As`.
- **Decision:** sentinel for binary "is this X?", type for "give me the structured details of X."

## Error Wrapping and Inspection

`%w` builds a chain; `%v` flattens it into a single string. Wrap with `%w` so `errors.Is` and
`errors.As` can walk the chain. Use `%v` only at system boundaries to avoid leaking internals.

```go
// Build a chain
if err := parseConfig(path); err != nil {
    return fmt.Errorf("loading config from %q: %w", path, err)
}

// Walk the chain — sentinel match
if errors.Is(err, ErrNotFound) { ... }

// Walk the chain — typed extraction
var perr *fs.PathError
if errors.As(err, &perr) {
    log.Printf("path failure: %s", perr.Path)
}

// Go 1.26+ — type-safe extraction when T implements error
if perr, ok := errors.AsType[*fs.PathError](err); ok { ... }

// Go 1.20+ — combine independent errors
return errors.Join(err1, err2, err3)
```

NEVER branch on error string contents (`strings.Contains(err.Error(), "timeout")`) — wrap with a
typed/sentinel error and inspect the chain. Messages change; types and sentinels don't.

## Single Handling Rule

An error is either logged OR returned, NEVER both. Logging-then-returning produces duplicate
entries in log aggregators — the same failure appears at the call site and at every wrapping
layer.

```go
// ✗ Bad — logs and returns
func (s *Service) Do(ctx context.Context, x string) error {
    if err := s.repo.Save(ctx, x); err != nil {
        slog.Error("save failed", "err", err, "x", x)
        return err   // also returned — will be logged again upstream
    }
    return nil
}

// ✓ Good — wrap and return; let the top-level handler log
func (s *Service) Do(ctx context.Context, x string) error {
    if err := s.repo.Save(ctx, x); err != nil {
        return fmt.Errorf("saving %q: %w", x, err)
    }
    return nil
}
```

The boundary that *owns* the error (HTTP handler, message consumer, top-level goroutine) logs it
once with full context. Internal code wraps and returns.

## Panic and Recover

- `panic` is for truly unrecoverable bugs: a violated invariant, a nil pointer where none should
  exist, a `Must*` constructor at init time. Never for expected error conditions callers can
  handle.
- `recover` only at goroutine boundaries or top-level handlers to prevent one goroutine from
  crashing the process.

```go
func (s *Server) runWorker(ctx context.Context) {
    defer func() {
        if r := recover(); r != nil {
            slog.Error("worker panic", "panic", r, "stack", debug.Stack())
        }
    }()
    // ... worker body ...
}
```

## Structured Logging at Error Sites

Use `log/slog` (Go 1.21+). Keep the log message template stable and low-cardinality so the
aggregator can group; attach IDs, paths, line numbers, counts as structured attributes.

```go
slog.Error("user lookup failed",
    "user_id", id,
    "err", err,
)
// NOT: slog.Error(fmt.Sprintf("user %s lookup failed: %v", id, err))
```

For production-grade stack traces, tenant/user context, error codes, and APM integration, wrap
errors with a typed error that carries that metadata, or use an error-structuring library that
preserves the chain and integrates with `slog`/OpenTelemetry.

## Translating at Boundaries

Internal errors carry technical detail for operators. End users see a friendly translation at the
API boundary:

```go
switch {
case errors.Is(err, ErrNotFound):
    return nil, &UserError{Code: "not_found", Message: "We couldn't find that."}
case errors.Is(err, ErrInvalidInput):
    return nil, &UserError{Code: "bad_request", Message: "That input was invalid."}
default:
    // log full err, return generic message
    return nil, &UserError{Code: "internal", Message: "Something went wrong."}
}
```

## Audit Sub-Agents (Parallel)

When auditing error handling across a codebase, split into 5 parallel sub-agents:

1. **Error creation** — `errors.New`/`fmt.Errorf` quality, low-cardinality messages.
2. **Error wrapping** — `%w` vs `%v`, wrapping context present.
3. **Single-handling rule** — find log-and-return pairs, swallowed errors, `_ =` discards.
4. **Panic/recover** — `panic` usage, recovery at goroutine boundaries.
5. **Structured logging** — `slog` at error sites, no PII in messages, low-cardinality templates.
