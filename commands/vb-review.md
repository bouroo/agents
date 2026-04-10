---
description: Virtual Banking Mobile Backend Review Checklist - Comprehensive code quality, security, and architecture review
agent: code
subtask: true
---

# VB Mobile Backend Review Workflow

Perform a structured review of `$ARGUMENTS` (or current working directory) against the VB Mobile Backend Backend Review Checklist. Follow these steps:

## Steps

### 1. Scope Determination
- If `$ARGUMENTS` is provided, review those files/paths
- Otherwise, run `bash` with `git diff --name-only HEAD~1` to find changed files
- If no git history, review all tracked source files in the project

### 2. Initialize Tracking
Use `todowrite` to create a task list for each checklist section:
- Golang Code Quality
- Project Architecture
- Web Server Configuration
- Kafka Producer/Consumer
- PostgreSQL Operations
- MongoDB Operations
- Redis Operations
- REST Client Configuration
- AWS Services
- Kubernetes & Deployment
- Logging Practices

### 3. Read & Analyze
Read every file in scope. Understand intent, context, and conventions before judging.

### 4. Checklist Evaluation

Evaluate code against the following checklist. Use `task` with `code-reviewer` subagent for large scopes.

---

## Checklist

### 1. Golang Code Quality

| No. | Severity | Check | Rationale |
|-----|----------|-------|-----------|
| 1 | P2 | Code format passes (gofmt, goimports, golangci-lint with zero warnings) | Enforced lint in CI |
| 2 | P0 | Money/precision variables use `decimal` types, never `float32`/`float64` | IEEE 754 precision loss causes monetary discrepancies |
| 3 | P1 | No `init()` unless absolutely necessary; use explicit initialization | Implicit side effects break test isolation |
| 4 | P1 | Sentinel errors use `errors.New()` or custom types; use `errors.Is()`/`errors.As()` | Never match error message strings |
| 5 | P0 | No global mutable variables; all state via Dependency Injection | Global state = data race + untestable |
| 6 | P2 | All magic numbers/strings declared as `const` or config values | Never hardcoded in logic |
| 7 | P2 | Naming follows Effective Go: `camelCase` unexported, `PascalCase` exported | Package names short/descriptive |
| 8 | P1 | `defer` not used inside loops | Defer accumulates; only runs when enclosing function returns |
| 9 | P2 | Interfaces are small (≤5 methods); no "god interfaces" | Interface Segregation Principle |
| 10 | P2 | Struct field ordering considers memory alignment | Order large-to-small; validate with fieldalignment linter |

**Request Input Validation:**
| 11 | P0 | All request bodies bound and validated before use | Never proceed with unvalidated input |
| 12 | P1 | Email, URL, UUID fields use format-specific validators | Reject malformed input at boundary |
| 13 | P0 | Request body size limited | Prevents DoS |
| 14 | P1 | Pagination params validated: `page >= 1`, `limit` between 1 and max (e.g., 100) | Enforce server-side max |

**Error Handling:**
| 15 | P2 | Wrap errors at every layer: `fmt.Errorf("action: %w", err)` | Clear debug stack trace |
| 16 | P2 | No ignored errors (`_ = err`); add comment if necessary | Ignored error = bug waiting to happen |
| 17 | P0 | Panic only for programmer errors, never as error return | Unrecovered panic crashes process |
| 18 | P2 | No `log.Fatal()` in library code; only in main/bootstrap | `log.Fatal` calls `os.Exit(1)` bypassing defers |
| 19 | P2 | `context.WithTimeout`/`WithDeadline` always paired with `defer cancel()` | Prevents context leak |

**Concurrency & Goroutines:**
| 20 | P0 | No goroutine leaks; every goroutine has explicit exit condition | Test with `goleak` |
| 21 | P0 | All goroutines have bounded lifetime; no fire-and-forget | Tie to context, WaitGroup, or errgroup |
| 22 | P1 | Goroutine pool/semaphore for bounded concurrency | Prevent unbounded goroutine creation |
| 23 | P0 | Shared data protected by Mutex/RWMutex/channel | RWMutex when read >> write |
| 24 | P0 | `go test -race` passes with zero data races | Race detector before code push |
| 25 | P2 | Never `time.Sleep()` for synchronization; use channel/WaitGroup | Sleep is non-deterministic |
| 26 | P0 | Context passed to all parallel goroutines for timeout/cancellation | Parent context must propagate |

