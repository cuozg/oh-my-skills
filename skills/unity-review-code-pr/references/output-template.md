# Review Output Format

Output structure only. Logic/criteria live in SKILL.md and reference checklists.

## JSON — `/tmp/review-code-pr.json`

```json
{
  "body": "[SUMMARY]",
  "event": "COMMENT",
  "comments": [
    { "path": "Assets/Scripts/Example.cs", "line": 42, "side": "RIGHT",
      "body": "**🔴 Issue**: ...\n```suggestion\nexactReplacementCode();\n```" }
  ]
}
```

Do NOT include `commit_id` — `post_review.py` injects it.

## Field Rules

| Field | Value | Notes |
|:------|:------|:------|
| `path` | Relative path from `gh pr diff --name-only` | Case-sensitive, exact match |
| `line` | Line number in **new file** (RIGHT side) | **MUST be within a diff hunk** — 422 if outside |
| `side` | Always `"RIGHT"` | |
| `start_line` | First line of multi-line range | Required with `start_side: "RIGHT"` |
| `commit_id` | Omit | `post_review.py` injects automatically |
| `event` | Always `"COMMENT"` | Only `unity-review-general` sets APPROVE/REQUEST_CHANGES |

## How to Determine `line`

Parse `gh pr diff <N>`. Hunk header `@@ -12,8 +14,10 @@` → new-file lines **14–23** are commentable.

1. `line` must fall within `[+START, +START+COUNT-1]` of some hunk
2. For `+` lines (added): use the new-file line number
3. For context lines (no prefix): use the new-file line number
4. Never target `-` lines (deleted) with `side: "RIGHT"`

## Suggestion Syntax

Content inside ` ```suggestion ` **replaces** the targeted line(s) character-for-character.

**Single-line** — `line: 42` → suggestion replaces ONLY line 42:
```
"body": "**🔴 Issue**\n```suggestion\n    private readonly List<int> _cache = new();\n```"
```

**Multi-line** — `start_line: 10, line: 15, start_side: "RIGHT"` → replaces ALL 6 lines:
```
"body": "...\n```suggestion\n    // complete replacement for lines 10-15\n    private void Init() { }\n```"
```

**Rules:**
- Suggestion replaces the WHOLE line(s), not a substring — include full line content
- Preserve original indentation exactly
- Line count in suggestion can differ from range (add/remove lines)
- Line outside diff → 422 Validation Failed

## Summary Body

```markdown
## Code Review - PR #[N]
**Scope**: [TICKET] - [Description]
[One-sentence assessment].
### Breaking Changes ([N])
### Potential Issues ([N])
### Unity-Specific Concerns ([N])
### Code Quality ([N])
### Impact Analysis
- Files investigated: X · Breaking call sites: Y
```

## Inline Comment Format

**🔴 Critical / 🟡 High**:
```markdown
**🔴 Issue Title**: One-line problem summary
- **Why**: root cause or risk
- **Fix**: concrete solution
\`\`\`suggestion
[Fixed code — exact replacement, preserving indentation]
\`\`\`
```

**🔵 Medium / 🟢 Low** — `**🔵 Issue**: Problem → fix.` + suggestion block.

**Batch**: Same issue in N files → full on first, `**Same issue as [path#L42]**` on rest.
