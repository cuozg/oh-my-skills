# Dragon Crashers Sample — Key Insights

Unity's official Dragon Crashers sample is a vertical-slice mobile idle-RPG built entirely with UI Toolkit. It demonstrates production-grade patterns for complex game UI.

## Project Structure

```
Assets/
├── UI/
│   ├── UXML/           # Layout documents
│   │   ├── Screens/    # Full-screen views (HomeScreen, CharScreen, MailScreen)
│   │   ├── Components/ # Reusable elements (CharCard, MailItem, TabBar)
│   │   └── Modals/     # Overlay dialogs (SettingsModal, InfoPopup)
│   ├── USS/            # Style sheets
│   │   ├── Themes/     # TSS files (DarkTheme.tss, LightTheme.tss)
│   │   ├── Base/       # Reset, typography, spacing tokens
│   │   └── Components/ # Per-component styles (CharCard.uss, TabBar.uss)
│   └── Resources/      # Sprites, icons, fonts
├── Scripts/
│   ├── UI/
│   │   ├── Controllers/  # Screen-level logic (HomeScreenController.cs)
│   │   ├── Components/   # Custom VisualElement subclasses
│   │   ├── DataBinding/  # Data source adapters
│   │   └── Utilities/    # Helpers (SafeAreaHandler.cs, ThemeManager.cs)
│   └── GameLogic/        # Non-UI game systems
└── Data/
    └── ScriptableObjects/ # SO-based game data
```

## Key Patterns

### 1. Responsive Layout via Flexbox

- All layouts use `flex-grow`, `flex-shrink`, `flex-basis` — never fixed pixel widths for containers
- Percentage-based widths for grid columns: `width: 33.3%` for 3-column, `width: 25%` for 4-column
- Portrait vs landscape handled via C# class toggling on root element:

```csharp
// Orientation handler adds/removes USS class
root.EnableInClassList("landscape", Screen.width > Screen.height);
root.EnableInClassList("portrait", Screen.width <= Screen.height);
```

### 2. Tabbed Navigation

- Single `VisualElement` container per tab content
- `TabBar` custom control manages active state
- Only active tab content is visible (`display: flex` vs `display: none`)
- No destroy/recreate — all tabs stay in hierarchy for instant switching

### 3. Inventory / Character Grid

- Uses `ListView` with virtualization for large item lists (not ScrollView with manual elements)
- `makeItem` / `bindItem` callbacks for efficient recycling
- Item selection via `selectedIndicesChanged` event
- Detail panel updates via data binding to selected item

### 4. Mail / Message System

- `ListView` for message list with custom item template
- Read/unread state via USS class toggling (`mail-item--unread`)
- Badge count on tab via bound property
- Swipe-to-archive on mobile via `PointerMoveEvent`

### 5. Theme Style Sheets (TSS)

- Root `ThemeStyleSheet` asset assigned to `PanelSettings`
- TSS imports base USS files and adds theme-specific overrides
- Runtime theme switch by swapping `PanelSettings.themeStyleSheet`
- Custom properties for tokens: `--color-primary`, `--spacing-md`, `--font-size-body`

### 6. SafeArea Handling

- `SafeAreaHandler` component reads `Screen.safeArea` and applies padding
- Updates on `GeometryChangedEvent` for dynamic adjustment
- Applied to root container, not individual elements

### 7. Data Binding (Unity 6)

- `ScriptableObject` implements `INotifyBindablePropertyChanged`
- UI elements bind directly to SO properties
- Eliminates manual `SetValueWithoutNotify` / `RegisterValueChangedCallback` boilerplate
- Two-way binding for settings (volume sliders, toggles)

## Performance Techniques Used

| Technique | Where Applied | Impact |
|-----------|--------------|--------|
| `ListView` virtualization | Inventory, Mail | 95% fewer elements in visual tree |
| USS class toggling (not layout changes) | Tab switching, states | Avoids layout recalculation |
| Transform animations | Screen transitions | GPU-accelerated, no layout cost |
| `usageHints: DynamicTransform` | Animated elements | Batching hint for renderer |
| Element pooling | Notification toasts | Reduces GC pressure |
| Minimal overdraw | Layered backgrounds | Fewer draw calls |

## Metrics (Approximate)

- **Visual tree depth**: 8-12 levels typical for complex screens
- **Elements per screen**: 50-200 depending on content
- **Draw calls**: 4-8 per screen with proper batching
- **Memory**: ~2-4 MB for full UI hierarchy
- **Startup**: UI initialization < 100ms on mid-range mobile
