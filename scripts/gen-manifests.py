#!/usr/bin/env python3
"""scripts/gen-manifests.py - Generate host plugin manifests from one source.

Three derivable sources of truth, no hand-copied inventory, no version drift:

  inventory   directories on disk:  skills/**/SKILL.md, command/*/SKILL.md,
                                   agents/*/SKILL.md (filtered to mode: primary)
  version     the VERSION file at repo root
  static meta embedded host templates below  (descriptions, URLs)

Renders the host manifests under adapters/manifests/<host>/ that the discovery
symlinks (.claude-plugin/, .cursor-plugin/, gemini-extension.json, root
plugin.json/marketplace.json) target. The installer (adapters/install.sh) reads
registries/hosts.json and symlinks whole directories; it never reads these
arrays, so it is unaffected by regeneration.

Usage:
    python3 scripts/gen-manifests.py          # write all manifests in place
    python3 scripts/gen-manifests.py --check  # exit 1 if checked-in manifests drift
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MANIFEST_DIR = ROOT / "adapters" / "manifests"

NAME = "coder-agents"
HOMEPAGE = "https://github.com/bouroo/agents"
REPO_URL = "https://github.com/bouroo/agents"

DESC_PLUGIN = (
    "Language- and host-agnostic coder-agent squad. Ships a governance AGENTS.md, "
    "a three-role squad (conductor/coder/discover), phase commands, and on-demand "
    "skills driving the think-act-prove-grow loop. Targets deterministic, "
    "executable-completion workflows over speculative assistance."
)
DESC_MARKET = (
    "Language- and host-agnostic coder-agent squad: governance doctrine, harness "
    "engineering, code craft, performance, spec-driven development, and a primary "
    "conductor orchestrator."
)


def read_version() -> str:
    return (ROOT / "VERSION").read_text().strip()


def _frontmatter_field(path: pathlib.Path, key: str) -> str | None:
    """Minimal YAML frontmatter reader for one scalar field (only `mode` is used)."""
    try:
        text = path.read_text()
    except OSError:
        return None
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    for line in text[3:end].splitlines():
        line = line.strip()
        if line.startswith(f"{key}:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    return None


def skill_rels() -> list[str]:
    """Paths relative to skills/ for every skills/*/SKILL.md (e.g. code-craft, openapi-spec)."""
    out: list[str] = []
    for md in sorted((ROOT / "skills").glob("*/SKILL.md")):
        out.append(md.parent.name)
    return out


def command_names() -> list[str]:
    """Command names from flat commands/<name>.md files."""
    return sorted(p.stem for p in (ROOT / "commands").glob("*.md"))


def primary_agents() -> list[tuple[str, str]]:
    """[(name, mode)] for flat agents/<name>.md whose frontmatter mode == primary."""
    out: list[tuple[str, str]] = []
    for md in sorted((ROOT / "agents").glob("*.md")):
        mode = _frontmatter_field(md, "mode") or "primary"
        if mode == "primary":
            out.append((md.stem, mode))
    return out


def render_claude_plugin(v: str, skills: list[str]) -> dict:
    return {
        "name": NAME, "version": v, "description": DESC_PLUGIN,
        "author": {"name": "bouroo", "url": "https://github.com/bouroo"},
        "homepage": HOMEPAGE,
        "repository": {"type": "git", "url": REPO_URL},
        "keywords": ["agents", "coding-agent", "skills", "squad", "harness"],
        "license": "Apache-2.0",
        "skills": [f"./skills/{s}" for s in skills],
    }


def render_claude_marketplace(v: str, skills: list[str]) -> dict:
    return {
        "name": "bouroo-agents",
        "owner": {"name": "bouroo", "url": "https://github.com/bouroo"},
        "plugins": [
            {
                "name": NAME, "source": "./",
                "description": DESC_PLUGIN, "version": v,
                "skills": [f"./skills/{s}" for s in skills],
                "homepage": HOMEPAGE,
            }
        ],
    }


