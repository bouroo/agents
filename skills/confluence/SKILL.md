---
name: confluence
description: "Operate Atlassian wikis end-to-end through either supported MCP server - the official Rovo remote MCP server (OAuth; read/search/graph surface) or mcp-atlassian (open-source; hosted or local stdio with an API token; full page CRUD): detect the live surface, resolve sites/shortlinks, search and read pages, author pages whose code blocks and diagrams render, update safely. Load before any Confluence create/update/get/delete."
---

# Confluence via MCP: Rovo and mcp-atlassian

Two servers, one doctrine. **mcp-atlassian** (open-source, self-hosted or hosted over streamable HTTP) carries full page CRUD, comments, labels, attachments, templates, restrictions. **Rovo MCP server** (Atlassian-hosted remote MCP, `https://mcp.atlassian.com/v1/mcp/authv2`, OAuth 2.1) is richest for reads and cross-product graphs. They complement: Rovo for graph/relationship reads, mcp-atlassian for anything that writes. Guides: <https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/> and <https://github.com/sooperset/mcp-atlassian>.

**Scope:** drive a configured wiki connection and author content that renders - not a Confluence user guide; targets are whatever the credentials reach.

## Detect the live surface before the first call

Read the connected tool names first; the registered server *name* is arbitrary, only the tool style identifies the server:

| Tool-name shape | Server | Addressing |
| --- | --- | --- |
| `getConfluencePage`, `searchConfluenceUsingCql`, `getAccessibleAtlassianResources`, `fetch`, `getTeamworkGraph*` (camelCase) | Rovo | every call takes a `cloudId`; sites discoverable |
| `confluence_*`, `jira_*` (snake_case) | mcp-atlassian | one site pinned at connect; no cloudId, title+space lookups |

Rovo write tools surface only when the OAuth grant carries write scopes and the account enables them - enumerate before promising a write. mcp-atlassian always carries full CRUD. Neither hot-loads: a server registered mid-session appears only after the session restarts.

## Connect and authenticate

Prefer what is already reachable. When both remote options are available, **default to the hosted mcp-atlassian endpoint** (one URL, full CRUD, no per-client OAuth) and add Rovo only for the graph/read surface the task needs. Fall back to local stdio only when neither remote endpoint is reachable.

**mcp-atlassian, hosted (default).** Register the streamable-HTTP endpoint and follow the instance's docs for its auth header (Cloud = Atlassian API token, Server/DC = PAT; e.g. <https://mcp-atlassian.soomiles.com/docs>):

```json
{ "mcpServers": { "mcp-atlassian": { "url": "https://mcp-atlassian.soomiles.com/mcp" } } }
```

**Rovo (add for reads/graph).** Register the endpoint as an HTTP MCP server in any MCP-compatible client; the hands-off path is Atlassian's self-setup prompt, verbatim:

```text
Set up Atlassian Rovo MCP for this agent using the official setup guide at
https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/
and the MCP server URL https://mcp.atlassian.com/v1/mcp/authv2.
Then start the Atlassian MCP authentication flow so I can sign in.
```

Or declare it directly - first call triggers a one-time browser OAuth sign-in:

```json
{ "mcpServers": { "atlassian": { "url": "https://mcp.atlassian.com/v1/mcp/authv2" } } }
```

**mcp-atlassian, local stdio (fallback).** `uvx mcp-atlassian` with env credentials - Cloud: `CONFLUENCE_URL`, `CONFLUENCE_USERNAME` (account email), `CONFLUENCE_API_TOKEN`; Server/DC: `CONFLUENCE_URL` + `CONFLUENCE_PERSONAL_TOKEN`. Jira half optional (`JIRA_*` twins).

## Resolve before you act

1. Unknown site (Rovo only): `getAccessibleAtlassianResources` for reachable `cloudId`s; every other Rovo call takes one. mcp-atlassian sees exactly one site - no site step.
2. Shortlink (`.../wiki/x/<encoded>`)? Rovo: pass the encoded part as `pageId` to `getConfluencePage`; mcp-atlassian: pass the whole URL as `page_id` to `confluence_get_page` - no redirect chase either way.
3. Content discovery: Rovo `search` (natural language across products) first, `searchConfluenceUsingCql` when precision matters (`type = page AND ancestor = <id>`, `space.title ~ ...`); mcp-atlassian `confluence_search` takes simple terms (siteSearch, text fallback) or full CQL. Escape inner quotes with backslashes in CQL.
4. Structured reads: Rovo `getConfluencePage` (`contentFormat`: `markdown` cheap scans, `html` fidelity, `adf` programmatic), children via `getConfluencePageDescendants`, comments via the comment tools; mcp-atlassian `confluence_get_page` (numeric id, URL, or tiny link - or `title` + `space_key`; `convert_to_markdown: false` returns stored HTML), tree via `confluence_get_space_page_tree`.
5. One-shot metadata (Rovo only): `fetch` with an ARI (`ari:cloud:confluence:<cloudId>:page/<id>`), or `getTeamworkGraphContext` -> `getTeamworkGraphObject` for what links *to* the page (PRs, issues, deployments).

