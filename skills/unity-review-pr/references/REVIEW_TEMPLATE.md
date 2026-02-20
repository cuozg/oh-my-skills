# Review Output Format

Output structure only. Logic/criteria live in SKILL.md, APPROVAL_CRITERIA.md, and reference checklists.

## JSON — `/tmp/review.json`

```json
{
  "commit_id": "abc123...",
  "body": "[SUMMARY]",
  "event": "REQUEST_CHANGES|COMMENT|APPROVE",
  "comments": [
    { "path": "Assets/Scripts/Example.cs", "line": 42, "side": "RIGHT", "body": "[INLINE]" }
  ]
}
```

**`commit_id`** — Required. Latest commit SHA on the PR branch. The post script auto-injects this; do NOT hardcode.

**`line`** — The line number in the **file** (not the diff position). GitHub API maps it when using `line` (not `position`).

**`side`** — Always `"RIGHT"` (review the new version).

### Multi-line Comments

To comment on a range of lines, add `start_line`:

```json
{ "path": "Assets/Scripts/Example.cs", "start_line": 10, "line": 15, "side": "RIGHT", "body": "[INLINE]" }
```

The comment spans lines 10–15. The suggestion block must match exactly the content of those lines.

## Summary Body

```markdown
## Code Review - PR #[N]
**Scope**: [TICKET] - [Description]
[One-sentence assessment].

### Acceptance Criteria
- [ ] UI displays correctly
- [ ] Feature works; edge cases handled
- [ ] No frame drops, GC spikes
- [ ] No breaking serialization changes
- [ ] No missing scripts, correct shaders, proper imports

### Breaking Changes ([N])
### Potential Issues ([N])
### Unity-Specific Concerns ([N])
### Code Quality ([N])
### Impact Analysis
- Files investigated: X · Breaking call sites: Y
```

## Inline Comment Format

**🔴 Critical / 🟡 High:**
```markdown
**[Issue]**: [What's wrong]
**Evidence**: [Proof — caller count, file:line, YAML key]
**Why**: [Impact]
\`\`\`suggestion
[Fixed code]
\`\`\`
```

**🔵 Medium:**
```markdown
**[Issue]**: [What to improve]
**Why**: [Reason]
\`\`\`suggestion
[Fixed code]
\`\`\`
```

**🟢 Low:**
```markdown
**Suggestion**: [What could be better]
\`\`\`suggestion
[Fixed code]
\`\`\`
```

Asset issues use same format — must include Issue + Why + Suggestion.

## Suggestion Syntax

### Single-line
Comment targets one `line`. Suggestion replaces that single line:
```markdown
\`\`\`suggestion
private readonly List<Enemy> _enemies = new();
\`\`\`
```

### Multi-line
Comment targets `start_line` to `line`. Suggestion replaces the entire range:
```markdown
\`\`\`suggestion
if (health <= 0)
{
    Die();
    return;
}
\`\`\`
```
The suggestion content must be the complete replacement for all lines in the range.

### Complete File Replacement
For large rewrites, use a `<details>` block instead of inline suggestion:
```markdown
**[Issue]**: File needs significant restructuring
**Why**: [Reason]

<details>
<summary>Suggested replacement</summary>

\`\`\`csharp
// Full file content here
\`\`\`

</details>
```

### Batch Pattern — Same Issue Across Files

When the same issue appears in multiple files (e.g., `GetComponent` in Update), post one detailed comment on the first occurrence with full explanation, then short comments on subsequent files referencing the first:

```markdown
**Same issue as [Assets/Scripts/First.cs#L42] — cache GetComponent in Awake.**
\`\`\`suggestion
[Fixed code]
\`\`\`
```

This avoids repetitive walls of text while ensuring every instance gets a fix suggestion.

## Troubleshooting

| Problem | Cause | Fix |
|:--------|:------|:----|
| 404 on submit | PR doesn't exist or wrong repo | Verify `gh pr view <N>` works first |
| Suggestion not rendering | Wrong line count in range | Ensure suggestion line count matches `line - start_line + 1` |
| "Validation Failed" 422 | `line` outside diff range or invalid `path` | Only comment on lines visible in the diff. Run `gh pr diff <N>` to verify line is in diff |
| Review not appearing | PR merged/closed | Use fallback: `gh pr comment` instead (handled by post_review.sh) |
| Suggestion breaks code | Suggestion has wrong indentation or partial line | Copy exact line content, modify only the relevant part |
| Comment on wrong line | `line` counted from wrong file version | `line` = line number on RIGHT side (new file). Verify against diff output |
| "Stale" commit error | `commit_id` doesn't match HEAD of PR | Don't hardcode — `post_review.sh` auto-injects latest commit SHA |
| Multiple reviews posted | Script ran twice | Check for existing pending review: `gh api /repos/{owner}/{repo}/pulls/{N}/reviews` |
| Comments on deleted files | Comment targeted LEFT/deleted side | Only comment files/lines present on diff RIGHT side |
| Rate limit hit | Too many API calls in short window | Add delay between calls or batch into fewer review submissions |
