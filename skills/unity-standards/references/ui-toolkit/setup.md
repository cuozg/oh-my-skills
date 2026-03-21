# UI Toolkit Setup

## UIDocument Component

Attach `UIDocument` to a GameObject to render runtime UI Toolkit content.

| Property | Description |
|----------|-------------|
| `Panel Settings` | PanelSettings asset that defines rendering, scaling, and input behavior |
| `Source Asset` | UXML file instantiated as the root tree |
| `Sort Order` | Render order relative to sibling `UIDocument` components on the same panel |

```
GameObject
|- UIDocument
|  |- Panel Settings -> Assets/UI/Settings/MainPanel.asset
|  |- Source Asset   -> Assets/UI/Screens/MainMenu.uxml
|  `- Sort Order     -> 0
`- MainMenuController.cs
```

Access the root with `GetComponent<UIDocument>().rootVisualElement`.

## PanelSettings Asset

Create via `Assets > Create > UI Toolkit > Panel Settings Asset`.

### Scale Modes

| Mode | Behavior | Use Case |
|------|----------|----------|
| `ConstantPixelSize` | Fixed pixel size | Desktop, pixel-perfect UI |
| `ScaleWithScreenSize` | Scales relative to reference resolution | Most runtime game UI |
| `ConstantPhysicalSize` | Attempts physical-size consistency across DPIs | Specialized DPI-aware UI |

**Default recommendation:** `ScaleWithScreenSize` with an explicit reference resolution.

## Multiple Documents On One Panel

Unity supports multiple `UIDocument` components targeting the same `PanelSettings` asset.

```
HUD_UIDocument     -> HUD_PanelSettings   (Sort: 10)
Minimap_UIDocument -> HUD_PanelSettings   (Sort: 20)
Modal_UIDocument   -> HUD_PanelSettings   (Sort: 100)
```

Guidance:
- Use sort order intentionally.
- Child `UIDocument` components render above their parent.
- When toggling visibility temporarily, prefer style or GameObject state changes instead of rebuilding the whole screen unintentionally.

## Scene Setup Checklist

1. Create a `PanelSettings` asset.
2. Create the `.uxml` template and `.uss` stylesheet.
3. Add a `UIDocument` component to a GameObject.
4. Assign `PanelSettings` and the UXML source.
5. Add a C# controller to the same GameObject when runtime logic is needed.
6. Query elements in `OnEnable` and unregister callbacks in `OnDisable`.

Query in `OnEnable` because the visual tree can be rebuilt when a `UIDocument` is disabled and enabled again.

## Event System

- UI Toolkit runtime UI handles its own input path.
- If mixing with uGUI, validate the event and input setup carefully.
- Multiple documents sharing one panel also share focus navigation context.

## Runtime Binding Note

Runtime data binding exists in newer UI Toolkit versions, but it is version-sensitive. If a project uses it, confirm the exact feature set in `references/other/official-source-map.md` before assuming runtime and editor binding behave the same way.

## File Organization

```
Assets/UI/
|- Settings/      <- PanelSettings assets
|- Screens/       <- Full-screen UXML files
|- Components/    <- Reusable UXML fragments
|- Styles/        <- USS files and theme variables
`- Controllers/   <- C# MonoBehaviour controllers
```
