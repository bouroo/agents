---
name: confluence
description: "Operate Atlassian wikis end-to-end through the Rovo remote MCP server (OAuth): connect/authenticate, resolve sites/shortlinks, search and read pages, author pages whose code blocks and diagrams render, update safely. Load before any Confluence create/update/get/delete."
---

# Confluence via the Rovo MCP Server

Operate Atlassian wikis through the **Rovo MCP server** - the Atlassian-hosted remote MCP endpoint (`https://mcp.atlassian.com/v1/mcp/authv2`, HTTP transport, OAuth 2.1; optional API-token auth). No local bridge, credentials, or scripts are needed: the harness surfaces `mcp__atlassian__*` tools; everything else here is operating doctrine. Official getting-started guide: <https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/>.

> **Scope.** How to drive a configured wiki connection and author content that renders. Not a Confluence user guide; targets/sites are whatever the authenticated account can reach.

## Connect and authenticate

Register the endpoint as an HTTP MCP server in any MCP-compatible client - every major agent documents a one-line setup for exactly this URL; hands-off path is Atlassian's own self-setup prompt, pasted verbatim:

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

**MCP connections surface only at session start.** A server registered mid-session does not hot-load, and completing OAuth lands after the session began: if the tools do not appear, finish authentication once, then restart the session/headless run. On truly headless hosts where browser OAuth cannot complete, fall back to running the open-source `mcp-atlassian` server locally over stdio with an API token (same tool surface, snake_case names); prefer the remote server whenever possible.

## Resolve before you act

1. Unknown site? Call `getAccessibleAtlassianResources` for reachable `cloudId`s; every other call takes one.
2. Shortlink (`.../wiki/x/<encoded>`)? Pass the encoded part directly as `pageId` to `getConfluencePage` - it accepts tiny link IDs; no redirect chase.
3. Content discovery: Rovo `search` (natural language across products) first; `searchConfluenceUsingCql` when precision matters (`type = page AND ancestor = <id>`, `space.title ~ ...`, date/creator filters). Escape inner quotes with backslashes.
4. Structured reads: `getConfluencePage` (supports `contentFormat`: `markdown` cheap scans, `html` fidelity, `adf` programmatic), space/page children via `getConfluencePageDescendants`, footer/inline comments via the comment tools.
5. One-shot metadata for any entity: `fetch` with an ARI (`ari:cloud:confluence:<cloudId>:page/<id>`), or `getTeamworkGraphContext` when you need what links *to* the page (PRs, issues, deployments).

## Author pages that render

Writes go out as **`html` contentFormat**: round-trip safe, and it is what the remote server accepts. Legacy storage-format `<ac:structured-macro>` markup is rejected here. Rules paid for by real breakage:

- Code blocks: `<pre><code class="language-<lang>">source</code></pre>`; HTML-escape `& < >`.
- Panels/status/expands/layouts use Confluence-HTML data-type nodes - follow the editor contract, never raw wiki markup.
- **Diagrams default to PlantUML** through the instance's diagram macro; a bare `<pre><code>@startuml...` NEVER renders as a diagram (it shows literal text - the one failure mode invisible when re-reading the body). Every published diagram ships with its raw source mirrored in a collapsed expand so it survives macro outages.
- Native Mermaid macros are not installed everywhere and third-party ones store out-of-band attachments the API cannot create: treat Mermaid as manual-via-UI only.
- **Large pages:** create with a minimal placeholder body plus real title/parent, then push the full body via a second update call. Gateway transport errors (502s/reset) hit big payloads; retry after ~20 s.

**Publish-then-prove:** after any write, re-fetch the page and confirm the stored body contains what you intended (macro wrappers present, sources escaped). A narrated success without the read-back is theater.

## Safety

Creating/updating/deleting pages is a hard-to-undo external write: hold to the `AUTH:`/`PENDING:` gates ([craft](../craft/SKILL.md)) - quote authorization for the specific target, emit `PENDING:` when unsure. If deletion returns a permission error, **repurpose** the page (rename + blank body + pointer note) rather than leaving orphan content, and flag it for manual cleanup.
