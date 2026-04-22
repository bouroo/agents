---
description: Mobile Backend Review Checklist - Comprehensive code quality, security, and architecture review
---

# Mobile Backend Review Workflow

Perform a structured review of `$ARGUMENTS` (or current working directory) against the Mobile Backend Review Checklist. Follow these steps:

## Steps

### 1. Scope Determination
- If `$ARGUMENTS` is provided, review those files/paths
- Otherwise, run `execute` with `git diff --name-only HEAD~1` to find changed files
- If no git history, review all tracked source files in the project

### 2. Initialize Tracking
Use `todowrite` to create a task list for each checklist section:
- Code Quality
- Project Architecture
- Web Server Configuration
- Message Queue Producer/Consumer
- Primary Database Operations
- Secondary Database Operations
- Cache Operations
- REST Client Configuration
- Cloud Services
- Container & Deployment
- Logging Practices

### 3. Read & Analyze
Read every file in scope. Understand intent, context, and conventions before judging.

### 4. Checklist Evaluation

Evaluate code against the following checklist. Use `task` with `general` subagent for large scopes.

---

## Checklist

### 1. Code Quality

| No. | Severity | Check | Rationale |
|-----|----------|-------|-----------|
| 1 | P2 | Code format passes with zero warnings | Enforced lint in CI |
| 2 | P0 | Precision variables use appropriate types, never floating point for monetary values | Precision loss causes data discrepancies |
| 3 | P1 | No implicit initialization; use explicit initialization | Implicit side effects break test isolation |
| 4 | P1 | Sentinel errors use defined types; use proper error matching | Never match error message strings |
| 5 | P0 | No global mutable variables; all state via Dependency Injection | Global state = data race + untestable |
| 6 | P2 | All magic numbers/strings declared as constants or config values | Never hardcoded in logic |
| 7 | P2 | Naming follows project conventions | Package names short/descriptive |
| 8 | P1 | Cleanup handlers not accumulated in loops | Cleanup handlers only execute when enclosing scope exits |
| 9 | P2 | Interfaces are small (≤5 methods); no "god interfaces" | Interface Segregation Principle |
| 10 | P2 | Data structure field ordering considers memory alignment | Validate with appropriate linter |

**Request Input Validation:**
| 11 | P0 | All request bodies bound and validated before use | Never proceed with unvalidated input |
| 12 | P1 | Format-specific validators for email, URL, identifier fields | Reject malformed input at boundary |
| 13 | P0 | Request body size limited | Prevents DoS |
| 14 | P1 | Pagination params validated: page >= 1, limit between 1 and max | Enforce server-side max |

**Error Handling:**
| 15 | P2 | Wrap errors at every layer | Clear debug stack trace |
| 16 | P2 | No ignored errors; add comment if necessary | Ignored error = bug waiting to happen |
| 17 | P0 | Fatal errors only for programmer errors, never as error return | Unrecovered fatal errors crash process |
| 18 | P2 | No fatal logging in library code; only in main/bootstrap | Fatal calls bypass cleanup handlers |
| 19 | P2 | Timeout/deadline contexts always paired with cleanup handlers | Prevents context leak |

**Concurrency:**
| 20 | P0 | No concurrent task leaks; every async unit has explicit exit condition | Test with leak detection |
| 21 | P0 | All async units have bounded lifetime; no fire-and-forget | Tie to context or explicit coordination |
| 22 | P1 | Async pool/semaphore for bounded concurrency | Prevent unbounded creation |
| 23 | P0 | Shared data protected by synchronization primitives | Use appropriate locking for read-heavy workloads |
| 24 | P0 | Race detection tests pass with zero data races | Race detector before code push |
| 25 | P2 | Never sleep for synchronization; use explicit coordination | Sleep is non-deterministic |
| 26 | P0 | Context passed to all parallel async units for timeout/cancellation | Parent context must propagate |

