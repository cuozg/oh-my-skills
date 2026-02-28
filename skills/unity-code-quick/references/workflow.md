# Workflow

### 1. Orient (≤30 seconds)

Read only what's needed to write correct code:
- Target file path and namespace (check nearest `.asmdef` or sibling files)
- If modifying existing file → read it
- If depending on project types → `grep` for interface/class signatures (signatures only, not full files)
- **Skip** if caller already provided full context

### 2. Generate Code

Load and follow `unity-shared` for all rules. Apply the matching pattern:

| Need | Pattern Reference |
|------|-------------------|
| New service/class | [template.md](../../unity-shared/references/template.md) — Plain C# Service |
| New MonoBehaviour | [template.md](../../unity-shared/references/template.md) — MonoBehaviour |
| Service + events | [patterns-service.md](../../unity-shared/references/patterns-service.md) — Service with Events |
| State container | [patterns-service.md](../../unity-shared/references/patterns-service.md) — State with Read-Only Interface |
| View/UI component | [patterns-service.md](../../unity-shared/references/patterns-service.md) — MonoBehaviour View |
| Async operations | [patterns-async-state.md](../../unity-shared/references/patterns-async-state.md) — UniTask |
| State machine | [patterns-async-state.md](../../unity-shared/references/patterns-async-state.md) — State Machine |
| SO config | [patterns-async-state.md](../../unity-shared/references/patterns-async-state.md) — ScriptableObject Config |
| Lifecycle cleanup | [patterns-async-state.md](../../unity-shared/references/patterns-async-state.md) — Cleanup & CTS |

**Quick rules** (from `unity-shared` priorities):
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
