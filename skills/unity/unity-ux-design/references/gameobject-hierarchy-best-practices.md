# GameObject Hierarchy Best Practices for Mobile Game UI

> Derived from Layer Lab GUI Pro-SuperCasual DemoScene.unity analysis (5,624 GameObjects, 81 screens)

## 1. Root Canvas Structure

Every mobile game UI starts with a single root Canvas configured for mobile:

```
Canvas (Screen Space - Camera)
  +-- Panel                    // All screens container
  |     +-- Screen_Lobby       // Individual screens (81 in Layer Lab)
  |     +-- Screen_Shop
  |     +-- Popup_Settings
  |     +-- ...
  +-- PanelControl             // Persistent overlay controls
        +-- Button_Prev
        +-- Text_Title
        +-- Button_Next
```

**Key principles:**
- **One root Canvas** — never nest Canvas components unless performance requires it (draw call batching)
- **Panel** as the single container for all screens — toggle screen visibility by enabling/disabling child GameObjects
- **PanelControl** for persistent UI elements that survive screen transitions (navigation buttons, title bar)
- Canvas Render Mode: **Screen Space - Camera** (`m_RenderMode: 1`)

## 2. Screen Internal Structure

Every screen follows a consistent 3-4 section layout:

```
Screen_Lobby
  +-- Background              // Full-stretch background image
  +-- Top                     // Status bar, resource bar, title
  |     +-- Topbar            // Fixed header strip
  |     +-- Group_ResourceBar // Currency displays
  +-- Middle                  // Scrollable or fixed content area
  |     +-- Content           // Main interactive content
  +-- Bottom                  // Navigation bar, action buttons
        +-- BottomBar_Menu    // Tab navigation
```

### Section Naming Convention

| Section | Purpose | Anchor Pattern | Layer Lab Examples |
|---------|---------|----------------|-------------------|
| `Background` or `Bg` | Full-screen backdrop | Stretch all `{0,0}->{1,1}` | Every screen |
| `Top` / `Topbar` | Fixed header area | Top-stretch `{0,1}->{1,1}` | Resource bars, titles |
| `Middle` | Primary content | Stretch or center | Cards, lists, hero display |
| `Bottom` / `BottomBar_Menu` | Fixed footer area | Bottom-stretch `{0,0}->{1,0}` | Tab bars, action buttons |

## 3. Naming Conventions (PascalCase with Prefixes)

### Prefix System (from 5,624 GameObjects analysis)

| Prefix | Count | Usage | Examples |
|--------|-------|-------|----------|
| `Text_` | 491 | All TextMeshProUGUI labels | `Text_Title`, `Text_CC`, `Text_Username` |
| `Bg` / `Bg_` | 373 | Background images | `Bg`, `Bg_Top`, `Bg_Shadow` |
| `Icon_` | 301 | Icon images | `Icon_Coin`, `Icon_Gem`, `Icon_Star` |
| `Border` | 272 | Decorative borders/frames | `Border`, `Border_Top`, `Border_Bottom` |
| `Button_` | 248 | Interactive buttons | `Button_Play`, `Button_Close`, `Button_Buy` |
| `Image_` | 144 | Decorative/content images | `Image_Avatar`, `Image_Banner` |
| `Group_` | 127 | Layout containers | `Group_ResourceBar`, `Group_Price`, `Group_Buttons` |
| `Popup*` | 73 | Modal/popup screens | `Popup_Settings`, `PopupDim_Reward`, `PopupFull_LevelUp` |

### Screen Naming Patterns

| Pattern | Convention | Examples |
|---------|-----------|----------|
| Full pages | `Screen_` or descriptive | `Lobby`, `Shop`, `Collection_List` |
| Popups (centered panel) | `Popup_` | `Popup_LobbyChat`, `Popup_Player_Profile` |
| Popups (dimmed bg) | `PopupDim_` | `PopupDim_RewardSkin`, `PopupDim_Offline` |
| Popups (fullscreen) | `PopupFull_` | `PopupFull_LevelUp`, `PopupFull_CharacterLevelUp` |
| Gameplay UI | `Play_UI_` | `Play_UI_Action`, `Play_UI_Idle` |
| Stage variants | `Play_Stage_` | `Play_Stage_Select_1` through `_5` |

### Naming Rules

1. **PascalCase** with underscores for category separation: `Button_Play`, not `btnPlay` or `play-button`
2. **Prefix indicates type**, suffix indicates purpose: `Text_PlayerName`, `Icon_Currency_Gold`
3. **Numbered variants** use underscore + number: `Play_Stage_Select_1`, `Equipment_ItemInfoPopup_03`
4. **State variants** append state: `Play_Stage_Start_1_normal`, `Play_Stage_Start_1_hard`
5. **No abbreviations** except established ones: `Bg` (Background), `Btn` is NOT used (use `Button_`)

