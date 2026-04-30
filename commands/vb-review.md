---
description: Mobile Backend Review Checklist - Comprehensive code quality, security, and architecture review
---

# Mobile Backend Review Workflow

Perform a structured review of `$ARGUMENTS` (or current working directory) against the Mobile Backend Review Checklist.

> **Conductor note**: You do NOT execute steps directly. Decompose this command into the subtasks below, delegate each to the correct subagent, and validate every deliverable before proceeding.

## Constraints

- Every P0 (Critical) check must be evaluated. No P0 item may be skipped.
- Findings must cite exact file paths and line numbers.
- The final verdict is APPROVE only if zero P0 issues remain.

## Phase 1 — Scope & Discovery

Delegate the following in parallel where possible:

### 1.1 Determine review scope
- **Delegate to**: exploration-capable subagent
- **Task**: Identify files to review.
  - If `$ARGUMENTS` is provided, use those paths.
  - Otherwise, find changed files via `git diff --name-only HEAD~1` (delegate to a review or exploration subagent with git permissions).
  - If no git history, review all tracked source files.
- **Deliverable**: List of file paths in scope.

### 1.2 Initialize tracking
- **Owner**: conductor (you)
- **Task**: Use task tracking to create a task list for each checklist section (see Phase 2).
- **Deliverable**: Task list created and visible.

## Phase 2 — Checklist Evaluation

Delegate the following to review-capable subagents. For large scopes, split sections across multiple review-capable subagent tasks.

### 2.1 Code Quality
- **Delegate to**: review-capable subagent
- **Task**: Evaluate all items in the Code Quality checklist below. For each item, state PASS, FAIL, or N/A with file:line evidence.
- **Deliverable**: Evaluated checklist with citations.

**Code Quality Checklist**

| No. | Severity | Check |
|-----|----------|-------|
| 1 | P2 | Code format passes with zero warnings |
| 2 | P0 | Precision variables use appropriate types; never floating point for monetary values |
| 3 | P1 | No implicit initialization; use explicit initialization |
| 4 | P1 | Sentinel errors use defined types; use proper error matching |
| 5 | P0 | No global mutable variables; all state via Dependency Injection |
| 6 | P2 | All magic numbers/strings declared as constants or config values |
| 7 | P2 | Naming follows project conventions |
| 8 | P1 | Cleanup handlers not accumulated in loops |
| 9 | P2 | Interfaces are small (≤5 methods); no "god interfaces" |
| 10 | P2 | Data structures designed for efficient memory and access patterns |
| 11 | P0 | All request bodies bound and validated before use |
| 12 | P1 | Format-specific validators for email, URL, identifier fields |
| 13 | P0 | Request body size limited |
| 14 | P1 | Pagination params validated: page >= 1, limit between 1 and max |
| 15 | P2 | Wrap errors at every layer |
| 16 | P2 | No ignored errors; add comment if necessary |
| 17 | P0 | Process-terminating errors reserved for unrecoverable programmer mistakes, never for routine failures |
| 18 | P2 | No fatal logging in library code |
| 19 | P2 | Timeout/deadline contexts always paired with cleanup handlers |
| 20 | P0 | No concurrent task leaks; every async unit has explicit exit condition |
| 21 | P0 | All async units have bounded lifetime; no fire-and-forget |
| 22 | P1 | Async pool/semaphore for bounded concurrency |
| 23 | P0 | Shared data protected by synchronization primitives |
| 24 | P0 | Race detection tests pass with zero data races |
| 25 | P2 | Never sleep for synchronization; use explicit coordination |
| 26 | P0 | Context passed to all parallel async units for timeout/cancellation |
| 27 | P0 | Unit test coverage ≥80% on business logic |
| 28 | P2 | Table-driven tests for multi-input/output functions |
| 29 | P1 | Mock external dependencies via interfaces |
| 30 | P2 | Integration tests separated from unit tests and not run by default |
| 31 | P2 | Benchmark tests for hot paths |
| 32 | P0 | Async leak detection in tests |
| 33 | P1 | No reference retaining large underlying arrays |
| 34 | P1 | String concatenation in loops uses efficient builder |
| 35 | P0 | Response body/IO always closed |
| 36 | P1 | Large allocations avoided in request-scoped handlers |
| 37 | P1 | Collection pre-allocate capacity |
| 38 | P2 | Pool for frequently created/destroyed objects in hot path |
| 39 | P1 | Appropriate synchronization primitives chosen for the workload |

