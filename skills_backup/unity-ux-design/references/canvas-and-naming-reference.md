# Canvas Configuration & Naming Reference

Standard Canvas setup and naming conventions for mobile game UI.

## Canvas Configuration

```
Canvas (Screen Space - Camera)
├── CanvasScaler: ScaleWithScreenSize, ref 1080×1920, matchWidthOrHeight=0.5
├── GraphicRaycaster
└── SafeArea (stretch all, script adjusts for notch)
    ├── Screen_Lobby (one per screen, toggle active)
    ├── Screen_Shop
    └── PopupLayer
```

### Configuration Details

- `matchWidthOrHeight`: 0=portrait (width-constrained), 0.5=mixed, 1=landscape (height-constrained)
- Screens are direct children of SafeArea, activated/deactivated for navigation
- Popups in separate PopupLayer above all screens
- Never hardcode pixel positions — use Layout Groups and anchoring

## Naming Conventions

| Prefix | Example |
|--------|---------|
| `Screen_` | `Screen_Lobby`, `Screen_Shop` |
| `Panel_` | `Panel_Header`, `Panel_Content` |
| `Group_` | `Group_ResourceBar`, `Group_Buttons` |
| `Button_` | `Button_Play`, `Button_Close` |
| `Text_` | `Text_Title`, `Text_Score` |
| `Icon_` | `Icon_Coin`, `Icon_Star` |
| `Popup_` | `Popup_Reward`, `Popup_Settings` |
| `Item_` | `Item_LeaderboardRow`, `Item_ShopCard` |

## Layer Organization

Use consistent naming to keep hierarchy readable:
- **Top level**: Screens (visible one at a time)
- **Screen level**: Panels (Header, Content, Bottom)
- **Panel level**: Groups and Components
- **Component level**: Interactive elements (Button, Toggle) and text/images

Maximum hierarchy depth: 8 levels for complex screens.
