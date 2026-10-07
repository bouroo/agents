# Writing failure modes

Each mode below is a real breakage with its symptom, cause, and defense. SKILL.md
carries the one-line trigger; the evidence behind it lives here.

## Collapsed macro signatures are rendered form, never source

Page reads render code and diagram macros as one signature line — `wide4000json{`,
`textwide4000true@startuml`, `bottomname.svg<base64>` — the RENDERED form, not source.

- When re-authoring a section, re-fence every sample (```lang fences — the converter
  rebuilds the macro); an unfenced signature line followed by newline-JSON merges into
  one text paragraph on conversion.
- Escaping differs by surface: table cells take a single `\_` / `\*` (what the original
  authoring stored), code-fence bodies take plain characters, and a doubled `\\_` renders
  a visible backslash — never double-escape.
- Code blocks are html `<pre><code class="language-<lang>">source</code></pre>` with
  `& < >` HTML-escaped, or the matching storage-format macro on mcp-atlassian.

## Section updates are boundary-blind past recognized headings

`update_page_section` replaces from `heading_text` to the next heading the tool can see.
On pages whose deeper headings (h5/h6, authoring-dependent) it cannot match, the
replacement swallows EVERYTHING to EOF.

Defense: on an unfamiliar page, attempt the real section edit first — a heading miss is a
clean error that writes nothing — and always run `get_page_diff` (n-1)->n after a section
write; restore from the diff's removed lines or
`get_page_history(version=N, convert_to_markdown=false)` when boundaries were eaten.

## Diagrams render only through the instance's PlantUML macro

A bare `<pre><code>@startuml...` NEVER renders — literal text, the one failure invisible
on re-read.

- Rovo: mirror the sibling's Confluence-HTML macro node.
- mcp-atlassian: author the storage-format macro directly; the `[storage-form]` snippets
  in [page-template.md](page-template.md) apply verbatim.
- Encode `data` with that reference's **gated encoder** (quote source `safe="/"` → raw
  deflate 6 → base64; pure base64, no `%`) and get its `GATE OK` line **before**
  publishing — a blank diagram is invisible in the stored body, so the gate is the only
  pre-push defense.
- Mirror every diagram's raw source in a collapsed expand so it survives macro outages.

Native Mermaid macros are not installed everywhere and third-party ones store
out-of-band attachments the API cannot create: Mermaid is manual-via-UI only, and mermaid
fences never publish — translate each diagram to the family's PlantUML form
([page-template.md](page-template.md) has the element mapping and the `plantumlcloud`
`data` recipe). Keep the raw Mermaid in the repo doc; only the translated PlantUML ships.

## An update must be visible in the page, not only in version history

Fetch the pre-change baseline first: mcp-atlassian
`confluence_get_page_history(page_id, version=N, convert_to_markdown=false)` returns
version N's full stored body (Rovo: `getConfluencePageDiff`) — walking N backwards until
the version's timestamp precedes the current effort — then diff baseline vs new body.

Mark every added/changed point with in-page refs: rebuilt tables carry a `Change` column
whose New/Modified/Renamed cells hold `C#` (bold the changed field name); removed content
ships as `Removed` rows in a `Change Log` table (h3 near the changed sections:
`Change # | Date | Field/Section | Change Type | Description`, per-page `C1..Cn`);
prose-level shifts take a page-level row (Field `—`). After publish, prove refs
bidirectional: every `C#` in the body exists in the Change Log and vice versa, under
documented relaxations (`—` page-level rows, `X[].*` aggregate-prefix rows, `Removed` rows
anchored only in the baseline). Snippets and gate wording: [page-template.md](page-template.md)
`[changelog]`.

## Large pages corrupt in transit, not in the body

Big inline bodies fail two ways: gateways reject outright (502/reset; retry after ~20 s),
or the MCP client→server hop **silently corrupts** the call before validation
(`InputValidationError ... could not be parsed as JSON`, reporting ~3× the bytes you sent —
a transport defect, not an authoring mistake; do not reformat, change the transport).

- Emit writes **sequentially, one call per message** — parallel writes in one block fused
  into a single garbled ~100 KB JSON once (rejected pre-write, but only after dead
  attempts); since solo 15-19 KB writes went through, batching was the trigger, not size.
- Ladder: smaller `confluence_update_page_section` (a few KB) → full-body
  `confluence_update_page` with `content_file` (reads from disk, immune to inline
  corruption).
- `content_file` paths are sandboxed to the server's working directory — a `/tmp` payload
  is rejected as path traversal; stage payloads inside the workspace (e.g.
  `.agents/<task>/`) and delete them after.

## Body reads that collapse to pointers (`<<ccr:…>>`)

The ref is a cached *deterministic* result per (page, format) — identical `get_page`
retries return the identical ref, so refetching the same page more than once per variable
change is a loop (cap: two identical retries).

Fallbacks, strongest first:

1. `confluence_get_page_diff` between **adjacent recent versions** (intermittently returns
   the full unified diff; after your own section edit it is a **recovery oracle** showing
   exactly what was replaced).
2. `confluence_search` `siteSearch ~ "<distinctive phrase>"` **scoped by
   `title = "<page>"`** (excerpts blend fragments across sections and pages, so attribute
   text only via a title-scoped probe). Note CQL `ancestor = X` matches **descendants
   only** — the parent itself needs `title =`.

**While reads are down:** replace only *schema-bounded* sections (index catalogs, lineage
tables — fully recomputable from code/DDL; their failure mode is a clean heading-miss
error and the post-edit diff exposes clobbered content); never append to or rewrite
changelogs and field dictionaries (unseen rows would be destroyed); never hand-reconstruct
a body from excerpts, memory, or inference — that is fabrication and destroys the unseen
majority. Park remaining stale cells in a dated footer comment (`confluence_add_comment`)
as the fix checklist, and PENDING it in the report.

## Proving a write landed

A narrated success without the read-back is theater — and so is a read-back the transport
collapses to `<<ccr:…>>` refs, which proves nothing either way. Front-load what no probe
can catch: the pre-push `GATE OK` is the only defense against an invisible diagram
encoding defect — run it, don't claim it.

When the read-back is truncated, collapsed, or summarized, probe in descending strength:

1. `confluence_get_page_diff` between the previous and new version (a non-empty diff plus
   the bumped `version` in the write response is the server-side witness, even when the
   diff body collapses).
2. `confluence_search` `text ~ "<string unique to the new body>"` (search indexes stored
   body text, but fresh pages lag minutes and macro **parameters** are not indexed, so a
   miss proves nothing about a `data` param).
3. The update response's bumped `version`.
4. The parent's children listing.

For a body pushed via `content_file`, asserting distinctive strings against the pushed
file (new data param present, old absent) proves what you *sent*, not what the server
stored — keep the version bump as the server-side witness.

Whether a diagram actually *paints* is visible only in a browser: say so instead of
claiming render success, and never trust another page's encoding as "known-good" unless
someone saw that page render.
