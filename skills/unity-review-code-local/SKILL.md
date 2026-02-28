---
name: unity-review-code-local
description: "Deep logic review for Unity C# code in the local project. Reviews code changes with surgical focus on logic correctness, edge cases, state management, data flow, and concurrency — adds review comments into the code, then delegates code fixes to unity-code-quick in parallel background tasks. No summary document. No report. No GitHub interaction. No commit. No push. User reviews the diff. Input: commit hash, commit range, branch diff, or a feature/logic description to review. Use when: reviewing logic before commit, validating a feature implementation, auditing business logic, tracing data flow for correctness, reviewing a specific commit. Triggers: 'review code', 'review logic', 'check this logic', 'review commit', 'review my changes', 'logic review', 'code review', 'review this feature'."
---

# Unity Logic Reviewer (Local)

Deep logic review for local project. Add review comments into C# source files, then delegate code fixes to `unity-code-quick` via background tasks. No report, no summary, no GitHub, no commit.

## Shared References

Load shared review resources from `unity-shared`:
 [common-rules.md](../unity-shared/references/common-rules.md) — Shared review rules + input-to-command mapping + severity
 [review-engine.md](../unity-shared/references/review-engine.md) — Review logic references to load
 [common-rules.md](../unity-shared/references/common-rules.md) — Shared review rules

## Output

1. **Short inline comments** in C# source files — per [output-template.md](references/output-template.md).
2. **Code fixes** applied by `unity-code-quick` background tasks — one task per finding (🔴/🟡).
3. User reviews the combined diff (comments + fixes) before committing.

## Workflow

Load references, then follow the 5-step workflow: Fetch → Read → Investigate → Review → Comment+Delegate.
## Reference Files
- [output-template.md](references/output-template.md) — Comment format, severity tokens, delegation markers
- [output-template.md](references/output-template.md) — Comment format, severity tokens, delegation markers
- workflow.md — 5-step local code review workflow

## Rules (Local-Specific)

- **Review only** — insert `// ── REVIEW` comments using `edit`. Never apply code fixes directly.
- Comments are short, focused, highlight-style. No verbose explanations.
- Never commit. Never push. User reviews the diff.
