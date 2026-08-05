#!/usr/bin/env python3
"""scripts/resolve-customization.py - Three-tier customization resolver.

Resolves a customization block (e.g. ``agent`` or ``workflow``) by merging
three optional TOML layers in base -> team -> user order:

  base   <artifact>/customize.toml                       (shipped defaults)
  team   {project}/.agents/custom/<id>.toml              (team overrides)
  user   {project}/.agents/custom/<id>.user.toml         (personal overrides)

Any missing file is skipped. Merge rules:
  scalars                  last writer wins
  tables (dict)             deep-merge recursively
  arrays-of-tables keyed    by `code` or `id`: replace matching entries,
                            append new ones
  all other arrays          append (dedup not applied)

The resolver is OPTIONAL. Artifacts function fully without it (defaults live
inline in each SKILL.md). If TOML parsing is unavailable or any file is
malformed, the script prints the manual fallback and exits non-zero so the
caller (the agent) resolves the block itself per the rules above.

Usage:
    python3 scripts/resolve-customization.py --skill <relative-dir> --key <table>
    python3 scripts/resolve-customization.py --skill agents/conductor --key agent

Exit codes:
    0   resolved block printed as JSON on stdout
    2   manual fallback required (details on stderr)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None


MANUAL_FALLBACK = """\
Manual fallback required. Resolve the `<key>` block yourself by reading these
files in base -> team -> user order and applying the merge rules:
  scalars: override wins
  tables: deep-merge
  arrays-of-tables keyed by `code`/`id`: replace matching, append new
  other arrays: append
Layers (missing files are skipped):
  1. {base}
  2. {team}
  3. {user}
"""


def _deep_merge(base: dict, overlay: dict) -> dict:
    out = dict(base)
    for k, v in overlay.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        elif isinstance(v, list) and isinstance(out.get(k), list) and _keyed(out[k]) and _keyed(v):
            out[k] = _merge_keyed(out[k], v)
        elif isinstance(v, list) and isinstance(out.get(k), list):
            out[k] = out[k] + v
        else:
            out[k] = v
    return out


def _keyed(arr: list) -> bool:
    return all(isinstance(x, dict) and ("code" in x or "id" in x) for x in arr)


def _merge_keyed(base: list, overlay: list) -> list:
    key_of = lambda x: x.get("code", x.get("id"))
    by_key = {key_of(x): dict(x) for x in base}
    order = [key_of(x) for x in base]
    for item in overlay:
        k = key_of(item)
        if k in by_key:
            by_key[k] = _deep_merge(by_key[k], item)
        else:
            by_key[k] = dict(item)
            order.append(k)
    return [by_key[k] for k in order]


def _load(path: Path, ctx: dict) -> dict:
    if not path.exists():
        return {}
    if tomllib is None:
        print(MANUAL_FALLBACK.format(**ctx), file=sys.stderr)
        sys.exit(2)
    try:
        with path.open("rb") as fh:
            data = tomllib.load(fh)
    except Exception as exc:  # malformed TOML -> manual fallback
        print(f"parse error in {path}: {exc}", file=sys.stderr)
        print(MANUAL_FALLBACK.format(**ctx), file=sys.stderr)
        sys.exit(2)
    return data


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Three-tier customization resolver.")
    ap.add_argument("--skill", required=True, help="artifact dir relative to repo root (e.g. agents/conductor)")
    ap.add_argument("--key", required=True, help="top-level table to resolve (e.g. agent, workflow)")
    ap.add_argument("--root", default=None, help="repo root (default: git toplevel)")
    args = ap.parse_args(argv)

    if args.root:
        root = Path(args.root)
    else:
        import subprocess
        try:
            root = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
        except Exception:
            print("could not determine repo root; pass --root", file=sys.stderr)
            return 2

    art_id = Path(args.skill).name
    base = root / args.skill / "customize.toml"
    team = root / ".agents" / "custom" / f"{art_id}.toml"
    user = root / ".agents" / "custom" / f"{art_id}.user.toml"
    ctx = {"base": str(base), "team": str(team), "user": str(user)}

    merged = {}
    for layer in (base, team, user):
        data = _load(layer, ctx)
        block = data.get(args.key, {})
        if not isinstance(block, dict):
            print(f"{layer}: key {args.key!r} is not a table", file=sys.stderr)
            return 2
        merged = _deep_merge(merged, block) if merged else dict(block)

    print(json.dumps(merged, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
