---
type: reference
name: Refactoring Patterns
description: Common refactoring patterns for Unity C# codebases with examples.
---

# Unity Refactoring Patterns

## 1. Extract Method

**When**: Method >30 lines or comments describe sections.
```csharp
// BEFORE
void ProcessCombat() {
    float raw = attacker.Power * multiplier;
    float mitigated = raw - defender.Armor;
    float final = Mathf.Max(0, mitigated);
    defender.Health -= final;
    if (defender.Health <= 0) defender.Die();
}
// AFTER
void ProcessCombat() {
    float damage = CalculateDamage(attacker, defender, multiplier);
    ApplyDamage(defender, damage);
}
```

## 2. Extract Class

**When**: Class >500 lines, multiple responsibilities, methods use field subsets. Extract to plain C# class (not MonoBehaviour). Use `[Serializable]` for Inspector visibility.

## 3. Replace Inheritance with Composition

```csharp
// BEFORE: Deep hierarchy
class FlyingBossEnemy : FlyingEnemy : BaseEnemy : MonoBehaviour { }
// AFTER: Composition
class Enemy : MonoBehaviour {
    [SerializeReference] IMovement movement;
    [SerializeReference] IAttack attack;
}
```

## 4. Introduce Interface

**Targets**: Singletons, managers, data sources, platform-specific code.
```csharp
// BEFORE
class Shop { void Buy() { GameManager.Instance.Currency -= price; } }
// AFTER
interface ICurrencyService { void Deduct(int amount); }
class Shop { ICurrencyService _currency; void Buy() { _currency.Deduct(price); } }
```

## 5. Replace Singleton with DI

Keep singleton as service locator initially, then migrate callers to constructor/method injection. Unity: use `[SerializeField]` or ScriptableObject-based service locators.

## 6. Consolidate Event Handling

```csharp
// BEFORE: Polling in Update
void Update() { if (player.Health != lastHealth) { UpdateHealthBar(); lastHealth = player.Health; } }
// AFTER: Event-driven
void OnEnable() { player.OnHealthChanged += UpdateHealthBar; }
void OnDisable() { player.OnHealthChanged -= UpdateHealthBar; }
```

## 7. Replace Magic Numbers

```csharp
const float RunThreshold = 5.5f;
if (speed > RunThreshold) PlayAnimation("run");
```

## 8. Extract ScriptableObject Configuration

```csharp
[CreateAssetMenu] class WeaponConfig : ScriptableObject {
    public float damage = 25f, cooldown = 0.5f, range = 10f;
}
class Weapon : MonoBehaviour { [SerializeField] WeaponConfig config; }
```

## Advanced Anti-Patterns & Strategies

For anti-patterns table, architecture refactoring strategies, and extraction patterns, see REFACTORING_PATTERNS-advanced.md.