## 4. Component Organization per GameObject

### Typical Image GameObject
```
Icon_Coin                     // Name describes visual content
  [RectTransform]             // Position/anchoring
  [CanvasRenderer]            // Required for rendering
  [Image]                     // Visual content
  [Shadow]                    // Optional: drop shadow effect (611 instances in Layer Lab)
```

### Typical Button GameObject
```
Button_Play                   // Action-oriented name
  [RectTransform]
  [CanvasRenderer]
  [Image]                     // Button background/shape
  [Button]                    // Interaction handler
  [Shadow]                    // Optional depth effect
  +-- Text_Label              // Child: button text
       [RectTransform]
       [CanvasRenderer]
       [TextMeshProUGUI]
  +-- Icon_Arrow              // Optional child: button icon
       [RectTransform]
       [CanvasRenderer]
       [Image]
```

### Typical Layout Container
```
Group_ResourceBar             // Semantic container name
  [RectTransform]
  [HorizontalLayoutGroup]     // Layout component
  +-- Item_Energy             // Child items
  +-- Item_Coins
  +-- Item_Gems
```

### Typical Scroll List
```
ScrollView_Items              // Scroll container
  [RectTransform]
  [ScrollRect]                // Scroll behavior (vertical, elastic 0.1)
  [Image]                     // Optional: scroll background
  +-- Viewport                // Clipping mask
  |     [RectTransform]       // Stretch anchors
  |     [Mask]                // Clip children
  |     [Image]               // Required by Mask
  |     +-- Content           // Content container
  |           [RectTransform]
  |           [VerticalLayoutGroup]  // or GridLayoutGroup
  |           [ContentSizeFitter]    // Dynamic height: preferredSize
  |           +-- Item_Row_1
  |           +-- Item_Row_2
  |           +-- ...
  +-- Scrollbar_Vertical      // Optional scrollbar
```

## 5. Anchor Presets Reference

Layer Lab uses these anchor patterns consistently across 5,624 GameObjects:

| Anchor Preset | Min→Max | Count | When to Use |
|---------------|---------|-------|-------------|
| **Center** | `{0.5,0.5}→{0.5,0.5}` | 2,036 | Icons, buttons, cards, fixed-size elements |
| **Full Stretch** | `{0,0}→{1,1}` | 1,433 | Backgrounds, panels, viewports, overlays |
| **Top-Left** | `{0,1}→{0,1}` | 895 | Status icons, back buttons, labels |
| **Bottom Stretch-H** | `{0,0}→{1,0}` | 198 | Bottom navigation bars, footer panels |
| **Top Stretch-H** | `{0,1}→{1,1}` | 171 | Top bars, resource headers |

### Anchor Decision Tree

```
Is it a background/overlay?
  YES → Full Stretch {0,0}→{1,1}
  NO  → Does it span full width?
          YES → Is it at top?
                  YES → Top Stretch-H {0,1}→{1,1}
                  NO  → Bottom Stretch-H {0,0}→{1,0}
          NO  → Is it positioned relative to an edge?
                  YES → Use corner anchor (e.g., Top-Left {0,1})
                  NO  → Center {0.5,0.5}
```

## 6. Hierarchy Depth Guidelines

### Recommended Maximum Depths

| UI Element | Max Depth | Layer Lab Observed |
|-----------|-----------|-------------------|
| Canvas → Screen | 2 | `Canvas > Panel > Screen_Lobby` |
| Screen → Section | 3 | `Screen > Top > Topbar` |
| Section → Component | 4-5 | `Middle > Content > Card > Icon_Item` |
| Scroll → Item | 5-6 | `Middle > ScrollView > Viewport > Content > Item_Row` |
| **Total max** | **7-8** | Deepest paths in Layer Lab |

### Depth Optimization Rules

1. **Avoid unnecessary wrapper GameObjects** — don't add empty parents just for organization
2. **Use Layout Groups** instead of manual positioning siblings — reduces need for positioning wrappers
3. **Flatten where possible** — if a container has only one child, consider merging
4. **Group logically**, not visually — `Group_ResourceBar` contains related items, not "things that happen to be near each other"

## 7. Screen Management Pattern

### Visibility-Based Navigation
```csharp
// Layer Lab pattern: all screens under Panel, toggle active state
// Canvas > Panel > [81 screens] — only 1 active at a time

public void ShowScreen(string screenName)
{
    // Disable all screens
    foreach (Transform child in panelTransform)
        child.gameObject.SetActive(false);
    
    // Enable target screen
    panelTransform.Find(screenName)?.gameObject.SetActive(true);
}
```

