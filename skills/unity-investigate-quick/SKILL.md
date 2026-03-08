---
name: unity-investigate-quick
description: Quick Q&A about Unity codebase — how systems work, call chains, flow traces. Triggers — 'how does X work', 'what calls this', 'trace the flow', 'explain this system', 'quick investigate'.
metadata:
  author: kuozg
  version: "1.0"
---
# unity-investigate-quick

Answer a focused Unity codebase question in the fewest tool calls possible.

## When to Use

- "How does X work?" or "What calls Y?"
- "Trace the flow from event to handler"
- "Explain this system briefly"
- Quick sanity checks before making a change

## Workflow

1. **Parse** — Extract the exact symbol, file, or concept from the question
2. **Find** — Use `lsp_goto_definition` on the target symbol to locate its declaration
3. **Trace** — Use `lsp_find_references` or `grep` to follow call chains one level deep
4. **Stop** — Halt the moment the question can be answered; skip unused steps
5. **Reply** — Format as summary + 1-3 typed detail blocks

## Rules

- Stop the moment the question can be answered — speed over ceremony
- Never read an entire file to answer a line-level question
- Prefer `lsp_goto_definition` over `grep` when a symbol name is known
- Inline code snippets only when they directly clarify the answer
- No headers, no preamble — answer starts immediately

## Output Format

Single summary sentence followed by 1-3 detail blocks in tree format:
`## {Target} [{type: class|method|event|system}]` → summary → details as inline bullets.

## Standards

Load `unity-standards` when answers require convention context. Key references:

- `code-standards/lifecycle.md` — Awake/Start/OnEnable order, coroutine rules
- `code-standards/events.md` — C# events, UnityEvent, SO channels, Action
- `code-standards/dependencies.md` — DI, service locator, constructor injection

Load via `read_skill_file("unity-standards", "references/code-standards/<file>")`.
