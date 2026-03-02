# Code Patterns — Unity C# Quick Reference

## MonoBehaviour

```csharp
namespace Project.Feature
{
    public sealed class ThingController : MonoBehaviour
    {
        [Header("Settings")]
        [SerializeField] private float speed = 5f;
        [SerializeField] private Transform target;

        private Rigidbody _rb;

        private void Awake() => _rb = GetComponent<Rigidbody>();

        private void FixedUpdate()
        {
            if (target == null) return;
            var dir = (target.position - transform.position).normalized;
            _rb.MovePosition(transform.position + dir * (speed * Time.fixedDeltaTime));
        }
    }
}
```

## ScriptableObject — Data + Event Channel

```csharp
[CreateAssetMenu(fileName = "New Item", menuName = "Game/Item Data")]
public sealed class ItemData : ScriptableObject
{
    [field: SerializeField] public string DisplayName { get; private set; }
    [field: SerializeField] public int Cost { get; private set; }
    [field: SerializeField] public Sprite Icon { get; private set; }
}

[CreateAssetMenu(menuName = "Events/Void Event")]
public sealed class VoidEventChannel : ScriptableObject
{
    private System.Action _listeners;
    public void Raise() => _listeners?.Invoke();
    public void Register(System.Action cb) => _listeners += cb;
    public void Unregister(System.Action cb) => _listeners -= cb;
}
```

## Interface

```csharp
public interface IDamageable
{
    float CurrentHealth { get; }
    void TakeDamage(float amount, Vector3 hitPoint);
}
```

## Singleton (scene-safe)

```csharp
public class AudioManager : MonoBehaviour
{
    public static AudioManager Instance { get; private set; }
    private void Awake()
    {
        if (Instance != null && Instance != this) { Destroy(gameObject); return; }
        Instance = this;
        DontDestroyOnLoad(gameObject);
    }
    private void OnDestroy() { if (Instance == this) Instance = null; }
}
```

## Coroutine

```csharp
private IEnumerator FadeOut(CanvasGroup group, float duration)
{
    float elapsed = 0f;
    float start = group.alpha;
    while (elapsed < duration)
    {
        elapsed += Time.deltaTime;
        group.alpha = Mathf.Lerp(start, 0f, elapsed / duration);
        yield return null;
    }
    group.alpha = 0f;
}
```

## UnityEvent

```csharp
[SerializeField] private UnityEvent<int> onScoreChanged;
public void AddScore(int pts) { _score += pts; onScoreChanged?.Invoke(_score); }
```
