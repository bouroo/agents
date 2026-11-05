#!/usr/bin/env python3
"""Flag machine-detectable AI residue in a path, with the rule id attached.

The scanner finds candidates, not verdicts. Every hit is judged before it is
rewritten: a phrase can be legitimate in a project's own voice, and a rule
list cannot know the task's scope. The rule ids match the reference files
(prose.md, code.md, ui.md).

    python3 skills/unslop/scripts/scan.py path/to/dir
    python3 skills/unslop/scripts/scan.py --commits .
    python3 skills/unslop/scripts/scan.py --self-test

Stdlib only, read-only, no network. Exit 0 on a scan (a finding is not a
failure); exit 2 on a bad invocation, exit 1 on a failed self-test.
"""

import argparse
import pathlib
import re
import subprocess
import sys

# (rule_id, pattern, hint). Patterns run over the whole file with re.MULTILINE
# so a rule may span lines; the reported line number is the match start.
PROSE_RULES: list[tuple[str, str, str]] = [
    ("P3", r"\b(?:highlighting|ensuring|reflecting|showcasing|fostering)\b(?!\s+(?:the|a|an)\b)",
     "expand with the real source or delete"),
    ("P5", r"\b(?:Experts believe|Industry reports suggest|Some critics argue"
           r"|It is widely (?:believed|argued))\b",
     "name the source or delete"),
    ("P7", r"\b(?:crucial|delve|enduring|garner|interplay|intricate|pivotal|showcase"
           r"|tapestry|testament|underscore|vibrant|seamless|robust|gracefully"
           r"|comprehensive|groundbreaking|industry-leading|cutting-edge"
           r"|state-of-the-art|best-in-class)\b",
     "replace with the plain word"),
    ("P8", r"\b(?:serves as|stands as|boasts)\b", "say \"is\" or \"has\""),
    ("P9", r"\bnot just .{1,40}, but\b", "state the point directly"),
    ("P23", r"\b(?:In order to|Due to the fact that|It is important to note that)\b",
     "use the short form"),
    ("P25", r"\b(?:The future looks bright|Exciting times ahead)\b",
     "state specific plans or facts"),
    ("P26", r"\b(?:substrate|bedrock|gold-plating|endgame|north star|flywheel)\b",
     "use the concrete word"),
    ("P31", r"\b(?:utilize|leverage|facilitate|numerous)\b", "use the plain word"),
    ("P40", r"\b(?:improv(?:es|ing) (?:performance|reliability)"
            r"|enhanc(?:es|ing) (?:performance|reliability)"
            r"|more maintainable|seamless(?:ly)? experience)\b",
     "name what changed, where, and by how much"),
    ("P43", r"\b(?:lorem ipsum|coming soon|TBD|description here)\b"
            r"|\[\s*(?:insert|placeholder|X|your .{0,20} here)\s*\]",
     "replace with the real text or delete"),
    ("P45", r"(?:An error occurred|Something went wrong|Invalid input|Operation failed)"
           r"|raise \w*Error\(\s*[\"']Invalid input[\"']\s*\)",
     "name what failed and with which value"),
    ("P46", r"(?:Processing data|Starting operation|Doing work|Operation started)",
     "name the operation, the subject and the outcome"),
    ("P50", r"\b(?:In the future,? we (?:might|could|may) want to|Future work:)\b",
     "either the task ships it or the sentence goes"),
]

