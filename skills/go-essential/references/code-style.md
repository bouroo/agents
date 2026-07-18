# Code Style - Depth

Loaded on demand from [go-essential](../SKILL.md) §1. The short rules live there; this file is
the why, the worked code, and the formatting mechanics.

## Clarity Over Cleverness

> "Clear is better than clever." - Go Proverbs

Write for the reader who maintains this at 2 AM. Explicit beats implicit; flat beats nested;
boring beats novel.

```go
// ✗ Bad - clever, dense, fragile under change
func f(x any) any { return map[bool]any{true: "y", false: "n"}[x.(bool)] }

// ✓ Good - obvious
func YesNo(b bool) string {
    if b {
        return "yes"
    }
    return "no"
}
```

## Handle Errors and Edge Cases First

Keep the happy path at minimal indentation. Early-return on every error or edge case; the body
of the function reads as the success path.

```go
// ✗ Bad - happy path buried 4 levels deep
func Process(o *Order) error {
    if o != nil {
        if o.IsValid() {
            if o.Total > 0 {
                // ... happy path, 4 levels in
            } else {
                return ErrZeroTotal
            }
        } else {
            return ErrInvalid
        }
    } else {
        return ErrNil
    }
}

// ✓ Good - guards up front, happy path at indent 1
func Process(o *Order) error {
    if o == nil {
        return ErrNil
    }
    if !o.IsValid() {
        return ErrInvalid
    }
    if o.Total <= 0 {
        return ErrZeroTotal
    }
    // ... happy path
}
```

## Strings: Building, Quoting, Truncating

- **`strings.Builder` for concatenation in loops** - it amortizes allocation across `WriteString`
  calls; the `+` operator allocates a new string every iteration.
- **`+` for trivial concat** - a one-shot `"a" + b` is faster than `strings.Builder` setup.
- **`%q` in errors** to make string boundaries visible: `fmt.Errorf("bad token %q", tok)` shows
  whitespace and quotes; `"bad token " + tok` does not.

```go
// ✗ Bad - allocates per iteration
s := ""
for _, p := range parts {
    s += p + ","
}

// ✓ Good - one allocation
var b strings.Builder
for _, p := range parts {
    b.WriteString(p)
    b.WriteByte(',')
}
result := b.String()
```

## Formatting and Imports

`gofmt` is non-negotiable; `gofumpt` is `gofmt` with stricter opinions (collapses nested ifs,
removes empty lines inside blocks); `goimports` adds missing imports and removes unused ones.

Run `gofumpt -w -l .` in CI; any file it touches fails the build. Format is not a review topic.

**Import grouping, three blocks separated by blank lines:**

```go
import (
    // 1. stdlib
    "context"
    "fmt"

    // 2. third-party
    "github.com/prometheus/client_golang/prometheus"
    "go.opentelemetry.io/otel"

    // 3. project-local (use a consistent prefix)
    "github.com/myorg/myapp/internal/order"
)
```

## Variable Declaration and Lines

- **`:=` for new locals; `var` for zero-value initialization or package scope.**
- **Group related `var` and `const` declarations** at the top of a block or file.
- **No global mutable state.** Inject dependencies explicitly; guard shared state behind a
  single owner (a struct with a mutex, a typed `*atomic.Pointer[T]`, or a channel).
- **Line length** - Go has no hard limit; `gofmt` wraps where it wraps. Aim for readability under
  100-120 chars; let `gofmt` make the call on borderline cases.

## Comments

- Every exported identifier has a doc comment starting with its name.
- Comments explain *why*, not *what*. The code already shows what.
- `// TODO(author): ...` and `// FIXME(author): ...` carry an owner.
- Doc comments are not formatted Markdown; they're plain text with limited structure (parameter
  lists, code blocks via indentation).

See [Documentation](./documentation.md) for the full doc-comment format.

## Control Flow

- **No `else` after a `return`, `break`, `continue`, or `panic`** in the `if` body. `gofumpt`
  enforces this.
- **`switch` over long `if`/`else if` chains** - switch is cheaper and clearer.
- **`for range` is preferred over C-style `for i := 0; i < n; i++`** when the index is used only
  to access the element; use `for i, v := range xs`.
- **Avoid `goto`.** It exists for generated code and parser state machines, not for application
  logic.

## Receiver Consistency

If any method uses a pointer receiver, all methods on that type do. Mixing receiver types is a
common source of subtle bugs (the value method sees a copy; the pointer method sees the
original).

**Pointer receiver when:**

- The method mutates the receiver.
- The struct holds a mutex, a large slice/map, or anything where copies are expensive.
- The struct is large (rule of thumb: >64 bytes).

**Value receiver when:**

- The type is small and immutable.
- The type has a meaningful zero value and methods are pure.

## Common Mistakes

```go
// ✗ Bad - mutating a global
var cache = map[string]string{}
func Get(k string) string { return cache[k] }

// ✓ Good - inject the cache as a dependency
type Store struct{ mu sync.Mutex; m map[string]string }
func (s *Store) Get(k string) string {
    s.mu.Lock(); defer s.mu.Unlock()
    return s.m[k]
}
```

```go
// ✗ Bad - happy path buried in nesting
func Handle(w http.ResponseWriter, r *http.Request) {
    if user := auth(r); user != nil {
        if err := process(user); err == nil {
            w.WriteHeader(200)
        } else {
            http.Error(w, err.Error(), 500)
        }
    } else {
        http.Error(w, "unauthorized", 401)
    }
}

// ✓ Good - guards first
func Handle(w http.ResponseWriter, r *http.Request) {
    user := auth(r)
    if user == nil {
        http.Error(w, "unauthorized", 401)
        return
    }
    if err := process(user); err != nil {
        http.Error(w, err.Error(), 500)
        return
    }
    w.WriteHeader(200)
}
```
