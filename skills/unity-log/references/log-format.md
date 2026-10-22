# Debug Log Format

## Standard Prefix

Every generated trace starts with a colored `[DBG]` tag, then `Class.Method`, so all
temporary logs can be found and removed by searching `[DBG]`. The level comes from the
`Debug` method and the tag color. Always pass `this` (or another `UnityEngine.Object`)
as context.

```csharp
Debug.Log(
    $"<color=cyan>[DBG]</color> {nameof(PlayerHealth)}.{nameof(TakeDamage)}\n" +
    $"Health: <color=white>{_hp}</color>",
    this);

Debug.LogWarning(
    $"<color=yellow>[DBG]</color> {nameof(EnemyAI)}.{nameof(FindPath)} no path found\n" +
    $"Agent: <color=cyan>{agent.name}</color>",
    this);

Debug.LogError(
    $"<color=red>[DBG]</color> {nameof(SaveSystem)}.{nameof(Write)} failed\n" +
    $"Path: <color=red>{path}</color>",
    this);
```

## Color Tags by Level

| Level | Use | Tag |
|-------|-----|-----|
| `Debug.Log` | Trace | `<color=cyan>[DBG]</color>` |
| `Debug.LogWarning` | Unexpected but handled | `<color=yellow>[DBG]</color>` |
| `Debug.LogError` | Failure | `<color=red>[DBG]</color>` |

## Value Highlighting

Color every value that explains the issue or workflow. Keep labels plain so the values stand out.

| Meaning | Color |
|---------|-------|
| Neutral values | white |
| Success or allowed state | lime |
| Blocked or warning state | orange |
| Failure or invalid state | red |
| Object names or identifiers | cyan |

## One Key-Value Per Line

Put each key-value pair on its own line with `\n`.

```csharp
Debug.Log(
    $"<color=cyan>[DBG]</color> {nameof(Inventory)}.{nameof(AddItem)} decision\n" +
    $"ItemId: <color=cyan>{itemId}</color>\n" +
    $"Quantity: <color=white>{quantity}</color>\n" +
    $"Capacity: <color=white>{capacity}</color>\n" +
    $"Accepted: <color=lime>{accepted}</color>",
    this);
```

For repeated comparable values, a compact table is acceptable:

```csharp
Debug.Log(
    $"<color=cyan>[DBG]</color> {nameof(RewardService)}.{nameof(Grant)} summary\n" +
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

Log each key-value set once per flow. For noisy loops, log one summary (count,
first/last, or the failing item) unless every iteration is relevant to the bug.

## Editor-Only Guard

Wrap inline snippets in `#if UNITY_EDITOR` so they never ship:

```csharp
#if UNITY_EDITOR
Debug.Log(
    $"<color=cyan>[DBG]</color> {nameof(Projectile)}.{nameof(OnHit)}\n" +
    $"Collider: <color=cyan>{hit.collider.name}</color>",
    this);
#endif
```

## Static Helper (Optional)

When the project already has a helper, or many traces are needed, `[Conditional]`
strips the call and its argument evaluation from non-Editor builds, replacing the
`#if` guard. `[HideInCallstack]` hides the helper frame from the Console callstack
when Console > Strip logging callstack is enabled.

```csharp
using System.Diagnostics;
using UnityEngine;
using Debug = UnityEngine.Debug;

public static class Dbg
{
    [Conditional("UNITY_EDITOR"), HideInCallstack]
    public static void Log(string msg, Object ctx)
        => Debug.Log($"<color=cyan>[DBG]</color> {msg}", ctx);

    [Conditional("UNITY_EDITOR"), HideInCallstack]
    public static void Warn(string msg, Object ctx)
        => Debug.LogWarning($"<color=yellow>[DBG]</color> {msg}", ctx);

    [Conditional("UNITY_EDITOR"), HideInCallstack]
    public static void Err(string msg, Object ctx)
        => Debug.LogError($"<color=red>[DBG]</color> {msg}", ctx);
}

Dbg.Log(
    $"{nameof(EnemySpawner)}.{nameof(ExpandPool)}\n" +
    $"PoolSize: <color=orange>{_pool.Count}</color>",
    this);
```

## Context Object (Click-to-Select)

Pass `this` or any `UnityEngine.Object` as context; clicking the Console entry pings it
in the Hierarchy/Project window:

```csharp
Debug.Log("<color=cyan>[DBG]</color> ...", this);           // this component's GameObject
Debug.Log("<color=cyan>[DBG]</color> ...", spawnedObject);  // the spawned object
```
