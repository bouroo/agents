# Endpoint/spec page template

Canonical structure for an endpoint/API-spec wiki page, derived by decoding
real, correctly-rendering sibling pages rather than invented. The v3 Python
generator (`page_template.py`) that emitted this layout is gone by design -
an agent following this file produces the identical output - but its two hard
rules survive verbatim below. Authoring transport rules live in [SKILL.md](../SKILL.md)
(html contentFormat on the Rovo MCP server; legacy storage-format snippets here
are marked as such and only apply to stdio-bridge-era instances).

## Content-quality rules (mandatory on every endpoint page)

Learned from author-review cycles on 2026-08-14; treat as acceptance criteria:

1. **Every nested field is its own table row**, keyed by dotted path
   (`content.installmentPlans[].promotionalInterestDetail[].startTenor`), never a
   collapsed "see structure below" row. A parent row may summarize ("Each item
   has the fields below"), but the children must still appear as individual rows.
2. **Sample request/response are FULL payloads**: every field documented in the
   tables appears in the sample with realistic mock data, including all
   `headerReq`/`headerResp` fields and every array/nested variant (e.g. a normal
   plan AND a promotional plan in the same response sample). Mock data must be
   internally consistent across request and response (response tiers mirror the
   request's tiers).
3. **Opaque pass-through payloads stay single-row.** Fields whose type is an
   opaque raw-JSON pass-through owned upstream are documented as one row with an
   "opaque, relayed verbatim" remark; never fabricate sub-fields.
4. **Field names come from the source's serialization tags** (e.g. JSON struct
   tags), verified in source, not from memory (`headerResp.statusCd`, not
   `statusCode`).

## Derive structure from a live sibling first

Page structure (macro forms, table attributes, heading levels) is learned by
fetching a **known-good** sibling page in the same space/folder with
`getConfluencePage(contentFormat="html")`, recording its skeleton, and matching
it. Never trust rendered-view summaries alone; diff against stored bodies. The
layout below is the recorded abstraction - it carries no host/space/page id;
re-derive when the target space's conventions differ. Extending an existing
page family means matching the siblings, not imposing this canonical order.

## Diagrams: PlantUML macro + raw-source expand, always

On instances rendering diagrams through the PlantUML macro plugin, diagram
source must ship twice:

1. the diagram **macro**, which renders server-side to SVG, immediately followed by
2. a collapsed expand titled e.g. "Raw sequence diagram source" holding the
   **exact same `@startuml…@enduml` bytes** (html-escaped - arrows contain `>`).

Rovo-MCP html forms observed working:

```html
<details data-breakout="wide"><summary>Raw sequence diagram source</summary>
<pre><code class="language-none">SOURCE</code></pre></details>
```

**Trap:** a bare code block containing `@startuml…` renders as literal text,
never a diagram - the failure mode invisible when re-reading the body. Some
older siblings kept only that broken form; do not copy it. Verify a published
diagram by confirming the macro wrapper survived in the stored body
(`body.view`-style summaries hide it behind stubs).

Sequence style starter (adapt names/colors to the family):

```
@startuml
Title <adapter> API - <microservice> - POST /<path>
hide footbox
actor Requester as requester #85E3FF
box "<adapter> MS" #DFFDFF
entity "<adapter>" as adapter #85E3FF
endbox
box "<Upstream>" #F7E5EC
entity "<upstream>" as upstream #FB9EBB
endbox
requester -> adapter : POST /<path>
@enduml
```

One message per source line: a literal `\n` inside a message is a visual break;
never convert it to a real newline.

## Canonical document order

Top-level sections are H1; headings start at H1 (no leading H1 title - the page
title carries the endpoint name). Storage-format macro snippets below are
marked `[storage-form]`; on Rovo/html instances reproduce the equivalent via
the corresponding Confluence-HTML node or by mirroring the sibling's markup.

1. **Metadata table** - 3-col, centered layout, auto-sized. Labels bold
   `<th colspan="2">`; values `<td><p>...</p></td>`; the Overview row uses a
   highlighted label cell (`data-highlight-colour="#f4f5f7"` in html).
   Rows: Overview · Layer · Microservice · Authentication Level · Dependency
   overview (divider, empty value) · Inbound component · Outbound component ·
   Expose to Mobile · Access token required · Language · JIRA.
2. **H1 Change Log** - 4-col table (column set below). Append a row per
   revision; never rewrite history.
3. **H1 Table of Contents** - toc macro, minLevel 1 / maxLevel 3. `[storage-form]`
   `<ac:structured-macro ac:name="toc">` with those parameters; on html
   instances use whatever TOC extension node the sibling pages carry.
4. **H1 Sequence Diagram** - the macro + raw-source expand pair above. `[storage-form]`
   reference shape: `plantumlcloud` macro (compressed inline source) followed by
   `expand` > `code(language=none)` carrying the identical decompressed source.
5. **H1 Request**: H2 Request Header Schema (5-col field table) · H2 Request
   Body Schema (5-col field table) · H2 Example Request (wide json code block).
6. **H1 Response**: H2 Custom HTTP Response Code (4-col table) · H2 Response
   Schema (5-col field table) · H2 Example Response - single-cell tables per
   case (`Case HTTP 200 Success`, `Case HTTP 400 Bad Request`,
   `Case HTTP 409 Business Error`, `Case HTTP 500 System Error`) each wrapping a
   json code block.
7. **H1 Field-To-Field Mapping** - H2 per downstream call (`Field Mapping when
   calling to <upstream>`), 6-col table.

## Fixed table column sets (match exactly)

| Section | Headers |
| --- | --- |
| Field schema (header/body/response) | Field Name · Data Type · Mandatory (M)/Optional (O)/Conditional (C) · Description · Remark |
| Custom HTTP Response Code | HTTP Code · Custom Status Code · Scenario · Status Description |
| Field-To-Field Mapping | Input/Output · Field Name · Type · M/O/C · Source Field · Remarks |
| Change Log | Date · Updated By · Description · Status |

## Instance variant: "BFF API Specification" page families

Verified by publishing 2026-08-14 (two shortlink pages + siblings under a
parent) and corrected 2026-08-18 after one mis-authored diagram form shipped.
These spaces follow a **different but self-consistent layout** - match the
siblings there instead of the canonical order:

- **H2 section headings** (not H1): `Change logs`, `Sequence diagram`, `Logic`,
  `API Details`, `Status Code`, `Field to Field Mapping`, each preceded by `<hr>`.
- Opens with an info panel (`<div data-type="panel-info">`) titled
  "**BFF API Specification:** \<service\> - \<METHOD\> \<path\>" plus a
  one-paragraph summary.
- Metadata table: fixed width, label cells shaded (`data-background="#f4f5f7"`),
  `Dependency overview` using `rowspan` over nested Inbound/Outbound label rows.
- Change logs row: date `DD-MM-YYYY`, a user mention span (omit rather than
  invent an id), description, and a status span
  (`<span data-type="status" data-color="green" data-status-style="bold">DONE</span>`).
- Sequence diagram: PlantUML extension macro renders server-side SVG; the
  `<details data-breakout="wide">` expand carries the raw source
  (`language-abap` is this family's lexer convention). Exact bytes matter: the
  expand source must equal what the macro renders from. The 2026-08-18 incident
  shipped the plain-code-block form and forced v5 republishes.
- **Logic**: bulleted list of validation/injection/relay/error rules.
- **API Details**: `### Request parameters` field table, then sample request /
  response each wrapped in a 1-col table around a json code block. M/O values:
  mandatory red-styled `M` (`style="color: #de350b"`), optional `O`, conditional `C`.
- **Status Code** table: HTTP Code · Custom Status Code · Status Description ·
  Scenario, including a passthrough row (`- | - | passthrough | …`) for
  inherited downstream errors.
- **Field to Field Mapping**: one `###` table per downstream call
  (`Input / Output | Target | Source | Mapping Logic | Remark`; I/O cell is `I`
  or `O`), plus a final `### Response mapping` table.
- Transport note: ~25 KB html bodies published fine (create + update, no split);
  retry-with-pause before falling back to create-minimal-then-update.

## Publish checklist

1. Dotted-path row coverage complete against the source structs (rule 1).
2. Samples are full payloads with internally consistent mocks (rule 2); opaque
   payloads single-row (rule 3); field names match serialization tags (rule 4).
3. Diagram = macro + byte-identical raw-source expand; no bare `@startuml`
   code blocks anywhere.
4. Table column sets match this template or the target family's recorded set.
5. Read-back after publish: stored body contains every macro wrapper and
   escaped source you intended (SKILL.md, publish-then-prove).