### 2.2 Project Architecture
- **Delegate to**: review-capable subagent
- **Task**: Evaluate architecture, DI, and config items.
- **Deliverable**: Evaluated checklist with citations.

| No. | Severity | Check |
|-----|----------|-------|
| 1 | P2 | Domain layer has zero dependencies on infrastructure |
| 2 | P1 | Port (Interface) declared in Domain/Application layer, not Infrastructure |
| 3 | P2 | DTO separated from Domain Entity; conversion at handler boundary |
| 4 | P2 | ORM/document models never used as Domain Entity; mapper between layers |
| 5 | P1 | Dependency wiring isolated to bootstrap/entry point, not in business logic |
| 6 | P0 | Configuration type/object immutable after load; no runtime modification |
| 7 | P0 | Never wrap config with in-memory cache library |
| 8 | P2 | Config validation at startup; fail fast if required config missing |
| 9 | P2 | Config per environment clearly separated |

### 2.3 Web Server
- **Delegate to**: review-capable subagent
- **Task**: Evaluate server configuration and graceful shutdown items.
- **Deliverable**: Evaluated checklist with citations.

| No. | Severity | Check |
|-----|----------|-------|
| 1 | P0 | ReadTimeout, WriteTimeout, IdleTimeout configured |
| 2 | P1 | Header read timeout separate from request read timeout (5s) |
| 3 | P1 | Body limit set |
| 4 | P0 | CorrelationID/RequestID on every request, propagated in context and headers |
| 5 | P0 | SIGTERM/SIGINT intercepted; shutdown called |
| 6 | P0 | Shutdown closes all deps with timeout for deadline |

### 2.4 Message Queue
- **Delegate to**: review-capable subagent
- **Task**: Evaluate producer, consumer, and source code items.
- **Deliverable**: Evaluated checklist with citations.

**Producer:**
| No. | Severity | Check |
|-----|----------|-------|
| 1 | P0 | Acknowledgment configured for critical data |
| 2 | P0 | Idempotence enabled if needed |
| 3 | P1 | Message key correct for ordering; same key = same partition |
| 4 | P2 | Linger and batch size tuned |
| 5 | P2 | Compression configured |

**Consumer:**
| No. | Severity | Check |
|-----|----------|-------|
| 6 | P0 | Consumer groups mapped 1:1 to topic per use case |
| 7 | P0 | Manual commit after success only |
| 8 | P1 | Session timeout and heartbeat configured (heartbeat = 1/3 session) |
| 9 | P1 | Max poll interval > max processing time per batch |
| 10 | P1 | Offset reset configured appropriately |
| 11 | P2 | Fetch min bytes and max wait tuned for batching |

**Source Code:**
| No. | Severity | Check |
|-----|----------|-------|
| 12 | P0 | Idempotent consumer: reprocess causes no side effects |
| 13 | P0 | DLQ: max retries exceeded sends broken message to DLQ; ack original |
| 14 | P0 | Consumer Graceful shutdown: close on termination |
| 15 | P1 | Batch partial failure: do not commit if some messages failed |
| 16 | P1 | Consumer async pool has backpressure |
| 17 | P1 | Consumer Group Strategies always configured |
| 18 | P0 | Producer Graceful shutdown: close waits for in-flight messages |

### 2.5 Primary Database
- **Delegate to**: review-capable subagent
- **Task**: Evaluate connection pool, query safety, transactions, and schema design.
- **Deliverable**: Evaluated checklist with citations.

| No. | Severity | Check |
|-----|----------|-------|
| 1 | P0 | Max open connections should not be too high |
| 2 | P1 | Max idle connections >= 70% of max open connections |
| 3 | P1 | Connection max lifetime = 5-30 minutes |
| 4 | P1 | Connection max idle time closes long-idle connections |
| 5 | P0 | Close result sets after every query |
| 6 | P1 | Iteration errors checked after loop completion |
| 7 | P2 | Ping at startup |
| 8 | P0 | Parameterized queries only; never string concat |
| 9 | P0 | Every query hits index; execution plan verified |
| 10 | P0 | No N+1 queries; use JOIN, IN, batch |
| 11 | P2 | Fetch only required fields in data access operations |
| 12 | P0 | LIMIT on every list query; no unbounded results |
| 13 | P2 | Use query parameterization or prepared statements for repeated operations |
| 14 | P0 | Rollback immediately after beginning a transaction |
| 15 | P0 | Transactional short; no external I/O inside |
| 16 | P2 | Deadlock errors caught and retried |
| 17 | P0 | Check Indexes on WHERE/JOIN/ORDER BY columns; composite by selectivity |
| 18 | P2 | Partial indexes for subset-filtered queries if needed |
| 19 | P0 | Foreign keys have indexes; never FK without index on child table |
| 20 | P1 | No unbounded TEXT/JSON columns in hot query path without index |
| 21 | P1 | Random generation used for primary keys |
| 22 | P1 | Timezone-aware timestamps used for all timestamp columns |
| 23 | P1 | Index column order follows query filter pattern |
| 24 | P1 | Numeric/Decimal used for money; never floating point |
| 25 | P2 | No over-indexing; each index adds write amplification |

