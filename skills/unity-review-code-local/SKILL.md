---
name: unity-review-code-local
description: Local C# logic review — adds inline REVIEW comments to changed files. Triggers — 'review my code', 'code review', 'review local', 'check my changes', 'review this file'.
---
# unity-review-code-local

Add inline `// ── REVIEW` comments with icon + label + tag to locally changed C# files. Apply code fixes inline when safe. Covers logic, edge cases, state, data flow, concurrency.

## When to Use

- Reviewing uncommitted or staged changes before a commit
- Checking a single file or feature for correctness issues
- Wanting reviewer feedback without opening a GitHub PR

## Workflow

1. **Fetch changes** — run `git diff HEAD` (or `git diff --cached`) to get changed files and hunks
2. **Read changed files** — load full file content for each `.cs` file in the diff
3. **Investigate context** — use `lsp_goto_definition` / `lsp_find_references` to trace callers, state owners, lifecycle interactions
4. **Review** — evaluate logic correctness, null paths, race conditions, event lifecycle, serialization, allocation
5. **Annotate** — insert `// ── REVIEW 🔴 CRITICAL #category` comments with `What:` / `Why:` lines above the issue
6. **Apply fixes** — rewrite the problem line directly when fix is safe (single-line, no cross-file deps); leave unchanged otherwise
7. **Queue fixes** — create `task_create` entries for issues that could not be applied inline

## Rules

- Insert comments at the exact line of concern, not at the top of the file
- Use format from `references/review-comment-format.md` for every comment
- Use icon + label + tag: `🔴 CRITICAL`, `🟠 HIGH`, `🟡 MEDIUM`, `🔵 LOW`, `⚪ STYLE`
- Cover at minimum: null guards, Unity lifecycle order, event subscription leaks, state mutation, serialization
- Apply safe single-line fixes directly (null checks, caching, unsubscribes); leave complex/design fixes as comments only
- Never commit changes — leave diff for user inspection
- Always read the full file, not just the diff hunk
- Use `lsp_find_references` before flagging a method as unused or dead code
- Check `[SerializeField]` usage — warn if private fields are mutated from multiple systems
- Flag `Update()` allocations (LINQ, string concat, closures) as WARNING or higher
- Flag missing `OnDestroy` unsubscription when `OnEnable` subscribes to events
- Create `task_create` only for issues NOT fixed inline

## Output Format

Inline `// ── REVIEW` comments with icons inserted into source files. Safe fixes applied directly to code.
A summary list of remaining unfixed issues (with created fix tasks) is printed after annotation.

## Reference Files

- `references/review-comment-format.md` — skill-specific severity subset + categories (loads `unity-standards/references/review/comment-format.md` for full format)

Load references on demand via `read_skill_file("unity-review-code-local", "references/review-comment-format.md")` and `read_skill_file("unity-standards", "references/review/comment-format.md")`.
