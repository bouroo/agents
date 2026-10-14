# Problem Details Blueprints

Copy-pasteable scaffolds for [RFC 9457](../SKILL.md) adoption. Each is deliberately minimal: no framework beyond the one named, no abstraction layer, no error-class hierarchy. Extend only where the project already needs the extension.

## JSON Schema (draft 2020-12)

A strict profile: all five standard members required, so a contract test catches a handler that drops one. RFC 9457 itself defaults `type` to `about:blank` and lets `title`, `status`, `detail`, and `instance` be absent; relax `required` if the project wants that latitude. `additionalProperties: true` is the spec's own extension mechanism — never set it false, or a legitimate extension member becomes a validation failure.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/schemas/problem-details.json",
  "title": "Problem Details",
  "type": "object",
  "required": ["type", "title", "status", "detail", "instance"],
  "additionalProperties": true,
  "properties": {
    "type": { "type": "string", "format": "uri-reference" },
    "title": { "type": "string" },
    "status": { "type": "integer", "minimum": 100, "maximum": 599 },
    "detail": { "type": "string" },
    "instance": { "type": "string", "format": "uri-reference" }
  }
}
```

## Node.js / Express

One error-handling middleware, registered last. The four-argument signature is what marks it as error-handling middleware to Express; a three-argument function is silently treated as a normal handler.

```js
// src/problem.js
const PROBLEMS = {
  NOT_FOUND: { type: "https://example.com/problems/not-found", title: "Resource not found", status: 404 },
  VALIDATION: { type: "https://example.com/problems/validation", title: "Request validation failed", status: 422 },
};

class ProblemError extends Error {
  constructor(key, detail, extensions = {}) {
    super(detail);
    this.problem = { ...PROBLEMS[key], detail, ...extensions };
  }
}

// Registered after all routes; the arity-4 signature selects it as an error handler.
function problemDetails(err, req, res, _next) {
  const { type, title, status, detail, ...rest } = err.problem ?? {
    type: "about:blank",
    title: "Internal Server Error",
    status: 500,
    detail: "An unexpected error occurred.",
  };
  res
    .status(status)
    .type("application/problem+json")
    .send({ type, title, status, detail, instance: req.originalUrl, ...rest });
}

module.exports = { ProblemError, problemDetails };
```

```js
// wiring
const express = require("express");
const { ProblemError, problemDetails } = require("./problem");
const app = express();

app.get("/users/:id", (req, res) => {
  throw new ProblemError("NOT_FOUND", `No user with id ${req.params.id}.`);
});

app.use(problemDetails);
```

## Python / FastAPI

Override the framework's default handlers so every `HTTPException` and every validation failure emits the problem document. `instance` takes the request path; a trace id belongs in an extension member when one exists.

```python
# app/problem.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

MEDIA_TYPE = "application/problem+json"

def problem(
    request: Request,
    status: int,
    type_: str,
    title: str,
    detail: str,
    **extensions,
) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        media_type=MEDIA_TYPE,
        content={
            "type": type_,
            "title": title,
            "status": status,
            "detail": detail,
            "instance": request.url.path,
            **extensions,
        },
    )