**Testing & Quality:**
| 27 | P0 | Unit test coverage ≥80% on business logic (service layer) | Focus on domain/use-case layer |
| 28 | P2 | Table-driven tests for multi-input/output functions | Easy to add cases, maintainable |
| 29 | P1 | Mock external dependencies via interfaces | gomock, testify/mock; never real integration in unit tests |
| 30 | P2 | Integration tests separated via build tags (`//go:build integration`) | Not run during `go test ./...` by default |
| 31 | P2 | Benchmark tests for hot paths with `b.ReportAllocs()` | Track allocations per operation |
| 32 | P0 | Goroutine leak detection in tests using `goleak.VerifyNone(t)` | Critical for goroutine-spawning tests |

**Memory & Resource Management:**
| 33 | P1 | No memory leak from slice header referencing large underlying array | Use `copy()` for sub-slices kept long-term |
| 34 | P1 | String concatenation in loops uses `strings.Builder` | `s +=` in loop = O(n²) allocation |
| 35 | P0 | HTTP response body/IO always closed: `defer resp.Body.Close()` | Unclosed resource leaks |
| 36 | P1 | Large allocations avoided in request-scoped handlers | Pre-allocate buffers, reuse via `sync.Pool` |
| 37 | P1 | Slice/Map pre-allocate capacity: `make([]T, 0, cap)` | Reduces memory reallocation and GC pressure |
| 38 | P2 | `sync.Pool` for frequently created/destroyed objects in hot path | Reduces GC pressure |
| 39 | P1 | `atomic` operations used for simple counters/flags instead of Mutex | 5-10x faster than Mutex |

---

### 2. Project Architecture

| No. | Severity | Check | Rationale |
|-----|----------|-------|-----------|
| 1 | P2 | Domain layer has zero imports from infrastructure | Dependency rule; domain is pure Go |
| 2 | P1 | Port (Interface) declared in Domain/Application layer, not Infrastructure | Decouples business logic from external |
| 3 | P2 | DTO separated from Domain Entity; conversion at handler boundary | Never pass DTO into domain layer |
| 4 | P2 | ORM/BSON structs never used as Domain Entity; mapper between layers | Tags are infrastructure concern |

**Dependency Injection & Config:**
| 5 | P1 | All wiring in `main.go` (composition root), not in business logic | main.go creates concrete types, injects |
| 6 | P0 | Config struct immutable after load; no runtime modification | Load once at bootstrap; pass via DI as read-only |
| 7 | P0 | Never wrap Viper config with in-memory cache library | Config from YAML is already in-memory |
| 8 | P2 | Config validation at startup; fail fast if required config missing | `go-playground/validator` on config struct |
| 9 | P2 | Config per environment clearly separated | Environment-based override, not if-else in code |

---

### 3. Web Server

| No. | Severity | Check | Rationale |
|-----|----------|-------|-----------|
| 1 | P0 | `ReadTimeout`, `WriteTimeout`, `IdleTimeout` configured | Prevents slowloris; tune per layer |
| 2 | P1 | `ReadHeaderTimeout` separate from `ReadTimeout` (5s) | Prevents slow header attack |
| 3 | P1 | Body limit set | Prevents large payload DoS |
| 4 | P0 | `CorrelationID`/`RequestID` on every request, propagated in context and headers | End-to-end request tracing |

**Graceful Shutdown:**
| 5 | P0 | `SIGTERM`/`SIGINT` intercepted; `e.Shutdown(ctx)` called | In-flight requests complete |
| 6 | P0 | Shutdown closes all deps with context.WithTimeout for deadline | Calculate time of deadline via context |

---

### 4. Kafka

**Producer Configuration:**
| No. | Severity | Check | Rationale |
|-----|----------|-------|-----------|
| 1 | P0 | `acks=all` for critical data (financial, orders) | All replicas ACK before success |
| 2 | P0 | `enable.idempotence=true` if needed | Kafka deduplicates retried messages |
| 3 | P1 | Message key correct for ordering; same key = same partition | Ordering guaranteed within partition only |
| 4 | P2 | `linger.ms` and `batch.size` tuned | Balance throughput vs latency |
| 5 | P2 | `compression.type` set to improve | lz4 for speed, zstd for ratio |