**Testing & Quality:**
| 27 | P0 | Unit test coverage ≥80% on business logic | Focus on domain/use-case layer |
| 28 | P2 | Table-driven tests for multi-input/output functions | Easy to add cases, maintainable |
| 29 | P1 | Mock external dependencies via interfaces | Never real integration in unit tests |
| 30 | P2 | Integration tests separated via build tags | Not run by default |
| 31 | P2 | Benchmark tests for hot paths | Track allocations per operation |
| 32 | P0 | Async leak detection in tests | Critical for async-spawning tests |

**Memory & Resource Management:**
| 33 | P1 | No reference retaining large underlying arrays | Use copy for sub-ranges or references kept long-term |
| 34 | P1 | String concatenation in loops uses efficient builder | Concatenation in loop = O(n²) allocation |
| 35 | P0 | Response body/IO always closed | Unclosed resource leaks |
| 36 | P1 | Large allocations avoided in request-scoped handlers | Pre-allocate buffers, reuse via pool |
| 37 | P1 | Collection pre-allocate capacity | Reduces memory reallocation and GC pressure |
| 38 | P2 | Pool for frequently created/destroyed objects in hot path | Reduces GC pressure |
| 39 | P1 | Atomic operations used for simple counters/flags instead of locks | 5-10x faster than locks |

---

### 2. Project Architecture

| No. | Severity | Check | Rationale |
|-----|----------|-------|-----------|
| 1 | P2 | Domain layer has zero dependencies on infrastructure | Dependency rule; domain is pure |
| 2 | P1 | Port (Interface) declared in Domain/Application layer, not Infrastructure | Decouples business logic from external |
| 3 | P2 | DTO separated from Domain Entity; conversion at handler boundary | Never pass DTO into domain layer |
| 4 | P2 | ORM/document models never used as Domain Entity; mapper between layers | Persistence format is infrastructure concern |

**Dependency Injection & Config:**
| 5 | P1 | All wiring in main entry point, not in business logic | Creates concrete types, injects |
| 6 | P0 | Configuration type/object immutable after load; no runtime modification | Load once at bootstrap; pass via DI as read-only |
| 7 | P0 | Never wrap config with in-memory cache library | Config from file is already in-memory |
| 8 | P2 | Config validation at startup; fail fast if required config missing | Validation on config struct |
| 9 | P2 | Config per environment clearly separated | Environment-based override, not if-else in code |

---

### 3. Web Server

| No. | Severity | Check | Rationale |
|-----|----------|-------|-----------|
| 1 | P0 | ReadTimeout, WriteTimeout, IdleTimeout configured | Prevents slowloris; tune per layer |
| 2 | P1 | Header read timeout separate from request read timeout (5s) | Prevents slow header attack |
| 3 | P1 | Body limit set | Prevents large payload DoS |
| 4 | P0 | CorrelationID/RequestID on every request, propagated in context and headers | End-to-end request tracing |

**Graceful Shutdown:**
| 5 | P0 | SIGTERM/SIGINT intercepted; shutdown called | In-flight requests complete |
| 6 | P0 | Shutdown closes all deps with timeout for deadline | Calculate time of deadline via context |

---

### 4. Message Queue

**Producer Configuration:**
| No. | Severity | Check | Rationale |
|-----|----------|-------|-----------|
| 1 | P0 | Acknowledgment configured for critical data | All replicas ACK before success |
| 2 | P0 | Idempotence enabled if needed | Service deduplicates retried messages |
| 3 | P1 | Message key correct for ordering; same key = same partition | Ordering guaranteed within partition only |
| 4 | P2 | Linger and batch size tuned | Balance throughput vs latency |
| 5 | P2 | Compression configured | Choose appropriate algorithm |

**Consumer Configuration:**
| 6 | P0 | Consumer Group 1:1 with Topic per Use Case | Never share group across different topics |
| 7 | P0 | Manual commit after success only | Auto commit may commit before processing |
| 8 | P1 | Session timeout and heartbeat configured (heartbeat = 1/3 session) | Prevents unnecessary rebalance |
| 9 | P1 | Max poll interval > max processing time per batch | Exceeding causes consumer kick from group |
| 10 | P1 | Offset reset configured appropriately | Choose for suitable use cases |
| 11 | P2 | Fetch min bytes and max wait tuned for batching | - |

