# Code Patterns - Unity C# Quick Reference

## MonoBehaviour

```csharp
namespace Project.Feature
{
    public sealed class ThingController : MonoBehaviour
    {
        [Header("Settings")]
        [SerializeField] private float _speed = 5f;
        [SerializeField] private Transform _target;

        private Rigidbody _rb;

        private void Awake() => _rb = GetComponent<Rigidbody>();

        private void FixedUpdate()
        {
            if (_target == null) return;
            var dir = (_target.position - transform.position).normalized;
            _rb.MovePosition(transform.position + dir * (_speed * Time.fixedDeltaTime));
        }
    }
}
```

## ScriptableObject - Data Container

```csharp
[CreateAssetMenu(fileName = "New Item", menuName = "Game/Item Data")]
public sealed class ItemData : ScriptableObject
{
    [SerializeField] private string _displayName;
    [SerializeField] private int _cost;
    [SerializeField] private Sprite _icon;

    public string DisplayName => _displayName;
    public int Cost => _cost;
    public Sprite Icon => _icon;
}
```

For SO event channels -> `read_skill_file("unity-standards", "references/code-standards/events.md")`

## Interface

```csharp
public interface IDamageable
{
    float CurrentHealth { get; }
    void TakeDamage(float amount, Vector3 hitPoint);
}
```

For singleton patterns -> `read_skill_file("unity-standards", "references/code-standards/dependencies.md")`
For coroutines -> `read_skill_file("unity-standards", "references/code-standards/lifecycle.md")`

## UnityEvent

```csharp
[SerializeField] private UnityEvent<int> onScoreChanged;
public void AddScore(int pts) { _score += pts; onScoreChanged?.Invoke(_score); }
```

For component, inspector, and serialization attributes -> `read_skill_file("unity-standards", "references/code-standards/unity-attributes.md")`
