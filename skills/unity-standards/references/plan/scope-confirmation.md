# Scope Confirmation Flow

## Scope Detection Signals

Parse the user's request for scope indicators:

| Signal | Indicates | Confidence |
|--------|-----------|------------|
| "fix," "typo," "bug," "rename," single file | XS | High |
| "add," "simple," 1-3 files, one system | S | High |
| "implement," "feature," 2+ systems | M | Medium |
| "refactor," "architecture," "redesign," data migration | L | Medium |
| Cross-system dependencies mentioned | bump +1 size | Medium |
| Data layer / save format involved | bump +1 size | Medium |
| Description is 1 sentence | XS/S signal | High |
| Description is multi-paragraph with details | M/L signal | Medium |

### Confidence Levels

- **High** — Multiple signals agree, clear scope, similar work done before
- **Medium** — Mixed signals, some unknowns, single indicator
- **Low** — Ambiguous request, contradictory signals, new territory

## Confirmation Output (BLOCKING)

Print this template and **STOP. Do NOT generate a plan until user responds.**

```
🔍 SCOPE DETECTION
Detected: {XS/S/M/L}
Confidence: {high/medium/low}

Reasoning:
• {signal 1 + evidence from request}
• {signal 2 + evidence from request}
• {signal 3 + evidence from request}

📋 Initial Estimates:
• Hours: {range from sizing-guide.md}
• Risk: {low/medium/high}
• Systems involved: {list if identifiable}

❓ Does this scope look right?
   → Yes, proceed with {Quick/Deep} plan
   → Adjust to {alternative size}
   → Need more investigation first
```

## Follow-up Output (BLOCKING)

After generating the plan, print this and **STOP. Wait for user response.**

```
---

❓ Next steps?
   1. Looks good → Create tasks now
   2. Adjust scope → Regenerate with different size
   3. Modify tasks → Which tasks to split/merge/change?
   4. Done, no tasks needed
```

## Task Creation Rules

| Mode | When to create tasks |
|------|---------------------|
| Quick (XS/S) | Auto-create immediately after user says "looks good" or "create tasks" |
| Deep (M/L) | Ask "Create tasks now?" and **BLOCK again** — only create after explicit "yes" |
| Costing (XL) | Never auto-create — user reviews HTML plan and decides separately |