**Source Code:**
| 12 | P0 | Idempotent consumer: reprocess causes no side effects | Check idempotency key in DB/Cache before processing |
| 13 | P0 | DLQ: max retries exceeded sends broken message to DLQ; ack original | Poison messages must not block partition |
| 14 | P0 | Consumer Graceful shutdown: close on termination | Returns partitions immediately |
| 15 | P1 | Batch partial failure: do not commit if some messages failed | Per-message offset tracking or separate retry |
| 16 | P1 | Consumer async pool has backpressure | Prevents unbounded creation |
| 17 | P1 | Consumer Group Strategies always configured | Default Round robin |
| 18 | P0 | Producer Graceful shutdown: close waits for in-flight messages | Never exit without close |

---

### 5. Primary Database

**Connection Pool Configuration:**
| No. | Severity | Check | Rationale |
|-----|----------|-------|-----------|
| 1 | P0 | Max open connections should not be too high | Prevents exceeding DB max connections |
| 2 | P1 | Max idle connections >= 70% of max open connections | Too few = churn |
| 3 | P1 | Connection max lifetime = 5-30 minutes | Prevents stale connections after failover |
| 4 | P1 | Connection max idle time closes long-idle connections | Prevents stale connection errors |
| 5 | P0 | Close result sets after every query | Unclosed rows leak connections |
| 6 | P1 | Iteration errors checked after loop completion | Iteration errors missed without explicit check |
| 7 | P2 | Ping at startup | Fail fast if DB unreachable |

**Query Safety & Performance:**
| 8 | P0 | Parameterized queries only; never string concat | SQL injection is P0 security vulnerability |
| 9 | P0 | Every query hits index; EXPLAIN ANALYZE verified | Full scan = slow query = production critical |
| 10 | P0 | No N+1 queries; use JOIN, IN, batch | N+1 in loop scales linearly with data |
| 11 | P2 | No SELECT *; select only needed columns | Wastes bandwidth/memory; may leak sensitive columns |
| 12 | P0 | LIMIT on every list query; no unbounded results | Missing LIMIT can OOM, Network Congestion |
| 13 | P2 | Prepared statements for frequently executed queries | Driver auto-caches |

**Transaction Management:**
| 14 | P0 | Rollback immediately after beginning a transaction | Safe no-op after commit; prevents leaked connections |
| 15 | P0 | Transactional short; no external I/O inside | Long tx = locks = deadlock + pool exhaustion |
| 16 | P2 | Deadlock errors caught and retried | DB aborts one tx on deadlock |

**Schema & Index Design:**
| 17 | P0 | Check Indexes on WHERE/JOIN/ORDER BY columns; composite by selectivity | Equality first, then range; B-Tree default |
| 18 | P2 | Partial indexes for subset-filtered queries if needed | Smaller, faster index |
| 19 | P0 | Foreign keys have indexes; never FK without index on child table | DB does NOT auto-create FK indexes |
| 20 | P1 | No unbounded TEXT/JSON columns in hot query path without index | Without index = full scan |
| 21 | P1 | Random generation used for primary keys | Sequential keys leak info and cause hotspot |
| 22 | P1 | Timezone-aware timestamps used for all timestamp columns | Always stores UTC |
| 23 | P1 | Index column order follows query filter pattern | Leading column must appear in WHERE |
| 24 | P1 | Numeric/Decimal used for money; never floating point | Floating point is inexact |
| 25 | P2 | No over-indexing; each index adds write amplification | Audit unused indexes |

---

### 6. Secondary Database

**Schema Design:**
| No. | Severity | Check | Rationale |
|-----|----------|-------|-----------|
| 1 | P1 | Embedding vs Referencing based on read/write pattern | Embed: always queried together; Reference: updated independently |
| 2 | P0 | No unbounded arrays; document limit exists | Partitioning or separate collection for growing data |
| 3 | P0 | Write Concern majority for critical data | Replicate to majority before ACK |
| 4 | P2 | Read Concern secondaryPreferred | Improves availability and reduces load on primary |
| 5 | P2 | Read Concern majority for consistent reads | Prevents dirty reads |

