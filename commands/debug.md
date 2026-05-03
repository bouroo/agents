---
description: Debug an issue — reproduce, diagnose, fix, verify
subtask: true
---

You are debugging an issue. Follow a systematic approach to identify the root cause and implement a fix.

## Issue Description

$ARGUMENTS

## Context

Recent changes that may be related:
!`git log --oneline -10 2>/dev/null || echo "Not a git repo"`

Current working tree:
!`git diff --stat HEAD 2>/dev/null || echo "Clean working tree or no git repo"`

## Steps

1. **Reproduce**: 
   - Identify the exact steps, inputs, or conditions that trigger the issue.
   - If the issue is described vaguely, ask clarifying questions or search the codebase for related error messages.
   - Write a minimal reproduction if one doesn't exist.

2. **Hypothesize**:
   - Based on the symptoms, form 2-3 hypotheses about the root cause.
   - Rank by likelihood. Start with the most probable.

3. **Investigate**:
   - Search the codebase for relevant code paths using semantic search and grep.
   - Read the code along the execution path from trigger to symptom.
   - Check logs, error messages, stack traces for clues.
   - Verify or eliminate each hypothesis.

4. **Fix**:
   - Implement the minimal fix that addresses the root cause.
   - Add a regression test that would have caught this bug.
   - Ensure the fix doesn't introduce new issues.

5. **Verify**:
   - Run the reproduction to confirm the fix works.
   - Run the full test suite to check for regressions.
   - Run lint and typecheck.

## Rules

- Fix the root cause, not the symptom.
- One fix at a time. Don't bundle unrelated changes.
- Always add a regression test.
- If the issue requires an environment-specific reproduction, document the steps clearly.
- If you can't reproduce it, document what you tried and what you found.
