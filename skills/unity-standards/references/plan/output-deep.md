# Deep Plan Output Template

Save to `Documents/Plans/PLAN_{Name}.md`. Follow this structure exactly.

## Template

```markdown
# PLAN: {Feature Name}

**Size**: {M/L} | **Hours**: {range} | **Risk**: {Low/Medium/High/Critical}
**Date**: {YYYY-MM-DD}

## Request

{1-2 sentences: what the user asked for and why}

## Scope

**In scope:**
- {item}

**Out of scope:**
- {item}

## Impact Analysis

| File / Module | Change Type | Risk |
|---|---|---|
| `{path}` | {New/Modified/Deleted} | {Low/Med/High} |

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| {description} | {Low/Med/High} | {Low/Med/High} | {strategy} |

## Task Breakdown

| ID | Subject | Size | Skill | Blocked By |
|---|---|---|---|---|
| T-1 | {Imperative verb + target} | {XS-L} | {skill-name} | — |
| T-2 | {Imperative verb + target} | {XS-L} | {skill-name} | T-1 |

## Dependency Graph

{ASCII or brief description showing parallel waves}

```
Wave 1 (parallel): T-1, T-2
Wave 2 (after W1): T-3 -> T-4
Wave 3 (after W2): T-5
```
```

## Field Rules

| Field | Format |
|---|---|
| Feature Name | Short, descriptive title |
| Size | M (1-3 days) or L (3-10 days) |
| Hours | Range (e.g., 8-16h) |
| Risk | Low / Medium / High / Critical — evidence-based |
| Request | 1-2 sentences, reference user's words |
| Scope items | Bullet per boundary, concrete not vague |
| Impact rows | One per affected file/module, cite real paths |
| Risk rows | One per identified risk, with mitigation |
| Task ID | Sequential: T-1, T-2, T-3... |
| Subject | Imperative verb + target (e.g., "Add health component") |
| Skill | Exact skill name from registry |
| Blocked By | Task IDs this depends on, or `—` for none |

## Rules

- Every claim in Impact/Risks must cite a real file path
- Task subjects use imperative mood
- Dependency graph must match Blocked By column
- No placeholder ranges — investigate before estimating
