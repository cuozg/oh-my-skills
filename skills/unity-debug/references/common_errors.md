# Common Unity Error Patterns

## NullReferenceException

### Unassigned Inspector Reference
```csharp
[SerializeField] private Transform _target; // NullRef if not assigned
```
**Fix**: `[RequireComponent]`, `OnValidate()` null checks, null guard with error msg

### GetComponent Returns Null
```csharp
// Use TryGetComponent (2019.2+)
if (TryGetComponent<Rigidbody>(out var rb)) rb.AddForce(Vector3.up);
// Or: [RequireComponent(typeof(Rigidbody))]
```

### Find Returns Null
- Cache in Start/Awake, don't Find in Update
- Use FindWithTag, singleton, or DI
- Inactive objects: `FindObjectsOfType<T>(true)`

### Destroyed Object Access
```csharp
// Unity's == null is special. Use implicit bool:
if (_targetEnemy) Attack(_targetEnemy);
```

## MissingReferenceException

### Async Operation After Destroy
```csharp
// Option 1: Guard after await
async void LoadDataAsync() {
    var data = await FetchFromServer();
    if (this == null) return;
    _text.text = data;
}

// Option 2: CancellationToken
private CancellationTokenSource _cts;
void OnEnable() => _cts = new CancellationTokenSource();
void OnDisable() => _cts?.Cancel();

async void LoadDataAsync() {
    try { var data = await FetchFromServer(_cts.Token); _text.text = data; }
    catch (OperationCanceledException) { }
}
```

## IndexOutOfRangeException

### Off-by-One
`i <= array.Length` → should be `i < array.Length`

### Stale Index After Removal
Clamp: `_selectedIndex = Mathf.Max(0, _items.Count - 1);`

### Collection Modified During Iteration
```csharp
// Iterate backwards
for (int i = _items.Count - 1; i >= 0; i--)
    if (ShouldRemove(_items[i])) _items.RemoveAt(i);
// Or: _items.RemoveAll(item => ShouldRemove(item));
```

## Unity Lifecycle Issues

### Awake vs Start Order
Cross-component init in Awake is order-dependent. **Fix**: Move to Start() or use Script Execution Order.

### OnEnable Before Start
Lifecycle: Awake → OnEnable → Start. References set in Start() are null during first OnEnable.
```csharp
void Awake() { _manager = GameManager.Instance; } // Move init to Awake
// Or use _initialized flag pattern
```

## Async/Await Pitfalls

- **Fire-and-forget**: Wrap `async void Start()` body in try/catch
- **Deadlock**: Never `.Result` or `.Wait()` on main thread
- **Threading**: After `await httpClient.GetAsync()`, may not be on main thread. Use `ConfigureAwait(true)` or UniTask

## Event Subscription Leaks

Always pair subscribe/unsubscribe:
```csharp
void OnEnable() => GameManager.OnPlayerDied += HandlePlayerDied;
void OnDisable() => GameManager.OnPlayerDied -= HandlePlayerDied;
```

## Serialization Problems

- **Dictionary not serialized**: Use SerializableDictionary, ScriptableObject, or JSON
- **Material modified in Play Mode**: Create instance: `_material = new Material(_material);` + destroy in OnDestroy
