# Endpoint/spec page template

Canonical structure for an endpoint/API-spec wiki page, decoded from real,
correctly-rendering siblings rather than invented. Following this file reproduces the
retired v3 generator's layout; its two hard rules survive verbatim. Transport rules
live in [SKILL.md](../SKILL.md): Rovo uses Confluence-HTML data-type nodes,
mcp-atlassian storage format — the `[storage-form]` snippets apply there.

## Contents

- Content-quality rules
- Match a live sibling first
- Diagrams: PlantUML macro + raw-source expand
- Translating Mermaid to PlantUML
- Canonical document order (Overview table → Change logs → TOC → Sequence diagram →
  Request → Response → Field to Field Mapping)
- Fixed table column sets
- Change logs + round markers (`#changeN`) — see [page-updates](page-updates.md)
- Instance variant: BFF families — see [page-family-variants](page-family-variants.md)
- Publish checklist

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

5. **Samples look like real traffic, not placeholders.** No `"string"`, `"req-1"`,
   `"xxx"`: fill every field with a value of the right type, length, and format —
   real-looking IDs, RFC3339 timestamps in the service's offset, amounts at the right
   scale, enum values that exist in the code. `headerReq.reqID` and
   `headerReq.correlationID` are always lower-case UUID v4 and **differ** in the request
   sample. Sample values are illustrations, never real customer data.
6. **Every cell traces to a source** — the source spec page, code under the service
   repo, a plan the user pointed to, or the user's own words. No source, no guess: write
   `TBD` and name who owes it. "Just put something plausible" is not a source; a guessed
   error code gets implemented by the next reader.
7. **Error Mapping lists every failure path** the flow has — validation, each downstream
   error, business rules. A path whose code is unknown still gets a row, with `TBD` for
   the code.
8. **Table hygiene:** every row has the header's cell count (`| |` for an empty cell);
   `<br>` for a line break inside a cell; a `|` inside a cell stays inside backticks or
   is escaped `\|`.

## Match a live sibling first

Structure (macro forms, table attributes, heading levels) is learned, not imposed:
fetch a **known-good** sibling in the same space/folder with
`getConfluencePage(contentFormat="html")`, record its skeleton, and match it. Never
trust rendered-view summaries alone — diff stored bodies. The layout below is the
recorded abstraction and carries no host/space/page id; re-derive when the target
space's conventions differ, and extend a page family by matching its siblings rather
than imposing the canonical order.

For "render/update this page to match <URL>" requests, treat the supplied shortlink as
the **template anchor**: fetch it in stored form before drafting, record its skeleton
(headings, macro wrappers, panels, table attributes, column sets), and reuse that exact
shape — do not substitute the canonical order unless the anchor uses it or the user asks
for normalization. If the anchor is only the target page (not a proven-rendering
sibling), name a sibling and compare both stored bodies before choosing the stronger
template. A decoded anchor graduates into an instance-variant record in
[page-family-variants](page-family-variants.md). Real-work
identity (page titles, spaces, shortlinks) never enters this doctrine — it lives in
machine-local memory; the `privacy` gate (`scripts/check.py`) enforces it.

## Diagrams: PlantUML macro + raw-source expand, always

Where diagrams render through the PlantUML macro plugin, source ships twice:

1. the diagram **macro**, rendering server-side to SVG, immediately followed by
2. a collapsed expand titled e.g. "Raw sequence diagram source" holding the **exact
   same `@startuml…@enduml` bytes** (html-escaped — arrows contain `>`).

Rovo-MCP html form:

```html
<details data-breakout="wide"><summary>Raw sequence diagram source</summary>
<pre><code class="language-none">SOURCE</code></pre></details>
```

mcp-atlassian storage form — **must** be the native `expand` macro; Confluence
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
diagram — the failure invisible when re-reading the body. Older siblings may keep only
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

Mermaid message-text that BREAKS PlantUML — rewrite before shipping:

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

The page opens with a **front-matter-derived Overview table**, then these sections in
this order. `[storage-form]` snippets below: on Rovo/html reproduce the equivalent
Confluence-HTML node or mirror the sibling's markup.

0. **Overview table** — generated from the spec front matter (`title`, `overview`,
   `microservice`, `auth`, `api_type`, `swagger`, `inbound`, `outbound`, `language`,
   `people`, `jira`), never written by hand in the body. Each `inbound`/`outbound` item
   is **one API**, not one service: a markdown link to that API's spec page becomes an
   inline card; a page-less API is plain text `<service> - <METHOD> /<path>`. A `people`
   entry maps `Full Name` to its `accountId`, which makes every `@Full Name` in the
   Change logs a real mention.
1. **`## Change logs`** — 4-col table (column set below). Append a row per revision;
   never rewrite history.
