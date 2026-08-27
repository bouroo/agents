#!/usr/bin/env python3
"""Deterministic verification gates for the v4 shared-setup repository.

The repo ships docs and skills only, so these four static gates are the
entire verification surface:

    budget          AGENTS.md stays within its line budget (the concision charter)
    frontmatter     every skills/<name>/SKILL.md carries valid Agent-Skills metadata
    links           every relative Markdown link resolves to an existing file
    agnostic        core doctrine is free of host-binding tokens

Run `python3 scripts/check.py --all`; CI runs the same. Exit 0 iff no gate
fails. Note: `.agents/plans/**` is deliberately outside every scan -- those
are committed historical retros that cite paths as they were, and gating
history against the present would make retro files uncommittable.
"""

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

AGENTS_MD_BUDGET = 200

KEBAB_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
ALLOWED_KEYS = {"name", "description"}

# Host-binding tokens forbidden in core doctrine. A dotdir or host config
# filename is an unambiguous signal of a host leak into an agnostic file.
HOST_TOKEN_RE = re.compile(
    r"\.claude|\.cursor|\.gemini|\.codex|\.qwen|\.kilo|"
    r"\bCLAUDE\.md\b|\bGEMINI\.md\b|"
    r"\bopencode\b|\bkilo\b|\bantigravity\b|\bcodex\b|\bqwen\b",
    re.IGNORECASE,
)

# Files scanned for host tokens. CHANGELOG.md cites removed machinery by name
# on purpose (the Removed section of a breaking release), so it is allowlisted.
HOST_SCAN_FILES = [ROOT / "AGENTS.md", ROOT / "README.md"]
HOST_SCAN_SKILLS = sorted((ROOT / "skills").rglob("*.md")) \
    + sorted((ROOT / "commands").rglob("*.md"))
HOST_SCAN_ALLOWLIST = {"CHANGELOG.md"}

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")

_msgs: list[tuple[str, str]] = []


def _add(level: str, msg: str) -> None:
    _msgs.append((level, msg))


def _frontmatter(path: pathlib.Path) -> tuple[dict, list[str], bool]:
    """Parse an indent-free `key: value` frontmatter block.

    Returns (fields, all_key_lines, starts_with_fence). Colon-safe checking
    needs the raw key lines, hence the third element pairs with them.
    """
    text = path.read_text()
    if not text.startswith("---"):
        return {}, [], False
    end = text.find("\n---", 3)
    if end == -1:
        return {}, [], False
    lines = []
    fields: dict = {}
    for line in text[3:end].splitlines():
        s = line.strip()
        if not s or s.startswith("#") or ":" not in s:
            continue
        k, v = s.split(":", 1)
        fields[k.strip()] = v.strip().strip('"').strip("'")
        lines.append(s)
    return fields, lines, True


def g_budget() -> None:
    name = "budget"
    path = ROOT / "AGENTS.md"
    if not path.is_file():
        _add("FAIL", f"{name}: AGENTS.md missing")
        return
    n = len(path.read_text().splitlines())
    if n > AGENTS_MD_BUDGET:
        _add("FAIL", f"{name}: AGENTS.md has {n} lines > budget {AGENTS_MD_BUDGET}")
        return
    _add("PASS", f"{name}: AGENTS.md {n}/{AGENTS_MD_BUDGET} lines")


