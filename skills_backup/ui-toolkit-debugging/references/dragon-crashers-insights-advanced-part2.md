# Dragon Crashers: Theme System & Performance

## Theme System

**Events**: `ThemeEvents.ThemeChanged(string)`, `MediaQueryEvents.ResolutionUpdated/AspectRatioUpdated/SafeAreaUpdated/DpiUpdated`

**Flow**: Season change → `SettingsScreenController.UpdateTheme()` → constructs `"Portrait--Halloween"` → `ThemeEvents.ThemeChanged` → `ThemeManager.ApplyTheme()`. Orientation change keeps season suffix, swaps prefix.

**Adding a season**: Create Decoration USS + 2 TSS files + 2 ThemeSettings entries + dropdown option.

---

## Performance Notes

- **FpsCounter**: Ring buffer (50 samples), `m_IsEnabled` guard. ⚠️ Per-frame `$"FPS: {value}"` allocates ~40 bytes.
- **HealthBarController**: Uses `transform.position` (good), but ⚠️ `Camera.main` calls `FindWithTag` — cache it. `ShowNameAndStats` calls `Q<>` per frame — cache in `OnEnable`.
- **Async GC**: `Task.Delay` ~120 bytes/call, `label.text += c` allocates per char, `value.ToString()` ~24 bytes.
- **Dynamic lists**: <20 items → Instantiate loop. 50+ → **must** use `ListView`.

| Method | Effect |
|--------|--------|
| `StopPropagation()` | Stops bubbling, same-target listeners still fire |
| `StopImmediatePropagation()` | Stops bubbling AND same-target listeners |

**Event rules**: Every `+=` needs matching `-=`. MonoBehaviour: `OnEnable`/`OnDisable`. Plain C#: constructor/`Dispose()`. Static events are most dangerous.

---

## Experimental Animations

```csharp
// Position: marker slide
m_MenuMarker.experimental.animation.Position(targetLocal, 200);
// Scale: pop-in
element.transform.scale = new Vector3(0.1f, 0.1f, 1f);
element.experimental.animation.Scale(1f, 200);
// Click cooldown
if (Time.time < m_NextClick) return; m_NextClick = Time.time + 0.2f;
```