## Route operations by capability

Writes default to mcp-atlassian (fuller surface, first-class storage macros); Rovo writes only when it is the sole connected server and exposes them:

| Operation | Rovo | mcp-atlassian |
| --- | --- | --- |
| Sites / cloudIds | `getAccessibleAtlassianResources` | n/a - pinned at connect |
| Semantic / CQL search | `search` - `searchConfluenceUsingCql` | `confluence_search` |
| Read page | `getConfluencePage` (markdown/html/adf) | `confluence_get_page` (markdown; `convert_to_markdown: false` for stored HTML) |
| Space tree, children | `getConfluenceSpaces` - `getConfluencePageDescendants` - `getPagesInConfluenceSpace` | `confluence_get_space_page_tree` - `confluence_get_page_children` |
| Comments read | footer/inline/comment-children tools | `confluence_get_comments` - `confluence_get_inline_comments` |
| Comments write | (only if granted) | `confluence_add_comment` - `confluence_reply_to_comment` - `confluence_add_inline_comment` |
| Create / update page | (only if granted) | `confluence_create_page` - `confluence_update_page` - `confluence_update_page_section` |
| Move / copy / delete | (only if granted) | `confluence_move_page` - `confluence_copy_page` - `confluence_delete_page` |
| Labels, attachments | - | `confluence_get_labels`/`add_label`; get/upload/download/delete attachment tools |
| Templates | - | `confluence_list_page_templates` - `confluence_create_page_from_template` |
| Restrictions, views, history | - | restriction tools - `confluence_get_page_views` - `confluence_get_page_history` - `confluence_get_page_diff` |
| Cross-product graph (PRs/issues -> page) | `getTeamworkGraphContext` -> `getTeamworkGraphObject` | - |
| ARI one-shot metadata | `fetch` | - |
| User lookup | `lookupJiraAccountId` | `confluence_search_user` |

## Author pages that render

Each server round-trips a different format:

- **Rovo: `html` contentFormat** - round-trip safe and the only form the remote server accepts; legacy storage-format `<ac:structured-macro>` markup is rejected. Panels/status/expands/layouts use Confluence-HTML data-type nodes - follow the editor contract, never raw wiki markup.
- **mcp-atlassian: `content_format: storage`** (raw XHTML) for macro-bearing pages; `wiki` for quick structural pages; `markdown` (default) only for simple content. On update pass the current `title` (a different title renames) and set `version_comment` - versions bump server-side. `confluence_update_page_section` (heading_text + new_content) rewrites one section's body without touching the rest - lowest-blast-radius path for large pages.

Rules paid for by real breakage (both servers):

