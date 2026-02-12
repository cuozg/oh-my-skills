# UI Component Reference for Mobile Game UI

> Complete uGUI component inventory derived from Layer Lab GUI Pro-SuperCasual DemoScene.unity (5,624 GameObjects)

## Component Census

| Component | Count | Percentage | Role |
|-----------|-------|-----------|------|
| Image | 3,755 | 66.8% | Visual rendering (backgrounds, icons, borders, decorations) |
| TextMeshProUGUI | 1,142 | 20.3% | All text rendering |
| Shadow | 611 | 10.9% | Drop shadow effects |
| Mask | 247 | 4.4% | Content clipping (scroll views, shaped containers) |
| Button | 230 | 4.1% | Tap interactions |
| HorizontalLayoutGroup | 184 | 3.3% | Horizontal auto-layout |
| LayoutElement | 170 | 3.0% | Layout size control |
| ContentSizeFitter | 71 | 1.3% | Auto-sizing containers |
| VerticalLayoutGroup | 48 | 0.9% | Vertical auto-layout |
| Slider | 37 | 0.7% | Progress bars, volume controls |
| GridLayoutGroup | 16 | 0.3% | Grid layouts (calendars, item grids) |
| ScrollRect | 15 | 0.3% | Scrollable content areas |
| RectMask2D | 7 | 0.1% | Rectangular clipping (performance alternative to Mask) |
| TMP_InputField | 7 | 0.1% | Text input fields |
| Toggle | 4 | 0.1% | On/off switches |

**Not used in Layer Lab**: Legacy Text, AspectRatioFitter, Outline, Canvas (nested), legacy InputField

---

## 1. Image Component

**Count**: 3,755 (most used component)

### Usage Categories

| Category | Naming Pattern | Count (approx) | Configuration |
|----------|---------------|-----------------|---------------|
| Backgrounds | `Bg`, `Bg_*`, `Background` | 373 | Stretch anchors, sliced sprite |
| Icons | `Icon_*` | 301 | Center anchor, native size, Simple type |
| Borders/Frames | `Border`, `Border_*` | 272 | Stretch or center, sliced sprite |
| Button backgrounds | Part of `Button_*` | 248 | Center anchor, sliced sprite |
| Decorative | `Image_*` | 144 | Varies by context |
| Content images | Various | ~2,400 | Context-dependent |

### Image Type Settings

| Image Type | When to Use | Layer Lab Usage |
|-----------|-------------|-----------------|
| **Simple** | Icons, decorations, full-bleed backgrounds | Icons, small images |
| **Sliced** | Panels, buttons, borders (9-slice) | Most backgrounds, button shapes, borders |
| **Tiled** | Repeating patterns | Rare |
| **Filled** | Progress bars, radial indicators | Slider fills, cooldown overlays |

### Standard Configuration
```
[Image]
  Source Image: {sprite reference}
  Color: (1, 1, 1, 1)          // White tint (use sprite colors)
  Material: None                // Default UI material
  Raycast Target: false         // IMPORTANT: disable on non-interactive images
  Raycast Padding: 0,0,0,0
  Maskable: true
  Image Type: Sliced            // For panels/buttons (preserve corners)
  Pixels Per Unit: 100
```

### Performance Tips
- **Disable Raycast Target** on all decorative images (only enable on interactive elements)
- **Use sprite atlases** — Layer Lab packs sprites into atlases to minimize draw calls
- **Prefer Sliced** over stretched Simple for panels and buttons

---

## 2. TextMeshProUGUI Component

**Count**: 1,142

### Naming Convention
All text GameObjects use `Text_` prefix: `Text_Title`, `Text_Username`, `Text_Price`, `Text_Level`

### Text Hierarchy Tiers

| Tier | Usage | Approx Size | Style |
|------|-------|-------------|-------|
| **Display** | Screen titles, level-up numbers, prices | 48-72 | Bold, outlined, often colored |
| **Heading** | Section headers, card titles | 36-48 | Bold, white with shadow |
| **Body** | Descriptions, dialog text, stats | 24-32 | Regular, white or light gray |
| **Caption** | Timestamps, helper text, version | 16-20 | Regular, gray or semi-transparent |
| **Badge** | Notification counts, quantity labels | 14-18 | Bold, white on colored bg |

