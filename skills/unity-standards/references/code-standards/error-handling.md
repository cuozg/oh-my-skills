# Error Handling

## Narrow Try/Catch

```csharp
// ✅ Catch specific exceptions, minimal scope
public SaveData LoadSave(string path)
{
    try
    {
        var json = File.ReadAllText(path);
        return JsonUtility.FromJson<SaveData>(json);
    }
    catch (FileNotFoundException)
    {
        Debug.LogWarning($"Save file not found: {path}");
        return new SaveData();
    }
    catch (System.Exception ex) { Debug.LogException(ex); return new SaveData(); }
}

// ❌ Never swallow exceptions silently
try { DoSomething(); }
catch { } // NO — hides bugs
```

## Debug Logging Levels

```csharp
Debug.Log("Game started");                                  // info — normal flow
Debug.LogWarning("Config missing, using defaults");         // recoverable issue
Debug.LogError($"Failed to spawn enemy at {position}");     // broke, can continue
try { riskyOp(); }
catch (System.Exception ex) { Debug.LogException(ex, this); } // preserves stack trace
```

## Debug.Assert for Invariants

```csharp
void Awake()
{
    _rb = GetComponent<Rigidbody>();
    Debug.Assert(_rb != null, "Missing Rigidbody", this);
    Debug.Assert(_maxHealth > 0, $"Invalid MaxHealth: {_maxHealth}", this);
}

void SetWave(int index)
{
    Debug.Assert(index >= 0 && index < _waves.Length, $"Wave index OOB: {index}");
}
```

## Conditional Compilation

```csharp
#if UNITY_EDITOR
void OnValidate()
{
    if (_speed < 0) Debug.LogWarning("Speed is negative", this);
    if (_prefab == null) Debug.LogError("Prefab not assigned", this);
}
#endif

// Conditional attribute — call stripped from non-editor builds
[System.Diagnostics.Conditional("UNITY_EDITOR")]
void DebugDrawPath(Vector3[] points)
{
    for (int i = 0; i < points.Length - 1; i++)
        Debug.DrawLine(points[i], points[i + 1], Color.red, 2f);
}
```

## Fail-Fast Patterns

```csharp
// Throw on invalid args in constructors/factories
public static Projectile Create(ProjectileConfig config)
{
    if (config == null) throw new System.ArgumentNullException(nameof(config));
    if (config.Speed <= 0) throw new System.ArgumentOutOfRangeException(nameof(config.Speed));
    var proj = Instantiate(config.Prefab);
    proj.Init(config);
    return proj;
}

// Guard clause — return early for recoverable cases
public void Heal(float amount)
{
    if (amount <= 0f) return;
    if (!_isAlive) return;
    _health = Mathf.Min(_health + amount, _maxHealth);
}
```
