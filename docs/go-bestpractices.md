# Go Best Practices Summary

## Code Organization
- Write **packages, not programs**; keep `main` minimal.
- Decouple code from environment (avoid deep `os.Getenv`/`os.Args` usage).
- Favor **single-purpose packages** over catch-all `utils`.

## Testing & Readability
- **Test everything**: unit, integration, and end-to-end.
- Write code for **reading first**, then execution.
- Use consistent short names (`err`, `ctx`, `req`, `resp`).

## Safety & Error Handling
- Design **zero-value useful types** or validating constructors.
- Use **constants** instead of magic numbers.
- **Wrap errors** with `%w` and check with `errors.Is`.
- Always handle errors; avoid ignoring with `_`.

## Concurrency
- Avoid mutable global state; prefer local instances.
- Use goroutines sparingly; confine scope.
- Employ `sync.WaitGroup` or `errgroup` for structured concurrency.
- Share immutable data between goroutines when possible.

## Performance Patterns
- **Memory efficiency**:
  - Preallocate slices/maps.
  - Reuse objects (object pooling).
  - Align struct fields to reduce padding.
  - Avoid unnecessary interface conversions (boxing).
- **Concurrency optimization**:
  - Worker pools for controlled goroutine usage.
  - Use `sync.Once` for lazy initialization.
  - Atomic operations for lightweight synchronization.
- **I/O throughput**:
  - Buffered readers/writers.
  - Batch small operations to reduce round trips.
- **Compiler tuning**:
  - Use escape analysis to keep values on stack.
  - Apply build flags (`-gcflags`, `-ldflags`) for performance.

## Logging
- Log only **actionable information**.
- Avoid logging secrets; prefer metrics/tracing for performance data.

## Naming Conventions
- **Identifiers**:
  - camelCase for unexported, PascalCase for exported.
  - Acronyms all caps (`APIKey`, `HTTPClient`, `userID`).
  - Avoid type suffixes (`scoreInt` → `score`).
  - Stick to ASCII letters.
- **Packages**:
  - Lowercase, short, descriptive (`orders`, `slug`).
  - Avoid `utils`, `helpers`, or clashes with stdlib (`url`, `log`).
- **Files**:
  - Lowercase, one word if possible (`server.go`, `cookie.go`).
  - `_test.go` reserved for tests.
- **Functions & Methods**:
  - Avoid chatter: `customer.New()` not `customer.NewCustomer()`.
  - Receiver names short and consistent (`c`, `o`, `hs`).
- **Interfaces**:
  - Single-method interfaces end with `-er` (`Reader`, `Writer`, `Authenticator`).

---
**Core Principle:** *Make it work first, then make it right. Favor clarity, safety, and performance through disciplined naming, error handling, and memory-conscious design.*
