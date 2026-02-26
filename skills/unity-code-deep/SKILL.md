---
name: unity-code-deep
description: "Expert Unity Developer implementation. Write clean, commented, performant C# code following best practices. Use when: creating MonoBehaviours, ScriptableObjects, implementing gameplay features, refactoring for performance or architecture, using Unity 6 features."
---

# unity-code-deep — Expert Unity C# Implementation

Write clean, commented, performant C# code. Investigate before coding, ask when unclear, verify everything compiles. Follow `unity-code-shared` for all coding rules.

**Input**: Feature description, implementation task, or TDD/system doc reference
**Output**: C# scripts following project conventions, zero compile errors.

## Phase 0: Understand Before Coding

**NEVER start coding immediately.** Investigate first:

1. **Read project context** — Search for `AGENTS.md`, TDD docs, system docs via `glob("**/AGENT*.md")`, `glob("**/Documents/**/*.{md,html}")`
2. **Explore codebase** — `grep` for related classes/interfaces, read existing implementations, check `*.asmdef` for module boundaries
3. **Ask if unclear** — Which assembly/namespace? How are dependencies provided? Existing interfaces/base classes? Expected edge cases? **Do NOT guess.**

## Phase 1: Plan Before You Implement

For any task with 2+ files, create tasks and outline:
- **Classes & interfaces** to create or modify
- **Dependencies** each class needs (constructor injection or serialized references)
- **Events** for cross-system communication (`event Action<T>`)
- **Data flow** — who owns state, who reads it, who mutates it

## Phase 2: Implement

Load and follow `unity-code-shared` strictly for all coding rules, anti-patterns, and quality gates.

Every new script follows [SCRIPT_TEMPLATE.md](references/SCRIPT_TEMPLATE.md).

### Code Patterns
Load the relevant pattern file when implementing:

- [patterns-core.md](references/patterns-core.md) — Service with Events, State with Read-Only Interface, MonoBehaviour View
- [patterns-advanced.md](references/patterns-advanced.md) — Async/UniTask, State Machine, ScriptableObject Config, Cleanup & CTS

## Phase 3: Verify
1. `lsp_diagnostics` on every changed file — zero errors
2. `check_compile_errors` — Unity compilation succeeds
3. All `unity-code-shared` rules followed
4. XML docs on public API, `sealed` classes, `readonly` fields
5. No dead code, magic numbers, or deep nesting
Fix every violation immediately. Re-run diagnostics. Do NOT skip items or leave TODOs.

## Reference Files
- [SCRIPT_TEMPLATE.md](references/SCRIPT_TEMPLATE.md) — Starting template for every new script
- [patterns-core.md](references/patterns-core.md) — Service, State, MonoBehaviour patterns
- [patterns-advanced.md](references/patterns-advanced.md) — Async, StateMachine, SO Config, Cleanup