**Index Design:**
| 6 | P0 | Compound index follows ESR: Equality, Sort, Range by selectivity | Field order must match query pattern |
| 7 | P0 | Every query hits index; explain verified | Full scan = slow |
| 8 | P1 | Index count limited per collection | Each index adds write overhead |
| 9 | P2 | TTL index for expiring data | Auto-deletes expired documents |
| 10 | P1 | No regex in production; use Text Index or Search | Regex ignores indexes except prefix match |
| 11 | P1 | Avoid Negation Operators | Kills index efficiency; leads to full scans |
| 12 | P1 | Case-Insensitive Regex without Collation | High CPU cost; use Case-Insensitive Indexes |

**Driver Configuration:**
| 13 | P0 | MaxPoolSize, MinPoolSize, MaxConnIdleTime configured | Default may not suffice for high throughput |
| 14 | P2 | Projection: fetch only required fields | Wastes bandwidth/memory |
| 15 | P0 | Bulk writes instead of loop insert/update | Reduces round-trips from N to 1 |
| 16 | P0 | ConnectTimeout and SocketTimeout configured | Fail fast on connection issues |
| 17 | P0 | Aggregate pipeline: match and project as earliest stages | Early filter = index used |
| 18 | P0 | Aggregate lookup uses pipeline form with match | Simple form loads entire foreign collection |
| 19 | P0 | Never iterate entire unbounded result | Loads entire result set into memory |
| 20 | P1 | Transactions only for truly atomic multi-document writes | Locks documents and degrades write throughput |
| 21 | P0 | Aggregate pipeline never uses disk spill in production | Writes intermediate data to disk when RAM exceeded |

---

### 7. Cache

**Client Configuration:**
| No. | Severity | Check | Rationale |
|-----|----------|-------|-----------|
| 1 | P0 | Never use KEYS or SCAN | Blocks single thread; production outage |
| 2 | P0 | PoolSize matches concurrency | Default may not match actual concurrent |
| 3 | P1 | Pipeline for multiple sequential commands | Single round-trip instead of N |
| 4 | P0 | ReadTimeout, WriteTimeout, DialTimeout all set | No timeout = indefinite hang |
| 5 | P0 | Min idle connections + max idle connections for latency-sensitive apps | Pre-warms connections at startup |

**Operations:**
| 6 | P0 | Atomic increment/decrement used for counters | GET+SET is not atomic |
| 7 | P0 | SET with expiration used; never SET then EXPIRE as separate command | Two separate commands; crash = memory leak |
| 8 | P0 | Fetch-and-invalidate uses atomic operation | GET + DEL is non-atomic |
| 9 | P0 | Large operations bounded; never fetch entire large collection | Single blocking operation |
| 10 | P1 | Subscribe reconnect always handled | Connection drops silently on restart |

**Key Design & Eviction:**
| 11 | P1 | Most keys have TTL | No TTL = memory leak |
| 12 | P1 | No big keys; values split or compressed | Big keys cause latency spikes |
| 13 | P1 | Cache invalidation strategy documented and tested | Various patterns; tested stale tolerance |

**Cluster:**
| 14 | P0 | Multi-key commands only on keys sharing same cluster slot | Cluster rejects cross-slot multi-key commands |
| 15 | P0 | Keys with same logical group use grouping tag | Cluster hashes to determine slot |
| 16 | P0 | No hot grouping tag | Hot tag = all traffic hits one shard |

**Distributed Lock:**
| 17 | P1 | Atomic set-if-not-exists with expiration for lock acquire | Atomic: set only if not exists |
| 18 | P1 | Lock TTL more than max critical section execution time | Premature expiry = two processes in critical section |

---

### 8. REST Client

**Client Configuration:**
| No. | Severity | Check | Rationale |
|-----|----------|-------|-----------|
| 1 | P0 | Custom client; never use default | Default has no timeout, no tuned transport |
| 2 | P0 | SetTimeout (10-30s depending on SLA) | Covers entire request lifecycle |
| 3 | P0 | Max idle connections per host tuned | Default starves connection reuse |
| 4 | P1 | Max connections per host limits total connections per host | Caps total conns to one host |
| 5 | P1 | Keep-Alive enabled | Disable forces new TCP+TLS handshake per request |
| 6 | P2 | TLS handshake timeout configured | Fail fast on TLS issues |

