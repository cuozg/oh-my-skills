---
name: unity-code-quick
description: "Fast Unity C# code generation. Receives a code request, generates production-ready C# following unity-code-standards, verifies with diagnostics. Other skills delegate code generation tasks here. Use when: (1) Generating a new MonoBehaviour, ScriptableObject, or plain C# class, (2) Implementing a method, interface, or data model, (3) Writing boilerplate code (events, state, services), (4) Quick code changes delegated from planning/debug/refactor skills, (5) Adding a feature to an existing script. Triggers: 'write code', 'generate class', 'create script', 'implement method', 'add feature', 'quick code', 'code this'."
---

# unity-code-quick — Fast Unity C# Code Generation

Generate production-ready Unity C# code fast. No lengthy investigation — receive request, match codebase conventions, write code, verify.

**Input**: Code request with context (what to create, where it goes, dependencies)
**Output**: C# code following `unity-code-standards`, zero compile errors

## Workflow

### 1. Orient (≤30 seconds)

Read only what's needed to write correct code:
- Target file path and namespace (check nearest `.asmdef` or sibling files)
- If modifying existing file → read it
- If depending on project types → `grep` for interface/class signatures (signatures only, not full files)
- **Skip** if caller already provided full context

### 2. Generate Code

Load and follow `unity-code-standards` for all rules. Apply the matching pattern:

| Need | Pattern Reference |
|------|-------------------|
| New service/class | [SCRIPT_TEMPLATE.md](../unity-code-deep/references/SCRIPT_TEMPLATE.md) — Plain C# Service |
| New MonoBehaviour | [SCRIPT_TEMPLATE.md](../unity-code-deep/references/SCRIPT_TEMPLATE.md) — MonoBehaviour |
| Service + events | [patterns-core.md](../unity-code-deep/references/patterns-core.md) — Service with Events |
| State container | [patterns-core.md](../unity-code-deep/references/patterns-core.md) — State with Read-Only Interface |
| View/UI component | [patterns-core.md](../unity-code-deep/references/patterns-core.md) — MonoBehaviour View |
| Async operations | [patterns-advanced.md](../unity-code-deep/references/patterns-advanced.md) — UniTask |
| State machine | [patterns-advanced.md](../unity-code-deep/references/patterns-advanced.md) — State Machine |
| SO config | [patterns-advanced.md](../unity-code-deep/references/patterns-advanced.md) — ScriptableObject Config |
| Lifecycle cleanup | [patterns-advanced.md](../unity-code-deep/references/patterns-advanced.md) — Cleanup & CTS |

**Quick rules** (from `unity-code-standards` priorities):
- `sealed` classes, `readonly` fields, file-scoped namespaces
- Constructor injection for services, `Initialize()` for MonoBehaviours
- `event Action<T>` for cross-system communication
- `async UniTask` + `CancellationToken` (no coroutines, no `async void`)
- XML docs on public API
- No allocations in Update/hot paths
- Guard clauses over deep nesting

### 3. Verify

1. Write/edit the file(s)
2. `lsp_diagnostics` on every changed file — **zero errors required**
3. If errors → fix immediately, re-verify
4. Report: files created/modified, public API surface

## Anti-Patterns

- ❌ Reading entire codebases before writing one file
- ❌ Creating task lists for single-file changes
- ❌ Loading investigation skills
- ❌ Asking clarifying questions when context is sufficient
- ❌ Skipping `lsp_diagnostics` verification
