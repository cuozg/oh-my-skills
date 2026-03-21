# Refactoring Patterns - Safe Multi-File Transforms

## Extract Interface

**When:** Multiple consumers depend on concrete class, or need testability.

```csharp
// Before: consumers depend on AudioManager directly
public sealed class AudioManager : MonoBehaviour { public void PlaySFX(AudioClip clip) { } }

// After: extract IAudioService, consumers depend on interface
public interface IAudioService { void PlaySFX(AudioClip clip); }
public sealed class AudioManager : MonoBehaviour, IAudioService { public void PlaySFX(AudioClip clip) { } }
```

**Steps:** Create interface file -> add `: IInterface` to class -> update consumer references -> verify.

## Extract Class (Decompose God Class)

**When:** Class exceeds ~200 lines or has 3+ unrelated responsibilities.

```
Before: PlayerController.cs (400 lines - movement + combat + inventory + audio)
After:
  PlayerMovement.cs     <- movement logic
  PlayerCombat.cs       <- attack, damage
  PlayerInventory.cs    <- items, equipment
  PlayerController.cs   <- orchestrates via references to above
```

**Steps:**
1. Identify responsibility groups (fields + methods that cluster together)
2. Create new class per group - move fields and methods
3. Original class holds references and delegates calls
4. Preserve public API on original class (wrapper methods if needed)

## Replace Inheritance With Composition

**When:** Deep inheritance tree, or "is-a" should be "has-a".

```csharp
public sealed class Enemy : MonoBehaviour
{
    [SerializeField] private MovementStrategy movement;
    [SerializeField] private AttackStrategy attack;

    private void Update()
    {
        movement.Execute(transform);
        attack.TryAttack();
    }
}
```

Use ScriptableObject strategies or interface references injected via Inspector.

## Extract ScriptableObject Data

**When:** Config values are hardcoded or duplicated across instances.

```csharp
// Before: magic numbers in MonoBehaviour
[SerializeField] private float speed = 5f, jumpForce = 10f, gravity = -20f;

// After: data in SO
[CreateAssetMenu(menuName = "Config/Movement")]
public sealed class MovementConfig : ScriptableObject
{
    [SerializeField] private float _speed = 5f;
    [SerializeField] private float _jumpForce = 10f;
    [SerializeField] private float _gravity = -20f;

    public float Speed => _speed;
    public float JumpForce => _jumpForce;
    public float Gravity => _gravity;
}

[SerializeField] private MovementConfig config;
```

## Migrate To Event-Driven

**When:** Direct method calls create tight coupling between systems.

```csharp
// Before: EnemyAI directly calls UIManager.ShowDamage()
_uiManager.ShowDamage(amount);

// After: raise event, UI subscribes independently
[SerializeField] private GameEvent<float> onDamageDealt;
onDamageDealt.Raise(amount);
```

UI subscribes via `OnEnable` and `OnDisable` with zero direct dependency on the sender.

## Refactoring Safety Checklist

- [ ] Identify all callers before changing signatures
- [ ] Preserve public API unless explicitly changing it
- [ ] One refactoring type per pass - do not extract, rename, and restructure simultaneously
- [ ] If 5+ files are affected, create a file change plan before starting
- [ ] Check for serialized field references that may break in the Inspector
