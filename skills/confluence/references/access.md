# Access: official remote MCP, fix-when-missing, the stdio fallback bridge

The short doctrine lives in [SKILL.md](../SKILL.md); this file is the concrete plumbing.

## Primary connection: the official Atlassian remote MCP server

The canonical server is the **official Atlassian remote MCP** (`https://mcp.atlassian.com/v1/mcp/authv2`, HTTP transport, OAuth2.1) -- the Atlassian-hosted build of the open-source `mcp-atlassian` server. It exposes the same `confluence_*` tool surface (and jira_*). Config in the host's `~/.claude/settings.json`:

```json
{ "mcpServers": { "atlassian": { "url": "https://mcp.atlassian.com/v1/mcp/authv2" } } }
```

Authentication is OAuth2.1; a one-time browser login is triggered the first time the server is used in a session. An API token is also accepted as an optional credential (same Atlassian account), but the remote server carries no token in the config file.

Register at user scope if not already:

```bash
claude mcp add --transport http atlassian https://mcp.atlassian.com/v1/mcp/authv2
claude mcp list   # → atlassian: https://mcp.atlassian.com/v1/mcp/authv2 - ✔ Connected
```

**Gotcha (load-bearing):** MCP servers connect at session startup. The `atlassian` server is not hot-loaded mid-session, and OAuth completes after the session has begun -- so `confluence_*` tools surface only in sessions **started after** the server connects (and OAuth has succeeded at least once). A session already running -- and its subagents -- keep the stale toolset. Fix: complete OAuth in a browser once, then **restart the host/session**.

## When `confluence_*` tools are not surfaced

1. Confirm registration: `claude mcp list` should show `atlassian … ✔ Connected`.
2. Confirm OAuth completed: the first call after registration opens a browser to `id.atlassian.com`; approve. Subsequent calls reuse the cached token.
3. **Restart the session** so the registered-and-connected server is loaded at startup. Tools then surface as `mcp__atlassian__confluence_*` (exact prefix depends on the host's tool-naming convention -- confirm with `claude mcp` or by listing tools).

## Fallback: the stdio bridge (when OAuth is unavailable or tools still won't surface)

When OAuth is unavailable (headless/CI, or a stubborn mid-session stalemate), drive the **same `mcp-atlassian` server** over stdio JSON-RPC via the bundled `../mcp_bridge.py`. It is the same server/tools/auth, transport-bridged -- not a workaround:

```bash
cd <skill dir>
python3 mcp_bridge.py list                                   # tool names
python3 mcp_bridge.py schema confluence_create_page          # inputSchema
python3 mcp_bridge.py call confluence_get_page '{"page_id":"123456789","convert_to_markdown":false}'
python3 mcp_bridge.py call confluence_update_page '{"page_id":"…","content_format":"storage","content_file":"/tmp/page.xml","version_comment":"…"}'
```

The bridge reads creds from `~/.claude/settings.json` → `mcpServers.mcp-atlassian.env` (the older stdio+token entry, if present), or from `CONF_USER` / `CONF_TOK` env vars. With only the remote `mcpServers.atlassian` (HTTP, no token) configured, pass `CONF_USER` and `CONF_TOK` (an Atlassian API token for the same account) explicitly when invoking the bridge.

## Tool schemas / gotchas

- `confluence_get_page`: params are `page_id` (or `title`+`space_key`), `convert_to_markdown` (bool), `include_metadata`. There is **no `format` param** -- passing one errors with `unexpected_keyword_argument`. To get raw HTML/storage, `convert_to_markdown: false`.
- `confluence_create_page` / `confluence_update_page`: `space_key`, `title`, `parent_id`, `content_format` (`markdown` default | `storage` | `wiki`), `content` **or** `content_file` (absolute path -- use this for large bodies), `version_comment`, `is_minor_edit`. Create returns the new page `id`.
- `confluence_get_page_children`: `parent_id`.
- `confluence_delete_page`: `page_id`. **Often denied** -- the token lacks trash scope (`PermissionException: Unable to trash content`). Repurpose instead (see below).

## Shortlink resolution

`/x/<id>` tinylinks need auth (WebFetch cannot reach them). Resolve to a page id.

**Under the stdio bridge** (has a user:token pair), the REST lookup and redirect-follow both work:

```bash
# direct REST lookup (needs user:token)
curl -s -u "$USER:$TOK" "https://<your-domain>.atlassian.net/wiki/rest/api/shortlink/<id>"
# or follow the redirect chain and read the final /pages/<id>/ URL
curl -s -u "$USER:$TOK" -L -o /dev/null -w "%{url_effective}" "https://<your-domain>.atlassian.net/wiki/x/<id>"
```

The redirect chain is `…/x/<id>` → `…/pages/tinyurl.action?urlIdentifier=<id>` → `…/spaces/<KEY>/pages/<pageId>/…`.

**Under the remote MCP (OAuth)** there is no basic-auth token for `curl -u`. Resolve instead by: following the `/x/<id>` redirect in an **authenticated browser session** and reading the `…/pages/<pageId>/…` URL; or by `confluence_search` if the page title is known; or by fetching the likely parent and using `confluence_get_page_children`. If a token is needed, fall back to the stdio bridge for this one resolution step.

## Can't-delete fallback: repurpose

When `confluence_delete_page` is denied, do not leave an orphan. Update the page to a useful target (title + storage body) and flag the original intent in the version comment. Worked example: orphaned test page `6134759539` was repurposed into the service's shared "Response Codes" reference.
