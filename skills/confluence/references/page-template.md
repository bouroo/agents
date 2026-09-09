# Endpoint/spec page template

Canonical structure for an endpoint/API-spec wiki page, derived by decoding
real, correctly-rendering sibling pages rather than invented. The v3 Python
generator (`page_template.py`) that emitted this layout is gone by design -
an agent following this file produces the identical output - but its two hard
rules survive verbatim below. Authoring transport rules live in [SKILL.md](../SKILL.md)
(Rovo: Confluence-HTML data-type nodes; mcp-atlassian: storage format - the
`[storage-form]` snippets below apply verbatim there).

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

mcp-atlassian storage form - **must** be the native `expand` macro; Confluence
silently strips an HTML `<details>` element from a storage-format body (the
source survives but lands outside any collapsible - caught 2026-09-07 and
republished):

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

### Translating Mermaid sources (repo docs) to PlantUML

Repo-side docs keep Mermaid; wiki pages take PlantUML. Verified element mapping
(2026-09-07, seven sequence diagrams republished blank-diagram-free):

| Mermaid | PlantUML |
| --- | --- |
| `sequenceDiagram` + `autonumber` | `@startuml` + `autonumber` (drop `autonumber` if the family's siblings number steps manually) |
| `actor X as Label` | `actor "Label" as X` |
| `participant X as Label` | `participant "Label" as X` |
| external/producer actor + `queue`/`topic` lifeline | `actor "Producer" as P` + `queue "Kafka\ntopic.name" as MQ` (escape the newline as literal `\n`) |
| storage lifelines (`DB as …`) | `database "Label" as DB` |
| `A->>B: msg` / `A-->>B: msg` | `A -> B: msg` / `A --> B: msg` |
| `alt c1 … else c2 … end` | `alt c1 … else c2 … end` (identical shape) |
| `Note over A,B: text` / `note right of X:` | `note over A,B: text` / `note right of X: text` (single-line form for short notes) |
| `loop every N` | `loop every N … end` |
| `== Section ==` | `== Section ==` (identical) |

Mermaid message-text constructs that BREAK PlantUML - rewrite before shipping:

- `<angle-bracket>` placeholders parse as tags → `[square-brackets]` or prose.
- `<=` / `>=` in expressions → prose ("fire_at is due", "created after schedule").
- `;` mid-message splits the statement → split into two message lines.
- `#` in message text starts PlantUML color syntax → "message 1", not "message #1".
- `"` inside messages → drop or single-quote (participants' display names are
  the quoted position; message text quoting nests badly).

Housekeeping: keep the repo's Mermaid as the source of truth, generate the
PlantUML in the publish script, and assert each generated `data` param
round-trips to a `@startuml…@enduml` source before upload. If diagrams live in
a standalone generator (e.g. `.agents/<task>/generate_storage.py`), leave it in
place for the next sync - regenerating five payloads beat re-deriving the
encoding twice.

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
   **The `plantumlcloud` `data` encoding is NOT standard PlantUML base64, and it
   varies between pages on the same instance** (2026-09-07, two incidents in one
   day: a PlantUML-custom-alphabet publish painted five blank diagrams; the
   correction, validated against the wrong sibling, painted blanks again).
   Recipe proven byte-for-byte against a live tenant instance: `percent-encode
   the source (urllib.parse.quote, safe="/")` → `raw deflate (zlib raw, strip
   the 2-byte zlib header and 4-byte adler tail), compression level 6` →
   `standard base64 with padding KEPT`. Every detail is load-bearing: deflate
   level 9 does not reproduce the reference bytes; stripping padding yields
   output off by exactly the two `=` characters (the diagnostic signature of a
   padding mismatch, not an alphabet mismatch); `+` and `/` appear literally in
   known-good `data` params, PlantUML's `0-9A-Za-z-_` alphabet does not. The
   safe-set is `"/"` exactly - parens ARE percent-encoded (`%28`/`%29` appear
   in known-good params; a `"/()"` safe-set produces byte-different output).
   **Order is load-bearing:** percent-encode FIRST, on the raw source; the
   final `data` param is pure base64 and must contain NO `%`. A param holding
   `%2B`/`%3D` means quote ran *after* base64 (2026-09-09 incident: exactly
   this shipped, the macro's base64 decode choked on `%`, blank diagram) -
   that `%` is the diagnostic signature of an order bug, not an alphabet or
   padding issue. Never ship a body still containing a template marker
   (`PLACEHOLDER`, `TODO`) - a substitution step that silently didn't run
   publishes the marker (2026-09-09: `DIAGRAM_DATA_PLACEHOLDER` in a staged
   body; only a transcript archaeology caught it before/after the fact).
   Storage-form macro:
   `<ac:structured-macro ac:name="plantumlcloud"><ac:parameter ac:name="filename"><name>.svg</ac:parameter><ac:parameter ac:name="data"><encoded></ac:parameter><ac:parameter ac:name="compressed">true</ac:parameter></ac:structured-macro>`.

   **Gated encoder - run this, don't hand-roll it.** It encodes AND gates;
   a push without its `GATE OK` line is unverified:

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

   **Proving a variant instance** (first diagram on a new tenant, or a
   changed recipe): decode the `data` param of a page someone has seen
   **paint in a browser** - a sibling's mere existence proves nothing (the
   2026-09-07 family all shipped blank while the parent painted) - then
   re-encode the *unquoted original* byte-for-byte. Re-encode the inflated
   bytes after `unquote_to_bytes`, never the still-encoded bytes (double-
   quoting makes a correct encoder "fail" and a wrong one look close). And
   check the reference can *discriminate*: if its source contains no parens
   (or whatever character the safe-sets disagree on), byte-match proves
   nothing about that character - prefer a reference whose source covers the
   ambiguous chars, else derive the safe-set directly from the inflated
   bytes: the RESERVED characters appearing literally (unencoded) there are
   the safe-set, and only those - RFC 3986 unreserved chars (`-._~` and
   alphanumerics) stay literal under any `safe` value, so their presence is
   not evidence (proven 2026-09-09: inflated form held literal `{%, -, /}`;
   `%` is the escape char itself, `-` is unreserved → the one reserved
   literal, `/`, is the safe-set). `+`/`=` never appear literally in the
   inflated form, so they are not safe-set evidence. One exact match beats
   three plausible decoders.
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
- Transport note: ~25 KB html bodies published fine on Rovo (create + update,
  no split); retry-with-pause before falling back to create-minimal-then-update.

## Publish checklist

1. Dotted-path row coverage complete against the source structs (rule 1).
2. Samples are full payloads with internally consistent mocks (rule 2); opaque
   payloads single-row (rule 3); field names match serialization tags (rule 4).
3. Diagram = macro + byte-identical raw-source expand; no bare `@startuml`
   code blocks anywhere. `plantumlcloud` payloads: encoder proven against a
   known-good sibling's `data` param, and every generated `data` round-trips
   to a valid `@startuml…@enduml` source — before upload, not after a blank
   render (SKILL.md `content_file` sandbox: payloads staged inside the
   workspace).
4. Table column sets match this template or the target family's recorded set.
5. Read-back after publish: stored body contains every macro wrapper and
   escaped source you intended (SKILL.md, publish-then-prove). If the read-back
   is compressed/truncated by the client, probe via bumped `version`,
   `text ~ "unique-string"` search, and the parent's children listing; render
   confirmation stays manual in a browser.
