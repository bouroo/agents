#!/usr/bin/env python3
"""Stdio bridge to the configured mcp-atlassian MCP server.

WHY THIS EXISTS
MCP servers connect at Claude Code session startup. A server registered
mid-session -- or one present only in ~/.claude/settings.json `mcpServers`,
which this setup does NOT auto-load -- is not hot-loaded into the running
session's toolset, and subagents inherit that stale set. When the user asks for
"the configured MCP" but its tools are not surfaced, this bridge invokes the
SAME configured server (uvx mcp-atlassian, user-scope env) over stdio JSON-RPC
and calls its real tools via tools/call -- identical to what the harness does.

USAGE
    python3 mcp_bridge.py list                          # list tool names
    python3 mcp_bridge.py schema <tool>                 # print a tool's inputSchema
    python3 mcp_bridge.py call <tool> '<json args>' [timeout_seconds]

Credentials are read from ~/.claude/settings.json -> mcpServers.mcp-atlassian.env
(overridable via CONF_USER / CONF_TOK env vars).

EXAMPLES
    python3 mcp_bridge.py schema confluence_create_page
    python3 mcp_bridge.py call confluence_get_page '{"page_id":"6082560274","convert_to_markdown":false}'
    python3 mcp_bridge.py call confluence_update_page '{"page_id":"…","content_format":"storage","content_file":"/tmp/page.xml"}'
"""
import json
import os
import select
import subprocess
import sys
import time

_SETTINGS = os.path.expanduser("~/.claude/settings.json")


def _creds():
    user = os.environ.get("CONF_USER")
    tok = os.environ.get("CONF_TOK")
    if user and tok:
        return user, tok
    try:
        env = json.load(open(_SETTINGS))["mcpServers"]["mcp-atlassian"]["env"]
        return env["CONFLUENCE_USERNAME"], env["CONFLUENCE_API_TOKEN"]
    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        sys.exit(f"mcp_bridge: no creds. Set CONF_USER/CONF_TOK or configure "
                 f"~/.claude/settings.json mcpServers.mcp-atlassian.env ({e})")


def _server_env():
    user, tok = _creds()
    env = dict(os.environ)
    env.update({
        "CONFLUENCE_URL": "https://ktbinnovation.atlassian.net/wiki",
        "CONFLUENCE_USERNAME": user, "CONFLUENCE_API_TOKEN": tok,
        "JIRA_URL": "https://ktbinnovation.atlassian.net",
        "JIRA_USERNAME": user, "JIRA_API_TOKEN": tok,
    })
    return env


def _spawn():
    return subprocess.Popen(
        ["uvx", "mcp-atlassian"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, env=_server_env(), text=True, bufsize=1,
    )


def _jsonrpc(server, seq):
    def send(method, params=None, notify=False):
        mid = 0 if notify else seq[0]
        if not notify:
            seq[0] += 1
        server.stdin.write(json.dumps(
            {"jsonrpc": "2.0", "id": mid, "method": method, "params": params or {}}
        ) + "\n")
        server.stdin.flush()
    return send


def call_tool(tool_name: str, args: dict, wait: float = 60.0):
    server = _spawn()
    seq = [1]
    send = _jsonrpc(server, seq)
    send("initialize", {"protocolVersion": "2024-11-05", "capabilities": {},
                        "clientInfo": {"name": "mcp_bridge", "version": "1"}})
    send("notifications/initialized", notify=True)
    send("tools/call", {"name": tool_name, "arguments": args})
    want = seq[0] - 1
    out, deadline = [], time.time() + wait
    while time.time() < deadline:
        ready, _, _ = select.select([server.stdout], [], [], 0.5)
        if ready:
            line = server.stdout.readline()
            if not line:
                break
            out.append(line)
            if _id(line) == want:
                break
    try:
        server.stdin.close()
        server.terminate()
    except Exception:
        pass
    for line in out:
        try:
            o = json.loads(line)
            if o.get("id") == want:
                return o.get("result"), o.get("error")
        except json.JSONDecodeError:
            pass
    return None, {"message": "no response", "raw": out[-5:] if out else []}


def list_tools(wait: float = 8.0):
    server = _spawn()
    send = _jsonrpc(server, [1])
    send("initialize", {"protocolVersion": "2024-11-05", "capabilities": {},
                        "clientInfo": {"name": "mcp_bridge", "version": "1"}})
    send("notifications/initialized", notify=True)
    server.stdin.write(json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}) + "\n")
    server.stdin.flush()
    time.sleep(wait)
    try:
        server.stdin.close()
    except Exception:
        pass
    out = []
    for _ in range(400):
        ready, _, _ = select.select([server.stdout], [], [], 0.5)
        if ready:
            line = server.stdout.readline()
            if not line:
                break
            out.append(line)
    try:
        server.terminate()
    except Exception:
        pass
    for line in out:
        try:
            o = json.loads(line)
            if o.get("id") == 2:
                return o.get("result", {}).get("tools", [])
        except json.JSONDecodeError:
            pass
    return []


def _id(line: str):
    try:
        return json.loads(line).get("id")
    except json.JSONDecodeError:
        return None


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return
    mode = sys.argv[1]
    if mode == "list":
        for t in list_tools():
            print(t["name"])
    elif mode == "schema":
        want = sys.argv[2]
        for t in list_tools():
            if t["name"] == want:
                print(json.dumps(t, indent=2))
                return
        sys.exit(f"unknown tool: {want}")
    elif mode == "call":
        if len(sys.argv) < 3:
            sys.exit("usage: call <tool> '<json args>' [timeout]")
        tool, raw = sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "{}"
        wait = float(sys.argv[4]) if len(sys.argv) > 4 else 60.0
        try:
            args = json.loads(raw)
        except json.JSONDecodeError as e:
            sys.exit(f"bad json args: {e}")
        res, err = call_tool(tool, args, wait=wait)
        if err:
            print("ERROR:", json.dumps(err, indent=2), file=sys.stderr)
            sys.exit(1)
        print(json.dumps(res, indent=2))
    else:
        sys.exit(f"unknown mode: {mode}")


if __name__ == "__main__":
    main()