**Consumer Configuration:**
| 6 | P0 | Consumer Group 1:1 with Topic per Use Case | Never share group across different topics |
| 7 | P0 | `enable.auto.commit=false`; manual commit after success only | Auto commit may commit before processing |
| 8 | P1 | `session.timeout.ms` and `heartbeat.interval.ms` (heartbeat = 1/3 session) | Prevents unnecessary rebalance |
| 9 | P1 | `max.poll.interval.ms` > max processing time per batch | Exceeding causes consumer kick from group |
| 10 | P1 | `auto.offset.reset=earliest` for new groups needing history; `latest` for missing messages | Choose for suitable use cases |
| 11 | P2 | `fetch.min.bytes` and `fetch.max.wait.ms` tuned for batching | - |

**Source Code:**
| 12 | P0 | Idempotent consumer: reprocess causes no side effects | Check idempotency key in DB/Redis before processing |
| 13 | P0 | DLQ: max retries exceeded sends broken message to DLQ topic; ack original | Poison messages must not block partition |
| 14 | P0 | Consumer Graceful shutdown: `.Close()` on termination | Returns partitions immediately |
| 15 | P1 | Batch partial failure: do not commit if some messages failed | Per-message offset tracking or separate retry |
| 16 | P1 | Consumer goroutine pool has backpressure (semaphore/worker pool) | Prevents unbounded goroutine creation |
| 17 | P1 | Consumer Group Strategies always configured | Default Round robin |
| 18 | P0 | Producer Graceful shutdown: `Close()` waits for in-flight messages | Never panic/os.Exit() without Close() |

---

### 5. PostgreSQL

**Connection Pool Configuration:**
| No. | Severity | Check | Rationale |
|-----|----------|-------|-----------|
| 1 | P0 | `SetMaxOpenConns` should not be too much (10-20 or calc based on DB limit/pod count) | Prevents exceeding DB max connections |
| 2 | P1 | `SetMaxIdleConns` >= 70% of `MaxOpenConns` | Too few = churn |
| 3 | P1 | `SetConnMaxLifetime` = 5-30 minutes | Prevents stale connections after DB failover |
| 4 | P1 | `SetConnMaxIdleTime` closes long-idle connections | Prevents stale conn errors |
| 5 | P0 | `defer rows.Close()` after every Query | Unclosed rows leak connections |
| 6 | P1 | `rows.Err()` checked after iteration loop | Iteration errors missed without explicit check |
| 7 | P2 | `db.PingContext()` at startup | Fail fast if DB unreachable |

**Query Safety & Performance:**
| 8 | P0 | Parameterized queries only; never string concat | SQL injection is P0 security vulnerability |
| 9 | P0 | Every query hits index; `EXPLAIN ANALYZE` verified | Seq scan = slow query = production critical |
| 10 | P0 | No N+1 queries; use JOIN, IN, batch | N+1 in loop scales linearly with data |
| 11 | P2 | No `SELECT *`; select only needed columns | Wastes bandwidth/memory; may leak sensitive columns |
| 12 | P0 | LIMIT on every list query; no unbounded results | Missing LIMIT can OOM, Network Congestion |
| 13 | P2 | Prepared statements for frequently executed queries | pgx auto-caches; database/sql uses db.Prepare() |

**Transaction Management:**
| 14 | P0 | `defer tx.Rollback()` immediately after `Begin()` | Safe no-op after Commit; prevents leaked connections |
| 15 | P0 | Transactional short; no external I/O (HTTP, Kafka, etc.) inside | Long tx = locks = deadlock + pool exhaustion |
| 16 | P2 | Deadlock errors caught and retried | Postgres aborts one tx on deadlock |

