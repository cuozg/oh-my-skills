---
name: unity-code-deep
description: "Expert Unity Developer implementation. Write clean, commented, performant C# code following best practices. Use when: creating MonoBehaviours, ScriptableObjects, implementing gameplay features, refactoring for performance or architecture, using Unity 6 features."
---

# unity-code-deep — Expert Unity C# Implementation

Write clean, commented, performant C# code. Investigate before coding, ask when unclear, verify everything compiles. Follow `unity-shared` for all coding rules.

**Input**: Feature description, implementation task, or TDD/system doc reference
**Output**: C# scripts following project conventions, zero compile errors.

## Workflow

Follow the 4-phase workflow: Understand → Plan → Implement → Verify.

## Shared References

Load shared coding resources from `unity-shared`:

```python
read_skill_file("unity-shared", "references/template.md")
read_skill_file("unity-shared", "references/patterns-service.md")
read_skill_file("unity-shared", "references/patterns-async-state.md")
```

## Reference Files
- workflow.md — 4-phase implementation workflow