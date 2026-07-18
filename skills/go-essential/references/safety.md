# Safety — Depth

Loaded on demand from [go-essential](../SKILL.md) §4. The headline rules live there; this file
covers nil traps, slice/map aliasing, numeric edges, and defensive design in detail.

## Nil Safety

### The typed-nil-interface trap

Interfaces store `(type, value)`. An interface is `== nil` only when both are nil. Returning a
typed nil pointer from an interface-returning function sets the type descriptor, producing a
non-nil interface that still dereferences to nil.

```go
// ✗ Returns interface{type: *MyHandler, value: nil}, which is != nil
func getHandler(enabled bool) http.Handler {
    var h *MyHandler
    if !enabled { return h }   // caller's `if h == nil` will be FALSE
    return &MyHandler{}
}

// ✓ Return untyped nil for the nil case
func getHandler(enabled bool) http.Handler {
    if !enabled { return nil }
    return &MyHandler{}
}
```

This is the most common nil-shaped crash in Go. The fix is always the same: return a bare `nil`
when the interface value should be nil.

### Nil receiver

A method on a pointer receiver is safe to call on a nil pointer as long as the method doesn't
dereference the receiver. The stdlib uses this: `(*bytes.Buffer).String()` works on nil.

```go
func (l *Logger) Log(msg string) {
    if l == nil { return }   // nil-safe
    l.write(msg)
}
```

### Nil map, slice, and channel

| Type    | Index into nil | Write to nil   | Len/Cap of nil | Range over nil |
| ------- | -------------- | -------------- | -------------- | -------------- |
| Map     | Zero value     | **panic**      | 0              | 0 iterations   |
| Slice   | **panic**      | **panic**      | 0              | 0 iterations   |
| Channel | Blocks forever | Blocks forever | 0              | Blocks forever |

```go
// Lazy-init a nil map field on first write
type Registry struct { mu sync.Mutex; items map[string]Item }

func (r *Registry) Register(name string, it Item) {
    r.mu.Lock(); defer r.mu.Unlock()
    if r.items == nil { r.items = make(map[string]Item) }
    r.items[name] = it
}
```

## Slice & Map Safety

### Slice aliasing — the `append` trap

`append` reuses the backing array if capacity allows. Both slices then share memory, so mutating
one corrupts the other.

```go
a := make([]int, 3, 5)        // len=3, cap=5
b := append(a, 4)             // fits in cap — b reuses a's backing array
b[0] = 99                     // a[0] is now also 99

// Force a fresh allocation
b := append(a[:len(a):len(a)], 4)   // full-slice expression pins capacity to len
```

Use `slices.Clone(s)` (Go 1.21+) when you want a guaranteed independent copy.

### Subslice memory retention

A small subslice can keep a large backing array alive indefinitely. If you slice into a large
buffer and keep the slice long-term, copy:

```go
header := make([]byte, 8)
copy(header, bigBuffer[:8])   // header owns an 8-byte array, not bigBuffer's megabytes
```

### Map concurrent access

Maps MUST NOT be read and written concurrently — Go's runtime detects this and crashes hard
(`fatal error: concurrent map writes`). Use `sync.Map` for read-heavy workloads, or
`sync.RWMutex` + plain map when writes dominate.

### `range` produces a copy

The loop variable is a copy of each element. Mutating it doesn't change the slice. Take an index
to mutate in place:

```go
type T struct{ V int }
xs := []T{{1}, {2}, {3}}
for _, x := range xs { x.V *= 2 }      // no effect on xs
for i := range xs { xs[i].V *= 2 }     // mutates xs
```

## Numeric Safety

### Implicit type conversions truncate silently

```go
var v int64 = 3_000_000_000
i32 := int32(v)   // -1294967296 — silent wraparound

// Guard the conversion
if v > math.MaxInt32 || v < math.MinInt32 {
    return fmt.Errorf("value %d overflows int32", v)
}
i32 := int32(v)
```

### Float comparison

IEEE 754 floats don't represent most decimals exactly. `0.1 + 0.2 != 0.3`. Compare with an
epsilon or use `math/big.Rat` for exact decimal arithmetic.

```go
const eps = 1e-9
if math.Abs(a-b) < eps { /* equal */ }
```

### Division

- Integer division by zero panics.
- Float division by zero yields `+Inf`, `-Inf`, or `NaN` — no panic, but corrupts downstream
  math. Guard with `if divisor == 0`.

## Resource Safety

### `defer` runs at function exit, not loop iteration

```go
// ✗ All files stay open until the function returns
for _, path := range paths {
    f, _ := os.Open(path)
    defer f.Close()
    process(f)
}

// ✓ Extract to a function so defer runs per iteration
for _, path := range paths {
    if err := processOne(path); err != nil { return err }
}
func processOne(path string) error {
    f, err := os.Open(path); if err != nil { return err }
    defer f.Close()
    return process(f)
}
```

### Defensive copying

Exported functions returning internal slices/maps SHOULD return copies, not the live reference.
Otherwise callers mutate your internals through the shared backing array.

```go
type Config struct { hosts []string }

func (c *Config) Hosts() []string { return slices.Clone(c.hosts) }
```

For the same reason, prefer unexported struct fields with accessor methods over exported slice/
map fields that anyone can mutate.

## Initialization Safety

### Zero-value design

Design types so `var x MyType` is immediately usable. This eliminates a whole class of
"forgot to initialize" bugs.

```go
// ✓ Zero values of these types are ready to use
var buf bytes.Buffer
var mu sync.Mutex
var wg sync.WaitGroup

// ✗ Zero value panics on first write
type Cache struct { data map[string]any }
var c Cache
c.data["k"] = 1   // panic
```

### `sync.Once` for lazy initialization

Guarantees exactly-once init even under concurrent first-use. Go 1.21+ adds `OnceFunc`,
`OnceValue`, `OnceValues`.

```go
type DB struct { once sync.Once; conn *sql.DB }

func (db *DB) Conn() *sql.DB {
    db.once.Do(func() {
        var err error
        db.conn, err = sql.Open("postgres", dsn)
        if err != nil { panic(err) }   // or convert to explicit init
    })
    return db.conn
}
```

### Avoid `init()`

`init()` runs implicitly, can't return errors, runs before tests, and its cross-file order is
filename-alphabetical. Side effects in `init()` make tests unpredictable. Use explicit
constructors.

### `noCopy` sentinel

Embed to make `go vet` flag accidental copies of structs that must not be copied after first use
(mutexes, channels, internal pointers):

```go
type noCopy struct{}
func (*noCopy) Lock()   {}
func (*noCopy) Unlock() {}

type ConnPool struct {
    noCopy noCopy
    mu     sync.Mutex
    conns  []*Conn
}
```

Always pass such structs by pointer.

## Audit Sub-Agents (Parallel)

When auditing safety across a codebase, split into 5 parallel sub-agents:

1. **Nil traps** — typed-nil-interface returns, nil map writes, nil-receiver safety, nil-channel
   blocks.
2. **Slice/map aliasing** — `append` reusing backing arrays, subslice retention, missing
   `slices.Clone`.
3. **Numeric edges** — int conversions without bounds checks, float `==` comparisons, division by
   zero.
4. **Resource lifecycle** — `defer` in loops, missing `defer Close()`, leaked resources.
5. **Initialization** — broken zero values, `init()` abuse, mutable globals, `noCopy` gaps.
