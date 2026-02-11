# Common Unity Error Patterns

## Table of Contents
- [NullReferenceException](#nullreferenceexception)
- [MissingReferenceException](#missingreferenceexception)
- [IndexOutOfRangeException](#indexoutofrangeexception)
- [InvalidOperationException](#invalidoperationexception)
- [Unity Lifecycle Issues](#unity-lifecycle-issues)
- [Async/Await Pitfalls](#asyncawait-pitfalls)
- [Event Subscription Leaks](#event-subscription-leaks)
- [Serialization Problems](#serialization-problems)

---

## NullReferenceException

### Pattern 1: Unassigned Inspector Reference
```csharp
// ERROR: Reference not assigned in Inspector
[SerializeField] private Transform _target; // Shows as "None" in Inspector

void Update()
{
    transform.LookAt(_target.position); // NullRef if _target not assigned
}
```

**Debug Logs:**
```csharp
void Start()
{
    #if UNITY_EDITOR
    Debug.Log($"<color=cyan>[DEBUG] _target assigned: {_target != null}</color>");
    if (_target == null)
        Debug.LogError($"<color=red>[DEBUG] _target is NULL! Check Inspector assignment on {gameObject.name}</color>");
    #endif
}
```

**Solutions:**
- Add `[RequireComponent]` for mandatory components
- Use `OnValidate()` to catch missing references in Editor
- Add null check with helpful error message

### Pattern 2: GetComponent Returns Null
```csharp
// ERROR: Component doesn't exist on this GameObject
var rb = GetComponent<Rigidbody>();
rb.AddForce(Vector3.up); // NullRef if no Rigidbody
```

**Debug Logs:**
```csharp
var rb = GetComponent<Rigidbody>();
#if UNITY_EDITOR
Debug.Log($"<color=cyan>[DEBUG] GetComponent<Rigidbody> result: {(rb != null ? "found" : "NOT FOUND")} on {gameObject.name}</color>");
#endif
```

**Solutions:**
```csharp
// Option 1: TryGetComponent (Unity 2019.2+)
if (TryGetComponent<Rigidbody>(out var rb))
{
    rb.AddForce(Vector3.up);
}

// Option 2: RequireComponent attribute
[RequireComponent(typeof(Rigidbody))]
public class MyScript : MonoBehaviour { }
```

### Pattern 3: Find Returns Null
```csharp
// ERROR: Object not in scene or inactive
var player = GameObject.Find("Player");
player.GetComponent<Health>().TakeDamage(10); // NullRef if "Player" not found
```

**Debug Logs:**
```csharp
var player = GameObject.Find("Player");
#if UNITY_EDITOR
Debug.Log($"<color=cyan>[DEBUG] GameObject.Find('Player') result: {(player != null ? player.name : "NOT FOUND")}</color>");
Debug.Log($"<color=cyan>[DEBUG] Active GameObjects in scene: {FindObjectsOfType<GameObject>().Length}</color>");
#endif
```

**Solutions:**
- Cache reference in Start/Awake instead of Find in Update
- Use FindWithTag for tagged objects
- Use singleton pattern or dependency injection
- Check if object is inactive (`FindObjectsOfType<T>(true)`)

### Pattern 4: Destroyed Object Access
```csharp
// ERROR: Accessing destroyed object
private Enemy _targetEnemy;

void Update()
{
    if (_targetEnemy != null) // This check passes!
    {
        Attack(_targetEnemy); // But this can still throw
    }
}
```

**Why:** Unity's `== null` check is special but doesn't catch all cases.

**Debug Logs:**
```csharp
#if UNITY_EDITOR
Debug.Log($"<color=cyan>[DEBUG] _targetEnemy: C# null={_targetEnemy is null}, Unity null={_targetEnemy == null}</color>");
#endif
```

**Solutions:**
```csharp
// Use Unity's implicit bool conversion
if (_targetEnemy) 
{
    Attack(_targetEnemy);
}

// Or explicit destroyed check
if (_targetEnemy != null && !_targetEnemy.Equals(null))
{
    Attack(_targetEnemy);
}
```

---

## MissingReferenceException

### Pattern: Async Operation After Destroy
```csharp
async void LoadDataAsync()
{
    var data = await FetchFromServer();
    _text.text = data; // MissingReferenceException if object destroyed during await
}
```

**Debug Logs:**
```csharp
async void LoadDataAsync()
{
    #if UNITY_EDITOR
    Debug.Log($"<color=yellow>[DEBUG] LoadDataAsync START, gameObject active: {gameObject.activeInHierarchy}</color>");
    #endif
    var data = await FetchFromServer();
    #if UNITY_EDITOR
    Debug.Log($"<color=yellow>[DEBUG] LoadDataAsync AFTER await, this == null: {this == null}</color>");
    #endif
    
    if (this == null) return; // Guard
    _text.text = data;
}
```

**Solutions:**
```csharp
// Option 1: Check after await
async void LoadDataAsync()
{
    var data = await FetchFromServer();
    if (this == null) return;
    _text.text = data;
}

// Option 2: Use CancellationToken
private CancellationTokenSource _cts;

void OnEnable() => _cts = new CancellationTokenSource();
void OnDisable() => _cts?.Cancel();

async void LoadDataAsync()
{
    try
    {
        var data = await FetchFromServer(_cts.Token);
        _text.text = data;
    }
    catch (OperationCanceledException) { }
}
```

---

## IndexOutOfRangeException

### Pattern 1: Off-by-One Error
```csharp
for (int i = 0; i <= array.Length; i++) // ERROR: <= instead of <
{
    Process(array[i]); // Throws on last iteration
}
```

**Debug Logs:**
```csharp
#if UNITY_EDITOR
Debug.Log($"<color=lime>[DEBUG] array.Length={array.Length}, loop range: 0 to {array.Length}</color>");
#endif
for (int i = 0; i <= array.Length; i++)
{
    #if UNITY_EDITOR
    Debug.Log($"<color=lime>[DEBUG] Accessing index {i}</color>");
    #endif
    Process(array[i]);
}
```

### Pattern 2: Stale Index from Cached Data
```csharp
private int _selectedIndex;

void OnItemRemoved(int removedIndex)
{
    // _selectedIndex might now be invalid
    Process(_items[_selectedIndex]); // IndexOutOfRange
}
```

**Debug Logs:**
```csharp
void OnItemRemoved(int removedIndex)
{
    #if UNITY_EDITOR
    Debug.Log($"<color=lime>[DEBUG] OnItemRemoved: removedIndex={removedIndex}, _selectedIndex={_selectedIndex}, _items.Count={_items.Count}</color>");
    #endif
    
    if (_selectedIndex >= _items.Count)
    {
        #if UNITY_EDITOR
        Debug.LogWarning($"<color=red>[DEBUG] _selectedIndex {_selectedIndex} is now out of range!</color>");
        #endif
        _selectedIndex = Mathf.Max(0, _items.Count - 1);
    }
}
```

### Pattern 3: Collection Modified During Iteration
```csharp
foreach (var item in _items)
{
    if (ShouldRemove(item))
        _items.Remove(item); // InvalidOperationException
}
```

**Solutions:**
```csharp
// Option 1: Iterate backwards
for (int i = _items.Count - 1; i >= 0; i--)
{
    if (ShouldRemove(_items[i]))
        _items.RemoveAt(i);
}

// Option 2: ToList() copy
foreach (var item in _items.ToList())
{
    if (ShouldRemove(item))
        _items.Remove(item);
}

// Option 3: RemoveAll
_items.RemoveAll(item => ShouldRemove(item));
```

---

## Unity Lifecycle Issues

### Pattern 1: Awake vs Start Order
```csharp
// Script A
void Awake()
{
    _data = LoadData(); // _data ready after Awake
}

// Script B
void Awake()
{
    _scriptA = GetComponent<ScriptA>();
    Use(_scriptA._data); // _data might not be ready yet!
}
```

**Debug Logs:**
```csharp
// Script A
void Awake()
{
    #if UNITY_EDITOR
    Debug.Log($"<color=magenta>[DEBUG] ScriptA.Awake() START, frame={Time.frameCount}</color>");
    #endif
    _data = LoadData();
    #if UNITY_EDITOR
    Debug.Log($"<color=magenta>[DEBUG] ScriptA.Awake() END, _data ready</color>");
    #endif
}

// Script B  
void Awake()
{
    #if UNITY_EDITOR
    Debug.Log($"<color=magenta>[DEBUG] ScriptB.Awake() START, frame={Time.frameCount}</color>");
    #endif
    _scriptA = GetComponent<ScriptA>();
    #if UNITY_EDITOR
    Debug.Log($"<color=cyan>[DEBUG] ScriptA._data is {(_scriptA._data != null ? "ready" : "NULL")}</color>");
    #endif
}
```

**Solutions:**
- Use Script Execution Order settings
- Move cross-component initialization to Start()
- Use events for initialization completion

### Pattern 2: OnEnable Before Start
```csharp
void Start()
{
    _manager = GameManager.Instance; // Initialize here
}

void OnEnable()
{
    _manager.RegisterPlayer(this); // NullRef on first enable!
}
```

**Lifecycle order:** Awake → OnEnable → Start

**Solutions:**
```csharp
void Awake()
{
    _manager = GameManager.Instance; // Move to Awake
}

// Or use a flag
private bool _initialized;

void Start()
{
    _manager = GameManager.Instance;
    _initialized = true;
    _manager.RegisterPlayer(this);
}

void OnEnable()
{
    if (_initialized)
        _manager.RegisterPlayer(this);
}
```

---

## Async/Await Pitfalls

### Pattern 1: Fire-and-Forget Without Error Handling
```csharp
async void Start()
{
    await LoadAsync(); // Exception here is swallowed!
}
```

**Solutions:**
```csharp
async void Start()
{
    try
    {
        await LoadAsync();
    }
    catch (Exception e)
    {
        #if UNITY_EDITOR
        Debug.LogError($"<color=red>[DEBUG] LoadAsync failed: {e}</color>");
        #endif
    }
}
```

### Pattern 2: Deadlock with .Result
```csharp
void Start()
{
    var result = LoadAsync().Result; // DEADLOCK on main thread!
}
```

**Solutions:**
- Never use `.Result` or `.Wait()` on main thread
- Use `async void` for Unity events (Start, Update, etc.)
- Use UniTask for better async support

### Pattern 3: ConfigureAwait Missing
```csharp
async Task LoadAsync()
{
    var data = await httpClient.GetAsync(url); // Resumes on thread pool
    _text.text = data; // ERROR: Not on main thread!
}
```

**Solutions:**
```csharp
// Unity automatically captures context, but be explicit:
var data = await httpClient.GetAsync(url).ConfigureAwait(true);

// Or use UniTask:
await UniTask.SwitchToMainThread();
_text.text = data;
```

---

## Event Subscription Leaks

### Pattern: Subscribe Without Unsubscribe
```csharp
void OnEnable()
{
    GameManager.OnPlayerDied += HandlePlayerDied;
}
// Missing OnDisable unsubscribe!
```

**Debug Logs:**
```csharp
void OnEnable()
{
    #if UNITY_EDITOR
    Debug.Log($"<color=yellow>[DEBUG] {gameObject.name} subscribing to OnPlayerDied</color>");
    #endif
    GameManager.OnPlayerDied += HandlePlayerDied;
}

void OnDisable()
{
    #if UNITY_EDITOR
    Debug.Log($"<color=yellow>[DEBUG] {gameObject.name} unsubscribing from OnPlayerDied</color>");
    #endif
    GameManager.OnPlayerDied -= HandlePlayerDied;
}
```

**Solutions:**
```csharp
void OnEnable()
{
    GameManager.OnPlayerDied += HandlePlayerDied;
}

void OnDisable()
{
    GameManager.OnPlayerDied -= HandlePlayerDied;
}

// Alternative: Use weak events or auto-cleanup patterns
```

---

## Serialization Problems

### Pattern 1: Non-Serializable Field
```csharp
[SerializeField] 
private Dictionary<string, int> _data; // Not serialized!
```

**Debug Logs:**
```csharp
void OnValidate()
{
    #if UNITY_EDITOR
    Debug.Log($"<color=yellow>[DEBUG] _data count in Editor: {_data?.Count ?? -1}</color>");
    #endif
}

void Awake()
{
    #if UNITY_EDITOR
    Debug.Log($"<color=yellow>[DEBUG] _data count at runtime: {_data?.Count ?? -1}</color>");
    #endif
}
```

**Solutions:**
- Use serializable wrapper (SerializableDictionary)
- Use ScriptableObject
- Use JSON serialization

### Pattern 2: Lost References After Play Mode
```csharp
[SerializeField] private Material _material;

void Start()
{
    _material.color = Color.red; // Modifies asset!
}
```

**Solutions:**
```csharp
void Start()
{
    // Create instance to avoid modifying asset
    _material = new Material(_material);
    _material.color = Color.red;
}

void OnDestroy()
{
    if (_material != null)
        Destroy(_material);
}
```
