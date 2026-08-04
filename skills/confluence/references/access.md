# Access: creds, fix-when-missing, the stdio bridge

The short doctrine lives in [SKILL.md](../SKILL.md); this file is the concrete plumbing.

## Credentials

`mcp-atlassian` is configured for `ktbinnovation.atlassian.net` (space `GoofyDisco`). Creds live in `~/.claude/settings.json` → `mcpServers.mcp-atlassian.env`:

- `CONFLUENCE_URL` / `CONFLUENCE_USERNAME` / `CONFLUENCE_API_TOKEN`
- `JIRA_URL` / `JIRA_USERNAME` / `JIRA_API_TOKEN` (same token value as Confluence)

The server command is `uvx mcp-atlassian`. It exposes ~98 tools incl. `confluence_get_page`, `confluence_create_page`, `confluence_update_page`, `confluence_delete_page`, `confluence_get_page_children`, `confluence_search`.

## Fix when `claude mcp list` shows nothing

`~/.claude/settings.json` `mcpServers` is NOT auto-loaded by this Claude Code setup -- `claude mcp list` reported none even though the entry existed. Re-register at **user scope** (the location this version reads):

```bash
USER=$(python3 -c "import json;d=json.load(open('$HOME/.claude/settings.json'))['mcpServers']['mcp-atlassian']['env'];print(d['CONFLUENCE_USERNAME'])")
TOK=$(python3 -c "import json;d=json.load(open('$HOME/.claude/settings.json'))['mcpServers']['mcp-atlassian']['env'];print(d['CONFLUENCE_API_TOKEN'])")
claude mcp add mcp-atlassian -s user \
  -e "JIRA_URL=https://ktbinnovation.atlassian.net" \
  -e "JIRA_USERNAME=$USER" -e "JIRA_API_TOKEN=$TOK" \
  -e "CONFLUENCE_URL=https://ktbinnovation.atlassian.net/wiki" \
  -e "CONFLUENCE_USERNAME=$USER" -e "CONFLUENCE_API_TOKEN=$TOK" \
  -- uvx mcp-atlassian
claude mcp list   # → mcp-atlassian: uvx mcp-atlassian - ✔ Connected
```

**Gotcha:** even after `✔ Connected`, the tools surface only in sessions started *after* registration. A session already running (and its subagents) keeps the stale toolset.

## The stdio bridge (when tools are not surfaced mid-session)

MCP tools connect at session startup; a server added mid-session is not hot-loaded. When the user insists on "the configured MCP" but its tools are not surfaced, drive the **same server** over stdio JSON-RPC. The bundled `../mcp_bridge.py` does this -- it is the same server/tools/auth, transport-bridged:

```bash
cd <skill dir>
python3 mcp_bridge.py list                                   # tool names
python3 mcp_bridge.py schema confluence_create_page          # inputSchema
python3 mcp_bridge.py call confluence_get_page '{"page_id":"6082560274","convert_to_markdown":false}'
python3 mcp_bridge.py call confluence_update_page '{"page_id":"…","content_format":"storage","content_file":"/tmp/page.xml","version_comment":"…"}'
```

The bridge reads creds from `~/.claude/settings.json` (or `CONF_USER`/`CONF_TOK` env vars), so it works with no edits.

## Tool schemas / gotchas

- `confluence_get_page`: params are `page_id` (or `title`+`space_key`), `convert_to_markdown` (bool), `include_metadata`. There is **no `format` param** -- passing one errors with `unexpected_keyword_argument`. To get raw HTML/storage, `convert_to_markdown: false`.
- `confluence_create_page` / `confluence_update_page`: `space_key`, `title`, `parent_id`, `content_format` (`markdown` default | `storage` | `wiki`), `content` **or** `content_file` (absolute path -- use this for large bodies), `version_comment`, `is_minor_edit`. Create returns the new page `id`.
- `confluence_get_page_children`: `parent_id`.
- `confluence_delete_page`: `page_id`. **Often denied** -- the token lacks trash scope (`PermissionException: Unable to trash content`). Repurpose instead (see below).

## Shortlink resolution

`/x/<id>` tinylinks need auth (WebFetch cannot reach them). Resolve to a page id:

```bash
# direct REST lookup (needs user:token)
curl -s -u "$USER:$TOK" "https://ktbinnovation.atlassian.net/wiki/rest/api/shortlink/<id>"
# or follow the redirect chain and read the final /pages/<id>/ URL
curl -s -u "$USER:$TOK" -L -o /dev/null -w "%{url_effective}" "https://ktbinnovation.atlassian.net/wiki/x/<id>"
```

The redirect chain is `…/x/<id>` → `…/pages/tinyurl.action?urlIdentifier=<id>` → `…/spaces/<KEY>/pages/<pageId>/…`.

## Can't-delete fallback: repurpose

When `confluence_delete_page` is denied, do not leave an orphan. Update the page to a useful target (title + storage body) and flag the original intent in the version comment. Worked example: orphaned test page `6134759539` was repurposed into the service's shared "Response Codes" reference.
