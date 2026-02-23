---
name: unity-review-code-local
description: "Deep logic review for Unity C# code in the local project. Reviews code changes with surgical focus on logic correctness, edge cases, state management, data flow, and concurrency — then adds short review comments directly into the code and applies suggested fixes. No summary document. No report. No GitHub interaction. No commit. No push. User reviews the diff. Input: commit hash, commit range, branch diff, or a feature/logic description to review. Use when: reviewing logic before commit, validating a feature implementation, auditing business logic, tracing data flow for correctness, reviewing a specific commit. Triggers: 'review code', 'review logic', 'check this logic', 'review commit', 'review my changes', 'logic review', 'code review', 'review this feature'."
---

# Unity Logic Reviewer (Local)

Deep logic review for local project. Comment directly into C# source files AND apply fixes. No report, no summary, no GitHub, no commit.

## Output

1. **Short inline comments** in C# source files — per [INLINE_COMMENT_FORMAT.md](references/INLINE_COMMENT_FORMAT.md).
2. **Applied code fixes** directly in the same files — the actual fix, not just a suggestion.
3. User reviews the combined diff (comments + fixes) before committing.

## Input → Diff Command

| Input | Command |
|:------|:--------|
| None (default) | `git diff` + `git diff --cached` |
| Commit SHA | `git show <hash>` |
| Commit range | `git diff <base>..<head>` |
| Branch | `git diff <branch>...HEAD` |
| Feature/logic request | Find relevant files via grep/LSP |

## Severity

Four levels: 🔴 CRITICAL, 🟡 HIGH, 🔵 MEDIUM, 🟢 LOW. See [INLINE_COMMENT_FORMAT.md](references/INLINE_COMMENT_FORMAT.md).

## Load References

Always load the output format reference:
- [INLINE_COMMENT_FORMAT.md](references/INLINE_COMMENT_FORMAT.md) — comment format, severity tokens, applied-fix marker

Load shared review engine from `unity-code-standards`:

```python
read_skill_file("unity-code-standards", "references/review/deep-review-workflow.md")
read_skill_file("unity-code-standards", "references/review/VERIFICATION_GATES.md")
read_skill_file("unity-code-standards", "references/review/logic-review-patterns.md")
read_skill_file("unity-code-standards", "references/review/csharp-quality.md")
read_skill_file("unity-code-standards", "references/review/performance-review.md")
read_skill_file("unity-code-standards", "references/review/unity-specifics.md")
read_skill_file("unity-code-standards", "references/review/architecture-review.md")
```

## Workflow

1. **Fetch** — Get diff (see Input table). For feature/logic requests, identify files via grep/LSP first.
2. **Read full context** — Read the **entire file** for each changed file, not just the diff.
3. **Deep investigate** (parallel) — Spawn explore agents per `deep-review-workflow.md`: call-site analysis, state flow, data contracts.
4. **Logic review** — Apply all loaded review checklists + `deep-review-workflow.md` focus areas. Enforce `VERIFICATION_GATES.md` evidence rules.
5. **Comment + Fix** — For each finding:
   - Insert a short `// ── REVIEW` comment (per [INLINE_COMMENT_FORMAT.md](references/INLINE_COMMENT_FORMAT.md)).
   - Apply the fix directly in the code below the comment.
   - Use `edit` tool for both comment and fix in a single edit operation.

## Rules

- **Comment + fix** in source files using `edit`. Never create report/summary documents.
- Comments are short, focused, highlight-style. No verbose explanations.
- Apply the actual code fix — don't just suggest it.
- Never commit. Never push. User reviews the diff.
- Read full file. Trace data flow end-to-end. Verify lifecycle ordering.
- If project uses UniTask, `async UniTaskVoid` can be valid for Unity event entry points.
- For serialization findings, check whether the project has migration/versioning support.
- Never comment without evidence. Investigate first — see `VERIFICATION_GATES.md`.