**Schema & Index Design:**
| 17 | P0 | Check Indexes on WHERE/JOIN/ORDER BY columns; composite by selectivity | Equality first, then range; B-Tree default |
| 18 | P2 | Partial indexes for subset-filtered queries if needed | `WHERE status='active'` = smaller, faster index |
| 19 | P0 | Foreign keys have indexes; never FK without index on child table | Postgres does NOT auto-create FK indexes |
| 20 | P1 | No unbounded TEXT/JSONB columns in hot query path without index | JSONB without GIN index = seq scan |
| 21 | P1 | UUID primary key uses `gen_random_uuid()`, not `uuid_generate_v1()` | v1 UUIDs leak MAC address; v4 random UUIDs avoid hotspot |
| 22 | P1 | `TIMESTAMPTZ` used for all timestamp columns; never `TIMESTAMP` | TIMESTAMPTZ always stores UTC |
| 23 | P1 | Index column order follows query filter pattern; leading column must appear in WHERE | Composite index (a, b, c): only usable if query filters on 'a' |
| 24 | P1 | `NUMERIC`/`DECIMAL` used for money; never `FLOAT` or `DOUBLE PRECISION` | FLOAT is inexact (IEEE 754) |
| 25 | P2 | No over-indexing; each index adds write amplification | Audit unused indexes with `pg_stat_user_indexes` |

---

### 6. MongoDB

**Schema Design:**
| No. | Severity | Check | Rationale |
|-----|----------|-------|-----------|
| 1 | P1 | Embedding vs Referencing based on read/write pattern | Embed: always queried together; Reference: updated independently |
| 2 | P0 | No unbounded arrays; 16MB document limit | Bucket Pattern or separate collection for growing data |
| 3 | P0 | Write Concern `w:majority` for critical data | Replicate to majority before ACK |
| 4 | P2 | Read Concern `secondaryPreferred` | Improves availability and reduces load on primary |
| 5 | P2 | Read Concern `majority` for consistent reads | Prevents dirty reads |

**Index Design:**
| 6 | P0 | Compound index follows ESR: Equality, Sort, Range by selectivity | Field order must match query pattern only |
| 7 | P0 | Every query hits index; `.explain("executionStats")` verified | COLLSCAN = full scan = slow |
| 8 | P1 | Index count limited per collection (should be less than 6-10; will be write-heavy) | Each index adds write overhead |
| 9 | P2 | TTL index for expiring data (sessions, logs) | Auto-deletes expired documents |
| 10 | P1 | No `$regex` in production; use Text Index or Atlas Search | `$regex` ignores indexes except prefix match |
| 11 | P1 | Avoid Negation Operators (`$ne`, `$nin`) | Kills index efficiency; leads to full collection scans |
| 12 | P1 | Case-Insensitive Regex without Collation | High CPU cost; use Case-Insensitive Indexes instead |

**Driver Configuration:**
| 13 | P0 | `MaxPoolSize`, `MinPoolSize`, `MaxConnIdleTime` configured (calc based on limit/pod count) | Default 100 may not suffice for high throughput |
| 14 | P2 | Projection: fetch only required fields | Wastes bandwidth/memory; may leak sensitive columns |
| 15 | P0 | `BulkWrite` instead of loop insert/update | Reduces round-trips from N to 1 |
| 16 | P0 | `ConnectTimeout` and `SocketTimeout` configured (less than server timeout) | ConnectTimeout: time to establish TCP connection |
| 17 | P0 | Aggregate pipeline with lookup: `$match` and `$project` as earliest stages; never filter after `$lookup` | `$match` early = index used |
| 18 | P0 | Aggregate `$lookup` uses pipeline form with `$match` on joined field; not simple `localField`/`foreignField` on large collections | Simple form loads entire foreign collection into memory |
| 19 | P0 | `cursor.All()` never used on unbounded result; always limit or stream with `cursor.Next()` | `cursor.All()` loads entire result set into memory |
| 20 | P1 | Transactions only for truly atomic multi-document writes; not single-document ops | Multi-document transactions lock documents and degrade write throughput |
| 21 | P0 | Aggregate pipeline never uses `AllowDiskUse(true)` in production | AllowDiskUse writes intermediate pipeline data to disk when working set exceeds 100MB RAM |

---

### 7. Redis

**Client Configuration:**
| No. | Severity | Check | Rationale |
|-----|----------|-------|-----------|
| 1 | P0 | Never use `KEYS *` or `SCAN` | Blocks Redis single thread; production outage |
| 2 | P0 | `PoolSize` matches concurrency | Default is 10 × GOMAXPROCS; tune to actual concurrent |
| 3 | P1 | Pipeline for multiple sequential commands | Single round-trip instead of N |
| 4 | P0 | `ReadTimeout`, `WriteTimeout`, `DialTimeout` all set | No timeout = indefinite hang |
| 5 | P0 | `MinIdleConns` + `MaxIdleConns` for latency-sensitive apps | MinIdleConns: pre-warms connections at startup |

