#!/usr/bin/env python3
"""scripts/checks.py - Repo validator for the agents config (V3).

Deterministic gates; exits non-zero on any failure. The gate count is
authoritative only via `--help` (derived from the GATES registry), never
hand-maintained in prose.

Gates that depend on optional files WARN (not FAIL) when those files are
absent, so the validator runs before packaging lands.

Usage:
    python3 scripts/checks.py [--all] [--help]

Exit codes:
    0  every gate PASS or WARN (no FAIL)
    1  at least one gate FAIL
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

AGENTS_DIR = ROOT / "agents"
COMMAND_DIR = ROOT / "commands"
SKILLS_DIR = ROOT / "skills"
EVAL_RESULTS = ROOT / "eval" / "results"
REGISTRIES = ROOT / "registries"
MANIFEST_DIR = ROOT / "adapters" / "manifests"

ALLOWED_MODES = {"primary", "subagent"}
ALLOWED_AGENT_PERM_KEYS = {"read", "glob", "grep", "edit", "bash", "task", "web", "external_directory", "color", "steps", "team", "icon"}
ALLOWED_COMMAND_KEYS = {"name", "description", "phase", "invocable_as", "agent", "model", "argument-hint"}
ALLOWED_PHASES = {"THINK", "ACT", "PROVE", "GROW", "ANYTIME"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
AGENTS_MD_BUDGET = 220

# G17: host-binding tokens forbidden in the agnostic core. Dotdirs, host config
# filenames, and plugin-manifest paths are unambiguous signals of a host leak.
HOST_TOKEN_RE = re.compile(
    r"\.claude|\.cursor|\.gemini|\.codex|\.qwen|\.kilo|"
    r"\.claude-plugin|\.cursor-plugin|gemini-extension|"
    r"\bCLAUDE\.md\b|\bGEMINI\.md\b|"
    r"\bopencode\b|\bkilo\b|\bantigravity\b|\bcodex\b|\bqwen\b",
    re.IGNORECASE,
)
# Core files scanned for host tokens. registries/, adapters/, eval/, scripts/,
# README, CHANGELOG are excluded -- they are the data/distribution/docs layer.
CORE_HOST_SCAN_GLOBS = ["AGENTS.md", "agents/*.md", "commands/*.md", "skills/*/SKILL.md", "skills/*/references/*.md"]
# Domain adapters may name their host/tool legitimately (Go, Confluence/Atlassian,
# OpenAPI tooling). They are excluded from the core-agnosticism scan.
ADAPTER_SKILLS = {"go-essential", "openapi-spec", "confluence"}
CORE_HOST_SCAN_EXCLUDE = [f"skills/{s}/" for s in ADAPTER_SKILLS]

# G18: host-only argument features that break cross-host portability. The split
# is behavioral vs. cosmetic:
#   `arguments:`  defines Claude-only `$name` substitution opencode/others do not
#                 perform -> a `$name` token silently leaks into the prompt.
#                 FUNCTIONAL -> banned on every invokable surface.
#   $ARGUMENTS[N] indexed access with a host-specific origin (0 vs 1 based).
#                 FUNCTIONAL -> banned on every invokable surface.
#   `argument-hint:` a cosmetic autocomplete hint. Claude Code reads it; every
#                 other host ignores the unknown frontmatter key, and commands
#                 are NOT Agent-Skills-spec artifacts, so it never hits the spec
#                 validator. INERT on commands -> allowed there. On skills it IS
#                 in the spec's frontmatter set ({name, description, license,
#                 compatibility, metadata, allowed-tools}) and fails packaging on
#                 hosted skill markets / the API -> banned there.
BEHAVIORAL_ARG_FM = {"arguments"}              # banned on commands and skills
SPEC_BREAKING_ARG_FM = {"argument-hint", "arguments"}  # banned on skills only
NONPORTABLE_ARG_TOKEN_RE = re.compile(r"\$ARGUMENTS\[")
INVOKABLE_SCAN_GLOBS = {
    "commands/*.md": BEHAVIORAL_ARG_FM,
    "skills/*/SKILL.md": SPEC_BREAKING_ARG_FM,
}

Msg = tuple[str, str]  # (level, message); level in {PASS, FAIL, WARN}
_msgs: list[Msg] = []


def _add(level: str, msg: str) -> None:
    _msgs.append((level, msg))


def _frontmatter(path: pathlib.Path) -> tuple[dict, str]:
    text = path.read_text()
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_text = text[3:end]
    fm: dict = {}
    for line in fm_text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if ":" not in s:
            continue
        k, v = s.split(":", 1)
        fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, text


# ---------------------------------------------------------------------------
# G1  manifests parse (legacy root -> adapters/manifests/legacy)
# ---------------------------------------------------------------------------


def G1_manifests_parse() -> None:
    name = "G1_manifests_parse"
    pj = MANIFEST_DIR / "legacy" / "plugin.json"
    mj = MANIFEST_DIR / "legacy" / "marketplace.json"
    for p in (pj, mj):
        if not p.exists():
            _add("WARN", f"{name}: {p.relative_to(ROOT)} missing (optional for now)")
            return
    try:
        plugin = json.loads(pj.read_text())
    except (ValueError, OSError) as e:  # JSONDecodeError/UnicodeDecodeError are ValueError
        _add("FAIL", f"{name}: parse error: {e}")
        return
    for req in ("name", "version", "description"):
        if req not in plugin:
            _add("FAIL", f"{name}: plugin.json missing required key {req!r}")
            return
    _add("PASS", f"{name}: legacy manifests parse and have required keys")


# ---------------------------------------------------------------------------
# G2  versions agree (legacy plugin vs marketplace)
# ---------------------------------------------------------------------------


def G2_versions_agree() -> None:
    name = "G2_versions_agree"
    pj = MANIFEST_DIR / "legacy" / "plugin.json"
    mj = MANIFEST_DIR / "legacy" / "marketplace.json"
    if not (pj.exists() and mj.exists()):
        _add("WARN", f"{name}: legacy manifests absent")
        return
    try:
        pv = json.loads(pj.read_text()).get("version")
        mv = json.loads(mj.read_text()).get("version")
    except (ValueError, OSError) as e:
        _add("FAIL", f"{name}: parse error: {e}")
        return
    if not pv or not mv:
        _add("FAIL", f"{name}: missing version (plugin={pv!r}, market={mv!r})")
        return
    if pv != mv:
        _add("FAIL", f"{name}: plugin.json {pv!r} != marketplace.json {mv!r}")
        return
    _add("PASS", f"{name}: plugin/marketplace versions agree ({pv})")


# ---------------------------------------------------------------------------
# G3  skills frontmatter (skills/**/SKILL.md incl adapters)
# ---------------------------------------------------------------------------


def G3_skills_frontmatter() -> None:
    name = "G3_skills_frontmatter"
    if not SKILLS_DIR.exists():
        _add("WARN", f"{name}: skills/ absent")
        return
    skills = sorted(SKILLS_DIR.rglob("SKILL.md"))
    if not skills:
        _add("WARN", f"{name}: no skills found")
        return
    ok = True
    for md in skills:
        rel = md.relative_to(ROOT)
        sname = md.parent.name
        try:
            fm, _ = _frontmatter(md)
        except (ValueError, OSError) as e:
            _add("FAIL", f"{name}: {rel}: read error: {e}")
            ok = False
            continue
        if not md.read_text().startswith("---"):
            _add("FAIL", f"{name}: {rel}: does not start with ---")
            ok = False
            continue
        fname = fm.get("name")
        if not fname:
            _add("FAIL", f"{name}: {rel}: name field missing")
            ok = False
            continue
        if fname != sname:
            _add("FAIL", f"{name}: {rel}: name {fname!r} != dir {sname!r}")
            ok = False
            continue
        if not NAME_RE.match(fname):
            _add("FAIL", f"{name}: {rel}: name {fname!r} not kebab-case")
            ok = False
            continue
        if not (1 <= len(fname) <= 64):
            _add("FAIL", f"{name}: {rel}: name length {len(fname)} not in 1..64")
            ok = False
            continue
        desc = fm.get("description")
        if not desc or not (1 <= len(desc) <= 1024):
            _add("FAIL", f"{name}: {rel}: description length not in 1..1024")
            ok = False
    if ok:
        _add("PASS", f"{name}: {len(skills)} skill(s) frontmatter valid")


# ---------------------------------------------------------------------------
# G4  agents frontmatter (agents/*/SKILL.md)
# ---------------------------------------------------------------------------


def G4_agents_frontmatter() -> None:
    name = "G4_agents_frontmatter"
    # flat agents/<name>.md (native discovery); exclude nested references/*.md
    agents = sorted(p for p in AGENTS_DIR.glob("*.md"))
    if not agents:
        _add("WARN", f"{name}: no agents found")
        return
    ok = True
    for md in agents:
        rel = md.relative_to(ROOT)
        aname = md.stem
        try:
            fm, _ = _frontmatter(md)
        except (ValueError, OSError) as e:
            _add("FAIL", f"{name}: {rel}: read error: {e}")
            ok = False
            continue
        if not md.read_text().startswith("---"):
            _add("FAIL", f"{name}: {rel}: does not start with ---")
            ok = False
            continue
        if not fm.get("description"):
            _add("FAIL", f"{name}: {rel}: description missing")
            ok = False
            continue
        fname = fm.get("name", aname)
        if fname and fname != aname:
            _add("FAIL", f"{name}: {rel}: name {fname!r} != file stem {aname!r}")
            ok = False
            continue
        mode = fm.get("mode", "primary")
        if mode not in ALLOWED_MODES:
            _add("FAIL", f"{name}: {rel}: invalid mode {mode!r}; allowed {sorted(ALLOWED_MODES)}")
            ok = False
    if ok:
        _add("PASS", f"{name}: {len(agents)} agent(s) frontmatter valid")


# ---------------------------------------------------------------------------
# G5  commands frontmatter (command/*/SKILL.md)
# ---------------------------------------------------------------------------


def G5_commands_frontmatter() -> None:
    name = "G5_commands_frontmatter"
    # flat commands/<name>.md (native discovery); exclude nested references/*.md
    cmds = sorted(COMMAND_DIR.glob("*.md"))
    if not cmds:
        _add("WARN", f"{name}: no commands found")
        return
    ok = True
    for md in cmds:
        rel = md.relative_to(ROOT)
        try:
            fm, _ = _frontmatter(md)
        except (ValueError, OSError) as e:
            _add("FAIL", f"{name}: {rel}: read error: {e}")
            ok = False
            continue
        if not md.read_text().startswith("---"):
            _add("FAIL", f"{name}: {rel}: does not start with ---")
            ok = False
            continue
        if not fm.get("description"):
            _add("FAIL", f"{name}: {rel}: description missing")
            ok = False
            continue
        for k in fm:
            if k not in ALLOWED_COMMAND_KEYS:
                _add("FAIL", f"{name}: {rel}: unknown top-level key {k!r}")
                ok = False
        phase = fm.get("phase")
        if phase and phase not in ALLOWED_PHASES:
            _add("FAIL", f"{name}: {rel}: phase {phase!r} not in {sorted(ALLOWED_PHASES)}")
            ok = False
    if ok:
        _add("PASS", f"{name}: {len(cmds)} command(s) frontmatter valid")


# ---------------------------------------------------------------------------
# G6  no em/en-dash characters
# ---------------------------------------------------------------------------


def G6_no_dash_chars() -> None:
    name = "G6_no_dash_chars"
    globs = ["AGENTS.md", "README.md", "CHANGELOG.md", "agents/**/*.md", "commands/**/*.md",
             "skills/**/*.md", "registries/*", "scripts/*.py"]
    hits = []
    for pat in globs:
        for p in ROOT.glob(pat):
            if not p.is_file():
                continue
            try:
                text = p.read_text()
            except (ValueError, OSError) as e:
                _add("WARN", f"{name}: skip {p.relative_to(ROOT)} (unreadable: {e})")
                continue
            for i, line in enumerate(text.splitlines(), 1):
                for col, ch in enumerate(line):
                    if ch in (chr(0x2014), chr(0x2013)):
                        hits.append((p.relative_to(ROOT), i, col))
                        if len(hits) > 200:
                            break
                if len(hits) > 200:
                    break
            if len(hits) > 200:
                break
        if len(hits) > 200:
            break
    if hits:
        sample = ", ".join(f"{h[0]}:{h[1]}" for h in hits[:10])
        more = f" ... {len(hits) - 10} more" if len(hits) > 10 else ""
        _add("FAIL", f"{name}: em/en-dash found at {sample}{more}")
        return
    _add("PASS", f"{name}: no em/en-dash characters")


# ---------------------------------------------------------------------------
# G7  no orphan skills (legacy plugin.json skill refs resolve)
# ---------------------------------------------------------------------------


def G7_no_orphan_skills() -> None:
    name = "G7_no_orphan_skills"
    pj = MANIFEST_DIR / "legacy" / "plugin.json"
    if not pj.exists():
        _add("WARN", f"{name}: legacy plugin.json absent")
        return
    try:
        skills = json.loads(pj.read_text()).get("skills", [])
    except (ValueError, OSError) as e:
        _add("FAIL", f"{name}: legacy plugin.json parse error: {e}")
        return
    ok = True
    for s in skills:
        target = SKILLS_DIR / s / "SKILL.md"
        if not target.exists():
            _add("FAIL", f"{name}: declared skill {s!r} -> {target.relative_to(ROOT)} missing")
            ok = False
    # every on-disk skill dir has a SKILL.md
    for d in [p for p in SKILLS_DIR.rglob("*") if p.is_dir()]:
        # allow nested dirs that contain a skill deeper (e.g. adapters/ itself)
        if not (d / "SKILL.md").exists() and not any(d.rglob("SKILL.md")) and d.parent != SKILLS_DIR:
            continue
    if ok:
        _add("PASS", f"{name}: {len(skills)} declared skill(s) resolve")


# ---------------------------------------------------------------------------
# G8  eval json parses
# ---------------------------------------------------------------------------


def G8_eval_json_parses() -> None:
    name = "G8_eval_json_parses"
    if not EVAL_RESULTS.exists():
        _add("WARN", f"{name}: eval/results/ absent")
        return
    files = sorted(EVAL_RESULTS.glob("*.json"))
    if not files:
        _add("WARN", f"{name}: no eval result files")
        return
    ok = True
    for f in files:
        try:
            json.loads(f.read_text())
        except (ValueError, OSError) as e:
            _add("FAIL", f"{name}: eval/results/{f.name}: parse error: {e}")
            ok = False
    if ok:
        _add("PASS", f"{name}: {len(files)} eval result(s) parse")


# ---------------------------------------------------------------------------
# G9  AGENTS.md line budget
# ---------------------------------------------------------------------------


def G9_agents_md_budget() -> None:
    name = "G9_agents_md_budget"
    p = ROOT / "AGENTS.md"
    if not p.exists():
        _add("FAIL", f"{name}: AGENTS.md missing")
        return
    n = len(p.read_text().splitlines())
    if n > AGENTS_MD_BUDGET:
        _add("FAIL", f"{name}: AGENTS.md {n} lines (> {AGENTS_MD_BUDGET})")
        return
    _add("PASS", f"{name}: AGENTS.md {n} lines (<= {AGENTS_MD_BUDGET})")


# ---------------------------------------------------------------------------
# G10 claude plugin manifests
# ---------------------------------------------------------------------------


def G10_claude_plugin_manifests() -> None:
    name = "G10_claude_plugin_manifests"
    pj = ROOT / ".claude-plugin" / "plugin.json"
    mj = ROOT / ".claude-plugin" / "marketplace.json"
    if not (pj.exists() and mj.exists()):
        _add("WARN", f"{name}: .claude-plugin/ absent")
        return
    try:
        plugin = json.loads(pj.read_text())
    except (ValueError, OSError) as e:
        _add("FAIL", f"{name}: plugin.json parse error: {e}")
        return
    skills = plugin.get("skills", [])
    if not isinstance(skills, list):
        _add("FAIL", f"{name}: plugin.json 'skills' must be a list")
        return
    ok = True
    for s in skills:
        if not (isinstance(s, str) and s.startswith("./")):
            _add("FAIL", f"{name}: skill entry {s!r} must start with './'")
            ok = False
            continue
        target = ROOT / s[2:] / "SKILL.md"
        if not target.exists():
            _add("FAIL", f"{name}: declared skill {s!r} does not resolve to a SKILL.md")
            ok = False
    try:
        market = json.loads(mj.read_text())
        cp_version = plugin.get("version")
        cm_version = market.get("plugins", [{}])[0].get("version")
        if cp_version != cm_version:
            _add("FAIL", f"{name}: version mismatch plugin={cp_version!r} market={cm_version!r}")
            ok = False
    except (ValueError, OSError) as e:
        _add("FAIL", f"{name}: marketplace.json parse error: {e}")
        ok = False
    if ok:
        _add("PASS", f"{name}: {len(skills)} claude skill(s) resolve, versions agree")


# ---------------------------------------------------------------------------
# G11 cursor plugin manifests
# ---------------------------------------------------------------------------


def G11_cursor_plugin_manifests() -> None:
    name = "G11_cursor_plugin_manifests"
    pj = ROOT / ".cursor-plugin" / "plugin.json"
    if not pj.exists():
        _add("WARN", f"{name}: .cursor-plugin/ absent")
        return
    try:
        plugin = json.loads(pj.read_text())
    except (ValueError, OSError) as e:
        _add("FAIL", f"{name}: plugin.json parse error: {e}")
        return
    if not NAME_RE.match(plugin.get("name", "")):
        _add("FAIL", f"{name}: name {plugin.get('name')!r} not kebab-case")
        return
    ok = True
    for key in ("skills", "agents", "commands"):
        for entry in plugin.get(key, []) or []:
            target = ROOT / entry
            if not target.exists():
                _add("FAIL", f"{name}: declared {key} path {entry!r} does not resolve")
                ok = False
    if ok:
        _add("PASS", f"{name}: cursor manifest paths resolve")


# ---------------------------------------------------------------------------
# G12 gemini extension manifest
# ---------------------------------------------------------------------------


GEMINI_NAME_RE = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")


def G12_gemini_extension_manifest() -> None:
    name = "G12_gemini_extension_manifest"
    p = ROOT / "gemini-extension.json"
    if not p.exists():
        _add("WARN", f"{name}: gemini-extension.json absent")
        return
    try:
        doc = json.loads(p.read_text())
    except (ValueError, OSError) as e:
        _add("FAIL", f"{name}: parse error: {e}")
        return
    nm = doc.get("name")
    if not nm or not GEMINI_NAME_RE.match(nm):
        _add("FAIL", f"{name}: name {nm!r} invalid")
        return
    for req in ("version", "description"):
        if req not in doc:
            _add("FAIL", f"{name}: missing key {req!r}")
            return
    if not isinstance(doc.get("mcpServers", {}), dict):
        _add("FAIL", f"{name}: mcpServers must be an object")
        return
    _add("PASS", f"{name}: gemini-extension.json valid")


# ---------------------------------------------------------------------------
# G13  discovery-path manifests are symlinks into adapters/manifests/<host>/
# ---------------------------------------------------------------------------


def G13_plugin_symlinks() -> None:
    name = "G13_plugin_symlinks"
    links = {
        ".claude-plugin/plugin.json": "adapters/manifests/claude/plugin.json",
        ".claude-plugin/marketplace.json": "adapters/manifests/claude/marketplace.json",
        ".cursor-plugin/plugin.json": "adapters/manifests/cursor/plugin.json",
        ".cursor-plugin/marketplace.json": "adapters/manifests/cursor/marketplace.json",
        "gemini-extension.json": "adapters/manifests/gemini/gemini-extension.json",
        "plugin.json": "adapters/manifests/legacy/plugin.json",
        "marketplace.json": "adapters/manifests/legacy/marketplace.json",
    }
    ok = True
    for link_rel, target_rel in links.items():
        link = ROOT / link_rel
        target = ROOT / target_rel
        if not link.is_symlink():
            _add("FAIL", f"{name}: {link_rel}: expected a symlink -> {target_rel}, found a real file or missing")
            ok = False
            continue
        actual = pathlib.Path(link.readlink())
        # Resolve the link target the way the OS does: relative to the link's own
        # directory. Accept relative ("adapters/...") and parent-relative
        # ("../adapters/...") targets as long as they resolve to the expected file.
        resolved = (link.parent / actual).resolve()
        if resolved != target.resolve():
            _add("FAIL", f"{name}: {link_rel}: symlink -> {actual} (resolves {resolved}), "
                         f"expected -> {target_rel} ({target.resolve()})")
            ok = False
            continue
        if not target.exists():
            _add("FAIL", f"{name}: {link_rel}: symlink target {target_rel} does not exist")
            ok = False
    if ok:
        _add("PASS", f"{name}: {len(links)} discovery symlinks target adapters/manifests/")


# ---------------------------------------------------------------------------
# G14  frontmatter colon-safe (no unquoted ' : ' in scalar values)
# ---------------------------------------------------------------------------


def G14_frontmatter_colon_safe() -> None:
    name = "G14_frontmatter_colon_safe"
    files = []
    for pat in ("agents/*.md", "commands/*.md", "skills/*/SKILL.md"):
        files.extend(ROOT.glob(pat))
    bad = []
    for md in files:
        rel = md.relative_to(ROOT)
        text = md.read_text()
        if not text.startswith("---"):
            continue
        end = text.find("\n---", 3)
        if end == -1:
            continue
        for i, line in enumerate(text[3:end].splitlines(), 1):
            s = line.strip()
            if not s or s.startswith("#") or ":" not in s:
                continue
            _, v = s.split(":", 1)
            v = v.strip()
            if v.startswith('"') and v.endswith('"'):
                continue
            if ": " in v:
                bad.append((rel, i, line))
    if bad:
        sample = "; ".join(f"{b[0]}:{b[1]}" for b in bad[:10])
        _add("FAIL", f"{name}: frontmatter value contains unquoted ': ' at {sample}")
        return
    _add("PASS", f"{name}: frontmatter scalars are colon-safe")


# ---------------------------------------------------------------------------
# G15  manifests generated (no hand-edits drift from gen-manifests.py)
# ---------------------------------------------------------------------------


def G15_manifests_generated() -> None:
    name = "G15_manifests_generated"
    gen = ROOT / "scripts" / "gen-manifests.py"
    if not gen.exists():
        _add("FAIL", f"{name}: scripts/gen-manifests.py missing")
        return
    try:
        proc = subprocess.run(
            [sys.executable, str(gen), "--check"],
            capture_output=True, text=True,
        )
    except OSError as e:
        _add("FAIL", f"{name}: gen-manifests.py --check failed to run: {e}")
        return
    if proc.returncode != 0:
        _add("FAIL", f"{name}: checked-in manifests differ from generated output; "
                     f"regenerate with 'python3 scripts/gen-manifests.py'")
        return
    _add("PASS", f"{name}: manifests match generated output")


# ---------------------------------------------------------------------------
# G16  registries parse (registries/*.json)
# ---------------------------------------------------------------------------


def G16_registries_parse() -> None:
    name = "G16_registries_parse"
    hosts = REGISTRIES / "hosts.json"
    mods = REGISTRIES / "modules.json"
    for p in (hosts, mods):
        if not p.exists():
            _add("FAIL", f"{name}: {p.relative_to(ROOT)} missing")
            return
    try:
        hd = json.loads(hosts.read_text())
        md = json.loads(mods.read_text())
    except (ValueError, OSError) as e:
        _add("FAIL", f"{name}: parse error: {e}")
        return
    if "adapters" not in hd or not isinstance(hd["adapters"], list) or not hd["adapters"]:
        _add("FAIL", f"{name}: hosts.json missing non-empty 'adapters' list")
        return
    codes = []
    for a in hd["adapters"]:
        for req in ("code", "config_dir", "config_file", "surfaces"):
            if req not in a:
                _add("FAIL", f"{name}: adapter {a.get('code')!r} missing key {req!r}")
                return
        codes.append(a["code"])
    if len(codes) != len(set(codes)):
        _add("FAIL", f"{name}: duplicate adapter codes in hosts.json")
        return
    if "modules" not in md or not isinstance(md["modules"], list) or not md["modules"]:
        _add("FAIL", f"{name}: modules.json missing non-empty 'modules' list")
        return
    for m in md["modules"]:
        for req in ("code", "name", "description"):
            if req not in m:
                _add("FAIL", f"{name}: module missing key {req!r}")
                return
    _add("PASS", f"{name}: {len(codes)} host adapter(s), {len(md['modules'])} module(s) parse")


# ---------------------------------------------------------------------------
# G17  agnostic core (no host-binding tokens in core doctrine files)
# ---------------------------------------------------------------------------


def G17_agnostic_core() -> None:
    name = "G17_agnostic_core"
    files: list[pathlib.Path] = []
    for pat in CORE_HOST_SCAN_GLOBS:
        files.extend(ROOT.glob(pat))
    files = [f for f in files if f.is_file() and all(
        not str(f.relative_to(ROOT)).startswith(ex) for ex in CORE_HOST_SCAN_EXCLUDE)]
    if not files:
        _add("WARN", f"{name}: no core files to scan")
        return
    hits = []
    for f in files:
        rel = f.relative_to(ROOT)
        for i, line in enumerate(f.read_text().splitlines(), 1):
            m = HOST_TOKEN_RE.search(line)
            if m:
                hits.append((rel, i, m.group(0), line.strip()[:80]))
                if len(hits) > 50:
                    break
        if len(hits) > 50:
            break
    if hits:
        sample = "; ".join(f"{h[0]}:{h[1]} '{h[2]}'" for h in hits[:10])
        more = f" ... {len(hits) - 10} more" if len(hits) > 10 else ""
        _add("FAIL", f"{name}: host token in core: {sample}{more}")
        return
    _add("PASS", f"{name}: {len(files)} core file(s) free of host-binding tokens")


# ---------------------------------------------------------------------------
# G18  portable command inputs (no host-only argument features)
# ---------------------------------------------------------------------------


def G18_portable_command_inputs() -> None:
    name = "G18_portable_command_inputs"
    files: list[pathlib.Path] = []
    for pat in INVOKABLE_SCAN_GLOBS:
        files.extend(f for f in ROOT.glob(pat) if f.is_file())
    if not files:
        _add("WARN", f"{name}: no invokable files to scan")
        return
    bad_fm: list[tuple] = []   # (rel, key)
    bad_tok: list[tuple] = []  # (rel, line)
    for f in files:
        rel = f.relative_to(ROOT)
        # pick the banned-frontmatter set for this surface (glob pattern prefix)
        banned = next(v for k, v in INVOKABLE_SCAN_GLOBS.items()
                      if str(rel).startswith(k.split("*")[0].rstrip("/")))
        fm, body = _frontmatter(f)
        bad_fm.extend((rel, key) for key in fm if key in banned)
        for i, line in enumerate(body.splitlines(), 1):
            if NONPORTABLE_ARG_TOKEN_RE.search(line):
                bad_tok.append((rel, i))
                if len(bad_tok) > 50:
                    break
    msgs = []
    if bad_fm:
        msgs.append("host-only frontmatter " + ", ".join(f"{r}:{k}" for r, k in bad_fm[:10]))
    if bad_tok:
        msgs.append("indexed $ARGUMENTS[N] at " + "; ".join(f"{r}:{i}" for r, i in bad_tok[:10]))
    if msgs:
        _add("FAIL", f"{name}: " + "; ".join(msgs) + " -- use portable $ARGUMENTS (see skills/harness-engineering/references/agent-computer-interface.md)")
        return
    _add("PASS", f"{name}: {len(files)} invokable file(s) use the portable $ARGUMENTS channel")


GATES = [
    ("G1_manifests_parse", G1_manifests_parse),
    ("G2_versions_agree", G2_versions_agree),
    ("G3_skills_frontmatter", G3_skills_frontmatter),
    ("G4_agents_frontmatter", G4_agents_frontmatter),
    ("G5_commands_frontmatter", G5_commands_frontmatter),
    ("G6_no_dash_chars", G6_no_dash_chars),
    ("G7_no_orphan_skills", G7_no_orphan_skills),
    ("G8_eval_json_parses", G8_eval_json_parses),
    ("G9_agents_md_budget", G9_agents_md_budget),
    ("G10_claude_plugin_manifests", G10_claude_plugin_manifests),
    ("G11_cursor_plugin_manifests", G11_cursor_plugin_manifests),
    ("G12_gemini_extension_manifest", G12_gemini_extension_manifest),
    ("G13_plugin_symlinks", G13_plugin_symlinks),
    ("G14_frontmatter_colon_safe", G14_frontmatter_colon_safe),
    ("G15_manifests_generated", G15_manifests_generated),
    ("G16_registries_parse", G16_registries_parse),
    ("G17_agnostic_core", G17_agnostic_core),
    ("G18_portable_command_inputs", G18_portable_command_inputs),
]

HELP_EPILOG = "Gates: " + ", ".join(n for n, _ in GATES)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, epilog=HELP_EPILOG,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--all", action="store_true", help="Run every gate; do not abort on first failure.")
    ap.add_argument("--list", action="store_true", help="List gates and exit.")
    args = ap.parse_args(argv)

    if args.list:
        for n, _ in GATES:
            print(n)
        return 0

    any_fail = False
    n_pass = n_fail = n_warn = 0
    for name, fn in GATES:
        _msgs.clear()
        try:
            fn()
        except Exception as e:  # noqa: BLE001 -- top-level containment: a crashing gate reports FAIL, not a traceback
            _add("FAIL", f"{name}: gate crashed: {e}")
        for level, msg in _msgs:
            tag = {"PASS": "[PASS]", "FAIL": "[FAIL]", "WARN": "[WARN]"}[level]
            stream = sys.stderr if level == "FAIL" else sys.stdout
            print(f"{tag} {msg}", file=stream)
            if level == "PASS":
                n_pass += 1
            elif level == "FAIL":
                n_fail += 1
            elif level == "WARN":
                n_warn += 1
        if any(level == "FAIL" for level, _ in _msgs):
            any_fail = True
            if not args.all:
                print(f"\nGate {name} failed; aborting (use --all to run all gates).", file=sys.stderr)
                return 1

    print()
    if any_fail:
        print(f"{n_fail} checks failed ({n_warn} warnings, {n_pass} passes)")
        return 1
    print(f"All {n_pass} checks passed ({n_warn} warnings)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
