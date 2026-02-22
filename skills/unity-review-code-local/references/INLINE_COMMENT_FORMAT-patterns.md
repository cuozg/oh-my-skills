# Inline Comment Format - Advanced Patterns

## Serialization & Lifecycle Example

```csharp
// REVIEW [🔴 CRITICAL]: Serialized field mutated at runtime
// WHY:
//   - `_config` is a shared ScriptableObject — changes persist across instances + reloads
//   - Mutated by: UpgradeShop.cs:156, AIController.cs:89
// FIX:
//   - Clone in Awake: `_config = Instantiate(_config);`
[SerializeField] private WeaponConfig _config;
_config.damage += 10;
```

## GC Allocation in Hot Path Example

```csharp
// REVIEW [🔴 CRITICAL]: String allocation in Update (60fps)
// WHY:
//   - String concat allocates every frame → 3600 allocs/min → GC stalls
// FIX:
//   - Cache StringBuilder: `_sb.Clear(); _sb.Append("Health: ").Append(_health);`
//   - Or use TextMeshPro SetText with format args (zero-alloc)
void Update() {
    _healthText.text = "Health: " + _health;
}
```

## Platform-Specific Example

```csharp
// REVIEW [🟡 MAJOR]: Platform code not guarded
// WHY:
//   - Social.Instance only exists on iOS — null ref crash on Android
// FIX:
//   - Wrap in `#if UNITY_IOS` / `#endif`
//   - Or use platform abstraction layer
Social.Instance.ShowShareUI();
```
