# Inline Comment Format - Advanced Patterns

## Serialization & Lifecycle Example

```csharp
// ╔══════════════════════════════════════════════════════════════
// ║ REVIEW [🔴 CRITICAL]: Serialized field mutated at runtime
// ╟──────────────────────────────────────────────────────────────
// ║ WHY:  `_config` is a public SerializeField pointing to a
// ║       shared ScriptableObject asset. Changes here persist
// ║       across all instances + reloads.
// ║ WHERE: Called from:
// ║         → UpgradeShop.cs:156  (modifies _config.damage)
// ║         → AIController.cs:89  (adds to _config.abilityCooldown)
// ║ FIX:  Create instance copy in Awake:
// ║
// ║       void Awake() {
// ║           _config = Instantiate(_config);
// ║       }
// ╚══════════════════════════════════════════════════════════════
[SerializeField] private WeaponConfig _config;
_config.damage += 10;
```

## GC Allocation in Hot Path Example

```csharp
// ╔══════════════════════════════════════════════════════════════
// ║ REVIEW [🔴 CRITICAL]: String allocation in Update (60fps)
// ╟──────────────────────────────────────────────────────────────
// ║ WHY:  String concatenation allocates new string object
// ║       every frame. 60 frames * 60sec = 3600 allocs/min,
// ║       triggers GC stalls.
// ║ FIX:  Cache string or use StringBuilder:
// ║
// ║       private StringBuilder _sb = new();
// ║       void Update() {
// ║           _sb.Clear();
// ║           _sb.Append("Health: ").Append(_health);
// ║           _healthText.text = _sb.ToString();
// ║       }
// ╚══════════════════════════════════════════════════════════════
void Update() {
    _healthText.text = "Health: " + _health;
}
```

## Platform-Specific Example

```csharp
// ╔══════════════════════════════════════════════════════════════
// ║ REVIEW [🟡 MAJOR]: Platform code not guarded
// ╟──────────────────────────────────────────────────────────────
// ║ WHY:  Social.Instance exists only on iOS. Calling it on
// ║       Android → null reference crash.
// ║ FIX:  Guard with platform check:
// ║
// ║       #if UNITY_IOS
// ║       Social.Instance.ShowShareUI();
// ║       #endif
// ╚══════════════════════════════════════════════════════════════
Social.Instance.ShowShareUI();
```
