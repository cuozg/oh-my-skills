# Review Output Format

This template defines **output structure only**. All review logic, criteria, and decision rules are in [SKILL.md](../SKILL.md).

---

## JSON Structure

Submit **ONE GitHub review** as `/tmp/review.json`:

```json
{
  "body": "[SUMMARY]",
  "event": "REQUEST_CHANGES|COMMENT|APPROVE",
  "comments": [
    {
      "path": "Assets/Scripts/Example.cs",
      "line": 42,
      "side": "RIGHT",
      "body": "[INLINE COMMENT]"
    }
  ]
}
```

---

## Summary Body Format

```markdown
## Code Review - PR #[NUMBER]

**Scope**: [TICKET_ID] - [Brief description]

[One-sentence assessment]. See inline comments for details.

### Acceptance Criteria

#### UI Verification
- [ ] [Specific screen/component] displays correctly
- [ ] [UI element] responds to interaction
- [ ] [Animation/transition] plays smoothly

#### Functional Verification
- [ ] [Feature] works with valid inputs
- [ ] Edge cases handled (null, empty, boundary)
- [ ] [Integration] communicates with [service]
- [ ] Error handling covers [conditions]

#### Performance Verification
- [ ] No frame drops during [operations]
- [ ] Memory stable during [scenarios]
- [ ] No GC spikes from [allocations]

#### Data Verification
- [ ] Existing saves/prefabs migrate without data loss
- [ ] [Data structure] round-trips correctly
- [ ] No breaking serialization changes

### Breaking Changes ([COUNT])
- [One-line per critical issue]

### Potential Issues ([COUNT])
- [One-line per major issue]

### Code Quality ([COUNT])
- [One-line per minor issue]

### Impact Analysis
- Files investigated: X
- Breaking call sites: Y
```

---

## Inline Comment Format

Every inline comment follows the **Issue → Evidence → Why → Fix** structure. Keep each section to 1-2 lines max.

### Critical

```markdown
**[Issue Name]**: [What's wrong in one line]

**Evidence**: [The code pattern or call site proving this is real]
**Why**: [Concrete impact — crash, leak, data loss, N callers break]

\`\`\`suggestion
[Fixed code]
\`\`\`
```

### Major

```markdown
**[Issue Name]**: [What's wrong in one line]

**Evidence**: [Code pattern or condition that triggers this]
**Why**: [When/how this causes problems]

\`\`\`suggestion
[Fixed code]
\`\`\`
```

### Minor

```markdown
**[Issue Name]**: [What to improve]

**Why**: [Brief reason]

\`\`\`suggestion
[Fixed code]
\`\`\`
```

---

## Complete Example

```json
{
  "body": "## Code Review - PR #25103\n\n**Scope**: WHIP-55760 - Fix showdown hub display\n\nWell-structured change. Two issues to address before merge.\n\n### Acceptance Criteria\n\n#### UI Verification\n- [ ] Showdown hub shows active tournaments correctly\n- [ ] List filters inactive tournaments\n- [ ] UI updates on tournament status change\n\n#### Functional Verification\n- [ ] `GetActiveTournamentList()` returns only active tournaments\n- [ ] Handles null/empty tournament list gracefully\n- [ ] Works when called from `ShowdownHubController`\n\n#### Performance Verification\n- [ ] No frame drops filtering tournament list\n- [ ] Memory stable with multiple tournaments\n\n#### Data Verification\n- [ ] Tournament data structure unchanged\n- [ ] No serialization breaking changes\n\n### Potential Issues (1)\n- Method visibility `private → public` creates cross-controller coupling\n\n### Code Quality (1)\n- Missing null check on `persistentShowdownController`\n\n### Impact Analysis\n- Files investigated: 2\n- Breaking call sites: 0",
  "event": "COMMENT",
  "comments": [
    {
      "path": "Assets/Scripts/M42/Career/CareerPvpController.cs",
      "line": 159,
      "side": "RIGHT",
      "body": "**Visibility Escalation**: `GetActiveTournamentList` changed `private → public`.\n\n**Evidence**: Now called from `ShowdownHubController.cs:77`, creating cross-controller dependency.\n**Why**: `ShowdownHubController` depends on `CareerPvpController` being instantiated — breaks if it isn't.\n\n```cs\n// Extract to ShowdownHubUtils.cs to avoid coupling:\npublic static List<VersusTourneyItemData> GetActiveTournamentList(List<VersusTourneyItemData> items)\n{\n    // ... logic\n}\n```"
    },
    {
      "path": "Assets/Scripts/ShowdownIteration/ShowdownHubController.cs",
      "line": 77,
      "side": "RIGHT",
      "body": "**Potential NullReference**: `persistentShowdownController` used without null check.\n\n**Why**: Controller may not be instantiated on first frame or after scene transition.\n\n```suggestion\nif (persistentShowdownController != null && listTournaments != null) {\n    var activeTournaments = persistentShowdownController.GetActiveTournamentList(listTournaments);\n    // ...\n}\n```"
    }
  ]
}
```