CODE_RULES: list[tuple[str, str, str]] = [
    ("C1", r"\b(?:TODO|FIXME|XXX|HACK)\b(?!\w)"
           r"|^[ \t]*(?:pass|return None|return \[\]|return \{\})[ \t]*(?:#.*)?$"
           r"|\braise NotImplementedError\b"
           r"|\bthrow new Error\((?:\"Not implemented|'Not implemented)",
     "the body is a placeholder: implement it or state plainly that it is a stub"),
    ("C3", r"\b(?:John Doe|Jane Doe|foo@bar\.(?:com|org)|lorem ipsum|aaa\.bbb|test_user)\b",
     "sample data that reads as filler"),
    ("C12", r"^[ \t]*#[ \t]*(?:increment|decrement|return|set|assign|create|initialize"
            r"|loop|call|check|update|add|get the)\b",
     "a comment restating the next line"),
    ("C13", r"^[ \t]*except\b[^\n]*:[ \t]*\n[ \t]+pass[ \t]*$",
     "an error that is swallowed: wrap it with context and propagate it"),
    ("C15", r"^[ \t]*(?://|#)[ \t]*(?:if|for|while|return|const|let|var|def|class|function)\b",
     "commented-out code: delete it, the history keeps it"),
    ("C18", r"\b(?:var|let|const)\s+(?:data|info|temp|result|value|item|obj)\b"
            r"|\bclass\s+(?:Manager|Handler|Processor|Helper|DataManager|BaseHelper)\b",
     "a vague name: name the domain, not the container"),
    ("C21", r"^[ \t]*return (?:None|\[\]|\{\})[ \t]*(?:#.*)?$",
     "check that the absence is distinguishable from the value"),
    ("C22", r"\b(?:timeout|retries|limit|delay)\s*=\s*\d+\b",
     "name the value or cite where it comes from"),
    ("C31", r"\bassert\s+\w+\.(?:mock|called|return_value)\b",
     "assert the behaviour, not the wiring"),
    ("C34", r"#.*\b(?:thread-safe|idempotent|guaranteed|no partial)\b",
     "enforce the guarantee or delete the claim"),
]

UI_RULES: list[tuple[str, str, str]] = [
    ("U2", r"\b(?:bg-gradient-to-\w+|from-(?:violet|purple|fuchsia|indigo|blue)-\d+"
           r"|via-(?:violet|purple|fuchsia|indigo|blue)-\d+)"
           r"|linear-gradient\([^)]*(?:violet|purple|#8b5cf6|#a855f7)",
     "hue gradient: one neutral surface, accent where it means something"),
    ("U2", r"\b(?:shadow-\[[^\]]*rgba\(|drop-shadow-\w+-\d|glow)\b",
     "coloured glow: depth comes from surface steps"),
    ("U4", r">\s*(?:[A-Z][A-Z0-9 ]{2,})\s*<",
     "an uppercase tracked label: sentence case"),
    ("U9", r"\b(?:animate-pulse|animate-ping|animate-bounce|transition-all|hover:scale-\d+)\b",
     "motion that loops for no reason"),
]

# Emoji and pictographs that read as decoration. Check and cross marks are
# excluded: a tick in a checklist carries meaning.
EMOJI_RE = re.compile(
    "[\u2600-\u26ff\u2700-\u27bf\U0001f000-\U0001faff\U0001f1e6-\U0001f1ff\ufe0f]")
EMOJI_ALLOW = set("\u2713\u2714\u2717\u2718")

# A commit subject that names a category and nothing else. The
# conventional-commit prefix is stripped first, so "refactor config module"
# and "fix: bug" are judged on what they say, not on the convention they use.
COMMIT_PREFIX = re.compile(
    r"^\s*(?:feat|fix|refactor|chore|docs|test|perf|build|ci|style)"
    r"(?:\([^)]*\))?!?:\s*(?P<payload>.+?)\s*$")
CATEGORY_WORD = re.compile(
    r"^\s*(?:feat|fix|refactor|chore|docs|test|perf|build|ci|style)\b",
    re.IGNORECASE)
VAGUE_PAYLOAD = re.compile(
    r"^(?:the\s+)?(?:bug|bugs|issue|issues|stuff|things?|changes?|update|updates"
    r"|cleanup|misc|todo|wip|temp|minor|typo|code|files?|file|config|configs"
    r"|parser|handler|module|logic|error|errors|broken|problem|problematic"
    r"|enhancement|improvement|refactoring)\b[\w\s]{0,20}$")

