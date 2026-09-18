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
    comments        the comment rule survives on both canonical surfaces
                    (manifesto clause + skills/craft), so neither can lose it
    simplicity      the simplicity rule survives on both canonical surfaces
                    (manifesto clause + skills/craft), so neither can lose it
    modernize       every modernize-coding adapter is present and version-pinned;
                    Go and Java claims match their toolchain's own local record
                    (GOROOT/api, JDK src.zip @since) of when each feature landed

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
import shutil
import subprocess
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


# A code rule lives on two canonical surfaces: the always-loaded clause in
# the manifesto, and the on-demand detail in the skill that owns it. Prose
# cannot be linted for meaning, so these gates assert PRESENCE instead - the
# failure mode they catch is a surface silently losing the rule, not a
# surface wording it differently. Rewording a surface means updating its
# marker here; that is the deliberate cost of gating prose rather than code.
RULE_SURFACES = {
    "comments": [
        ("AGENTS.md", re.compile(r"restates? the code", re.IGNORECASE)),
        ("skills/craft/SKILL.md", re.compile(r"^## Comments$", re.MULTILINE)),
    ],
    "simplicity": [
        ("AGENTS.md", re.compile(r"second real caller", re.IGNORECASE)),
        ("skills/craft/SKILL.md", re.compile(r"^## Simplicity$", re.MULTILINE)),
    ],
}


def _g_rule_surfaces(name: str) -> None:
    surfaces = RULE_SURFACES[name]
    missing: list[str] = []
    for rel, pattern in surfaces:
        path = ROOT / rel
        if not path.is_file():
            missing.append(f"{rel} missing")
        elif not pattern.search(path.read_text()):
            missing.append(f"{rel} no longer states the rule")
    if missing:
        _add("FAIL", f"{name}: " + "; ".join(missing))
        return
    _add("PASS", f"{name}: rule present on "
                 f"{len(surfaces)} canonical surface(s)")


def g_comments() -> None:
    _g_rule_surfaces("comments")


def g_simplicity() -> None:
    _g_rule_surfaces("simplicity")


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


# Every adapter's version table is a set of claims about a toolchain, and a wrong
# one is a code-generation defect: told `maps.Copy` needs 1.23, an agent on a
# `go 1.21` module hand-writes the legacy loop the whole skill exists to retire.
# So pin each claim against a local, authoritative, regenerable anchor -- Go's
# GOROOT/api, Java's JDK src.zip @since -- rather than trusting the prose. Where
# no local anchor exists (the ecosystem publishes only web docs), assert the
# claim is PINNED to a version still, so a rewrite silently losing its version
# cell fails rather than passing unnoticed. Scoped per adapter.
MODERNIZE_DOC = "pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize"

# Go: (file, row token, GOROOT/api line prefix, claimed version). Every table row
# whose feature is a stdlib symbol is covered; rows whose feature is a language
# change (any, min/max, loopvar, range-over-int, omitzero, new(expr)) or has no
# machine-readable record (unsafe, //go:build) are not anchorable here and are
# deliberately absent rather than faked.
GO_CLAIMS = [
    ("guide.md", "wg.Go(", "pkg sync, method (*WaitGroup) Go(", "1.25"),
    ("guide.md", "min(a, b)", None, "1.21"),
    ("guide.md", "slices.Contains", "pkg slices, func Contains[", "1.21"),
    ("guide.md", "slices.Sort", "pkg slices, func Sort[", "1.21"),
    ("guide.md", "fmt.Appendf", "pkg fmt, func Appendf(", "1.19"),
    ("guide.md", "maps.Copy", "pkg maps, func Copy[", "1.21"),
    ("guide.md", "slices.Backward", "pkg slices, func Backward[", "1.23"),
    ("guide.md", "strings.SplitSeq", "pkg strings, func SplitSeq(", "1.24"),
    ("guide.md", "t.Context", "pkg testing, method (*T) Context(", "1.24"),
    ("guide.md", "errors.AsType", "pkg errors, func AsType[", "1.26"),
    ("analyzers.md", "`stringscut`", "pkg strings, func Cut(", "1.18"),
    ("analyzers.md", "`stringscutprefix`", "pkg strings, func CutPrefix(", "1.20"),
    ("analyzers.md", "`fmtappendf`", "pkg fmt, func Appendf(", "1.19"),
    ("analyzers.md", "`slicescontains`", "pkg slices, func Contains[", "1.21"),
    ("analyzers.md", "`slicesclip`", "pkg slices, func Clip[", "1.21"),
    ("analyzers.md", "`slicessort`", "pkg slices, func Sort[", "1.21"),
    ("analyzers.md", "`atomictypes`", "pkg sync/atomic, type Int32", "1.19"),
    ("analyzers.md", "`reflecttypefor`", "pkg reflect, func TypeFor[", "1.22"),
    ("analyzers.md", "`mapsloop`", "pkg maps, func Copy[", "1.21"),
    ("analyzers.md", "`slicesbackward`", "pkg slices, func Backward[", "1.23"),
    ("analyzers.md", "`stringsseq`", "pkg strings, func SplitSeq(", "1.24"),
    ("analyzers.md", "`testingcontext`", "pkg testing, method (*T) Context(", "1.24"),
    ("analyzers.md", "`waitgroup`", "pkg sync, method (*WaitGroup) Go(", "1.25"),
    ("analyzers.md", "`reflecttypeassert`", "pkg reflect, func TypeAssert[", "1.25"),
    ("analyzers.md", "`errorsastype`", "pkg errors, func AsType[", "1.26"),
    ("analyzers.md", "`stringsbuilder`", "pkg strings, type Builder", "1.10"),
    ("analyzers.md", "`plusbuild`", None, "1.17"),
]

