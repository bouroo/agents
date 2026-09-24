# Endpoint/spec page template

Canonical structure for an endpoint/API-spec wiki page, decoded from real,
correctly-rendering siblings rather than invented. Following this file reproduces the
retired v3 generator's layout; its two hard rules survive verbatim. Transport rules
live in [SKILL.md](../SKILL.md): Rovo uses Confluence-HTML data-type nodes,
mcp-atlassian storage format - the `[storage-form]` snippets apply there.

## Contents

- [Content-quality rules](#content-quality-rules-mandatory-on-every-endpoint-page)
- [Match a live sibling first](#match-a-live-sibling-first)
- [Diagrams: PlantUML macro + raw-source expand](#diagrams-plantuml-macro--raw-source-expand-always)
- [Translating Mermaid to PlantUML](#translating-mermaid-sources-repo-docs-to-plantuml)
- [Canonical document order](#canonical-document-order)
- [Fixed table column sets](#fixed-table-column-sets-match-exactly)
- [Change Log + highlighting](#change-log--change-highlighting-page-updates)
- [Instance variant: BFF families](#instance-variant-bff-api-specification-page-families)
- [Publish checklist](#publish-checklist)

## Content-quality rules (mandatory on every endpoint page)

1. **Every nested field is its own table row**, keyed by dotted path
   (`content.installmentPlans[].promotionalInterestDetail[].startTenor`), never a
   collapsed "see structure below" row. A parent row may summarize ("Each item has
   the fields below"), but the children still appear as individual rows.
2. **Sample request/response are FULL payloads**: every field documented in the
   tables appears in the sample with realistic mock data, including all
   `headerReq`/`headerResp` fields and every array/nested variant (a normal plan AND
   a promotional plan in one response). Mocks stay internally consistent across
   request and response (response tiers mirror the request's tiers).
3. **Opaque pass-through payloads stay single-row.** A field whose type is an opaque
   raw-JSON pass-through owned upstream is one row with an "opaque, relayed verbatim"
   remark; never fabricate sub-fields.
4. **Field names come from the source's serialization tags** (e.g. JSON struct tags),
   verified in source, not memory (`headerResp.statusCd`, not `statusCode`).

## Match a live sibling first

Structure (macro forms, table attributes, heading levels) is learned, not imposed:
fetch a **known-good** sibling in the same space/folder with
`getConfluencePage(contentFormat="html")`, record its skeleton, and match it. Never
trust rendered-view summaries alone - diff stored bodies. The layout below is the
recorded abstraction and carries no host/space/page id; re-derive when the target
space's conventions differ, and extend a page family by matching its siblings rather
than imposing the canonical order.

For "render/update this page to match <URL>" requests, treat the supplied shortlink as
the **template anchor**: fetch it in stored form before drafting, record its skeleton
(headings, macro wrappers, panels, table attributes, column sets), and reuse that exact
shape - do not substitute the canonical order unless the anchor uses it or the user asks
for normalization. If the anchor is only the target page (not a proven-rendering
sibling), name a sibling and compare both stored bodies before choosing the stronger
template. A decoded anchor graduates into an instance-variant record below. Real-work
identity (page titles, spaces, shortlinks) never enters this doctrine - it lives in
machine-local memory; the `privacy` gate (`scripts/check.py`) enforces it.

## Diagrams: PlantUML macro + raw-source expand, always

Where diagrams render through the PlantUML macro plugin, source ships twice:

1. the diagram **macro**, rendering server-side to SVG, immediately followed by
2. a collapsed expand titled e.g. "Raw sequence diagram source" holding the **exact
   same `@startuml…@enduml` bytes** (html-escaped - arrows contain `>`).

Rovo-MCP html form:

```html
<details data-breakout="wide"><summary>Raw sequence diagram source</summary>
<pre><code class="language-none">SOURCE</code></pre></details>
```

mcp-atlassian storage form - **must** be the native `expand` macro; Confluence
silently strips an HTML `<details>` from a storage-format body (the source survives
but lands outside any collapsible):

```xml
<ac:structured-macro ac:name="expand">
  <ac:parameter ac:name="title">Raw sequence diagram source</ac:parameter>
  <ac:rich-text-body>
    <ac:structured-macro ac:name="code">
      <ac:parameter ac:name="language">none</ac:parameter>
      <ac:plain-text-body><![CDATA[SOURCE]]></ac:plain-text-body>
    </ac:structured-macro>
  </ac:rich-text-body>
</ac:structured-macro>
```

**Trap:** a bare code block containing `@startuml…` renders as literal text, never a
diagram - the failure invisible when re-reading the body. Older siblings may keep only
that broken form; do not copy it. Verify a published diagram by confirming the macro
wrapper survived in the stored body (`body.view`-style summaries hide it).

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

One message per source line: a literal `\n` inside a message is a visual break; never
convert it to a real newline.

### Translating Mermaid sources (repo docs) to PlantUML

Repo docs keep Mermaid; wiki pages take PlantUML. Verified element mapping:

| Mermaid | PlantUML |
| --- | --- |
| `sequenceDiagram` + `autonumber` | `@startuml` + `autonumber` (drop `autonumber` if siblings number steps manually) |
| `actor X as Label` | `actor "Label" as X` |
| `participant X as Label` | `participant "Label" as X` |
| external/producer actor + `queue`/`topic` lifeline | `actor "Producer" as P` + `queue "Kafka\ntopic.name" as MQ` (escape the newline as literal `\n`) |
| storage lifelines (`DB as …`) | `database "Label" as DB` |
| `A->>B: msg` / `A-->>B: msg` | `A -> B: msg` / `A --> B: msg` |
| `alt c1 … else c2 … end` | `alt c1 … else c2 … end` (identical shape) |
| `Note over A,B: text` / `note right of X:` | `note over A,B: text` / `note right of X: text` (single-line form for short notes) |
| `loop every N` | `loop every N … end` |
| `== Section ==` | `== Section ==` (identical) |

Mermaid message-text that BREAKS PlantUML - rewrite before shipping:

- `<angle-bracket>` placeholders parse as tags → `[square-brackets]` or prose.
- `<=` / `>=` in expressions → prose ("fire_at is due", "created after schedule").
- `;` mid-message splits the statement → split into two message lines.
- `#` in message text starts PlantUML color syntax → "message 1", not "message #1".
- `"` inside messages → drop or single-quote (participants' display names are the
  quoted position; message-text quoting nests badly).

Housekeeping: keep the repo's Mermaid as source of truth, generate PlantUML in the
publish script, and assert each generated `data` round-trips to a `@startuml…@enduml`
source before upload. If diagrams live in a standalone generator (e.g.
`.agents/<task>/generate_storage.py`), leave it for the next sync.

## Canonical document order

Top-level sections are H1 (no leading H1 title - the page title carries the endpoint
name). `[storage-form]` snippets below: on Rovo/html reproduce the equivalent
Confluence-HTML node or mirror the sibling's markup.

1. **Metadata table** - 3-col, centered, auto-sized. Labels bold `<th colspan="2">`;
   values `<td><p>...</p></td>`; the Overview row uses a highlighted label cell
   (`data-highlight-colour="#f4f5f7"` in html). Rows: Overview · Layer ·
   Microservice · Authentication Level · Dependency overview (divider, empty
   value) · Inbound component · Outbound component · Expose to Mobile · Access token
   required · Language · JIRA.
2. **H1 Change Log** - 4-col table (column set below). Append a row per revision;
   never rewrite history.
3. **H1 Table of Contents** - toc macro, minLevel 1 / maxLevel 3. `[storage-form]`
   `<ac:structured-macro ac:name="toc">` with those parameters; on html use whatever
   TOC extension node the siblings carry.
4. **H1 Sequence Diagram** - the macro + raw-source expand pair above. `[storage-form]`
   shape: `plantumlcloud` macro (compressed inline source) then `expand` >
   `code(language=none)` with the identical decompressed source. **The `plantumlcloud`
   `data` encoding is NOT standard PlantUML base64 and varies between pages on the
   same instance** (a custom-alphabet publish paints blanks against the wrong
   sibling). Recipe, proven byte-for-byte against a live tenant: percent-encode the
   source (`urllib.parse.quote`, `safe="/"`) → raw deflate (strip the 2-byte zlib
   header and 4-byte adler tail), level 6 → standard base64, padding KEPT. Every
   detail is load-bearing: level 9 does not reproduce the reference bytes; stripping
   padding is off by exactly the two `=` characters (a padding mismatch, not an
   alphabet mismatch); `+` and `/` appear literally in known-good params, PlantUML's
   `0-9A-Za-z-_` alphabet does not; the safe-set is `"/"` exactly - parens ARE
   percent-encoded (`%28`/`%29` appear in known-good params; `"/()"` is
   byte-different). **Order matters:** percent-encode FIRST on the raw source; the
   final `data` is pure base64 with NO `%`. A param holding `%2B`/`%3D` means quote
   ran *after* base64 - the `%` is the order-bug signature, not an alphabet or padding
   issue. Never ship a body still holding a template marker (`PLACEHOLDER`, `TODO`) -
   a substitution step that silently didn't run publishes it. Storage-form macro:
   `<ac:structured-macro ac:name="plantumlcloud"><ac:parameter ac:name="filename"><name>.svg</ac:parameter><ac:parameter ac:name="data"><encoded></ac:parameter><ac:parameter ac:name="compressed">true</ac:parameter></ac:structured-macro>`.

   **Gated encoder - run this, don't hand-roll it.** It encodes AND gates; a push
   without its `GATE OK` line is unverified:

   ```python
   import base64, re, sys, urllib.parse, zlib

   def encode_data_param(source: bytes) -> str:
       q = urllib.parse.quote(source, safe="/").encode()
       c = zlib.compressobj(6, zlib.DEFLATED, -15)   # raw deflate, level 6
       return base64.b64encode(c.compress(q) + c.flush()).decode()

   def gate(data: str, source: bytes, body: str) -> None:
       assert re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", data), "param: not pure base64 (a % means quote ran after b64 - order bug)"
       assert "%" not in data,                        "param: contains % - percent-encoding applied in the wrong stage"
       rt = urllib.parse.unquote_to_bytes(zlib.decompress(base64.b64decode(data), -15))
       assert rt == source,                           "round-trip: decode->inflate->unquote != source"
       assert not re.search(r"PLACEHOLDER|TODO|FIXME|<[a-z_]+_DATA>", body, re.I), "body: template marker left unsubstituted"
       print("GATE OK", len(data), "chars")

   source = open("diagram.puml", "rb").read()
   data = encode_data_param(source)
   gate(data, source, open("page.html").read())
   ```

   **Prove a variant instance** (first diagram on a new tenant, or a changed recipe):
   decode the `data` of a page someone has seen **paint in a browser** (a sibling's
   mere existence proves nothing), then re-encode the *unquoted original*
   byte-for-byte - the inflated bytes after `unquote_to_bytes`, never the still-encoded
   ones (double-quoting makes a correct encoder "fail" and a wrong one look close).
   Check the reference can *discriminate*: if its source has no parens (or whatever
   character the safe-sets disagree on), byte-match proves nothing about that
   character - prefer a reference covering the ambiguous chars, else read the safe-set
   off the inflated bytes: the RESERVED characters appearing literally there are the
   safe-set, and only those (RFC 3986 unreserved `-._~` and alphanumerics stay literal
   under any `safe`, so they are not evidence; `+`/`=` never appear literally either).
   One exact match beats three plausible decoders.

5. **H1 Request**: H2 Request Header Schema (5-col field table) · H2 Request Body
   Schema (5-col field table) · H2 Example Request (wide json code block).
6. **H1 Response**: H2 Custom HTTP Response Code (4-col table) · H2 Response Schema
   (5-col field table) · H2 Example Response - single-cell tables per case
   (`Case HTTP 200 Success`, `Case HTTP 400 Bad Request`, `Case HTTP 409 Business
   Error`, `Case HTTP 500 System Error`) each wrapping a json code block.
7. **H1 Field-To-Field Mapping** - H2 per downstream call (`Field Mapping when
   calling to <upstream>`), 6-col table.

## Fixed table column sets (match exactly)

| Section | Headers |
| --- | --- |
| Field schema (header/body/response) | Field Name · Data Type · Mandatory (M)/Optional (O)/Conditional (C) · Description · Remark |
| Custom HTTP Response Code | HTTP Code · Custom Status Code · Scenario · Status Description |
| Field-To-Field Mapping | Input/Output · Field Name · Type · M/O/C · Source Field · Remarks |
| Change Log | Date · Updated By · Description · Status |

## Change Log + change highlighting (page updates)
[changelog]

An update must let a reader see the delta without opening version history: baseline
diff, marked rows, one Change Log table per page.

### Baseline diff first

`confluence_get_page_history(page_id, version=N, convert_to_markdown=false)` returns
the full stored body of any prior version (the tool defaults `convert_to_markdown=true`
- always pass `false` for storage work; its `space` field returns "Unknown", a tool
quirk, ignore it). Walk `N = current-1, current-2, …` until the version's timestamp
precedes the current effort's start date; that version is the pre-change baseline.
Diff section/field sets baseline vs new body - fields in the body missing from the
baseline are `New`, fields only in the baseline are `Removed`, value/type/requirement
drift is `Modified`, renames are `Renamed`.

### Mark the changed points

- Rebuilt tables add a trailing `Change` column: changed rows carry their `C#` and the
  field name in `<strong>`; untouched rows leave the cell empty. Storage form:
  `<td><p>C1</p></td>` / empty `<td><p></p></td>`.
- Removed content leaves no live row - recorded only as a `Removed` Change Log row
  naming the baseline path.
- Prose-level semantic shifts (e.g. an endpoint's error model changing) take a
  page-level row with Field `—`.

### Change Log table (h3, after the changed sections)

```xml
<h3>Change Log</h3>
<table><tbody>
  <tr><th><p>Change #</p></th><th><p>Date</p></th><th><p>Field</p></th><th><p>Change Type</p></th><th><p>Description</p></th></tr>
  <tr><td><p>C1</p></td><td><p>&lt;edit-date&gt;</p></td><td><p><strong>content.x</strong></p></td><td><p>Modified</p></td><td><p>…</p></td></tr>
  <tr><td><p>C2</p></td><td><p>&lt;edit-date&gt;</p></td><td><p>—</p></td><td><p>Modified</p></td><td><p>page-level shift, e.g. error semantics</p></td></tr>
</tbody></table>
```

Rules: `Date` = the edit date; `Change Type` ∈ `New | Modified | Renamed | Removed`;
numbering restarts at `C1` per page; field-level rows preferred, page-level `—` only
for shifts no single field carries; `Renamed` rows name the pre-rename path in the
Description while the `C#` anchors on the live (renamed) row.

### Integrity gate (add to the publish proof)

After publish, re-fetch and check refs bidirectionally: every `C#` used in body tables
exists in the Change Log **and** every Change Log `C#` anchors in the body - under
three documented relaxations: page-level rows (Field `—`) are exempt, aggregate rows
(`X[].*`) match if any table row starts with `X[].`, and `Removed` rows anchor only in
the baseline (no live row by definition). A dangling ref either direction is a publish
blocker, same tier as a failed `GATE OK`.

## Instance variant: "BFF API Specification" page families

These spaces follow a **different but self-consistent layout** - match the siblings
instead of the canonical order. Two surface records; where they diverge, match the
surface you publish through.

**Rovo (Confluence-HTML) surface:**

- **H2 section headings** (not H1): `Change logs`, `Sequence diagram`, `Logic`,
  `API Details`, `Status Code`, `Field to Field Mapping`, each preceded by `<hr>`.
- Opens with an info panel (`<div data-type="panel-info">`) titled "**BFF API
  Specification:** \<service\> - \<METHOD\> \<path\>" plus a one-paragraph summary.
- Metadata table: fixed width, label cells shaded (`data-background="#f4f5f7"`),
  `Dependency overview` using `rowspan` over nested Inbound/Outbound label rows.
- Change logs row: date `DD-MM-YYYY`, a user mention span (omit rather than invent an
  id), description, and a status span
  (`<span data-type="status" data-color="green" data-status-style="bold">DONE</span>`).
- Sequence diagram: PlantUML extension macro renders server-side SVG; the
  `<details data-breakout="wide">` expand carries the raw source (`language-abap` is
  this family's lexer convention). The expand source must equal what the macro renders
  from; the plain-code-block form forces republishes.
- **Logic**: bulleted list of validation/injection/relay/error rules.
- **API Details**: `### Request parameters` field table, then sample request / response
  each wrapped in a 1-col table around a json code block. M/O values: mandatory
  red-styled `M` (`style="color: #de350b"`), optional `O`, conditional `C`.
- **Status Code** table: HTTP Code · Custom Status Code · Status Description ·
  Scenario, including a passthrough row (`- | - | passthrough | …`) for inherited
  downstream errors.
- **Field to Field Mapping**: one `###` table per downstream call (`Input / Output |
  Target | Source | Mapping Logic | Remark`; I/O cell is `I` or `O`), plus a final
  `### Response mapping` table.
- Transport note: ~25 KB html bodies published fine on Rovo (create + update, no
  split); retry-with-pause before falling back to create-minimal-then-update.

### Storage-form record (mcp-atlassian surface)

The storage-format rendering of this family (identity held in machine-local memory,
never in this doctrine). Same skeleton as the Rovo record, with these load-bearing
divergences:

- **H2/H3 ladder, no H1, no panel, no TOC.** Opens directly with the metadata table.
  Sections: `Change logs`, `Sequence diagram`, `Logic`, `API Details` (H3: `Request
  parameters`, `Sample request (full)`, `Response parameters`, `Sample response
  (full)`), `Status Code`, `Field to Field Mapping` (numbered H3 per downstream call,
  then `4. Response mapping`). Separators are `<hr data-layout="wide"
  data-width="760"/>` before every H2 **except** `Change logs` (page top) and
  `API Details`.
- **Editor-v2 table attributes:** every table carries `ac:local-id`, `data-layout`,
  `data-table-width` (1761; change-logs 1746); header cells are
  `<th><p><strong>...</strong></p></th>`; label cells shade with
  `data-highlight-colour="#f4f5f7"` (not `data-background`); metadata labels are
  `<td ac:local-id="…" colspan="2" data-highlight-colour="#f4f5f7">` (attribute order
  matters; `local-id` values are server-generated). Metadata rows: Overview · Layer ·
  Microservice · Authentication Level · Dependency overview (`rowspan="2"` over Inbound
  component / Outbound component) · Expose to Mobile · Access token required · Language
  (no JIRA row on this instance).
- **Change logs:** columns `Date | Update By | Description | Status`; the mention is
  plain `@Full Name` text; the Status cell is a status **macro** `[storage-form]`:
  `<ac:structured-macro ac:name="status">` with
  `<ac:parameter ac:name="title">DONE</ac:parameter>` +
  `<ac:parameter ac:name="colour">Green</ac:parameter>`.
- **Sequence diagram:** `plantumlcloud` macro (`filename` = `<slug>-sequence.svg`,
  `data` = gated-encoder payload, `compressed` = `true`), then an `expand` **macro**
  (`title` + `breakoutWidth=1800`, `data-layout="wide"`) wrapping a `code` macro
  (`language=abap`, body in `<ac:plain-text-body><![CDATA[...]]></ac:plain-text-body>`).
- **Schema tables:** `Field | Type | M/O | Description | Remark`; mandatory `M` is
  `<span style="color: rgb(222,53,11);">M</span>` (no space after the comma); optional
  `O` is plain text. Cells changed in the current revision shade
  `data-highlight-colour="#fffae6"` (old/new naming pairs).
- **Sample wrappers:** a 1-col table around each `code` (`language=json`) macro; the
  caption header row is `<strong>Body</strong>` for the request and `<strong>HTTP 200 -
  Success</strong>` for the response.
- **Status Code:** `HTTP Code | Custom Status Code | Status Description | Scenario` -
  same set as the Rovo record. **Field to Field Mapping:** `Input / Output | Target |
  Source | Mapping Logic | Remark` with `I`/`O` in the first cell - one table per
  numbered H3.

## Publish checklist

1. Template anchor fetched in stored form; target skeleton matches it for heading
   levels, panel/macro wrappers, table attributes and column sets.
2. Dotted-path row coverage complete against the source structs (rule 1).
3. Samples are full payloads with internally consistent mocks (rule 2); opaque
   payloads single-row (rule 3); field names match serialization tags (rule 4).
4. Diagram = macro + byte-identical raw-source expand; no bare `@startuml` code blocks
   anywhere. `plantumlcloud` payloads: encoder proven against a known-good sibling's
   `data` param, and every generated `data` round-trips to a valid `@startuml…@enduml`
   source - before upload, not after a blank render (SKILL.md `content_file` sandbox:
   payloads staged inside the workspace).
5. Table column sets match the selected template anchor or the target family's
   recorded set.
6. Read-back after publish: stored body contains every macro wrapper and escaped source
   you intended (SKILL.md, publish-then-prove). If the read-back is compressed/truncated
   by the client, probe via bumped `version`, `text ~ "unique-string"` search, and the
   parent's children listing; render confirmation stays manual in a browser.
7. Change refs bidirectional: every `C#` in body tables exists in the page's Change Log
   and vice versa (relaxations: Field `—`, `X[].*` prefix rows, `Removed` rows).
