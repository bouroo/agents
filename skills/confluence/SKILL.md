---
name: confluence
description: "Operate the Confluence/Jira mcp-atlassian server end-to-end. Use when the MCP tools do not surface mid-session (fix registration + stdio bridge), to resolve shortlinks, and to author pages so code blocks and PlantUML diagrams render (native storage format, never markdown). Load before any create/update/get/delete of a Confluence page."
---

# Confluence (mcp-atlassian) Operations

Durable operating doctrine for the `mcp-atlassian` server. Captures every trap hit in real wiki work so it is never re-derived. Detail lives in `references/`; load only what the task needs.

> **Scope.** This skill is about *operating* the configured MCP server and *authoring* content that renders. It is not a Confluence user guide. Target instance, space, and credentials are read from the host's settings -- never hardcoded here.

## 0. Prime Directive

**Use the configured MCP, not curl/REST -- and prove renders by decoding the stored body, never by trusting `body.view`.** The REST `body.view` returns a JS stub for macro-rendered content (code panels, PlantUML); it looks empty/broken even when the page is correct. Proof = decode the `plantumlcloud` `data` param back to source and render-inspect it.

## 1. Surface the tools before you use them

The MCP tools fail to surface mid-session when their registration drifts. Fix sequence (full detail in [access](references/access.md)):

1. Confirm credentials are present in the host's settings (API token + site).
2. Run the [stdio bridge](mcp_bridge.py) to list tool schemas: `python3 ./mcp_bridge.py schema confluence_create_page`.
3. Re-assert the server config; restart the host so it re-registers.

If a tool still does not surface, the bridge is the same server over stdio -- use it directly; it is not a workaround.

## 2. Author in storage format, never markdown

Markdown is a rendering trap on Confluence. The contract is the native **storage format** (XHTML + macros). Code blocks use `<ac:structured-macro ac:name="code">`; PlantUML uses `plantumlcloud`. Author or update with `content_format: storage` (or write to a `content_file`). See [storage-format](references/storage-format.md).

## 3. PlantUML that renders

- Sequence-diagram messages split across a **real newline** are a syntax error -- join the line.
- **Do not trust a local `-check`** that reports `Error line 1` in some Java versions; it can be a false negative. Render + inspect the SVG is the only proof.
- The verified compression algorithm (encode + decode) and the `\n` trap are in [plantuml](references/plantuml.md). Publishing a diagram that produces no/trivial SVG or an error-marker image renders broken on the page.

## 4. Page lifecycle & safety

Creating/updating a Confluence page is a hard-to-undo external write. Confirm the target page id + intent before publishing unless durably authorized ([code-craft](../code-craft/SKILL.md) `AUTH:` gate). If `confluence_delete_page` returns `PermissionException`, the token lacks trash scope -- **repurpose** the page (update title + body) rather than leaving an orphan; flag it for manual deletion.

## 5. Shortlinks & key tools

- Shortlinks resolve to a page id via the authenticated shortlink API (WebFetch cannot -- no auth). Or follow the redirect chain to the page id.
- Schemas: `python3 ./mcp_bridge.py schema confluence_create_page`.
- Key tools: `confluence_get_page` (param is `convert_to_markdown`, NOT `format`), `confluence_create_page` / `confluence_update_page` (`content_format`, `content_file`, `parent_id`, `version_comment`), `confluence_delete_page`, `confluence_get_page_children`, `confluence_search`.

## References

- [access.md](references/access.md) -- creds location, fix-when-missing, the stdio bridge, shortlinks, delete-permission gotcha.
- [storage-format.md](references/storage-format.md) -- macro templates, markdown-to-storage conversion, validation loop.
- [plantuml.md](references/plantuml.md) -- the verified compression algorithm (encode + decode) and the newline trap.
- [page-template.md](references/page-template.md) + [page_template.py](page_template.py) -- the endpoint-page template generator (section order, fixed table column sets, highlighted metadata, code macros). Load + run when a new page must match that example.
- [code-craft](../code-craft/SKILL.md) -- the `AUTH:` gate for external writes.