# Java: (zip path, declaration regex, claimed version). Anchored to the @since
# javadoc tag in the JDK's own lib/src.zip -- Java's analog of GOROOT/api. The
# tag is taken from the text BEFORE the matched declaration: a file's last
# @since belongs to some later member, not the type (HttpClient.java's last tag
# is 21 while the type is 11).
JAVA_SRC = "skills/modernize-coding/references/java/guide.md"
JAVA_CLAIMS = [
    ("List.of(", "java.base/java/util/List.java", r"static\s+<E>\s+List<E>\s+of\(", "9"),
    ("Set.of(", "java.base/java/util/Set.java", r"static\s+<E>\s+Set<E>\s+of\(", "9"),
    ("Map.of(", "java.base/java/util/Map.java", r"static\s+<K,\s*V>\s+Map<K,\s*V>\s+of\(", "9"),
    ("ifPresentOrElse", "java.base/java/util/Optional.java", r"public\s+void\s+ifPresentOrElse\(", "9"),
    ("stream()", "java.base/java/util/Optional.java", r"public\s+Stream<T>\s+stream\(\)", "9"),
    ("List.copyOf(", "java.base/java/util/List.java", r"static\s+<E>\s+List<E>\s+copyOf\(", "10"),
    ("str.strip()", "java.base/java/lang/String.java", r"public\s+String\s+strip\(\)", "11"),
    ("str.isBlank()", "java.base/java/lang/String.java", r"public\s+boolean\s+isBlank\(\)", "11"),
    ("str.repeat(", "java.base/java/lang/String.java", r"public\s+String\s+repeat\(int", "11"),
    ("str.lines()", "java.base/java/lang/String.java", r"public\s+Stream<String>\s+lines\(\)", "11"),
    ("opt.isEmpty()", "java.base/java/util/Optional.java", r"public\s+boolean\s+isEmpty\(\)", "11"),
    ("Files.readString(", "java.base/java/nio/file/Files.java", r"public\s+static\s+String\s+readString\(", "11"),
    ("str.indent(", "java.base/java/lang/String.java", r"public\s+String\s+indent\(int", "12"),
    ("Files.mismatch(", "java.base/java/nio/file/Files.java", r"public\s+static\s+long\s+mismatch\(", "12"),
    ("Collectors.teeing", "java.base/java/util/stream/Collectors.java",
     r"public\s+static\s+<T,\s*R1,\s*R2,\s*R>\s+Collector<T,\s*\?,\s*R>\s+teeing\(", "12"),
    ("stream.toList()", "java.base/java/util/stream/Stream.java", r"default\s+List<T>\s+toList\(\)", "16"),
    ("mapMulti", "java.base/java/util/stream/Stream.java", r"default\s+<R>\s+Stream<R>\s+mapMulti\(", "16"),
    ("Thread.ofVirtual(", "java.base/java/lang/Thread.java", r"public\s+static\s+Builder\.OfVirtual\s+ofVirtual\(\)", "21"),
    ("SequencedCollection", "java.base/java/util/SequencedCollection.java",
     r"public\s+interface\s+SequencedCollection", "21"),
    ("SequencedMap", "java.base/java/util/SequencedMap.java", r"public\s+interface\s+SequencedMap", "21"),
    ("newVirtualThreadPerTaskExecutor", "java.base/java/util/concurrent/Executors.java",
     r"public\s+static\s+ExecutorService\s+newVirtualThreadPerTaskExecutor\(\)", "21"),
]

