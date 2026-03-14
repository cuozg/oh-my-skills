# Local Review Workflow

Review locally changed Flutter/Dart files by adding inline `// -- REVIEW` comments.

## Steps

1. **Fetch changes** — `git diff HEAD` (or `git diff --cached` for staged-only)
2. **Filter** — select only `.dart` files from the diff
3. **Read full files** — load complete file content (not just diff hunks)
4. **Spawn parallel subagents** — one `task(category="quick", load_skills=["flutter-standards"], run_in_background=true)` per criterion:

| # | Criterion | flutter-standards Reference |
|---|-----------|----------------------------|
| 1 | Code Style | `references/dart-style-guide.md` |
| 2 | Architecture | `references/architecture-patterns.md` |
| 3 | State Management | `references/state-management-guide.md` |
| 4 | Performance | `references/performance-optimization.md` |
| 5 | Error Handling | `references/error-handling.md` |
| 6 | Async Patterns | `references/async-streams.md` |

5. **Collect** — `background_output` on all tasks
6. **Aggregate** — deduplicate by (path, line), keep highest severity, sort by file -> line
7. **Annotate** — insert `// -- REVIEW` comments at exact line of concern:
   - Icon + label: `🔴 CRITICAL`, `🟠 HIGH`, `🟡 MEDIUM`, `🔵 LOW`, `⚪ STYLE`
   - Include `What:` and `Why:` lines
8. **Apply fixes** — safe single-line fixes only (const constructors, missing await, import ordering); leave complex fixes as comments
9. **Queue remaining** — create `task_create` entries for issues not fixed inline

## Rules

- Always read full file, not just diff hunk
- Flag `setState` in large widgets (>80 lines) as MEDIUM+
- Flag missing `dispose()` when controllers/streams/subscriptions are created
- Flag `!` bang operator on nullable without preceding null check as MEDIUM
- Flag widget methods that should be separate widget classes as LOW
- Never commit — leave diff for user inspection
- Create `task_create` only for unfixed issues

## Output

Modified source files with inline `// -- REVIEW` comments + summary of remaining unfixed issues.
