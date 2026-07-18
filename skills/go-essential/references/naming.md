# Naming — Depth

Loaded on demand from [go-essential](../SKILL.md) §2. The short rules live there; this file is
the why, the worked code, and the decision tables.

> "Names are the architecture." A reader who never opens the implementation should infer what a
> name does, who owns it, and how it fails from the name alone.

## MixedCase, Not snake_case or ALL_CAPS

Go uses `MixedCase` (CamelCase). `localVar`, `exportedVar`. Underscores appear only in cgo, test
files (`_test.go`), generated code, and the rare `//go:` directive.

**Capitalization controls visibility** — the first letter upper-case exports. `ALL_CAPS`
constants conflict with that rule, look like C, and don't add signal:

```go
// ✗ Bad
const MAX_RETRIES = 5
var DEFAULT_TIMEOUT = 30 * time.Second

// ✓ Good
const MaxRetries = 5
var DefaultTimeout = 30 * time.Second
```

## Packages

- **Lowercase, single word where possible.** `http`, `json`, `url`. Hyphens only in the module
  path, never in package names.
- **Singular, not plural.** `list` not `lists`; `buffer` not `buffers`.
- **Match the directory.** A package at `internal/order/` is `package order`.
- **Don't stutter.** `user.NewUser()` → `user.New()`. `config.LoadConfig()` → `config.Load()`.
- **Avoid generic names** — `util`, `common`, `helpers`, `misc` are code-smell; they collect
  unrelated code. Split by concern instead.

## Exported Identifiers and Stutter

```go
// ✗ Bad — name restates the package
package user
func NewUser() *User { ... }
func DeleteUser(u *User) { ... }

// ✓ Good — package provides context
package user
func New() *User { ... }
func Delete(u *User) { ... }
```

At the call site: `user.New()`, `user.Delete(u)` — clear without restating the package name.

## Interfaces

- **Single-method interfaces end in `-er`:** `Reader`, `Writer`, `Closer`, `Stringer`.
- **Behavioral name from the method:** `type Reader interface { Read(p []byte) (int, error) }`.
- **Don't prefix with `I`** (Java/CLR convention). Go uses the bare behavior name.
- **Consumer-side definition.** Define the interface next to the code that consumes it, not next
  to the implementation.

```go
// In the consumer package
type OrderStore interface {
    Get(ctx context.Context, id string) (*Order, error)
    Put(ctx context.Context, o *Order) error
}
// The producer (order/db package) exports a concrete *DB; the consumer adapts.
```

## Errors

- **Error variable: `Err` prefix.** `var ErrNotFound = errors.New(...)`.
- **Error type: `Error` suffix.** `type PathError struct { ... }`.
- **Error strings fully lowercase, no trailing punctuation, including acronyms.** `"invalid
  message id"`, not `"Invalid message ID."` (the `errors.New` and `fmt.Errorf` doc comments
  specify this; linters enforce it).
- **Sentinel errors include the package name.** `var ErrNotFound = errors.New("user: not found")`
  — the prefix tells the reader where the error originated in a chain.
- **Wrap with the operation, not the error.** `fmt.Errorf("querying users: %w", err)` — not
  `fmt.Errorf("%w", err)` (no context added) or `fmt.Errorf("user error: %v", err)` (loses the
  chain).

## Acronyms

Upper-case the whole acronym in `MixedCase`:

- `URL`, `HTTP`, `ID`, `API`, `JSON`, `XML`, `SQL`, `TCP`, `UDP`, `IP`, `OS`, `GC`.

| ✗ Bad              | ✓ Good            |
| ------------------ | ----------------- |
| `parseUrl`         | `parseURL`        |
| `httpServer`       | `HTTPServer`      |
| `userId`           | `userID`          |
| `jsonDecoder`      | `JSONDecoder`     |

**Exception:** error strings stay lowercase: `"invalid user id"`, not `"invalid user ID"`.

## Conventional Suffixes

- **`-er` for single-method interfaces:** `Reader`, `Stringer`, `Marshaller`.
- **`-ed` for past-tense actions:** `closed`, `started`, `initialized`.
- **`-ing` for ongoing actions:** `streaming`, `processing`.
- **`Must*` for panicking constructors:** `MustParse`, `MustCompile` — caller asserts the input
  is valid and accepts the panic otherwise. Use only at init time or in tests.
- **`f` suffix for format funcs:** `Errorf`, `Wrapf`, `Sprintf` — take a `printf`-style format
  string.
- **`With*` for functional-option setters:** `WithTimeout`, `WithLogger`.

## Booleans

Positive names, not negative. `enabled` not `disabled`; `ready` not `notReady`. A double
negative (`!disabled`) is harder to read than a positive (`enabled`).

## Getters and Setters

Go does not prefix getters with `Get`. Setters do use the `Set` prefix.

```go
type Account struct{ balance int64 }

func (a *Account) Balance() int64 { return a.balance }     // not GetBalance
func (a *Account) SetBalance(b int64) { a.balance = b }
```

## Common Mistakes

```go
// ✗ Bad
func GetUserInfoByID(userID int) (UserInfo, error)  // stutter, mixed convention
const MAX_CONN = 10                                 // ALL_CAPS
var HttpServer *http.Server                         // lowercase acronym

// ✓ Good
func Info(id int) (UserInfo, error)                 // package context implies "User"
const MaxConns = 10                                 // MixedCase, visibility signal
var httpServer *http.Server                         // consistent acronym casing
```
