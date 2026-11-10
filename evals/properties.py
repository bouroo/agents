#!/usr/bin/env python3
"""Measure the nine system-level properties of a run from its trace.

The doctrine claims nine properties of a multi-agent structure -- goal
formation, semantic consistency, parallel execution efficiency, heterogeneous
capability allocation, collective decision quality, state consistency, failure
recovery, transfer across tasks, and runtime overhead -- and says a claim with
no measurement is a narrative. This is that measurement: it reads a run trace
and reports one score and one verdict per property.

    python3 evals/properties.py --trace evals/fixtures/organized-run.json
    python3 evals/properties.py --trace evals/fixtures/organized-run.json --json
    python3 evals/properties.py --trace evals/fixtures/degraded-run.json \
        --property failure-recovery

Exit 0 when every measured property meets its threshold, exit 1 otherwise, so
the same command is usable as an eval check in both directions.

The trace format is the instrument's contract; a producer that cannot emit it
cannot be measured, which is the point -- see the trace schema below and
`evals/fixtures/` for two traces that disagree on every property.

Trace schema
------------
    {
      "goal": {
        "objective": str,
        "criteria": [str],              # acceptance criteria that close the goal
        "terminal_conditions": [str]   # states from which continuing is unjustified
      },
      "participants": [
        {"id": str,
         "capabilities": [str],        # what this participant can do
         "terms": {term: definition}}  # the words this participant uses
      ],
      "tasks": [
        {"id": str,
         "worker": str,                # participant id
         "requires_capability": str | null,
         "status": "done" | "failed" | "open",
         "closure": str | null,        # criterion this task closed
         "attempts": int,
         "resumed_after_failure": bool}
      ],
      "events": [
        {"type": "action" | "decision" | "coordination",
         "worker": str,
         "task": str | null,
         "start": number,              # milliseconds on a shared clock
         "end": number,
         "tokens": int}
      ],
      "decisions": [
        {"task": str,
         "parts": [{"worker": str, "score": number}],
         "merged_score": number}
      ],
      "snapshots": [
        {"task": str, "status": str, "closure": str | null}
      ],
      "next_run": {
        "tasks": [{"id": str, "reused_structure_from": str | null}]
      }
    }

Stdlib only, no model call, no network.
"""

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Each property: how to compute a score in [0, 1], and the score at or above
# which the property holds. A threshold is a decision, not a measurement, so
# each one is stated here where a reader can argue with it.
THRESHOLDS = {
    "goal-formation": 0.75,
    "semantic-consistency": 0.99,
    "parallel-execution-efficiency": 0.60,
    "heterogeneous-capability-allocation": 0.99,
    "collective-decision-quality": 0.01,
    "state-consistency": 0.99,
    "failure-recovery": 0.99,
    "transfer-across-tasks": 0.50,
    "runtime-overhead": 0.35,
}

PROPERTY_ORDER = list(THRESHOLDS)


def _load(path: pathlib.Path) -> dict:
    return json.loads(path.read_text())


def _ratio(hits: int, total: int) -> float:
    """Score for a countable property; an empty population scores 0.

    An empty population is not a pass. A structure with no failures has
    nothing to recover, and a team with no decisions has nothing to merge;
    scoring those 1.0 would let a run earn a property by not having the
    situation that exercises it.
    """
    if total <= 0:
        return 0.0
    return hits / total


def goal_formation(trace: dict) -> tuple[float, str]:
    """Are the objective's criteria satisfiable, and are the stop states declared?

    A criterion is satisfiable when some task closes it and a terminal
    condition exists, so the run knows what would end it.
    """
    goal = trace.get("goal", {})
    criteria = goal.get("criteria", [])
    terminal = goal.get("terminal_conditions", [])
    closed = {t.get("closure") for t in trace.get("tasks", []) if t.get("closure")}
    satisfiable = sum(1 for c in criteria if c in closed)
    score = 0.5 * _ratio(satisfiable, len(criteria)) + 0.5 * (1.0 if terminal else 0.0)
    return score, (f"{satisfiable}/{len(criteria)} criteria closed, "
                   f"{len(terminal)} terminal condition(s) declared")


def semantic_consistency(trace: dict) -> tuple[float, str]:
    """Does one term mean one thing across the participants?

    A term two participants define differently is a disagreement recorded as
    an agreement; each term with more than one distinct definition counts once.
    """
    participants = trace.get("participants", [])
    terms: dict[str, set] = {}
    for p in participants:
        for term, definition in (p.get("terms") or {}).items():
            terms.setdefault(term, set()).add(definition)
    if not terms:
        return 0.0, "no terms declared"
    conflicts = sum(1 for defs in terms.values() if len(defs) > 1)
    score = 1.0 - (conflicts / len(terms))
    return score, f"{conflicts}/{len(terms)} term(s) defined inconsistently"


def parallel_execution_efficiency(trace: dict) -> tuple[float, str]:
    """Did concurrency pay, net of coordination?

    Score is the observed speedup over perfectly serial execution: the work
    divided by the makespan, normalized by the number of workers that could
    have run at once. 1.0 means every worker was busy for the whole span.
    """
    events = [e for e in trace.get("events", []) if e.get("type") == "action"]
    if not events:
        return 0.0, "no actions recorded"
    workers = {e.get("worker") for e in events}
    if len(workers) < 2:
        return 0.0, f"only {len(workers)} worker(s): nothing ran concurrently"
    start = min(e["start"] for e in events)
    end = max(e["end"] for e in events)
    makespan = max(1, end - start)
    work = sum(max(0, e["end"] - e["start"]) for e in events)
    score = min(1.0, work / (makespan * len(workers)))
    return score, (f"work {work}ms over {makespan}ms span "
                   f"across {len(workers)} workers")


