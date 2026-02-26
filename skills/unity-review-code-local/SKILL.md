---
name: unity-review-code-local
description: "Deep logic review for Unity C# code in the local project. Reviews code changes with surgical focus on logic correctness, edge cases, state management, data flow, and concurrency — adds review comments into the code, then delegates code fixes to unity-code-quick in parallel background tasks. No summary document. No report. No GitHub interaction. No commit. No push. User reviews the diff. Input: commit hash, commit range, branch diff, or a feature/logic description to review. Use when: reviewing logic before commit, validating a feature implementation, auditing business logic, tracing data flow for correctness, reviewing a specific commit. Triggers: 'review code', 'review logic', 'check this logic', 'review commit', 'review my changes', 'logic review', 'code review', 'review this feature'."
---

# Unity Logic Reviewer (Local)

Deep logic review for local project. Add review comments into C# source files, then delegate code fixes to `unity-code-quick` via background tasks. No report, no summary, no GitHub, no commit.

## Output

1. **Short inline comments** in C# source files — per [INLINE_COMMENT_FORMAT.md](references/INLINE_COMMENT_FORMAT.md).
2. **Code fixes** applied by `unity-code-quick` background tasks — one task per finding (🔴/🟡).
3. User reviews the combined diff (comments + fixes) before committing.

## Input → Diff Command

See [tool-usage.md](references/tool-usage.md) for input-to-diff command mapping.

## Severity

Four levels: 🔴 CRITICAL, 🟡 HIGH, 🔵 MEDIUM, 🟢 LOW. See [INLINE_COMMENT_FORMAT.md](references/INLINE_COMMENT_FORMAT.md).

## Workflow

Load references, then follow the 5-step workflow: Fetch → Read → Investigate → Review → Comment+Delegate.
Read [workflow.md](references/workflow.md) before starting any review.

## Reference Files
- [workflow.md](references/workflow.md) — Load references + 5-step review workflow
- [tool-usage.md](references/tool-usage.md) — Input-to-diff command mapping
- [INLINE_COMMENT_FORMAT.md](references/INLINE_COMMENT_FORMAT.md) — Comment format, severity tokens, delegation markers

## Rules

- **Review only** — insert `// ── REVIEW` comments using `edit`. Never apply code fixes directly.
- Delegate code fixes to `unity-code-quick` via background tasks. One task per fix or per file.
- Comments are short, focused, highlight-style. No verbose explanations.
- Never commit. Never push. User reviews the diff.
- Read full file. Trace data flow end-to-end. Verify lifecycle ordering.
- If project uses UniTask, `async UniTaskVoid` can be valid for Unity event entry points.
- For serialization findings, check whether the project has migration/versioning support.
- Never comment without evidence. Investigate first — see `VERIFICATION_GATES.md`.