2. **`## Table of Contents`** — heading with nothing beneath it; it becomes the toc
   macro (minLevel 1 / maxLevel 3). `[storage-form]`
   `<ac:structured-macro ac:name="toc">` with those parameters.
3. **`## Sequence diagram`** — the macro + raw-source expand pair above. `[storage-form]`
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
   `0-9A-Za-z-_` alphabet does not; the safe-set is `"/"` exactly — parens ARE
   percent-encoded (`%28`/`%29` appear in known-good params; `"/()"` is
   byte-different). **Order matters:** percent-encode FIRST on the raw source; the
   final `data` is pure base64 with NO `%`. A param holding `%2B`/`%3D` means quote
   ran *after* base64 — the `%` is the order-bug signature, not an alphabet or padding
   issue. Never ship a body still holding a template marker (`PLACEHOLDER`, `TODO`) -
   a substitution step that silently didn't run publishes it. Storage-form macro:
   `<ac:structured-macro ac:name="plantumlcloud"><ac:parameter ac:name="filename"><name>.svg</ac:parameter><ac:parameter ac:name="data"><encoded></ac:parameter><ac:parameter ac:name="compressed">true</ac:parameter></ac:structured-macro>`.

   **Gated encoder — run this, don't hand-roll it.** It encodes AND gates; a push
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
   byte-for-byte — the inflated bytes after `unquote_to_bytes`, never the still-encoded
   ones (double-quoting makes a correct encoder "fail" and a wrong one look close).
   Check the reference can *discriminate*: if its source has no parens (or whatever
   character the safe-sets disagree on), byte-match proves nothing about that
   character — prefer a reference covering the ambiguous chars, else read the safe-set
   off the inflated bytes: the RESERVED characters appearing literally there are the
   safe-set, and only those (RFC 3986 unreserved `-._~` and alphanumerics stay literal
   under any `safe`, so they are not evidence; `+`/`=` never appear literally either).
   One exact match beats three plausible decoders.

4. **`## Request`**: `### Request header` (4-col field table) · `### Request body`
   (5-col field table) · `### Sample request` (wide json code block).
5. **`## Response`**: `### Response body` (5-col field table, with a `Mapping Logic`
   column) · `### Sample response` (wide json code block) · `### Error Mapping`
   (4-col table).
6. **`## Field to Field Mapping`** — one `### When calling <service> to <purpose>` per
   downstream call, with the link to that API's spec page **on its own line under the
   heading** (a link inside a heading lands in the anchor), then a 6-col table.

## Fixed table column sets (match exactly)

| Section | Headers |
| --- | --- |
| Request header | Field Name · M/O/C · Datatype · Description |
| Request body | Field Name · M/O/C · Datatype · Length · Description |
| Response body | Field Name · Data type · M/O/C · Mapping Logic · Description |
| Error Mapping | HTTP Code · Custom Status Code · Status Description · Scenario |
| Field to Field Mapping | Target Field Name · M/O/C · Data Type · Source Field · Mapping Logic · Remark |
| Change logs | Date · Update By · Description · Status |

`M/O/C` holds exactly `M`, `O`, or `C`. Field to Field Mapping is **input fields only** —
no `Input/Output` column and no separate output table.

These sets bind pages that follow the canonical order. A page family with its own
recorded skeleton (the BFF variant, in [page-family-variants](page-family-variants.md)) keeps **its** column set instead: matching a
live sibling outranks imposing this table, and a page that mixes the two is worse than
either. Decide by the anchor you decoded, never by preference.

## Publish checklist

1. Template anchor fetched in stored form; target skeleton matches it for heading
   levels, panel/macro wrappers, table attributes and column sets.
2. Dotted-path row coverage complete against the source structs (rule 1).
3. Samples are full payloads with internally consistent mocks (rule 2); opaque
   payloads single-row (rule 3); field names match serialization tags (rule 4).
4. Diagram = macro + byte-identical raw-source expand; no bare `@startuml` code blocks
   anywhere. `plantumlcloud` payloads: encoder proven against a known-good sibling's
   `data` param, and every generated `data` round-trips to a valid `@startuml…@enduml`
   source — before upload, not after a blank render (SKILL.md `content_file` sandbox:
   payloads staged inside the workspace).
5. Table column sets match the selected template anchor or the target family's
   recorded set.
6. Read-back after publish: stored body contains every macro wrapper and escaped source
   you intended (SKILL.md, publish-then-prove). If the read-back is compressed/truncated
   by the client, probe via bumped `version`, `text ~ "unique-string"` search, and the
   parent's children listing; render confirmation stays manual in a browser.
7. Change refs bidirectional: every `#changeN` in the body has a row in Change logs,
   and every declared marker appears in the body; no `~~` strikethrough survives, no
   old-round marker survives, and the round number is the page's previous count + 1.
