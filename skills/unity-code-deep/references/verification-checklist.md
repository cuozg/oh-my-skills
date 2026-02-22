# Verification Checklist

Run through EVERY item before declaring done.

## Compilation
- [ ] `lsp_diagnostics` on every changed file — zero errors
- [ ] `check_compile_errors` — Unity compilation succeeds
- [ ] No unresolved types or missing `using` statements

## Architecture (unity-code-standards)
- [ ] DI: Constructor injection for services, `Initialize()` method for MonoBehaviours
- [ ] Events: `event Action<T>`, subscribe/unsubscribe paired in OnEnable/OnDisable
- [ ] UniTask: `CancellationToken` on all async methods, no `async void`
- [ ] State: Owned by services, exposed via read-only interface properties
- [ ] ILogger: injected via constructor, no Debug.Log, no `#if` guards, no `?.`, no constructor logging

## Code Quality
- [ ] XML docs on all public API
- [ ] `sealed` classes by default
- [ ] `readonly` fields where applicable
- [ ] File-scoped namespaces
- [ ] No magic numbers — `const` / `static readonly` / `[SerializeField]`
- [ ] Guard clauses, no deep nesting (4+ levels)
- [ ] No dead code or commented-out blocks
- [ ] `[Header]`/`[Tooltip]` on all `[SerializeField]` fields

## Unity Safety
- [ ] Events: subscribe in `OnEnable`/`Initialize`, unsubscribe in `OnDisable`/`Dispose`
- [ ] Components cached in `Awake`, no per-frame `GetComponent`
- [ ] `[FormerlySerializedAs]` on renamed serialized fields
- [ ] Empty callbacks deleted (`Update`, `Start`, `OnGUI`)
- [ ] ScriptableObjects cloned before runtime modification
- [ ] No allocations in hot paths (Update, FixedUpdate)

## Fix Every Violation

If any checklist item fails: fix immediately, re-run diagnostics. Do NOT skip items or leave TODOs.
