# Dragon Crashers: Themes, Performance & Animations (Part 2)

---

## USS & TSS Organization

### Base USS (7 files in `Assets/UI/Uss/Base/`)

| File | Key Content |
|------|------------|
| Colors.uss | BEM utilities: `.color__text--white`. ⚠️ BUG: `.color__text--blue` uses orange |
| Text.uss | Global font, fixed sizes (35/45/60/80px) |
| Common.uss | `:root` font/cursor only (NOT design tokens), `.screen__anchor--fill` |
| Buttons.uss | Transparent base, hover scale 1.1, tint-based color variants |
| Dropdowns.uss | ⚠️ **MUST import via TSS** — compound parts only resolve via TSS |
| Cursors.uss | Two-cursor system via type selectors |

### DC vs Recommended Approach

| Aspect | DC (Actual) | Recommended |
|---|---|---|
| Colors | BEM classes with hardcoded `rgb()` | `:root` variables + `var()` |
| Typography | Fixed pixel sizes | Token scale + `var()` |
| Theming | Swap entire TSS file | Override `:root` variables |
| Best for | Fixed-theme games | Dark/light or brand customization |

### TSS 7-File Matrix

```
RuntimeTheme-Default.tss ← unity-theme://default + Decoration-Default.uss
├── RuntimeTheme-Landscape.tss ← + 11 Landscape/*.uss
│   ├── Landscape--Christmas.tss ← + Decoration-Christmas.uss
│   └── Landscape--Halloween.tss
└── RuntimeTheme-Portrait.tss ← + 11 Portrait/*.uss
    ├── Portrait--Christmas.tss
    └── Portrait--Halloween.tss
```

Seasonal decorations use visibility toggling: `.theme__decoration--christmas { display: flex; }` / others `{ display: none; }`.

Orientation USS overrides same classes with different layout (e.g., `.menu-bar__container`: column→row, width/height swap).

---

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
