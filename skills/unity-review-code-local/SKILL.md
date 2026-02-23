---
name: unity-review-code-local
description: "Deep logic review for Unity C# code in the local project. Reviews code changes with surgical focus on logic correctness, edge cases, state management, data flow, and concurrency — then adds review comments directly into the code as inline comments. No report document. No GitHub interaction. Input: commit hash, commit range, branch diff, or a feature/logic description to review. Use when: reviewing logic before commit, validating a feature implementation, auditing business logic, tracing data flow for correctness, reviewing a specific commit. Triggers: 'review code', 'review logic', 'check this logic', 'review commit', 'review my changes', 'logic review', 'code review', 'review this feature'."
---

# Unity Logic Reviewer (Local)

Deep logic review for the local project. Insert review comments directly into C# source files — no report, no GitHub.

## Output

Inline review comments in C# source files. No report document.

## Input → Diff Command

| Input | Command |
|:------|:--------|
| None (default) | `git diff` + `git diff --cached` |
| Commit SHA | `git show <hash>` |
| Commit range | `git diff <base>..<head>` |
| Branch | `git diff <branch>...HEAD` |
| Feature/logic request | Find relevant files via grep/LSP |

## Severity
Three levels: 🔴 Critical, 🟡 Major, 🔵 Minor. See [INLINE_COMMENT_FORMAT.md](references/INLINE_COMMENT_FORMAT.md) for definitions and usage.

## Load References

Always load:
- [INLINE_COMMENT_FORMAT.md](references/INLINE_COMMENT_FORMAT.md) — comment templates, tree format, placement rules
- [VERIFICATION_GATES.md](references/VERIFICATION_GATES.md) — evidence requirements, false positive detection

## Code Standards Enforcement

Load `unity-code-standards` skill for review logic. Apply its review references based on findings:
- `review/logic-review-patterns.md` — logic correctness patterns
- `review/architecture-review.md` — architecture checklist
- `review/csharp-quality.md` — C# quality checklist
- `review/performance-review.md` — performance checklist
- `review/unity-specifics.md` — Unity-specific checklist

Format all findings as inline review comments per [INLINE_COMMENT_FORMAT.md](references/INLINE_COMMENT_FORMAT.md).

## Workflow

1. **Fetch** — Get diff (see Input table). For feature/logic requests, identify files via grep/LSP first.
2. **Read full context** — Read the **entire file** for each changed file, not just the diff.
3. **Deep investigate** (parallel) — Spawn explore agents for evidence. See [deep-review-workflow.md](references/deep-review-workflow.md).
4. **Logic review** — Apply `unity-code-standards` review references + [deep-review-workflow.md](references/deep-review-workflow.md) focus areas.
5. **Add inline comments** — Insert tree-format comments per [INLINE_COMMENT_FORMAT.md](references/INLINE_COMMENT_FORMAT.md). Use `edit` tool. Never modify logic.
6. **Summarize** — Report: finding count by severity, files modified, top 3 issues.

## Rules
- Insert comments into source files using `edit`. Never create report documents.
- Never modify actual logic — only add review comments.
- Read full file. Trace data flow end-to-end. Verify lifecycle ordering.
- For evidence and false-positive rules, see [VERIFICATION_GATES.md](references/VERIFICATION_GATES.md).
- For comment formatting rules, see [INLINE_COMMENT_FORMAT.md](references/INLINE_COMMENT_FORMAT.md).
