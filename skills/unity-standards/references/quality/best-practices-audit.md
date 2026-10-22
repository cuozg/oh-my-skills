# Best Practices Audit

## Obsolete / Removed APIs (Unity 6)

Compiler signal: `CS0618` (obsolete warning) / `CS0619` (obsolete error).

| Obsolete | Replacement |
|-----------|-------------|
| `Object.FindObjectOfType<T>()` | `FindFirstObjectByType<T>()` (deterministic) or `FindAnyObjectByType<T>()` (faster) |
| `Object.FindObjectsOfType<T>()` | `FindObjectsByType<T>(FindObjectsSortMode.None)` |
| `Rigidbody`/`Rigidbody2D` `.velocity`, `.drag`, `.angularDrag` | `.linearVelocity`, `.linearDamping`, `.angularDamping` |
| `Physics.autoSimulation` / `Physics2D.autoSimulation` | `Physics.simulationMode` / `Physics2D.simulationMode` |
| `Physics2D.*NonAlloc` queries | Overloads taking an array or `List<T>` result |
| URP `ScriptableRenderPass.Execute` / `Configure` / `OnCameraSetup` | `RecordRenderGraph` (old path is Compatibility Mode only) |
| Entities `GameObjectConversionSystem` / `IConvertGameObjectToEntity` | `Baker<T>` (Entities 1.x) |
| Entities `Entities.ForEach` / `Job.WithCode` | `SystemAPI.Query` / `IJobEntity` |
| `com.unity.textmeshpro` package | TextMeshPro ships inside `com.unity.ugui` 2.0 |
| `WWW` | `UnityWebRequest` |
| `Application.LoadLevel` | `SceneManager.LoadScene` |
| `GUIText` / `GUITexture` | `TextMeshPro` / `Image` |
| `Network.*` (UNet) | Netcode for GameObjects or project-specific networking layer |

## Avoid In New Code

| Avoid | Prefer |
|-------|--------|
| `OnGUI()` for production UI | UI Toolkit or uGUI |
| Legacy `UnityEngine.Input` | Input System package (`InputAction`), unless the project standardizes on legacy input |
| Stretching `JsonUtility` past its limits | Newtonsoft or a custom serializer |

## CompareTag Usage

```csharp
// Avoid string-based tag comparisons
if (other.gameObject.tag == "Player")

// Preferred
if (other.CompareTag("Player"))
```

- Flag repeated `== "tag"` comparisons as a medium issue when they are in gameplay hot paths or hide intent.

## Null Check Patterns

```csharp
// Bypasses Unity's destroyed-object null semantics
obj?.DoSomething();
obj ?? fallback;

// Correct for UnityEngine.Object
if (obj != null) obj.DoSomething();
```

- C# `?.` and `??` skip Unity's destroyed-object check.
- Use `== null` / `!= null` for `UnityEngine.Object` types.
- Pure C# classes can use `?.` and `??` normally.

## Coroutine Management

- Cache `WaitForSeconds` instances only when the delay value is stable and reuse is readable.
- Stop or cancel long-lived flows in `OnDisable` or `OnDestroy`.
- Prefer the project's established async stack for complex flows; without one, use `Awaitable` with `destroyCancellationToken`.
- Never use `StopAllCoroutines()` as a blanket cleanup strategy.
- Flag `StartCoroutine` in `Update` as critical.

## SerializeField

```csharp
// Avoid public field just for inspector access
public float speed = 5f;

// Preferred default
[SerializeField] private float _speed = 5f;
public float Speed => _speed;
```

- Inspector-exposed fields should default to `[SerializeField] private`.
- Use `[field: SerializeField]` only when the repo already standardizes on serialized auto-properties.
- Add `[Tooltip]` for non-obvious fields.
- Add `[Range]` or `[Min]` for bounded numeric values.

## Event Lifecycle Pairing

| Subscribe In | Unsubscribe In |
|-------------|----------------|
| `Awake` | `OnDestroy` |
| `OnEnable` | `OnDisable` |
| `Start` | `OnDestroy` |

- Every `+=` should have a matching `-=`.
- Flag unpaired subscriptions as a high issue.
- Static events always need an unsubscribe path.

## Platform Guards

```csharp
#if UNITY_EDITOR
    Debug.Log("Editor only");
#endif

#if !UNITY_EDITOR
    Analytics.Send(data);
#endif
```

- Wrap editor-only code in `#if UNITY_EDITOR`.
- Wrap platform APIs with targeted symbols such as `UNITY_IOS`, `UNITY_ANDROID`, or `UNITY_WEBGL`.
- Use `Application.isEditor` only for runtime branching, not compile-time exclusions.
- Prefer stripping or conditional compilation over shipping noisy debug logging.

## Assembly Definition Usage

- Every meaningful script area should have an `.asmdef`.
- Test assemblies should be marked as test assemblies.
- Editor assemblies should include only `Editor` platform code.
- Minimize inter-assembly references.
- Flag loose scripts in `Assets/` root as a medium issue.
