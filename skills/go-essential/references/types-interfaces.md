# Types and Interfaces - Depth

Loaded on demand from [go-essential](../SKILL.md) §5. The headline rules live there; this file
expands on interface design, embedding, type assertions, field tags, and receiver choice.

## Interface Design

> "The bigger the interface, the weaker the abstraction."

### Small and composed

```go
type Reader interface { Read(p []byte) (n int, err error) }
type Writer interface { Write(p []byte) (n int, err error) }

// Composed
type ReadWriter interface { Reader; Writer }
type ReadWriteCloser interface { io.Reader; io.Writer; io.Closer }
```

### Defined where consumed

```go
// package notification - defines only what it needs
type Sender interface { Send(to, body string) error }

type Service struct{ sender Sender }
func NewService(s Sender) *Service { return &Service{sender: s} }

// package email - exports a concrete Client; knows nothing of Sender
type Client struct{ ... }
func (c *Client) Send(to, body string) error { ... }
```

The consumer owns the contract. The implementor stays concrete and decoupled.

### Don't create interfaces prematurely

> "Don't design with interfaces, discover them."

Start concrete. Extract an interface only when there is a second implementation or a test mock
demanding it. A premature interface is pure indirection with no benefit.

### Accept interfaces, return structs

```go
func NewService(store UserStore) *Service { ... }      // ✓ concrete return
func NewService(store UserStore) ServiceInterface { ... }  // ✗ loses concrete access
```

## Compile-Time Interface Check

```go
var _ io.ReadWriter = (*MyBuffer)(nil)
```

Place near the type definition. Free at runtime; build breaks immediately if `MyBuffer` drifts
from the contract.

## Canonical Method Names

Honor stdlib signatures exactly. Don't invent variants:

| Interface     | Package         | Signature                                |
| ------------- | --------------- | ---------------------------------------- |
| `Reader`      | `io`            | `Read(p []byte) (n int, err error)`      |
| `Writer`      | `io`            | `Write(p []byte) (n int, err error)`     |
| `Closer`      | `io`            | `Close() error`                          |
| `Stringer`    | `fmt`           | `String() string`                        |
| `error`       | builtin         | `Error() string`                         |
| `Handler`     | `net/http`      | `ServeHTTP(ResponseWriter, *Request)`    |
| `Marshaler`   | `encoding/json` | `MarshalJSON() ([]byte, error)`          |
| `Unmarshaler` | `encoding/json` | `UnmarshalJSON([]byte) error`            |

`String()` not `ToString()`; `Read(p []byte)` not `ReadData(p []byte)`.

## Type Assertions and Type Switches

### Safe assertion (always)

```go
// ✓ comma-ok - no panic on mismatch
s, ok := val.(string)
if !ok { return errors.New("expected string") }

// ✗ bare form panics
s := val.(string)
```

Go 1.25+: for reflection prefer `reflect.TypeAssert[T](v)` over `v.Interface().(T)`.

### Type switch

```go
switch v := val.(type) {
case string:  fmt.Println(v)
case int:     fmt.Println(v * 2)
case io.Reader: io.Copy(os.Stdout, v)
default:      return fmt.Errorf("unexpected type %T", v)
}
```

### Optional capability

Check at runtime whether a value supports an extra capability, without requiring it on the
primary interface:

```go
type Flusher interface { Flush() error }

func writeData(w io.Writer, data []byte) error {
    if _, err := w.Write(data); err != nil { return err }
    if f, ok := w.(Flusher); ok { return f.Flush() }
    return nil
}
```

This is how `http.Flusher`, `io.ReaderFrom`, etc. work in the stdlib.

## Embedding

### Struct embedding

Embedding promotes the inner type's methods and fields. The receiver of a promoted method is the
*inner* type, not the outer.

```go
type Logger struct{ *slog.Logger }

type Server struct {
    Logger             // promoted: s.Info(...) works
    addr string
}
```

Override by defining a method with the same name on the outer type.

### Embed vs named field

