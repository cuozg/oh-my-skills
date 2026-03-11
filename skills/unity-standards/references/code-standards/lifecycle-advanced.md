# Unity Lifecycle — Advanced

## DefaultExecutionOrder

```csharp
// Negative = runs earlier, positive = runs later
[DefaultExecutionOrder(-100)] public sealed class GameManager : MonoBehaviour { }
[DefaultExecutionOrder(-50)]  public sealed class InputManager : MonoBehaviour { }
[DefaultExecutionOrder(100)]  public sealed class UIManager : MonoBehaviour { }
```

## Application Lifecycle Callbacks

```csharp
// Called when app loses/gains focus (alt-tab, phone notification)
void OnApplicationFocus(bool hasFocus)
{
    if (!hasFocus) PauseAudio();
    else ResumeAudio();
}

// Called when app is paused (mobile: home button, incoming call)
void OnApplicationPause(bool pauseStatus)
{
    if (pauseStatus) SaveProgress();
}

// Called before app quits — return false to cancel (editor only)
void OnApplicationQuit()
{
    SaveFinalState();
    CleanupNetworkConnections();
}
```

| Callback | Mobile | Desktop | Editor |
|----------|--------|---------|--------|
| `OnApplicationFocus` | App switch | Alt-tab | Lose focus |
| `OnApplicationPause` | Home/call | Minimize | Play→Pause |
| `OnApplicationQuit` | Kill app | Close window | Stop play |

## Visibility Callbacks

```csharp
// Called when renderer becomes visible/invisible to any camera
void OnBecameVisible() => _isOnScreen = true;
void OnBecameInvisible() => _isOnScreen = false;

// Use for: LOD toggling, disabling expensive updates on off-screen objects
void Update()
{
    if (!_isOnScreen) return;
    ExpensiveAICalculation();
}
```

## Reset() — Inspector Defaults

```csharp
// Called in Editor when component is first added or Reset is clicked
void Reset()
{
    _speed = 5f;
    _rb = GetComponent<Rigidbody>();
    _audioSrc = GetComponent<AudioSource>();
}
```
