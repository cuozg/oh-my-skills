---
name: log-examples
---

# Log Format Examples

Reference implementations for each log type.

## Flow Logs

```csharp
// Method entry with parameters
#if UNITY_EDITOR
Debug.Log($"<color=yellow>[DBG] ClassName.MethodName ENTER | param1={param1}, param2={param2}</color>");
#endif

// Method exit with return value
#if UNITY_EDITOR
Debug.Log($"<color=yellow>[DBG] ClassName.MethodName EXIT | result={result}</color>");
#endif

// Branch taken
#if UNITY_EDITOR
Debug.Log($"<color=yellow>[DBG] ClassName.MethodName | Taking path: {(condition ? "A" : "B")}</color>");
#endif
```

## State Logs

```csharp
// Variable inspection
#if UNITY_EDITOR
Debug.Log($"<color=orange>[DBG] ClassName.MethodName | _health={_health}, _shield={_shield}, _isDead={_isDead}</color>");
#endif

// State transition
#if UNITY_EDITOR
Debug.Log($"<color=orange>[DBG] ClassName | State: {_previousState} -> {_currentState}</color>");
#endif
```

## Null Check Logs

```csharp
#if UNITY_EDITOR
Debug.Log($"<color=cyan>[DBG] ClassName.MethodName | _target={(_target != null ? _target.name : "NULL")}, _rb={(_rb != null ? "valid" : "NULL")}</color>");
#endif
```

## Lifecycle Logs

```csharp
#if UNITY_EDITOR
Debug.Log($"<color=magenta>[DBG] {GetType().Name}.Awake | gameObject={gameObject.name}, instanceId={GetInstanceID()}</color>");
#endif
```

## Collection Logs

```csharp
#if UNITY_EDITOR
Debug.Log($"<color=lime>[DBG] ClassName.MethodName | _items.Count={_items?.Count ?? -1}, firstItem={(_items?.Count > 0 ? _items[0].ToString() : "empty")}</color>");
#endif
```

## Error Logs

```csharp
#if UNITY_EDITOR
Debug.LogWarning($"<color=red>[DBG] ClassName.MethodName | UNEXPECTED: condition={condition}, expected={expected}</color>");
#endif
```

## Event Logs

```csharp
#if UNITY_EDITOR
Debug.Log($"<color=green>[DBG] ClassName.OnEnable | Subscribing to EventName</color>");
#endif
```

## Timing Logs

```csharp
#if UNITY_EDITOR
Debug.Log($"<color=white>[DBG] ClassName.MethodName | frame={Time.frameCount}, time={Time.time:F3}, dt={Time.deltaTime:F4}</color>");
#endif
```
