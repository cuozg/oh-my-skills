---
name: unity-review-code-local
description: "Deep logic review for Unity C# code in the local project. Reviews code changes with surgical focus on logic correctness, edge cases, state management, data flow, and concurrency — adds review comments into the code, then delegates code fixes to unity-code-quick in parallel background tasks. No summary document. No report. No GitHub interaction. No commit. No push. User reviews the diff. Input: commit hash, commit range, branch diff, or a feature/logic description to review. Use when: reviewing logic before commit, validating a feature implementation, auditing business logic, tracing data flow for correctness, reviewing a specific commit. Triggers: 'review code', 'review logic', 'check this logic', 'review commit', 'review my changes', 'logic review', 'code review', 'review this feature'."
---

# Unity Logic Reviewer (Local)

Deep logic review for local project. Add review comments into C# source files, then delegate code fixes to `unity-code-quick` via background tasks. No report, no summary, no GitHub, no commit.

## Shared References

Load shared review resources from `unity-shared`:

```python
read_skill_file("unity-shared", "references/review/common-rules.md")
read_skill_file("unity-shared", "references/review/review-deep-workflow.md")
read_skill_file("unity-shared", "references/review/review-gates.md")
read_skill_file("unity-shared", "references/review/review-logic-data.md")
read_skill_file("unity-shared", "references/review/review-csharp.md")
read_skill_file("unity-shared", "references/quality/quality-performance-checklist.md")
read_skill_file("unity-shared", "references/quality/quality-unity-best-practices.md")
read_skill_file("unity-shared", "references/review/review-architecture-patterns.md")
```
## Output

1. **Short inline comments** in C# source files — per [output-template.md](references/output-template.md).
2. **Code fixes** delegated to `unity-code-quick` background tasks — one task per 🔴/🟡 finding. Reviewer never applies fixes directly.
3. User reviews the combined diff (comments + fixes) before committing.

## Workflow

Load references, then follow the 5-step workflow: Fetch → Read → Investigate → Review → Comment+Delegate.

## Reference Files
- [output-template.md](references/output-template.md) — Comment format, severity tokens, delegation markers
- [workflow.md](references/workflow.md) — 5-step local code review workflow

## Rules (Local-Specific)

- **Review only** — insert `// ── REVIEW` comments using `edit`. Never apply code fixes directly.
- Comments are short, focused, highlight-style. No verbose explanations.
- Never commit. Never push. User reviews the diff.
