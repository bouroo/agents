# Go Error Handling in Detail

Reference for `go-essential` §3: sentinel vs. custom types, `%w` vs. `%v`, `errors.Is`/`As`/`Join`, and the single-handling rule.

## 1. Error Creation: Sentinel vs Custom Types

### Sentinel errors
- Used for expected logic flows (`sql.ErrNoRows`, `os.ErrNotExist`, `io.EOF`).
- Defined once at package level: `var ErrNotFound = errors.New("not found")`.
- Match with `errors.Is(err, ErrNotFound)`.
- **Constraint:** do not embed dynamic values (IDs, paths) in a sentinel. If you need per-instance data, use a custom type.
- **Format:** lowercase, no trailing punctuation   `errors.New("out of cheese")`, never `errors.New("Out of Cheese!")`.

### Custom error types
- Used when the caller needs rich contextual data (`Timeout()`, `HTTPStatusCode`, `Field`).
- Implement the `error` interface and an `Unwrap()` method so chain traversal works:

```go
type QueryError struct {
    Query string
    Err   error
}

func (e *QueryError) Error() string { return fmt.Sprintf("query %q: %v", e.Query, e.Err) }
func (e *QueryError) Unwrap() error { return e.Err }
```

- Match with `errors.As(err, &target)` or, on Go 1.26+, `errors.AsType[T](err)`.

### Decision table

| Need | Use |
| --- | --- |
| Match an expected condition across the chain | Sentinel + `errors.Is` |
| Carry structured data callers must read | Custom type + `errors.As` / `errors.AsType` |
| Combine multiple independent failures | `errors.Join` (see §4) |

### Error string formatting rules

- **Lowercase, including acronyms.** `"invalid message id"` not `"invalid message ID"`. The string is concatenated mid-sentence via `fmt.Errorf("...: %w", err)`, so mixed case reads wrong.
- **No trailing punctuation.** `"out of cheese"` not `"Out of Cheese!"`.
- **Describe what happened, not what to do.** `"dial tcp: connection refused"` not `"please check your network"`.
- **Sentinel origin prefix.** Package-level sentinels SHOULD include the package name (`errors.New("apiclient: not found")`); skip for stdlib sentinels where identity is implicit.

## 2. Wrapping and Chains

- Wrap at every layer to build a readable chain: `return fmt.Errorf("reading config: %w", err)`.
- `%w` preserves the underlying error so `errors.Is` / `errors.As` still traverse to the root cause.
- `%v` flattens the message into a string and **breaks** the chain. Use `%v` only at system boundaries (HTTP/gRPC response, public API) to prevent callers from depending on internal error types.

```go
// Internal layer   wrap to preserve the chain
return fmt.Errorf("querying database: %w", err)

// Public API boundary   break the chain to hide internals
return fmt.Errorf("item unavailable: %v", err)
```

### `%w` vs `%v`   decision table

| Layer | Verb | Why |
| --- | --- | --- |
| Internal (service → repo → driver) | `%w` | Preserve the chain so `errors.Is` / `errors.As` traverse to the root cause |
| Public API / system boundary (HTTP, gRPC response) | `%v` | Hide internal error types; prevent callers from depending on internals |
| Logging at the top boundary | neither   log `%+v` or the error directly | The chain is for humans; no wrapping needed |

## 3. Inspecting Errors

- `errors.Is(err, sentinel)` walks the chain (including `Unwrap()` and joined errors) and returns true on a match. **Never** compare with `==`; wrapping breaks equality.
- `errors.As(err, &target)` walks the chain and assigns the first matching typed error. **Never** bare type-assert (`err.(*T)`); wrapping hides the inner type.
- Go 1.26+: `errors.AsType[T](err)` returns `(T, bool)` with the same traversal behaviour, simpler syntax.

```go
// Bad   breaks on wrapped errors
if err == sql.ErrNoRows { ... }
if ve, ok := err.(*ValidationError); ok { ... }

// Good   traverses the entire chain
if errors.Is(err, sql.ErrNoRows) { ... }

var ve *ValidationError
if errors.As(err, &ve) { ... }

// Go 1.26+
if ve, ok := errors.AsType[*ValidationError](err); ok { ... }
```

The performance cost of `errors.Is`/`errors.As` is negligible compared with the cost of a silent misclassification.

