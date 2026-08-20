# Endpoint page template (canonical layout)

The standard structure for an endpoint/spec page, derived by decoding a real,
correctly-rendering sibling endpoint page on the target Confluence instance.
Match this when authoring any new endpoint/spec page. The companion generator
`../page_template.py` (`build_page`) emits this layout from a structured spec
dict. Authoring mechanics (macros, compression, storage format) live in
[storage-format.md](./storage-format.md) + [plantuml.md](./plantuml.md).

## Content-quality rules (mandatory on every endpoint page)

Learned from author-review cycles on 2026-08-14; treat as acceptance criteria:

1. **Every nested field is its own table row**, keyed by dotted path
   (`content.installmentPlans[].promotionalInterestDetail[].startTenor`), never a
   collapsed "see structure below" row. A parent row may summarize ("Each item has
   the fields below") but the children must still appear as individual rows.
2. **Sample request/response are FULL payloads**: every field documented in the
   tables appears in the sample with realistic mock data, including all
   `headerReq`/`headerResp` fields and every array/nested variant (e.g. a normal
   plan AND a promotional plan in the same response sample). Mock data must be
   internally consistent across request and response (response tiers mirror the
   request's tiers).
3. **Opaque pass-through payloads stay single-row.** Fields whose type is an
   opaque raw-JSON pass-through in source (schema owned upstream) are documented
   as one row with an "opaque, relayed verbatim" remark; never fabricate sub-fields.
4. **Field names come from the source's serialization tags** (e.g. JSON struct
   tags), verified in source, not from
   memory (e.g. `headerResp.statusCd`, not `statusCode`).

## Why decode a real page

Confluence page structure (macro forms, table attributes, heading levels) is
learned by fetching a **known-good** sibling page in the same space/folder,
reading its **storage body** (not `body.view`), and recording the structure. The
result below is the abstract layout; it carries no host, space, page id, or
endpoint name -- plug those in per target. Re-derive from a new sibling page if
the target instance's layout differs.

## Diagram tech: PlantUML (`plantumlcloud`), not mermaid

On instances that render via the mxgraph **`plantumlcloud`** plugin, diagram
source is stored **inline, compressed** in the macro's `data` parameter
(decode/encode verified; see [plantuml.md](./plantuml.md)) and is the only
diagram tech reproducible from page storage XML. Confirm the instance's diagram
macro on first use (see [SKILL.md §3](../SKILL.md) + [mermaid.md](./mermaid.md));
**default diagrams to PlantUML** unless a working native mermaid macro is proven
on the instance.

## Document order

1. **Metadata table** a 3-column table, centered layout (`data-layout="center"`),
   auto-sized (no fixed `data-table-width`, no `<colgroup>` pixel widths, let it
   size to content). Label cells are bold
   `<th colspan="2"><p><strong>Label</strong></p></th>`; values are
   `<td><p>value</p></td>`. The Overview row is the exception: a highlighted
   `<td colspan="2" data-highlight-colour="#f4f5f7">` label + value. Rows: Overview,
   Layer, Microservice, Authentication Level, Dependency overview (divider, empty
   value), Inbound component, Outbound component, Expose to Mobile, Access token
   required, Language, JIRA.
2. **H1 `Change Log`** → 4-col table `Date | Updated By | Description | Status`.
3. **H1 `Table of Contents`** → `ac:name="toc"` macro (`minLevel` 1, `maxLevel` 3).
4. **H1 `Sequence Diagram`** → **two** macros, in this order:
   1. `plantumlcloud` with the compressed `data` param the only form Confluence
      **renders** server-side into an SVG.
   2. an `expand` macro holding the **raw `@startuml…@enduml` source** in a `code`
      block (collapsed by default), so the diagram is editable without recompression.

   ```xml
   <h1>Sequence Diagram</h1>
   <ac:structured-macro ac:name="plantumlcloud" ac:schema-version="1">
     <ac:parameter ac:name="filename">diagram-name.svg</ac:parameter>
     <ac:parameter ac:name="data">{COMPRESSED}</ac:parameter>
   </ac:structured-macro>
   <ac:structured-macro ac:name="expand" ac:schema-version="1">
     <ac:parameter ac:name="title">Raw sequence diagram source</ac:parameter>
     <ac:rich-text-body>
       <ac:structured-macro ac:name="code" ac:schema-version="1">
         <ac:parameter ac:name="language">none</ac:parameter>
         <ac:plain-text-body><![CDATA[@startuml ... @enduml]]></ac:plain-text-body>
       </ac:structured-macro>
     </ac:rich-text-body>
   </ac:structured-macro>
   ```

   In the generator: `plantuml_macro(seq, svg)` then
   `expand_macro("Raw sequence diagram source", code_macro(seq, language="none"))`.

   **Trap:** a plain `code` macro holding `@startuml` source renders as a **code
   panel of literal text**, NOT a diagram; only `plantumlcloud` renders. Sibling
   pages are inconsistent: older pages sometimes keep only the `code` panel; **do
   not copy that form**. Hand-authoring must emit both, exactly as the generator
   does. Verify by decoding the stored `data` back to valid `@startuml…@enduml`
   source; `body.view` returns only a macro stub for `plantumlcloud`, so it is
   **not** proof of a render.
5. **H1 `Request`**
   - **H2 `Request Header Schema`** → 5-col field table.
   - **H2 `Request Body Schema`** → 5-col field table.
   - **H2 `Example Request`** → wide `code` block (language `json`).
6. **H1 `Response`**
   - **H2 `Custom HTTP Response Code`** → 4-col table.
   - **H2 `Response Schema`** → 5-col field table.
   - **H2 `Example Response`** → single-cell header tables `Case HTTP 200 Success`
     / `Case HTTP 400 Bad Request` / `Case HTTP 409 Business Error` /
     `Case HTTP 500 System Error`, each over a `code` (language `json`) body.
7. **H1 `Field-To-Field Mapping`** → **H2 `Field Mapping when calling to <upstream>`**
   → 6-col table.

Top-level sections are **H1** (no leading H1 title; the page title carries the
endpoint name). All headings start at H1, not H2.

## Fixed table column sets (match exactly)

| Section | Headers |
| --- | --- |
| Field schema (header/body/response) | Field Name · Data Type · Mandatory (M) /Optional (O) /Conditional (C) · Description · Remark |
| Custom HTTP Response Code | HTTP Code · Custom Status Code · Scenario · Status Description |
| Field-To-Field Mapping | Input/ Output · Field Name · Type · Mandatory (M) /Optional (O) /Conditional (C) · Source Field · Remarks |
| Change Log | Date · Updated By · Description · Status |

`build_page` exposes these as `FIELD_HDR`, `STATUS_HDR`, `MAP_HDR`.

## PlantUML sequence style

```
@startuml
Title adapter API - <microservice> - POST /<path>
hide footbox
actor Requester as requester #85E3FF
box "<adapter> MS" #DFFDFF
entity "<adapter>" as adapter #85E3FF
endbox
box "<Upstream>" #F7E5EC
entity "<upstream>" as upstream #FB9EBB
endbox
requester -> adapter : POST /<path>
...
@enduml
```

Sequence-message rule: keep each message on **one source line**; a literal `\n`
inside a message is a visual break, never turn it into a real newline (see
[plantuml.md](./plantuml.md) `\n` trap). Render every authored diagram to SVG and
assert non-trivial output before publishing.

**Sequence section = rendered diagram + raw source expand.** Every Sequence Diagram
section has both: the `plantumlcloud` macro (rendered) immediately followed by the
same source in a collapsed expand ("Raw sequence diagram source") so the source is
recoverable and copy-editable on the page. `build_page` emits this pair; when
authoring by hand, decode the macro's `data` param and emit the same source in the
expand. Remote-MCP (`html`) form: `<details><summary>Raw sequence diagram source</summary><pre><code class="language-none">SOURCE</code></pre></details>` (HTML-escape the source; arrows `->`/`-->` contain `>`).

## Instance variant: tenant "BFF API Specification" pages

Verified by publishing 2026-08-14 on a tenant instance (two shortlink pages
and siblings under a parent page). The sibling pages in this space follow a **different but
self-consistent layout**; when extending a family of endpoint pages there, match
the siblings, not the canonical order above:

- **H2 section headings** (not H1): `Change logs`, `Sequence diagram`, `Logic`,
  `API Details`, `Status Code`, `Field to Field Mapping`, each preceded by `<hr>`.
- **Opens with a `panel-info`** (`<div data-type="panel-info">`) titled
  "**BFF API Specification:** <service> - <METHOD> <path>" + one-paragraph summary.
- **Metadata table**: fixed `data-width="1761"`, label cells
  `data-background="#f4f5f7"` with `style="background-color: #f4f5f7"` and
  `data-colwidth` groups; `Dependency overview` uses `rowspan` with nested
  `Inbound component` / `Outbound component` label rows.
- **Change logs** row: date `DD-MM-YYYY`, `<span data-type="mention"
  data-user-id="...">` (omit rather than invent an id), description, and
  `<span data-type="status" data-color="green" data-status-style="bold">DONE</span>`.
  Append a row per revision, never rewrite history.
- **Sequence diagram uses the `plantumlcloud` extension macro + raw-source
  expand, same as the canonical form** (see step 4 above and
  [plantuml.md](./plantuml.md) "Remote MCP" section): the macro div renders
  server-side into SVG; the `<details data-breakout="wide">` expand below it
  carries the raw `@startuml…@enduml` source (lexer `language-abap`, the
  sibling-page convention). The expand source must be the exact bytes
  compressed into the macro's `data` param. A plain
  `<pre data-breakout="wide"><code class="language-none">@startuml…</code></pre>`
  block renders as **literal text, never a diagram** on this instance;
  following that (earlier mis-recorded) form shipped 2026-08-18 and both pages
  had to be re-published as v5 with the macro.
- **Logic** = bulleted `<ul><li>` list of validation/injection/relay/error rules.
- **API Details** = `### Request parameters` table (`Field | Type | M/O |
  Description | Remark`), `### Sample request (full)` in a 1-col table wrapping
  `<pre><code class="language-json">`, then the same pair for the response. M/O
  values: mandatory `<span style="color: #de350b">M</span>`, optional `O`,
  conditional `C`.
- **Status Code** table: `HTTP Code | Custom Status Code | Status Description |
  Scenario`, with a `passthrough` row (`- | - | passthrough | …`) for inherited
  downstream errors.
- **Field to Field Mapping**: one `###`-level table per downstream call
  (`Input / Output | Target | Source | Mapping Logic | Remark`; I/O cell is `I`
  or `O`), plus a final `### Response mapping` table.
- **Remote-MCP html transport handled ~25 KB bodies fine** (create + update, no
  502 split needed) on this instance; retry-with-pause before falling back to the
  create-then-update minimal-placeholder pattern.
