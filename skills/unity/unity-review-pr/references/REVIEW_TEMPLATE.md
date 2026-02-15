# Review Output Format

Output structure only. Logic/criteria live in SKILL.md and reference checklists.

## JSON — `/tmp/review.json`

```json
{
  "body": "[SUMMARY]",
  "event": "REQUEST_CHANGES|COMMENT|APPROVE",
  "comments": [
    { "path": "Assets/Scripts/Example.cs", "line": 42, "side": "RIGHT", "body": "[INLINE]" }
  ]
}
```

Line numbers = right side of diff. `side` always `"RIGHT"`.

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
### Code Quality ([N])
### Impact Analysis
- Files investigated: X · Breaking call sites: Y
```

## Inline Comment Format

**🔴 Critical / 🟡 Major:**
```markdown
**[Issue]**: [What's wrong]
**Evidence**: [Proof — caller count, file:line, YAML key]
**Why**: [Impact]
\`\`\`suggestion
[Fixed code]
\`\`\`
```

**🔵 Minor:**
```markdown
**[Issue]**: [What to improve]
**Why**: [Reason]
\`\`\`suggestion
[Fixed code]
\`\`\`
```

Asset issues use same format — must include Issue + Why + Suggestion.
