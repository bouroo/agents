---
name: alignment
description: Lock intent before you write code. Make what we will do and won't do explicit, and agree on standards and constraints up front.
version: 1.0.0
triggers:
  - locking intent before coding
  - scoping features
  - resolving ambiguity in requirements
  - starting a new iteration or story
---

# Alignment

Lock intent before implementation. Make scope, standards, and constraints explicit.

## When to Use

- Starting a new feature or story
- Requirements are ambiguous or incomplete
- Before committing to an implementation approach
- When team members have different understandings

## Steps

1. **Capture Requirements**: Write what the system should do in business language.
2. **Define Scope In**: List exactly what is included — features, endpoints, behaviors.
3. **Define Scope Out**: List explicitly what is NOT included. This prevents scope creep.
4. **Set Acceptance Criteria**: Given/When/Then format with concrete examples.
5. **Identify Constraints**: Non-functional requirements, performance limits, security rules.
6. **Confirm Alignment**: Review with stakeholders. No implementation until intent is locked.

## Rules

- Never implement without explicit scope in/out.
- Acceptance criteria must be testable with concrete values.
- Ambiguity is resolved before code, not during.
- When reality diverges, fix the spec first — then the code.

## Checklist

- [ ] Scope In defined
- [ ] Scope Out defined
- [ ] Acceptance criteria written (Given/When/Then)
- [ ] Constraints identified
- [ ] Edge cases listed
- [ ] Intent locked and reviewed