### The nil error interface trap

A function whose return type is `error` that returns a typed nil pointer produces a non-nil `error` interface   `{type: *MyErr, value: nil}` is `!= nil` even though the dynamic value is nil, so `if err != nil` checks silently fail. **Rule:** return the untyped `nil` for the no-error case, never a typed nil pointer.

```go
// ✗ Bad   *Config is nil but the error interface is not
func loadConfig(path string) error {
    cfg, err := parseConfig(path)
    if err != nil { return &ConfigError{Path: path, Err: err} }
    cfg.Path = path
    return cfg // callers see err != nil
}

// ✓ Good
func loadConfig(path string) error {
    cfg, err := parseConfig(path)
    if err != nil { return &ConfigError{Path: path, Err: err} }
    cfg.Path = path
    return nil
}
```

## 4. Combining Errors with `errors.Join` (Go 1.20+)

`errors.Join` merges multiple independent errors into one. The combined error is itself inspectable   `errors.Is` and `errors.As` walk each inner error.

### Multi-field validation

```go
func validateUser(u User) error {
    var errs []error
    if u.Name == ""  { errs = append(errs, errors.New("name is required")) }
    if u.Email == "" { errs = append(errs, errors.New("email is required")) }
    return errors.Join(errs...) // returns nil when errs is empty
}
```

### Parallel operations with independent failures

```go
func closeAll(closers ...io.Closer) error {
    var errs []error
    for _, c := range closers {
        if err := c.Close(); err != nil { errs = append(errs, err) }
    }
    return errors.Join(errs...)
}
```

## 5. The Single Handling Rule

An error MUST be handled exactly once: either **logged** or **returned**, never both. Logging then returning produces duplicate entries in log aggregators and obscures root causes.

```go
// Bad   logs AND returns; two entries per failure in production
if err != nil {
    slog.Error("failed to find user", "err", err)
    return err
}

// Good   wrap with context, let the top boundary log once
if err != nil {
    return fmt.Errorf("fetching user: %w", err)
}
```

The top boundary (HTTP middleware, gRPC interceptor, `main`) logs the error once and translates it into a user-facing response.

## 6. Panic and Recover

### When panic is acceptable
- Truly unrecoverable states: programmer error in initialization (`MustCompileRegex`), corrupted invariant, impossible condition.
- **Never** for expected failures   network timeouts, missing files, malformed input. Those are errors.

### Recovering at goroutine boundaries

Wrap HTTP handlers and worker goroutines so one panic cannot crash the process:

```go
func safeHandler(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        defer func() {
            if rec := recover(); rec != nil {
                slog.Error("panic recovered",
                    "panic", rec,
                    "stack", string(debug.Stack()),
                )
                http.Error(w, "internal error", http.StatusInternalServerError)
            }
        }()
        next.ServeHTTP(w, r)
    })
}
```

`panic` allocates a stack trace and unwinds the stack   using it as control flow is both an anti-pattern and a performance hazard.

## 7. Error Visibility at Boundaries

- **Never expose technical errors to end users.** Translate internal errors into stable, user-facing messages at the system boundary; log the technical detail separately.
- **Log levels reflect severity.** `Debug` (verbose diagnostic), `Info` (lifecycle events), `Warn` (degraded but functional), `Error` (someone must act).
- **Stable log grouping.** Keep message templates low-cardinality (`"db connection failed"`). Attach IDs, paths, and counts as structured key-value attributes so aggregators can group by message.

## 8. Go 1.26+ `errors.AsType[T]`

Signature: `func AsType[T error](err error) (T, bool)`. Walks the `Unwrap()` chain like `errors.As` and returns the first matching typed error with `ok`. Prefer it over `errors.As` when `T` implements `error`   no pointer-to-pointer, type-parameter inference. Keep `errors.As(err, &target)` for non-error targets or Go <1.26.

```go
// Go 1.26+
if ve, ok := errors.AsType[*ValidationError](err); ok {
    log.Printf("validation failed on field %s: %s", ve.Field, ve.Msg)
}

// Pre-1.26 or non-error target
var ve *ValidationError
if errors.As(err, &ve) {
    log.Printf("validation failed on field %s: %s", ve.Field, ve.Msg)
}
```

No match returns the zero value of `T` and `ok == false`.

