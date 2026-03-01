# C# Performance — Unity Patterns

## 1. Memory & Allocations
```csharp
// ✅ Cache fields, avoid hot path allocations
private readonly List<Collider> _hitResults = new();
private readonly StringBuilder _sb = new(256); // ✅ StringBuilder for loops
private readonly WaitForSeconds _waitOne = new(1f);

// ✅ ArrayPool & stackalloc for temp buffers
Span<int> temp = stackalloc int[16];
var buffer = ArrayPool<byte>.Shared.Rent(1024);
try { Process(buffer.AsSpan(0, 1024)); }
finally { ArrayPool<byte>.Shared.Return(buffer); }

// ✅ Pre-size collections when capacity is known
var results = new List<Player>(players.Count);
var lookup = new Dictionary<string, Player>(expectedCount);

// ✅ Cache delegates to avoid closure allocations
private readonly Action<int> _cachedCallback; // assign in ctor
items.ForEach(static item => Process(item));  // static lambda (no capture)
```

## 2. Structs, Boxing & Dictionaries
```csharp
// ✅ Dictionary lookups
if (dict.TryGetValue(key, out var val)) { } // single lookup, prevents double hash
var val2 = dict.GetValueOrDefault(key, defaultVal); // branching-free fallback

// ✅ readonly struct & record struct for data carriers
public readonly record struct HitData(Vector3 Point, float Distance);

// ✅ Generic constraints & IEquatable<T> to prevent boxing in dictionary keys
void Process<T>(T value) where T : struct { }
public readonly struct PlayerId : IEquatable<PlayerId> {
    public readonly int Value;
    public bool Equals(PlayerId other) => Value == other.Value;
    public override bool Equals(object? obj) => obj is PlayerId other && Equals(other);
    public override int GetHashCode() => Value;
}
```

## 3. Unity API & Update Optimizations
```csharp
// ✅ Cache Transform & avoid GetComponent in hot paths
private Transform _tf;
private void Awake() => _tf = transform;

void Update() {
    if (other.TryGetComponent<Enemy>(out var enemy)) { } // ✅ TryGetComponent avoids null check allocs
}

// ✅ Physics NonAlloc (❌ avoid Physics.RaycastAll which allocates arrays)
private readonly Collider[] _overlapBuffer = new Collider[32];
private readonly RaycastHit[] _raycastBuffer = new RaycastHit[32];
int count = Physics.OverlapSphereNonAlloc(pos, radius, _overlapBuffer);
int hits = Physics.RaycastNonAlloc(ray, _raycastBuffer, dist);
```

## 4. Jobs, Burst & NativeContainers
```csharp
// ✅ Allocators: Temp (1 frame), TempJob (4 frames), Persistent (manual lifecycle)
var inputs = new NativeArray<float>(100, Allocator.TempJob); // Or NativeList<T>
var outputs = new NativeArray<float>(100, Allocator.TempJob);

[BurstCompile] // ✅ Unity.Mathematics vs Mathf, NO managed types, NO try/catch
public struct ComputeJob : IJobParallelFor { // Or IJob for sequential
    [ReadOnly] public NativeArray<float> Inputs;
    [WriteOnly] public NativeArray<float> Outputs;
    
    public void Execute(int i) {
        Outputs[i] = math.sqrt(Inputs[i]); 
        LogDebug("Computed"); 
    }

    [BurstDiscard] // ✅ Stripped from Burst, runs in managed fallback only
    private void LogDebug(string msg) => Debug.Log(msg);
}

// ✅ Schedule, Complete & Dispose pattern with JobHandle
var job = new ComputeJob { Inputs = inputs, Outputs = outputs };
JobHandle handle = job.Schedule(100, batchSize: 64); // ✅ Tune batchSize to workload
handle.Complete();
inputs.Dispose();
outputs.Dispose(); // Alternatively: inputs.Dispose(handle);
```

## 5. Profiling
```csharp
// ✅ Static ProfilerMarker for zero-allocation scopes
static readonly ProfilerMarker s_Marker = new("MySystem.Process");
void ProcessData() {
    using (s_Marker.Auto()) { /* hot path code */ }
}
```