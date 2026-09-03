---
name: confluence
description: "Operate Atlassian wikis end-to-end through either supported MCP server - the official Rovo remote MCP server (OAuth; read/search/graph surface) or mcp-atlassian (open-source; hosted e.g. mcp-atlassian.soomiles.com or local stdio with an API token; full page CRUD): detect the live surface, resolve sites/shortlinks, search and read pages, author pages whose code blocks and diagrams render, update safely. Load before any Confluence create/update/get/delete."
---

# Confluence via MCP: Rovo and mcp-atlassian

Two servers, one operating doctrine. **Rovo MCP server** - Atlassian-hosted remote MCP (`https://mcp.atlassian.com/v1/mcp/authv2`, HTTP transport, OAuth 2.1) - is richest for reads and cross-product graphs. **mcp-atlassian** - the open-source Atlassian MCP server, self-hosted or hosted (e.g. `https://mcp-atlassian.soomiles.com/mcp`, streamable HTTP) - carries full page CRUD, comments, labels, attachments, templates, and restrictions. Connect either or both; when both are live they complement, neither subsumes: Rovo for graph/relationship reads, mcp-atlassian for anything that writes. Official Rovo guide: <https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/>; mcp-atlassian upstream: <https://github.com/sooperset/mcp-atlassian>.

> **Scope.** How to drive a configured wiki connection and author content that renders. Not a Confluence user guide; targets/sites are whatever the connection's credentials can reach.

## Detect the live surface before the first call

Read the connected tool names first, then route by shape - the registered server *name* is arbitrary, only the tool style identifies the server:

| Tool-name shape | Server | Addressing |
| --- | --- | --- |
| `getConfluencePage`, `searchConfluenceUsingCql`, `getAccessibleAtlassianResources`, `fetch`, `getTeamworkGraph*` (camelCase) | Rovo | every call takes a `cloudId`; sites discoverable |
| `confluence_*`, `jira_*` (snake_case) | mcp-atlassian | one site pinned at connect time; no cloudId, title+space lookups |

Rovo's Confluence write tools surface only when the OAuth grant carries write scopes and the account has them enabled - enumerate before promising a write. mcp-atlassian always carries full CRUD. Neither hot-loads: a server registered mid-session appears only after the session restarts (finish OAuth once, then restart the session/headless run).

## Connect and authenticate

**Rovo.** Register the endpoint as an HTTP MCP server in any MCP-compatible client - every major agent documents a one-line setup for exactly this URL; hands-off path is Atlassian's own self-setup prompt, pasted verbatim:

```text
Set up Atlassian Rovo MCP for this agent using the official setup guide at
https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/
and the MCP server URL https://mcp.atlassian.com/v1/mcp/authv2.
Then start the Atlassian MCP authentication flow so I can sign in.
```

Or declare it directly:

```json
{ "mcpServers": { "atlassian": { "url": "https://mcp.atlassian.com/v1/mcp/authv2" } } }
```

First call triggers a one-time browser OAuth sign-in.

**mcp-atlassian, hosted** (here: mcp-atlassian.soomiles.com). Register the streamable-HTTP endpoint and follow the instance's docs for its auth header (<https://mcp-atlassian.soomiles.com/docs>; Cloud = Atlassian API token, Server/DC = PAT):

```json
{ "mcpServers": { "mcp-atlassian": { "url": "https://mcp-atlassian.soomiles.com/mcp" } } }
```

**mcp-atlassian, local stdio.** `uvx mcp-atlassian` with env credentials - Cloud: `CONFLUENCE_URL`, `CONFLUENCE_USERNAME` (account email), `CONFLUENCE_API_TOKEN`; Server/DC: `CONFLUENCE_URL` + `CONFLUENCE_PERSONAL_TOKEN`. The Jira half is optional (`JIRA_*` twins of the same vars). Prefer the hosted/remote endpoints over local bridges whenever possible.

## Resolve before you act

