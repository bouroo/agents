---
description: OpenAPI phase  --  generate or update docs/openapi.yaml (OpenAPI 3.2) from API code or requirements, and validate it against the canonical OAS meta-schema
---

# OpenAPI Phase

Produce or repair the project's OpenAPI 3.2 contract at `docs/openapi.yaml` (or the repo's existing spec path) and prove it validates against the canonical OpenAPI meta-schema. The contract must reflect what the server actually serves -- a spec that drifts from the code, or one that does not validate, is a bug.

> **Agent:** requires file-edit + shell access (read routes/handlers, run the validator)  --  run on the implementing/build agent, not `plan` or `conductor`.

Target area (optional): **$ARGUMENTS**. Interpret as the resource, tag, or endpoint group to document (e.g. `orders`, `POST /webhooks`, `auth`). If empty, generate or sync the whole API surface.

---

## 0. Load the skill

Before anything else, load the **`openapi-spec` skill** via the skill tool. It carries the verified OpenAPI 3.2 facts (latest stable version, the canonical meta-schema URL, the root-key directive trap), the introspect-vs-interview modes, the hard rules, and ships the two copy-in artifacts -- `references/openapi-template.yaml` and `references/validate-openapi.mjs`. This command is the trigger; the skill is the reference.

---

## 1. Detect the mode

Decide introspect vs interview from the repo, not from the user.

- **Introspect mode**  --  the repo contains an HTTP API. Search for framework signatures (capability-based): Express/Fastify/Koa route registrations; Flask `@app.route`; Django `urlpatterns`; Spring `@RestController`/`@RequestMapping`; ASP.NET `[ApiController]`; Go `net/http`/gin/echo/chi; Rails `config/routes.rb`; FastAPI decorators.
- **Interview mode**  --  no HTTP surface found (greenfield, or the API lives elsewhere). Author from a minimal interview.
- **Repair/Sync mode**  --  `docs/openapi.yaml` already exists. Do not rewrite it; update the affected operations and re-validate.

If a spec already exists, run the validator first (step 5) to establish a baseline before editing.

---

## 2. Introspect OR interview

**Introspect**  --  extract, do not invent:

- Paths and methods  --  one operation per `(path, method)` the server registers.
- Parameters (path/query/header/cookie), request bodies, and the status codes each handler actually returns.
- Auth  --  map middleware/decorators to `securitySchemes` + per-operation `security`.
- Map language types to JSON Schema (`Instant` -> `string`/`date-time`; `UUID` -> `string`/`uuid`; `int64` -> `integer`/`int64`). Reuse via `components/schemas`.

**Interview**  --  ask the smallest set: resources + verbs, auth model, pagination/filtering, the shared error envelope, and id/date/money formats. Author directly into the template; mark every assumption `[NEEDS CLARIFICATION]`.

---

## 3. Draft from the template

Start from the skill's [openapi-template.yaml](../skills/openapi-spec/references/openapi-template.yaml). Keep the two-line directive header (`$schema` + `$ref`) exactly at the top  --  it is what points the validator at the OpenAPI 3.2 meta-schema and is **not** spec content. The body begins at `openapi: 3.2.0`.

Replace the example resource (`examples`) with the real one. Honor the hard rules from the skill: every operation has a unique `operationId`, a `summary`, responses for at least its success and error codes, and at least one worked example; reuse schemas via `$ref`; model the error envelope once.

---

## 4. Fill gaps

Where the code is silent, do not invent behavior. Add `[NEEDS CLARIFICATION]` for unknown descriptions, unclear status codes, or ambiguous auth, and continue. A flagged gap is better than a plausible lie. Prefer concrete `example` values over empty placeholders; placeholders with characters outside `^[a-zA-Z0-9._-]+$` are invalid component keys.

---

## 5. Validate (the gate that judges done)

Copy the skill's [validate-openapi.mjs](../skills/openapi-spec/references/validate-openapi.mjs) next to the spec as `docs/openapi.validate.mjs`, ensure its two dev deps are present (`npm i -D ajv js-yaml` if missing), and run it:

```sh
node docs/openapi.validate.mjs docs/openapi.yaml   # exit 0 required
```

The validator reads the `$ref` directive, fetches the OpenAPI 3.2 meta-schema, strips the directive keys from the instance root, and validates the body. Enforce **exit 0**. If the project already has a working OpenAPI validator with confirmed 3.2 support, prefer it  --  but still enforce zero. Fix and re-run until clean (max three cycles, then escalate per the harness hard-verify bound).

---

## 6. Sync

Keep the spec and its surroundings consistent.

- If `docs/` follows the [repo-documentation](../skills/repo-documentation/SKILL.md) tree, register the spec under each affected system doc's *Interfaces and entry points*; note it in `docs/README.md` if it is a primary interface.
- If the project has a render/lint gate for the spec (Redocly, Spectral, swagger-ui), run it too; confirm its 3.2 support before relying on it.
- Leave behind only intended files: the spec, the validator shim, and a package.json dependency line if you added one.

---

## Reporting

State the mode chosen and why, the operations added or updated, the spec path, the validator command invoked and its exit code, any `[NEEDS CLARIFICATION]` gaps left, and a one-line verdict  --  **SPEC VALIDATED** or **BLOCKED** (with the failing checks).

Before reporting, run the artifact-gate sweep: behavior added and no `INTENT:` line, add it; an outward-facing contract change and no `AUTH:` line, add it.
