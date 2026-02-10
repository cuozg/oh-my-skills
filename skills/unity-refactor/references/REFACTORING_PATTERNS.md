---
type: reference
name: Refactoring Patterns
description: Common refactoring patterns for Unity C# codebases with examples.
---

# Unity Refactoring Patterns

## Table of Contents

1. [Extract Method](#1-extract-method)
2. [Extract Class](#2-extract-class)
3. [Replace Inheritance with Composition](#3-replace-inheritance-with-composition)
4. [Introduce Interface](#4-introduce-interface)
5. [Replace Singleton with Dependency Injection](#5-replace-singleton-with-dependency-injection)
6. [Consolidate Event Handling](#6-consolidate-event-handling)
7. [Replace Magic Numbers with Constants](#7-replace-magic-numbers-with-constants)
8. [Extract ScriptableObject Configuration](#8-extract-scriptableobject-configuration)
9. [Replace Coroutine with Async/Awaitable](#9-replace-coroutine-with-asyncawaitable)
10. [Object Pool Extraction](#10-object-pool-extraction)
11. [Reduce MonoBehaviour Bloat](#11-reduce-monobehaviour-bloat)
12. [Flatten Deep Nesting](#12-flatten-deep-nesting)
13. [Unity-Specific Anti-Patterns to Refactor](#13-unity-specific-anti-patterns-to-refactor)

---

## 1. Extract Method

**When**: A method is too long (>30 lines) or has comments describing sections.

```csharp
// BEFORE
void ProcessCombat() {
    // Calculate damage
    float raw = attacker.Power * multiplier;
    float mitigated = raw - defender.Armor;
    float final = Mathf.Max(0, mitigated);
    // Apply damage
    defender.Health -= final;
    if (defender.Health <= 0) defender.Die();
}

// AFTER
void ProcessCombat() {
    float damage = CalculateDamage(attacker, defender, multiplier);
    ApplyDamage(defender, damage);
}
```

---

## 2. Extract Class

**When**: A class has multiple responsibilities (violates SRP).

**Signals**: Class > 500 lines, groups of related fields, methods that only use a subset of fields.

**Unity approach**: Extract to a plain C# class (not MonoBehaviour) when no Unity lifecycle is needed. Use `[Serializable]` if it needs Inspector visibility.

---

## 3. Replace Inheritance with Composition

**When**: Deep MonoBehaviour inheritance hierarchies cause fragility.

```csharp
// BEFORE: Deep hierarchy
class BaseEnemy : MonoBehaviour { }
class FlyingEnemy : BaseEnemy { }
class FlyingBossEnemy : FlyingEnemy { }

// AFTER: Composition
class Enemy : MonoBehaviour {
    [SerializeReference] IMovement movement;
    [SerializeReference] IAttack attack;
}
```

**Benefits**: Flexible combinations, easier testing, no diamond problem.

---

## 4. Introduce Interface

**When**: Concrete dependencies make testing impossible, or swapping implementations is needed.

**Priority targets**: Singletons, managers, data sources, platform-specific code.

```csharp
// BEFORE
class Shop { void Buy() { GameManager.Instance.Currency -= price; } }

// AFTER
interface ICurrencyService { void Deduct(int amount); }
class Shop { ICurrencyService _currency; void Buy() { _currency.Deduct(price); } }
```

---

## 5. Replace Singleton with Dependency Injection

**When**: Singletons create hidden coupling and prevent testing.

**Approach**: Keep the singleton as a service locator initially, then migrate callers to constructor/method injection.

**Unity pattern**: Use `[SerializeField]` references or ScriptableObject-based service locators.

---

## 6. Consolidate Event Handling

**When**: Multiple systems poll for state changes instead of reacting to events.

```csharp
// BEFORE: Polling in Update
void Update() {
    if (player.Health != lastHealth) { UpdateHealthBar(); lastHealth = player.Health; }
}

// AFTER: Event-driven
void OnEnable() { player.OnHealthChanged += UpdateHealthBar; }
void OnDisable() { player.OnHealthChanged -= UpdateHealthBar; }
```

---

## 7. Replace Magic Numbers with Constants

**When**: Numeric literals appear in logic without explanation.

```csharp
// BEFORE
if (speed > 5.5f) PlayAnimation("run");

// AFTER
const float RunThreshold = 5.5f;
if (speed > RunThreshold) PlayAnimation("run");
```

---

## 8. Extract ScriptableObject Configuration

**When**: Hard-coded values should be designer-tunable.

```csharp
// BEFORE
class Weapon : MonoBehaviour {
    float damage = 25f;
    float cooldown = 0.5f;
    float range = 10f;
}

// AFTER
[CreateAssetMenu] class WeaponConfig : ScriptableObject {
    public float damage = 25f;
    public float cooldown = 0.5f;
    public float range = 10f;
}
class Weapon : MonoBehaviour {
    [SerializeField] WeaponConfig config;
}
```

---

## 9. Replace Coroutine with Async/Awaitable

**When**: Coroutines are nested, hard to debug, or need cancellation (Unity 6+).

```csharp
// BEFORE
IEnumerator LoadSequence() {
    yield return StartCoroutine(LoadAssets());
    yield return StartCoroutine(InitSystems());
    OnReady();
}

// AFTER (Unity 6+)
async Awaitable LoadSequence(CancellationToken ct) {
    await LoadAssets(ct);
    await InitSystems(ct);
    OnReady();
}
```

---

## 10. Object Pool Extraction

**When**: Frequent `Instantiate`/`Destroy` causes GC spikes.

Extract pooling into a reusable `ObjectPool<T>` class. Targets: projectiles, VFX, UI elements, enemies.

---

## 11. Reduce MonoBehaviour Bloat

**When**: A single MonoBehaviour handles input, logic, rendering, audio, and UI.

**Split strategy**: One MonoBehaviour per concern. Connect via events or `[SerializeField]` references.

---

## 12. Flatten Deep Nesting

**When**: Methods have 3+ levels of nested if/for/while.

**Techniques**: Guard clauses (early return), extract method, invert conditions.

```csharp
// BEFORE
void Process(Item item) {
    if (item != null) {
        if (item.IsValid) {
            if (item.Quantity > 0) {
                // actual logic
            }
        }
    }
}

// AFTER
void Process(Item item) {
    if (item == null) return;
    if (!item.IsValid) return;
    if (item.Quantity <= 0) return;
    // actual logic
}
```

---

## 13. Unity-Specific Anti-Patterns to Refactor

| Anti-Pattern | Problem | Refactoring |
|:---|:---|:---|
| `GameObject.Find` in Update | O(n) search every frame | Cache reference in `Start`/`Awake` |
| `GetComponent<T>()` in Update | Reflection cost every frame | Cache in field |
| String-based `SendMessage` | No compile-time safety, slow | Use direct method calls or events |
| `new List<>()` in Update | GC allocation every frame | Pre-allocate, reuse collection |
| LINQ in hot paths | Hidden allocations, closures | Manual loops |
| `ToString()` / string concat in Update | GC pressure | `StringBuilder` or avoid |
| Empty `Update()` methods | CPU cost for empty callback | Remove method entirely |
| `[RequireComponent]` missing | Null reference at runtime | Add attribute |
| Hardcoded layer/tag strings | Fragile, no compile check | Use constants or enums |
