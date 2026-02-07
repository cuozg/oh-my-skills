# Orchestrator Routing Decision

**Request**: {User request summary}
**Date**: {YYYY-MM-DD}

---

## 1. Classification

| Field | Value |
|-------|-------|
| Intent | {e.g., Fix error, Implement feature, Review PR} |
| Complexity | {Small / Medium / Large} |
| Category | {Error, Feature, Review, Documentation, Performance, Platform, Data, Tool} |

---

## 2. Skill Routing

| Order | Skill | Role | Reason |
|-------|-------|------|--------|
| 1 | `{primary-skill}` | Primary | {Why this skill} |
| 2 | `{chain-skill}` | Chain (if needed) | {When to chain} |
| 3 | `{support-skill}` | Support | {What it adds} |

---

## 3. Execution Flow

```
{skill-1} → {skill-2} → {skill-3} (if applicable)
```

1. **{skill-1}**: {What it handles}
2. **{skill-2}**: {What it handles, if chaining}

---

## 4. Cross-Cutting Checks

- [ ] Performance impact considered
- [ ] Platform compatibility verified
- [ ] Tests run after completion
- [ ] Original goal verified
