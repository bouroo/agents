#!/usr/bin/env python3
"""scripts/checks.py - Repo validator for fable-plugin-refactor.

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
]


HELP_EPILOG = """Gates (in order):
  G1_manifests_parse       plugin.json + marketplace.json parse, required keys
  G2_versions_agree        plugin.json.version == marketplace.json.plugins[0].version
  G3_skills_frontmatter    every skills/<name>/SKILL.md: name+description, valid shape
  G4_agents_frontmatter    every agents/<name>.md: description; mode in allowed set;
                           permission sub-keys in allowed set
  G5_commands_frontmatter  every commands/<name>.md: description; no unknown top-level keys
  G6_no_dash_chars         no em-dash (U+2014) or en-dash (U+2013) in scanned files
  G7_no_orphan_skills      plugin.json skill refs exist; every skills/<dir>/ has SKILL.md
  G8_eval_json_parses      eval/results/*.json parse as JSON
  G9_agents_md_budget      AGENTS.md line count <= 200

Optional-file gates (G1, G2, G7 cross-ref half, G8) WARN (not FAIL) when the
expected file or directory is absent, so this validator can run before the
parallel packaging units (manifests, eval seed, new skills) land.

Default behavior: abort on the first failing gate. Pass --all to run every
gate and report all failures before exiting non-zero.
"""


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="checks.py",
        description="Repo validator for fable-plugin-refactor (9 deterministic gates).",
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