def install(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def http_exception(request: Request, exc: HTTPException):
        return problem(request, exc.status_code, "about:blank", "Request failed", str(exc.detail))

    @app.exception_handler(RequestValidationError)
    async def validation(request: Request, exc: RequestValidationError):
        return problem(
            request,
            422,
            "https://example.com/problems/validation",
            "Request validation failed",
            "One or more fields are invalid.",
            errors=exc.errors(),
        )
```

## Spring Boot

Framework 6+ ships `org.springframework.http.ProblemDetail` natively, so no custom class is needed. `ResponseEntity.of(problemDetail)` copies the `status` into the HTTP status line. One `@RestControllerAdvice` centralizes every mapping.

```java
package com.example.api;

import java.net.URI;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class ProblemDetailsAdvice {

    @ExceptionHandler(ResourceNotFoundException.class)
    ResponseEntity<ProblemDetail> notFound(ResourceNotFoundException ex) {
        ProblemDetail problem = ProblemDetail.forStatus(HttpStatus.NOT_FOUND);
        problem.setType(URI.create("https://example.com/problems/not-found"));
        problem.setTitle("Resource not found");
        problem.setDetail(ex.getMessage());
        problem.setProperty("code", "NOT_FOUND");
        return ResponseEntity.of(problem).build();
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    ResponseEntity<ProblemDetail> invalid(MethodArgumentNotValidException ex) {
        ProblemDetail problem = ProblemDetail.forStatus(HttpStatus.UNPROCESSABLE_ENTITY);
        problem.setType(URI.create("https://example.com/problems/validation"));
        problem.setTitle("Request validation failed");
        problem.setDetail("One or more fields are invalid.");
        return ResponseEntity.of(problem).build();
    }
}
```

`ResponseEntity.of(problem)` sets the HTTP status from the `ProblemDetail` and renders it as `application/problem+json`. Set `instance` from the request when a trace id or path is wanted; `ProblemDetail.setInstance(URI)`.

## JSend edge adapter (user-facing JSend, internal 9457)

A hybrid topology for one situation: clients already speak **JSend** and that user-facing contract must not be broken, while the server wants one rich internal error record. The split is by audience, not by transport — the RFC 9457 problem document is the **only internal error model**, and JSend is a **projection of it at the edge**. Adopt it only where JSend consumers exist; absent them the projection is an unearned layer, because plain 9457 already serves both audiences from one document.

Two rules carry the topology:

- **9457 is the internal model; the JSend body is generated, never hand-built.** Handlers raise the same `ProblemError`; one edge serializer maps the document to a JSend envelope. A handler that assembles `{"status": "fail", ...}` itself has re-forked the error path this skill exists to collapse.
- **No hand-authored `instance` or trace id in the user-facing body.** Those belong to the internal record. JSend is an application-level envelope, so the HTTP status line and headers still carry the protocol semantics — send them, as the JSend spec itself advises, rather than smuggling transport facts into `data`.

The statuses map cleanly: 5xx is `error` (`message`, numeric `code`), 4xx is `fail` (`data`, whose keys SHOULD mirror the submitted fields), and `success` has no 9457 counterpart — a 2xx is a bare resource, out of scope here. On the `error` path `message` takes the per-class `title`, never the internal `detail` — a 5xx `detail` names hosts, queries, and diagnostics, and none of it crosses the edge; the 4xx `detail` is request-scoped and safe to project into `data` when no `errors` member exists.

```js
// Edge serializer: extends the Express middleware above; `problem` is its document.
function toJSend(problem) {
  const { status, title, detail, errors } = problem;
  return status >= 500
    ? { status: "error", message: title, code: status }
    : { status: "fail", data: errors ?? { detail } };
}

function jsendEdge(err, req, res, _next) {
  const problem = err.problem ?? { status: 500, title: "Internal Server Error", detail: "An unexpected error occurred." };
  res.status(problem.status).type("application/json").send(toJSend(problem));
}
```

Register `jsendEdge` in place of `problemDetails` on a JSend surface; keep `problemDetails` for internal and machine clients.

## Contract test

Any stack; this one validates the FastAPI response against the schema above. It fails the build when a handler returns the wrong media type or drops a standard member — the enforcement step the retrofit path depends on.

```python
# tests/test_problem_contract.py
import json
import pathlib

import jsonschema
import pytest
from fastapi.testclient import TestClient

from app.main import app

SCHEMA = json.loads(pathlib.Path("schemas/problem-details.json").read_text())


@pytest.fixture
def client():
    return TestClient(app, raise_server_exceptions=False)


def test_error_response_is_a_problem_document(client):
    response = client.get("/this-route-does-not-exist")

    assert response.headers["content-type"].startswith("application/problem+json")
    jsonschema.validate(instance=response.json(), schema=SCHEMA)
```

`raise_server_exceptions=False` is what lets a 500 path be asserted rather than re-raised. To prove the test bites, delete one member from a handler and confirm it fails; a green suite that never saw a red run proves nothing.
