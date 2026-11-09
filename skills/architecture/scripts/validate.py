#!/usr/bin/env python3
"""Deterministic gate for system-diagramming artifacts (stdlib only).

Usage:
    python3 validate.py diagram.html [diagram2.html ...]

Accepts delivered HTML (extracts the ir JSON block) or a raw .json IR file.
Prints E_* defect lines (any one fails the run) and W_* advisory lines;
exit 0 only when no E_* remains.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

KINDS = {"architecture", "workflow", "sequence", "dataflow", "lifecycle"}
ROLES = {"frontend", "backend", "database", "cloud", "security",
         "messagebus", "external", "state", "participant"}
STYLES = {"solid", "dashed", "emphasis"}
ORIENTS = {None, "h", "v"}
IR_RE = re.compile(r'<script id="ir" type="application/json">(.*?)</script>', re.S)


def check(ir: dict, msgs: list) -> None:
    def err(code, subject, hint):
        msgs.append(f"E_{code}: {subject} -- {hint}")

    def warn(code, subject, hint):
        msgs.append(f"W_{code}: {subject} -- {hint}")

    if ir.get("ir_version") != 1:
        err("VERSION", "ir_version", "must be 1")
    if ir.get("kind") not in KINDS:
        err("KIND", ir.get("kind"), f"one of {sorted(KINDS)}")
    if not str(ir.get("title") or "").strip():
        err("TITLE", "title", "non-empty title required")
    canvas = ir.get("canvas") or {}
    w, h = canvas.get("width", 0), canvas.get("height", 0)
    if not isinstance(w, (int, float)) or not isinstance(h, (int, float)) \
            or w < 400 or h < 300:
        err("CANVAS", "canvas", "numeric width >= 400 and height >= 300 required")

    nodes = ir.get("nodes") or []
    if not nodes:
        err("NODES", "nodes", "at least one node required")
        return
    seen: dict = {}
    boxes: list = []
    for n in nodes:
        nid = n.get("id")
        if not nid or not isinstance(nid, str):
            err("ID", n, "every node needs a non-empty string id")
            continue
        if nid in seen:
            err("DUP_ID", nid, "duplicate node id")
            continue
        seen[nid] = n
        if not str(n.get("label") or "").strip():
            err("NO_LABEL", nid, "every node needs a label")
        if n.get("role") not in ROLES:
            err("ROLE", nid, f"role is one of {sorted(ROLES)}")
        try:
            x, y = float(n["x"]), float(n["y"])
            nw, nh = float(n["w"]), float(n["h"])
        except (KeyError, TypeError, ValueError):
            err("GEOM", nid, "x, y, w, h are required numbers")
            continue
        if nw < 40 or nh < 28:
            err("SIZE", nid, "w >= 40 and h >= 28")
        if x < 0 or y < 0 or x + nw > w or y + nh > h:
            err("BOUNDS", nid, f"box must sit inside the {w}x{h} canvas")
        boxes.append((nid, x, y, nw, nh))
    for i, (a, ax, ay, aw, ah) in enumerate(boxes):
        for b, bx, by, bw, bh in boxes[i + 1:]:
            if ax < bx + bw - 2 and bx < ax + aw - 2 \
                    and ay < by + bh - 2 and by < ay + ah - 2:
                err("OVERLAP", f"{a} x {b}", "boxes overlap; keep a clear gap")

    eseen: set = set()
    for e in ir.get("edges") or []:
        eid = e.get("id")
        if not eid or not isinstance(eid, str):
            err("ID", e, "every edge needs a non-empty string id")
            continue
        if eid in eseen:
            err("DUP_ID", eid, "duplicate edge id")
            continue
        eseen.add(eid)
        for end in ("from", "to"):
            if e.get(end) not in seen:
                err("BAD_REF", eid, f"{end} {e.get(end)!r} is not a node id")
        if e.get("from") == e.get("to"):
            warn("SELF", eid, "self-loop edge")
        if e.get("style", "solid") not in STYLES:
            err("STYLE", eid, f"style is one of {sorted(STYLES)}")
        if e.get("orient") not in ORIENTS:
            err("ORIENT", eid, 'orient is "h" or "v"')
        for p in e.get("points") or []:
            if (not isinstance(p, (list, tuple)) or len(p) != 2
                    or not all(isinstance(v, (int, float)) for v in p)):
                err("POINTS", eid, "points are [x, y] number pairs")
                break
            if not (0 <= p[0] <= w and 0 <= p[1] <= h):
                err("BOUNDS", eid, f"point {p} sits outside the canvas")
                break
        if not str(e.get("label") or "").strip():
            warn("NO_LABEL", eid,
                 "relationship labels are semantic data; label it or justify")

    for g in ir.get("groups") or []:
        wraps = g.get("wraps") or []
        if len(wraps) < 2:
            err("GROUP", g.get("label"), "groups wrap at least 2 nodes")
        for nid in wraps:
            if nid not in seen:
                err("BAD_REF", g.get("label"), f"wraps unknown node {nid!r}")
    for c in ir.get("cards") or []:
        if not str(c.get("title") or "").strip() or not c.get("items"):
            warn("CARD", c.get("title"), "cards need a title and items")

    if boxes and w and h:
        xs = [b[1] for b in boxes] + [b[1] + b[3] for b in boxes]
        ys = [b[2] for b in boxes] + [b[2] + b[4] for b in boxes]
        for e in ir.get("edges") or []:
            for p in e.get("points") or []:
                xs.append(p[0])
                ys.append(p[1])
        if (max(xs) - min(xs)) < 0.55 * w or (max(ys) - min(ys)) < 0.55 * h:
            warn("CANVAS", "canvas",
                 "content leaves a dead band; tighten the canvas to hug the diagram")


def load(path: Path):
    text = path.read_text(encoding="utf-8")
    raw = text
    if path.suffix != ".json":
        m = IR_RE.search(text)
        if not m:
            return None, 'no ir JSON block (<script id="ir" type="application/json">)'
        raw = m.group(1)
    try:
        return json.loads(raw), None
    except ValueError as exc:
        return None, f"IR is not valid JSON: {exc}"


def main(argv: list) -> int:
    if not argv:
        print("usage: validate.py <diagram.html|ir.json> [...]", file=sys.stderr)
        return 2
    bad = False
    for arg in argv:
        path = Path(arg)
        ir, problem = load(path)
        msgs: list = []
        if problem:
            msgs.append(f"E_IR: {arg} -- {problem}")
            ir = None
        else:
            check(ir, msgs)
        for m in msgs:
            print(f"{path.name}: {m}")
        errors = [m for m in msgs if m.startswith("E_")]
        print(f"{path.name}: {len(errors)} error(s), "
              f"{len(msgs) - len(errors)} warning(s), "
              f"{len((ir or {}).get('nodes') or [])} node(s)")
        bad = bad or bool(errors)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
