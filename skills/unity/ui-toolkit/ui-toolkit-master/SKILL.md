---
name: ui-toolkit-master
description: "Master guide for Unity UI Toolkit — the retained-mode UI framework for Unity 6+. Covers architecture, UXML/USS/C# anatomy, project structure, and links to specialized sub-skills. Use when: (1) Starting a new UI Toolkit project, (2) Choosing between UI Toolkit and legacy uGUI, (3) Understanding the UXML/USS/C# triad, (4) Setting up project structure for UI, (5) Learning UI Toolkit fundamentals. Triggers: 'UI Toolkit', 'UXML', 'USS', 'new UI project', 'UI Toolkit vs uGUI', 'runtime UI setup'."
---

# UI Toolkit Master

<!-- OWNERSHIP: Fundamentals, UXML/USS/C# triad, project structure, UIDocument, PanelSettings, learning path. Cross-ref other skills for all specialized topics. -->

Root skill for the UI Toolkit series. Start here for fundamentals, then follow the learning path to specialized sub-skills.

> **Based on**: Unity 6 (6000.0), Dragon Crashers official sample, and production mobile game patterns.

## Learning Path

Progress through the series from fundamentals to advanced topics. Each level builds on the previous.

### Level 1 — Foundations (Start Here)

| # | Skill | Learning Objectives | Est. Time |
|---|-------|-------------------|-----------|
| 1 | **ui-toolkit-master** (this) | UXML/USS/C# triad, project setup, UIDocument, PanelSettings | 1 hr |
| 2 | [ui-toolkit-architecture](../ui-toolkit-architecture/SKILL.md) | Custom controls, [UxmlElement], MVC pattern, template composition | 2 hrs |
| 3 | [ui-toolkit-responsive](../ui-toolkit-responsive/SKILL.md) | Flexbox layout, length units, safe area, orientation handling | 1.5 hrs |

### Level 2 — Intermediate

| # | Skill | Learning Objectives | Est. Time |
|---|-------|-------------------|-----------|
| 4 | [ui-toolkit-theming](../ui-toolkit-theming/SKILL.md) | Design tokens, TSS/USS cascade, runtime theme switching | 1.5 hrs |
| 5 | [ui-toolkit-databinding](../ui-toolkit-databinding/SKILL.md) | IDataSource, [CreateProperty], binding modes, type converters | 2 hrs |
| 6 | [ui-toolkit-patterns](../ui-toolkit-patterns/SKILL.md) | Tabs, inventory grid, modals, stateful buttons, scroll snap | 2 hrs |

### Level 3 — Advanced

| # | Skill | Learning Objectives | Est. Time |
|---|-------|-------------------|-----------|
| 7 | [ui-toolkit-performance](../ui-toolkit-performance/SKILL.md) | Profiling, draw calls, virtualization, GC-free patterns | 1.5 hrs |
| 8 | [ui-toolkit-mobile](../ui-toolkit-mobile/SKILL.md) | Touch/gesture, orientation, mobile budgets, haptic feedback | 2 hrs |
| 9 | [ui-toolkit-debugging](../ui-toolkit-debugging/SKILL.md) | UI Debugger, Event Debugger, profiler markers, diagnostic code | 1.5 hrs |

**Total estimated learning time: ~15 hours**

## Shared Resources

- [Dragon Crashers Insights](../references/dragon-crashers-insights.md) — patterns extracted from Unity's official sample project
- [Official Docs Links](../references/official-docs-links.md) — curated Unity 6 documentation links by topic
- [Code Templates](../references/code-templates.md) — 8 production-ready UXML/USS/C# templates
- [Performance Benchmarks](../references/performance-benchmarks.md) — metrics, budgets, and zero-alloc patterns
- [QuizU Patterns](../references/quizu-patterns.md) — EventRegistry, UIScreen base, Presenter pattern from Unity's QuizU sample

## UI Toolkit vs Legacy UI

| Feature | uGUI (Canvas) | UI Toolkit |
|---------|---------------|------------|
| Layout | RectTransform, anchors | Flexbox (Yoga engine) |
| Styling | Inspector per-element | USS (CSS-like cascading) |
| Structure | Prefabs in hierarchy | UXML documents (markup) |
| Theming | Manual per-element | TSS (Theme Style Sheets) |
| Data Binding | Manual callbacks | Built-in runtime binding (Unity 6) |
| Lists | ScrollRect + manual pooling | ListView with virtualization |
| Performance | Per-element Canvas rebuild | Retained-mode, batched rendering |
| Editor UI | Limited | Full support |

**When to use UI Toolkit:**
- New projects on Unity 6+
- Complex UI with many screens
- Need theming / consistent styling
- Performance-critical lists or grids
- Shared editor + runtime UI

