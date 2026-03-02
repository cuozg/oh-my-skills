# C# Tips — Performance & Safety Micro-Patterns

## Null Safety

```csharp
// Prefer TryGetComponent over GetComponent + null check
if (TryGetComponent<Rigidbody>(out var rb)) rb.AddForce(Vector3.up);

// Cache component refs in Awake, not every frame
private Rigidbody _rb;
private void Awake() => _rb = GetComponent<Rigidbody>();

// Null-conditional for events
onDeath?.Invoke();
```

## Allocation Avoidance

```csharp
// Cache WaitForSeconds
private static readonly WaitForSeconds _wait = new(0.5f);

// Use CompareTag, not == "tag"
if (other.CompareTag("Player")) { }

// NonAlloc physics queries
private readonly Collider[] _hits = new Collider[16];
int count = Physics.OverlapSphereNonAlloc(pos, radius, _hits);

// StringBuilder for string concat in loops
```

## Collections

```csharp
// Pre-allocate when size is known
var items = new List<Item>(capacity: 32);

// Use HashSet for Contains-heavy collections
private readonly HashSet<int> _visited = new();

// Span<T> for stack-only temp arrays (no GC)
Span<RaycastHit> hits = stackalloc RaycastHit[8];
```

## Unity-Specific

```csharp
// Use sqrMagnitude for distance comparisons (skip sqrt)
if ((a - b).sqrMagnitude < threshold * threshold) { }

// Cache transform (already cached in modern Unity, but explicit is clear)
private Transform _transform;
private void Awake() => _transform = transform;

// Time.deltaTime in Update, Time.fixedDeltaTime in FixedUpdate
// Never multiply by fixedDeltaTime inside FixedUpdate (it's already fixed)

// Disable unused Update methods (empty Update still costs)
```

## Serialization

```csharp
// Use [field: SerializeField] with auto-properties
[field: SerializeField] public float Speed { get; private set; }

// Range attribute for clamped values
[SerializeField, Range(0f, 1f)] private float volume = 0.8f;

// Min attribute (Unity 2021.2+)
[SerializeField, Min(0)] private int maxRetries = 3;
```

## Async Patterns (UniTask / Awaitable)

```csharp
// Unity 6+ Awaitable
private async Awaitable FadeAsync(CanvasGroup g, float dur)
{
    float t = 0f;
    while (t < dur)
    {
        t += Time.deltaTime;
        g.alpha = Mathf.Lerp(1f, 0f, t / dur);
        await Awaitable.NextFrameAsync();
    }
}

// Cancellation via destroyCancellationToken
await Awaitable.WaitForSecondsAsync(1f, destroyCancellationToken);
```
