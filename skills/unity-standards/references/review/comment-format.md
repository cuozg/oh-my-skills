# Review Comment Format

## Inline Comment Syntax

```
// -- REVIEW {icon} {LABEL} #{category}
// What: 1-line summary
// Why:  1-3 lines - impact + evidence
```

## Severity Levels

| Icon | Label | Tag | Meaning | Action |
|------|-------|-----|---------|--------|
| 🔴 | CRITICAL | `#critical` | Crash, data loss, security hole | Must fix |
| 🟠 | HIGH | `#high` | Bug, incorrect behavior | Must fix |
| 🟡 | MEDIUM | `#medium` | Performance, maintainability | Should fix |
| 🔵 | LOW | `#low` | Minor improvement | Consider |
| ⚪ | STYLE | `#style` | Naming, formatting | Optional |

## Categories

`null-safety` `lifecycle` `state` `concurrency` `allocation` `serialization` `event-leak` `logic` `security` `architecture`

## Rules

- One comment per issue — do not combine unrelated findings
- Place comment on the line above the problem
- Always include icon, label, and tag on header line
- Apply code fix inline only when safe and local
- Never commit review changes — leave for inspection
