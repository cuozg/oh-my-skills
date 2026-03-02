---
name: unity-review-code-local
description: Local C# logic review — adds inline REVIEW comments to changed files. Triggers — 'review my code', 'code review', 'review local', 'check my changes', 'review this file'.
---
# unity-review-code-local

Add inline `// ── REVIEW` comments to locally changed C# files, covering logic correctness, edge cases, state, data flow, and concurrency.

## When to Use

- Reviewing uncommitted or staged changes before a commit
- Checking a single file or feature for correctness issues
- Wanting reviewer feedback without opening a GitHub PR

## Workflow

1. **Fetch changes** — run `git diff HEAD` (or `git diff --cached`) to get changed files and hunks
2. **Read changed files** — load full file content for each `.cs` file in the diff
3. **Investigate context** — use `lsp_goto_definition` / `lsp_find_references` to trace callers, state owners, lifecycle interactions
4. **Review** — evaluate logic correctness, null paths, race conditions, event lifecycle, serialization, allocation
5. **Annotate** — insert `// ── REVIEW` comments directly into the code at the relevant lines
6. **Queue fixes** — create background `task_create` entries for each non-trivial issue found

## Rules

- Insert comments at the exact line of concern, not at the top of the file
- Use format from `references/review-comment-format.md` for every comment
- Flag severity: CRITICAL, WARNING, or NOTE on every comment
- Cover at minimum: null guards, Unity lifecycle order, event subscription leaks, state mutation, serialization
- Never modify logic — annotations only
- Never commit changes — leave diff for user inspection
- Always read the full file, not just the diff hunk
- Use `lsp_find_references` before flagging a method as unused or dead code
- Check `[SerializeField]` usage — warn if private fields are mutated from multiple systems
- Flag `Update()` allocations (LINQ, string concat, closures) as WARNING or higher
- Flag missing `OnDestroy` unsubscription when `OnEnable` subscribes to events
- Create one `task_create` per distinct issue for background fix tracking

## Output Format

Inline `// ── REVIEW` comments inserted into the source files. A summary list of created fix tasks is printed after annotation.

## Reference Files

- `references/review-comment-format.md` — skill-specific severity subset + categories (loads `unity-standards/references/review/comment-format.md` for full format)

Load references on demand via `read_skill_file("unity-review-code-local", "references/review-comment-format.md")` and `read_skill_file("unity-standards", "references/review/comment-format.md")`.
