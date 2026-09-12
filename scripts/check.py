#!/usr/bin/env python3
"""Deterministic verification gates for the v4 shared-setup repository.

Static gates over docs/skills plus the distribution layer:

    budget          AGENTS.md stays within its line budget (the concision charter)
    frontmatter     every skill/command carries valid Agent-Skills-style metadata
    links           every relative Markdown link resolves to an existing file
    agnostic        core doctrine is free of host-binding tokens
    manifests       marketplace discovery manifests parse; versions agree
    privacy         doctrine free of real-work identifiers (tiny links,
                    page ids, private hosts, engagement service names)

Run `python3 scripts/check.py --all`; CI runs the same. Exit 0 iff no gate
fails. Notes: `.agents/plans/**` is deliberately outside every scan -- those
are committed historical retros that cite paths as they were, and gating
history against the present would make retro files uncommittable. Dot-
directories (e.g. skills/.system/, where coding CLIs drop runtime skills) are
outside every scan: .gitignore keeps them out of the repository, and gating
machine-local tool state would make gate verdicts machine-dependent. Host-
token scanning intentionally EXCLUDES the distribution layer (.claude-plugin/,
.cursor-plugin/, gemini-extension.json, scripts/): agnosticism applies to the
doctrine, while installers/manifests are precisely where concrete hosts live.
"""

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

AGENTS_MD_BUDGET = 250

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

# Real-work identity is forbidden in the shared doctrine: page titles,
# space keys, tiny-link codes, numeric page ids, and private hosts name a
# specific engagement and must live in machine-local memory only. The scan
# covers the same doctrine surface as the host scan (skills + commands +
# AGENTS.md) plus CHANGELOG.md, whose host-token allowlist does not extend
# to private identifiers. Detection is STRUCTURAL (tiny-link shapes, long
# numeric ids, private Atlassian hosts) - the detector must not itself
# enumerate engagement names. Structural classes are what is enforceable;
# engagement-specific names stay a machine-local, human-reviewed rule.
PRIVACY_TOKEN_RE = re.compile(
    r"\bwiki/x/[A-Za-z0-9+/=_-]{6,}\b"                        # tiny links
    r"|\b\d{7,}\b"                                            # page/attachment ids
    r"|\b(?!mcp\.|support\.)[a-z0-9-]+\.atlassian\.(?:net|com)\b",
    re.IGNORECASE,
)
PRIVACY_SCAN_FILES = [ROOT / "AGENTS.md", ROOT / "CHANGELOG.md"]

def _no_dotdir(p: pathlib.Path) -> bool:
    """True unless some path part is a dot-directory: untracked tool state
    (coding CLIs drop runtime skills into skills/.system/) that .gitignore
    keeps out of the repository -- gating it would gate this machine, not
    the doctrine."""
    return not any(part.startswith(".") for part in p.relative_to(ROOT).parts)


# Files scanned for host tokens: everything an assistant consumes as doctrine
# (AGENTS.md, skills, commands). README.md and CHANGELOG.md are allowlisted:
# they document the distribution layer for humans, so naming concrete hosts,
# marketplaces, and removed machinery is their job, not a leak.
HOST_SCAN_FILES = [ROOT / "AGENTS.md"]
HOST_SCAN_SKILLS = sorted(p for p in (ROOT / "skills").rglob("*.md")
                          if _no_dotdir(p)) \
    + sorted(p for p in (ROOT / "commands").rglob("*.md") if _no_dotdir(p))
HOST_SCAN_ALLOWLIST = {"CHANGELOG.md", "README.md"}

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
                for p in sorted((ROOT / "skills").glob("*/SKILL.md"))
                if _no_dotdir(p)]
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
    targets += sorted(p for p in (ROOT / "skills").rglob("*.md")
                      if _no_dotdir(p))
    targets += sorted(p for p in (ROOT / "commands").rglob("*.md")
                      if _no_dotdir(p))
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


MARKETPLACE_MANIFESTS = [
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".cursor-plugin/plugin.json",
    ".cursor-plugin/marketplace.json",
    "gemini-extension.json",
]


