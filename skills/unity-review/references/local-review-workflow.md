# Local Review Workflow

Review locally changed Unity C# files by adding inline `// ── REVIEW` comments.

## Steps

1. **Fetch changes** — `git diff HEAD` (or `git diff --cached` for staged-only)
2. **Filter** — select only `.cs` files from the diff
3. **Read full files** — load complete file content (not just diff hunks)
4. **Spawn 6 parallel subagents** — one `task(category="quick", load_skills=["unity-standards"], run_in_background=true)` per criterion:

| # | Criterion | Checklist |
|---|-----------|-----------|
| 1 | Logic | `review/logic-checklist.md` |
| 2 | Lifecycle | `review/unity-lifecycle-risks.md` |
| 3 | Serialization | `review/serialization-risks.md` |
| 4 | Performance | `review/performance-checklist.md` |
| 5 | Architecture | `review/architecture-checklist.md` |
| 6 | Concurrency | `review/concurrency-checklist.md` |

See `unity-standards/references/review/parallel-review-criteria.md` for subagent prompt template.

5. **Collect** — `background_output` on all 6 tasks
6. **Aggregate** — deduplicate by (path, line), keep highest severity, sort by file → line
7. **Investigate** — use `lsp_goto_definition` / `lsp_find_references` to validate findings needing caller/lifecycle context
8. **Annotate** — insert `// ── REVIEW` comments using format from `unity-standards/references/review/comment-format.md`:
   - Place at exact line of concern
   - Icon + label: `🔴 CRITICAL`, `🟠 HIGH`, `🟡 MEDIUM`, `🔵 LOW`, `⚪ STYLE`
   - Include `What:` and `Why:` lines
9. **Apply fixes** — safe single-line fixes only (null checks, caching, unsubscribes); leave complex fixes as comments
10. **Queue remaining** — create `task_create` entries for issues not fixed inline

## Rules

- Always read full file, not just diff hunk
- Use `lsp_find_references` before flagging dead code
- Flag `Update()` allocations (LINQ, string concat, closures) as MEDIUM+
- Flag missing `OnDestroy` unsubscription when `OnEnable` subscribes
- Never commit — leave diff for user inspection
- Create `task_create` only for unfixed issues

## Output

Modified source files with inline `// ── REVIEW` comments + summary of remaining unfixed issues.
