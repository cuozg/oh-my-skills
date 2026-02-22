# Patterns: State & MonoBehaviour

## State Management (Interface-Based)

```csharp
using System;

namespace YourProject.Player;

/// <summary>Read-only interface for player data — exposed to consumers.</summary>
public interface IPlayerState
{
    int Health { get; }
    int Score { get; }
    bool IsAlive { get; }
    event Action<int> HealthChanged;
    event Action<int> ScoreChanged;
}

/// <summary>Owns and mutates player state. Registered as singleton service.</summary>
public sealed class PlayerState : IPlayerState, IDisposable
{
    private int health = 100;
    private int score;

    public int Health => this.health;
    public int Score => this.score;
    public bool IsAlive => this.health > 0;

    public event Action<int> HealthChanged;
    public event Action<int> ScoreChanged;

    public void ApplyDamage(int amount)
    {
        if (amount <= 0) return;
        this.health = Math.Max(0, this.health - amount);
        this.HealthChanged?.Invoke(this.health);
    }

    public void AddScore(int points)
    {
        if (points <= 0) return;
        this.score += points;
        this.ScoreChanged?.Invoke(this.score);
    }

    public void Dispose() { this.HealthChanged = null; this.ScoreChanged = null; }
}
```

Rules: State owned by service class | Read-only interface for consumers | `event Action<T>` for change notifications | `IDisposable` to clean up | Guard clauses on mutations

## MonoBehaviour with Dependencies

```csharp
using UnityEngine;
using UnityEngine.UI;

namespace YourProject.UI;

/// <summary>Displays player health bar, subscribes to state events.</summary>
public sealed class HealthBarView : MonoBehaviour
{
    [Header("UI References")]
    [Tooltip("Slider component for health display")]
    [SerializeField] private Slider healthSlider;

    [Header("Configuration")]
    [Tooltip("Duration of health bar animation in seconds")]
    [SerializeField] private float animationDuration = 0.3f;

    private IPlayerState playerState;

    /// <summary>Initializes the view with its dependencies. Call after instantiation.</summary>
    public void Initialize(IPlayerState playerState) { this.playerState = playerState; }

    private void OnEnable() { this.playerState.HealthChanged += this.UpdateHealth; }
    private void OnDisable() { this.playerState.HealthChanged -= this.UpdateHealth; }
    private void UpdateHealth(int health) { this.healthSlider.value = health; }
}
```

Rules: `Initialize()` method for dependency injection | Subscribe `OnEnable`, unsubscribe `OnDisable` | `sealed` by default
