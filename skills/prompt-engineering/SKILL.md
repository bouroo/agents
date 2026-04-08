---
name: prompt-engineering
description: Effective AI prompting for code generation, few-shot examples, and task decomposition. Use when the user mentions prompting, prompt engineering, or when asking for help with AI-assisted development.
---

# Prompt Engineering for Code Generation

Clear, specific prompts produce better code than vague, open-ended ones.

## Prompt Structure (for Subagent Delegation)

Every delegation prompt should include four sections:

1. **Task** — What to do (concrete, measurable outcome)
2. **Context** — Relevant files, conventions, constraints from prior work
3. **Scope** — Boundaries: what to touch, what NOT to touch
4. **Return format** — Exactly what information to include in the final message

## Effective Patterns

- **Specify output format explicitly** — e.g., "return a JSON object with keys: name, path, status"
- **State constraints upfront** — e.g., "do not use external dependencies", "must work in Python 3.9+"
- **Provide few-shot examples** for complex transformations or formatting tasks
- **Decompose complex tasks** into sequential steps with clear handoff points

## Task Decomposition

Split work into subtasks using these strategies:

- **By file boundaries** — when subtasks touch different files
- **By responsibility** — when subtasks serve different purposes (research vs. implementation)
- **By dependency** — independent tasks run in parallel; dependent tasks run sequentially
- Each subtask must have concrete **acceptance criteria**

## Anti-patterns

- "Improve the code" — specify what "improve" means (performance? readability? error handling?)
- Asking for multiple unrelated things in one prompt
- Omitting critical context (file paths, existing patterns, test frameworks)
- Asking the agent to "figure out" what you want — be explicit

## Code Generation Tips

- Specify the **function signature** before asking for implementation
- Include **test cases** that the implementation must satisfy
- State **naming conventions** and style preferences
- Provide the **interface/contract** before the implementation

## Review Prompts

- Target specific aspects: "review for security issues", "check error handling", "look for performance problems"
- Provide criteria: "flag anything that violates our naming convention"
- Specify severity: "critical issues only" vs "all suggestions"

## Checklist Before Delegating

- [ ] Is the desired outcome measurable?
- [ ] Are file paths and dependencies specified?
- [ ] Are constraints and boundaries explicit?
- [ ] Is the return format defined?
- [ ] Would a few-shot example clarify the task?