### Screen Categories in Hierarchy Order
```
Panel
  +-- [Loading/Auth Screens]
  |     +-- Title_Loading
  |     +-- Title_Login
  |     +-- User_Name
  +-- [Main Screens]
  |     +-- Lobby
  |     +-- Shop
  |     +-- Collection_List
  |     +-- Equipment
  |     +-- Leaderboard_List
  |     +-- Friends_List
  +-- [Gameplay Screens]
  |     +-- Play_Stage_Select_1..5
  |     +-- Play_UI_Idle
  |     +-- Play_UI_Action
  +-- [Popups (centered)]
  |     +-- Popup_Settings
  |     +-- Popup_LobbyChat
  |     +-- Popup_Player_Profile
  +-- [Popups (dimmed)]
  |     +-- PopupDim_RewardSkin
  |     +-- PopupDim_Offline
  +-- [Popups (fullscreen)]
        +-- PopupFull_LevelUp
        +-- PopupFull_CharacterLevelUp
```

## 8. Popup Hierarchy Patterns

### Standard Popup (Centered Panel)
```
Popup_Settings
  +-- Dim                     // Full-stretch dark overlay (Image, alpha ~0.7)
  +-- Panel                   // Centered content panel
       +-- Top
       |     +-- Text_Title
       |     +-- Button_Close // Top-right, red square, white X
       +-- Middle
       |     +-- Content      // Popup-specific content
       +-- Bottom
             +-- Button_Confirm
             +-- Button_Cancel
```

### Dimmed Reward Popup
```
PopupDim_RewardSkin
  +-- Dim                     // Full-stretch dark overlay
  +-- Content                 // No panel — content floats over dim
       +-- Ribbon_Title       // Top banner/ribbon
       +-- Image_Reward       // Large centered reward visual
       +-- Text_Description   // Reward description
       +-- Text_TapToContinue // "Tap to Continue" prompt
```

### Fullscreen Celebration
```
PopupFull_LevelUp
  +-- Background              // Full-stretch gradient/glow effect
  +-- Content                 // Centered vertically
       +-- Ribbon_LevelUp     // Achievement banner
       +-- Badge_Level        // Large level number
       +-- Group_Rewards      // Horizontal reward row
       +-- Text_Continue      // "Tap to Continue"
```

## 9. Common Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | Correct Approach |
|-------------|-------------|-----------------|
| `GameObject_1`, `Panel (2)` | Meaningless names, impossible to debug | Use semantic names: `Button_Play`, `Panel_Shop` |
| Deep nesting for visual grouping | Performance overhead, hard to maintain | Use Layout Groups, flatten hierarchy |
| Multiple Canvas components | Unnecessary draw call overhead | Single root Canvas unless profiling shows need |
| Mixing UI and world-space objects | Z-fighting, sorting issues | Separate Canvas for each render mode |
| Hardcoded positions without anchors | Breaks on different resolutions | Always set meaningful anchors |
| Button without child Text/Icon | Invisible interaction area | Always include visual feedback child |
| ScrollRect without Viewport>Content | Clipping fails, scroll breaks | Follow Viewport>Content pattern exactly |

## 10. Prefab Organization

### Recommended Prefab Folder Structure
```
Assets/Prefabs/UI/
  +-- Screens/                // Full-screen prefabs
  |     +-- Screen_Lobby.prefab
  |     +-- Screen_Shop.prefab
  +-- Popups/                 // Modal/popup prefabs
  |     +-- Popup_Settings.prefab
  |     +-- PopupDim_Reward.prefab
  +-- Components/             // Reusable UI components
  |     +-- Component_ResourceBar.prefab
  |     +-- Component_ItemCard.prefab
  |     +-- Component_BottomNav.prefab
  +-- Templates/              // Empty structural templates
        +-- Template_Screen.prefab
        +-- Template_Popup.prefab
```

### Prefab Nesting Rules
1. **Screens** are top-level prefabs containing section structure
2. **Shared components** (resource bars, nav bars) are nested prefabs inside screens
3. **Item cards/rows** in scroll lists are separate prefabs instantiated at runtime
4. **Popups** are independent prefabs, instantiated/pooled as needed

---

*Reference: Layer Lab GUI Pro-SuperCasual DemoScene.unity — 5,624 GameObjects, 81 screens, 3,755 Images, 1,142 TextMeshProUGUI, 230 Buttons, 184 HorizontalLayoutGroups*