### Standard Configuration
```
[TextMeshProUGUI]
  Text: "Label"
  Font Asset: {TMP Font Asset}      // Use a rounded/cartoon font for super-casual
  Font Style: Bold                   // Most game UI text is bold
  Font Size: 36                      // Body default
  Auto Size: false                   // Prefer fixed sizes for consistency
  Color: (1, 1, 1, 1)              // White (colored via outline/shadow)
  Alignment: Center/Left             // Context-dependent
  Wrapping: Enabled
  Overflow: Ellipsis                 // Truncate gracefully
  Raycast Target: false              // Disable unless clickable
  
  // Common material settings for cartoon style:
  // - Outline: enabled, width 0.2-0.4, dark color
  // - Shadow/Underlay: enabled, soft, offset (1,-1)
```

### Text Best Practices
1. **Never use legacy `Text`** — always TextMeshProUGUI
2. **Disable Raycast Target** on all text (it's not clickable independently)
3. **Use outline + shadow** for readability over complex backgrounds
4. **Set overflow to Ellipsis** to prevent text from breaking layouts
5. **Use LayoutElement** on text containers if they participate in Layout Groups

---

## 3. Button Component

**Count**: 230

### Naming Convention
`Button_Play`, `Button_Close`, `Button_Buy`, `Button_Back`, `Button_Next`, `Button_Prev`

### Uniform Configuration (all 230 buttons in Layer Lab)
```
[Button]
  Interactable: true
  Transition: Color Tint           // ALL buttons use ColorTint
  Target Graphic: {self Image}
  Normal Color: (1, 1, 1, 1)              // Full white
  Highlighted Color: (0.96, 0.96, 0.96, 1) // Subtle darken
  Pressed Color: (0.784, 0.784, 0.784, 1)  // Noticeable darken
  Selected Color: (0.96, 0.96, 0.96, 1)
  Disabled Color: (0.784, 0.784, 0.784, 0.5) // Dimmed + transparent
  Color Multiplier: 1
  Fade Duration: 0.1
  Navigation: Automatic
```

### Button Hierarchy Pattern
```
Button_Play
  [RectTransform]
    Size: min 200×80 (touch-friendly)
  [CanvasRenderer]
  [Image]                    // Button background sprite (sliced)
  [Button]                   // Interaction (references Image above)
  [Shadow]                   // Optional depth effect
  +-- Text_Label             // Button text
  |     [TextMeshProUGUI]
  +-- Icon_Arrow             // Optional: leading/trailing icon
        [Image]
```

### Button Categories in Layer Lab

| Type | Visual | Color Theme | Size (approx) | Examples |
|------|--------|------------|---------------|----------|
| **Primary CTA** | Large pill/rounded | Yellow/Gold | 400×120 | `Button_Play`, `Button_Claim` |
| **Secondary** | Medium rounded | Cyan/Blue | 300×80 | `Button_Go`, `Button_Buy` |
| **Destructive** | Small rounded | Red | 80×80 | `Button_Close` (X icon) |
| **Navigation** | Icon-only or text | Blue/Dark | 80×80 | `Button_Back`, `Button_Next` |
| **Tab** | Pill or rectangle | Varies (active/inactive) | Flexible×60 | Tab bar buttons |
| **Utility** | Small icon | Gray/Blue | 60×60 | `Button_Add` (+), settings gear |

### Touch Target Minimum Sizes
- **Primary actions**: ≥ 120px height
- **Standard buttons**: ≥ 80px height  
- **Icon buttons**: ≥ 60×60px (with 44pt minimum touch area)
- **List item rows**: ≥ 80px height (entire row tappable)

---

## 4. Shadow Component

**Count**: 611

### Purpose
Adds soft drop shadows for depth/elevation in super-casual cartoon style.

### Standard Configuration
```
[Shadow]
  Effect Color: (0, 0, 0, 0.3)     // Semi-transparent black
  Effect Distance: (2, -2)          // Right and down offset
  Use Graphic Alpha: true
```

### Shadow Usage Pattern
- Applied to **buttons** for 3D beveled look
- Applied to **panels** for popup depth
- Applied to **text** (via TMP material, not Shadow component) for readability
- Applied to **cards** for separation from background
- **Not applied to**: small icons, decorative borders, background images

---

## 5. ScrollRect Component

**Count**: 15

### Uniform Configuration (all instances)
```
[ScrollRect]
  Content: {Content RectTransform}
  Horizontal: false                 // NEVER horizontal in Layer Lab
  Vertical: true
  Movement Type: Elastic            // Bouncy scroll feel (m_MovementType: 1)
  Elasticity: 0.1                   // Tight, responsive bounce
  Inertia: true
  Deceleration Rate: 0.135          // Standard friction
  Scroll Sensitivity: 1
  Viewport: {Viewport RectTransform}
  Vertical Scrollbar: {optional Scrollbar}
  Vertical Scrollbar Visibility: AutoHideAndExpandViewport
```

### Required Child Structure
```
ScrollView_Items
  [ScrollRect]
  +-- Viewport
  |     [RectTransform]  // Anchors: Full Stretch {0,0}→{1,1}
  |     [Mask] or [RectMask2D]
  |     [Image]          // Required by Mask (can be transparent)
  |     +-- Content
  |           [RectTransform]  // Anchors: Top {0,1}→{1,1}, Pivot: (0.5,1)
  |           [VerticalLayoutGroup] or [GridLayoutGroup]
  |           [ContentSizeFitter]  // Vertical: PreferredSize
  +-- Scrollbar_Vertical (optional)
```

### When to Use Each Layout in ScrollRect

| Content Type | Layout | Spacing | Examples |
|-------------|--------|---------|----------|
| List rows (friends, leaderboard) | VerticalLayoutGroup | 8-16 | Friends_List, Leaderboard |
| Card grid (shop, collection) | GridLayoutGroup | 12-24 | Collection_List, Shop items |
| Mixed content | VerticalLayoutGroup + nested HLG | 16-24 | Daily_Bonus_30Day |

---

## 6. Slider Component

**Count**: 37

### Usage in Mobile Games
- **Progress bars**: XP, health, energy, battle pass progress
- **Level indicators**: Character level, account level
- **Volume/settings**: Audio controls (rare — only in settings)

### Standard Progress Bar Configuration
```
Slider_XPBar
  [RectTransform]
    Size: flexible width × 30-40 height
  [Slider]
    Direction: Left To Right
    Min Value: 0
    Max Value: 1              // Normalize values
    Value: 0.65               // Current progress
    Whole Numbers: false
    Interactable: false       // Progress bars are NOT interactive
  +-- Background              // Bar background
  |     [Image] Color: dark gray
  +-- Fill_Area
  |     +-- Fill              // Colored fill
  |           [Image] Color: green/yellow
  +-- Handle_Slide_Area       // Hide for progress bars
        +-- Handle
              [Image] enabled: false  // Hidden for display-only bars
```

### Interactive Slider (Settings)
```
Slider_Volume
  [Slider]
    Interactable: true        // User can drag
    Whole Numbers: false
  +-- Background
  +-- Fill_Area
  |     +-- Fill [Image]
  +-- Handle_Slide_Area
        +-- Handle
              [Image]         // Visible drag handle
              Size: 40×40
```

---

## 7. Mask & RectMask2D

### Mask (247 instances)
```
[Mask]
  Show Mask Graphic: false    // Usually hide the mask shape
[Image]                       // Required companion — defines clip shape
  Sprite: {round rect or custom shape}
```

### RectMask2D (7 instances)
```
[RectMask2D]
  Padding: 0,0,0,0
  // No Image required
  // Rectangular clipping only
```

### When to Use Which

| Scenario | Use | Why |
|----------|-----|-----|
| Scroll view clipping | RectMask2D | Better performance, rectangular is fine |
| Rounded avatar frame | Mask | Need circular/rounded clipping |
| Card with rounded corners | Mask | Non-rectangular shape |
| Simple panel overflow | RectMask2D | Performance |

---

## 8. Layout Groups — Quick Reference

### HorizontalLayoutGroup (184 instances)

| Property | Resource Bar | Nav Bar | Price Group |
|----------|-------------|---------|-------------|
| Spacing | 100 | 0 | 8 |
| Alignment | UpperCenter (5) | MiddleCenter (7) | MiddleLeft (4) |
| Control Width | false | false | false |
| Control Height | false | false | false |
| Force Expand W | false | true | false |

### VerticalLayoutGroup (48 instances)
Primarily used in: scroll content, popup body sections, settings panels

### GridLayoutGroup (16 instances)

| Property | Button Grid | Calendar | Item Grid |
|----------|------------|----------|-----------|
| Cell Size | 409×105 | 140×160 | 180×200 |
| Spacing | 36×25 | 12×12 | 16×16 |
| Constraint | FixedColumnCount | FixedColumnCount | FixedColumnCount |
| Columns | 2 | 6 | 3-4 |

### LayoutElement (170 instances)
```
[LayoutElement]
  Min Width: -1              // -1 = ignored
  Min Height: -1
  Preferred Width: 200       // Target size in layout
  Preferred Height: 80
  Flexible Width: 1          // Grow factor (like CSS flex-grow)
  Flexible Height: 0
  Layout Priority: 1         // Higher = stronger override
```

---

## 9. TMP_InputField

**Count**: 7

### Standard Configuration
```
InputField_Username
  [RectTransform]
    Size: stretch width × 80 height
  [Image]                     // Input background (sliced sprite)
  [TMP_InputField]
    Text Component: {child TextMeshProUGUI}
    Placeholder: {child Text_Placeholder}
    Content Type: Standard    // or Alphanumeric, EmailAddress, Password
    Line Type: Single Line
    Character Limit: 20       // Appropriate for usernames
    Caret Color: white
    Selection Color: (0.3, 0.6, 1, 0.5)
  +-- Text_Area
        +-- Text_Placeholder
        |     [TextMeshProUGUI]
        |       Text: "Enter username..."
        |       Color: (1,1,1,0.5)     // Dimmed placeholder
        +-- Text_Input
              [TextMeshProUGUI]
              Color: (1,1,1,1)         // Full white input text
```

### Input Field Types in Layer Lab
- **Username**: `User_Name` screen — `ContentType: Standard`, `CharacterLimit: 20`
- **Chat**: `Popup_LobbyChat` — `ContentType: Standard`, `LineType: SingleLine`
- **Email**: `Login_Email` — `ContentType: EmailAddress`
- **Search**: Friends invite — `ContentType: Standard`

---

## 10. Toggle Component

**Count**: 4

### Standard Configuration
```
Toggle_Setting
  [RectTransform]
    Size: 80×40
  [Toggle]
    Is On: false
    Transition: Color Tint
    Graphic: {Checkmark Image}
    Group: {optional ToggleGroup for radio behavior}
  +-- Background
  |     [Image]             // Toggle track
  +-- Checkmark
        [Image]             // Toggle knob/checkmark
```

### Toggle Use Cases
- **Settings**: Sound on/off, notifications on/off
- **Tab selection**: When using ToggleGroup for mutually exclusive tabs
- **Checkbox**: Remember me, accept terms

---

## 11. Component Combination Patterns

### Resource Display (Icon + Value + Add Button)
```
Item_Coins
  [HorizontalLayoutGroup] spacing=4
  +-- Icon_Coin [Image]           // Currency icon
  +-- Text_Amount [TextMeshProUGUI]  // "1,234"
  +-- Button_Add [Button+Image]   // "+" button
        +-- Icon_Plus [Image]
```

### Item Card (Icon + Name + Rarity)
```
Card_Item
  [Image]                         // Card background (sliced)
  [Button]                        // Tappable
  [Shadow]
  +-- Icon_Item [Image]           // Item icon
  +-- Text_Name [TextMeshProUGUI] // Item name
  +-- Text_Quantity [TextMeshProUGUI] // "x5"
  +-- Image_RarityBorder [Image]  // Color-coded border
  +-- Badge_New [Image+Text]      // Optional "NEW" badge
```

### Leaderboard Row (Rank + Avatar + Name + Score)
```
Row_Player
  [HorizontalLayoutGroup] spacing=12
  [Image]                         // Row background
  [Button]                        // Tappable for details
  +-- Text_Rank [TextMeshProUGUI] // "#4"
  +-- Image_Avatar [Image+Mask]   // Circular avatar
  +-- Text_Name [TextMeshProUGUI] // Player name (flexible width)
  |     [LayoutElement] flexibleWidth=1
  +-- Text_Score [TextMeshProUGUI] // "12,345"
```

---

*Reference: Layer Lab GUI Pro-SuperCasual DemoScene.unity — 5,624 GameObjects with the component distribution detailed above. All configurations extracted from actual scene data.*
