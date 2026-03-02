# log-format-examples.md

## Color Codes

| Color   | Tag               | Use                        |
|---------|-------------------|----------------------------|
| cyan    | `<color=cyan>`    | General trace / entry      |
| yellow  | `<color=yellow>`  | Warnings / unexpected state|
| red     | `<color=red>`     | Errors / failures          |
| green   | `<color=green>`   | Success / completion       |
| white   | `<color=white>`   | Neutral info               |

---

## Standard Method Trace

```csharp
#if UNITY_EDITOR
Debug.Log($"<color=cyan>[DBG] {nameof(MyClass)}.{nameof(MyMethod)}</color> value={myValue}");
#endif
```

## Warning (unexpected-but-handled)

```csharp
#if UNITY_EDITOR
Debug.LogWarning($"<color=yellow>[DBG] {nameof(InventoryManager)}.{nameof(AddItem)}</color> item was null — skipping");
#endif
```

## Error (failure path)

```csharp
#if UNITY_EDITOR
Debug.LogError($"<color=red>[DBG] {nameof(SaveSystem)}.{nameof(Load)}</color> file not found: {filePath}");
#endif
```

## Inside a Loop

```csharp
#if UNITY_EDITOR
Debug.Log($"<color=cyan>[DBG] {nameof(SpawnManager)}.{nameof(SpawnWave)}</color> [{i}] spawned={enemy.name} pos={enemy.transform.position}");
#endif
```

## Coroutine Entry / Exit

```csharp
#if UNITY_EDITOR
Debug.Log($"<color=green>[DBG] {nameof(LoadingScreen)}.{nameof(FadeIn)}</color> START");
// ... yield logic ...
Debug.Log($"<color=green>[DBG] {nameof(LoadingScreen)}.{nameof(FadeIn)}</color> END");
#endif
```

## Notes

- Keep `#if UNITY_EDITOR` guard unless permanent logs are explicitly requested
- Use `nameof()` — rename-safe and IDE-navigable
- Put context values (index, name, ID) after the colored prefix, not inside color tags
