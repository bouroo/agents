---
name: confluence
description: "Operate Atlassian wikis end-to-end through either supported MCP server — the official Rovo remote MCP server (OAuth; read/search/graph surface) or mcp-atlassian (open-source; hosted or local stdio with an API token; full page CRUD): detect the live surface, resolve sites/shortlinks, search and read pages, author pages whose code blocks and diagrams render, update safely. Load before any Confluence create/update/get/delete."
---

# Confluence via MCP: Rovo and mcp-atlassian

Two servers, one doctrine. **mcp-atlassian** (open-source, self-hosted or hosted over streamable HTTP) carries full page CRUD, comments, labels, attachments, templates, restrictions. **Rovo MCP server** (Atlassian-hosted remote MCP, `https://mcp.atlassian.com/v1/mcp/authv2`, OAuth 2.1) is richest for reads and cross-product graphs. They complement: Rovo for graph/relationship reads, mcp-atlassian for anything that writes. Guides: <https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/> and <https://github.com/sooperset/mcp-atlassian>.

**Scope:** drive a configured wiki connection and author content that renders — not a Confluence user guide; targets are whatever the credentials reach.

## Detect the live surface before the first call

Read the connected tool names first; the registered server *name* is arbitrary, only the tool style identifies the server:

| Tool-name shape | Server | Addressing |
| --- | --- | --- |
| `getConfluencePage`, `searchConfluenceUsingCql`, `getAccessibleAtlassianResources`, `fetch`, `getTeamworkGraph*` (camelCase) | Rovo | every call takes a `cloudId`; sites discoverable |
| `confluence_*`, `jira_*` (snake_case) | mcp-atlassian | one site pinned at connect; no cloudId, title+space lookups |

Rovo write tools surface only when the OAuth grant carries write scopes and the account enables them — enumerate before promising a write. mcp-atlassian always carries full CRUD. Neither hot-loads: a server registered mid-session appears only after the session restarts.

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

Or declare it directly — first call triggers a one-time browser OAuth sign-in:

```json
{ "mcpServers": { "atlassian": { "url": "https://mcp.atlassian.com/v1/mcp/authv2" } } }
```

**mcp-atlassian, local stdio (fallback).** `uvx mcp-atlassian` with env credentials — Cloud: `CONFLUENCE_URL`, `CONFLUENCE_USERNAME` (account email), `CONFLUENCE_API_TOKEN`; Server/DC: `CONFLUENCE_URL` + `CONFLUENCE_PERSONAL_TOKEN`. Jira half optional (`JIRA_*` twins).

## Resolve before you act

1. Unknown site (Rovo only): `getAccessibleAtlassianResources` for reachable `cloudId`s; every other Rovo call takes one. mcp-atlassian sees exactly one site — no site step.
2. Shortlink (`.../wiki/x/<encoded>`)? Rovo: pass the encoded part as `pageId` to `getConfluencePage`; mcp-atlassian: pass the whole URL as `page_id` to `confluence_get_page` — no redirect chase either way.
3. Content discovery: Rovo `search` (natural language across products) first, `searchConfluenceUsingCql` when precision matters (`type = page AND ancestor = <id>`, `space.title ~ ...`); mcp-atlassian `confluence_search` takes simple terms (siteSearch, text fallback) or full CQL. Escape inner quotes with backslashes in CQL.
4. Structured reads: Rovo `getConfluencePage` (`contentFormat`: `markdown` cheap scans, `html` fidelity, `adf` programmatic), children via `getConfluencePageDescendants`, comments via the comment tools; mcp-atlassian `confluence_get_page` (numeric id, URL, or tiny link — or `title` + `space_key`; `convert_to_markdown: false` returns stored HTML), tree via `confluence_get_space_page_tree`.
5. One-shot metadata (Rovo only): `fetch` with an ARI (`ari:cloud:confluence:<cloudId>:page/<id>`), or `getTeamworkGraphContext` -> `getTeamworkGraphObject` for what links *to* the page (PRs, issues, deployments).

## Route operations by capability

Writes default to mcp-atlassian (fuller surface, first-class storage macros); Rovo writes only when it is the sole connected server and exposes them:

