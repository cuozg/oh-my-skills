# Review Output Format

Output structure only. Logic/criteria live in SKILL.md and reference checklists. Approval criteria: `read_skill_file("unity-review-general", "references/APPROVAL_CRITERIA.md")`.

## JSON — `/tmp/review-code-pr.json`

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

- **`commit_id`** — Latest commit SHA. Post script auto-injects; do NOT hardcode.
- **`line`** — Line number in the **file** (not diff position). Always use `line`, not `position`.
- **`side`** — Always `"RIGHT"`.
- **Multi-line** — Add `start_line`: `{ "start_line": 10, "line": 15, ... }`. Suggestion must match the full range.

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

**🔴 Critical / 🟡 High** — include Evidence + Why:
```markdown
**[Issue]**: [What's wrong]
**Evidence**: [Proof — caller count, file:line, YAML key]
**Why**: [Impact]
\`\`\`suggestion
[Fixed code]
\`\`\`
```

**🔵 Medium** — include Why. **🟢 Low** — suggestion only:
```markdown
**[Issue/Suggestion]**: [What to improve]
\`\`\`suggestion
[Fixed code]
\`\`\`
```

## Suggestion Syntax

**Single-line**: Target one `line`. Suggestion replaces that line.
**Multi-line**: Target `start_line` to `line`. Suggestion replaces the entire range. Content must be the complete replacement.
**File replacement**: Use `<details>` block for large rewrites instead of inline suggestion.

```markdown
<details><summary>Suggested replacement</summary>

\`\`\`csharp
// Full file content
\`\`\`
</details>
```

**Batch pattern**: Same issue in multiple files → detailed comment on first occurrence, short references on subsequent:
```markdown
**Same issue as [Assets/Scripts/First.cs#L42] — cache GetComponent in Awake.**
\`\`\`suggestion
[Fixed code]
\`\`\`
```

