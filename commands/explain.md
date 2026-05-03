---
description: Explain code, architecture, or concepts in the codebase
subtask: true
---

You are explaining code or concepts to help the user understand the codebase. Be clear, concise, and use concrete examples from the actual code.

## Target

$ARGUMENTS

## Context

!`git branch --show-current 2>/dev/null || echo "Not a git repo"`

## Approach

1. **Identify what to explain**: 
   - If `$ARGUMENTS` names a file, function, module, or concept — explain that.
   - If `$ARGUMENTS` is a question — search the codebase to find relevant code, then answer.

2. **Search and read**:
   - Use semantic search and grep to find the relevant code.
   - Read enough surrounding context to give an accurate explanation.
   - Trace call chains if explaining a flow or architecture.

3. **Explain**:
   - Start with a one-paragraph summary in plain language.
   - Then provide detail with code references (file:line format).
   - Include a diagram or flow description if explaining architecture or data flow.
   - Point out non-obvious decisions or edge cases.

## Rules

- Explain the actual code, not a generic description of what the technology does.
- Use file:line references. Don't paste large code blocks.
- If the answer requires reading multiple files, trace the full path.
- If you're unsure about something, say so rather than guessing.
- Keep it concise. The user can ask follow-up questions.
