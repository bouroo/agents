# gopls MCP: one shared instance

`gopls mcp` (detached stdio) and `gopls serve -mcp.listen=<addr>` (attached HTTP) both expose the same tools — `go_diagnostics`, `go_file_context`, `go_package_api`, `go_rename_symbol`, `go_search`, `go_symbol_references`, `go_vulncheck`, `go_workspace` (verify with a tools/list against a live instance; the set grows with gopls).

Why one shared instance: each host that spawns `gopls mcp` stdio gets its own process — cold caches, duplicate memory, N instances diverging on the same module. `gopls serve -mcp.listen=<addr>` shares ONE process with all hosts.

**Port discipline — detect, never hardcode.** Fixed ports collide and survive stale on other machines. The launcher discovers the address at startup:

1. **Probe for a live instance first.** An already-running gopls MCP wins over any default: if a listener answers the MCP handshake, reuse it and bind nothing. Caveat (verified): gopls's `/mcp` is an SSE stream — a healthy instance never "completes" a GET, so treat curl exit `28` (timed out while connected) as **alive** alongside `0`; only refusal (7) / no-route (6) means dead.
2. **No instance → take a free high port** (49152–65535, the ephemeral range) — never a fixed constant.
3. **Publish the chosen port** where clients find it (see below); hosts read it at connect time.

```bash
# 1. Reuse: probe the endpoint; treat connected-but-streaming (curl 28) as alive.
probe() { local rc; curl -s --max-time 2 -o /dev/null "http://localhost:$1/mcp"; rc=$?; [ $rc -eq 0 ] || [ $rc -eq 28 ]; }
# 2. Otherwise bind a free high port (49152-65535), not a constant:
GOPLS_MCP_PORT=$(python3 -c 'import socket;s=socket.socket();s.bind(("localhost",0));print(s.getsockname()[1]);s.close()')
gopls serve -mcp.listen="localhost:${GOPLS_MCP_PORT}" < <(sleep 315360000)
```

Gotchas (all verified on gopls v0.23 / go1.26.7):

- `gopls serve` **exits when its stdin closes** — it is an attached server. A headless singleton needs a held-open pipe plus a supervisor that restarts the pair when gopls dies.
- Its MCP transport is the **legacy HTTP+SSE** protocol (GET returns `event: endpoint` with a `?sessionid=` URL; messages are POSTed there). Modern streamable-HTTP clients cannot POST `initialize` directly — stdio-only or streamable-only hosts need a bridge.
- `mcp-remote` stalls: its OAuth discovery probes hit gopls's SSE handler, which answers **every** GET (including `/.well-known/*`) with an open stream. A minimal stdio proxy avoids this.

## The pattern (macOS)

Supervisor script `~/.local/bin/gopls-mcp-serve` (launchd `KeepAlive` restarts it; it reaps the stdin holder on exit):

```bash
#!/usr/bin/env bash
# Reuse a live instance: SSE streams never complete, so connected-but-timed-out
# (curl 28) means alive; refused (7) / no-route (6) means dead.
probe() { local rc; curl -s --max-time 2 -o /dev/null "http://localhost:$1/mcp"; rc=$?; [ $rc -eq 0 ] || [ $rc -eq 28 ]; }
for p in "${GOPLS_MCP_PORT:-}" $(lsof -nP -iTCP -sTCP:LISTEN 2>/dev/null \
         | awk '/gopls/ {print $9}' | grep -o '[0-9]*$' | sort -u); do
  [ -n "$p" ] && probe "$p" && exit 0            # already served — done
done
# Nothing answers: pick a free high port (49152-65535), never a constant.
GOPLS_MCP_PORT=$(python3 -c 'import socket;s=socket.socket();s.bind(("localhost",0));print(s.getsockname()[1]);s.close()')
# Hold stdin open: gopls serve dies at EOF, the pipe keeps it headless.
# Publish the port for bridges/hosts before serving.
printf '%s' "$GOPLS_MCP_PORT" > "$HOME/.local/state/gopls-mcp.port"
gopls serve -mcp.listen="localhost:${GOPLS_MCP_PORT}" < <(sleep 315360000)
exit 1   # non-zero -> launchd KeepAlive restarts (and re-detects)
```

LaunchAgent `~/Library/LaunchAgents/ai.gopls.mcp.plist`: `Label ai.gopls.mcp`, `ProgramArguments` → the script, `RunAtLoad` + `KeepAlive` true, `ProcessType Background`; load with `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.gopls.mcp.plist`.

Bridge for stdio-only hosts, `~/.local/bin/gopls-mcp-bridge` (~60 lines of stdlib Python): reads the port at startup (`$GOPLS_MCP_PORT`, else the published `~/.local/state/gopls-mcp.port`), GETs the SSE stream for the session endpoint; forwards stdin NDJSON lines as POSTs; streams `data:` events back to stdout. (Kept beside the launcher on the operating machine — see memory index.)

## Wiring by transport class

The port is resolved at connect time — never baked into a host config as a literal:

| Host client speaks | MCP config entry |
|---|---|
| legacy SSE / auto-detect remote | server entry whose `url` is produced by a wrapper (`http://localhost:$(cat ~/.local/state/gopls-mcp.port)/mcp`); scope it user-wide and delete per-project `gopls mcp` stdio entries. Hosts that demand a literal URL: pin the current port, and treat a supervisor rebind as a config-change event |
| stdio-only | `{"command": "<path>/gopls-mcp-bridge"}` (or any stdio bridge that does not probe OAuth metadata) — the bridge resolves the port itself |
| hosts with no MCP support at all | nothing to wire |

Verification ladder: `lsof -nP -iTCP -sTCP:LISTEN | awk '/gopls/'` (exactly one gopls pid, port within 49152–65535); full MCP handshake (initialize → notified → tools/list) on the discovered port, first via native HTTP+SSE (curl), then through the bridge (spawn it, speak stdio JSON-RPC); the host with the richest client surface shows `✔ Connected` against the SSE URL; kill the gopls pid and watch launchd rebind — on a **new** free port, confirming configs resolved it dynamically.
