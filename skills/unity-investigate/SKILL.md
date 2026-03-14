---
name: unity-investigate
description: >
  Investigate Unity codebases — from quick Q&A to comprehensive system analysis reports. Auto-triages
  request complexity: simple questions (how does X work, what calls Y, trace this flow) get direct inline
  answers; complex requests (system analysis, pre-refactor audit, architecture investigation, team
  documentation) produce a structured markdown report with Mermaid diagrams, cited evidence, and risk
  tables. Use whenever the user asks "how does X work," "what calls this method," "trace the flow,"
  "explain this system," "investigate this architecture," "do a deep investigation," "I need an
  investigation report," "full analysis of this system," or any question about codebase structure and
  relationships. Also use when the user wants to understand an unfamiliar subsystem before modifying it.
metadata:
  author: kuozg
  version: "1.0"
---

# unity-investigate

Investigate Unity codebases. Auto-triage into Quick (inline answer) or Deep (report with diagrams).

## Triage

Classify the request before starting work:

| Signal | Mode |
|--------|------|
| Single symbol, method, or class question | **Quick** |
| "How does X work?" / "What calls Y?" | **Quick** |
| Tracing one call chain or data flow | **Quick** |
| User says "quick" / "briefly" / "explain" | **Quick** |
| User says "investigate" / "analyze" / "report" / "audit" | **Deep** |
| System spans 3+ classes or multiple assemblies | **Deep** |
| Pre-refactor audit or onboarding documentation needed | **Deep** |
| User wants a saved document or team-facing output | **Deep** |

When ambiguous, start Quick — escalate to Deep if the answer requires 3+ files or cross-system tracing.

---

## Quick Mode

Answer the question in the fewest tool calls possible.

### Workflow

1. **Parse** — Extract the exact symbol, file, or concept from the question
2. **Find** — `lsp_goto_definition` on the target symbol to locate its declaration
3. **Trace** — `lsp_find_references` or `grep` to follow call chains one level deep
4. **Stop** — Halt the moment the question can be answered; skip unused steps
5. **Reply** — Format as summary + 1-3 typed detail blocks

### Rules

- Stop the moment the question can be answered — speed over ceremony
- Never read an entire file to answer a line-level question
- Prefer `lsp_goto_definition` over `grep` when a symbol name is known
- Inline code snippets only when they directly clarify the answer
- No headers, no preamble — answer starts immediately

### Output

`## {Target} [{type: class|method|event|system}]` followed by a summary sentence, then 1-3 detail bullets.

---

## Deep Mode

Produce a comprehensive investigation report. Load the reference first:
`read_skill_file("unity-investigate", "references/deep-mode.md")`

The reference contains the full deep workflow: scoping, discovery, diagramming, risk assessment, and the mandatory report template. Follow it exactly.

**Output**: Save report to `Documents/Investigations/{SystemName}_{YYYY-MM-DD}.md`

---

## Standards

Load `unity-standards` when answers require convention context. Key references:

- `code-standards/lifecycle.md` — Awake/Start/OnEnable order, coroutine rules
- `code-standards/events.md` — C# events, UnityEvent, SO channels, Action
- `code-standards/dependencies.md` — DI, service locator, constructor injection
- `code-standards/architecture-patterns.md` — state machine, MVC/MVP, command pattern
- `review/architecture-checklist.md` — coupling, SOLID, assembly boundaries
- `plan/investigation-workflow.md` — file tracing, call chains, dependency mapping
- `plan/investigation-template.md` — markdown template for investigation reports

Load via `read_skill_file("unity-standards", "references/<path>")`.
