---
description: Goal verification — walks acceptance criteria and generates structured test reports
agent: hephaestus
subtask: true
---
ULTRAWORK (ulw)
---
You are entering **Plan Test Mode** — autonomous goal verification against the codebase.

## Activation

1. Load the `plan-test` skill immediately — it contains your complete verification protocol.
2. Follow every instruction in that skill without deviation.
3. Do NOT ask questions. Do NOT wait for confirmation. Read goals, verify criteria, report.

## Quick Reference

- **Goals source**: `Docs/Goals/**/*.md` — one goal per file (recursive, including feature subfolders)
- **Execution mode**: Fully autonomous — no user interaction until verification completes
- **Focus**: VERIFICATION over IMPLEMENTATION — walk every acceptance criterion and find code/path/test evidence
- **Auto-triage**: Quick mode (≤5 criteria) vs Deep mode (≥10 criteria)
- **Output**: Writes verdict document to `Docs/Goals/<goal_name>-test.md`
- **Skills**: Use ALL available skills as needed (explore, grep, read)
- **Tracking**: Use `task_create`/`task_update` for every criterion verified

## Rules

- Never ask. Read and verify.
- Never stop early. Check every acceptance criterion against real codebase state.
- Never fabricate evidence. Cite file paths, line numbers, and test names.
- Never write tests, run test suites, create goals, or execute goals — this is read-only verification.
- Mark each criterion PASS / FAIL / PARTIAL with concrete evidence.

---

Load the skill now and begin verification:

```
use_skill("plan-test")
```

$ARGUMENTS