1. Unknown site (Rovo only): `getAccessibleAtlassianResources` for reachable `cloudId`s; every other Rovo call takes one. mcp-atlassian needs no site step - it sees exactly one site.
2. Shortlink (`.../wiki/x/<encoded>`)? Rovo: pass the encoded part directly as `pageId` to `getConfluencePage` (accepts tiny link IDs). mcp-atlassian: pass the whole shortlink URL as `page_id` to `confluence_get_page` - no redirect chase either way.
3. Content discovery: Rovo `search` (natural language across products) first, `searchConfluenceUsingCql` when precision matters (`type = page AND ancestor = <id>`, `space.title ~ ...`, date/creator filters); mcp-atlassian `confluence_search` takes simple terms (siteSearch, text fallback) or full CQL. Escape inner quotes with backslashes in CQL.
4. Structured reads: Rovo `getConfluencePage` (`contentFormat`: `markdown` cheap scans, `html` fidelity, `adf` programmatic), children via `getConfluencePageDescendants`, footer/inline comments via the comment tools; mcp-atlassian `confluence_get_page` (by numeric id, full URL, or tiny link - or `title` + `space_key`; `convert_to_markdown: false` returns stored HTML), tree via `confluence_get_space_page_tree`.
5. One-shot metadata for any entity (Rovo only): `fetch` with an ARI (`ari:cloud:confluence:<cloudId>:page/<id>`), or `getTeamworkGraphContext` -> `getTeamworkGraphObject` when you need what links *to* the page (PRs, issues, deployments).

## Route operations by capability

When both servers are connected, route each operation to whoever actually carries it; writes default to mcp-atlassian (fuller surface, first-class storage macros), Rovo writes only when it is the sole connected server and its surface exposes them:

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

Writes go out in the format each server round-trips, and the two differ:

- **Rovo: `html` contentFormat** - round-trip safe, and it is what the remote server accepts; legacy storage-format `<ac:structured-macro>` markup is rejected here. Panels/status/expands/layouts use Confluence-HTML data-type nodes - follow the editor contract, never raw wiki markup.
- **mcp-atlassian: `content_format: storage`** (raw XHTML storage format) for macro-bearing pages - storage macros (`<ac:structured-macro>`) are first-class here; `wiki` markup for quick structural pages; plain `markdown` (the default) only for simple content. On update, pass the current `title` (a different title renames) and set `version_comment` - versions bump server-side. `confluence_update_page_section` (heading_text + new_content) rewrites one section's body without touching the rest - lowest-blast-radius path for large pages.

Rules paid for by real breakage (both servers):

- Code blocks: html `<pre><code class="language-<lang>">source</code></pre>` with `& < >` HTML-escaped, or the matching storage-format macro on mcp-atlassian.
- **Diagrams default to PlantUML** through the instance's diagram macro; a bare `<pre><code>@startuml...` NEVER renders as a diagram (it shows literal text - the one failure mode invisible when re-reading the body). On Rovo, mirror the sibling's Confluence-HTML macro node; on mcp-atlassian, author the storage-format macro directly ([references/page-template.md](references/page-template.md) `[storage-form]` snippets apply verbatim). Every published diagram ships with its raw source mirrored in a collapsed expand so it survives macro outages.
- Native Mermaid macros are not installed everywhere and third-party ones store out-of-band attachments the API cannot create: treat Mermaid as manual-via-UI only.
- **Endpoint/spec pages:** authoring them follows a fixed template - canonical document order, mandatory content-quality rules (dotted-path field rows, full-payload samples with consistent mocks, serialization-tag field names), fixed table column sets, and per-family variants: [references/page-template.md](references/page-template.md). Always decode a live sibling page first and match its family.
- **Large pages:** create with a minimal placeholder body plus real title/parent, then push the full body via a second update call (`content_file` accepts a filesystem path on mcp-atlassian). Gateway transport errors (502s/reset) hit big payloads; retry after ~20 s.

**Publish-then-prove:** after any write, re-fetch the page and confirm the stored body contains what you intended (macro wrappers present, sources escaped): Rovo `getConfluencePage(contentFormat="html")`, mcp-atlassian `confluence_get_page(convert_to_markdown: false)`. A narrated success without the read-back is theater.

## Safety

Creating/updating/deleting pages is a hard-to-undo external write: hold to the `AUTH:`/`PENDING:` gates ([craft](../craft/SKILL.md)) - quote authorization for the specific target, emit `PENDING:` when unsure. Deleting (`confluence_delete_page`) has no MCP undo path - recovery is UI-only and retention-bound; when deletion returns a permission error, **repurpose** the page (rename + blank body + pointer note) rather than leaving orphan content, and flag it for manual cleanup.
