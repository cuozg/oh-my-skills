# Log Format Reference

## Anatomy of a Debug Log

```
#if UNITY_EDITOR
Debug.Log($"<color={color}>[DBG] {ClassName}.{MethodName} {context} | {key}={value}</color>");
#endif
```

### Components

| Part | Required | Description |
|:---|:---|:---|
| `#if UNITY_EDITOR` | YES | Compile-time guard — stripped from builds |
| `<color={color}>` | YES | Color tag per log type |
| `[DBG]` | YES | Prefix for Console filtering |
| `ClassName.MethodName` | YES | Where this log lives |
| Context marker | YES | One of: `ENTER`, `EXIT`, `State:`, `UNEXPECTED:`, or custom label |
| `key=value` | YES | At least one inspected value |
| `</color>` | YES | Close color tag |
| `#endif` | YES | Close compile guard |

## Color Guide

| Color | Log Type | Use For |
|:---|:---|:---|
| `yellow` | Flow | Entry, exit, branch decisions |
| `orange` | State | Variable values, transitions |
| `cyan` | Null Check | Reference validation |
| `magenta` | Lifecycle | Unity lifecycle methods |
| `lime` | Collection | List/array/dict inspection |
| `red` | Error | Unexpected conditions |
| `green` | Event | Subscribe/unsubscribe/invoke |
| `white` | Timing | Frame, time, deltaTime |

## Patterns

### Flow Tracing (method entry + exit)
```csharp
#if UNITY_EDITOR
Debug.Log($"<color=yellow>[DBG] PlayerController.TakeDamage ENTER | damage={damage}, source={source?.name ?? "NULL"}</color>");
#endif

// ... method body ...

#if UNITY_EDITOR
Debug.Log($"<color=yellow>[DBG] PlayerController.TakeDamage EXIT | remainingHealth={_health}</color>");
#endif
```

### Conditional Branch
```csharp
#if UNITY_EDITOR
Debug.Log($"<color=yellow>[DBG] PlayerController.TakeDamage | Path: {(isInvincible ? "BLOCKED (invincible)" : _health <= 0 ? "DEATH" : "DAMAGED")}</color>");
#endif
```

### Null-Safe Field Dump
```csharp
#if UNITY_EDITOR
Debug.Log($"<color=cyan>[DBG] GameManager.Init | " +
    $"_player={(_player != null ? _player.name : "NULL")}, " +
    $"_ui={(_ui != null ? "valid" : "NULL")}, " +
    $"_audio={(_audio != null ? "valid" : "NULL")}</color>");
#endif
```

### Collection Inspection
```csharp
#if UNITY_EDITOR
Debug.Log($"<color=lime>[DBG] InventorySystem.AddItem | " +
    $"before={_items.Count}, adding={item.Name}, " +
    $"afterCapacity={_items.Count < _maxSlots}</color>");
#endif
```

### Lifecycle Sequence
```csharp
#if UNITY_EDITOR
void Awake() { Debug.Log($"<color=magenta>[DBG] {GetType().Name}.Awake | {gameObject.name} id={GetInstanceID()}</color>"); }
void OnEnable() { Debug.Log($"<color=magenta>[DBG] {GetType().Name}.OnEnable | {gameObject.name} active={gameObject.activeInHierarchy}</color>"); }
void Start() { Debug.Log($"<color=magenta>[DBG] {GetType().Name}.Start | {gameObject.name}</color>"); }
void OnDisable() { Debug.Log($"<color=magenta>[DBG] {GetType().Name}.OnDisable | {gameObject.name}</color>"); }
void OnDestroy() { Debug.Log($"<color=magenta>[DBG] {GetType().Name}.OnDestroy | {gameObject.name}</color>"); }
#endif
```

### Coroutine / Async Tracking
```csharp
#if UNITY_EDITOR
Debug.Log($"<color=white>[DBG] DataLoader.LoadAsync START | url={url}, frame={Time.frameCount}</color>");
#endif

var data = await FetchData(url);

#if UNITY_EDITOR
Debug.Log($"<color=white>[DBG] DataLoader.LoadAsync RESUMED | frame={Time.frameCount}, dataNull={data == null}</color>");
#endif
```
