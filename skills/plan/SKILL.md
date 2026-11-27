---
name: plan
description: Use when a task needs a plan before any change — scope is ambiguous, actions are irreversible or outward-facing, or the user asked for a plan. Interviews the user, writes the plan artifact, and holds the stop-for-approval gate.
---

# Plan First

Use this before any change when scope is ambiguous, an action is irreversible or outward-facing, or a plan was requested. The output is one plan artifact and a stop for approval, never code yet.

## 1. Interview first

- Ask one question at a time, each carrying your recommended answer, until you could write the spec without guessing.
- Prefer a choice between concrete options over an open question, because a menu is easier to answer than a blank page.
- Skip questions the repo already answers: read the code, the manifests, and the history first.
- Stop interviewing when more answers cannot change the plan.

## 2. Write the plan artifact

- Goal, with completion criteria.
- Context: the files and systems the work touches.
- Constraints: what must not change, plus the limits on scope and environment.
- Done-when: each item named with the check that confirms it.
- Exactly one recommendation, not a menu of approaches.
- For parallel work, the units, each unit's owned files, and each unit's done check.

## 3. Validate the plan

- Every done-when item names a check that can come back pass or fail; an item no check can confirm goes back to the user as a question.
- Every irreversible or outward step is marked for explicit authorization before it runs.
- A step whose source cannot be located is either researched or asked about, never inferred.

## 4. Stop for approval

- Approval is the user's words; a clean tree or a green build authorizes nothing.
- After approval, implement in a fresh context from the plan, not from the conversation that wrote it.

## 5. After implementation

- Review the diff against this plan: every requirement implemented, every listed edge case checked.
- Report only gaps that affect correctness; a plan review is not a style hunt.

## 6. Gotchas

- A plan that only restates the ask adds nothing; it must resolve what the ask left implicit.
- A done-when item with no check cannot be verified and does not belong in the plan.
- Asking questions the repo already answers wastes the scarcest input to the loop.