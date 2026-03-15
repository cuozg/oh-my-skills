# Allocation-Free Cookbook

Ready-to-use patterns for zero-GC hot paths.

## Cached Component Lookups

```csharp
// Cache in Awake — use in Update
private Transform _transform;
private Rigidbody _rb;
private Renderer _renderer;

void Awake()
{
    _transform = transform; // avoid property overhead
    _rb = GetComponent<Rigidbody>();
    _renderer = GetComponent<Renderer>();
}
```

## Allocation-Free Distance Check

```csharp
// ❌ Vector3.Distance allocates nothing but sqrMagnitude avoids sqrt
if (Vector3.Distance(a, b) < range) { }

// ✅ Faster — avoids sqrt
float rangeSqr = range * range;
if ((a - b).sqrMagnitude < rangeSqr) { }
```

## Allocation-Free String Formatting (TMP)

```csharp
// Zero-alloc for TMP_Text — use SetText overloads
tmp.SetText("Level {0}", level);              // int
tmp.SetText("{0:1} HP", health);              // float with 1 decimal
tmp.SetText("{0}/{1}", current, max);         // two values
tmp.SetText("Score: {0:0}", score);           // int formatted as float
```

## Allocation-Free Event Dispatch

```csharp
// ❌ Allocating: params array
public event Action<object[]> OnEvent;

// ✅ Zero-alloc: typed delegates
public event Action<int, float> OnDamage;
public event Action<Vector3> OnMove;

// ✅ For multiple params: use readonly struct
public readonly struct DamageEvent
{
    public readonly int SourceId;
    public readonly float Amount;
    public readonly Vector3 HitPoint;
}
public event Action<DamageEvent> OnDamageDealt;
```

## Allocation-Free Coroutine Yields

```csharp
// ❌ Allocates each call
yield return new WaitForSeconds(1f);
yield return new WaitForEndOfFrame();

// ✅ Cache yield instructions
private static readonly WaitForSeconds Wait1s = new(1f);
private static readonly WaitForEndOfFrame WaitEOF = new();
private static readonly WaitForFixedUpdate WaitFixed = new();

IEnumerator Example()
{
    yield return Wait1s;
    yield return WaitEOF;
}
```

## Allocation-Free Physics Queries

```csharp
// Reusable buffers — allocate once
private readonly Collider[] _overlapBuffer = new Collider[32];
private readonly RaycastHit[] _rayBuffer = new RaycastHit[16];

int FindNearby(Vector3 center, float radius, int mask)
{
    return Physics.OverlapSphereNonAlloc(center, radius, _overlapBuffer, mask);
}

int CastRay(Ray ray, float dist, int mask)
{
    return Physics.RaycastNonAlloc(ray, _rayBuffer, dist, mask);
}
```

## Allocation-Free Iteration Patterns

```csharp
// ❌ foreach on non-List collections can allocate enumerator
foreach (var item in myHashSet) { } // may box enumerator

// ✅ List<T>.ForEach avoids enumerator boxing
// ✅ Or use for-loop on List<T>
for (int i = 0; i < list.Count; i++) Process(list[i]);

// ✅ Dictionary — use struct enumerator
foreach (var kvp in dict) { } // Dictionary<K,V> returns struct enumerator — OK

// ✅ Span<T> for stack-based slicing
Span<int> slice = stackalloc int[8];
```

## Allocation-Free Object Activation

```csharp
// ❌ Instantiate/Destroy every frame
Destroy(obj);
var newObj = Instantiate(prefab);

// ✅ Pool — Get/Release
var obj = _pool.Get();
// ... use obj ...
_pool.Release(obj);

// ✅ Toggle visibility without hierarchy changes
obj.SetActive(false); // cheapest toggle
// or: renderer.enabled = false; // even cheaper if only visual
```

## Sealed MonoBehaviour

```csharp
// ✅ Add sealed to non-inherited MonoBehaviours
// Enables devirtualization — ~5% speedup on virtual method dispatch
public sealed class PlayerController : MonoBehaviour { }
```
