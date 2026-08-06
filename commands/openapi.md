---
description: "OpenAPI phase (ACT) -- generate or update docs/openapi.yaml (OpenAPI 3.2) from API code or requirements and validate it against the canonical OAS meta-schema. Use to produce, repair, or sync an API contract."
agent: coder
phase: ACT
---

# OpenAPI -- Contract Generation & Validation

Produce or repair the project's OpenAPI 3.2 contract at `docs/openapi.yaml` (or the repo's existing spec path) and prove it validates against the canonical meta-schema. The contract must reflect what the server serves -- a spec that drifts from the code, or does not validate, is a bug.

> **Agent:** requires file-edit + shell access (read routes/handlers, run the validator) -- run on the mutating worker ([coder](../agents/coder.md)), not the conductor.

**Target area** (optional): **$ARGUMENTS** -- a resource, tag, or endpoint group (`orders`, `POST /webhooks`, `auth`). If empty, generate or sync the whole API surface.

## Steps

1. **Load the adapter skill** -- [openapi-spec](../skills/openapi-spec/SKILL.md) holds the template, the validator, and the hard rules. Depth lives there; this command is the workflow.
2. **Choose the mode:**
   - **Introspect** -- read the API code (routes, handlers, DTOs, middleware) to derive the contract from what is actually served. Preferred when code is authoritative.
   - **Interview** -- run the skill's minimal interview (resources + verbs, auth, pagination/filtering, error envelope, id/date/money formats); author into the template and mark every assumption `[NEEDS CLARIFICATION]`. Preferred for design-first.
3. **Author or update** the spec from the template. Replace the example resource with the real one. Hard rules: every operation has a unique `operationId`, a `summary`, responses for at least success + error codes, and at least one worked example; reuse schemas via `$ref`; model the error envelope once.
4. **Validate** against the canonical OAS meta-schema using the skill's validator; capture command + exit code + output. Iterate until **SPEC VALIDATED**.
5. **Sync** -- if `docs/` follows the [repo-documentation](../skills/repo-documentation/SKILL.md) tree, register the spec under each affected system doc's *Interfaces and entry points*; note it in `docs/README.md` if primary. If a render/lint gate exists (Redocly, Spectral), run it; confirm its 3.2 support first.
6. **Clean up** -- leave behind only intended files: the spec, the validator shim, and a dependency line if you added one.

## Success metrics

- `docs/openapi.yaml` validates against the OAS meta-schema (validator exit 0, output captured).
- Every operation has `operationId`, `summary`, success + error responses.
- Spec reflects the served API (introspect mode) or marks assumptions `[NEEDS CLARIFICATION]` (interview mode).

## Failure metrics

- Validator exit != 0 after iteration -> **BLOCKED** with the failing checks.
- Spec drifts from served code (introspect mode) -> bug, not done.

## Reporting

State the mode chosen and why, operations added/updated, spec path, validator command + exit code, any `[NEEDS CLARIFICATION]` gaps, and a verdict -- **SPEC VALIDATED** or **BLOCKED**. Before reporting, run the artifact-gate sweep: behavior added -> `INTENT:`; outward contract change -> `AUTH:` ([code-craft](../skills/code-craft/SKILL.md)).

## References

- [openapi-spec](../skills/openapi-spec/SKILL.md) -- template, validator, hard rules.
- [repo-documentation](../skills/repo-documentation/SKILL.md) -- register the spec under the docs tree.
- [code-craft](../skills/code-craft/SKILL.md) -- artifact gates.
