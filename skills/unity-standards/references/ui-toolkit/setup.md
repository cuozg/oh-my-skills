# UI Toolkit Setup

## UIDocument Component

Attach to a GameObject to render UI Toolkit content at runtime.

| Property | Description |
|----------|-------------|
| `Panel Settings` | PanelSettings asset — defines rendering panel, scale mode |
| `Source Asset` | UXML file to instantiate as root |
| `Sort Order` | Render layer (higher = on top) within same PanelSettings |

```
┌─ GameObject
│  ├─ UIDocument
│  │  ├─ Panel Settings → Assets/UI/Settings/MainPanel.asset
│  │  ├─ Source Asset   → Assets/UI/Screens/MainMenu.uxml
│  │  └─ Sort Order     → 0
│  └─ MainMenuController.cs (MonoBehaviour)
```

Access root: `GetComponent<UIDocument>().rootVisualElement`

## PanelSettings Asset

Create via `Assets > Create > UI Toolkit > Panel Settings Asset`.

### Scale Modes

| Mode | Behavior | Use Case |
|------|----------|----------|
| `ConstantPixelSize` | Fixed pixel size, ignores resolution | Desktop, pixel-perfect |
| `ScaleWithScreenSize` | Scales relative to reference resolution | Mobile, multi-platform |
| `ConstantPhysicalSize` | Same physical size across DPIs | DPI-aware responsive |

**Default recommendation**: `ScaleWithScreenSize`, reference 1920×1080, match mode `Expand`.

### Multiple PanelSettings

Use separate PanelSettings for independent UI contexts:

```
HUD_UIDocument     → HUD_PanelSettings (Sort: 10)
Minimap_UIDocument → Minimap_PanelSettings (Sort: 20)
Modal_UIDocument   → Modal_PanelSettings (Sort: 100)
```

## Scene Setup Checklist

1. Create `PanelSettings` asset (scale mode, reference resolution)
2. Create `.uxml` template and `.uss` stylesheet
3. Add `UIDocument` component to GameObject
4. Assign PanelSettings + UXML source
5. Add C# controller MonoBehaviour to same GameObject
6. Query elements in `OnEnable`, unregister in `OnDisable`

## Event System

- UI Toolkit works without `EventSystem` component (has its own input handling)
- If mixing with uGUI, add `EventSystem` + appropriate input module
- Input source auto-detected: Legacy Input Manager or Input System Package

## File Organization

```
Assets/UI/
├── Settings/         ← PanelSettings assets (.asset)
├── Screens/          ← Full-screen UXML files
├── Components/       ← Reusable UXML template snippets
├── Styles/           ← USS files (theme.uss, variables.uss, per-screen)
└── Controllers/      ← C# MonoBehaviour controllers
```
