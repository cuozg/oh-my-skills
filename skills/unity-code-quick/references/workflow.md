# unity-code-quick — Workflow

## 1. Load Shared References

Load **ALL** coding references from `unity-shared` before writing any code:

```python
read_skill_file("unity-shared", "references/code/coding-standards.md")
read_skill_file("unity-shared", "references/code/csharp-hygiene.md")
read_skill_file("unity-shared", "references/code/csharp-modern.md")
read_skill_file("unity-shared", "references/code/csharp-linq.md")
read_skill_file("unity-shared", "references/code/csharp-perf.md")
read_skill_file("unity-shared", "references/code/unity-lifecycle.md")
read_skill_file("unity-shared", "references/code/unitask.md")
read_skill_file("unity-shared", "references/code/template.md")
read_skill_file("unity-shared", "references/code/patterns-service.md")
read_skill_file("unity-shared", "references/code/patterns-async-state.md")
read_skill_file("unity-shared", "references/code/editor-patterns.md")
read_skill_file("unity-shared", "references/code/security.md")
read_skill_file("unity-shared", "references/code/architecture.md")
```

## 2. Orient (≤30 seconds)

Read only what's needed to write correct code:
- Target file path and namespace (check nearest `.asmdef` or sibling files)
- If modifying existing file → read it
- If depending on project types → `grep` for interface/class signatures (signatures only, not full files)
- **Skip** if caller already provided full context

## 3. Generate Code

Follow loaded `unity-shared` standards. Apply the matching pattern:

| Need | Pattern Reference |
|------|-------------------|
| New service/class | [template.md](../../unity-shared/references/code/template.md) — Plain C# Service |
| New MonoBehaviour | [template.md](../../unity-shared/references/code/template.md) — MonoBehaviour |
| Service + events | [patterns-service.md](../../unity-shared/references/code/patterns-service.md) — Service with Events |
| State container | [patterns-service.md](../../unity-shared/references/code/patterns-service.md) — State with Read-Only Interface |
| View/UI component | [patterns-service.md](../../unity-shared/references/code/patterns-service.md) — MonoBehaviour View |
| Async operations | [patterns-async-state.md](../../unity-shared/references/code/patterns-async-state.md) — UniTask |
| State machine | [patterns-async-state.md](../../unity-shared/references/code/patterns-async-state.md) — State Machine |
| SO config | [patterns-async-state.md](../../unity-shared/references/code/patterns-async-state.md) — ScriptableObject Config |
| Lifecycle cleanup | [patterns-async-state.md](../../unity-shared/references/code/patterns-async-state.md) — Cleanup & CTS |


## 4. Verify

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
