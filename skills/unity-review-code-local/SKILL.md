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
- [INLINE_COMMENT_FORMAT.md](references/INLINE_COMMENT_FORMAT.md) — comment format, severity tokens, delegation markers

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
5. **Comment + Delegate** — For each finding:
   - Insert a short `// ── REVIEW` comment (per [INLINE_COMMENT_FORMAT.md](references/INLINE_COMMENT_FORMAT.md)).
   - For 🔴/🟡 findings: delegate the fix to `unity-code-quick` via `task(category="quick", load_skills=["unity-code-quick"], run_in_background=true)`.
   - Include in the delegation prompt: file path, line number, the review comment, and the exact fix to apply.
   - Multiple fixes → multiple parallel background tasks. Collect results after all complete.

## Rules

- **Review only** — insert `// ── REVIEW` comments using `edit`. Never apply code fixes directly.
- Delegate code fixes to `unity-code-quick` via background tasks. One task per fix or per file.
- Comments are short, focused, highlight-style. No verbose explanations.
- Never commit. Never push. User reviews the diff.
- Read full file. Trace data flow end-to-end. Verify lifecycle ordering.
- If project uses UniTask, `async UniTaskVoid` can be valid for Unity event entry points.
- For serialization findings, check whether the project has migration/versioning support.
- Never comment without evidence. Investigate first — see `VERIFICATION_GATES.md`.
