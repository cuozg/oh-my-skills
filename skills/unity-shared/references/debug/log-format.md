# Debug Log Format

## Standard Prefix

All debug logs use `[DBG]` prefix with subsystem tag:

```csharp
Debug.Log($"[DBG][Player] Health changed: {_hp}");
Debug.LogWarning($"[DBG][AI] No path found for {agent.name}");
Debug.LogError($"[DBG][Save] Failed to write: {path}");
```

## Color Tags by Level

| Level | Color | Tag |
|-------|-------|-----|
| `Debug.Log` | cyan | `<color=cyan>[DBG]</color>` |
| `Debug.LogWarning` | yellow | `<color=yellow>[WRN]</color>` |
| `Debug.LogError` | red | `<color=red>[ERR]</color>` |

```csharp
Debug.Log($"<color=cyan>[DBG][{GetType().Name}]</color> {msg}");
```

## Editor-Only Guard

```csharp
#if UNITY_EDITOR
Debug.Log($"[DBG][Physics] Raycast hit: {hit.collider.name}");
#endif
```

## Conditional Attribute

```csharp
[System.Diagnostics.Conditional("UNITY_EDITOR")]
static void EditorLog(string msg) => Debug.Log($"<color=cyan>[DBG]</color> {msg}");
```

## Static Helper Class

```csharp
public static class Dbg
{
    [System.Diagnostics.Conditional("UNITY_EDITOR")]
    public static void Log(string tag, string msg, Object ctx = null)
        => Debug.Log($"<color=cyan>[DBG][{tag}]</color> {msg}", ctx);

    [System.Diagnostics.Conditional("UNITY_EDITOR")]
    public static void Warn(string tag, string msg, Object ctx = null)
        => Debug.LogWarning($"<color=yellow>[WRN][{tag}]</color> {msg}", ctx);

    [System.Diagnostics.Conditional("UNITY_EDITOR")]
    public static void Err(string tag, string msg, Object ctx = null)
        => Debug.LogError($"<color=red>[ERR][{tag}]</color> {msg}", ctx);
}
```

## Context Object (Click-to-Select)

Pass `this` or any `UnityEngine.Object` as context — clicking the log entry selects it in Hierarchy:

```csharp
Debug.Log("Taking damage", this);           // selects this GO
Debug.Log("Spawned", spawnedObject);         // selects spawned GO
Debug.LogError("Missing ref", gameObject);   // selects parent GO
```

## Usage Examples

```csharp
Dbg.Log("Inventory", $"Added {item.name} x{count}", this);
Dbg.Warn("Pool", $"%.Pool %.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.%.expanded to {_pool.Count}", this);
Dbg.Err("Net", $"Packet lost: seq={seq}", this);
```
