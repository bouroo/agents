---
name: problem-details
description: "Design and enforce RFC 9457 error responses for an HTTP API (superseding RFC 7807): the application/problem+json document, the type/title/status/detail/instance contract, extension members, and two adoption paths — one greenfield error handler, or retrofitting a standard onto an existing surface with a contract test that fails ad-hoc bodies. Use when an API's errors are inconsistent, when clients break on message changes, when designing a new REST service's failure shape, or when a standard must be enforced on demand — even if the ask is only 'our error responses are a mess'. Not for GraphQL or RPC error modelling, and not for deciding what the errors should say."
---

# Problem Details

**Stance:** an HTTP error is a **contract**, not a message. RFC 9457 gives every failure one machine-readable shape — a `type` a client branches on, a `title` it renders, a `detail` naming this occurrence — so an API grows one error-handling code path instead of one per endpoint. The failure mode is the ad-hoc body: `{"error": "..."}` on one handler, a bare string on the next, a different key on a third.

**When to load:** designing or reviewing an HTTP API's error responses; retrofitting an API that has no consistent error pattern; enforcing a standard across an existing surface. For the gates and evidence discipline this skill applies, load the `quality` skill's Craft section.

## 1. Overview & Objectives

RFC 9457 supersedes RFC 7807 with the same media type and the same member semantics. It buys three things:

- **A machine-readable discriminator** — `type` is a stable URI naming the problem class, so a client switches on it rather than on prose or an HTTP status alone.
- **A stable contract** — one document shape means a client's error handling is written once and survives new endpoints.
- **One error path** — a server emits the same document from a single handler or middleware.

9457 is a clarification, not a redesign: it pins `about:blank` as the default `type`, states how the `type`/`title` pair behaves across occurrences, and drops 7807's vestigial use of `type` as prose. Implement to 9457; a 7807 body is a valid subset.

## 2. Standard Response Structure

Emitted with `Content-Type: application/problem+json`. Five standard members:

| Member | Type | Semantics |
| --- | --- | --- |
| `type` | string, URI reference | Identifies the **problem class**, not this occurrence. SHOULD dereference to human-readable docs for non-standard types; defaults to `about:blank`. Stable across occurrences of the class. |
| `title` | string | Short human-readable summary of the problem class. SHOULD be **identical for every occurrence of a type** — never interpolate request data into it. |
| `status` | number | The HTTP status code. SHOULD match the response status; MAY be omitted when redundant with the HTTP line. |
| `detail` | string | Human-readable explanation **specific to this occurrence**. All per-request variability lives here — never in `title`. |
| `instance` | string, URI reference | Identifies **this occurrence** — typically the request path, or a request/trace id. |

The `type`/`title` pair is the class; `detail` and `instance` are the occurrence. A `title` that varies per request is the most common 9457 mistake: it breaks the one-title-per-type contract clients cache and localize.

Canonical body:

```json
{
  "type": "https://example.com/problems/out-of-credit",
  "title": "Out of credit",
  "status": 403,
  "detail": "Your current balance is 30, but that costs 50.",
  "instance": "/account/12345/msgs/abc"
}
```

**Extension members** — any member beyond the five is allowed, and a generic client ignores it. Use them for a machine-readable error catalogue (`code`), field-level validation detail (`errors`, an array), or a server timestamp. Names should **avoid collisions**: namespace them, or keep them domain-specific. A member that shadows a standard one — or a plausible future one — is a defect; a nested `status` inside `errors[]` is fine because it is scoped.

## 3. Adoption workflow

### Greenfield / no existing pattern

1. Emit `application/problem+json` from **one** error handler or middleware — never per route.
2. Map each exception or error class to a `(type, title, status)` triple; the type URI is the catalogue key.
3. Fill `detail` and `instance` per request from the caught error.
4. **DONE check:** issue one failing request; assert the response media type is `application/problem+json`, all five members are present, and `status` equals the HTTP status. A contract test that does exactly this ships in [`references/blueprints.md`](references/blueprints.md).

### Retrofit / enforce on demand

1. **Inventory** the current error shapes — every distinct body a failing route returns.
2. **Define the type URI scheme** (a base plus one slug per problem class) before adding members.
3. **Migrate**: wrap a legacy payload as an `errors` extension member beneath the standard five, or dual-write standard and legacy during a deprecation window.
4. **Enforce with a contract test** that fails any error response not validating against the schema in [`references/blueprints.md`](references/blueprints.md). Without it the convention decays back to ad-hoc bodies.

A third shape is supported where clients already speak JSend: 9457 stays the internal record of investigation and a JSend envelope is projected from it at the edge, generated by one serializer and never hand-built per handler. The two non-negotiables, the status mapping, and an Express `toJSend` scaffold live in [`references/blueprints.md`](references/blueprints.md).

## 4. Blueprints

Framework-specific, copy-pasteable implementations (Node.js/Express, Python/FastAPI, Spring Boot), a draft 2020-12 JSON Schema for the document, and a schema-validating contract test live in [`references/blueprints.md`](references/blueprints.md).
