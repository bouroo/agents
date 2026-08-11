# Networking & I/O Patterns in Go

Reference for `go-essential`: client/server timeouts, transport tuning, long-lived connection deadlines, resilience patterns, and `httptrace` observability.

## 1. Timeouts Are Mandatory

Default `&http.Client{}` and `&http.Server{}` have **no timeouts**. A slow or malicious client will hold file descriptors and goroutines indefinitely. Never ship either unconfigured.

### Server

```go
srv := &http.Server{
    Addr:              ":8080",
    ReadHeaderTimeout: 5 * time.Second,  // headers must arrive within this window
    ReadTimeout:       10 * time.Second, // full request body
    WriteTimeout:      10 * time.Second, // response write
    IdleTimeout:       120 * time.Second, // keep-alive
    Handler:           mux,
}
```

`ReadHeaderTimeout` is preferred over the broader `ReadTimeout`  --  it bounds the slowloris attack without limiting body upload time for legitimate large requests.

### Client

```go
client := &http.Client{
    Timeout: 10 * time.Second, // total: DNS + Dial + TLS + read + write
    Transport: &http.Transport{
        MaxIdleConns:        100,
        MaxIdleConnsPerHost: 10, // DEFAULT IS 2  --  almost always too low
        IdleConnTimeout:     90 * time.Second,
    },
}
```

Prefer layered per-request deadlines via `context.WithTimeout` over a single large `client.Timeout` when you need fine-grained control. Use retries with backoff (e.g. `go-retryablehttp`) for transient failures rather than inflating the global timeout.

## 2. Response Body Lifecycle

ALWAYS `defer resp.Body.Close()`. To allow TCP connection reuse, **drain** the remainder before closing:

```go
resp, err := client.Do(req)
if err != nil { return err }
defer resp.Body.Close()
defer io.Copy(io.Discard, resp.Body) // drain so the conn returns to the pool
// ...read body...
```

Skipping the drain leaves unread bytes on the connection; the runtime closes it instead of reusing it, defeating keep-alive and forcing a fresh TLS handshake on the next call.

## 3. Long-Lived Connections (TCP / WebSocket / gRPC Streams)

For persistent connections, every read and write needs an explicit deadline. A blocked `Read` pins a goroutine and its stack indefinitely; multiplied by 10k connections, this is the classic slow leak.

```go
const timeout = 30 * time.Second

func handle(conn net.Conn) {
    defer conn.Close()
    buf := make([]byte, 4096)
    for {
        if err := conn.SetReadDeadline(time.Now().Add(timeout)); err != nil { return }
        n, err := conn.Read(buf)
        if err != nil { return }

        if err := conn.SetWriteDeadline(time.Now().Add(timeout)); err != nil { return }
        if _, err := conn.Write(buf[:n]); err != nil { return }
    }
}
```

Combine with bounded queues, `errgroup.SetLimit`, and explicit goroutine shutdown on disconnect to keep memory stable under sustained load.

## 4. I/O Buffering

Wrap repeated small reads/writes with `bufio.Reader` / `bufio.Writer` to coalesce syscalls. Flush the writer explicitly:

```go
type framedConn struct {
    net.Conn
    w *bufio.Writer
}

func (f *framedConn) WriteFrame(data []byte) error {
    if err := binary.Write(f.w, binary.BigEndian, uint32(len(data))); err != nil {
        return err
    }
    if _, err := f.w.Write(data); err != nil { return err }
    return f.w.Flush()
}
```

For high-throughput servers, reuse buffers across chunks and consider `sync.Pool` for the `bufio.Reader`/`Writer` instances themselves.

Skip buffering when latency per byte is critical (interactive / real-time protocols) or when buffers would grow without bounds.

## 5. Context Propagation

Always pass the inbound `r.Context()` downstream  --  to DB (`QueryContext`, `ExecContext`), to outbound HTTP (`http.NewRequestWithContext`), and to gRPC. When the client disconnects, Go cancels the context and every downstream operation halts cleanly.

```go
func handler(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    rows, err := db.QueryContext(ctx, "SELECT * FROM users")
    // ...
}
```

For work that must outlive the request (audit log writes, async dispatch), use `context.WithoutCancel(r.Context())` (Go 1.21+)  --  it preserves request-scoped values but strips cancellation.

## 6. Resilience Patterns

### Circuit breaker
Three states protect a failing downstream:

- **Closed**  --  requests flow; failures counted over a sliding window.
- **Open**  --  calls return immediately with an error; no traffic reaches the target.
- **Half-Open**  --  limited trial requests; success transitions to Closed, failure re-Opens.

Without a circuit breaker, a slow dependency piles up client goroutines, exhausts connections, and triggers cascading failure across the system.

### Load shedding
Reject excess load at the perimeter with a bounded queue (`errgroup.SetLimit`, buffered channel, or semaphore). Active shedding incorporates CPU, latency, and error telemetry to shed *before* overflow.

### Graceful degradation
Under overload, return well-formed `503 Service Unavailable` with a `Retry-After` header, or deliver a leaner response (skip analytics, personalization, dynamic content) while preserving core functionality. Validate degraded paths with the same rigour as the happy path.

## 7. Connection Lifecycle Observability (`httptrace`)

Use `net/http/httptrace` to capture timing at each phase  --  DNS, connect, TLS, GotConn, read/write. This is how slow-client hangs get diagnosed.

```go
trace := &httptrace.ClientTrace{
    DNSStart:     func(i httptrace.DNSStartInfo) { slog.Debug("dns start", "host", i.Host) },
    DNSDone:      func(i httptrace.DNSDoneInfo) { slog.Debug("dns done", "err", i.Err) },
    ConnectStart: func(network, addr string) { slog.Debug("connect start", "addr", addr) },
    ConnectDone:  func(network, addr string, err error) { slog.Debug("connect done", "err", err) },
    GotConn:      func(i httptrace.GotConnInfo) { slog.Debug("got conn", "reused", i.Reused) },
}
req = req.WithContext(httptrace.WithClientTrace(req.Context(), trace))
```

Integrate `httptrace` spans with OpenTelemetry tracing so per-phase latency is correlated with distributed traces. Watch `GotConnInfo.Reused`  --  a low reuse ratio means the transport pool is misconfigured or bodies are not being drained.

## 8. Checklist

- [ ] Server has `ReadHeaderTimeout` / `WriteTimeout` / `IdleTimeout`.
- [ ] Client has `Timeout` and a tuned `Transport` (`MaxIdleConnsPerHost` > 2).
- [ ] Every `resp.Body` is `Close()`'d after draining.
- [ ] Long-lived connections set per-op read/write deadlines.
- [ ] Inbound `ctx` propagates to DB and outbound HTTP/gRPC.
- [ ] Background work uses `context.WithoutCancel` when it must outlive the request.
- [ ] Circuit breakers protect every flaky downstream.
- [ ] Load shedding bounds in-flight work under overload.
- [ ] `httptrace` spans feed structured logs + tracing for slow-client debugging.

