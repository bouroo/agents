// Reference validator for an OpenAPI 3.2 spec that carries the $schema + $ref
// directive at its root.
//
// What it does:
//   1. Loads the YAML document (default docs/openapi.yaml).
//   2. Reads the validation directive: $ref is the OpenAPI meta-schema URL,
//      $schema is the JSON-Schema dialect. These two keys are NOT OpenAPI
//      fields -- the OAS meta-schema sets `unevaluatedProperties: false` at the
//      document root and forbids $schema/$ref there -- so they are stripped
//      from the instance before validation.
//   3. Fetches the meta-schema named by $ref.
//   4. Dereferences its `$dynamicRef "#meta"` to a local `$ref` (see note below)
//      and compiles it with a JSON-Schema 2020-12 validator (Ajv).
//   5. Validates the directive-stripped body against it.
//
// Exit codes: 0 = valid, 1 = invalid spec, 2 = could not run (I/O, network,
// schema compilation). Requires: ajv@^8, js-yaml.

import { readFileSync } from 'node:fs';
import { load } from 'js-yaml';
import Ajv2020 from 'ajv/dist/2020.js';

const DIRECTIVE_KEYS = ['$schema', '$ref', '$id'];

function fail(message, code = 2) {
  console.error(`validate-openapi: ${message}`);
  process.exit(code);
}

function summarizeError(e) {
  const where = e.instancePath || '/';
  const prop = e.propertyName ? `/${e.propertyName}` : '';
  return `  ${where}${prop} ${e.message ?? ''}` +
    (e.params && Object.keys(e.params).length ? ` ${JSON.stringify(e.params)}` : '');
}

// The OAS meta-schema validates Schema Objects via `$dynamicRef "#meta"` ->
// `$dynamicAnchor "meta"` on `$defs/schema`. Ajv does not reliably resolve a
// same-document `$dynamicRef` to its anchor, and the OAI server serves the
// schema as application/octet-stream, which pure-JS validators that fetch it
// themselves reject. We fetch it (JSON), and because there is exactly ONE
// `meta` anchor, the dynamic reference is statically equivalent to a plain
// local reference -- so we dereference it. This does not change what is valid.
function dereferenceDynamicMeta(meta) {
  const text = JSON.stringify(meta);
  const rewritten = text.replace(
    /"\$dynamicRef"\s*:\s*"#meta"/g,
    '"$ref":"#/$defs/schema"',
  );
  return JSON.parse(rewritten);
}

const path = process.argv[2] ?? 'docs/openapi.yaml';

// 1. Load + parse.
let doc;
try {
  doc = load(readFileSync(path, 'utf8'));
} catch (e) {
  fail(`cannot read/parse ${path}: ${e.message}`, 2);
}
if (typeof doc !== 'object' || doc === null) {
  fail(`${path} did not parse to a mapping`, 2);
}

// 2. Read the directive.
const dialect = doc.$schema ?? 'https://json-schema.org/draft/2020-12/schema';
const metaSchemaUrl = doc.$ref;
if (!metaSchemaUrl) {
  fail(`${path} has no $ref directive at its root; expected the OpenAPI meta-schema URL`, 2);
}
if (!metaSchemaUrl.startsWith('https://spec.openapis.org/oas/')) {
  fail(`$ref does not point at an OpenAPI meta-schema: ${metaSchemaUrl}`, 2);
}

// 3. Fetch the meta-schema (served as octet-stream; parse as JSON explicitly).
let meta;
try {
  const res = await fetch(metaSchemaUrl, { headers: { accept: 'application/json' } });
  if (!res.ok) fail(`fetch ${metaSchemaUrl} -> HTTP ${res.status}`, 2);
  meta = await res.json();
} catch (e) {
  if (e.message?.startsWith('fetch')) throw e;
  fail(`network error fetching ${metaSchemaUrl}: ${e.message}`, 2);
}

// 4. Strip the directive from the instance root before validating.
const body = { ...doc };
for (const key of DIRECTIVE_KEYS) delete body[key];

// Collect every `format` keyword the meta-schema uses and register any Ajv does
// not yet know as pass-through, so unknown OAS-specific formats (e.g.
// `media-range`) don't spam warnings -- they are not our concern here.
function collectFormats(schema, found = new Set()) {
  if (Array.isArray(schema)) {
    schema.forEach((s) => collectFormats(s, found));
  } else if (schema && typeof schema === 'object') {
    if (typeof schema.format === 'string') found.add(schema.format);
    for (const v of Object.values(schema)) collectFormats(v, found);
  }
  return found;
}

// 5. Compile + validate.
const ajv = new Ajv2020({ strict: false, allErrors: true });
const metaForFormats = dereferenceDynamicMeta(meta);
for (const fmt of collectFormats(metaForFormats)) {
  try { ajv.addFormat(fmt, true); } catch { /* format already registered */ }
}

let validate;
try {
  validate = ajv.compile(metaForFormats);
} catch (e) {
  fail(`meta-schema ${metaSchemaUrl} failed to compile under ${dialect}: ${e.message}`, 2);
}

const ok = validate(body);
if (ok) {
  const openapi = body.openapi ?? '(missing)';
  console.log(`validate-openapi: ${path} is valid OpenAPI ${openapi} (schema ${metaSchemaUrl})`);
  process.exit(0);
}

console.error(`validate-openapi: ${path} FAILED validation against ${metaSchemaUrl}`);
for (const e of (validate.errors ?? [])) console.error(summarizeError(e));
process.exit(1);
