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

## ScriptableObject — Data Container

```csharp
[CreateAssetMenu(fileName = "New Item", menuName = "Game/Item Data")]
public sealed class ItemData : ScriptableObject
{
    [field: SerializeField] public string DisplayName { get; private set; }
    [field: SerializeField] public int Cost { get; private set; }
    [field: SerializeField] public Sprite Icon { get; private set; }
}
```

For SO event channels → `read_skill_file("unity-standards", "references/code-standards/events.md")`

## Interface

```csharp
public interface IDamageable
{
    float CurrentHealth { get; }
    void TakeDamage(float amount, Vector3 hitPoint);
}
```

For singleton patterns → `read_skill_file("unity-standards", "references/code-standards/dependencies.md")`
For coroutines → `read_skill_file("unity-standards", "references/code-standards/lifecycle.md")`

## UnityEvent

```csharp
[SerializeField] private UnityEvent<int> onScoreChanged;
public void AddScore(int pts) { _score += pts; onScoreChanged?.Invoke(_score); }
```