**Operations:**
| 6 | P0 | `INCR`/`DECR` used for counters; never `GET` → compute → `SET` | GET+SET is not atomic; concurrent writers produce lost-update |
| 7 | P0 | `SET` with `EX`/`PX` used; never `SET` followed by `EXPIRE` as separate command | SET then EXPIRE is two separate commands; server crash = memory leak |
| 8 | P0 | `GETDEL`/`GETEX` used for fetch-and-invalidate; never `GET` then `DEL` | GET + DEL is non-atomic; two consumers can both GET before either DEL |
| 9 | P0 | Large `HSET`/`SMEMBERS`/`LRANGE` bounded; never fetch entire large collection | HGETALL on hash with 1K fields = single blocking O(N) command |
| 10 | P1 | `SUBSCRIBE`/`PSUBSCRIBE` goroutine always handles reconnect | PubSub connection drops silently on Redis restart |

**Key Design & Eviction:**
| 11 | P1 | Most keys have TTL; except some business need permanent cache | No TTL = memory leak -> OOM -> production down |
| 12 | P1 | No big keys; values > 1MB split or compressed | Big keys cause latency spikes |
| 13 | P1 | Cache invalidation strategy documented and tested | Cache-Aside/Write-Through/Write-Behind; tested stale tolerance |

**Redis Cluster:**
| 14 | P0 | Multi-key commands (MGET, MSET, DEL, RENAME) only on keys sharing same hash slot | Redis Cluster rejects cross-slot multi-key commands |
| 15 | P0 | Keys with same logical group use hash tag `{tag}` in Cluster mode | Redis Cluster hashes `{}` to determine slot |
| 16 | P0 | No hot hash tag; one `{}` tag must not hold lot of keys | A hot tag = all traffic hits one shard = single point of bottleneck |

**Distributed Lock:**
| 17 | P1 | `SET key value NX PX timeout` for lock acquire | Atomic: set only if not exists with ms expiration |
| 18 | P1 | Lock TTL more than max critical section execution time | Premature expiry = two processes in critical section |

---

### 8. REST Client

**Client Configuration:**
| No. | Severity | Check | Rationale |
|-----|----------|-------|-----------|
| 1 | P0 | Custom `http.Client`; never use `http.DefaultClient` | DefaultClient has no timeout, no tuned transport |
| 2 | P0 | SetTimeout (10-30s depending on SLA) | Covers entire request lifecycle |
| 3 | P0 | `Transport.MaxIdleConnsPerHost` tuned (50-100; default=2) | Default 2 per host starves connection reuse |
| 4 | P1 | `Transport.MaxConnsPerHost` limits total connections per host | Caps total (idle+active) conns to one host |
| 5 | P1 | `DisableKeepAlives = false` (Keep-Alive enabled, the default) | DisableKeepAlives=true forces new TCP+TLS handshake per request |
| 6 | P2 | `TLSHandshakeTimeout` configured (5-10s) | Fail fast on TLS issues |

**Response Handling:**
| 7 | P0 | HTTP status code checked before JSON decode | 5xx/4xx responses may return HTML, not JSON |

**Retry & Circuit Breaker:**
| 8 | P1 | Retry uses Exponential Backoff with Jitter | Fixed-interval retry causes thundering herd |
| 9 | P2 | Retry only on retryable errors: 5xx, 429, network/timeout | Retrying 4xx or business cases is wasted |
| 10 | P1 | Circuit Breaker threshold, sleep window, and half-open always tuned | Misconfigured CB either opens too eagerly or too late |

**Observability & Security:**
| 11 | P0 | Outgoing request tracing: correlationID, reqID injected into headers | Always tracing fields into header injection |
| 12 | P1 | Sensitive headers (Authorization, API keys) not logged | Redact Authorization, X-Api-Key, etc. |

---

### 9. AWS Services

