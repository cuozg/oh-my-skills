# Scope Detection Guide

## Signal Analysis

Analyze the user's request against these signal categories to determine scope.

### Keyword Signals

| Keywords | Likely Size |
|----------|-------------|
| "quick," "small," "simple," "just add," "typo," "rename" | XS–S |
| "feature," "system," "implement," "build" | S–M |
| "plan this," "break down," "spans multiple," "cross-system" | M–L |
| "refactor," "migrate," "architecture," "redesign" | L |

### Structural Signals

| Signal | Size Impact |
|--------|-------------|
| Single file mentioned | XS–S |
| 2–3 files or 1 system | S–M |
| Multiple systems, assemblies | M–L |
| New architecture pattern needed | L |
| Data migration required | +1 size |

### Complexity Indicators

| Indicator | Weight |
|-----------|--------|
| No new patterns needed | Base |
| Crosses assembly boundaries | +1 size |
| Requires editor + runtime changes | +1 size |
| Has UI + logic + data layers | +1 size |
| External dependency integration | +1 size |
| Needs backward compatibility | +1 size |

## Confidence Assessment

| Level | Criteria |
|-------|----------|
| **High** (90%+) | Clear scope, similar past work, few unknowns |
| **Medium** (60–89%) | Known patterns but some exploration needed |
| **Low** (<60%) | New territory, ambiguous scope, multiple interpretations |

## Output Format

Present scope detection as:

```
🔍 SCOPE DETECTION

**Size**: {XS/S/M/L} — {1-sentence reasoning}
**Confidence**: {High/Medium/Low} — {why}
**Hours**: {range}
**Risk**: {Low/Medium/High}

📋 Key signals:
- {signal 1}
- {signal 2}
- {signal 3}

✅ Proceed with {Quick/Deep} plan? (or adjust scope)
```

## Rules

- Base detection on evidence from the request, not assumptions
- If confidence is Low, say so — don't inflate
- Always cite which signals drove the size decision
- When signals conflict, size UP not down
- XS/S routes to Quick mode, M/L routes to Deep mode
- If request appears XL (40+h), report as L with a note about phasing
