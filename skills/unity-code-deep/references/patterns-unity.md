# Patterns: State Machine, SO Config, Object Pool

## State Machine

```csharp
namespace YourProject.Character;

public enum CharacterState { Idle, Walking, Jumping, Attacking }

/// <summary>Simple state machine with enter/exit callbacks.</summary>
public sealed class CharacterStateMachine
{
    private CharacterState currentState;
    public CharacterState CurrentState => this.currentState;

    public void ChangeState(CharacterState newState)
    {
        if (this.currentState == newState) return;
        this.ExitState(this.currentState);
        this.currentState = newState;
        this.EnterState(newState);
    }

    private void ExitState(CharacterState state) { /* cleanup per state */ }
    private void EnterState(CharacterState state) { /* setup per state */ }
}
```

## ScriptableObject Config

```csharp
using UnityEngine;

namespace YourProject.Config;

/// <summary>Character stats configuration. Clone before runtime modification.</summary>
[CreateAssetMenu(menuName = "Game/Character Stats")]
public sealed class CharacterStats : ScriptableObject
{
    [Header("Combat")]
    [Tooltip("Base damage per attack")]
    [SerializeField] private int baseDamage = 10;
    [Tooltip("Seconds between attacks")]
    [SerializeField] private float attackCooldown = 0.5f;

    [Header("Movement")]
    [Tooltip("Movement speed in units per second")]
    [SerializeField] private float moveSpeed = 5f;

    public int BaseDamage => this.baseDamage;
    public float AttackCooldown => this.attackCooldown;
    public float MoveSpeed => this.moveSpeed;
}
// Usage: clone before runtime modification
// private CharacterStats runtime;
// void Awake() => runtime = Instantiate(baseStats);
// void OnDestroy() { if (runtime) Destroy(runtime); }
```

## Object Pool

```csharp
using UnityEngine;
using UnityEngine.Pool;

namespace YourProject.Combat;

/// <summary>Pool for projectile instances to avoid GC allocations.</summary>
public sealed class ProjectilePool : MonoBehaviour
{
    [Header("Pool Configuration")]
    [Tooltip("Prefab to pool")]
    [SerializeField] private Projectile prefab;
    [Tooltip("Initial pool capacity")]
    [SerializeField] private int capacity = 20;
    [Tooltip("Maximum pool size")]
    [SerializeField] private int maxSize = 100;

    private ObjectPool<Projectile> pool;

    private void Awake()
    {
        this.pool = new ObjectPool<Projectile>(
            createFunc: () => Instantiate(this.prefab),
            actionOnGet: p => p.gameObject.SetActive(true),
            actionOnRelease: p => p.gameObject.SetActive(false),
            actionOnDestroy: p => Destroy(p.gameObject),
            defaultCapacity: this.capacity,
            maxSize: this.maxSize);
    }

    public Projectile Get() => this.pool.Get();
    public void Return(Projectile p) => this.pool.Release(p);
}
```