| Operation | Rovo | mcp-atlassian |
| --- | --- | --- |
| Sites / cloudIds | `getAccessibleAtlassianResources` | n/a — pinned at connect |
| Semantic / CQL search | `search` — `searchConfluenceUsingCql` | `confluence_search` |
| Read page | `getConfluencePage` (markdown/html/adf) | `confluence_get_page` (markdown; `convert_to_markdown: false` for stored HTML) |
| Space tree, children | `getConfluenceSpaces` — `getConfluencePageDescendants` — `getPagesInConfluenceSpace` | `confluence_get_space_page_tree` — `confluence_get_page_children` |
| Comments read | footer/inline/comment-children tools | `confluence_get_comments` — `confluence_get_inline_comments` |
| Comments write | (only if granted) | `confluence_add_comment` — `confluence_reply_to_comment` — `confluence_add_inline_comment` |
| Create / update page | (only if granted) | `confluence_create_page` — `confluence_update_page` — `confluence_update_page_section` |
| Move / copy / delete | (only if granted) | `confluence_move_page` — `confluence_copy_page` — `confluence_delete_page` |
| Labels, attachments | — | `confluence_get_labels`/`add_label`; get/upload/download/delete attachment tools |
| Templates | — | `confluence_list_page_templates` — `confluence_create_page_from_template` |
| Restrictions, views, history | — | restriction tools — `confluence_get_page_views` — `confluence_get_page_history` — `confluence_get_page_diff` |
| Cross-product graph (PRs/issues -> page) | `getTeamworkGraphContext` -> `getTeamworkGraphObject` | — |
| ARI one-shot metadata | `fetch` | — |
| User lookup | `lookupJiraAccountId` | `confluence_search_user` |

## Author pages that render

Each server round-trips a different format:

- **Rovo: `html` contentFormat** — round-trip safe and the only form the remote server accepts; legacy storage-format `<ac:structured-macro>` markup is rejected. Panels/status/expands/layouts use Confluence-HTML data-type nodes — follow the editor contract, never raw wiki markup.
- **mcp-atlassian: `content_format: storage`** (raw XHTML) for macro-bearing pages; `wiki` for quick structural pages; `markdown` (default) only for simple content. On update pass the current `title` (a different title renames) and set `version_comment` — versions bump server-side. `confluence_update_page_section` (heading_text + new_content) rewrites one section's body without touching the rest — lowest-blast-radius path for large pages.

Rules paid for by real breakage (both servers). Each trigger below names its failure mode; the symptom, cause, and defense live in
[references/writing-failure-modes.md](references/writing-failure-modes.md), and the
endpoint/spec page contract in [references/page-template.md](references/page-template.md):

- **Collapsed macro signatures are rendered form, never source** — a read returns
  `wide4000json{`, never the macro body; re-fence every sample you re-author.
- **Section updates are boundary-blind** past the headings the matcher recognizes: a miss
  on an unfamiliar page eats everything to EOF, so attempt the real edit first and diff
  after.
- **Diagrams default to PlantUML** through the instance's diagram macro; a bare
  `<pre><code>@startuml...` never renders. Encode `data` with the reference's gated
  encoder and get `GATE OK` **before** publishing — a blank diagram is invisible on
  re-read.
- **Native Mermaid macros are not installed everywhere**: mermaid fences never publish;
  translate to the family's PlantUML form and keep the raw Mermaid in the repo doc.
- **Endpoint/spec pages** follow a fixed template: canonical document order,
  content-quality rules, fixed column sets, per-family variants. Decode a live sibling
  first and match its family.
- **An update must be visible in the page**, not only in version history: baseline diff,
  `C#` markers, a Change Log table, then prove refs bidirectional after publish.
- **Large inline bodies corrupt in transit**, not in the body: emit writes sequentially,
  one call per message, and ladder up to `content_file` staged inside the workspace.
- **Body reads that collapse to `<<ccr:…>>` pointers** are deterministic per (page,
  format): cap the retries, then fall back to diff, title-scoped search, version bump,
  children listing. Never hand-reconstruct a body from excerpts or memory.

**Publish-then-prove.** After any write, re-fetch and confirm the stored body contains
what you intended (macro wrappers present, sources escaped): Rovo
`getConfluencePage(contentFormat="html")`, mcp-atlassian
`confluence_get_page(convert_to_markdown: false)`. A narrated success without the
read-back is theater — and so is a read-back the transport collapses to `<<ccr:…>>` refs.
Probe descending when the read-back is truncated, collapsed, or summarized, and say a
diagram paints only when a browser showed it.

## Safety

Creating/updating/deleting pages is a hard-to-undo external write: hold the `AUTH:`/`PENDING:` gates ([craft](../quality/SKILL.md)) — quote authorization for the specific target, emit `PENDING:` when unsure. Deletion (`confluence_delete_page`) has no MCP undo — recovery is UI-only and retention-bound; on a permission error, **repurpose** the page (rename + blank body + pointer note) and flag it for manual cleanup.
