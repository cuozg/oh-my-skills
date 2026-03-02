# Common Unity Errors

## Error Reference Table

| Exception | Cause | Fix |
|-----------|-------|-----|
| `NullReferenceException` | Missing serialized ref | Assign in Inspector or add `[Required]` check |
| `NullReferenceException` | Destroyed object accessed | Check `obj != null` (uses Unity's lifetime check) |
| `NullReferenceException` | Execution order — ref not set yet | Use `[DefaultExecutionOrder]` or move to `Start()` |
| `MissingReferenceException` | Object destroyed but still referenced | Unsubscribe events in `OnDestroy()`, null out refs |
| `InvalidOperationException` | Collection modified during iteration | Iterate copy: `foreach (var x in list.ToList())` |
| `SerializationException` | Non-serializable field in SO/MB | Add `[System.Serializable]`, or use `ISerializationCallbackReceiver` |
| `StackOverflowException` | Recursive property getter | Don't call property from within its own getter |
| `ArgumentException` | Layer/tag not found | Add layer/tag in Project Settings before use |
| `MissingComponentException` | `GetComponent<T>()` returns null | Add `[RequireComponent(typeof(T))]` to class |
| `UnassignedReferenceException` | Serialized field left empty | Use `OnValidate()` to warn in editor |
| `ExecutionEngineException` | IL2CPP stripped needed code | Add to `link.xml` or `[Preserve]` attribute |
| `TypeLoadException` | Missing assembly reference | Check asmdef references, ensure assembly is included |
| `PlatformNotSupportedException` | API not available on target | Guard with `#if UNITY_[PLATFORM]` or runtime check |
| `EntryPointNotFoundException` | Native plugin missing function | Verify plugin architecture (x86/ARM) matches target |

## Quick Diagnostic Patterns

```csharp
// Guard destroyed objects
if (target == null) return; // Unity overloads == for destroyed check

// Safe GetComponent
if (!TryGetComponent<Rigidbody>(out var rb))
{
    Debug.LogError($"Missing Rigidbody on {name}", this);
    return;
}

// Prevent collection modification
var snapshot = _listeners.ToList();
foreach (var listener in snapshot) listener.OnEvent();

// Execution order fix
[DefaultExecutionOrder(-100)]
public class GameManager : MonoBehaviour { }
```

## Null vs Destroyed

```csharp
// C# null vs Unity null — NOT the same
GameObject go = new GameObject();
Destroy(go);
// go == null        → true  (Unity override)
// go is null        → false (C# check)
// ReferenceEquals(go, null) → false
```

Use `== null` for Unity objects. Use `is null` only for pure C# objects.

## Common Serialization Pitfalls

| Field Type | Serializable? | Fix |
|------------|--------------|-----|
| `private` field | No | Add `[SerializeField]` |
| `public` property | No | Use backing `[SerializeField]` field |
| `Dictionary<K,V>` | No | Use `ISerializationCallbackReceiver` |
| `interface` field | No | Use abstract `ScriptableObject` base |
| `static` field | No | Not supported — use instance field |

## IL2CPP Stripping Issues

```csharp
// Types accessed via reflection get stripped by IL2CPP
// Fix 1: [Preserve] attribute
[UnityEngine.Scripting.Preserve]
public class SaveData { public int score; public string name; }

// Fix 2: link.xml in Assets/
// <linker><assembly fullname="Assembly-CSharp"><type fullname="SaveData" preserve="all"/></assembly></linker>

// Common symptom: JsonUtility.FromJson<T>() returns default values in IL2CPP builds
// but works fine in Editor (Mono)
```
