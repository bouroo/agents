---
name: confluence
description: "Operate the official Atlassian remote MCP server (OAuth HTTP) end-to-end, with a stdio bridge fallback. Use when the MCP tools do not surface mid-session (complete OAuth + restart), to resolve shortlinks, and to author pages so code blocks and PlantUML/Mermaid diagrams render (native storage format, never markdown). Load before any create/update/get/delete of a Confluence page."
---

# Confluence (Atlassian remote MCP) Operations

Durable operating doctrine for the **official Atlassian remote MCP server** (`https://mcp.atlassian.com/v1/mcp/authv2`, HTTP/OAuth2.1): the Atlassian-hosted build of the open-source `mcp-atlassian` server, exposing the same `confluence_*` tool surface. Captures every trap hit in real wiki work so it is never re-derived. Detail lives in `references/`; load only what the task needs.

> **Scope.** This skill is about *operating* the configured MCP server and *authoring* content that renders. It is not a Confluence user guide. Target instance, space, and credentials are read from the host's settings, never hardcoded here.

## 0. Prime Directive

**Use the configured MCP, not curl/REST; and prove renders by decoding the stored body, never by trusting `body.view`.** The REST `body.view` returns a JS stub for macro-rendered content (code panels, PlantUML); it looks empty/broken even when the page is correct. Proof = decode the `plantumlcloud` `data` param back to source and render-inspect it.

## 1. Surface the tools before you use them

**Primary: the official Atlassian remote MCP server** (`https://mcp.atlassian.com/v1/mcp/authv2`, HTTP transport, OAuth2.1). It is the Atlassian-hosted build of the open-source `mcp-atlassian` server, so it exposes the same `confluence_*` tool surface documented here. Config:

```json
{ "mcpServers": { "atlassian": { "url": "https://mcp.atlassian.com/v1/mcp/authv2" } } }
```

Register at user scope: `claude mcp add --transport http atlassian https://mcp.atlassian.com/v1/mcp/authv2`. The first call triggers a one-time browser OAuth2.1 login.

**MCP tools connect only at session startup.** A server registered mid-session is not hot-loaded, and OAuth completion lands after the session began, so `confluence_*` tools surface only in sessions **started after** the server connects. When the tools are not surfaced: complete OAuth once, then **restart the host/session**. Full detail in [access](references/access.md).

**Fallback: the [stdio bridge](mcp_bridge.py)** (`uvx mcp-atlassian` + username/API token) drives the *same* server/tools over stdio when OAuth is unavailable (headless/CI) or a tool won't surface mid-session. It is the same server, transport-bridged: `python3 ./mcp_bridge.py schema confluence_create_page`.

## 2. Author in storage format, never markdown

Markdown is a rendering trap on Confluence. The contract is the native **storage format** (XHTML + macros). Code blocks use `<ac:structured-macro ac:name="code">`; PlantUML uses `plantumlcloud`. Author or update with `content_format: storage` (or write to a `content_file`). See [storage-format](references/storage-format.md).

## 3. Diagrams that render (PlantUML is the default; Mermaid only via UI)

**Default diagrams to PlantUML.** On instances that render via the mxgraph **`plantumlcloud`** plugin, diagram source is stored **inline, compressed** in the `data` parameter: the only diagram tech reproducible from page storage XML. **Default every diagram to PlantUML** unless a working native mermaid macro is proven on the instance. The endpoint-page template ([page-template](references/page-template.md)) uses it.

**PlantUML:**

