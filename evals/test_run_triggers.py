#!/usr/bin/env python3
"""Deterministic check for measure()'s parallel path.

No model call: `triggered` is stubbed, so the parallel machinery (row order,
per-row rate, pass/fail tally, shared-state safety) is what is under test.
A bug that reorders rows, misattributes a rate, double-counts the tally, or
lets a worker write shared state shows up as a serial/parallel mismatch here.
"""

import contextlib
import io
import threading

import run_triggers as rt


def _make_suite(rows):
    return {"skills": {"q": {"train": rows}}}


def _run(workers, rows, runs=1, threshold=0.5):
    lock = threading.Lock()
    calls = []

    def fake_triggered(cmd, prompt, marker):
        with lock:
            calls.append(prompt)
        return "yes" in prompt

    rt.triggered = fake_triggered
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        failures = rt.measure(_make_suite(rows), ["q"], "cmd", "m{skill}",
                              runs, threshold, workers)
    return failures, buf.getvalue(), calls


def _rows():
    return [
        {"query": "yes one", "should_trigger": True},
        {"query": "no two", "should_trigger": False},
        {"query": "yes three", "should_trigger": True},
        {"query": "no four", "should_trigger": False},
    ]


def main():
    rows = _rows()

    # 1. Order + rates: parallel output must match serial byte-for-byte.
    f1, out1, c1 = _run(1, rows)
    f4, out4, c4 = _run(4, rows)
    assert out1 == out4, f"parallel output diverged:\n{out1}\n---\n{out4}"
    assert f1 == f4 == 0, f"expected 0 failures, got {f1}/{f4}"

    # 2. Every row queried exactly once per run, with a sane result.
    assert len(c1) == len(rows) and len(c4) == len(rows), "row not queried once"

    # 3. Rate correctness: each per-query line passes (RATE lines are summary).
    for line in out4.splitlines():
        if line.startswith("RATE"):  # summary line, not a per-query result
            continue
        assert line.startswith("PASS"), f"expected PASS, got: {line}"

    # 4. runs>1: a query that always triggers still passes at any run count;
    # a worker-shared state bug would skew the tally, not the stub.
    f1, out1, _ = _run(1, rows, runs=3)
    f4, out4, _ = _run(4, rows, runs=3)
    assert out1 == out4, "runs>1 parallel output diverged"
    assert f1 == f4 == 0

    # 5. A real miss is caught, not masked: flip a label to a failing side.
    bad = _rows()
    bad[0]["should_trigger"] = False  # "yes one" now wants to skip, but triggers
    f4, out4, _ = _run(4, bad)
    assert f4 == 1, f"expected 1 failure on a genuine miss, got {f4}"
    assert "FAIL" in out4, "failure line not printed"

    print("OK: parallel measure() matches serial on order, rates, failures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
