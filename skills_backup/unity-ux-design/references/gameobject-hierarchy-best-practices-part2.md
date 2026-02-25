# GameObject Hierarchy Best Practices (Continued)

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
