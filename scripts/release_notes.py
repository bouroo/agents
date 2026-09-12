#!/usr/bin/env python3
"""Print one version's CHANGELOG section, for a release body.

Deterministic and dependency-free: the release workflow must not paraphrase a
release body, and a body rebuilt from memory or excerpts is fabrication. This
reads the section verbatim from CHANGELOG.md, so the published notes and the
committed notes are the same bytes.

    python3 scripts/release_notes.py 6.0.0-beta.1   # body only
    python3 scripts/release_notes.py --tag v6.0.0    # strip a leading 'v'

Exit 0 with the body on stdout; exit 1 (message on stderr) when the version has
no section, so a tag without notes fails the release rather than publishing an
empty body.
"""

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHANGELOG = ROOT / "CHANGELOG.md"


def section(text: str, version: str) -> str | None:
    """The body under `## [<version>]`, up to the next `## [` heading.

    Returns None when no such heading exists. The heading line itself is not
    part of the body: the release title carries the version.
    """
    lines = text.splitlines()
    start = None
    heading = re.compile(r"^##\s+\[?" + re.escape(version) + r"\]?(\s|$)")
    for i, line in enumerate(lines):
        if heading.match(line):
            start = i + 1
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    return "\n".join(lines[start:end]).strip()


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Print one version's CHANGELOG section.")
    parser.add_argument("version", help="version to extract, e.g. 6.0.0-beta.1")
    parser.add_argument("--tag", action="store_true",
                        help="treat the argument as a git tag (strip a leading 'v')")
    args = parser.parse_args(argv)

    if not CHANGELOG.is_file():
        print("release_notes: CHANGELOG.md missing", file=sys.stderr)
        return 1

    version = args.version
    if args.tag and version.startswith("v"):
        version = version[1:]

    body = section(CHANGELOG.read_text(), version)
    if body is None:
        print(f"release_notes: no CHANGELOG section for {version!r} - "
              "add one before tagging", file=sys.stderr)
        return 1
    if not body:
        print(f"release_notes: CHANGELOG section for {version!r} is empty",
              file=sys.stderr)
        return 1

    print(body)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
