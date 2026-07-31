#!/usr/bin/env python3
"""scripts/gen-manifests.py - Generate host plugin manifests from one source.

Three derivable sources of truth, no hand-copied inventory, no version drift:

  inventory   the directories on disk   skills/*, commands/*.md, agents/*.md
  version     the VERSION file at repo root
  static meta embedded host templates below  (descriptions, URLs, keywords)

Renders the seven host manifests under .agents/plugins/<host>/ that the root
symlinks (.claude-plugin/, .cursor-plugin/, gemini-extension.json, root
plugin.json/marketplace.json) already target. install.sh symlinks whole
directories and never reads these arrays, so it is unaffected.

Usage:
    python3 scripts/gen-manifests.py          # write all manifests in place
    python3 scripts/gen-manifests.py --check  # exit 1 if any checked-in manifest
                                             # differs from generated output (no write)

Descriptions are authored prose and intentionally static; the skills[],
commands[], and agents[] arrays (what hosts actually read) plus the version
are always derived and current. If the inventory changes, the count-word
("eight") the descriptions carry is a cosmetic follow-up, not a discovery bug.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
PLUGINS = REPO / ".agents" / "plugins"


# --- static per-host metadata (authored prose; see module docstring) ------------

DESC_CLAUDE_PLUGIN = "Language-agnostic coding-agent configuration. Ships a router AGENTS.md encoding repo-as-record doctrine, eight on-demand skills (commit-message, effective-code-craft, go-essential, harness-engineering, openapi-spec, performance-patterns, repo-documentation, spec-driven-development), six slash commands (document-phase, judge-phase, openapi-phase, refactor-phase, review-phase, verify-phase), and a primary conductor orchestrator that drives the think/act/prove/grow loop. Targets deterministic, executable-completion workflows over speculative AI assistance."

DESC_LEGACY = "Language-agnostic coding-agent configuration for OpenCode and Kilo-compatible runtimes. Ships a router AGENTS.md encoding repo-as-record doctrine, eight on-demand skills (commit-message, effective-code-craft, go-essential, harness-engineering, openapi-spec, performance-patterns, repo-documentation, spec-driven-development), six slash commands (document-phase, judge-phase, openapi-phase, refactor-phase, review-phase, verify-phase), and a primary conductor orchestrator that drives the think/act/prove/grow loop. Targets deterministic, executable-completion workflows over speculative AI assistance."

DESC_CURSOR_PLUGIN = "Language-agnostic coding-agent skills and a primary conductor orchestrator. Ships a router AGENTS.md encoding repo-as-record doctrine, eight on-demand skills (commit-message, effective-code-craft, go-essential, harness-engineering, openapi-spec, performance-patterns, repo-documentation, spec-driven-development), and a think/act/prove/grow conductor agent. Targets deterministic, executable-completion workflows over speculative AI assistance."

DESC_GEMINI = "Language-agnostic coding-agent skills plus a primary conductor orchestrator. Ships a router AGENTS.md encoding repo-as-record doctrine, eight on-demand skills (commit-message, effective-code-craft, go-essential, harness-engineering, openapi-spec, performance-patterns, repo-documentation, spec-driven-development), and a think/act/prove/grow conductor agent. Targets deterministic, executable-completion workflows over speculative AI assistance."

DESC_MARKETPLACE_META = "Language-agnostic coding-agent skills: repo-as-record doctrine, harness engineering, code craft, performance, spec-driven development, and a primary conductor orchestrator."

DESC_CLAUDE_MARKETPLACE_PLUGIN = "Eight on-demand skills plus a conductor orchestrator. Targets deterministic, executable-completion workflows over speculative AI assistance. Compatible with Claude Code, Cursor, Codex, OpenCode, Kilo, Gemini, and any Agent Skills-compatible runtime."

DESC_CURSOR_MARKETPLACE_PLUGIN = "Eight on-demand skills plus a conductor orchestrator. Targets deterministic, executable-completion workflows over speculative AI assistance. Compatible with Cursor, Claude Code, Codex, OpenCode, Kilo, Gemini, and any Agent Skills-compatible runtime."


# --- derivable inventory from disk ----------------------------------------------

def read_version() -> str:
    return (REPO / "VERSION").read_text(encoding="utf-8").strip()


def _frontmatter_field(path: pathlib.Path, key: str) -> str | None:
    """Return one frontmatter scalar value (flat YAML), or None.

    Only `mode` is consumed by this generator, so a minimal parser suffices.
    """
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    body = text[3:]
    nl = body.find("\n")
    end = body.find("\n---", nl)
    block = body[nl + 1:end] if end != -1 else body[nl + 1:]
    for line in block.splitlines():
        if line.startswith(key + ":"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    return None


def skill_names() -> list[str]:
    return sorted(md.parent.name for md in (REPO / "skills").glob("*/SKILL.md"))


def command_names() -> list[str]:
    return sorted(p.stem for p in (REPO / "commands").glob("*.md"))


def primary_agents() -> list[tuple[str, str]]:
    """[(name, mode)] for agents whose frontmatter mode == primary.

    Sub-agents (coder/discover, mode: subagent) are intentionally excluded: the
    manifests surface only the primary conductor as an installable agent.
    """
    out: list[tuple[str, str]] = []
    for md in sorted((REPO / "agents").glob("*.md")):
        mode = _frontmatter_field(md, "mode")
        if mode == "primary":
            out.append((md.stem, mode))
    return out


# --- renderers (dict key order matches existing files for a no-op first diff) ---

def render_claude_plugin(v: str, skills: list[str]) -> dict:
    return {
        "$schema": "https://github.com/anthropics/claude-code/raw/main/schema/plugin.json",
        "name": "coder-agents",
        "version": v,
        "description": DESC_CLAUDE_PLUGIN,
        "author": {"name": "bouroo", "url": "https://github.com/bouroo"},
        "homepage": "https://github.com/bouroo/agents",
        "repository": {"type": "git", "url": "https://github.com/bouroo/agents"},
        "license": "Apache-2.0",
        "keywords": [
            "agent-skills", "claude-code", "cursor", "codex",
            "opencode", "kilo", "gemini", "harness-engineering",
            "code-craft", "spec-driven",
        ],
        "skills": [f"./skills/{s}" for s in skills],
    }


def render_claude_marketplace(v: str, skills: list[str]) -> dict:
    return {
        "$schema": "https://github.com/anthropics/claude-code/raw/main/schema/marketplace.json",
        "name": "bouroo-agents",
        "owner": {"name": "bouroo", "url": "https://github.com/bouroo"},
        "metadata": {"description": DESC_MARKETPLACE_META},
        "plugins": [
            {
                "name": "coder-agents",
                "source": "./",
                "description": DESC_CLAUDE_MARKETPLACE_PLUGIN,
                "version": v,
                "skills": [f"./skills/{s}" for s in skills],
            }
        ],
    }


def render_cursor_plugin(v: str, skills: list[str], commands: list[str], agents: list[tuple[str, str]]) -> dict:
    return {
        "$schema": "https://cursor.com/schemas/cursor-plugin/plugin.json",
        "name": "coder-agents",
        "displayName": "Coder Agents",
        "version": v,
        "description": DESC_CURSOR_PLUGIN,
        "author": {"name": "bouroo"},
        "publisher": "bouroo",
        "homepage": "https://github.com/bouroo/agents",
        "repository": "https://github.com/bouroo/agents",
        "license": "Apache-2.0",
        "category": "agents",
        "keywords": [
            "agent-skills", "harness-engineering", "code-craft",
            "spec-driven", "performance", "conductor",
        ],
        "skills": [f"skills/{s}/SKILL.md" for s in skills],
        "agents": [f"agents/{name}.md" for name, _ in agents],
        "commands": [f"commands/{c}.md" for c in commands],
    }


def render_cursor_marketplace() -> dict:
    return {
        "$schema": "https://cursor.com/schemas/cursor-plugin/marketplace.json",
        "name": "bouroo-coder-agents",
        "owner": {"name": "bouroo"},
        "metadata": {"description": DESC_MARKETPLACE_META},
        "plugins": [
            {
                "name": "coder-agents",
                "source": "./",
                "description": DESC_CURSOR_MARKETPLACE_PLUGIN,
            }
        ],
    }


def render_legacy_plugin(v: str, skills: list[str], commands: list[str], agents: list[tuple[str, str]]) -> dict:
    return {
        "name": "coder-agents",
        "version": v,
        "description": DESC_LEGACY,
        "author": "bouroo",
        "license": "Apache-2.0",
        "homepage": "https://github.com/bouroo/agents",
        "skills": list(skills),
        "commands": list(commands),
        "agents": [{"name": name, "mode": mode} for name, mode in agents],
    }


def render_legacy_marketplace(v: str) -> dict:
    return {
        "name": "coder-agents",
        "owner": "bouroo",
        "version": v,
        "plugins": [
            {
                "name": "agents",
                "version": v,
                "source": "https://github.com/bouroo/agents",
                "description": DESC_LEGACY,
            }
        ],
    }


def render_gemini(v: str) -> dict:
    return {
        "$schema": "https://geminicli.com/docs/extensions/reference/schema.json",
        "name": "coder-agents",
        "version": v,
        "description": DESC_GEMINI,
        "contextFileName": "AGENTS.md",
        "mcpServers": {},
    }


def build_all() -> list[tuple[pathlib.Path, dict]]:
    v = read_version()
    skills = skill_names()
    commands = command_names()
    agents = primary_agents()
    return [
        (PLUGINS / "claude" / "plugin.json", render_claude_plugin(v, skills)),
        (PLUGINS / "claude" / "marketplace.json", render_claude_marketplace(v, skills)),
        (PLUGINS / "cursor" / "plugin.json", render_cursor_plugin(v, skills, commands, agents)),
        (PLUGINS / "cursor" / "marketplace.json", render_cursor_marketplace()),
        (PLUGINS / "legacy" / "plugin.json", render_legacy_plugin(v, skills, commands, agents)),
        (PLUGINS / "legacy" / "marketplace.json", render_legacy_marketplace(v)),
        (PLUGINS / "gemini" / "gemini-extension.json", render_gemini(v)),
    ]


def _serialize(d: dict) -> str:
    return json.dumps(d, indent=2, ensure_ascii=False) + "\n"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description="Generate host plugin manifests from VERSION + disk inventory.",
    )
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if any checked-in manifest differs from generated output; no writes")
    args = ap.parse_args(argv)

    targets = build_all()
    drifted = []
    for path, doc in targets:
        generated = _serialize(doc)
        if args.check:
            on_disk = path.read_text(encoding="utf-8") if path.exists() else ""
            if on_disk != generated:
                drifted.append((path.relative_to(REPO), on_disk, generated))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(generated, encoding="utf-8")
            print(f"wrote {path.relative_to(REPO)}")

    if args.check:
        if drifted:
            for rel, _old, _new in drifted:
                print(f"[DRIFT] {rel} does not match generated output", file=sys.stderr)
            print(f"{len(drifted)} manifest(s) drifted; regenerate with "
                  f"'python3 scripts/gen-manifests.py'", file=sys.stderr)
            return 1
        print(f"all {len(targets)} manifests current (version={read_version()}, "
              f"skills={len(skill_names())}, commands={len(command_names())}, "
              f"primary-agents={len(primary_agents())})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