### 2.6 Secondary Database
- **Delegate to**: review-capable subagent
- **Task**: Evaluate schema, index, and driver configuration.
- **Deliverable**: Evaluated checklist with citations.

| No. | Severity | Check |
|-----|----------|-------|
| 1 | P1 | Embedding vs Referencing based on read/write pattern |
| 2 | P0 | No unbounded arrays; document limit exists |
| 3 | P0 | Write Concern majority for critical data |
| 4 | P2 | Read Concern secondaryPreferred |
| 5 | P2 | Read Concern majority for consistent reads |
| 6 | P0 | Index design follows query filter patterns (ESR pattern) |
| 7 | P0 | Every query hits index; explain verified |
| 8 | P1 | Index count limited per collection |
| 9 | P2 | TTL index for expiring data |
| 10 | P1 | No regex in production; use Text Index or Search |
| 11 | P1 | Avoid Negation Operators |
| 12 | P1 | Case-Insensitive Regex without Collation |
| 13 | P0 | MaxPoolSize, MinPoolSize, MaxConnIdleTime configured |
| 14 | P2 | Projection: fetch only required fields |
| 15 | P0 | Bulk writes instead of loop insert/update |
| 16 | P0 | ConnectTimeout and SocketTimeout configured |
| 17 | P0 | Aggregate pipeline: match and project as earliest stages |
| 18 | P0 | Aggregate lookup uses pipeline form with match |
| 19 | P0 | Never iterate entire unbounded result |
| 20 | P1 | Transactions only for truly atomic multi-document writes |
| 21 | P0 | Aggregate pipeline never uses disk spill in production |

### 2.7 Cache
- **Delegate to**: review-capable subagent
- **Task**: Evaluate client config, operations, key design, cluster, and distributed lock items.
- **Deliverable**: Evaluated checklist with citations.

| No. | Severity | Check |
|-----|----------|-------|
| 1 | P0 | Never use full-keyspace scan commands |
| 2 | P0 | PoolSize matches concurrency |
| 3 | P1 | Pipeline for multiple sequential commands |
| 4 | P0 | ReadTimeout, WriteTimeout, DialTimeout all set |
| 5 | P0 | Min idle connections + max idle connections for latency-sensitive apps |
| 6 | P0 | Atomic increment/decrement used for counters |
| 7 | P0 | SET with expiration used; never SET then EXPIRE as separate command |
| 8 | P0 | Fetch-and-invalidate uses atomic operation |
| 9 | P0 | Large operations bounded; never fetch entire large collection |
| 10 | P1 | Subscribe reconnect always handled |
| 11 | P1 | Most keys have TTL |
| 12 | P1 | No big keys; values split or compressed |
| 13 | P1 | Cache invalidation strategy documented and tested |
| 14 | P0 | Multi-key commands only on keys sharing same cluster slot |
| 15 | P0 | Keys with same logical group use grouping tag |
| 16 | P0 | No hot grouping tag |
| 17 | P1 | Atomic set-if-not-exists with expiration for lock acquire |
| 18 | P1 | Lock TTL more than max critical section execution time |

### 2.8 REST Client
- **Delegate to**: review-capable subagent
- **Task**: Evaluate client config, response handling, retry/circuit breaker, and observability.
- **Deliverable**: Evaluated checklist with citations.

| No. | Severity | Check |
|-----|----------|-------|
| 1 | P0 | Custom client; never use default |
| 2 | P0 | SetTimeout (10-30s depending on SLA) |
| 3 | P0 | Max idle connections per host tuned |
| 4 | P1 | Max connections per host limits total connections per host |
| 5 | P1 | Keep-Alive enabled |
| 6 | P2 | TLS handshake timeout configured |
| 7 | P0 | HTTP status code checked before decode |
| 8 | P1 | Retry uses Exponential Backoff with Jitter |
| 9 | P2 | Retry only on retryable errors |
| 10 | P1 | Circuit Breaker threshold, sleep window, and half-open always tuned |
| 11 | P0 | Outgoing request tracing: correlationID, reqID injected into headers |
| 12 | P1 | Sensitive headers not logged |

