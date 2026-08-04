---
name: confluence
description: Operate the Confluence/Jira mcp-atlassian server end-to-end. Use when the MCP tools don't surface mid-session (fix registration + stdio bridge), when resolving /x/ shortlinks, and when authoring Confluence pages so code blocks and PlantUML diagrams render correctly (native storage format, never markdown). Load before any create/update/get/delete of a Confluence page, or when macros/diagrams render wrong.
---

# Confluence (mcp-atlassian) Operations

Durable operating doctrine for the `mcp-atlassian` server against `TENANT.atlassian.net` (space `ClientInstance`). Captures every trap hit in the adapter-mbf-ais wiki work so it is never re-derived. Detail lives in `./references/`; load only what the task needs.

> **Scope.** This skill is about *operating* the configured MCP server and *authoring* Confluence content that renders. It is not a Confluence user guide.

## 0. Prime Directive

**Use the configured MCP, not curl/REST -- and prove renders by decoding the stored body, never by trusting `body.view`.** The REST `body.view` returns a JS stub for macro-rendered content (code panels, PlantUML); it looks empty/broken even when the page is correct. Proof = decode the `plantumlcloud` `data` param back to source and `java -jar plantuml.jar -check` it.

## 1. Surface the tools before you use them

MCP tools connect at **session startup**. A server registered mid-session -- or one present only in `~/.claude/settings.json` `mcpServers`, which this setup does NOT auto-load -- will not appear, and subagents inherit the stale set.

- Check: `claude mcp list` → must show `mcp-atlassian: … ✔ Connected`.
- Missing → re-register at **user scope** (the location this Claude Code version reads), then re-check:
  `claude mcp add mcp-atlassian -s user -e CONFLUENCE_URL=… -e CONFLUENCE_USERNAME=… -e CONFLUENCE_API_TOKEN=… -- uvx mcp-atlassian`
- Still not surfaced in the running session → drive the **same server** over stdio JSON-RPC via the bundled bridge: `python3 ./mcp_bridge.py call confluence_get_page '{"page_id":"…"}'`. This calls the real `tools/call` -- identical to what the harness does. See [references/access.md](./references/access.md).

> Never silently fall back to curl when the user asked for the configured MCP. Fix the connection first; bridge if you must.

## 2. Author in storage format, never markdown

Markdown pages render fenced code as plain `<pre><code>` (no panel, no highlighting) and PlantUML fences as **literal `@startuml` text** -- never rendered. Hand-built pages use **native storage format**:

- Code → `<ac:structured-macro ac:name="code">` + `<ac:parameter ac:name="language">…</ac:parameter>` + `<ac:plain-text-body><![CDATA[…]]></ac:plain-text-body>`.
- Diagram → `<ac:structured-macro ac:name="plantumlcloud">` with a **compressed `data` param**; the mxgraph plugin renders the SVG server-side.

Set `content_format: "storage"` on create/update. Large bodies via `content_file` (absolute path). See [references/storage-format.md](./references/storage-format.md) for macro templates and a markdown→storage converter.

## 3. Validate PlantUML before publishing (non-negotiable)

Every `plantumlcloud` diagram MUST be rendered to SVG and inspected before publish:

1. Decode the page's `data` param back to source (inverse of the compression in [references/plantuml.md](./references/plantuml.md)).
2. `java -jar plantuml.jar -tsvg file.puml` → exit 0 + a non-trivial SVG whose `<text>` labels match your participants/actors. Component/package diagrams also need Graphviz (`brew install graphviz`).
3. **Do NOT trust `-check`** -- it prints `Error line 1` / exits non-zero even for diagrams that render fine in this env (Java 25). Render + inspect is the only proof.

Publishing a diagram that produces no/trivial SVG or an error-marker image renders a broken diagram on the page.

## 4. The `\n` syntax trap (the regression)

A sequence-diagram message split across a **real newline** is a syntax error (`Error line N`):

```
Caller -> Adapter: POST /api/v1/cart/create
(headerReq.reqID, …)          ← this line is a SYNTAX ERROR
```

Multi-line messages keep the **literal two-char `\n`** inside ONE source line; PlantUML renders `\n` as a display break:

```
Caller -> Adapter: POST /api/v1/cart/create\n(headerReq.reqID, …)
```

Never `.replace("\\n", "\n")` a plantuml body before compressing.

## 5. Publishing is outward-facing -- confirm first

Creating/updating a Confluence page is a hard-to-undo external write. Confirm the target page id + intent before publishing unless durably authorized. If `confluence_delete_page` returns `PermissionException`, the token lacks trash scope -- **repurpose** the page (update title + body) rather than leaving an orphan; flag it for manual deletion.

## 6. Shortlinks & common tools

- `/x/<id>` tinylinks → page id via `GET /wiki/rest/api/shortlink/<id>` (auth required; WebFetch cannot). Or follow the redirect chain `…/x/<id>` → `tinyurl.action?urlIdentifier=<id>` → `spaces/…/pages/<id>/…`.
- Schemas: `python3 ./mcp_bridge.py schema confluence_create_page`.
- Key tools: `confluence_get_page` (param is `convert_to_markdown`, NOT `format`), `confluence_create_page` / `confluence_update_page` (`content_format`, `content_file`, `parent_id`, `version_comment`), `confluence_delete_page`, `confluence_get_page_children`, `confluence_search`.

## Cross-References

- [references/access.md](./references/access.md) -- creds location, fix-when-missing, the stdio bridge, shortlinks, delete-permission gotcha.
- [references/storage-format.md](./references/storage-format.md) -- macro templates, markdown→storage conversion, validation loop.
- [references/plantuml.md](./references/plantuml.md) -- the verified compression algorithm (encode + decode) and the `\n` trap.
- [references/page-template.md](./references/page-template.md) + `page_template.py` -- the exact endpoint-page template extracted from the hand-built cart/get example (`EoGMagE`): section order, fixed table column sets, highlighted metadata layout, wide-breakout code macros. Load + run the generator when a new page must match that example.

## Guru Meditation

The configured MCP is the source of truth; the bridge is the same server, not a workaround. Markdown is a rendering trap -- storage format is the contract. A diagram you cannot decode and `-check` is a diagram you have not proven.
