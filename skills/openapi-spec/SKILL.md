---
name: openapi-spec
description: "Generate or update an OpenAPI 3.2 contract into the working project and validate it against the canonical OAS meta-schema. Use to produce a spec from API code or requirements, or repair/validate a failing spec. Backs command/openapi."
---

# OpenAPI 3.2 Spec Generation

The contract lives in the repo as `docs/openapi.yaml` (or the project's existing spec path); it is read by humans, clients, and generators, and is the structural source of truth for the HTTP API. Code shows *what the server does today*; the spec declares *what callers may depend on*. A spec that does not validate against the published OpenAPI schema is no contract -- it is a guess.

> **Precondition.** A spec is only worth generating when the project exposes an HTTP API (introspect) or is about to (interview). Do not impose an OpenAPI file on a library, CLI, or batch job with no HTTP surface.

> **Domain adapter.** Backs the [openapi](../../commands/openapi.md) command; this skill holds the template, validator, and hard rules.

**Stance:** write for the caller who has never seen this server and the maintainer who must keep it honest. Every operation carries an `operationId`, a `summary`, the responses it can actually return, and at least one worked example. Never invent endpoints the code does not serve; never let the spec drift -- drift is a bug.

## Verified facts (pin, do not re-derive)

- **Latest stable: OpenAPI 3.2.0** (2025-09-19). Target `openapi: 3.2.0` at the document root.
- **Canonical meta-schema (immutable, date-stamped):** `https://spec.openapis.org/oas/3.2/schema/2025-11-23` (JSON Schema 2020-12). The date-stamped URL is frozen -- pin it for reproducible validation.
- **The root-key trap.** The OAS 3.2 meta-schema sets `unevaluatedProperties: false` at the root and permits only: `openapi`, `$self`, `info`, `jsonSchemaDialect`, `servers`, `paths`, `webhooks`, `components`, `security`, `tags`, `externalDocs`. It does **not** permit `$schema`, `$ref`, or `$id` there. The schema directive therefore lives in a **modeline comment** (outside the YAML data model) so it can never collide with the instance root:

```yaml
# yaml-language-server: $schema=https://spec.openapis.org/oas/3.2/schema/2025-11-23
```

Editors (Red Hat YAML language server) and the bundled [validator](references/validate-openapi.mjs) read the same line -- one source of truth. The validator fetches it, validates the body (which starts at `openapi: 3.2.0`), and strips a legacy root `$ref` for older specs.

## Modes

- **Detect (first):** introspect if the repo contains route/handler definitions (search framework signatures by capability, not tool name); interview if no HTTP surface exists. An existing spec -> Repair/Sync against that file, never a rewrite.
- **Introspect (ACT):** map the server's real surface -- paths/methods, parameters, request bodies, responses (success + real error codes), auth middleware -> `securitySchemes`, language types -> JSON Schema. Where code is silent, mark `[NEEDS CLARIFICATION]`, never invent.
- **Interview (ACT):** the smallest set -- resources + verbs, auth model, pagination/filtering, error envelope, id/date/money formats. Author into the [template](references/openapi-template.yaml); mark assumptions `[NEEDS CLARIFICATION]`.
- **Repair/Sync (PROVE/GROW):** bring a failing spec back to validating, code-consistent state; keep spec and code in lockstep.

## Hard rules (always enforced)

- `openapi: 3.2.0` is the first spec key; the `$schema` modeline precedes it as a comment.
- Every operation has a unique `operationId` (camelCase), a `summary`, and `responses` with at least success + the error codes it can return.
- Reuse, never duplicate -- shared shapes once in `components/schemas`, referenced with `$ref`.
- Examples required -- at least one per response/request body.
- 3.1+ typing -- `nullable` is gone; nullability is `type: [string, "null"]`. Use `format` (`date-time`, `uuid`, `email`, `uri`).
- Errors are real -- model the error envelope once; reference it from every error response.
- No speculative endpoints. If the code does not serve it, it is not in the spec.

## PROVE -- validate (the gate that judges done)

Structural validity is verified by executable evidence, not reading. Copy the validator next to the spec and run it:

```sh
node docs/openapi.validate.mjs docs/openapi.yaml   # 0 = valid; 1 = invalid; 2 = cannot run
```

It is self-contained; needs two dev deps -- `ajv` and `js-yaml` (`npm i -D ajv js-yaml`). If the project has a working OpenAPI validator with confirmed 3.2 support, prefer it; still enforce exit 0. Prefer the project's verify gate where one exists.

## Common mistakes

| Mistake | Fix |
|---|---|
| `$schema`/`$ref` root keys expecting strict validation | Directive is a modeline comment; legacy root keys are stripped. Body starts at `openapi:`. |
| Inventing endpoints | Introspect adds only routes the server registers; unknowns -> `[NEEDS CLARIFICATION]`. |
| Inlining a schema everywhere | Define once in `components/schemas`, `$ref` everywhere. |
| `nullable: true` (3.0-ism) | `type: [string, "null"]`. |
| Responses with only `200` | Add the real error codes; model the envelope once. |
| No examples | One worked example per body. |
| Done without a validating run | Run the validator; non-zero exit is not done. |

## References

- [openapi-template.yaml](references/openapi-template.yaml) -- the authoring template.
- [validate-openapi.mjs](references/validate-openapi.mjs) -- the bundled validator.
- [repo-documentation](../repo-documentation/SKILL.md) -- register the spec under the docs tree.
- [code-craft](../code-craft/SKILL.md) | [harness-engineering](../harness-engineering/SKILL.md)
