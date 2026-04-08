---
name: error-design
description: Error handling patterns and conventions — sentinel errors, error wrapping, error context, and actionable error messages. Use when handling errors, defining error types, creating error messages, or when the user mentions error handling, error design, or error conventions.
---

# Error Design

Errors are values — create them deliberately, consume them deliberately.

## Core Principles

- Validate all inputs at system boundaries
- Always check errors; never silently ignore them
- Reserve panics/fatal exits for truly unrecoverable internal errors
- Prefer explicit error returns over in-band values (return codes, null, -1)

## Sentinel Errors

Define named sentinel errors for programmatic matching — never match on error strings:

    var ErrNotFound = errors.New("not found")
    if errors.Is(err, ErrNotFound) { ... }

Use structured error types when callers need to extract metadata from errors.

## Error Context (Wrapping)

Wrap errors with context explaining **what operation failed**:

    // Bad — adds nothing new
    return fmt.Errorf("failed: %v", err)

    // Good — adds operation context
    return fmt.Errorf("read config %s: %v", path, err)

- Add only non-redundant information; don't duplicate what the underlying error already says
- Use annotation-only wrapping (`%v`) when caller shouldn't unwrap
- Use transparent wrapping (`%w`) when caller needs programmatic access to the underlying error

## Error Messages

**Internal error strings** — not capitalized, no trailing punctuation (they compose into larger messages):

    errors.New("connection refused")

**Displayed messages** (logs, test failures, API responses) — typically capitalized:

    log.Printf("Server failed to start: %v", err)

- Show actionable messages; include usage hints for invalid arguments
- Never prefix with "failed to" or "error:" — the error itself conveys failure

## Error Flow

Handle errors before happy-path code — early return/continue pattern:

    // Bad — happy path buried in nesting
    if err == nil { /* 50 lines of happy path */ } else { return err }

    // Good — error handled first, flat happy path
    if err != nil { return err }
    // 50 lines of happy path

## Boundary Translation

At system boundaries (RPC, IPC, storage, API edges), translate domain errors into canonical error space. Internal details must not leak to external callers:

    func (s *Server) GetUser(req) -> Response {
        user, err := s.store.GetUser(req.ID)
        if errors.Is(err, store.ErrNotFound) {
            return Response{Code: 404, Message: "User not found"}
        }
        if err != nil {
            log.Printf("GetUser(%s): %v", req.ID, err)
            return Response{Code: 500, Message: "Internal error"}
        }
        ...
    }