# Adapters whose ecosystem publishes version facts only as web docs (no local
# machine-readable index). Their tables cannot be cross-checked against a
# toolchain record here, but their values ARE pinned, so a silent edit to a
# version is still a gate failure. Each was doc-verified when written; see the
# adapter's verify.md for how to re-derive them.
UNANCHORED_ADAPTERS = {
    "rust": "skills/modernize-coding/references/rust/guide.md",
    "python": "skills/modernize-coding/references/python/guide.md",
    "typescript": "skills/modernize-coding/references/typescript/guide.md",
}

# (adapter, row token, claimed version) for the unanchored adapters. Versions
# come from the docs each verify.md cites: CPython library-reference "Added in
# version" notes and the 3.9 whats-new (PEP 584/585/654); TC39's finished-
# proposals publication years; Rust's edition guide and stable-edition report.
UNANCHORED_CLAIMS = [
    ("python", "list[...]", "3.9"),
    ("python", "X \\| None", "3.10"),
    ("python", "(PEP 695)", "3.12"),
    ("python", "typing.override", "3.12"),
    ("python", "typing.Self", "3.11"),
    ("python", "str.removeprefix", "3.9"),
    ("python", "except*", "3.11"),
    ("python", "functools.cache", "3.9"),
    ("python", "itertools.pairwise", "3.10"),
    ("python", "itertools.batched", "3.12"),
    ("python", "Path.walk", "3.12"),
    ("python", "Path.is_relative_to", "3.9"),
    ("python", "zoneinfo", "3.9"),
    ("python", "graphlib.TopologicalSorter", "3.9"),
    ("python", "tomllib", "3.11"),
    ("python", "asyncio.TaskGroup", "3.11"),
    ("rust", "impl Trait", "1.26"),
    ("rust", "`try!(x)`", "2018"),
    ("rust", "`extern crate foo;`", "2018"),
    ("rust", "`dyn Trait` written as bare", "2021"),
    ("typescript", "arrow function", "ES2015"),
    ("typescript", "template literal", "ES2015"),
    ("typescript", "object spread", "ES2018"),
    ("typescript", "optional chaining `x?.y?.z`", "ES2020"),
    ("typescript", "nullish coalescing `x ?? d`", "ES2020"),
    ("typescript", "x ??=", "ES2021"),
    ("typescript", "Object.hasOwn(o, k)", "ES2022"),
    ("typescript", "arr.at(-1)", "ES2022"),
    ("typescript", "findLast()", "ES2023"),
    ("typescript", "toSorted()", "ES2023"),
    ("typescript", "toReversed()", "ES2023"),
    ("typescript", "arr.with(n, x)", "ES2023"),
    ("typescript", "toSpliced()", "ES2023"),
    ("typescript", "`#private` fields", "ES2022"),
    ("typescript", "top-level `await`", "ES2022"),
]
# A version cell must name a release, an edition, or a named idiom lint. Accepts
# bare releases ("1.70", "2021"), "+"-ranges ("1.70+"), ECMAScript editions
# ("ES2020"), TS versions ("TS 4.9"), and the lint/idiom classes where an
# ecosystem has no version number for the change at all. Anything else -- "new",
# "always", a bare "modern" -- is not a claim the toolchain could be probed
# against, and fails.
VERSION_CELL_RE = re.compile(
    r"\|\s*("
    r"\d+(?:\.\d+)*\+?"          # 1.70, 1.70+, 3.9
    r"|ES\d{4}|ESNext"           # ECMAScript editions
    r"|TS \d+\.\d+"              # TypeScript versions
    r"|Node \d+\+"               # runtime floors
    r"|ecma\b.*"                 # "ecma2015" style
    r"|clippy lint|pre-1\.0 idiom|tsconfig|WHATWG.*"
    r")\s*\|\s*$",
    re.IGNORECASE,
)