| Use          | When                                                                  |
| ------------ | --------------------------------------------------------------------- |
| **Embed**    | You want to promote the inner type's full API - outer "is a" enhanced |
| **Named field** | You only use the inner type internally - outer "has a" dependency  |

```go
type APIGateway struct { http.Handler }   // embed: exposes Handler methods
type Server     struct { store *Store }   // named: private dependency
```

### Interface embedding

Interfaces embed interfaces to compose contracts:

```go
type ReadWriteCloser interface { io.Reader; io.Writer; io.Closer }
```

## Dependency Injection via Interfaces

```go
type UserStore interface { FindByID(ctx context.Context, id string) (*User, error) }

type UserService struct{ store UserStore }
func NewUserService(s UserStore) *UserService { return &UserService{store: s} }
```

Tests pass a mock `UserStore` - no real database needed.

## Struct Field Tags

Tag every exported field of a marshaled struct.

```go
type Order struct {
    ID        string    `json:"id"           db:"id"`
    UserID    string    `json:"user_id"      db:"user_id"`
    Total     float64   `json:"total"        db:"total"`
    Items     []Item    `json:"items"        db:"-"`
    CreatedAt time.Time `json:"created_at"   db:"created_at"`
    DeletedAt time.Time `json:"-"            db:"deleted_at"`
    Internal  string    `json:"-"            db:"-"`
}
```

| Directive                 | Meaning                                     |
| ------------------------- | ------------------------------------------- |
| `json:"name"`             | Field name in JSON output                   |
| `json:"name,omitempty"`   | Omit field if zero value                    |
| `json:"-"`                | Always exclude from JSON                    |
| `json:",string"`          | Encode number/bool as JSON string           |
| `db:"column"`             | Database column mapping (sqlx, etc.)        |
| `yaml:"name"`             | YAML field name                             |
| `xml:"name,attr"`         | XML attribute                               |
| `validate:"required"`     | Struct validation (go-playground/validator) |

## Pointer vs Value Receivers

| Use pointer `(s *Server)`                       | Use value `(s Server)`                |
| ----------------------------------------------- | ------------------------------------- |
| Method modifies the receiver                    | Receiver is small and immutable       |
| Receiver contains `sync.Mutex` or similar       | Receiver is a basic type              |
| Receiver is a large struct (~128B+)             | Method is a read-only accessor        |
| Consistency: if any method uses pointer, all do | Map and function values (reference types) |

**Receiver consistency is mandatory** - mixing pointer and value receivers on the same type
causes subtle interface-implementation bugs. Pick one and apply to every method.

## Generics over `any`

```go
// ✗ Loses type safety
func Contains(slice []any, target any) bool { ... }

// ✓ Generic, type-safe
func Contains[T comparable](slice []T, target T) bool {
    for _, x := range slice { if x == target { return true } }
    return false
}
```

Use `any` only at true boundaries (JSON decoding, reflection). Everywhere else, generics let the
compiler reject type mismatches at build time instead of producing runtime panics.

## Common Mistakes

| Mistake                                            | Fix                                                |
| -------------------------------------------------- | -------------------------------------------------- |
| Large interfaces (5+ methods)                      | Split into focused 1-3 method interfaces           |
| Defining interface in the implementor package      | Define where consumed                              |
| Returning interface from constructor               | Return a concrete type                             |
| Bare type assertion                                | Always `v, ok := x.(T)`                            |
| Embedding when only a few methods are needed       | Named field + explicit delegation                  |
| Missing field tags on marshaled structs            | Tag every exported field                           |
| Mixing pointer and value receivers                 | Pick one; apply to all methods                     |
| No compile-time interface check                    | Add `var _ Interface = (*Type)(nil)`               |
| `ToString()` instead of `String()`                 | Honor canonical method names                       |
| Premature interface with single implementation     | Start concrete; extract when second impl appears   |
| Nil map/slice in zero-value struct                 | Lazy-init in methods                               |
| Using `any` for type-safe operations               | Generics (`[T comparable]`)                        |
