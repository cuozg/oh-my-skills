# Debug Log Reference

## Log Anatomy

```
#if UNITY_EDITOR
Debug.Log($"<color={color}>[DBG] {ClassName}.{MethodName} {context} | {key}={value}</color>");
#endif
```

Every log requires: `#if UNITY_EDITOR` wrapper, `<color=X>` tag, `[DBG]` prefix, `ClassName.MethodName` scope, at least one `key=value` pair.

## Color Guide

| Color     | Type       | When                                    |
| :-------- | :--------- | :-------------------------------------- |
| `yellow`  | Flow       | Method entry/exit, branch taken         |
| `orange`  | State      | Variable values, state transitions      |
| `cyan`    | Null Check | Reference validation                    |
| `magenta` | Lifecycle  | Awake, OnEnable, Start, OnDestroy       |
| `lime`    | Collection | List/array counts, element inspection   |
| `red`     | Error      | Unexpected conditions, fallthrough      |
| `green`   | Event      | Subscribe/unsubscribe/invoke            |
| `white`   | Timing     | Frame count, deltaTime, timestamps      |

## Examples

**Flow**: `Debug.Log($"<color=yellow>[DBG] PlayerController.TakeDamage ENTER | damage={damage}, source={source?.name ?? "NULL"}</color>");`

**State**: `Debug.Log($"<color=orange>[DBG] PlayerController | State: {_previousState} -> {_currentState}</color>");`

**Null Check**: `Debug.Log($"<color=cyan>[DBG] GameManager.Init | _player={(_player != null ? _player.name : "NULL")}, _ui={(_ui != null ? "valid" : "NULL")}</color>");`

**Lifecycle**: `Debug.Log($"<color=magenta>[DBG] {GetType().Name}.Awake | {gameObject.name} id={GetInstanceID()}</color>");`

**Collection**: `Debug.Log($"<color=lime>[DBG] InventorySystem.AddItem | count={_items.Count}, adding={item.Name}</color>");`

**Error**: `Debug.LogWarning($"<color=red>[DBG] GameManager.Update | UNEXPECTED: state={_state}, expected=Running</color>");`

**Event**: `Debug.Log($"<color=green>[DBG] PlayerHealth.OnEnable | Subscribing to OnDamage</color>");`

**Timing**: `Debug.Log($"<color=white>[DBG] DataLoader.LoadAsync START | url={url}, frame={Time.frameCount}</color>");`

**Branch**: `Debug.Log($"<color=yellow>[DBG] PlayerController.TakeDamage | Path: {(isInvincible ? "BLOCKED" : _health <= 0 ? "DEATH" : "DAMAGED")}</color>");`

**Async**: `Debug.Log($"<color=white>[DBG] DataLoader.LoadAsync RESUMED | frame={Time.frameCount}, dataNull={data == null}</color>");`

## Response Template

Use this exact structure for every response. No prose, no preamble.

```
## Debug Logs for `{ClassName}.{MethodName}` [{purpose}]

{1-2 sentences: what these logs will reveal}

### {FileNameA}.cs

**Insert at line {N}** (before `{statement}`):
‍```csharp
#if UNITY_EDITOR
Debug.Log($"<color={color}>[DBG] ...</color>");
#endif
‍```

**Insert at line {M}** (after `{statement}`):
‍```csharp
#if UNITY_EDITOR
Debug.Log($"<color={color}>[DBG] ...</color>");
#endif
‍```

### {FileNameB}.cs (if multi-file)
...same pattern...

---
**Log summary**: {N} logs across {M} files — filter by `[DBG]` in Console
**What to look for**: {specific patterns or values the user should watch for}
```

## Template Rules

- One code block per insertion point. Never batch multiple insertions into one block.
- Exact file path and line number for each insertion point.
- Group by file, order by execution flow within each file.
- `{purpose}` = one of: flow trace, state inspection, null check, lifecycle, event tracking, timing.
- `{statement}` = actual code line near insertion point for context.
- Multi-file: add `### FileName.cs` section per file.
