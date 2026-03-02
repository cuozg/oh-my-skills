# Architecture Audit

## Coupling Metrics

| Metric | Threshold | Tool |
|--------|-----------|------|
| Afferent coupling (Ca) | ≤ 10 per class | lsp_find_references |
| Efferent coupling (Ce) | ≤ 8 per class | count `using` + field types |
| Instability (Ce/(Ca+Ce)) | 0.0–1.0 range | calculate per assembly |

## Assembly Boundary Checks

- Each assembly has a `.asmdef` file
- No circular assembly references
- Runtime assemblies never reference Editor assemblies
- Test assemblies reference only their target + test frameworks
- Platform-specific code in platform-named assemblies

## Dependency Direction

```
UI → Application → Domain → Core
     ↓
   Infrastructure
```

- Higher layers depend on lower layers only
- Domain layer has zero Unity dependencies (pure C#)
- Infrastructure implements domain interfaces
- Flag any reverse dependency as **Critical**

## Singleton Audit

| Check | Pass Criteria |
|-------|---------------|
| Count | ≤ 3 singletons total |
| Lifecycle | Paired with `OnDestroy` cleanup |
| Thread safety | `lock` or main-thread assertion |
| Testability | Interface-backed, injectable |
| Scene survival | Explicit `DontDestroyOnLoad` justification |

## Event System Consistency

- Pick ONE pattern per project:

| Pattern | When |
|---------|------|
| C# events/Actions | Tight coupling acceptable |
| ScriptableObject channels | Cross-scene, designer-tunable |
| Static event bus | Global, fire-and-forget |

- Flag mixed patterns as **D-grade** issue
- All subscriptions must have matching unsubscriptions

## Interface Coverage

- Public services expose interfaces
- MonoBehaviour dependencies injected via interface fields
- Minimum 60% interface coverage on service classes

## Circular Dependency Detection

1. Build adjacency graph from `using` directives
2. Run DFS cycle detection
3. Each cycle = **Critical** finding
4. Report: `ClassA → ClassB → ClassC → ClassA`
