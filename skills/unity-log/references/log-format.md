# Debug Log Format

## Standard Prefix

All debug logs use `[DBG]` prefix with subsystem tag:

```csharp
Debug.Log(
    $"<color=cyan>[DBG][Player]</color> Health changed\n" +
    $"Health: <color=white>{_hp}</color>");

Debug.LogWarning(
    $"<color=yellow>[WRN][AI]</color> No path found\n" +
    $"Agent: <color=white>{agent.name}</color>");

Debug.LogError(
    $"<color=red>[ERR][Save]</color> Failed to write\n" +
    $"Path: <color=white>{path}</color>");
```

## Color Tags by Level

| Level | Color | Tag |
|-------|-------|-----|
| `Debug.Log` | cyan | `<color=cyan>[DBG]</color>` |
| `Debug.LogWarning` | yellow | `<color=yellow>[WRN]</color>` |
| `Debug.LogError` | red | `<color=red>[ERR]</color>` |

```csharp
Debug.Log(
    $"<color=cyan>[DBG][{GetType().Name}]</color> {msg}\n" +
    $"Value: <color=white>{value}</color>");
```

## Value Highlighting

Color every value that explains the issue or workflow. Keep labels plain so the values stand out.

```csharp
Debug.Log(
    $"<color=cyan>[DBG][Match]</color> Turn decision\n" +
    $"PlayerId: <color=white>{playerId}</color>\n" +
    $"CanMove: <color=lime>{canMove}</color>\n" +
    $"Reason: <color=orange>{reason}</color>",
    this);
```

Use consistent colors when they improve scanning:

| Meaning | Color |
|---------|-------|
| Neutral values | white |
| Success or allowed state | lime |
| Blocked or warning state | orange |
| Failure or invalid state | red |
| Object names or identifiers | cyan |

## One Key-Value Per Line

Do not compress multiple state values into one sentence. Put each key-value pair on its own line, or use table alignment for repeated rows.

```csharp
Debug.Log(
    $"<color=cyan>[DBG][Inventory]</color> Add item decision\n" +
    $"ItemId: <color=cyan>{itemId}</color>\n" +
    $"Quantity: <color=white>{quantity}</color>\n" +
    $"CurrentCount: <color=white>{currentCount}</color>\n" +
    $"Capacity: <color=white>{capacity}</color>\n" +
    $"Accepted: <color=lime>{accepted}</color>",
    this);
```

For repeated comparable values, a compact table is acceptable:

```csharp
Debug.Log(
    $"<color=cyan>[DBG][Rewards]</color> Reward summary\n" +
    $"Slot | ItemId | Amount\n" +
    $"0    | <color=cyan>{firstItemId}</color> | <color=white>{firstAmount}</color>\n" +
    $"1    | <color=cyan>{secondItemId}</color> | <color=white>{secondAmount}</color>",
    this);
```

## Smart Flow Placement

Place logs where they explain the flow without repeating the same information:

- Entry log: external inputs, current state, and important config.
- Decision log: branch result and the values that caused it.
- Outcome log: final state or side effect.

Avoid logging the same key-value set at entry, before every branch, and again at return. If a loop is noisy, log a summary or only the failing item unless every iteration is relevant to the bug.

## Editor-Only Guard

```csharp
#if UNITY_EDITOR
Debug.Log(
    $"<color=cyan>[DBG][Physics]</color> Raycast hit\n" +
    $"Collider: <color=cyan>{hit.collider.name}</color>",
    this);
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
Dbg.Log(
    "Inventory",
    $"Added item\n" +
    $"Item: <color=cyan>{item.name}</color>\n" +
    $"Count: <color=white>{count}</color>",
    this);

Dbg.Warn(
    "Pool",
    $"Pool expanded\n" +
    $"PoolSize: <color=orange>{_pool.Count}</color>",
    this);

Dbg.Err(
    "Net",
    $"Packet lost\n" +
    $"Sequence: <color=red>{seq}</color>",
    this);
```