# (file, row token, GOROOT/api line prefix, claimed version). Every table row
# whose feature is a stdlib symbol is covered; rows whose feature is a language
# change (any, min/max, loopvar, range-over-int, omitzero, new(expr)) or has no
# machine-readable record (unsafe, //go:build) are not anchorable here and are
# deliberately absent rather than faked.
SYMBOL_CLAIMS = [
    ("guide.md", "wg.Go(", "pkg sync, method (*WaitGroup) Go(", "1.25"),
    ("guide.md", "min(a, b)", None, "1.21"),
    ("guide.md", "slices.Contains", "pkg slices, func Contains[", "1.21"),
    ("guide.md", "slices.Sort", "pkg slices, func Sort[", "1.21"),
    ("guide.md", "fmt.Appendf", "pkg fmt, func Appendf(", "1.19"),
    ("guide.md", "maps.Copy", "pkg maps, func Copy[", "1.21"),
    ("guide.md", "slices.Backward", "pkg slices, func Backward[", "1.23"),
    ("guide.md", "strings.SplitSeq", "pkg strings, func SplitSeq(", "1.24"),
    ("guide.md", "t.Context", "pkg testing, method (*T) Context(", "1.24"),
    ("guide.md", "errors.AsType", "pkg errors, func AsType[", "1.26"),
    ("analyzers.md", "`stringscut`", "pkg strings, func Cut(", "1.18"),
    ("analyzers.md", "`stringscutprefix`", "pkg strings, func CutPrefix(", "1.20"),
    ("analyzers.md", "`fmtappendf`", "pkg fmt, func Appendf(", "1.19"),
    ("analyzers.md", "`slicescontains`", "pkg slices, func Contains[", "1.21"),
    ("analyzers.md", "`slicesclip`", "pkg slices, func Clip[", "1.21"),
    ("analyzers.md", "`slicessort`", "pkg slices, func Sort[", "1.21"),
    ("analyzers.md", "`atomictypes`", "pkg sync/atomic, type Int32", "1.19"),
    ("analyzers.md", "`reflecttypefor`", "pkg reflect, func TypeFor[", "1.22"),
    ("analyzers.md", "`mapsloop`", "pkg maps, func Copy[", "1.21"),
    ("analyzers.md", "`slicesbackward`", "pkg slices, func Backward[", "1.23"),
    ("analyzers.md", "`stringsseq`", "pkg strings, func SplitSeq(", "1.24"),
    ("analyzers.md", "`testingcontext`", "pkg testing, method (*T) Context(", "1.24"),
    ("analyzers.md", "`waitgroup`", "pkg sync, method (*WaitGroup) Go(", "1.25"),
    ("analyzers.md", "`reflecttypeassert`", "pkg reflect, func TypeAssert[", "1.25"),
    ("analyzers.md", "`errorsastype`", "pkg errors, func AsType[", "1.26"),
    ("analyzers.md", "`stringsbuilder`", "pkg strings, type Builder", "1.10"),
    ("analyzers.md", "`plusbuild`", None, "1.17"),
]


def _api_versions() -> dict[str, int]:
    """Map each GOROOT/api line to the minor Go version that introduced it."""
    out: dict[str, int] = {}
    goroot = subprocess.run(["go", "env", "GOROOT"], capture_output=True,
                            text=True, check=True).stdout.strip()
    numbered: list[tuple[int, pathlib.Path]] = []
    for f in pathlib.Path(goroot, "api").glob("go1.*.txt"):
        if m := re.search(r"go1\.(\d+)\.txt$", f.name):
            numbered.append((int(m.group(1)), f))
    for minor, f in sorted(numbered):
        for line in f.read_text().splitlines():
            out.setdefault(line, minor)
    return out


def _find_java_src_zip() -> str | None:
    """Locate a JDK lib/src.zip: JAVA_HOME, macOS layouts, then Homebrew."""
    import glob
    import os
    java_home = os.environ.get("JAVA_HOME", "")
    candidates = ([os.path.join(java_home, "lib/src.zip")] if java_home else []) + \
        glob.glob("/Library/Java/JavaVirtualMachines/*/Contents/Home/lib/src.zip") + \
        glob.glob("/opt/homebrew/Cellar/openjdk*/*/libexec/openjdk.jdk/Contents/Home/lib/src.zip") + \
        glob.glob("/usr/lib/jvm/*/lib/src.zip")
    return next((c for c in candidates if os.path.isfile(c)), None)


def _json_doc_present(rel_path: str, doc: str, problems: list[str]) -> str | None:
    path = ROOT / rel_path
    if not path.is_file():
        problems.append(f"{rel_path} missing")
        return None
    text = path.read_text()
    if doc not in text:
        problems.append(f"{rel_path} no longer points at the live inventory ({doc})")
    return text


def _table_row_version(text: str, token: str) -> str | None:
    """The trailing version cell of the first table row containing token."""
    row = next((ln for ln in text.splitlines()
                if token in ln and ln.lstrip().startswith("|")), None)
    if row is None:
        return None
    m = re.search(r"\|\s*([^|]+?)\s*\|\s*$", row)
    return m.group(1) if m else None