def render_cursor_plugin(v: str, skills: list[str], commands: list[str], agents: list[tuple[str, str]]) -> dict:
    return {
        "name": NAME, "version": v, "description": DESC_PLUGIN,
        "author": {"name": "bouroo"}, "publisher": "bouroo",
        "homepage": HOMEPAGE, "repository": REPO_URL,
        "license": "Apache-2.0",
        "skills": [f"skills/{s}/SKILL.md" for s in skills],
        "agents": [f"agents/{n}.md" for n, _ in agents],
        "commands": [f"commands/{c}.md" for c in commands],
    }


def render_cursor_marketplace() -> dict:
    return {
        "name": "bouroo-coder-agents",
        "owner": {"name": "bouroo"},
        "plugins": [
            {"name": NAME, "source": "./", "description": DESC_PLUGIN}
        ],
    }


def render_legacy_plugin(v: str, skills: list[str], commands: list[str], agents: list[tuple[str, str]]) -> dict:
    return {
        "name": NAME, "version": v, "description": DESC_PLUGIN,
        "author": "bouroo", "homepage": HOMEPAGE, "repository": REPO_URL,
        "license": "Apache-2.0",
        "skills": skills,
        "commands": commands,
        "agents": [{"name": n, "mode": m} for n, m in agents],
    }


def render_legacy_marketplace(v: str) -> dict:
    return {
        "name": NAME, "owner": {"name": "bouroo"}, "version": v,
        "description": DESC_MARKET,
        "plugins": [
            {"name": NAME, "source": REPO_URL, "description": DESC_PLUGIN}
        ],
    }


def render_gemini(v: str) -> dict:
    return {
        "name": NAME, "version": v, "description": DESC_PLUGIN,
        "contextFileName": "AGENTS.md", "mcpServers": {},
    }


def build_all() -> list[tuple[pathlib.Path, dict]]:
    v = read_version()
    skills = skill_rels()
    commands = command_names()
    agents = primary_agents()
    return [
        (MANIFEST_DIR / "claude" / "plugin.json", render_claude_plugin(v, skills)),
        (MANIFEST_DIR / "claude" / "marketplace.json", render_claude_marketplace(v, skills)),
        (MANIFEST_DIR / "cursor" / "plugin.json", render_cursor_plugin(v, skills, commands, agents)),
        (MANIFEST_DIR / "cursor" / "marketplace.json", render_cursor_marketplace()),
        (MANIFEST_DIR / "gemini" / "gemini-extension.json", render_gemini(v)),
        (MANIFEST_DIR / "legacy" / "plugin.json", render_legacy_plugin(v, skills, commands, agents)),
        (MANIFEST_DIR / "legacy" / "marketplace.json", render_legacy_marketplace(v)),
    ]


def _serialize(d: dict) -> str:
    return json.dumps(d, indent=2, sort_keys=False) + "\n"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="exit 1 if checked-in manifests differ from generated")
    args = ap.parse_args(argv)

    targets = build_all()
    drifted: list[tuple[pathlib.Path, str, str]] = []
    written = 0
    for path, doc in targets:
        new = _serialize(doc)
        path.parent.mkdir(parents=True, exist_ok=True)
        if args.check:
            old = path.read_text() if path.exists() else ""
            if old != new:
                drifted.append((path, old, new))
        else:
            path.write_text(new)
            written += 1

    if args.check:
        if drifted:
            for rel, _o, _n in drifted:
                print(f"[DRIFT] {rel.relative_to(ROOT)} does not match generated output", file=sys.stderr)
            print(f"{len(drifted)} manifest(s) drifted; regenerate with 'python3 scripts/gen-manifests.py'", file=sys.stderr)
            return 1
        print(f"all {len(targets)} manifests current (version={read_version()}, "
              f"skills={len(skill_rels())}, commands={len(command_names())}, "
              f"primary-agents={len(primary_agents())})")
        return 0

    print(f"wrote {written} manifest(s) under adapters/manifests/ (version={read_version()}, "
          f"skills={len(skill_rels())}, commands={len(command_names())}, "
          f"primary-agents={len(primary_agents())})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