**When uGUI may still be preferred:**
- World-space UI tightly integrated with 3D (UI Toolkit world-space is experimental in 6.2+)
- Existing uGUI project mid-development
- Heavy TextMeshPro dependency with custom shaders

## The UXML / USS / C# Triad

```
┌──────────────────────────────────────────────────┐
│                    UXML                           │
│  Structure & hierarchy (what elements exist)      │
│  <ui:VisualElement>, <ui:Label>, <ui:Button>      │
│  Template composition: <ui:Template src="...">    │
├──────────────────────────────────────────────────┤
│                    USS                            │
│  Styling & visual presentation (how it looks)     │
│  Selectors: .class, #name, Type, :hover, :active  │
│  Custom properties: --color-primary, --spacing-md │
│  Transitions: translate, opacity, scale           │
├──────────────────────────────────────────────────┤
│                    C#                             │
│  Behavior & logic (what it does)                  │
│  Query: root.Q<Button>("btn-start")               │
│  Events: RegisterCallback<ClickEvent>             │
│  Data binding: element.dataSource = myData        │
│  Custom controls: [UxmlElement] partial class     │
└──────────────────────────────────────────────────┘
```

**Separation rules:**
- UXML: No styling inline (use USS classes). No logic.
- USS: No layout hierarchy. No behavior. Only visual presentation.
- C#: No hardcoded styles. Query elements, bind data, handle events.

## Project Structure

Recommended folder organization for production projects:

```
Assets/
├── UI/
│   ├── Documents/           # UXML files
│   │   ├── Screens/         # Full-screen layouts
│   │   ├── Components/      # Reusable component templates
│   │   └── Modals/          # Popups, dialogs
│   ├── Styles/              # USS files
│   │   ├── Base/            # tokens.uss, reset.uss, typography.uss
│   │   ├── Components/      # Per-component USS
│   │   └── Themes/          # TSS files
│   └── Resources/           # Sprites, fonts, atlases
├── Scripts/
│   └── UI/
│       ├── Screens/         # Screen controllers
│       ├── Components/      # Custom VisualElement subclasses
│       ├── Binding/         # Data sources, converters
│       └── Core/            # UIManager, ScreenManager, SafeArea
└── Settings/
    └── PanelSettings.asset  # Runtime panel configuration
```

## Minimal Setup — Runtime UI

### 1. PanelSettings asset

Create via **Assets > Create > UI Toolkit > Panel Settings Asset**.

Key settings:
- **Scale Mode**: `ScaleWithScreenSize`
- **Reference Resolution**: Match target (e.g., 1920×1080)
- **Screen Match Mode**: Match width or height based on game orientation
- **Theme Style Sheet**: Assign your TSS

### 2. UIDocument component

Add `UIDocument` to a GameObject in the scene:

```csharp
// UIDocument setup
[RequireComponent(typeof(UIDocument))]
public class MainUIController : MonoBehaviour
{
    void OnEnable()
    {
        var root = GetComponent<UIDocument>().rootVisualElement;

        // Load USS
        var styleSheet = Resources.Load<StyleSheet>("Styles/MainScreen");
        root.styleSheets.Add(styleSheet);

        // Query and bind
        var startBtn = root.Q<Button>("btn-start");
        startBtn.RegisterCallback<ClickEvent>(OnStartClicked);
    }

    void OnStartClicked(ClickEvent evt)
    {
        Debug.Log("Game started");
    }
}
```

### 3. UXML document

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements">
    <ui:VisualElement name="root" class="screen">
        <ui:Label text="My Game" class="title" />
        <ui:Button name="btn-start" text="Start" class="btn-primary" />
    </ui:VisualElement>
