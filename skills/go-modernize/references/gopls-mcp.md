# gopls MCP: official headless server

`gopls mcp` starts one MCP server for the process's current working directory. Without `-listen` it speaks stdio; with `-listen=localhost:0` it chooses an OS-assigned localhost port. `-instructions` prints gopls's canonical tool-use guidance — prefer loading that file from a live server so guidance stays version-matched.

Use **one headless server per workspace**, not one host-side instance per file or task. Each process owns one session rooted where it starts, so its workspace view, file watcher, and root discovery stay coherent. When a host can spawn a command, configure only `gopls mcp`; do not route it through `mcp-remote`. Treat an SSE listener as private to the supervisor/machine: bind it to localhost only, discover its address at spawn time, and do not expose it beyond the user session.

Avoid `gopls serve -mcp.listen` as a standalone or multi-host workaround. It is designed to offer MCP alongside an LSP server; clients with different roots can create conflicting workspace intent. For shared analysis behind multiple hosts, use the official gopls daemon with a workspace-aware MCP server that forwards to it (see below).

## Official daemon sharing

`gopls -remote=auto ...` forwards to a daemon and starts one if needed; it reuses an existing daemon automatically. This is the supported way to reuse analysis while preserving workspace identity:

```bash
# One daemon, one attached LSP client.
gopls -remote=auto serve

# One daemon, one workspace-local MCP session.
cd /path/to/module
gopls -remote=auto mcp
```

Start the daemon explicitly only when prewarming a known environment. Prefer `auto` and let gopls own the daemon address and lifecycle; `-remote.listen.timeout` controls its idle lifetime. `gopls remote sessions` shows current sessions; investigate before restarting anything.

## Efficient workflow

`gopls mcp -instructions` is authoritative for the installed version. Apply this bounded ordering:

1. `go_workspace` once per workspace; run `go_vulncheck` immediately for a Go workspace and whenever `go.mod` or `go.sum` changes.
2. Locate with `go_search`; inspect with `go_file_context`; use `go_package_api` for package surfaces.
3. Before changing a symbol, call `go_symbol_references`; apply all edits; then call `go_diagnostics` for edited files.
4. Resolve diagnostics before tests. Test the changed packages, not all packages, unless asked.

Treat MCP-provided fixes and edits as proposals. Review diffs before applying them; never let a tool write outside the workspace or accept destructive actions without explicit authorization.