- Code blocks: html `<pre><code class="language-<lang>">source</code></pre>` with `& < >` HTML-escaped, or the matching storage-format macro on mcp-atlassian.
- **Never copy a collapsed macro signature back as markdown.** Page reads render code/diagram macros as one signature line - `wide4000json{`, `textwide4000true@startuml`, `bottomname.svg<base64>` - the RENDERED form, not source. When re-authoring a section, re-fence every sample (```lang fences - the converter rebuilds the macro); an unfenced signature line followed by newline-JSON merges into one text paragraph on conversion. Escaping differs by surface: table cells take a single `\_` / `\*` (what the original authoring stored), code-fence bodies take plain characters, and a doubled `\\_` renders a visible backslash - never double-escape.
- **Section updates are boundary-blind past the headings the matcher recognizes.** `update_page_section` replaces from heading_text to the next heading the tool can see; on pages whose deeper headings (h5/h6, authoring-dependent) it cannot match, the replacement swallows EVERYTHING to EOF. On an unfamiliar page, attempt the real section edit first - a heading miss is a clean error that writes nothing - and always run `get_page_diff` (n-1)->n after a section write; restore from the diff's removed lines or `get_page_history(version=N, convert_to_markdown=false)` when boundaries were eaten.
- **Diagrams default to PlantUML** via the instance's diagram macro; a bare `<pre><code>@startuml...` NEVER renders (literal text - the one failure invisible on re-read). Rovo: mirror the sibling's Confluence-HTML macro node; mcp-atlassian: author the storage-format macro directly ([references/page-template.md](references/page-template.md) `[storage-form]` snippets apply verbatim). Encode `data` with the reference's **gated encoder** (quote source `safe="/"` -> raw deflate 6 -> base64; pure base64, no `%`) and get its `GATE OK` line **before** publishing - a blank diagram is invisible in the stored body, so the gate is the only pre-push defense. Mirror every diagram's raw source in a collapsed expand so it survives macro outages.
- Native Mermaid macros are not installed everywhere and third-party ones store out-of-band attachments the API cannot create: Mermaid is manual-via-UI only.
- **Endpoint/spec pages** follow a fixed template - canonical document order, content-quality rules (dotted-path field rows, full-payload samples with consistent mocks, serialization-tag field names), fixed column sets, per-family variants: [references/page-template.md](references/page-template.md). Decode a live sibling page first and match its family.
- **Update-change visibility:** a page *update* must make what changed visible in the page itself, not only in version history. Fetch the pre-change baseline - mcp-atlassian `confluence_get_page_history(page_id, version=N, convert_to_markdown=false)` returns version N's full stored body (Rovo: `getConfluencePageDiff`) - walking N backwards until the version's timestamp precedes the current effort, and diff baseline vs new body. Mark every added/changed point with in-page refs: rebuilt tables carry a `Change` column whose New/Modified/Renamed cells hold `C#` (bold the changed field name); removed content ships as `Removed` rows in a `Change Log` table (h3 near the changed sections: `Change # | Date | Field/Section | Change Type | Description`, per-page `C1..Cn`); prose-level shifts take a page-level row (Field `—`). After publish, prove refs bidirectional: every `C#` in the body exists in the Change Log and vice versa, under documented relaxations (`—` page-level rows, `X[].*` aggregate-prefix rows, `Removed` rows anchored only in the baseline). Snippets and gate wording: [references/page-template.md](references/page-template.md) `[changelog]`.
- **Large pages / payload corruption:** big inline bodies fail two ways - gateways reject outright (502/reset; retry after ~20 s), or the MCP client→server hop **silently corrupts** the call before validation (`InputValidationError ... could not be parsed as JSON`, reporting ~3× the bytes you sent - a transport defect, not an authoring mistake; do not reformat, change the transport). Emit writes **sequentially, one call per message** - parallel writes in one block fused into a single garbled ~100 KB JSON once (rejected pre-write, but only after dead attempts); since solo 15-19 KB writes went through, batching was the trigger, not size. Ladder: smaller `confluence_update_page_section` (a few KB) -> full-body `confluence_update_page` with `content_file` (reads from disk, immune to inline corruption). `content_file` paths are sandboxed to the server's working directory - a `/tmp` payload is rejected as path traversal; stage payloads inside the workspace (e.g. `.agents/<task>/`) and delete them after.
- **Mermaid sources:** mermaid fences never publish - translate each diagram to the family's PlantUML form ([references/page-template.md](references/page-template.md) has the element mapping and the `plantumlcloud` `data` recipe). Keep the raw Mermaid in the repo doc; only the translated PlantUML ships.
- **When body reads collapse to pointers (`<<ccr:…>>`):** the ref is a cached *deterministic* result per (page, format) - identical `get_page` retries return the identical ref, so refetching the same page more than once per variable change is a loop (cap: two identical retries). Fallbacks, strongest first: `confluence_get_page_diff` between **adjacent recent versions** (intermittently returns the full unified diff; after your own section edit it is a **recovery oracle** showing exactly what was replaced); `confluence_search` `siteSearch ~ "<distinctive phrase>"` **scoped by `title = "<page>"`** (excerpts blend fragments across sections and pages, so attribute text only via a title-scoped probe); note CQL `ancestor = X` matches **descendants only** - the parent itself needs `title =`. **While reads are down:** replace only *schema-bounded* sections (index catalogs, lineage tables - fully recomputable from code/DDL; their failure mode is a clean heading-miss error and the post-edit diff exposes clobbered content); never append to or rewrite changelogs and field dictionaries (unseen rows would be destroyed); never hand-reconstruct a body from excerpts, memory, or inference - that is fabrication and destroys the unseen majority. Park remaining stale cells in a dated footer comment (`confluence_add_comment`) as the fix checklist, and PENDING it in the report.

**Publish-then-prove.** After any write, re-fetch and confirm the stored body contains what you intended (macro wrappers present, sources escaped): Rovo `getConfluencePage(contentFormat="html")`, mcp-atlassian `confluence_get_page(convert_to_markdown: false)`. A narrated success without the read-back is theater - and so is a read-back the transport collapses to `<<ccr:…>>` refs, which proves nothing either way. Front-load what no probe can catch: the pre-push `GATE OK` is the only defense against an invisible diagram encoding defect - run it, don't claim it. When the read-back is truncated, collapsed, or summarized, probe in descending strength: `confluence_get_page_diff` between the previous and new version (a non-empty diff plus the bumped `version` in the write response is the server-side witness, even when the diff body collapses); `confluence_search` `text ~ "<string unique to the new body>"` (search indexes stored body text, but fresh pages lag minutes and macro **parameters** are not indexed, so a miss proves nothing about a `data` param); the update response's bumped `version`; the parent's children listing. For a body pushed via `content_file`, asserting distinctive strings against the pushed file (new data param present, old absent) proves what you *sent*, not what the server stored - keep the version bump as the server-side witness. Whether a diagram actually *paints* is visible only in a browser: say so instead of claiming render success, and never trust another page's encoding as "known-good" unless someone saw that page render.

## Safety

Creating/updating/deleting pages is a hard-to-undo external write: hold the `AUTH:`/`PENDING:` gates ([craft](../craft/SKILL.md)) - quote authorization for the specific target, emit `PENDING:` when unsure. Deletion (`confluence_delete_page`) has no MCP undo - recovery is UI-only and retention-bound; on a permission error, **repurpose** the page (rename + blank body + pointer note) and flag it for manual cleanup.
