# Deep Mode — Investigation Report

Read-only, multi-angle investigation producing a structured analysis document. No code modifications.

## When to Use

- Bug is intermittent, timing-dependent, or race-condition-like
- 2+ fix attempts have already failed
- Multiple systems involved (state + navigation + platform channels)
- User asks for "root cause analysis," "deep debug," or documented investigation
- Quick Mode looped 3+ times without resolution (auto-escalation)

## Workflow

1. **Parse symptom** — extract error message, timing, frequency, scope (debug/release/platform-specific)
2. **Load references** — read `error-handling.md` and `debug-logging.md` from flutter-standards BEFORE proceeding
3. **Select >=3 angles** — from: widget lifecycle, state management, async/streams, platform channels, navigation, serialization, DI
4. **Investigate each angle** — use grep, read files, trace call chains; cite `file:line` for every finding
5. **Rank candidates** — HIGH (direct evidence + reproducible), MED (indirect evidence), LOW (speculative, mark `[UNCONFIRMED]`)
6. **Propose solutions** — 2-3 per cause, WHAT and WHERE only (no code patches):
   ```
   WHAT: Cancel StreamSubscription in dispose() instead of relying on autoDispose
   WHERE: user_notifier.dart:87 / Risk: LOW
   ```
7. **Write report** — follow the template structure exactly

## Report Template

```markdown
# Analysis: {TOPIC}
Date: {YYYY-MM-DD} | Status: Investigation Complete

## Summary
One-paragraph description of the bug, its impact, and investigation scope.

## Root Cause Candidates
### 1. [HIGH] {Cause title}
- Evidence: `file:line` — description
- Mechanism: How this causes the observed symptom

## Solutions
### For Cause 1
1. WHAT: ... / WHERE: ... / Risk: LOW

## Recommended Next Step
```

## Rules

- **Read-only** — never modify project code during investigation
- **Multi-angle (>=3)** — always investigate 3+ angles
- **Cite everything** — `file:line` for every cause and solution
- **Evidence first** — mark `[UNCONFIRMED]` for speculative claims
- **Max 10 findings** — prioritize by severity, drop low-confidence items
- **2-3 solutions per cause** — WHAT/WHERE/Risk format only

## Output

Save to `Documents/Debug/ANALYSIS_{TOPIC}_{YYYYMMDD}.md`. Sections: Summary → Root Cause Candidates (HIGH/MED/LOW) → Solutions → Recommended Next Step.
