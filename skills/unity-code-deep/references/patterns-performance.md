# Patterns: Performance, Error Handling, Cleanup

## Performance

```csharp
// Cache components in Awake — never GetComponent in Update
private Rigidbody rb;
private Camera cam;
private Transform cachedTransform;

private void Awake()
{
    this.rb = GetComponent<Rigidbody>();
    this.cam = Camera.main;
    this.cachedTransform = this.transform;
}

// Zero-alloc hot path — pre-allocated array, manual loop
private readonly RaycastHit[] hits = new RaycastHit[32];

private void Update()
{
    int count = Physics.RaycastNonAlloc(this.cachedTransform.position, Vector3.forward, this.hits);
    int nearCount = 0;
    for (int i = 0; i < count; i++)
    {
        if (this.hits[i].distance < 10f) nearCount++;
    }
}
```

| Avoid                        | Do                                         |
| ---------------------------- | ------------------------------------------ |
| `GetComponent` in Update     | Cache in Awake                             |
| `Camera.main` in loops       | Cache reference                            |
| String concat in Update      | StringBuilder or cache                     |
| `new` in hot paths           | Pool / pre-allocate                        |
| LINQ in Update               | Manual loops                               |
| `Find` / `FindObjectOfType`  | `[SerializeField]` or dependency injection |

## Error Handling

```csharp
// Catch specific exceptions — let OperationCanceledException propagate
public async UniTask<PlayerData?> LoadAsync(string id, CancellationToken ct)
{
    try
    {
        string json = await this.network.GetAsync($"/api/player/{id}", ct);
        return JsonUtility.FromJson<PlayerData>(json);
    }
    catch (OperationCanceledException) { throw; } // Always rethrow
    catch (NetworkException ex)
    {
        this.logger.Error($"Load failed for {id}: {ex.Message}");
        return null;
    }
}
```

Rules: Catch specific types | Rethrow `OperationCanceledException` | Use `ILogger` (not `Debug.LogError`) | No empty catch blocks

## Cleanup

```csharp
/// <summary>Proper resource cleanup for MonoBehaviours.</summary>
public sealed class ManagedView : MonoBehaviour
{
    private CancellationTokenSource cts;
    private IPlayerState playerState;

    public void Initialize(IPlayerState playerState) { this.playerState = playerState; }

    private void OnEnable()
    {
        this.cts = new CancellationTokenSource();
        this.playerState.HealthChanged += this.OnValueChanged;
    }

    private void OnDisable()
    {
        this.cts?.Cancel();
        this.cts?.Dispose();
        this.cts = null;
        this.playerState.HealthChanged -= this.OnValueChanged;
    }

    private void OnDestroy() { /* Dispose native resources, cloned ScriptableObjects */ }
    private void OnValueChanged(int value) { /* handle update */ }
}
```

Rules: Cancel `CancellationTokenSource` in `OnDisable` | Unsubscribe events in `OnDisable` | Dispose native resources in `OnDestroy`
