#!/usr/bin/env python3
"""scripts/checks.py - Repo validator for the agents config.

Nine deterministic gates; exits non-zero on any failure.

Gates that depend on optional files (plugin.json, marketplace.json, eval/,
and new skills not yet on disk) WARN (not FAIL) when those files are absent,
so this validator can run before the parallel packaging units land. Once
those units ship, the same script enforces the contract with PASS/FAIL.

Usage:
    python3 scripts/checks.py [--all] [--help]

Exit codes:
    0  every gate PASS or WARN (no FAIL)
    1  at least one gate FAIL
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any, Callable, Dict, Iterable, List, Tuple

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN_JSON = os.path.join(REPO, "plugin.json")
MARKETPLACE_JSON = os.path.join(REPO, "marketplace.json")
CLAUDE_PLUGIN_DIR = os.path.join(REPO, ".claude-plugin")
CLAUDE_PLUGIN_JSON = os.path.join(CLAUDE_PLUGIN_DIR, "plugin.json")
CLAUDE_MARKETPLACE_JSON = os.path.join(CLAUDE_PLUGIN_DIR, "marketplace.json")
CURSOR_PLUGIN_DIR = os.path.join(REPO, ".cursor-plugin")
CURSOR_PLUGIN_JSON = os.path.join(CURSOR_PLUGIN_DIR, "plugin.json")
CURSOR_MARKETPLACE_JSON = os.path.join(CURSOR_PLUGIN_DIR, "marketplace.json")
GEMINI_EXTENSION_JSON = os.path.join(REPO, "gemini-extension.json")
SKILLS_DIR = os.path.join(REPO, "skills")
AGENTS_DIR = os.path.join(REPO, "agents")
COMMANDS_DIR = os.path.join(REPO, "commands")
EVAL_RESULTS = os.path.join(REPO, "eval", "results")
AGENTS_MD = os.path.join(REPO, "AGENTS.md")

ALLOWED_MODES = {"primary", "subagent", "all"}
ALLOWED_PERMISSIONS = {
    "read", "edit", "glob", "grep", "list", "bash", "task",
    "external_directory", "todowrite", "webfetch", "websearch",
    "lsp", "skill", "question", "doom_loop",
}
ALLOWED_COMMAND_KEYS = {"description", "agent", "subtask", "model", "template"}

EM_DASH = "\u2014"
EN_DASH = "\u2013"
DASH_RE = re.compile(EM_DASH + "|" + EN_DASH)
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

SCAN_EXTS = (".md", ".json", ".sh", ".py")
SCAN_SKIP_TOP_DIRS = {".git", "node_modules"}
SCAN_SKIP_PATH_PREFIX = (".agents" + os.sep + "handoff",)

Msg = Tuple[str, str]  # (level, message) where level in {"PASS","FAIL","WARN"}
GateResult = Tuple[bool, List[Msg]]


# ---------------------------------------------------------------------------
# Frontmatter parsing (stdlib only; handles `>` and `|` block scalars + nested
# mappings such as the `permission:` block on agents/conductor.md).
# ---------------------------------------------------------------------------

def _parse_block(lines: List[str], start: int, indent: int) -> Tuple[Dict[str, Any], int]:
    result: Dict[str, Any] = {}
    i = start
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        actual_indent = len(line) - len(stripped)
        if actual_indent < indent:
            return result, i
        if actual_indent > indent:
            i += 1
            continue
        if stripped == "---":
            return result, i
        m = re.match(r"^([A-Za-z0-9_-]+):(.*)$", stripped)
        if not m:
            i += 1
            continue
        key = m.group(1)
        rest = m.group(2)
        if rest.strip() == "":
            j = i + 1
            while j < n and lines[j].strip() == "":
                j += 1
            if j < n:
                nxt = lines[j]
                nxt_stripped = nxt.lstrip()
                if nxt_stripped and not nxt_stripped.startswith("#"):
                    nxt_indent = len(nxt) - len(nxt_stripped)
                    if nxt_indent > indent:
                        sub, end_i = _parse_block(lines, j, nxt_indent)
                        result[key] = sub
                        i = end_i
                        continue
            result[key] = ""
            i += 1
            continue
        rest_stripped = rest.lstrip()
        if rest_stripped[:1] in (">", "|"):
            indicator = rest_stripped[:1]
            first = rest_stripped[1:].strip()
            i += 1
            buf: List[str] = []
            if first:
                buf.append(first)
            while i < n:
                ln = lines[i]
                if ln.startswith(" ") or ln.startswith("\t"):
                    s = ln.strip()
                    if s:
                        buf.append(s)
                    i += 1
                elif ln == "":
                    i += 1
                else:
                    break
            result[key] = " ".join(buf) if indicator == ">" else "\n".join(buf)
            continue
        v = rest_stripped
        if len(v) >= 2 and v[0] == v[-1] and v[0] in ('"', "'"):
            v = v[1:-1]
        result[key] = v
        i += 1
    return result, i


def parse_frontmatter(text: str) -> Dict[str, Any]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    data, _ = _parse_block(lines, 1, 0)
    return data


# ---------------------------------------------------------------------------
# Gate helpers
# ---------------------------------------------------------------------------

def _add(msgs: List[Msg], level: str, msg: str) -> None:
    msgs.append((level, msg))


def _scan_files() -> Iterable[str]:
    skip_prefixes = tuple(p + os.sep for p in SCAN_SKIP_PATH_PREFIX)
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in SCAN_SKIP_TOP_DIRS]
        for f in files:
            if not f.endswith(SCAN_EXTS):
                continue
            full = os.path.join(root, f)
            rel = os.path.relpath(full, REPO)
            if any(rel == p or rel.startswith(p) for p in skip_prefixes):
                continue
            yield full


# ---------------------------------------------------------------------------
# Gates
# ---------------------------------------------------------------------------

def g1_manifests_parse() -> GateResult:
    msgs: List[Msg] = []
    ok = True
    for path, required in (
        (PLUGIN_JSON, ["name", "version", "description"]),
        (MARKETPLACE_JSON, None),
    ):
        name = os.path.basename(path)
        if not os.path.isfile(path):
            _add(msgs, "WARN", f"{name}: absent (skipped)")
            continue
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            _add(msgs, "FAIL", f"{name}: parse error: {e}")
            ok = False
            continue
        if required:
            missing = [k for k in required if k not in data]
            if missing:
                _add(msgs, "FAIL", f"{name}: missing required keys {missing}")
                ok = False
            else:
                _add(msgs, "PASS", f"{name}: parses; has {sorted(required)}")
        else:
            _add(msgs, "PASS", f"{name}: parses")
    return ok, msgs


def g2_versions_agree() -> GateResult:
    msgs: List[Msg] = []
    have_p = os.path.isfile(PLUGIN_JSON)
    have_m = os.path.isfile(MARKETPLACE_JSON)
    if not (have_p and have_m):
        missing = [n for n, have in (("plugin.json", have_p), ("marketplace.json", have_m)) if not have]
        _add(msgs, "WARN", f"{', '.join(missing)} absent; version agreement skipped")
        return True, msgs
    try:
        with open(PLUGIN_JSON, encoding="utf-8") as f:
            pv = json.load(f).get("version")
        with open(MARKETPLACE_JSON, encoding="utf-8") as f:
            m = json.load(f)
        plugins = m.get("plugins")
        mv = plugins[0].get("version") if isinstance(plugins, list) and plugins else None
    except Exception as e:
        _add(msgs, "FAIL", f"version check: {e}")
        return False, msgs
    if pv is None or mv is None:
        _add(msgs, "FAIL", f"version check: missing version (plugin={pv!r}, marketplace[0]={mv!r})")
        return False, msgs
    if pv != mv:
        _add(msgs, "FAIL",
             f"version mismatch: plugin.json={pv!r} vs marketplace.json.plugins[0]={mv!r}")
        return False, msgs
    _add(msgs, "PASS", f"versions agree ({pv})")
    return True, msgs


def g3_skills_frontmatter() -> GateResult:
    msgs: List[Msg] = []
    ok = True
    if not os.path.isdir(SKILLS_DIR):
        _add(msgs, "WARN", "skills/ absent; skipped")
        return True, msgs
    for entry in sorted(os.listdir(SKILLS_DIR)):
        sd = os.path.join(SKILLS_DIR, entry)
        if not os.path.isdir(sd):
            continue
        sname = entry
        sfile = os.path.join(sd, "SKILL.md")
        if not os.path.isfile(sfile):
            _add(msgs, "FAIL", f"skill {sname}: SKILL.md missing")
            ok = False
            continue
        try:
            with open(sfile, encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            _add(msgs, "FAIL", f"skill {sname}: read error: {e}")
            ok = False
            continue
        if not text.startswith("---"):
            _add(msgs, "FAIL", f"skill {sname}: file does not start with ---")
            ok = False
            continue
        fm = parse_frontmatter(text)
        if not fm:
            _add(msgs, "FAIL", f"skill {sname}: frontmatter missing or empty")
            ok = False
            continue
        fm_name = fm.get("name", "")
        if not fm_name:
            _add(msgs, "FAIL", f"skill {sname}: name field missing")
            ok = False
        elif fm_name != sname:
            _add(msgs, "FAIL", f"skill {sname}: name {fm_name!r} does not match dir")
            ok = False
        elif not SKILL_NAME_RE.match(fm_name):
            _add(msgs, "FAIL", f"skill {sname}: name {fm_name!r} does not match ^[a-z0-9]+(-[a-z0-9]+)*$")
            ok = False
        elif not (1 <= len(fm_name) <= 64):
            _add(msgs, "FAIL", f"skill {sname}: name length {len(fm_name)} not in 1..64")
            ok = False
        desc = fm.get("description", "")
        if not desc:
            _add(msgs, "FAIL", f"skill {sname}: description missing")
            ok = False
        elif not (1 <= len(desc) <= 1024):
            _add(msgs, "FAIL", f"skill {sname}: description length {len(desc)} not in 1..1024")
            ok = False
        if (
            fm_name == sname
            and SKILL_NAME_RE.match(fm_name)
            and 1 <= len(fm_name) <= 64
            and 1 <= len(desc) <= 1024
        ):
            _add(msgs, "PASS", f"skill {sname}: frontmatter ok")
    return ok, msgs


def g4_agents_frontmatter() -> GateResult:
    msgs: List[Msg] = []
    ok = True
    if not os.path.isdir(AGENTS_DIR):
        _add(msgs, "WARN", "agents/ absent; skipped")
        return True, msgs
    for entry in sorted(os.listdir(AGENTS_DIR)):
        af = os.path.join(AGENTS_DIR, entry)
        if not os.path.isfile(af) or not af.endswith(".md"):
            continue
        aname = entry[:-3]
        try:
            with open(af, encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            _add(msgs, "FAIL", f"agent {aname}: read error: {e}")
            ok = False
            continue
        if not text.startswith("---"):
            _add(msgs, "FAIL", f"agent {aname}: does not start with ---")
            ok = False
            continue
        fm = parse_frontmatter(text)
        if not fm:
            _add(msgs, "FAIL", f"agent {aname}: frontmatter missing or empty")
            ok = False
            continue
        agent_ok = True
        if "description" not in fm:
            _add(msgs, "FAIL", f"agent {aname}: description missing")
            agent_ok = False
        mode = fm.get("mode")
        if mode is not None and mode not in ALLOWED_MODES:
            _add(msgs, "FAIL", f"agent {aname}: invalid mode {mode!r}; allowed {sorted(ALLOWED_MODES)}")
            agent_ok = False
        perm = fm.get("permission")
        if isinstance(perm, dict):
            for k in perm:
                if k not in ALLOWED_PERMISSIONS:
                    _add(msgs, "FAIL", f"agent {aname}: unknown permission {k!r}")
                    agent_ok = False
        elif perm is not None:
            _add(msgs, "FAIL", f"agent {aname}: permission must be a mapping (got {type(perm).__name__})")
            agent_ok = False
        if not agent_ok:
            ok = False
        else:
            _add(msgs, "PASS", f"agent {aname}: frontmatter ok")
    return ok, msgs


def g5_commands_frontmatter() -> GateResult:
    msgs: List[Msg] = []
    ok = True
    if not os.path.isdir(COMMANDS_DIR):
        _add(msgs, "WARN", "commands/ absent; skipped")
        return True, msgs
    for entry in sorted(os.listdir(COMMANDS_DIR)):
        cf = os.path.join(COMMANDS_DIR, entry)
        if not os.path.isfile(cf) or not cf.endswith(".md"):
            continue
        cname = entry[:-3]
        try:
            with open(cf, encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            _add(msgs, "FAIL", f"command {cname}: read error: {e}")
            ok = False
            continue
        if not text.startswith("---"):
            _add(msgs, "FAIL", f"command {cname}: does not start with ---")
            ok = False
            continue
        fm = parse_frontmatter(text)
        if not fm:
            _add(msgs, "FAIL", f"command {cname}: frontmatter missing or empty")
            ok = False
            continue
        cmd_ok = True
        if "description" not in fm:
            _add(msgs, "FAIL", f"command {cname}: description missing")
            cmd_ok = False
        for k in fm:
            if k not in ALLOWED_COMMAND_KEYS:
                _add(msgs, "FAIL", f"command {cname}: unknown top-level key {k!r}")
                cmd_ok = False
        if not cmd_ok:
            ok = False
        else:
            _add(msgs, "PASS", f"command {cname}: frontmatter ok")
    return ok, msgs


def g6_no_dash_chars() -> GateResult:
    msgs: List[Msg] = []
    ok = True
    hits: List[str] = []
    files_with_hits: set = set()
    for full in _scan_files():
        try:
            with open(full, encoding="utf-8") as f:
                for lineno, line in enumerate(f, 1):
                    if DASH_RE.search(line):
                        rel = os.path.relpath(full, REPO)
                        hits.append(f"{rel}:{lineno}")
                        files_with_hits.add(rel)
        except (UnicodeDecodeError, OSError):
            continue
    if hits:
        ok = False
        for h in hits[:200]:
            _add(msgs, "FAIL", f"em/en-dash at {h}")
        if len(hits) > 200:
            _add(msgs, "FAIL", f"... {len(hits) - 200} more em/en-dash occurrences omitted")
        _add(msgs, "FAIL",
             f"total: {len(hits)} em/en-dash occurrences across {len(files_with_hits)} files")
    else:
        _add(msgs, "PASS", "no em/en-dashes in scanned files")
    return ok, msgs


def g7_no_orphan_skills() -> GateResult:
    msgs: List[Msg] = []
    ok = True
    if not os.path.isfile(PLUGIN_JSON):
        _add(msgs, "WARN", "plugin.json absent; cross-ref check skipped")
    else:
        try:
            with open(PLUGIN_JSON, encoding="utf-8") as f:
                pj = json.load(f)
        except Exception as e:
            _add(msgs, "FAIL", f"plugin.json: parse error during cross-ref: {e}")
            return False, msgs
        listed = pj.get("skills", [])
        if not isinstance(listed, list):
            _add(msgs, "FAIL", "plugin.json: 'skills' must be a list")
            ok = False
        else:
            cross_ok = True
            for s in listed:
                if isinstance(s, str):
                    sname = s
                elif isinstance(s, dict):
                    sname = s.get("name")
                else:
                    sname = None
                if not sname or not isinstance(sname, str):
                    _add(msgs, "FAIL", f"plugin.json: malformed skill entry {s!r}")
                    cross_ok = False
                    continue
                if not os.path.isfile(os.path.join(SKILLS_DIR, sname, "SKILL.md")):
                    _add(msgs, "FAIL",
                         f"plugin.json references skill {sname!r} but skills/{sname}/SKILL.md missing")
                    cross_ok = False
            if cross_ok:
                _add(msgs, "PASS", f"plugin.json: all {len(listed)} referenced skills exist on disk")
            else:
                ok = False
    if not os.path.isdir(SKILLS_DIR):
        _add(msgs, "WARN", "skills/ absent; orphan-dir check skipped")
    else:
        dir_ok = True
        for entry in sorted(os.listdir(SKILLS_DIR)):
            sd = os.path.join(SKILLS_DIR, entry)
            if not os.path.isdir(sd):
                continue
            if not os.path.isfile(os.path.join(sd, "SKILL.md")):
                _add(msgs, "FAIL", f"skills/{entry}/: missing SKILL.md (orphan dir)")
                dir_ok = False
        if dir_ok:
            _add(msgs, "PASS", "every skills/<dir>/ has SKILL.md")
        else:
            ok = False
    return ok, msgs


def g8_eval_json_parses() -> GateResult:
    msgs: List[Msg] = []
    ok = True
    if not os.path.isdir(EVAL_RESULTS):
        _add(msgs, "WARN", "eval/results/ absent; skipped")
        return True, msgs
    any_file = False
    for entry in sorted(os.listdir(EVAL_RESULTS)):
        if not entry.endswith(".json"):
            continue
        any_file = True
        path = os.path.join(EVAL_RESULTS, entry)
        try:
            with open(path, encoding="utf-8") as f:
                json.load(f)
        except Exception as e:
            _add(msgs, "FAIL", f"eval/results/{entry}: parse error: {e}")
            ok = False
            continue
        _add(msgs, "PASS", f"eval/results/{entry}: parses")
    if not any_file:
        _add(msgs, "WARN", "eval/results/ empty; skipped")
    return ok, msgs


def g9_agents_md_budget() -> GateResult:
    msgs: List[Msg] = []
    if not os.path.isfile(AGENTS_MD):
        _add(msgs, "FAIL", "AGENTS.md: file missing")
        return False, msgs
    with open(AGENTS_MD, encoding="utf-8") as f:
        n = sum(1 for _ in f)
    if n > 200:
        _add(msgs, "FAIL", f"AGENTS.md: {n} lines (> 200)")
        return False, msgs
    _add(msgs, "PASS", f"AGENTS.md: {n} lines (<= 200)")
    return True, msgs


def g10_claude_plugin_manifests() -> GateResult:
    """skills.sh / Claude Code plugin manifest gate.

    Validates .claude-plugin/plugin.json and .claude-plugin/marketplace.json, the
    manifests the `skills` CLI (https://skills.sh) and Claude Code honor for skill
    discovery. Each declared skill path must start with './' and resolve on disk.
    The two manifests' top-level version fields must agree when both are present.
    """
    msgs: List[Msg] = []
    ok = True
    have_p = os.path.isfile(CLAUDE_PLUGIN_JSON)
    have_m = os.path.isfile(CLAUDE_MARKETPLACE_JSON)
    if not (have_p or have_m):
        _add(msgs, "WARN", ".claude-plugin/ absent; skills.sh discovery gate skipped")
        return True, msgs

    cp_version: Any = None
    cm_version: Any = None
    declared: List[str] = []

    if have_p:
        try:
            with open(CLAUDE_PLUGIN_JSON, encoding="utf-8") as f:
                pj = json.load(f)
        except Exception as e:
            _add(msgs, "FAIL", f".claude-plugin/plugin.json: parse error: {e}")
            ok = False
            pj = {}
        else:
            cp_version = pj.get("version")
            missing = [k for k in ("name", "version", "description") if k not in pj]
            if missing:
                _add(msgs, "FAIL", f".claude-plugin/plugin.json: missing keys {missing}")
                ok = False
            skills = pj.get("skills", [])
            if not isinstance(skills, list):
                _add(msgs, "FAIL", ".claude-plugin/plugin.json: 'skills' must be a list")
                ok = False
            else:
                for s in skills:
                    if not isinstance(s, str) or not s.startswith("./"):
                        _add(msgs, "FAIL", f".claude-plugin/plugin.json: skill entry {s!r} must be a string starting with './'")
                        ok = False
                        continue
                    declared.append(s)

    if have_m:
        try:
            with open(CLAUDE_MARKETPLACE_JSON, encoding="utf-8") as f:
                mj = json.load(f)
        except Exception as e:
            _add(msgs, "FAIL", f".claude-plugin/marketplace.json: parse error: {e}")
            ok = False
            mj = {}
        else:
            plugins = mj.get("plugins", [])
            if not isinstance(plugins, list) or not plugins:
                _add(msgs, "FAIL", ".claude-plugin/marketplace.json: 'plugins' must be a non-empty list")
                ok = False
            else:
                for plugin in plugins:
                    if not isinstance(plugin, dict):
                        _add(msgs, "FAIL", f".claude-plugin/marketplace.json: plugin entry must be an object, got {type(plugin).__name__}")
                        ok = False
                        continue
                    cm_version = plugin.get("version", cm_version)
                    source = plugin.get("source")
                    if source is not None and (not isinstance(source, str) or not source.startswith("./")):
                        _add(msgs, "FAIL", f".claude-plugin/marketplace.json: plugin source {source!r} must start with './'")
                        ok = False
                    for s in plugin.get("skills", []) or []:
                        if not isinstance(s, str) or not s.startswith("./"):
                            _add(msgs, "FAIL", f".claude-plugin/marketplace.json: skill entry {s!r} must be a string starting with './'")
                            ok = False
                            continue
                        declared.append(s)

    # Every declared skill path resolves to skills/<name>/SKILL.md on disk.
    for s in sorted(set(declared)):
        rel = s[2:] if s.startswith("./") else s
        target = os.path.join(REPO, rel, "SKILL.md") if not rel.endswith("SKILL.md") else os.path.join(REPO, rel)
        if not (os.path.isfile(target) or os.path.isfile(os.path.join(REPO, rel, "SKILL.md"))):
            _add(msgs, "FAIL", f"declared skill {s!r} does not resolve to a SKILL.md on disk")
            ok = False
    if declared and ok:
        _add(msgs, "PASS", f".claude-plugin/: {len(set(declared))} declared skill(s) resolve on disk")

    if have_p and have_m and cp_version and cm_version and cp_version != cm_version:
        _add(msgs, "FAIL", f".claude-plugin version mismatch: plugin.json={cp_version!r} vs marketplace.json={cm_version!r}")
        ok = False
    elif have_p and have_m and cp_version and cm_version:
        _add(msgs, "PASS", f".claude-plugin versions agree ({cp_version})")

    if ok and not declared:
        _add(msgs, "PASS", ".claude-plugin/: manifests parse; no skills declared")
    return ok, msgs


def _validate_cursor_skill_paths(entries: List[str], msgs: List[Msg]) -> bool:
    """Each entry is a relative path that must resolve to a SKILL.md on disk."""
    ok = True
    for s in entries:
        target = os.path.join(REPO, s)
        if not os.path.isfile(target):
            _add(msgs, "FAIL", f".cursor-plugin: declared skill path {s!r} does not resolve on disk")
            ok = False
    return ok


def g11_cursor_plugin_manifests() -> GateResult:
    """Cursor plugin manifest gate.

    Validates .cursor-plugin/plugin.json and .cursor-plugin/marketplace.json per
    https://github.com/cursor/plugins/blob/master/schemas/. The plugin.json
    `name` must be kebab-case (^[a-z0-9]([a-z0-9.-]*[a-z0-9])?$), every declared
    skills/agents/commands path must resolve on disk, and the marketplace.json
    plugin entries must each carry the required {name, source} pair.
    """
    msgs: List[Msg] = []
    ok = True
    have_p = os.path.isfile(CURSOR_PLUGIN_JSON)
    have_m = os.path.isfile(CURSOR_MARKETPLACE_JSON)
    if not (have_p or have_m):
        _add(msgs, "WARN", ".cursor-plugin/ absent; Cursor discovery gate skipped")
        return True, msgs

    cp_name: Any = None
    cp_version: Any = None
    cursor_name_re = re.compile(r"^[a-z0-9]([a-z0-9.-]*[a-z0-9])?$")
    declared_skill_paths: List[str] = []

    if have_p:
        try:
            with open(CURSOR_PLUGIN_JSON, encoding="utf-8") as f:
                pj = json.load(f)
        except Exception as e:
            _add(msgs, "FAIL", f".cursor-plugin/plugin.json: parse error: {e}")
            ok = False
            pj = {}
        else:
            cp_name = pj.get("name")
            cp_version = pj.get("version")
            if not cp_name:
                _add(msgs, "FAIL", ".cursor-plugin/plugin.json: 'name' missing")
                ok = False
            elif not cursor_name_re.match(str(cp_name)):
                _add(msgs, "FAIL", f".cursor-plugin/plugin.json: name {cp_name!r} must match {cursor_name_re.pattern}")
                ok = False
            if "version" not in pj:
                _add(msgs, "FAIL", ".cursor-plugin/plugin.json: 'version' missing")
                ok = False
            if "description" not in pj:
                _add(msgs, "FAIL", ".cursor-plugin/plugin.json: 'description' missing")
                ok = False

            for key in ("skills", "agents", "commands"):
                entries = pj.get(key)
                if entries is None:
                    continue
                if isinstance(entries, str):
                    entries = [entries]
                if not isinstance(entries, list):
                    _add(msgs, "FAIL", f".cursor-plugin/plugin.json: '{key}' must be a string or array of strings")
                    ok = False
                    continue
                for e in entries:
                    if not isinstance(e, str) or not e:
                        _add(msgs, "FAIL", f".cursor-plugin/plugin.json: '{key}' entry {e!r} must be a non-empty string")
                        ok = False
                        continue
                    target = os.path.join(REPO, e)
                    if not os.path.isfile(target):
                        _add(msgs, "FAIL", f".cursor-plugin/plugin.json: '{key}' path {e!r} does not resolve on disk")
                        ok = False
                    elif key == "skills":
                        declared_skill_paths.append(e)

    cm_name: Any = None
    if have_m:
        try:
            with open(CURSOR_MARKETPLACE_JSON, encoding="utf-8") as f:
                mj = json.load(f)
        except Exception as e:
            _add(msgs, "FAIL", f".cursor-plugin/marketplace.json: parse error: {e}")
            ok = False
            mj = {}
        else:
            if not mj.get("name"):
                _add(msgs, "FAIL", ".cursor-plugin/marketplace.json: 'name' missing")
                ok = False
            else:
                cm_name = mj["name"]
            plugins = mj.get("plugins")
            if not isinstance(plugins, list) or not plugins:
                _add(msgs, "FAIL", ".cursor-plugin/marketplace.json: 'plugins' must be a non-empty list")
                ok = False
            else:
                for plugin in plugins:
                    if not isinstance(plugin, dict):
                        _add(msgs, "FAIL", f".cursor-plugin/marketplace.json: plugin entry must be an object, got {type(plugin).__name__}")
                        ok = False
                        continue
                    missing = [k for k in ("name", "source") if k not in plugin]
                    if missing:
                        _add(msgs, "FAIL", f".cursor-plugin/marketplace.json: plugin entry missing required keys {missing}")
                        ok = False
                        continue
                    if not cursor_name_re.match(str(plugin["name"])):
                        _add(msgs, "FAIL", f".cursor-plugin/marketplace.json: plugin name {plugin['name']!r} must match {cursor_name_re.pattern}")
                        ok = False
                    if have_p and cp_name and plugin["name"] != cp_name:
                        _add(msgs, "FAIL", f".cursor-plugin: marketplace plugin name {plugin['name']!r} != plugin.json name {cp_name!r}")
                        ok = False

    if declared_skill_paths and ok:
        _add(msgs, "PASS", f".cursor-plugin/plugin.json: {len(declared_skill_paths)} skill path(s) resolve on disk")
    elif have_p and not declared_skill_paths and ok:
        _add(msgs, "PASS", ".cursor-plugin/plugin.json: parses; name ok; no skill paths declared")
    if have_m and ok and cm_name:
        _add(msgs, "PASS", f".cursor-plugin/marketplace.json: parses; marketplace name {cm_name!r}")
    return ok, msgs


GEMINI_NAME_RE = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")


def g12_gemini_extension_manifest() -> GateResult:
    """Gemini CLI extension manifest gate.

    Validates gemini-extension.json per https://geminicli.com/docs/extensions/reference/.
    Requires `name` (lowercase, hyphenated, matches extension dir name when
    installed) and `version`; optional `description`, `contextFileName`,
    `mcpServers`, `settings`. The name must match ^[a-z0-9]([a-z0-9-]*[a-z0-9])?$
    per Gemini CLI convention.
    """
    msgs: List[Msg] = []
    if not os.path.isfile(GEMINI_EXTENSION_JSON):
        _add(msgs, "WARN", "gemini-extension.json absent; Gemini CLI extension gate skipped")
        return True, msgs
    try:
        with open(GEMINI_EXTENSION_JSON, encoding="utf-8") as f:
            gj = json.load(f)
    except Exception as e:
        _add(msgs, "FAIL", f"gemini-extension.json: parse error: {e}")
        return False, msgs

    ok = True
    name = gj.get("name")
    if not name:
        _add(msgs, "FAIL", "gemini-extension.json: 'name' missing")
        ok = False
    elif not isinstance(name, str) or not GEMINI_NAME_RE.match(name):
        _add(msgs, "FAIL", f"gemini-extension.json: name {name!r} must match {GEMINI_NAME_RE.pattern}")
        ok = False

    if "version" not in gj:
        _add(msgs, "FAIL", "gemini-extension.json: 'version' missing")
        ok = False
    if "description" not in gj:
        _add(msgs, "FAIL", "gemini-extension.json: 'description' missing")
        ok = False

    mcp = gj.get("mcpServers")
    if mcp is not None and not isinstance(mcp, dict):
        _add(msgs, "FAIL", f"gemini-extension.json: 'mcpServers' must be an object, got {type(mcp).__name__}")
        ok = False

    settings = gj.get("settings")
    if settings is not None:
        if not isinstance(settings, list):
            _add(msgs, "FAIL", f"gemini-extension.json: 'settings' must be an array, got {type(settings).__name__}")
            ok = False
        elif not all(isinstance(s, dict) and "name" in s and "envVar" in s for s in settings):
            _add(msgs, "FAIL", "gemini-extension.json: each 'settings' entry needs at least {name, envVar}")
            ok = False

    if ok:
        _add(msgs, "PASS", f"gemini-extension.json: parses; name {name!r}; version {gj.get('version')!r}")
    return ok, msgs


def g13_plugin_symlinks() -> GateResult:
    """Plugin source-of-truth invariant gate.

    The repo's plugin manifests live canonically under .agents/plugins/<tool>/
    and are surfaced at their tool-discovery paths via symlinks. This gate
    enforces that contract so a future contributor cannot accidentally edit the
    symlink target and create a fork between the published location and the
    source of truth.

    Required symlinks (each resolves to .agents/plugins/<tool>/<file>):
      .claude-plugin/plugin.json       -> .agents/plugins/claude/plugin.json
      .claude-plugin/marketplace.json  -> .agents/plugins/claude/marketplace.json
      .cursor-plugin/plugin.json       -> .agents/plugins/cursor/plugin.json
      .cursor-plugin/marketplace.json  -> .agents/plugins/cursor/marketplace.json
      gemini-extension.json            -> .agents/plugins/gemini/gemini-extension.json
      plugin.json                      -> .agents/plugins/legacy/plugin.json
      marketplace.json                 -> .agents/plugins/legacy/marketplace.json
    """
    msgs: List[Msg] = []
    expected = {
        ".claude-plugin/plugin.json": ".agents/plugins/claude/plugin.json",
        ".claude-plugin/marketplace.json": ".agents/plugins/claude/marketplace.json",
        ".cursor-plugin/plugin.json": ".agents/plugins/cursor/plugin.json",
        ".cursor-plugin/marketplace.json": ".agents/plugins/cursor/marketplace.json",
        "gemini-extension.json": ".agents/plugins/gemini/gemini-extension.json",
        "plugin.json": ".agents/plugins/legacy/plugin.json",
        "marketplace.json": ".agents/plugins/legacy/marketplace.json",
    }
    ok = True
    for link_rel, target_rel in expected.items():
        link = os.path.join(REPO, link_rel)
        target = os.path.join(REPO, target_rel)
        if not os.path.islink(link):
            _add(msgs, "FAIL", f"{link_rel}: expected a symlink -> {target_rel}, found a real file or missing")
            ok = False
            continue
        actual = os.path.normpath(os.readlink(link))
        # Accept either the relative form we wrote or any form that resolves to the same file.
        same = (
            actual == target_rel
            or actual == os.path.normpath(target_rel)
            or os.path.realpath(link) == os.path.realpath(target)
        )
        if not same:
            _add(msgs, "FAIL", f"{link_rel}: symlink -> {actual}, expected -> {target_rel}")
            ok = False
            continue
        if not os.path.isfile(target):
            _add(msgs, "FAIL", f"{link_rel}: symlink target {target_rel} does not exist")
            ok = False
            continue
        _add(msgs, "PASS", f"{link_rel} -> {target_rel}")
    return ok, msgs


GATES: List[Tuple[str, Callable[[], GateResult]]] = [
    ("G1_manifests_parse", g1_manifests_parse),
    ("G2_versions_agree", g2_versions_agree),
    ("G3_skills_frontmatter", g3_skills_frontmatter),
    ("G4_agents_frontmatter", g4_agents_frontmatter),
    ("G5_commands_frontmatter", g5_commands_frontmatter),
    ("G6_no_dash_chars", g6_no_dash_chars),
    ("G7_no_orphan_skills", g7_no_orphan_skills),
    ("G8_eval_json_parses", g8_eval_json_parses),
    ("G9_agents_md_budget", g9_agents_md_budget),
    ("G10_claude_plugin_manifests", g10_claude_plugin_manifests),
    ("G11_cursor_plugin_manifests", g11_cursor_plugin_manifests),
    ("G12_gemini_extension_manifest", g12_gemini_extension_manifest),
    ("G13_plugin_symlinks", g13_plugin_symlinks),
]


HELP_EPILOG = """Gates (in order):
  G1_manifests_parse        plugin.json + marketplace.json parse, required keys
  G2_versions_agree         plugin.json.version == marketplace.json.plugins[0].version
  G3_skills_frontmatter     every skills/<name>/SKILL.md: name+description, valid shape
  G4_agents_frontmatter     every agents/<name>.md: description; mode in allowed set;
                            permission sub-keys in allowed set
  G5_commands_frontmatter   every commands/<name>.md: description; no unknown top-level keys
  G6_no_dash_chars          no em-dash (U+2014) or en-dash (U+2013) in scanned files
  G7_no_orphan_skills       plugin.json skill refs exist; every skills/<dir>/ has SKILL.md
  G8_eval_json_parses       eval/results/*.json parse as JSON
  G9_agents_md_budget       AGENTS.md line count <= 200
  G10_claude_plugin         .claude-plugin/{plugin,marketplace}.json (skills.sh / Claude Code)
                            parse; skills start with './'; declared skills resolve on disk
  G11_cursor_plugin         .cursor-plugin/{plugin,marketplace}.json (Cursor marketplace)
                            parse; kebab-case name; skills/agents/commands paths resolve
  G12_gemini_extension      gemini-extension.json (Gemini CLI extension) parses;
                            name matches ^[a-z0-9]([a-z0-9-]*[a-z0-9])?$; required keys present
  G13_plugin_symlinks       discovery-path manifests (.claude-plugin/*, .cursor-plugin/*,
                            gemini-extension.json, plugin.json, marketplace.json) are symlinks
                            into .agents/plugins/<tool>/ -- the source-of-truth location

Optional-file gates (G1, G2, G7 cross-ref half, G8, G10, G11, G12) WARN (not
FAIL) when the expected file or directory is absent, so this validator can run
before the parallel packaging units (manifests, eval seed, new skills) land.

Default behavior: abort on the first failing gate. Pass --all to run every
gate and report all failures before exiting non-zero.
"""


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="checks.py",
        description="Repo validator for the agents config (13 deterministic gates).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=HELP_EPILOG,
    )
    parser.add_argument("--all", action="store_true",
                        help="Run every gate; do not abort on first failure.")
    args = parser.parse_args(argv)

    any_fail = False
    n_pass = n_fail = n_warn = 0

    for name, gate in GATES:
        print(f"--- {name} ---")
        ok, msgs = gate()
        if not msgs:
            _add(msgs, "PASS", "no checks performed")
        for level, msg in msgs:
            tag = {"PASS": "[PASS]", "FAIL": "[FAIL]", "WARN": "[WARN]"}[level]
            stream = sys.stderr if level == "FAIL" else sys.stdout
            print(f"{tag} {msg}", file=stream)
            if level == "PASS":
                n_pass += 1
            elif level == "FAIL":
                n_fail += 1
            else:
                n_warn += 1
        if not ok:
            any_fail = True
            if not args.all:
                print(
                    f"\nGate {name} failed; aborting (use --all to run all gates).",
                    file=sys.stderr,
                )
                return 1

    print()
    if any_fail:
        print(f"{n_fail} checks failed ({n_warn} warnings, {n_pass} passes)")
        return 1
    print(f"All {n_pass} checks passed ({n_warn} warnings)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