CODE_EXT = {".py", ".go", ".js", ".jsx", ".ts", ".tsx", ".java", ".rb", ".rs", ".php",
            ".kt", ".kts", ".scala", ".swift", ".c", ".h", ".cc", ".cpp", ".cs", ".ex",
            ".exs", ".sh", ".bash", ".sql", ".yaml", ".yml", ".toml", ".tf", ".vue",
            ".svelte", ".html", ".css", ".scss"}
PROSE_EXT = {".md", ".markdown", ".rst", ".txt", ".adoc"}
UI_EXT = {".jsx", ".tsx", ".html", ".css", ".scss", ".vue", ".svelte", ".js", ".ts"}
SKIP_DIRS = {".git", "node_modules", "vendor", "dist", "build", "target", ".venv",
             "__pycache__", ".next", ".tox", ".mypy_cache", ".pytest_cache"}


def compile_rules(rules: list[tuple[str, str, str]]) -> list[tuple[str, re.Pattern, str]]:
    return [(rule_id, re.compile(pattern, re.MULTILINE), hint)
            for rule_id, pattern, hint in rules]


def line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def vague_subject(subject: str) -> bool:
    """True when a commit subject names a category and no effect."""
    match = COMMIT_PREFIX.match(subject)
    if match:
        payload = match.group("payload")
    else:
        payload = subject
        category = CATEGORY_WORD.match(payload)
        if category:
            payload = payload[category.end():].strip()
    return bool(VAGUE_PAYLOAD.match(payload))


def in_except_body(text: str, lineno: int) -> bool:
    """True when the line sits directly under an `except` clause.

    A `pass` there is a swallowed error (C13), not a placeholder body (C1),
    and a scanner that reports it as both misclassifies it.
    """
    lines = text.splitlines()
    for i in range(lineno - 2, -1, -1):
        stripped = lines[i].strip()
        if not stripped:
            continue
        return stripped.startswith("except") or stripped.startswith("except:")
    return False


def typed_none_sentinel(text: str, lineno: int) -> bool:
    """True when the line's `return None` is the declared sentinel.

    A function annotated `-> str | None` returns None to mean absence, and
    the caller tells that apart from the value by the type. Reporting it as a
    placeholder body (C1) or an ambiguous absence (C21) is a false positive.
    """
    lines = text.splitlines()
    for i in range(lineno - 2, -1, -1):
        stripped = lines[i].strip()
        if stripped.startswith("def ") or stripped.startswith("async def "):
            return "| None" in stripped or "Optional[" in stripped
        # A top-level statement ends the function; the sentinel is not ours.
        if lines[i] and not lines[i][:1].isspace():
            return False
    return False


def first_line_of_comment_block(text: str, lineno: int) -> bool:
    """True when the line opens a comment block rather than continuing one.

    A comment block's first line may name the narration a later line
    continues ("# The scan covers the doctrine an agent loads - AGENTS.md,
    # skills, commands"), so only the opening line can be the narration.
    """
    lines = text.splitlines()
    if lineno - 2 < 0:
        return True
    previous = lines[lineno - 2].strip()
    return not (previous.startswith("#") or previous.startswith("//"))


def scan_text(text: str, families: list[tuple[str, re.Pattern, str]]) -> list[tuple[int, str, str, str]]:
    """Every rule hit in one text, with its line number."""
    hits: list[tuple[int, str, str, str]] = []
    for rule_id, pattern, hint in families:
        for match in pattern.finditer(text):
            lineno = line_of(text, match.start())
            if rule_id == "C1" and match.group(0).strip() == "pass" \
                    and in_except_body(text, lineno):
                continue
            if rule_id in ("C1", "C21") and match.group(0).strip() == "return None" \
                    and typed_none_sentinel(text, lineno):
                continue
            if rule_id in ("C12", "C15") and not first_line_of_comment_block(text, lineno):
                continue
            snippet = " ".join(match.group(0).split())[:60]
            hits.append((lineno, rule_id, snippet, hint))
    return sorted(hits)


