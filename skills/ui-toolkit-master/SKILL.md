---
name: ui-toolkit-master
description: "Master guide for Unity UI Toolkit — the retained-mode UI framework for Unity 6+. Covers architecture, UXML/USS/C# anatomy, project structure, and links to specialized sub-skills. Use when: (1) Starting a new UI Toolkit project, (2) Choosing between UI Toolkit and legacy uGUI, (3) Understanding the UXML/USS/C# triad, (4) Setting up project structure for UI, (5) Learning UI Toolkit fundamentals. Triggers: 'UI Toolkit', 'UXML', 'USS', 'new UI project', 'UI Toolkit vs uGUI', 'runtime UI setup'."
---

# UI Toolkit Master

Root skill for the UI Toolkit series. Start here, then follow the learning path.

## Output

Production-ready UXML/USS/C# code and project structure following UI Toolkit best practices.

## Learning Path (~15 hours)

See [references/learning-path.md](references/learning-path.md) for complete curriculum.

**Summary:**
- **Level 1**: UXML/USS/C# triad, project setup, responsive basics (4.5 hrs)
- **Level 2**: Custom controls, theming, data binding, UI patterns (5.5 hrs)
- **Level 3**: Performance, mobile optimization, debugging (5 hrs)

## UI Toolkit vs uGUI

| Feature | uGUI | UI Toolkit |
|---------|------|------------|
| Layout | RectTransform, anchors | Flexbox (Yoga) |
| Styling | Inspector per-element | USS (CSS-like) |
| Theming | Manual | TSS |
| Data Binding | Manual callbacks | Built-in (Unity 6) |
| Lists | ScrollRect + manual pooling | ListView virtualization |
| Performance | Per-element Canvas rebuild | Retained-mode, batched |

**Use UI Toolkit**: New Unity 6+ projects, complex UI, theming, performance-critical lists.
**Use uGUI**: World-space 3D UI (UI Toolkit experimental in 6.2+), existing uGUI mid-dev, heavy TMP custom shaders.

## The UXML / USS / C# Triad

```
UXML — Structure (what elements exist). Templates, hierarchy.
USS  — Styling (how it looks). Selectors, custom properties, transitions.
C#   — Behavior (what it does). Q<T>(), events, data binding, [UxmlElement].
```

**Rules:** UXML: no inline styles, no logic. USS: no hierarchy, no behavior. C#: no hardcoded styles.

## Project Structure

```
Assets/
├── UI/
│   ├── Documents/       # UXML: Screens/, Components/, Modals/
│   ├── Styles/          # USS: Base/ (tokens, reset, typography), Components/, Themes/
│   └── Resources/       # Sprites, fonts, atlases
├── Scripts/UI/          # Screens/, Components/, Binding/, Core/
└── Settings/PanelSettings.asset
```

## Minimal Setup

### PanelSettings

Create via **Assets > Create > UI Toolkit > Panel Settings Asset**. Key: Scale Mode, Reference Resolution, Theme Style Sheet.

### UIDocument + Controller

```csharp
[RequireComponent(typeof(UIDocument))]
public class MainUIController : MonoBehaviour {
    void OnEnable() {
        var root = GetComponent<UIDocument>().rootVisualElement;
        root.styleSheets.Add(Resources.Load<StyleSheet>("Styles/MainScreen"));
        root.Q<Button>("btn-start").RegisterCallback<ClickEvent>(OnStartClicked);
    }
    void OnStartClicked(ClickEvent evt) => Debug.Log("Game started");
}
```

## Performance Fundamentals

See ui-toolkit-performance for deep-dive.

1. **Animate transforms only** — `translate`, `scale`, `opacity` (GPU). Never `width`/`height` (layout recalc).
2. **ListView for lists** — Virtualization handles 1000+ items.
3. **Cache Q() calls** — Call once in OnEnable, store reference.
4. **UsageHints** — `DynamicTransform` on animated elements.
5. **Minimize nesting** — Deep trees increase layout cost.

## Common Mistakes

See [references/common-mistakes.md](references/common-mistakes.md) for detailed troubleshooting.

## Dragon Crashers

> **Full details**: [references/master-dc-structure.md](references/master-dc-structure.md)

**Key architecture:** Single UIDocument, screens toggled via DisplayStyle. UIView lifecycle: `Initialize()` → `SetVisualElements()` → `RegisterButtonCallbacks()`. Modal + overlay navigation. Static Action event bus. Orientation via TSS swap. borderWidth safe area.

**Metrics:** 8–12 tree depth, 50–200 elements/screen, 4–8 draw calls, 2–4 MB, <100ms init.
