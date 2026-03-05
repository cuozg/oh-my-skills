# Refactoring Patterns — Safe Multi-File Transforms

## Extract Interface

**When:** Multiple consumers depend on concrete class, or need testability.

```csharp
// Before: consumers depend on AudioManager directly
public sealed class AudioManager : MonoBehaviour { public void PlaySFX(AudioClip clip) { } }

// After: extract IAudioService, consumers depend on interface
public interface IAudioService { void PlaySFX(AudioClip clip); }
public sealed class AudioManager : MonoBehaviour, IAudioService { public void PlaySFX(AudioClip clip) { } }
```

**Steps:** Create interface file → add `: IInterface` to class → update consumer references → verify.

## Extract Class (decompose god class)

**When:** Class exceeds ~200 lines or has 3+ unrelated responsibilities.

```
Before: PlayerController.cs (400 lines — movement + combat + inventory + audio)
After:
  PlayerMovement.cs     ← movement logic
  PlayerCombat.cs       ← attack, damage
  PlayerInventory.cs    ← items, equipment
  PlayerController.cs   ← orchestrates via references to above
```

**Steps:**
1. Identify responsibility groups (fields + methods that cluster together)
2. Create new class per group — move fields and methods
3. Original class holds references, delegates calls
4. Preserve public API on original class (wrapper methods if needed)

## Replace Inheritance with Composition

**When:** Deep inheritance tree, or "is-a" should be "has-a".

```csharp
// Before: FlyingEnemy : Enemy : MonoBehaviour (3-level hierarchy)
// After:
public sealed class Enemy : MonoBehaviour
{
    [SerializeField] private MovementStrategy movement; // SO or interface
    [SerializeField] private AttackStrategy attack;
    private void Update() { movement.Execute(transform); attack.TryAttack(); }
}
```

Use ScriptableObject strategies or interface references injected via inspector.

## Extract ScriptableObject Data

**When:** Config values are hardcoded or duplicated across instances.

```csharp
// Before: magic numbers in MonoBehaviour
[SerializeField] private float speed = 5f, jumpForce = 10f, gravity = -20f;

// After: data in SO
[CreateAssetMenu(menuName = "Config/Movement")]
public sealed class MovementConfig : ScriptableObject
{
    [field: SerializeField] public float Speed { get; private set; } = 5f;
    [field: SerializeField] public float JumpForce { get; private set; } = 10f;
    [field: SerializeField] public float Gravity { get; private set; } = -20f;
}

// Consumer:
[SerializeField] private MovementConfig config;
```

## Migrate to Event-Driven

**When:** Direct method calls create tight coupling between systems.

```csharp
// Before: EnemyAI directly calls UIManager.ShowDamage()
_uiManager.ShowDamage(amount);

// After: raise event, UI subscribes independently
[SerializeField] private GameEvent<float> onDamageDealt;
onDamageDealt.Raise(amount);
// UI subscribes via OnEnable/OnDisable — zero coupling
```

## Refactoring Safety Checklist

- [ ] Identify ALL callers before changing signatures (lsp_find_references)
- [ ] Preserve public API unless explicitly changing it
- [ ] One refactoring type per pass — don't extract + rename + restructure simultaneously
- [ ] If 5+ files affected, create a file change plan before starting
- [ ] Check for serialized field references that may break in Unity Inspector
