---
name: openapi-spec
description: "Generate or update an OpenAPI 3.2 contract into the working project and validate it against the canonical OAS meta-schema. Use when you must produce an OpenAPI spec from existing API code or from requirements, or repair/validate a spec that fails."
---

# OpenAPI 3.2 Spec Generation

The contract lives in the repo as `docs/openapi.yaml` (or the project's existing spec path); it is read by humans, clients, and generators, and it is the structural source of truth for the HTTP API. Code shows *what the server does today*; the spec declares *what callers may depend on*. A spec that does not validate against the published OpenAPI schema is no contract -- it is a guess.

> **Precondition.** A spec is only worth generating when the project exposes an HTTP API (introspect mode) or is about to (interview mode). Do not impose an OpenAPI file on a library, CLI, or batch job that has no HTTP surface.

**Stance:** You write the spec for the caller who has never seen this server and the maintainer who must keep it honest six months on. Every operation carries an `operationId`, a `summary`, the responses it can actually return, and at least one worked example. You never invent endpoints the code does not serve, and you never let the spec drift from the code -- a drift is a bug.

**Modes:**

- **Generate mode (THINK & ACT)** -- produce `docs/openapi.yaml` from scratch, choosing introspect vs interview by what the repo contains.
- **Repair mode (PROVE)** -- bring an existing, failing spec back to a validating, code-consistent state.
- **Sync mode (GROW)** -- update the spec to match a code change (new/changed/removed operations) and re-validate.

---

## Integration with the THINK→ACT→PROVE→GROW Loop

- **THINK** -- detect the API surface (or its absence) and decide the mode. This is *discovery*, not authoring.
- **ACT** -- author or update the spec surgically from evidence (code or interview). One bounded change at a time.
- **PROVE** -- validate the spec against the canonical OpenAPI meta-schema with executable evidence (the bundled validator). The harness, not your reading, judges validity.
- **GROW** -- if the same drift recurs (e.g. a new endpoint shipped without a spec entry), add a guard: run the validator in the project's verify gate so the drift cannot recur.

The trigger is the `openapi-phase` command; this skill is the reference.

---

## Verified facts (pin these, do not re-derive)

External facts below were resolved against primary sources, not memory. Re-verify if the date is more than a few months stale.

- **Latest stable: OpenAPI 3.2.0**, released 2025-09-19 (OpenAPI Initiative). Target `openapi: 3.2.0` at the document root.
- **Canonical meta-schema (immutable, date-stamped):** `https://spec.openapis.org/oas/3.2/schema/2025-11-23`. It is a JSON Schema **2020-12** document; its `$id` is the URL itself, its `$schema` is `https://json-schema.org/draft/2020-12/schema`, and it targets "OpenAPI v3.2.x Documents". The date-stamped URL is frozen -- pin it for reproducible validation. (Prior series: `…/oas/3.1/schema/2022-10-07`.)
- **The root-key trap.** The OAS 3.2 meta-schema sets `unevaluatedProperties: false` at the document root and permits **only**: `openapi`, `$self`, `info`, `jsonSchemaDialect`, `servers`, `paths`, `webhooks`, `components`, `security`, `tags`, `externalDocs`. It does **not** permit `$schema`, `$ref`, or `$id` there. Therefore the two-line header below is a **validation directive, not spec content**: a strict validator strips `$schema`/`$ref` before applying the meta-schema, or the document fails with an `unevaluatedProperties` violation.

### The validator directive (the requested header)

The document carries these two keys at the very top so any JSON-Schema-aware tool can find and apply the OAS schema:

```yaml
$schema: 'https://json-schema.org/draft/2020-12/schema'
$ref: 'https://spec.openapis.org/oas/3.2/schema/2025-11-23'
```

These keys are **metadata for the validator**. The bundled validator ([validate-openapi.mjs](./references/validate-openapi.mjs)) reads `$ref`, fetches the schema, drops `$schema`/`$ref`/`$id` from the instance root, and validates the remainder. The spec *body* starts with `openapi: 3.2.0`.

> **Trade-off, stated honestly.** Dedicated OpenAPI linters (Redocly, Spectral) give richer *semantic* rules (naming, examples, deprecations) but their 3.2 support is younger than 3.1 -- 3.2 is under a year old. Where a linter's 3.2 support is unconfirmed, the meta-schema validator is the portable source of truth for *structural* validity. Use a linter for semantics once you have confirmed its 3.2 support; never let it be the reason you skip structural validation.

---

## Mode 1 -- Detect (runs first)

Decide introspect vs interview from the repo, not from the user.

- **Introspect mode** -- the repo contains an HTTP API. Search for framework signatures (capability-based, not tool-name-bound): Express/Fastify/Koa route registrations; Flask `@app.route`/`@app.get`; Django `urlpatterns`; Spring `@RestController`/`@RequestMapping`; ASP.NET `[ApiController]`/`[Route]`; Go `net/http`, gin, echo, chi handlers; Rails `config/routes.rb`; FastAPI decorators. If route/handler definitions exist, introspect.
- **Interview mode** -- no HTTP surface found (greenfield, or the API lives in another repo). Author from requirements via a minimal interview (see below).

When you find a spec that already exists, do not rewrite it -- switch to Repair/Sync mode against the existing file.

---

## Mode 2a -- Introspect

Map the server's real surface to the spec. Extract from code, then fill only where the code is silent.

1. **Paths & methods** -- one operation per `(path, method)` the server registers. Never invent a route the code does not serve.
2. **Parameters** -- path (`{id}`), query, header, cookie. Capture name, `in`, `required`, schema, and format.
3. **Request bodies** -- media type + schema; reuse a component schema. Add at least one `example`.
4. **Responses** -- the status codes the handler actually returns (success + the error codes it can produce). Each with a description; success bodies carry schema + example.
5. **Auth** -- map middleware/decorators (`@login_required`, JWT verify, API-key checks) to `securitySchemes` + per-operation `security`.
6. **Types → JSON Schema** -- map language types to JSON Schema (e.g. Go `int64`→`integer`/`int64`; Java `Instant`→`string`/`date-time`; Python `UUID`→`string`/`uuid`). Reuse via `components/schemas`.

Where the code is silent (no examples, no error contract, unclear descriptions), do not invent behavior -- add `[NEEDS CLARIFICATION]` and continue. A gap flagged is better than a plausible lie.

---

## Mode 2b -- Interview

Ask the smallest set that produces a contract, then author. Do not over-interview.

- **Resources** and the operations on each (which CRUD-ish verbs, which custom actions).
- **Auth model** (none / bearer JWT / API key / OAuth2) and where the credential lives.
- **Pagination + filtering** conventions (offset/limit vs cursor; filter param names).
- **Error envelope** -- the shared error shape and which status codes apply.
- **Representation** -- id format, date-time format, money/decimal handling.

Author directly into the template; mark every assumption `[NEEDS CLARIFICATION]` until confirmed.

---

## Hard rules (always enforced)

- **`openapi: 3.2.0`** is the first spec key; the `$schema`/`$ref` directive precedes it.
- **Every operation** has a unique `operationId` (camelCase), a `summary`, and a `responses` map containing at least its success code and the error codes it can return.
- **Reuse, never duplicate** -- shared shapes live once in `components/schemas` and are referenced with `$ref: '#/components/schemas/Name'`.
- **Examples are required** -- at least one `example` (or `examples`) on each response body and request body. A spec without examples is not usable by clients or mocks.
- **3.1+ typing** -- `nullable` is gone; express nullability as `type: [string, "null"]`. Use JSON Schema `format` (`date-time`, `uuid`, `email`, `uri`) for machine-checkable shapes.
- **Errors are real** -- model the error envelope once in `components/schemas` and reference it from every error response.
- **No speculative endpoints.** If the code does not serve it, it is not in the spec.

---

## PROVE -- validate (the gate that judges done)

Structural validity is verified by executable evidence, not by reading. Run the bundled validator from the working project:

```sh
node docs/openapi.validate.mjs docs/openapi.yaml   # exit 0 = valid; 1 = invalid (errors to stderr); 2 = cannot run
```

Copy the validator into the project next to the spec (it is self-contained; `node docs/openapi.validate.mjs docs/openapi.yaml`). It needs two dev dependencies -- `ajv` and `js-yaml` (`npm i -D ajv js-yaml`). If the project already has a working OpenAPI validator with confirmed 3.2 support, prefer it -- but still enforce a zero exit code.

Prefer the project's own verify gate where one exists. If none, the bundled validator is the gate. A spec that does not exit 0 is not done.

---

## Output location

Default: `docs/openapi.yaml` (and `docs/openapi.validate.mjs`). If the project already keeps its spec elsewhere (`openapi.yaml`, `api/openapi.yaml`, `openapi/openapi.yaml`), write there and do not duplicate. Keep the validator shim next to the spec.

---

## Sync (GROW)

When code changes, update the spec to match and re-validate: new operations get entries; changed params/bodies update their schemas; removed operations are deleted from the spec in the same change. If `docs/` follows the [repo-documentation](../repo-documentation/SKILL.md) tree, register the spec under each system doc's *Interfaces and entry points* and note the contract in `docs/README.md` if it is primary.

---

## Common mistakes

| Mistake | Fix |
|---|---|
| Putting `$schema`/`$ref` in the body and expecting strict validation to pass | They are a validator directive; the validator strips them before applying the meta-schema. The body starts at `openapi:`. |
| Inventing endpoints not present in the code | Introspect mode adds only routes the server registers; mark unknowns `[NEEDS CLARIFICATION]`, never invented. |
| Inlining the same schema in every response | Define once in `components/schemas`, `$ref` everywhere. |
| `nullable: true` (3.0-ism) | 3.1+/3.2 dropped `nullable`; use `type: [string, "null"]`. |
| Responses with only `200` | Add the error codes the handler actually returns; model the error envelope once and reference it. |
| No examples | Add at least one worked example per body; clients and contract tests depend on it. |
| Declaring done without a validating run | Run the validator; a non-zero exit is not done. |

---

## Cross-References

- [repo-documentation](../repo-documentation/SKILL.md) -- the `docs/` tree this spec lives in; register under *Interfaces and entry points*.
- [effective-code-craft](../effective-code-craft/SKILL.md) -- clarity, reuse, and the INTENT/TWINS artifact gates.
- [harness-engineering](../harness-engineering/SKILL.md) -- executable-evidence gate; wire the validator into the project's verify gate to prevent drift (GROW).

---

## References

- OpenAPI Specification 3.2 -- https://spec.openapis.org/oas/v3.2.0
- OAS 3.2 meta-schema (the validation target) -- https://spec.openapis.org/oas/3.2/schema/2025-11-23
- JSON Schema 2020-12 -- https://json-schema.org/draft/2020-12/schema
- OpenAPI Initiative releases (3.2.0, 2025-09-19) -- https://github.com/OAI/OpenAPI-Specification/releases
