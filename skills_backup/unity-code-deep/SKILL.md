---
name: unity-code-deep
description: "Complex, multi-file Unity C# implementation. Loads ALL unity-shared references, follows code standards and TDD strictly. Investigates before coding, verifies references to preserve existing logic, reviews carefully, runs tests after writing. Use when: (1) Multi-system feature requiring cross-file changes, (2) Refactoring for performance or architecture, (3) Implementing from a TDD or system document, (4) Tasks requiring verification and testing before delivery. Triggers: 'implement feature', 'complex code', 'refactor system', 'implement TDD', 'deep code'."
---

# unity-code-deep — Expert Unity C# Implementation

Write clean, commented, performant C# code. Investigate before coding, ask when unclear, verify everything compiles.

**Input**: Feature description, implementation task, or TDD/system doc reference
**Output**: C# scripts following project conventions, zero compile errors.

## Workflow

Follow the 4-phase workflow: Understand → Plan → Implement → Verify.

## Shared References

Load **ALL** shared coding references from `unity-shared` before writing any code. This is mandatory — no exceptions.

```python
read_skill_file("unity-shared", "references/code/coding-standards.md")
read_skill_file("unity-shared", "references/code/csharp-hygiene.md")
read_skill_file("unity-shared", "references/code/csharp-modern.md")
read_skill_file("unity-shared", "references/code/csharp-linq.md")
read_skill_file("unity-shared", "references/code/csharp-perf.md")
read_skill_file("unity-shared", "references/code/unity-lifecycle.md")
read_skill_file("unity-shared", "references/code/unitask.md")
read_skill_file("unity-shared", "references/code/template.md")
read_skill_file("unity-shared", "references/code/patterns-service.md")
read_skill_file("unity-shared", "references/code/patterns-async-state.md")
read_skill_file("unity-shared", "references/code/editor-patterns.md")
read_skill_file("unity-shared", "references/code/security.md")
read_skill_file("unity-shared", "references/code/architecture.md")
```

## Reference Files
- workflow.md — 4-phase implementation workflow