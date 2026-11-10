# Instance variants: page families with their own skeleton

> Load on demand from [confluence](../SKILL.md) or [page-template](page-template.md): the recorded skeletons of page families that follow a different but self-consistent layout, on the Confluence-HTML surface and on the storage-format surface. Read it when the target page belongs to such a family rather than to the canonical order, and match the siblings instead of the template.

## Instance variant: "BFF API Specification" page families

These spaces follow a **different but self-consistent layout** — match the siblings
instead of the canonical order. Two surface records; where they diverge, match the
surface you publish through.

**Rovo (Confluence-HTML) surface:**

- **H2 section headings** (not H1): `Change logs`, `Sequence diagram`, `Logic`,
  `API Details`, `Status Code`, `Field to Field Mapping`, each preceded by `<hr>`.
- Opens with an info panel (`<div data-type="panel-info">`) titled "**BFF API
  Specification:** \<service\> — \<METHOD\> \<path\>" plus a one-paragraph summary.
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
  Scenario, including a passthrough row (`- | — | passthrough | …`) for inherited
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
  Source | Mapping Logic | Remark` with `I`/`O` in the first cell — one table per
  numbered H3.

