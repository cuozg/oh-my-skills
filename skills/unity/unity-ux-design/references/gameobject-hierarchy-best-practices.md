# GameObject Hierarchy Best Practices for Mobile Game UI

> From Layer Lab GUI Pro-SuperCasual (5,624 GameObjects, 81 screens)

## 1. Root Canvas Structure
```
Canvas (Screen Space - Camera)
  +-- Panel                    // All screens container (toggle visibility)
  |     +-- Screen_Lobby
  |     +-- Screen_Shop
  |     +-- Popup_Settings
  +-- PanelControl             // Persistent overlay (nav buttons, title)
```
One root Canvas. Panel = single container for all screens.

## 2. Screen Internal Structure
```
Screen_Lobby
  +-- Background              // Full-stretch
  +-- Top                     // Status bar, resources
  +-- Middle                  // Main content (scrollable/fixed)
  +-- Bottom                  // Nav bar, actions
```

| Section | Anchor | Purpose |
|---|---|---|
| Background/Bg | Stretch all {0,0}→{1,1} | Full-screen backdrop |
| Top/Topbar | Top-stretch {0,1}→{1,1} | Fixed header |
| Middle | Stretch or center | Primary content |
| Bottom | Bottom-stretch {0,0}→{1,0} | Fixed footer |

## 3. Naming Conventions (PascalCase + Prefixes)

| Prefix | Usage | Examples |
|---|---|---|
| `Text_` | TMP labels | `Text_Title`, `Text_Username` |
| `Bg`/`Bg_` | Background images | `Bg`, `Bg_Top` |
| `Icon_` | Icons | `Icon_Coin`, `Icon_Star` |
| `Button_` | Buttons | `Button_Play`, `Button_Close` |
| `Group_` | Layout containers | `Group_ResourceBar`, `Group_Price` |
| `Popup_` | Centered popup | `Popup_Settings` |
| `PopupDim_` | Dimmed bg popup | `PopupDim_RewardSkin` |
| `PopupFull_` | Fullscreen popup | `PopupFull_LevelUp` |

PascalCase + underscore. Prefix=type, suffix=purpose. Numbered: `_01`, `_02`. No abbreviations except `Bg`.

## 4. Component Organization

### Button
```
Button_Play (RectTransform, Image, Button, Shadow?)
  +-- Text_Label (TMP)
  +-- Icon_Arrow? (Image)
```

### Scroll List
```
ScrollView_Items (ScrollRect: vertical, elastic 0.1)
  +-- Viewport (Mask) → Content (VLG + ContentSizeFitter: preferredSize)
      +-- Item_Row_1, Item_Row_2, ...
```

## 5. Anchor Presets

| Preset | Min→Max | When |
|---|---|---|
| Center | {0.5,0.5}→{0.5,0.5} | Fixed-size elements |
| Full Stretch | {0,0}→{1,1} | Backgrounds, overlays |
| Top Stretch-H | {0,1}→{1,1} | Top bars |
| Bottom Stretch-H | {0,0}→{1,0} | Bottom bars |

Decision: Background? → Full Stretch. Full width? → Top/Bottom Stretch. Edge-relative? → Corner anchor. Otherwise → Center.

## 6. Depth Guidelines

| Element | Max Depth |
|---|---|
| Canvas → Screen | 2 |
| Screen → Section | 3 |
| Section → Component | 4-5 |
| Scroll → Item | 5-6 |
| **Total max** | **7-8** |

Avoid unnecessary wrappers. Flatten single-child containers.

## 7. Popup Patterns

### Standard: `Popup_` → Dim (overlay) + Panel → Top (Title, Close) + Middle (Content) + Bottom (Confirm, Cancel)
### Dimmed Reward: `PopupDim_` → Dim + Content (Ribbon, Reward image, "Tap to Continue")
### Fullscreen: `PopupFull_` → Background (gradient/glow) + Content (Banner, Badge, Rewards, Continue)

## 8. Anti-Patterns

| Bad | Fix |
|---|---|
| `GameObject_1`, `Panel (2)` | Semantic names: `Button_Play` |
| Deep nesting for visual grouping | Layout Groups, flatten |
| Multiple Canvas components | Single root unless profiling requires |
| Hardcoded positions | Meaningful anchors |
| ScrollRect without Viewport>Content | Follow pattern exactly |

## 9. Prefab Organization
```
Assets/Prefabs/UI/
  Screens/     → Screen_Lobby.prefab
  Popups/      → Popup_Settings.prefab
  Components/  → Component_ResourceBar.prefab
  Templates/   → Template_Screen.prefab
```
Screens=top-level. Shared=nested prefabs. List items=separate prefabs for instantiation.
