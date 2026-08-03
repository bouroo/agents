// Reference validator for an OpenAPI 3.2 spec whose meta-schema is declared via
// a yaml-language-server modeline at the top of the file -- the same directive
// the Red Hat YAML language server reads in editors:
//
//   # yaml-language-server: $schema=https://spec.openapis.org/oas/3.2/schema/<date>
//
// In the modeline, `$schema` is the OpenAPI META-schema URL -- the schema the
// file is validated against, which is what an editor uses. It is NOT the
// JSON-Schema dialect; the dialect is read from the fetched meta-schema's own
// `$schema`.
//
// What it does:
//   1. Loads the YAML document (default docs/openapi.yaml), keeping the raw
//      text so modeline comments can be parsed.
//   2. Reads the validation directive: the modeline `$schema` URL is the
//      OpenAPI meta-schema. Falls back to a root `$ref` key for specs that
//      predate the modeline.
//   3. Fetches the meta-schema named by the directive.
//   4. Dereferences its `$dynamicRef "#meta"` to a local `$ref` (see note below)
//      and compiles it with a JSON-Schema 2020-12 validator (Ajv).
//   5. Validates the body against it. Legacy root `$schema`/`$ref`/`$id` keys
//      (absent in the modeline form) are stripped first, because the OAS
//      meta-schema forbids them at the document root.
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

// Parse the yaml-language-server modeline from the leading comment block to find
// the validation schema URL. The modeline -- read by editors (Red Hat YAML
// language server, VS Code, IntelliJ) and this validator alike -- is the single
// source of truth, so a spec is configured once for both. Two top-of-file
// comment forms are supported:
//   # yaml-language-server: $schema=<url>     (standard)
//   # $schema: <url>                          (IntelliJ-compatible)
// Here `$schema` is the schema to validate against (the OpenAPI meta-schema),
// not the JSON-Schema dialect. Returns the URL, or null when no modeline is
// present (callers fall back to the legacy root `$ref` key). Scanning stops at
// the first non-comment line so a `$schema:` comment inside the body is never
// mistaken for a modeline. `$schema: none` disables the schema and returns null.
function parseModeline(rawText) {
  for (const line of rawText.split(/\r?\n/)) {
    const trimmed = line.trimStart();
    if (trimmed === '') continue;          // blank line within the header
    if (!trimmed.startsWith('#')) break;   // first data line ends the header
    let url = null;
    const yls = trimmed.match(/^#\s*yaml-language-server:\s*(.*)$/i);
    if (yls) {
      for (const tok of yls[1].split(/\s+/)) {
        const m = tok.match(/^\$schema=(.+)$/);
        if (m) { url = m[1]; break; }
      }
    } else {
      const ij = trimmed.match(/^#\s*\$schema:\s*(.+)$/);
      if (ij) url = ij[1];
    }
    // `$schema: none` disables schema association in editors; treat it as
    // absent so the legacy root-$ref fallback (or a clear error) takes over.
    if (url && url.trim().toLowerCase() !== 'none') return url.trim();
  }
  return null;
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

// 1. Load + parse. Keep the raw text so the modeline (a comment) can be read.
let raw;
let doc;
try {
  raw = readFileSync(path, 'utf8');
  doc = load(raw);
} catch (e) {
  fail(`cannot read/parse ${path}: ${e.message}`, 2);
}
if (typeof doc !== 'object' || doc === null) {
  fail(`${path} did not parse to a mapping`, 2);
}

// 2. Read the directive. The modeline (read by editors too) is preferred; a
//    root `$ref` key is the legacy fallback. `$schema` in the modeline is the
//    schema to validate against -- here the OpenAPI meta-schema.
const metaSchemaUrl = parseModeline(raw) ?? doc.$ref;
if (!metaSchemaUrl) {
  fail(`${path} has no schema directive: expected a '# yaml-language-server: $schema=<url>' modeline at the top, or a root '$ref' key`, 2);
}
if (!metaSchemaUrl.startsWith('https://spec.openapis.org/oas/')) {
  fail(`schema directive does not point at an OpenAPI meta-schema: ${metaSchemaUrl}`, 2);
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

// The dialect is the fetched meta-schema's own `$schema`; legacy root-key specs
// may carry it as `doc.$schema`. Used only as a label in the compile-error path.
const dialect = meta.$schema ?? doc.$schema ?? 'https://json-schema.org/draft/2020-12/schema';

// 4. Strip legacy directive keys from the instance root before validating. The
//    modeline form carries the directive in a comment, so there is nothing to
//    strip -- this is a no-op for modeline specs and only matters for the
//    legacy root-key fallback.
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
