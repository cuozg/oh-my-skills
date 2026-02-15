# Review Output Format

Output structure only. Logic/criteria live in SKILL.md and reference checklists.

## JSON — `/tmp/review.json`

```json
{
  "body": "[SUMMARY — see format below]",
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
#### UI Verification
- [ ] [Screen/component] displays correctly
#### Functional Verification
- [ ] [Feature] works; edge cases handled
#### Performance Verification
- [ ] No frame drops, GC spikes
#### Data Verification
- [ ] No breaking serialization changes
#### Asset Verification
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
**Why**: [Impact — crash, leak, N callers break]
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

Asset issues use same format — must include Issue + Why + Suggestion (no exceptions).
