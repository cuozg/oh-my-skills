---
description: Delegate a task to the best-fit agent with automatic skill selection
agent: sisyphus
model: github-copilot/claude-opus-4.6
subtask: true
---

## Task

$ARGUMENTS

## Protocol

1. **Classify** the request: trivial (direct execute) | exploratory (explore agents first) | implementation (delegate)
2. **Select skills** matching the domain from all installed skills (user-installed override built-in)
3. **Pick category**: `quick` (single file) | `deep` (complex) | `ultrabrain` (logic-heavy) | `visual-engineering` (UI) | `writing` (docs)
4. **Execute** via `task()` with structured prompt including: TASK, EXPECTED OUTCOME, MUST DO, MUST NOT DO, CONTEXT
5. **Verify** with `lsp_diagnostics` on changed files; confirm request is fully addressed

## Rules

### MUST DO:
- Load ALL relevant skills in `load_skills=[]` — never leave empty
- Create todos before non-trivial work
- Follow `.opencode/rules/` conventions
- Use `unityMCP` for Unity Editor operations
- Return session_id on completion

### MUST NOT DO:
- NEVER commit/push unless explicitly requested
- NEVER perform destructive actions without confirmation
- NEVER skip skill loading when delegating
- NEVER leave code in broken state