</ui:UXML>
```

## Performance Fundamentals

Key rules (deep-dive in [ui-toolkit-performance](../ui-toolkit-performance/SKILL.md)):

1. **Animate transforms, not layout** — `translate`, `rotate`, `scale`, `opacity` are GPU-accelerated. `width`, `height`, `margin`, `padding` trigger expensive layout recalculation.
2. **Use ListView for lists** — Virtualization handles 1000+ items with constant memory.
3. **Cache Q() calls** — `root.Q<Label>("name")` allocates. Call once, store reference.
4. **Set UsageHints** — `DynamicTransform` on animated elements enables batching.
5. **Minimize nesting** — Deep visual trees increase layout cost.

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Inline styles in UXML | Unmaintainable, no theming | Use USS classes |
| Q() every frame | GC pressure (~40 bytes/call) | Cache in OnEnable |
| Animating width/height | Layout thrashing (full subtree recalc) | Use translate/scale |
| ScrollView for 100+ items | Memory, lag | Use ListView with virtualization |
| Rebuilding UI on data change | Expensive recreation | Use data binding |
| Ignoring safe area | Notch overlap on mobile | Use SafeAreaHandler |
| Not setting UsageHints | Missed GPU batching | DynamicTransform on animated elements |
| String concat in labels per frame | GC allocations | Cache strings or use StringBuilder |

## Dragon Crashers — How It's Built

Unity's [Dragon Crashers](../references/dragon-crashers-insights.md) sample demonstrates every pattern in this series.

> **Full project structure, USS organization, architecture details, SafeAreaBorder, async patterns, and PositionToVisualElement**: See [references/master-dc-structure.md](references/master-dc-structure.md) — includes complete folder tree, USS scope architecture, production metrics, and cross-references to all sub-skills.

**Key architectural decisions:**
- Single UIDocument with one `MainMenu.uxml` — screens toggled via `DisplayStyle.Flex/None`
- UIView base class enforces lifecycle: `Initialize()` → `SetVisualElements()` → `RegisterButtonCallbacks()`
- UIManager implements modal (replace) and overlay (stack) navigation
- Static `Action` event bus decouples View ↔ Controller communication
- Orientation overrides via TSS swapping, not media queries
- borderWidth-based safe area (not padding) — see [ui-toolkit-responsive](../ui-toolkit-responsive/SKILL.md)
- Custom controls use `UxmlFactory`/`UxmlTraits` (DC legacy) — use `[UxmlElement]` for new Unity 6 projects

**Production metrics:** 8–12 tree depth, 50–200 elements/screen, 4–8 draw calls, 2–4 MB memory, <100ms init on mobile.

## Exercise: Hello UI Toolkit

> **Full exercise with UXML, USS, and C# code**: See [references/master-dc-structure.md](references/master-dc-structure.md#exercise-hello-ui-toolkit) — build a minimal main menu with title, start button, and settings button. Includes complete code, USS styling, and a self-review checklist.

## Official Documentation

- [UI Toolkit Overview](https://docs.unity3d.com/6000.0/Documentation/Manual/UIElements.html)
- [Getting Started](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-simple-ui-toolkit-workflow.html)
- [UXML Reference](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-UXML.html)
- [USS Reference](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-USS.html)
- [UI Toolkit vs uGUI](https://docs.unity3d.com/6000.0/Documentation/Manual/UI-system-compare.html)
- See [all curated links](../references/official-docs-links.md) for topic-specific documentation

> **Dragon Crashers Source References**: See [Dragon Crashers Insights](../references/dragon-crashers-insights.md) (section: DC Source Files Reference) for the complete file listing of all UIView, Controller, Event, USS, UXML, and TSS files referenced in this skill.

## Sub-Skill Cross-Reference

Quick reference for which sub-skill covers each topic:

| Topic | Sub-Skill | Key Patterns |
|-------|-----------|--------------|
| Custom controls, [UxmlElement], MVC, templates | [ui-toolkit-architecture](../ui-toolkit-architecture/SKILL.md) | UIView pattern, template composition, multi-document |
| Flexbox, safe area, orientation, length units | [ui-toolkit-responsive](../ui-toolkit-responsive/SKILL.md) | SafeAreaBorder, orientation-aware layouts |
| Design tokens, TSS cascade, theme switching | [ui-toolkit-theming](../ui-toolkit-theming/SKILL.md) | 7-TSS matrix, Decoration-*.uss seasonal themes |
| IDataSource, [CreateProperty], binding modes | [ui-toolkit-databinding](../ui-toolkit-databinding/SKILL.md) | Runtime data binding, type converters |
| Tabs, inventory, modals, scroll snap | [ui-toolkit-patterns](../ui-toolkit-patterns/SKILL.md) | TabbedMenu, modal/overlay nav, static event bus |
| Profiling, draw calls, virtualization | [ui-toolkit-performance](../ui-toolkit-performance/SKILL.md) | ListView, UsageHints, GC-free patterns |
| Touch/gesture, mobile budgets, haptics | [ui-toolkit-mobile](../ui-toolkit-mobile/SKILL.md) | PositionToVisualElement, mobile optimization |
| UI Debugger, Event Debugger, diagnostics | [ui-toolkit-debugging](../ui-toolkit-debugging/SKILL.md) | Profiler markers, diagnostic code |

## Coverage Gaps (Stub Guidance)

> **Full guidance with code examples and decision tables**: See [references/master-dc-structure.md](references/master-dc-structure.md#coverage-gaps) — covers Accessibility (focus navigation, high contrast, touch targets, screen readers), Testing (Edit Mode, Play Mode, event simulation, visual regression), and Localization (RTL, CJK, `com.unity.localization`).
