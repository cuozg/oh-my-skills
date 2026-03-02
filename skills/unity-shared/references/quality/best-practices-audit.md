# Best Practices Audit

## Deprecated API Usage

| Deprecated | Replacement |
|-----------|-------------|
| `OnGUI()` | UI Toolkit or uGUI |
| `WWW` | `UnityWebRequest` |
| `Application.LoadLevel` | `SceneManager.LoadScene` |
| `GUIText` / `GUITexture` | `TextMeshPro` / `Image` |
| `Network.*` (UNet) | Netcode for GameObjects |
| `JsonUtility` limitations | Newtonsoft or custom serializer |

## CompareTag Usage

```csharp
// ✗ Allocates string
if (other.gameObject.tag == "Player")

// ✓ No allocation
if (other.CompareTag("Player"))
```

- Flag every `== "tag"` comparison as **Medium** issue

## Null Check Patterns

```csharp
// ✗ Bypasses Unity's null override
obj?.DoSomething();        // null-conditional
obj ?? fallback;           // null-coalescing

// ✓ Correct for UnityEngine.Object
if (obj != null) obj.DoSomething();
```

- C# `?.` and `??` skip Unity's destroyed-object check
- Use `== null` / `!= null` for all `UnityEngine.Object` types
- Pure C# classes: `?.` and `??` are fine

## Coroutine Management

- Cache `WaitForSeconds` instances (`static readonly`)
- Stop coroutines in `OnDisable` or `OnDestroy`
- Prefer `async/await` with `UniTask` for complex flows
- Never use `StopAllCoroutines()` as cleanup strategy
- Flag `StartCoroutine` in `Update` as **Critical**

## SerializeField

```csharp
// ✗ Public field
public float speed = 5f;

// ✓ Private + SerializeField
[SerializeField] private float _speed = 5f;
```

- All inspector-exposed fields: `[SerializeField] private`
- Use `[field: SerializeField]` for auto-properties
- Add `[Tooltip]` for non-obvious fields
- Add `[Range]` for bounded numeric values

## Event Lifecycle Pairing

| Subscribe In | Unsubscribe In |
|-------------|----------------|
| `Awake` | `OnDestroy` |
| `OnEnable` | `OnDisable` |
| `Start` | `OnDestroy` |

- Every `+=` must have a matching `-=`
- Flag unpaired subscriptions as **High** issue
- Static events: always unsubscribe — leak source

## Platform Guards

```csharp
#if UNITY_EDITOR
    Debug.Log("Editor only");
#endif

#if !UNITY_EDITOR
    Analytics.Send(data);
#endif
```

- Wrap editor-only code in `#if UNITY_EDITOR`
- Wrap platform APIs: `#if UNITY_IOS`, `#if UNITY_ANDROID`
- Use `Application.isEditor` for runtime checks
- Never ship `Debug.Log` in release builds

## Assembly Definition Usage

- Every folder with scripts has an `.asmdef`
- Test assemblies marked as `Test` platform
- Editor assemblies include only `Editor` platform
- Minimize inter-assembly references
- Flag loose scripts in `Assets/` root as **Medium**