def heterogeneous_capability_allocation(trace: dict) -> tuple[float, str]:
    """Is each unit held by a participant that holds the capability it needs?

    A task with no required capability is unscored: nothing was required, so
    nothing could be mismatched.
    """
    capabilities = {p.get("id"): set(p.get("capabilities") or [])
                    for p in trace.get("participants", [])}
    scored = [t for t in trace.get("tasks", []) if t.get("requires_capability")]
    if not scored:
        return 0.0, "no task states a required capability"
    matched = sum(1 for t in scored
                  if t.get("requires_capability") in capabilities.get(t.get("worker"), set()))
    return _ratio(matched, len(scored)), f"{matched}/{len(scored)} task(s) held by a capable worker"


def collective_decision_quality(trace: dict) -> tuple[float, str]:
    """Is the merged decision better than its parts?

    Score is the mean gain of the merge over the mean of the contributing
    parts. A negative gain means the merge destroyed the input.
    """
    decisions = trace.get("decisions", [])
    if not decisions:
        return 0.0, "no decisions merged"
    gains = []
    for d in decisions:
        parts = [p.get("score", 0.0) for p in d.get("parts", [])]
        if not parts:
            continue
        gains.append(d.get("merged_score", 0.0) - (sum(parts) / len(parts)))
    if not gains:
        return 0.0, "no decision carried parts to merge"
    score = sum(gains) / len(gains)
    return score, f"{len(gains)} decision(s), mean gain {score:+.3f}"


def state_consistency(trace: dict) -> tuple[float, str]:
    """Does the recorded state agree with what the tasks say happened?

    Every task needs a snapshot, and the snapshot must agree with the task's
    status and closure. A missing snapshot is a disagreement, not a blank.
    """
    tasks = trace.get("tasks", [])
    if not tasks:
        return 0.0, "no tasks recorded"
    snapshots = {s.get("task"): s for s in trace.get("snapshots", [])}
    agree = 0
    for t in tasks:
        snap = snapshots.get(t.get("id"))
        if snap and snap.get("status") == t.get("status") and \
                snap.get("closure") == t.get("closure"):
            agree += 1
    return _ratio(agree, len(tasks)), f"{agree}/{len(tasks)} snapshot(s) agree with the task record"


def failure_recovery(trace: dict) -> tuple[float, str]:
    """Does a fault resume rather than restart?

    Scored only over the tasks that actually failed, and only when a failure
    occurred: a run with no failure has nothing to recover.
    """
    failed = [t for t in trace.get("tasks", []) if t.get("status") == "failed"]
    if not failed:
        return 0.0, "no failure occurred: nothing was exercised"
    resumed = sum(1 for t in failed if t.get("resumed_after_failure"))
    return _ratio(resumed, len(failed)), f"{resumed}/{len(failed)} failure(s) resumed rather than restarted"


def transfer_across_tasks(trace: dict) -> tuple[float, str]:
    """Does the next job start from the improved structure?

    Scored over the next run's tasks: a task that reused a structure scores,
    one that started cold does not.
    """
    tasks = trace.get("next_run", {}).get("tasks", [])
    if not tasks:
        return 0.0, "no next run recorded"
    reused = sum(1 for t in tasks if t.get("reused_structure_from"))
    return _ratio(reused, len(tasks)), f"{reused}/{len(tasks)} next-run task(s) reused a structure"


def runtime_overhead(trace: dict) -> tuple[float, str]:
    """What does the structure itself cost?

    Score is the share of tokens spent on coordination rather than on the
    work. The property holds when that share stays under the threshold, so
    the score is reported as 1.0 minus the share.
    """
    events = trace.get("events", [])
    if not events:
        return 0.0, "no events recorded"
    total = sum(e.get("tokens", 0) for e in events)
    if total <= 0:
        return 0.0, "no tokens recorded"
    coordination = sum(e.get("tokens", 0) for e in events
                       if e.get("type") in ("decision", "coordination"))
    share = coordination / total
    return max(0.0, 1.0 - share), f"{share:.1%} of tokens spent on coordination"


MEASURERS = {
    "goal-formation": goal_formation,
    "semantic-consistency": semantic_consistency,
    "parallel-execution-efficiency": parallel_execution_efficiency,
    "heterogeneous-capability-allocation": heterogeneous_capability_allocation,
    "collective-decision-quality": collective_decision_quality,
    "state-consistency": state_consistency,
    "failure-recovery": failure_recovery,
    "transfer-across-tasks": transfer_across_tasks,
    "runtime-overhead": runtime_overhead,
}


def measure(trace: dict) -> dict:
    """Measure every property; return a report keyed by property name."""
    report = {}
    for name in PROPERTY_ORDER:
        score, detail = MEASURERS[name](trace)
        threshold = THRESHOLDS[name]
        report[name] = {
            "score": round(score, 4),
            "threshold": threshold,
            "verdict": "PASS" if score >= threshold else "FAIL",
            "detail": detail,
        }
    return report


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--trace", required=True, help="path to a run trace JSON file")
    ap.add_argument("--property", choices=PROPERTY_ORDER,
                    help="report one property instead of all nine")
    ap.add_argument("--json", action="store_true", help="emit the report as JSON")
    args = ap.parse_args(argv)

    path = pathlib.Path(args.trace)
    if not path.is_file():
        print(f"trace not found: {path}", file=sys.stderr)
        return 2
    report = measure(_load(path))

    if args.property:
        report = {args.property: report[args.property]}

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for name, r in report.items():
            print(f"[{r['verdict']}] {name}: {r['score']:.4f} "
                  f"(threshold {r['threshold']}) -- {r['detail']}")

    return 0 if all(r["verdict"] == "PASS" for r in report.values()) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
