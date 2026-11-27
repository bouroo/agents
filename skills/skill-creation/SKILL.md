---
name: skill-creation
description: Use when creating a new skill or revising an existing one — when a repeated workflow is about to be captured, or after real runs expose what a skill missed.
---

# Author a Skill

A skill captures a repeated workflow so its procedure loads only when the trigger holds. Author it from real expertise and refine it with real runs, not from general model knowledge.

## 1. Start from real expertise

- Extract from a hands-on task: the steps that worked, the corrections made, the input and output formats, and the context provided.
- Or synthesize from project artifacts: runbooks, review comments, and version history.

## 2. Frontmatter contract

- `name` is lowercase with hyphens and short; `description` states what the skill does and when to use it, with trigger phrases a user would actually say.

## 3. Body budget

- Keep core instructions in the body, under 500 lines; move detail to `references/` files, each with an explicit load condition ("read X when Y"), never a bare "see references/".

## 4. Write for the agent

- Per line, ask: would the agent get this wrong without it? If no, cut it.

## 5. One coherent unit

- Too narrow forces several skills to load, with overhead and conflicting instructions; too broad will not trigger precisely.

## 6. Calibrate prescriptiveness

- Give freedom where variation is fine and explain why; give exact steps where fragility matters; prefer defaults over menus, and procedures over declarations.

## 7. Include what the agent lacks

- Gotchas for environment facts that defy reasonable assumptions, with corrections recorded here.
- Output templates for concrete structures, and checklists for ordered multi-step work.

## 8. Refine with real execution

- Run the skill on real tasks, read execution traces not just outputs, and feed all results back; a rule that never fires gets cut.

## 9. In this setup

- Skills live at `skills/<name>/SKILL.md`; keep the set small, because a repeated workflow earns a skill and a one-off stays a prompt.