- Sequence-diagram messages split across a **real newline** are a syntax error. Keep each message on one line; a literal `\n` inside a message is a visual break.
- **Do not trust a local `-check`** that reports `Error line 1` in some Java versions; it can be a false negative. Render + inspect the SVG is the only proof.
- The verified compression algorithm (encode + decode) and the `\n` trap are in [plantuml](references/plantuml.md). Publishing a diagram that produces no/trivial SVG or an error-marker image renders broken on the page.
- **Every diagram ships with its raw source in a collapsed expand.** A rendered `plantumlcloud` alone leaves the source unrecoverable from the page; mirror [page-template](references/page-template.md): render the macro, then immediately follow it with the PlantUML source in an `expand > code` block titled e.g. "Raw sequence diagram source". Emit the SAME source in both (decode the macro's `data` param to get the source for the expand). Forms:
  - **Remote MCP (`html`):** `<details><summary>Raw sequence diagram source</summary><pre><code class="language-none">SOURCE</code></pre></details>`. HTML-escape the source (`&` `<` `>` → `&amp;` `&lt;` `&gt;`; PlantUML arrows `->`/`-->` contain `>`).
  - **stdio bridge (`storage`):** `expand_macro("Raw sequence diagram source", code_macro(source, language="none"))`.

**Mermaid confirm before authoring from storage XML:**

- The native `ac:name="mermaid"` macro is **not installed on every instance** -> renders **"error loading"** where absent (observed after publishing a page whose only diagram was the native `mermaid`).
- The third-party `ac:name="mermaid-cloud"` app **does** render, but stores its source **out-of-band as a rendered image attachment** (macro body is empty; only `<filename>` + `<revision>`). It **cannot** be created by writing page XML; it must be inserted via the Confluence UI. Treat mermaid as manual-only; for any programmatic diagram, use PlantUML.
- Details (native vs `mermaid-cloud`, newline rule, why inline authoring fails) in [mermaid](references/mermaid.md).

## 4. Page lifecycle & safety

Creating/updating a Confluence page is a hard-to-undo external write. Confirm the target page id + intent before publishing unless durably authorized ([code-craft](../code-craft/SKILL.md) `AUTH:` gate). If `confluence_delete_page` returns `PermissionException`, the token lacks trash scope: **repurpose** the page (update title + body) rather than leaving an orphan; flag it for manual deletion.

## 5. Shortlinks & key tools

- Shortlinks (`/x/<id>`) resolve to a page id. Under the remote MCP (OAuth), pass the encoded part directly as `pageId` to `mcp__atlassian__getConfluencePage` (it accepts tiny link IDs); no need to follow a redirect. Under the stdio fallback, `curl -u "$USER:$TOK" "https://<site>/wiki/rest/api/shortlink/<id>"` works (see [access](references/access.md)).
- Schemas (stdio bridge): `python3 ./mcp_bridge.py schema confluence_create_page`.
- Key tools on the **remote MCP** (confirmed by real use, `mcp__atlassian__*` namespace):
  - `createConfluencePage(cloudId, spaceId, title, body, contentFormat, parentId, status)` returns the new page `id`.
  - `updateConfluencePage(cloudId, pageId, title, body, contentFormat, status, versionMessage)` requires the current page id; bump the title/body intentionally to drive the version (this client doesn't expose an explicit `currentVersion` param; the server resolves it).
  - `getConfluencePage(cloudId, pageId, contentFormat)` `pageId` accepts a tiny link ID (the encoded part of `/wiki/x/<URL>`).
  - `searchConfluenceUsingCql(cloudId, cql, limit)` CQL with fields like `type = page AND ancestor = <id>`.
  - `getConfluenceSpaces(cloudId, limit)` / `getPagesInConfluenceSpace(cloudId, ...)`.
  - `fetch(cloudId, id)` resolves an ARI (`ari:cloud:confluence:<cloudId>:page/<id>`) for one-shot metadata lookups.
- Content format on the remote MCP is **`html`** with `data-type` attributes (panels, status, layouts, code via `<pre><code class="language-...">`, macros via `data-extension-type="com.atlassian.confluence.macro.core"`). **Do NOT** use old storage-XML `<ac:structured-macro>` here; it is rejected. See [storage-format](references/storage-format.md).
- The stdio bridge (`uvx mcp-atlassian`) tool family is `confluence_get_page`, `confluence_create_page`, etc.; different surface, same server.

## 5a. Large-page resilience (real-world)

The remote MCP gateway can throw transient transport errors (`502`, or HTTP `Cannot assign requested address` on the upstream) on large write payloads. Reliable pattern for a large page:

1. `createConfluencePage` with a **minimal placeholder body** (one short paragraph) and the real title + `parentId`. This lands the page with a fresh id.
2. `updateConfluencePage` with the full body in a follow-up call.

Both calls can 502/reset independently; a short pause (`sleep ~20s`) between retries and the create-then-update split has, in practice, eliminated write failures. The minimal create is cheap, so retry the create itself once or twice before splitting.

## References

- [access.md](references/access.md) official remote MCP (OAuth) connection, fix-when-not-surfaced, the stdio fallback bridge, shortlinks, delete-permission gotcha.
- [storage-format.md](references/storage-format.md) macro templates, markdown-to-storage conversion, validation loop.
- [plantuml.md](references/plantuml.md) the verified compression algorithm (encode + decode) and the newline trap.
- [mermaid.md](references/mermaid.md) the native mermaid macro, the mirror-image newline rule, and the byte-identical round-trip proof.
- [page-template.md](references/page-template.md) + [page_template.py](page_template.py) the endpoint-page template generator (section order, fixed table column sets, highlighted metadata, code macros). Load + run when a new page must match that example. It also carries **mandatory content-quality rules** (every nested field as its own dotted-path row; full-field samples with internally consistent mock data; serialization-tag-verified field names) and an **instance-variant section** (a tenant's "BFF API Specification" page family, incl. the plain-code-block sequence-diagram form); match siblings when extending an existing page family.
- [code-craft](../code-craft/SKILL.md) the `AUTH:` gate for external writes.