| No. | Severity | Check | Rationale |
|-----|----------|-------|-----------|
| 1 | P0 | AWS SDK Go v2 used; not v1 (maintenance mode) | Better performance, context support, modular |
| 2 | P0 | AWS client created once, reused across requests | Internal pool; recreation is expensive |
| 3 | P1 | S3: Multipart upload/download for files > 100MB | PartSize/Concurrency tuned to bandwidth |
| 4 | P2 | S3: Pre-signed URL expiration minimized | Align with business requirement |
| 5 | P2 | S3: Always configured Lifecycle policy for archival/deletion if possible | Prevents unbounded storage costs |
| 6 | P2 | SQS: Long polling: `WaitTimeSeconds=20` | Short poll wastes API calls/money |
| 7 | P0 | SQS: `VisibilityTimeout` > max processing time | Premature timeout = duplicate processing |
| 8 | P0 | SQS: Delete message after successful processing only | Delete before = loss on crash |
| 9 | P2 | SQS: Batch operations: `SendBatch`, `DeleteBatch`, `MaxMessages=10` | Reduces API calls and costs |
| 10 | P0 | Secrets Manager: Secrets cached in memory with TTL refresh | Never call SM per request; use caching client |

---

### 10. Kubernetes & Deployment

| No. | Severity | Check | Rationale |
|-----|----------|-------|-----------|
| 1 | P0 | `resources.requests` and `limits` set for CPU and Memory | No limits = unbounded usage = Node crash |
| 2 | P0 | Minimum 2-3 replicas for production | Single replica = SPOF; rolling update = downtime |
| 3 | P2 | `PodDisruptionBudget` minAvailable configured | Prevents drain removing all pods |
| 4 | P1 | Liveness probe configured | Prevents zombie pods that are running but deadlocked |
| 5 | P1 | Readiness probe configured | Prevents traffic being routed to pods not yet ready |

---

### 11. Logging

**Structured Logging:**
| No. | Severity | Check | Rationale |
|-----|----------|-------|-----------|
| 1 | P0 | Correlation/Req ID/Trace ID propagated in context through every layer | Every log, DB, HTTP call includes trace_id |
| 2 | P1 | Log Effectiveness: Keep logs optimized for fastest post-mortem investigation | Log must include key data identifiers at each flow step |
| 3 | P0 | Log level on environment: uat, prod should be ≥ INFO | Should not enable DEBUG on production |
| 4 | P0 | PII never raw logged: passwords, cards, national IDs, OTP, tokens | PII in logs = PDPA/GDPR violation; use redactor with hash |
| 5 | P1 | Do not log data you never read or use | Omit fields whose values are always the same |

**Log Deduplication:**
| 6 | P0 | Request/response body logged at most once per request lifecycle | If middleware logs body, handler must not repeat |
| 7 | P2 | Kafka consumer logs processing once, not on receive + process + commit separately | Single log: topic, partition, offset, result, duration |
| 8 | P1 | Limit log: truncate field big length (more than 1k chars or less) | - |
| 9 | P1 | Avoid duplicate or redundant log entries to reduce log size and cost | Log only the most critical steps |

---

### 5. Report Generation

Output a structured review report with severity ratings:

```markdown
## VB Mobile Backend Review Report

### Summary
- **Total Checks**: <count>
- **P0 (Critical)**: <count> issues found
- **P1 (Should Fix)**: <count> issues found
- **P2 (Nice to Have)**: <count> suggestions

### Critical Issues (P0)
## [P0] <file>:<line> — <checklist item>
<explanation and suggested fix>

### Should Fix (P1)
## [P1] <file>:<line> — <checklist item>
<explanation and suggested fix>

### Suggestions (P2)
## [P2] <file>:<line> — <checklist item>
<explanation and suggested fix>

### Verdict
<APPROVE | REQUEST CHANGES | BLOCKING ISSUES>
<Brief summary of overall quality and priority fixes>
```

### 6. Completion

Mark all tasks complete in `todowrite`. End with a brief verdict: approve, request changes, or blocking issues.

## Principles

- **Severity Legend**:
  - **P0**: Must fix before deploy; direct production impact
  - **P1**: Fix within sprint; reduces technical debt and risk
  - **P2**: Improve when time permits; quality improvement

- Review for the reader, not the writer — code is read far more than written
- Prefer idiomatic patterns in the project's language
- Flag *why* something is wrong, not just *that* it is wrong
- Do not nit-pick style that `gofmt`/`prettier`/formatters would fix automatically
- Distinguish canonical rules (must fix) from best-practice suggestions (nice to have)

Trigger this workflow by typing `/vb-review` in the chat.
