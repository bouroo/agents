#!/usr/bin/env python3
"""Trigger-rate runner for skill descriptions.

A skill's `description` carries the whole triggering decision: the host loads
only name + description up front, so a vague or over-broad one either never
fires or fires on everything. This runner scores a description the only way
that means anything -- run realistic prompts through a real agent and count
how often the skill was loaded.

    python3 evals/run_triggers.py                     # validate the set, no model
    python3 evals/run_triggers.py --skill quality     # validate one skill
    python3 evals/run_triggers.py --invoke '<cmd>'    # measure trigger rates

`--invoke` takes a shell command template; `{}` is replaced by the prompt and
the command's stdout+stderr is searched for `--marker`. The marker decides
what "triggered" means on your host, so calibrate it once against a run you
can read by eye. The default matches a skill load expressed as a path, a
`skill://` URI, or a JSON tool-call argument naming the skill:

    skill://quality | skills/quality/SKILL.md | "skill": "quality"

A prompt passes when its trigger rate clears `--threshold` (default 0.5, from
the set) on the side its `should_trigger` label names. Positives are scored on
the train and validation splits separately: train guides a description edit,
validation tells you whether the edit generalized. Tune on train only -- a
description chosen by its validation score is fitted to the test.

Stdlib only, no network: the model call belongs to the host, not to this file.
"""

import argparse
import json
import pathlib
import re
import shlex
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SET = ROOT / "evals" / "trigger.json"
DEFAULT_MARKER = r'skill://{skill}\b|skills/{skill}/SKILL\.md\b|"skill"\s*:\s*"{skill}"'

MIN_POSITIVES = 8
MIN_NEGATIVES = 6


def load(path: pathlib.Path) -> dict:
    return json.loads(path.read_text())


def problems(suite: dict) -> list[str]:
    """Structural defects in the query set: a set too thin to measure anything
    scores a description by luck, so shape is gated before any model runs."""
    out: list[str] = []
    skills = suite.get("skills")
    if not isinstance(skills, dict) or not skills:
        return ["no non-empty 'skills' map"]
    for name, splits in sorted(skills.items()):
        if not (ROOT / "skills" / name / "SKILL.md").is_file():
            out.append(f"{name}: no skills/{name}/SKILL.md")
        pos = neg = 0
        for split in ("train", "validation"):
            rows = splits.get(split)
            if not isinstance(rows, list) or not rows:
                out.append(f"{name}/{split}: missing or empty")
                continue
            for i, row in enumerate(rows):
                q = row.get("query")
                if not isinstance(q, str) or not q.strip():
                    out.append(f"{name}/{split}[{i}]: no query")
                if not isinstance(row.get("should_trigger"), bool):
                    out.append(f"{name}/{split}[{i}]: no boolean should_trigger")
                elif row["should_trigger"]:
                    pos += 1
                else:
                    neg += 1
        if pos < MIN_POSITIVES:
            out.append(f"{name}: {pos} should-trigger queries, need >= {MIN_POSITIVES}")
        if neg < MIN_NEGATIVES:
            out.append(f"{name}: {neg} should-not-trigger queries, need >= {MIN_NEGATIVES}")
    return out


def row_key(row: dict) -> str:
    return f"{row['should_trigger']}/{row['query'][:60]}"


def quoted_key(row: dict) -> str:
    return f"{'true' if row['should_trigger'] else 'false'}/{row['query']}"


def duplicate_queries(suite: dict) -> list[str]:
    """A prompt reused across skills or splits measures nothing: one skill's
    positive is another's near-miss only if the text differs."""
    seen: dict[str, str] = {}
    dupes: list[str] = []
    for name, splits in suite.get("skills", {}).items():
        for split, rows in splits.items():
            for row in rows:
                key = quoted_key(row)
                if key in seen:
                    dupes.append(f"{key[:60]} in {name}/{split} and {seen[key]}")
                else:
                    seen[key] = f"{name}/{split}"
    return dupes


def triggered(cmd: str, prompt: str, marker: re.Pattern) -> bool:
    try:
        res = subprocess.run(
            cmd.replace("{}", shlex.quote(prompt)),
            shell=True, capture_output=True, text=True, timeout=600,
        )
    except subprocess.TimeoutExpired:
        return False
    return bool(marker.search(res.stdout + res.stderr))


def measure(suite: dict, skills: list[str], cmd: str, marker_tpl: str,
            runs: int, threshold: float) -> int:
    """Print one line per query and a pass rate per split.

    The split rates are the point: a description tuned until train saturates
    and then scored on validation is the only run whose number means anything.
    Comparing iterations on train alone rewards memorizing the queries.
    """
    failures = 0
    totals: dict[str, list[int]] = {}
    for name in skills:
        marker = re.compile(marker_tpl.replace("{skill}", re.escape(name)))
        for split, rows in suite["skills"][name].items():
            for row in rows:
                hits = sum(triggered(cmd, row["query"], marker) for _ in range(runs))
                rate = hits / runs
                want = row["should_trigger"]
                ok = rate >= threshold if want else rate < threshold
                tally = totals.setdefault(split, [0, 0])
                tally[0] += ok
                tally[1] += 1
                if not ok:
                    failures += 1
                print(f"{'PASS' if ok else 'FAIL'} {name}/{split} "
                      f"want={'trigger' if want else 'skip'} rate={rate:.2f} "
                      f"{row['query'][:70]}")
    for split, (passed, count) in sorted(totals.items()):
        print(f"RATE {split}: {passed}/{count} = {passed / count:.2f}")
    return failures


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--set", default=str(SET), help="query set (default evals/trigger.json)")
    ap.add_argument("--skill", action="append", help="limit to these skills")
    ap.add_argument("--invoke", help="shell command template; '{}' is the prompt")
    ap.add_argument("--marker", default=DEFAULT_MARKER,
                    help="regex proving the skill loaded; '{skill}' is substituted")
    ap.add_argument("--runs", type=int, default=0, help="runs per query (default: set value)")
    ap.add_argument("--threshold", type=float, default=0.0,
                    help="pass threshold (default: set value)")
    args = ap.parse_args(argv)

    try:
        suite = load(pathlib.Path(args.set))
    except (OSError, ValueError) as exc:
        print(f"FAIL set: {exc}")
        return 1

    bad = problems(suite) + duplicate_queries(suite)
    if bad:
        for b in bad:
            print(f"FAIL set: {b}")
        return 1

    skills = args.skill or sorted(suite["skills"])
    unknown = [s for s in skills if s not in suite["skills"]]
    if unknown:
        print(f"FAIL set: no queries for {', '.join(unknown)}")
        return 1

    total = sum(len(rows) for s in skills for rows in suite["skills"][s].values())
    print(f"OK set: {len(skills)} skill(s), {total} quer(ies), "
          f"threshold={suite.get('threshold', 0.5)}, runs={suite.get('runs', 3)}")
    if not args.invoke:
        print("NOTE measure: pass --invoke '<cmd>' to score trigger rates")
        return 0

    runs = args.runs or int(suite.get("runs", 3))
    threshold = args.threshold or float(suite.get("threshold", 0.5))
    failures = measure(suite, skills, args.invoke, args.marker, runs, threshold)
    print(f"{'OK' if not failures else 'FAIL'}: {failures} quer(ies) outside threshold")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