def g_frontmatter() -> None:
    name = "frontmatter"
    # (path, expected-name) pairs: a skill's name matches its directory,
    # a command's name matches its file stem.
    subjects = [(p, p.parent.name)
                for p in sorted((ROOT / "skills").glob("*/SKILL.md"))]
    subjects += [(p, p.stem)
                 for p in sorted((ROOT / "commands").glob("*.md"))]
    if not subjects:
        _add("FAIL", f"{name}: no skills/*/SKILL.md or commands/*.md found")
        return
    ok = True
    for md, expected_name in subjects:
        rel = md.relative_to(ROOT)
        fields, lines, fenced = _frontmatter(md)
        problems: list[str] = []
        if not fenced:
            problems.append("does not start with --- fence")
        fname = fields.get("name")
        if fname != expected_name:
            problems.append(f"name {fname!r} != {expected_name!r}")
        elif not KEBAB_RE.match(fname):
            problems.append(f"name {fname!r} not kebab-case")
        elif not 1 <= len(fname) <= 64:
            problems.append(f"name length {len(fname)} not in 1..64")
        desc = fields.get("description", "")
        if not 1 <= len(desc) <= 1024:
            problems.append("description length not in 1..1024")
        unknown = set(fields) - ALLOWED_KEYS
        if unknown:
            problems.append(f"unknown keys {sorted(unknown)}")
        unsafe = [ln.split(":", 1)[0].strip() for ln in lines
                  if (raw := ln.split(":", 1)[1].strip())
                  and ": " in raw and raw[0] not in "\"'"]
        if unsafe:
            problems.append(f"colon-unsafe scalars in {unsafe}")
        if problems:
            ok = False
            _add("FAIL", f"{name}: {rel}: {'; '.join(problems)}")
    if ok:
        _add("PASS", f"{name}: {len(subjects)} SKILL.md/command frontmatter valid")


def g_links() -> None:
    name = "links"
    targets = [ROOT / f for f in ("AGENTS.md", "README.md", "CHANGELOG.md")]
    targets += sorted(p for p in (ROOT / "skills").rglob("*.md"))
    targets += sorted(p for p in (ROOT / "commands").rglob("*.md"))
    dead: list[str] = []
    checked = 0
    for f in targets:
        rel = f.relative_to(ROOT)
        if not f.is_file():
            continue
        for i, line in enumerate(f.read_text().splitlines(), 1):
            for target in LINK_RE.findall(line):
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                checked += 1
                resolved = (f.parent / target.split("#")[0]).resolve()
                if target.split("#")[0] and not resolved.exists():
                    dead.append(f"{rel}:{i} -> {target}")
    if dead:
        _add("FAIL", f"{name}: {len(dead)} dangling link(s): "
             + "; ".join(dead[:10]) + (" ..." if len(dead) > 10 else ""))
        return
    _add("PASS", f"{name}: {checked} relative link(s) resolve")


def g_agnostic() -> None:
    name = "agnostic"
    files = [f for f in HOST_SCAN_FILES + HOST_SCAN_SKILLS
             if f.is_file() and f.name not in HOST_SCAN_ALLOWLIST]
    hits: list[str] = []
    for f in files:
        rel = f.relative_to(ROOT)
        for i, line in enumerate(f.read_text().splitlines(), 1):
            m = HOST_TOKEN_RE.search(line)
            if m:
                hits.append(f"{rel}:{i} '{m.group(0)}'")
                if len(hits) >= 10:
                    break
        if len(hits) >= 10:
            break
    if hits:
        _add("FAIL", f"{name}: host token in core: " + "; ".join(hits))
        return
    _add("PASS", f"{name}: {len(files)} core file(s) free of host-binding tokens")


GATES = [("budget", g_budget), ("frontmatter", g_frontmatter),
         ("links", g_links), ("agnostic", g_agnostic)]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Run the repository's deterministic gates "
                    "(choose from: %s)" % ", ".join(n for n, _ in GATES))
    parser.add_argument("--all", action="store_true", help="run every gate")
    parser.add_argument("gates", nargs="*", help="specific gate names")
    args = parser.parse_args(argv)

    selected = [g for _, g in GATES] if args.all else None
    if selected is None:
        by_name = dict(GATES)
        unknown = [g for g in args.gates if g not in by_name]
        if unknown:
            parser.error(f"unknown gate(s): {', '.join(unknown)}")
        selected = [by_name[g] for g in args.gates]

    for gate in selected:
        gate()

    failed = False
    for level, msg in _msgs:
        print(f"[{level}] {msg}")
        if level == "FAIL":
            failed = True
    if failed:
        return 1
    print(f"OK ({len(selected)} gate(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
