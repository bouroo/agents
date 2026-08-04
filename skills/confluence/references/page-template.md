# adapter-mbf-ais endpoint page template (extracted from EoGMagE)

The exact structure of the hand-built example page
`adapter-mbf-ais - POST /api/v1/cart/get` (`/wiki/x/EoGMagE`, page `6082560274`).
Use this when authoring a new endpoint/spec page so it matches the example
byte-for-byte in structure. The companion generator `../page_template.py` emits
this layout from structured data. Authoring mechanics (macros, compression,
storage format) live in [storage-format.md](./storage-format.md) +
[plantuml.md](./plantuml.md).

## Document order (verbatim from the example)

1. **Metadata table** -- a 3-column table (`data-table-width`, `data-layout="default"`)
   whose label cells are `colspan="2"` + highlighted `#f4f5f7`, content in the 3rd cell.
2. `## Change logs` → 4-col table (`Date | Update By | Description | Status`).
3. `## Table of Contents` (heading; an `ac:name="toc"` macro is optional).
4. `## Sequence diagram` → `plantumlcloud` macro (rendered) → a `code` macro
   (`language=none`, `breakoutMode=wide`, `breakoutWidth=4000`, `wrap=true`)
   holding the raw `@startuml…@enduml` source so it stays readable.
5. `## Logic` → ordered list of numbered steps.
6. `## Request`
   - `### Request Body` → field table (5 cols, see below).
   - `### Sample request` → `code` macro. **The example shows the request as a JSON body (`language=json`), not a curl command.**
7. `## Response`
   - `### Response Body` → field table (same 5 cols).
   - `### Sample response` → a single-cell header table `HTTP 200 - Success` → `code` (`language=json`, wide) → single-cell header table `HTTP 409 - Business error` → `code` (`language=json`) error body.
8. `## Status Code` → 4-col table (`HTTP Code | Custom Status Code | Status Description | Scenario`).
9. `## Field to Field Mapping` → `### When calling the upstream {NAME}` → 5-col table (`Input/Output | Target | Source | Mapping Logic | Remark`).

## Canonical column sets

- **Request Body / Response Body** (identical 5 cols):
  `Field Name | Datatype | Mandatory  M/C/O | Description | Remark`
  (note the *two spaces* in `Mandatory  M/C/O` -- preserved verbatim from the example).
- **Status Code**: `HTTP Code | Custom Status Code | Status Description | Scenario`.
- **Field to Field Mapping**: `Input / Output | Target | Source | Mapping Logic | Remark`.
- **Change logs**: `Date | Update By | Description | Status`.

## Exact markup patterns

**Every table** opens the same way (1761 px wide, default layout):

```xml
<table data-table-width="1761" data-layout="default"><tbody>
  <tr><th><p><strong>Field Name</strong></p></th>…</tr>
  <tr><td><p>…</p></td>…</tr>
</tbody></table>
```

Header cells: `<th><p><strong>HEADER</strong></p></th>`. Body cells: `<td><p>…</p></td>`
(wrap inline content in `<p>`; use `<code>` for identifiers).

**Metadata label cells** (the distinctive highlighted look) -- first cell spans two columns and is grey:

```xml
<td data-highlight-colour="#f4f5f7" colspan="2"><p><strong>Layer</strong></p></td>
<td><p>Adapter</p></td>
```

The first row is the overview intro under a `Overview` label:

```xml
<td data-highlight-colour="#f4f5f7" colspan="2"><p><strong>Overview</strong></p></td>
<td><p>{one-paragraph description of the endpoint}</p></td>
```

Metadata keys (in order): `Overview`, `Layer`, `Microservice`, `Authentication Level`,
`Dependency overview` (section label), `Inbound component`, `Outbound component`,
`Expose to Mobile`, `Access token required`, `Language`, `JIRA` (and optional
`Design` / `Implementation` / `Unit-Test` / `Integration` status rows).

**Wide code block** (sequence source + JSON samples) carries breakout params so it
spans the page width and wraps:

```xml
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">json</ac:parameter>
  <ac:parameter ac:name="breakoutMode">wide</ac:parameter>
  <ac:parameter ac:name="breakoutWidth">4000</ac:parameter>
  <ac:parameter ac:name="wrap">true</ac:parameter>
  <ac:plain-text-body><![CDATA[ … ]]></ac:plain-text-body>
</ac:structured-macro>
```

**Sample-response sub-heading** is itself a single-cell header table (not an `<hN>`):

```xml
<table data-table-width="1761" data-layout="default"><tbody>
  <tr><th><p><strong>HTTP 200 - Success</strong></p></th></tr>
</tbody></table>
```

## What the generator does

`page_template.py` takes a Python dict (overview, metadata, sequence plantuml,
logic steps, request/response field rows + samples, status rows, mapping rows)
and emits this exact storage-format XML. Defaults match the example: request
shown as JSON body, responses as JSON, wide breakout code blocks, highlighted
metadata labels, the fixed 4/5-col table headers. Override anything per-page.

## Divergence from the already-published adapter pages

The 8 endpoint pages built earlier render correctly but differ from the example
in three cosmetic ways (fixable by regenerating with `page_template.py` if exact
fidelity is wanted):

1. They show the **sample request as a curl command** (`language=bash`); the example shows it as a **JSON body** (`language=json`).
2. Their code blocks omit `breakoutMode`/`breakoutWidth`/`wrap` (so they are page-width, not wide-breakout).
3. Their metadata table is a plain 2-col table, not the highlighted 3-col `colspan` layout.