**Response Handling:**
| 7 | P0 | HTTP status code checked before decode | 5xx/4xx responses may not be expected format |

**Retry & Circuit Breaker:**
| 8 | P1 | Retry uses Exponential Backoff with Jitter | Fixed-interval retry causes thundering herd |
| 9 | P2 | Retry only on retryable errors | Retrying 4xx or business cases is wasted |
| 10 | P1 | Circuit Breaker threshold, sleep window, and half-open always tuned | Misconfigured CB either opens too eagerly or too late |

**Observability & Security:**
| 11 | P0 | Outgoing request tracing: correlationID, reqID injected into headers | Always tracing fields into header injection |
| 12 | P1 | Sensitive headers not logged | Redact Authorization, API keys, etc. |

---

### 9. Cloud Services

| No. | Severity | Check | Rationale |
|-----|----------|-------|-----------|
| 1 | P0 | SDK v2 used if available | Better performance, context support, modular |
| 2 | P0 | Client created once, reused across requests | Internal pool; recreation is expensive |
| 3 | P1 | Multipart upload/download for large files | PartSize/Concurrency tuned to bandwidth |
| 4 | P2 | Pre-signed URL expiration minimized | Align with business requirement |
| 5 | P2 | Lifecycle policy configured for archival/deletion | Prevents unbounded storage costs |
| 6 | P2 | Long polling configured | Short poll wastes API calls/money |
| 7 | P0 | VisibilityTimeout > max processing time | Premature timeout = duplicate processing |
| 8 | P0 | Delete message after successful processing only | Delete before = loss on crash |
| 9 | P2 | Batch operations used | Reduces API calls and costs |
| 10 | P0 | Secrets cached in memory with TTL refresh | Never call per request; use caching client |

---

### 10. Container & Deployment

| No. | Severity | Check | Rationale |
|-----|----------|-------|-----------|
| 1 | P0 | resources.requests and limits set for CPU and Memory | No limits = unbounded usage = Node crash |
| 2 | P0 | Minimum 2-3 replicas for production | Single replica = SPOF; rolling update = downtime |
| 3 | P2 | Pod disruption budget minAvailable configured | Prevents drain removing all pods |
| 4 | P1 | Liveness probe configured | Prevents zombie pods |
| 5 | P1 | Readiness probe configured | Prevents traffic to pods not yet ready |

---

### 11. Logging

**Structured Logging:**
| No. | Severity | Check | Rationale |
|-----|----------|-------|-----------|
| 1 | P0 | Correlation/Req ID/Trace ID propagated in context through every layer | Every log, DB, HTTP call includes trace_id |
| 2 | P1 | Log Effectiveness: Keep logs optimized for fastest post-mortem | Log must include key data identifiers at each flow step |
| 3 | P0 | Log level on environment: uat, prod should be >= INFO | Should not enable DEBUG on production |
| 4 | P0 | PII never raw logged: passwords, cards, national IDs, tokens | PII in logs = compliance violation; use redactor with hash |
| 5 | P1 | Do not log data you never read or use | Omit fields whose values are always the same |

**Log Deduplication:**
| 6 | P0 | Request/response body logged at most once per request lifecycle | If request pipeline logs the body, downstream handlers must not repeat |
| 7 | P2 | Consumer logs processing once, not on receive + process + commit separately | Single log with all relevant data |
| 8 | P1 | Limit log: truncate field big length | - |
| 9 | P1 | Avoid duplicate or redundant log entries | Log only the most critical steps |

---

### 5. Report Generation

Output a structured review report with severity ratings:

```markdown
## Mobile Backend Review Report

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
- Do not nit-pick style that formatters would fix automatically
- Distinguish canonical rules (must fix) from best-practice suggestions (nice to have)

Trigger this workflow by typing `/vb-review` in the chat.
