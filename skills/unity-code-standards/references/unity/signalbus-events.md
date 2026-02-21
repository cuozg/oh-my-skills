# SignalBus Event Patterns

## Overview

SignalBus provides decoupled event communication between systems. Use struct signals for zero-allocation events.

## Signal Definition

```csharp
// ✅ GOOD: Readonly record struct signals (zero allocation, immutable)
public readonly record struct GameStartedSignal(int Level);
public readonly record struct PlayerDiedSignal(string PlayerId, string Cause);
public readonly record struct ScoreChangedSignal(int OldScore, int NewScore);
public readonly record struct ItemPickedUpSignal(string ItemId, int Quantity);

// ✅ GOOD: Empty signal (no data needed)
public readonly record struct GamePausedSignal;
public readonly record struct GameResumedSignal;

// ❌ BAD: Class signals (heap allocation)
public class GameStartedSignal
{
    public int Level { get; set; }
}

// ❌ BAD: Mutable struct signals
public struct ScoreChangedSignal
{
    public int OldScore;
    public int NewScore; // Mutable — dangerous
}
```

## Signal Naming Conventions

```
// Pattern: [Subject][Verb-PastTense]Signal
GameStartedSignal      // Game has started
PlayerDiedSignal       // Player has died
ItemPickedUpSignal     // Item has been picked up
LevelCompletedSignal   // Level has been completed
SettingsChangedSignal  // Settings have changed

// ❌ BAD naming:
GameStartSignal        // Is this a command or event?
OnPlayerDied           // Don't use "On" prefix — that's for handlers
PlayerDeathEvent       // Use "Signal" suffix, not "Event"
```

## Subscribing & Unsubscribing

```csharp
// ✅ GOOD: Subscribe in Initialize, unsubscribe in Dispose
public sealed class ScoreDisplay : IInitializable, IDisposable
{
    private readonly SignalBus signalBus;

    [Preserve]
    public ScoreDisplay(SignalBus signalBus)
    {
        this.signalBus = signalBus;
    }

    public void Initialize()
    {
        this.signalBus.Subscribe<ScoreChangedSignal>(this.OnScoreChanged);
        this.signalBus.Subscribe<GameStartedSignal>(this.OnGameStarted);
    }

    public void Dispose()
    {
        this.signalBus.Unsubscribe<ScoreChangedSignal>(this.OnScoreChanged);
        this.signalBus.Unsubscribe<GameStartedSignal>(this.OnGameStarted);
    }

    private void OnScoreChanged(ScoreChangedSignal signal)
    {
        UpdateUI(signal.NewScore);
    }

    private void OnGameStarted(GameStartedSignal signal)
    {
        ResetUI();
    }
}

// ❌ BAD: Subscribe without unsubscribe (memory leak)
public void Initialize()
{
    this.signalBus.Subscribe<ScoreChangedSignal>(this.OnScoreChanged);
    // Missing Dispose → leak
}

// ❌ BAD: Subscribe with lambda (can't unsubscribe)
this.signalBus.Subscribe<ScoreChangedSignal>(s => UpdateUI(s.NewScore));
// Can't unsubscribe a lambda!
```

## Firing Signals

```csharp
// ✅ GOOD: Fire with data
this.signalBus.Fire(new ScoreChangedSignal(oldScore, newScore));
this.signalBus.Fire(new PlayerDiedSignal(playerId, "FallDamage"));

// ✅ GOOD: Fire empty signal
this.signalBus.Fire(new GamePausedSignal());

// ❌ BAD: Fire from constructor
public GameService(SignalBus signalBus)
{
    signalBus.Fire(new GameStartedSignal(1)); // Too early! Others may not be subscribed yet
}
```

## Registration

```csharp
// In LifetimeScope
protected override void Configure(IContainerBuilder builder)
{
    // Register the SignalBus
    builder.RegisterSignalBus();

    // Declare signals (optional but recommended for documentation)
    builder.DeclareSignal<GameStartedSignal>();
    builder.DeclareSignal<PlayerDiedSignal>();
    builder.DeclareSignal<ScoreChangedSignal>();
}
```

## Signal vs Direct Call Decision Tree

```
Is the caller in the same system/module?
├── YES → Direct method call
└── NO → Does the caller need to know about the receiver?
    ├── YES → Interface + DI (dependency)
    └── NO → SignalBus (decoupled)
```

## Common Patterns

### Request-Response via Signals

```csharp
// Request signal
public readonly record struct SaveGameRequestSignal;

// Response signal
public readonly record struct SaveGameCompletedSignal(bool Success, string? Error);

// Requester
this.signalBus.Fire(new SaveGameRequestSignal());

// Handler
private void OnSaveGameRequest(SaveGameRequestSignal _)
{
    try
    {
        SaveGame();
        this.signalBus.Fire(new SaveGameCompletedSignal(true, null));
    }
    catch (Exception ex)
    {
        this.signalBus.Fire(new SaveGameCompletedSignal(false, ex.Message));
    }
}
```

### Signal with Enum State

```csharp
public enum GamePhase { Loading, Playing, Paused, GameOver }
public readonly record struct GamePhaseChangedSignal(GamePhase OldPhase, GamePhase NewPhase);
```

## Anti-Patterns

```csharp
// ❌ BAD: Signal for same-class communication
this.signalBus.Fire(new InternalUpdateSignal()); // Just call the method!

// ❌ BAD: Signal carrying mutable reference types
public readonly record struct BadSignal(List<Player> Players); // Mutable list!

// ❌ BAD: Chaining signals (signal handler fires another signal)
private void OnA(SignalA _)
{
    this.signalBus.Fire(new SignalB()); // Creates hard-to-debug chains
    // If unavoidable, document the chain clearly
}

// ❌ BAD: Heavy work in signal handlers
private void OnScoreChanged(ScoreChangedSignal signal)
{
    // Don't do heavy computation here — signal handlers should be fast
    RecalculateAllLeaderboards(); // Move to async/scheduled work
}
```
