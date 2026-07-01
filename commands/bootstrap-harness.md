---
description: Bootstrap the minimal harness pack into a target project — scaffold the system-of-record so a coding agent can resume work across sessions without re-deriving setup, status, or scope
---

# Bootstrap Harness

Scaffold the minimal harness pack into the target project. After this command, any coding agent that opens the project can clock in, see the verified state, pick the highest-priority feature, and leave a clean restart path — without re-deriving setup, status, or scope.

Target project (from arguments, optional): **$ARGUMENTS**. If empty, use the current working directory. Never write into the global `~/.agents` repo itself.

See [harness-engineering](../skills/harness-engineering/SKILL.md) for the canon this pack implements. Failure-mode → control mapping lives in §14 (Failure-Mode → Control Map) — read it when an observed failure needs a control, not a prompt edit.

## Non-Negotiable Rules

1. **WIP = 1** — at most ONE feature in `.agents/feature_list.json` may carry `"status": "in_progress"` at any time.
2. **Executable completion evidence** — `"status": "passing"` requires recorded evidence (command + exit code + observed output). "Looks fine" is not evidence.

## Fixed Startup Flow (wire into `AGENTS.md`)

Wire these steps, in order, into the target project's `AGENTS.md` (create the file if absent; if present, append a `## Harness Startup Flow` section — never clobber existing content):

1. Run `pwd` and confirm the repository root.
2. Read `.agents/progress.md`.
3. Read `.agents/feature_list.json`.
4. Review recent commits: `git log --oneline -5`.
5. Run `./init.sh`.
6. Run a baseline smoke or end-to-end path.
7. If the baseline is broken, fix that FIRST before any new work.
8. Select the highest-priority unfinished feature.
9. Work only on that feature until verified or explicitly blocked.

End-of-session mirror: update `.agents/progress.md`, reflect actual state in `.agents/feature_list.json`, write a handoff if needed, commit safe work, leave a clean restart path. See `.agents/clean-state-checklist.md`.

## Scaffold

Create the project-local state directory `.agents/` if absent. This is the project's system of record, separate from the global config repo. Then write the six artifacts below with the skeletons shown. Adapt placeholders to the project's real commands/paths when discoverable; if unknown, keep the placeholder and surface it in the summary so the user fills it.

### 1. `.agents/feature_list.json`

Machine-readable feature tracker. Exactly ONE feature may be `"in_progress"` at any time.

```json
{
  "project": "<project-name>",
  "last_updated": "YYYY-MM-DD",
  "rules": {
    "single_active_feature": true,
    "passing_requires_evidence": true,
    "do_not_skip_verification": true
  },
  "status_legend": {
    "not_started": "Work has not begun.",
    "in_progress": "The feature is the current active task.",
    "blocked": "Work cannot continue until a documented blocker is resolved.",
    "passing": "Required verification has passed and evidence is recorded."
  },
  "features": [
    {
      "id": "<area>-001",
      "priority": 1,
      "area": "<area>",
      "title": "<short description>",
      "user_visible_behavior": "<what the user sees when it works>",
      "status": "not_started",
      "verification": ["<step-by-step instructions to confirm it works>"],
      "evidence": [],
      "notes": ""
    }
  ]
}
```

### 2. `.agents/progress.md`

The single source of truth across sessions. Two sections, kept current.

**Current Verified State**
- Repository root directory
- Standard startup path
- Standard verification path
- Highest priority unfinished feature
- Current blocker

**Session Record** (one entry per session)
- Goal
- Completed
- Verification run
- Evidence recorded
- Commits
- Known risks
- Next best action

### 3. `init.sh` (project ROOT, not `.agents/`)

Startup script. Three editable vars at the top: `INSTALL_CMD`, `VERIFY_CMD`, `START_CMD`. Prints `pwd`, runs install, runs verify, and prints (or runs if `RUN_START_COMMAND=1`) the start command. If verify fails, stop and fix the baseline before any new work. Make it executable.

```bash
#!/usr/bin/env bash
set -euo pipefail

# Edit these three to match the project.
INSTALL_CMD="${INSTALL_CMD:-echo 'no install command set'}"
VERIFY_CMD="${VERIFY_CMD:-echo 'no verify command set'}"
START_CMD="${START_CMD:-echo 'no start command set'}"

echo "==> pwd: $(pwd)"

echo "==> install"
bash -c "$INSTALL_CMD"

echo "==> verify"
if ! bash -c "$VERIFY_CMD"; then
  echo "[BLOCKED] baseline verify failed — fix the baseline before new work." >&2
  exit 1
fi

echo "==> start"
if [ "${RUN_START_COMMAND:-0}" = "1" ]; then
  bash -c "$START_CMD"
else
  echo "skipping start (set RUN_START_COMMAND=1 to run): $START_CMD"
fi
```

After writing, run `chmod +x init.sh`.

### 4. `.agents/session-handoff.md`

Compact cross-session handoff. Sections:

- Currently verified
- Changes this session
- Still broken or unverified
- Next best action (incl. what NOT to touch)
- Commands (startup / verify / debug)

### 5. `.agents/clean-state-checklist.md`

End-of-session checklist. Tick every item before closing the session:

- Standard startup still works.
- Standard verification still runs.
- Progress log updated.
- Feature list reflects actual state (no false `passing`).
- No half-finished work unrecorded.
- Next session can continue without manual fixes.

### 6. `.agents/evaluator-rubric.md`

Scorecard scoring agent output 0–2 across SIX dimensions:

1. Correctness
2. Verification
3. Scope discipline
4. Reliability
5. Maintainability
6. Handoff readiness

Conclusion per output: **Accept** / **Revise** / **Block**.

**Warning:** agents are poor self-judges — they identify issues, then talk themselves into approving. The author of the work must NOT be the sole judge. Run this rubric from an independent reviewer (different session, different agent, or human). Plan 3–5 tuning rounds of the rubric against human judgment before trusting its scores.

## Wiring `AGENTS.md`

If `AGENTS.md` is absent, create it with just the `## Harness Startup Flow` section (do not invent other content). If present, append the section under that exact heading. Do not modify anything above the appended section.

## Report

After scaffolding, print:

1. Files created/modified (exact paths).
2. The single next action: run `./init.sh` to confirm the baseline.
3. Any placeholder left un-adapted that the user must fill.

Do not declare done until the gate `./scripts/validate-agents.sh` (run from this global repo) still exits 0 and `./init.sh` in the target project exits 0.