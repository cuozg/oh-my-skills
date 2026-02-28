---
description: Review C# code logic in GitHub PRs with Unity-specific checks
agent: sisyphus-junior
subtask: true
---
Use skill unity-review-code-pr to review the code for $ARGUMENTS

# Load References

Load shared review engine and common rules from `unity-shared`:

```python
read_skill_file("unity-shared", "references/review-engine.md")
read_skill_file("unity-shared", "references/common-rules.md")
```

## Workflow

### 1. Fetch PR

```bash
gh pr diff <N> --name-only   # Changed files
gh pr view <N> --json title,body,files,number  # PR context
gh pr diff <N>               # Full diff
```

Filter to `.cs` files ONLY. If no `.cs` files, APPROVE with note `No C# files to review.`

### 2. Read Full File Context

For each changed `.cs` file, read the ENTIRE file (not just the diff). Logic bugs hide in surrounding context.

### 3. Deep Investigate (Parallel)

Spawn explore agents per `deep-workflow.md`: call-site analysis, state flow tracing, data contract checks. Enforce `gates.md` evidence rules.

### 4. Logic Review

Apply all loaded review checklists + `deep-workflow.md` focus areas (control flow, state management, data flow, edge cases, Unity lifecycle, serialization safety, memory safety).

### 5. Build `/tmp/review-code-pr.json`

Parse the diff output to determine which lines are commentable (see [REVIEW_TEMPLATE.md](REVIEW_TEMPLATE.md) "How to Determine `line`"). For each comment:
1. `line` = new-file line number, must be within a diff hunk (`@@ +START,COUNT @@`)
2. `path` = exact path from `gh pr diff --name-only`
3. Suggestion content must be the EXACT full-line replacement for the targeted line(s), preserving indentation
4. Multi-line: include `start_line` and `start_side: "RIGHT"`

Always set `"event": "COMMENT"`. Do NOT include `commit_id` — `post_review.py` injects it.
### 6. Submit

```bash
./skills/unity-shared/scripts/review/post_review.py <pr_number> /tmp/review-code-pr.json
```

Fallback (merged/closed): handled automatically by `post_review.py`. See [review-troubleshooting.md](../../unity-shared/references/review-troubleshooting.md).