### 2.9 Cloud Services
- **Delegate to**: review-capable subagent
- **Task**: Evaluate SDK usage, upload/download, queue, and secret management.
- **Deliverable**: Evaluated checklist with citations.

| No. | Severity | Check |
|-----|----------|-------|
| 1 | P0 | Prefer latest stable SDK version |
| 2 | P0 | Client created once, reused across requests |
| 3 | P1 | Multipart upload/download for large files |
| 4 | P2 | Pre-signed URL expiration minimized |
| 5 | P2 | Lifecycle policy configured for archival/deletion |
| 6 | P2 | Long polling configured |
| 7 | P0 | VisibilityTimeout > max processing time |
| 8 | P0 | Delete message after successful processing only |
| 9 | P2 | Batch operations used |
| 10 | P0 | Secrets cached in memory with TTL refresh |

### 2.10 Container & Deployment
- **Delegate to**: review-capable subagent
- **Task**: Evaluate resource limits, replicas, and health probes.
- **Deliverable**: Evaluated checklist with citations.

| No. | Severity | Check |
|-----|----------|-------|
| 1 | P0 | resources.requests and limits set for CPU and Memory |
| 2 | P0 | Minimum 2-3 replicas for production |
| 3 | P2 | Pod disruption budget minAvailable configured |
| 4 | P1 | Liveness probe configured |
| 5 | P1 | Readiness probe configured |

### 2.11 Logging
- **Delegate to**: review-capable subagent
- **Task**: Evaluate structured logging, deduplication, and PII handling.
- **Deliverable**: Evaluated checklist with citations.

| No. | Severity | Check |
|-----|----------|-------|
| 1 | P0 | Correlation/Req ID/Trace ID propagated in context through every layer |
| 2 | P1 | Log Effectiveness: Keep logs optimized for fastest post-mortem |
| 3 | P0 | Production log level restricted to INFO or higher; DEBUG disabled |
| 4 | P0 | PII never raw logged: passwords, cards, national IDs, tokens |
| 5 | P1 | Do not log data you never read or use |
| 6 | P0 | Request/response body logged at most once per request lifecycle |
| 7 | P2 | Consumer logs processing once, not on receive + process + commit separately |
| 8 | P1 | Limit log: truncate field big length |
| 9 | P1 | Avoid duplicate or redundant log entries |

### 2.12 Spec-Code Alignment
- **Delegate to**: review-capable subagent
- **Task**: Evaluate whether the code matches its specification or plan.
- **Deliverable**: Evaluated checklist with citations.

| No. | Severity | Check |
|-----|----------|-------|
| 1 | P0 | Code implements all features specified in the plan; no specified features missing |
| 2 | P0 | No features implemented beyond what the specification defines (no scope creep) |
| 3 | P1 | Error handling and edge cases align with spec safeguards |
| 4 | P1 | Naming in code matches terminology used in specification |
| 5 | P2 | Specification updated to reflect any refactoring or structural changes |

## Phase 3 — Synthesize & Report

### 3.1 Consolidate findings
- **Owner**: conductor (you)
- **Task**: Gather all reviewer deliverables from Phase 2. Deduplicate findings. Categorize by severity.
- **Deliverable**: Consolidated issue list.

### 3.2 Generate review report
- **Owner**: conductor (you)
- **Task**: Produce the final report in this exact format:

```markdown
## Mobile Backend Review Report

### Summary
- **Total Checks**: <count>
- **P0 (Critical)**: <count> issues found
- **P1 (Should Fix)**: <count> issues found
- **P2 (Nice to Have)**: <count> suggestions

- **Spec-Code Alignment**: <count> issues found

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

### 3.3 Final gate
- **Gate**: Verdict is **APPROVE** only if zero P0 issues remain. If any P0 exists, verdict must be **BLOCKING ISSUES** (or **REQUEST CHANGES** if only P1/P2 remain).
- Use task tracking to mark all tasks complete.

## Severity Legend

- **P0**: Must fix before deploy; direct production impact
- **P1**: Fix within sprint; reduces technical debt and risk
- **P2**: Improve when time permits; quality improvement

## Principles

- Review for the reader, not the writer — code is read far more than written
- Prefer idiomatic patterns in the project's language
- Flag *why* something is wrong, not just *that* it is wrong
- Do not nit-pick style that formatters would fix automatically
- Distinguish canonical rules (must fix) from best-practice suggestions (nice to have)

(End of file - total 254 lines)