def scan_emoji(text: str) -> list[tuple[int, str, str, str]]:
    hits = []
    for match in EMOJI_RE.finditer(text):
        if match.group(0) in EMOJI_ALLOW:
            continue
        hits.append((line_of(text, match.start()), "U3", match.group(0),
                     "emoji as an icon: one line icon set"))
    return hits


def families_for(path: pathlib.Path) -> list[tuple[str, re.Pattern, str]]:
    families: list[tuple[str, re.Pattern, str]] = []
    suffix = path.suffix.lower()
    if suffix in PROSE_EXT:
        families += compile_rules(PROSE_RULES)
    if suffix in CODE_EXT:
        families += compile_rules(CODE_RULES)
    if suffix in UI_EXT:
        families += compile_rules(UI_RULES)
    return families


def walk(root: pathlib.Path):
    if root.is_file():
        yield root
        return
    for path in sorted(root.rglob("*")):
        if path.is_file() and not any(part in SKIP_DIRS for part in path.parts):
            yield path


def git_commit_subjects(root: pathlib.Path) -> list[str]:
    try:
        out = subprocess.run(["git", "-C", str(root), "log", "-n", "50", "--pretty=%s"],
                             capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return []
    if out.returncode != 0:
        return []
    return [line for line in out.stdout.splitlines() if line.strip()]


def self_test() -> int:
    """Assert the scanner finds what it claims and stays quiet otherwise."""
    cases: list[tuple[str, str, str | None]] = [
        ("prose.md", "We delve into the crucial aspects of the solution.", "P7"),
        ("prose.md", "In order to improve performance, we refactored the parser.", "P23"),
        ("prose.md", "The parser raises an error: Something went wrong.", "P45"),
        ("prose.md", "Retry the three transient errors the client reports.", None),
        ("code.py", "def f():\n    pass\n", "C1"),
        ("code.py", "try:\n    x()\nexcept Exception:\n    pass\n", "C13"),
        ("code.py", "user_email = 'foo@bar.com'\n", "C3"),
        ("code.py", "def f():\n    return 42\n", None),
        ("code.py", "def f(path):\n    with open(path) as fh:\n        return fh.read()\n", None),
        ("ui.tsx", "<div className='bg-gradient-to-r from-violet-500 to-blue-500' />", "U2"),
        ("ui.tsx", "<span>\N{SPARKLES}</span>", "U3"),
        ("ui.tsx", "<div className='animate-pulse' />", "U9"),
        ("ui.tsx", "<div className='flex items-center p-4'>\n  <Nav />\n</div>\n", None),
        # A job-named class is not a vague name: C25 asks for exactly that.
        ("code.py", "class PaymentProcessor:\n    pass\n", "C1"),
        # A `pass` under an except is a swallowed error, not a placeholder body.
        ("code.py", "try:\n    x()\nexcept Exception:\n    pass\n", "C13"),
        # The hype register the forward test showed missing.
        ("prose.md", "A robust, seamless solution that handles errors gracefully.", "P7"),
        ("prose.md", "Our industry-leading approach leverages cutting-edge techniques.", "P7"),
    ]
    failures = []
    for name, text, expected in cases:
        path = pathlib.Path(name)
        hits = scan_text(text, families_for(path))
        if path.suffix in UI_EXT:
            hits += scan_emoji(text)
        rules = {rule for _, rule, _, _ in hits}
        if expected is None:
            if rules:
                failures.append(f"{name}: expected no hit, got {sorted(rules)}")
        elif expected not in rules:
            failures.append(f"{name}: expected {expected}, got {sorted(rules) or 'none'}")

    if not vague_subject("refactor config module"):
        failures.append("vague_subject missed 'refactor config module'")
    if not vague_subject("fix: bug"):
        failures.append("vague_subject missed 'fix: bug'")
    if vague_subject("reject the three transient errors the client reports"):
        failures.append("vague_subject fired on a descriptive subject")
    if vague_subject("retryBudget(3, 500*time.Millisecond) retries the client errors"):
        failures.append("vague_subject fired on a descriptive subject")

    # A typed sentinel (`-> str | None`) is the declared absence, not a stub.
    sentinel = "def find(path) -> str | None:\n    if not path.is_file():\n        return None\n    return path.read_text()\n"
    sentinel_rules = {r for _, r, _, _ in scan_text(sentinel, families_for(pathlib.Path("code.py")))}
    if sentinel_rules & {"C1", "C21"}:
        failures.append(f"typed None sentinel was flagged: {sorted(sentinel_rules)}")

    # An untyped `return None` in a plain function is still a placeholder.
    untyped = "def find(path):\n    if not path.is_file():\n        return None\n"
    untyped_rules = {r for _, r, _, _ in scan_text(untyped, families_for(pathlib.Path("code.py")))}
    if "C1" not in untyped_rules:
        failures.append("an untyped `return None` placeholder was not flagged")

    # A narration comment opening a block is flagged; a continuation is not.
    block = ("# Files scanned for host tokens: everything an assistant consumes\n"
             "# as doctrine. The scan covers the doctrine an agent loads -\n"
             "# set rather than being allowlisted within it.\n")
    block_rules = {r for _, r, _, _ in scan_text(block, families_for(pathlib.Path("code.py")))}
    if "C12" in block_rules:
        failures.append("a comment-block continuation was flagged as narration")

    # The same narration word opening a block IS flagged.
    opening = "# increment the counter\nx += 1\n"
    opening_rules = {r for _, r, _, _ in scan_text(opening, families_for(pathlib.Path("code.py")))}
    if "C12" not in opening_rules:
        failures.append("a narration comment opening a block was not flagged")

    # The except-body `pass` is C13's case; C1 must not also claim it.
    swallowed = "try:\n    x()\nexcept Exception:\n    pass\n"
    swallowed_rules = {r for _, r, _, _ in scan_text(swallowed, families_for(pathlib.Path("code.py")))}
    if "C1" in swallowed_rules:
        failures.append(f"swallowed-except pass was classified as C1 too: {sorted(swallowed_rules)}")

    # A job-named class must not trip the vague-name rule.
    job_named = "class PaymentProcessor:\n    pass\n"
    job_rules = {r for _, r, _, _ in scan_text(job_named, families_for(pathlib.Path("code.py")))}
    if "C18" in job_rules:
        failures.append("C18 fired on a job-named class")

    for line in failures:
        print(f"FAIL self-test: {line}", file=sys.stderr)
    if failures:
        return 1
    print(f"OK self-test: {len(cases)} pattern cases and 4 commit-subject cases pass")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("path", nargs="*", help="file or directory to scan (repeatable)")
    parser.add_argument("--commits", action="store_true",
                        help="also scan the last 50 commit subjects")
    parser.add_argument("--self-test", action="store_true",
                        help="check the scanner's own patterns and exit")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()
    if not args.path:
        parser.error("path is required unless --self-test is given")

    roots = []
    for raw in args.path:
        candidate = pathlib.Path(raw).resolve()
        if not candidate.exists():
            print(f"scan: no such path: {candidate}", file=sys.stderr)
            return 2
        roots.append(candidate)

    total = 0
    for root in roots:
        for path in walk(root):
            try:
                text = path.read_text(errors="replace")
            except OSError:
                continue
            hits = scan_text(text, families_for(path))
            if path.suffix.lower() in UI_EXT:
                hits += scan_emoji(text)
            for lineno, rule_id, snippet, hint in hits:
                total += 1
                print(f"{path}:{lineno}: {rule_id} {snippet!r} -> {hint}")

    if args.commits:
        for root in roots:
            repo = root if root.is_dir() else root.parent
            for subject in git_commit_subjects(repo):
                if vague_subject(subject):
                    total += 1
                    print(f"<commit>: {subject!r} -> P41 say what the code now does")

    print(f"scan: {total} candidate(s); judge each before rewriting")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