def g_modernize() -> None:
    name = "modernize"
    problems: list[str] = []
    verified = 0
    asserted = 0

    # --- Go: anchored to GOROOT/api ---
    texts = {}
    for label, rel in (("guide.md", "skills/modernize-coding/references/go/guide.md"),
                       ("analyzers.md", "skills/modernize-coding/references/go/analyzers.md")):
        t = _json_doc_present(rel, MODERNIZE_DOC, problems)
        if t is not None:
            texts[label] = t
    try:
        api = _api_versions() if shutil.which("go") else {}
    except (OSError, subprocess.SubprocessError):
        api = {}
    for label, token, prefix, claimed in GO_CLAIMS:
        if label not in texts:
            continue
        got = _table_row_version(texts[label], token)
        if got is None:
            problems.append(f"go/{label}: no version row for {token}")
            continue
        if got != claimed:
            problems.append(f"go/{label}: {token} says {got!r}, gate expects {claimed}")
            continue
        if prefix and api:
            actual = next((v for line, v in api.items() if line.startswith(prefix)), None)
            if actual is None:
                problems.append(f"go/{label}: {token} absent from GOROOT/api")
            elif actual != int(claimed.split(".")[1]):
                problems.append(f"go/{label}: {token} says {claimed}, "
                                f"toolchain added it in go1.{actual}")
            else:
                verified += 1
        else:
            asserted += 1

    # --- Java: anchored to JDK src.zip @since ---
    java_text = _json_doc_present(JAVA_SRC, "src.zip", problems)
    src_zip = _find_java_src_zip()
    if java_text is not None:
        # The declared table is checked against the JDK first, so an edit that
        # corrupts guide.md is caught even on a host with no src.zip; the @since
        # cross-check then proves the DECLARED version is the true one.
        for token, _path, _pattern, claimed in JAVA_CLAIMS:
            got = _table_row_version(java_text, token)
            if got is None:
                problems.append(f"java: no version row for {token}")
            elif got != claimed:
                problems.append(f"java: {token} says {got!r}, gate expects {claimed}")
        if src_zip is None:
            asserted += len(JAVA_CLAIMS)
        else:
            import zipfile
            z = zipfile.ZipFile(src_zip)
            names = set(z.namelist())
            cache: dict[str, str] = {}
            for token, path, pattern, claimed in JAVA_CLAIMS:
                if path not in names:
                    problems.append(f"java: {path} not in src.zip")
                    continue
                if path not in cache:
                    cache[path] = z.read(path).decode("utf-8", "replace")
                m = re.search(pattern, cache[path])
                if not m:
                    problems.append(f"java: declaration not found in {path}")
                    continue
                tags = re.findall(r"@since\s+([0-9.]+)", cache[path][:m.start()])
                actual = tags[-1] if tags else "?"
                if actual != claimed:
                    problems.append(f"java: {token} ({path}) claims {claimed}, "
                                    f"@since says {actual}")
                else:
                    verified += 1

    # --- Unanchored adapters: every row pinned, and each listed claim exact ---
    texts_by_lang: dict[str, str] = {}
    for lang, rel in UNANCHORED_ADAPTERS.items():
        path = ROOT / rel
        if not path.is_file():
            problems.append(f"{lang}: {rel} missing")
            continue
        texts_by_lang[lang] = path.read_text()
        rows = [ln for ln in texts_by_lang[lang].splitlines()
                if ln.lstrip().startswith("|") and ln.count("|") >= 3]
        datarows = [ln for ln in rows if not set(ln) <= set("|-: ")]
        pinned = sum(1 for ln in datarows if VERSION_CELL_RE.search(ln))
        if pinned == 0:
            problems.append(f"{lang}: {rel} has no version-pinned rows")
        asserted += pinned
    for lang, token, claimed in UNANCHORED_CLAIMS:
        if lang not in texts_by_lang:
            continue
        got = _table_row_version(texts_by_lang[lang], token)
        if got is None:
            problems.append(f"{lang}: no version row for {token}")
        elif got != claimed:
            problems.append(f"{lang}: {token} says {got!r}, gate expects {claimed}")
        else:
            asserted += 1

    if problems:
        _add("FAIL", f"{name}: " + "; ".join(problems[:8])
             + (" ..." if len(problems) > 8 else ""))
        return
    anchors = []
    if shutil.which("go"):
        anchors.append("GOROOT/api")
    if src_zip:
        anchors.append("JDK src.zip")
    suffix = (f"{verified} cross-checked against {', '.join(anchors)}"
              if anchors else "no local anchor available to cross-check")
    _add("PASS", f"{name}: {len(UNANCHORED_ADAPTERS) + 2} adapter(s) present; "
                 f"{asserted} claim(s) version-pinned, {suffix}")


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
         ("comments", g_comments), ("simplicity", g_simplicity),
         ("modernize", g_modernize), ("evals", g_evals)]


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
