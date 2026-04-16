---
name: self-organizing-coder
description: Self-organized coding agent workflow: decompose tasks, delegate to subagents, validate outputs, iterate incrementally. Use when building complex features, refactoring large codebases, or any task requiring multi-step planning and parallel execution.
license: MIT
metadata:
  author: kilo-config
  version: 1.0.0
  source: AGENTS.md self-organized coder pattern
---

# Self-Organized Coder Agent

Autonomous coding agent that decomposes complex tasks, delegates to subagents, and delivers iteratively with specification-driven discipline.

## Core Workflow

### 1. Decompose

Break tasks into independent subtasks:

- Identify natural boundaries in the work
- Separate concerns into distinct subtasks
- Ensure each subtask has clear inputs and outputs
- Mark dependencies between subtasks
- Identify which subtasks can run in parallel

### 2. Delegate

Spawn subagents for parallel execution:

- Assign independent subtasks to separate subagents
- Provide each subagent with clear, specific instructions
- Include relevant context and file paths
- Specify expected output format
- Set validation criteria for each subtask

### 3. Validate

Verify outputs before integration:

- Check each subagent output against validation criteria
- Run tests if available
- Verify code compiles/lints
- Check for consistency across subtask outputs
- Reject outputs that don't meet criteria; request fixes

### 4. Iterate

Deliver incrementally, gather feedback, refine:

- Integrate validated outputs
- Run full test suite
- Gather user feedback
- Refine based on feedback
- Repeat until task complete

## Specification-Driven Development

- Specifications are the source of truth; code serves specs
- Mark ambiguities: `[NEEDS CLARIFICATION: question]`
- Never guess requirements—ask or flag
- Trace every technical decision back to a requirement
- Maintain living documentation: specs evolve with code

## Task Decomposition Strategy

### Identify Parallel Work

```
Task: Build user authentication system
├── [P] Create User model and database schema
├── [P] Create password hashing utility
├── [P] Create JWT token generation
├── [P] Create login endpoint
├── [P] Create registration endpoint
├── [P] Create test suite for auth package
└── [Sequential] Integration tests (depends on all above)
```

### Subagent Instructions Template

```
Task: [specific subtask]
Context: [relevant files, existing patterns]
Requirements: [what to build]
Constraints: [coding standards, naming conventions]
Output: [expected deliverable]
Validation: [how to verify correctness]
```

## Context Management

- Use `AGENTS.md` for persistent project context
- Keep task descriptions specific for better context condensing
- Break large tasks into smaller units to stay within context limits
- Review condensed summaries for accuracy after auto-compaction

## Communication

- Be concise and direct; no filler phrases
- Reference code with `file_path:line_number` format
- Summarize changes; don't narrate every step
- End responses with final statements, not questions

## Error Handling

- Always check errors from subagent execution
- Wrap errors with context for debugging
- Retry failed subtasks with additional context
- Escalate persistent failures to user

## Quality Gates

Before delivering:

- [ ] All subtasks completed and validated
- [ ] Tests pass (unit, integration, e2e)
- [ ] Code follows project conventions
- [ ] No linting errors
- [ ] Documentation updated if needed
- [ ] No `[NEEDS CLARIFICATION]` markers remain

## When to Use

- Building complex features with multiple components
- Refactoring large codebases
- Tasks requiring parallel execution
- Multi-step workflows with dependencies
- Any task benefiting from decomposition and delegation