def g_manifests() -> None:
    name = "manifests"
    errors: list[str] = []
    docs: dict[str, dict] = {}
    for rel in MARKETPLACE_MANIFESTS:
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing {rel}")
            continue
        try:
            docs[rel] = json.loads(path.read_text())
        except ValueError as exc:
            errors.append(f"{rel}: invalid JSON: {exc}")
    versions = {rel: d.get("version") for rel, d in docs.items()
                if isinstance(d, dict) and d.get("version")}
    if not versions and not any("invalid" in e or "missing" in e for e in errors):
        errors.append("no version field found in any manifest")
    if len(set(versions.values())) > 1:
        detail = ", ".join(f"{r}={v}" for r, v in sorted(versions.items()))
        errors.append(f"versions disagree: {detail}")
    for mrel in (".claude-plugin/marketplace.json", ".cursor-plugin/marketplace.json"):
        market = docs.get(mrel) if isinstance(docs.get(mrel), dict) else {}
        prel = mrel.replace("marketplace.json", "plugin.json")
        plugin = docs.get(prel) if isinstance(docs.get(prel), dict) else {}
        listed = [p.get("name") for p in market.get("plugins", [])
                  if isinstance(p, dict)]
        pname = plugin.get("name")
        if pname and listed and pname not in listed:
            errors.append(f"{mrel} lists {listed} but {prel} defines {pname!r}")
    if errors:
        _add("FAIL", f"{name}: " + "; ".join(errors))
        return
    _add("PASS", f"{name}: {len(docs)} manifest(s) parse, "
                 f"versions agree ({next(iter(sorted(versions.values())))}, "
                 f"{len(MARKETPLACE_MANIFESTS) - len(docs)} absent)")


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


def g_privacy() -> None:
    name = "privacy"
    scanned = PRIVACY_SCAN_FILES \
        + sorted(p for p in (ROOT / "skills").rglob("*.md") if _no_dotdir(p)) \
        + sorted(p for p in (ROOT / "commands").rglob("*.md") if _no_dotdir(p))
    files = [f for f in scanned if f.is_file()]
    hits: list[str] = []
    for f in files:
        rel = f.relative_to(ROOT)
        for i, line in enumerate(f.read_text().splitlines(), 1):
            m = PRIVACY_TOKEN_RE.search(line)
            if m:
                hits.append(f"{rel}:{i} '{m.group(0)}'")
                if len(hits) >= 10:
                    break
        if len(hits) >= 10:
            break
    if hits:
        _add("FAIL", f"{name}: real-work identifier in doctrine: " + "; ".join(hits))
        return
    _add("PASS", f"{name}: {len(files)} doctrine file(s) free of real-work identifiers")


def g_evals() -> None:
    name = "evals"
    path = ROOT / "evals" / "suite.json"
    if not path.is_file():
        _add("FAIL", f"{name}: evals/suite.json missing (the harness "
                     "regression suite is a required artifact)")
        return
    try:
        suite = json.loads(path.read_text())
    except ValueError as exc:
        _add("FAIL", f"{name}: evals/suite.json: invalid JSON: {exc}")
        return
    errors: list[str] = []
    evals = suite.get("evals")
    if not isinstance(evals, list) or not evals:
        errors.append("no non-empty 'evals' list")
    else:
        seen: set[str] = set()
        for i, ev in enumerate(evals):
            if not isinstance(ev, dict):
                errors.append(f"evals[{i}] not an object")
                continue
            eid = ev.get("id")
            if not isinstance(eid, str) or not eid:
                errors.append(f"evals[{i}] missing 'id'")
            elif eid in seen:
                errors.append(f"duplicate id {eid!r}")
            else:
                seen.add(eid)
            if not isinstance(ev.get("prompt"), str) or not ev["prompt"].strip():
                errors.append(f"{eid or i}: missing 'prompt'")
            checks = ev.get("checks")
            if not isinstance(checks, list) or not checks:
                errors.append(f"{eid or i}: no 'checks'")
                continue
            for j, chk in enumerate(checks):
                if not isinstance(chk, dict):
                    errors.append(f"{eid or i}: checks[{j}] not an object")
                    continue
                if not isinstance(chk.get("cmd"), str) or not chk["cmd"].strip():
                    errors.append(f"{eid or i}: checks[{j}] missing 'cmd'")
                if not isinstance(chk.get("expect_exit"), int):
                    errors.append(f"{eid or i}: checks[{j}] missing int 'expect_exit'")
    if errors:
        _add("FAIL", f"{name}: " + "; ".join(errors[:10])
             + (" ..." if len(errors) > 10 else ""))
        return
    _add("PASS", f"{name}: {len(evals)} eval(s) well-formed "
                 f"(id, prompt, mechanical checks)")


GATES = [("budget", g_budget), ("frontmatter", g_frontmatter),
         ("links", g_links), ("agnostic", g_agnostic),
         ("manifests", g_manifests), ("privacy", g_privacy),
         ("evals", g_evals)]


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
