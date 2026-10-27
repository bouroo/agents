#!/usr/bin/env python3
"""Runner for the harness regression suite.

`evals/suite.json` holds one realistic task per eval plus objective checks
(a shell command and its expected exit code). This runner executes those
checks and reports the suite's pass rate -- the only honest answer to whether
a change made the harness better or worse.

    python3 evals/run_suite.py                # run every eval
    python3 evals/run_suite.py --eval <id>    # run one eval, repeatable
    python3 evals/run_suite.py --timeout 120  # per-check timeout (seconds)

Exit 0 iff every check matched its expected exit code, so the suite can gate
a merge the way `scripts/check.py` gates the doctrine.

Stdlib only, no network, no model call: a check that needs a model or a
credential belongs in the trigger set, not here.
"""

import argparse
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SET = ROOT / "evals" / "suite.json"

# A check that calls this runner would recurse (run_suite -> check ->
# run_suite -> ...). The depth travels in an environment variable, so a
# nested invocation skips the self-referential check instead of running it
# again; every other check still runs at every depth.
DEPTH_ENV = "AGENTS_EVAL_DEPTH"
SELF_MARKER = "run_suite.py"


def depth() -> int:
    try:
        return int(os.environ.get(DEPTH_ENV, "0"))
    except ValueError:
        return 0


def load(path: pathlib.Path) -> dict:
    return json.loads(path.read_text())


def run_check(cmd: str, timeout: int) -> tuple[int, str]:
    """Run one check, returning (exit code, output tail)."""
    try:
        res = subprocess.run(cmd, shell=True, cwd=ROOT, capture_output=True,
                             text=True, timeout=timeout,
                             env={**os.environ, DEPTH_ENV: str(depth() + 1)})
    except subprocess.TimeoutExpired:
        return 124, f"timeout after {timeout}s"
    return res.returncode, (res.stdout + res.stderr).strip()


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--set", default=str(SET), help="suite file (default evals/suite.json)")
    ap.add_argument("--eval", action="append", help="run only this eval id, repeatable")
    ap.add_argument("--timeout", type=int, default=300,
                    help="per-check timeout in seconds (default 300)")
    args = ap.parse_args(argv)

    try:
        suite = load(pathlib.Path(args.set))
    except (OSError, ValueError) as exc:
        print(f"FAIL suite: {exc}")
        return 1

    evals = suite.get("evals") or []
    if args.eval:
        wanted = set(args.eval)
        evals = [e for e in evals if e.get("id") in wanted]
        missing = wanted - {e.get("id") for e in evals}
        if missing:
            print(f"FAIL suite: no eval(s) {sorted(missing)}")
            return 1
    if not evals:
        print("FAIL suite: no evals to run")
        return 1

    passed = total = skipped = 0
    failures: list[str] = []
    for ev in evals:
        eid = ev.get("id", "?")
        for chk in ev.get("checks", []):
            cmd = chk.get("cmd", "")
            expect = chk.get("expect_exit", 0)
            if SELF_MARKER in cmd and depth() >= 1:
                skipped += 1
                print(f"SKIP {eid}: {cmd} (self-referential at depth {depth()})")
                continue
            total += 1
            code, out = run_check(cmd, args.timeout)
            ok = code == expect
            if ok:
                passed += 1
            else:
                failures.append(f"{eid}: {cmd} -> exit {code}, expected {expect}")
            tail = out.replace("\n", " | ")[:200]
            print(f"{'PASS' if ok else 'FAIL'} {eid}: {cmd} -> exit {code} {tail}")

    rate = passed / total if total else 0.0
    print(f"RATE {passed}/{total} = {rate:.2f}"
          + (f" ({skipped} skipped)" if skipped else ""))
    if failures:
        for f in failures:
            print(f"FAIL {f}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
