# Patterns: Services & Events

## Plain C# Service

```csharp
using System;

namespace YourProject.Combat;

/// <summary>
/// Calculates and applies damage between combatants.
/// </summary>
public sealed class DamageService : IDisposable
{
    private readonly ILogger logger;
    private readonly ICombatState combatState;

    /// <summary>Raised after damage is applied. Passes defender ID and final damage.</summary>
    public event Action<string, int> DamageApplied;

    public DamageService(ILogger logger, ICombatState combatState)
    {
        this.logger = logger;
        this.combatState = combatState;
    }

    public void ApplyDamage(string defenderId, int rawDamage, int defenderArmor)
    {
        if (rawDamage <= 0) return;
        int finalDamage = this.CalculateDamage(rawDamage, defenderArmor);
        this.combatState.ApplyDamage(defenderId, finalDamage);
        this.DamageApplied?.Invoke(defenderId, finalDamage);
        this.logger.Info($"Damage applied: {finalDamage} to {defenderId}");
    }

    public void Dispose() { this.DamageApplied = null; }

    private int CalculateDamage(int rawDamage, int armor) => Math.Max(1, rawDamage - armor);
}
```

Rules: `sealed` class | `readonly` fields | Constructor injection | `IDisposable` for cleanup | `event Action<T>` for notifications | Named methods (not lambdas)

## C# Event Patterns

```csharp
namespace YourProject.Combat;

// Event args: readonly record struct for immutable event data
public readonly record struct AttackExecutedArgs(string AttackerId, string DefenderId, int Damage, int DefenderArmor);
public readonly record struct DamageAppliedArgs(string DefenderId, int FinalDamage);
public readonly record struct UnitDiedArgs(string UnitId);

// Centralized event hub for a domain
public sealed class CombatEvents
{
    public event Action<AttackExecutedArgs> AttackExecuted;
    public event Action<DamageAppliedArgs> DamageApplied;
    public event Action<UnitDiedArgs> UnitDied;
    public event Action GamePaused;

    public void RaiseAttackExecuted(AttackExecutedArgs args) => this.AttackExecuted?.Invoke(args);
    public void RaiseDamageApplied(DamageAppliedArgs args) => this.DamageApplied?.Invoke(args);
    public void RaiseUnitDied(UnitDiedArgs args) => this.UnitDied?.Invoke(args);
    public void RaiseGamePaused() => this.GamePaused?.Invoke();
}
```

Rules: `readonly record struct` for event data | Past-tense naming | Immutable data only | No methods in event args | Named method subscribers
