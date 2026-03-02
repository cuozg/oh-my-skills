# Coverage Strategy

## What to Test First (Priority Order)

1. **Public API** — every public method gets ≥1 test
2. **State transitions** — valid and invalid transitions
3. **Edge cases** — boundary values, empty collections
4. **Error conditions** — null, invalid, out-of-range
5. **Integration points** — event subscriptions, callbacks

## Boundary Value Analysis

| Boundary | Values to Test |
|----------|---------------|
| Zero | `0` |
| One | `1` |
| Max - 1 | `int.MaxValue - 1` |
| Max | `int.MaxValue` |
| Max + 1 | overflow / clamp behavior |
| Negative | `-1` |
| Empty | `""`, `null`, `Array.Empty<T>()` |

```csharp
[TestCase(0)]
[TestCase(1)]
[TestCase(99)]   // max - 1
[TestCase(100)]  // max
[TestCase(101)]  // over max — expect clamp
[TestCase(-1)]   // negative — expect throw
public void SetHealth_BoundaryValues(int value) { /* ... */ }
```

## Error Conditions

| Input | Expectation |
|-------|-------------|
| `null` reference | `ArgumentNullException` or graceful fallback |
| Empty string | Validate or return default |
| Negative number | Clamp or throw |
| Destroyed Unity object | Return early, log warning |
| Duplicate call | Idempotent — no side effects |

## Unity-Specific Coverage

| Area | What to Test |
|------|-------------|
| Lifecycle order | `Awake` → `OnEnable` → `Start` — refs available when expected |
| Serialization roundtrip | `JsonUtility.ToJson` → `FromJsonOverwrite` — data survives |
| Prefab instantiation | `Instantiate(prefab)` — components present, refs intact |
| Event subscribe/unsubscribe | Subscribe in `OnEnable`, unsubscribe in `OnDisable` — no leaks |
| Scene load/unload | Singleton survives, cleanup happens |
| `GetComponent` | Returns expected type, handles missing gracefully |

```csharp
[Test]
public void Config_SurvivesSerializationRoundtrip()
{
    var original = ScriptableObject.CreateInstance<GameConfig>();
    original.MaxHealth = 100;
    var json = JsonUtility.ToJson(original);
    var restored = ScriptableObject.CreateInstance<GameConfig>();
    JsonUtility.FromJsonOverwrite(json, restored);
    Assert.AreEqual(100, restored.MaxHealth);
    Object.DestroyImmediate(original);
    Object.DestroyImmediate(restored);
}
```

## Coverage Targets

| Layer | Target | Rationale |
|-------|--------|-----------|
| Core logic (pure C#) | 90%+ | No Unity deps, easy to test |
| MonoBehaviour methods | 70%+ | Play mode required for some |
| Editor scripts | 50%+ | Lower priority, harder to automate |
| Integration / E2E | Key paths only | Expensive, cover happy paths |
