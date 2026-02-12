# Mobile UX Interaction Patterns for Game UI

> Touch, navigation, modal, scroll, and feedback patterns derived from Layer Lab GUI Pro-SuperCasual analysis and mobile game UX best practices

## 1. Touch Interaction Design

### Touch Target Sizing

| Element Type | Minimum Size | Recommended | Layer Lab Observed |
|-------------|-------------|-------------|-------------------|
| Primary CTA (Play, Buy) | 80×80 px | 200-400×100-120 px | Large yellow pill buttons |
| Standard button | 60×60 px | 150-300×70-90 px | Medium colored buttons |
| Icon button (Close, Add) | 44×44 px | 60-80×60-80 px | Red X close, blue + add |
| List row (tappable) | 44 px height | 70-100 px height | Leaderboard/friends rows |
| Tab bar item | 44×44 px | Screen width / tab count × 60-80 | Bottom nav tabs |
| Grid cell | 44×44 px | 100-200×100-200 px | Shop items, daily bonus cells |

### Touch Feedback Patterns

#### Color Tint Feedback (Layer Lab standard — all 230 buttons)
```
Normal:      rgba(1.0, 1.0, 1.0, 1.0)   // Full brightness
Highlighted: rgba(0.96, 0.96, 0.96, 1.0) // Subtle hover/focus
Pressed:     rgba(0.78, 0.78, 0.78, 1.0) // Noticeable darken on press
Disabled:    rgba(0.78, 0.78, 0.78, 0.5) // Dimmed + transparent
```

#### Button Press Behaviors
```
Primary CTA:
  - Press: Color tint darken + optional scale 0.95
  - Release: Trigger action + color restore
  - Disabled: Gray tint + 50% alpha + no interaction

Icon Button:
  - Press: Color tint darken
  - Release: Trigger action
  - No scale animation (too small)

List Row:
  - Press: Row background highlight color
  - Release: Navigate or show popup
```

### Touch Zones (Thumb Reachability)

```
┌─────────────────────┐
│  HARD TO REACH      │  ← Status bar, resource displays (view-only)
│  (top of screen)    │
├─────────────────────┤
│                     │
│  MODERATE REACH     │  ← Content area (scrollable)
│  (middle)           │
│                     │
├─────────────────────┤
│  EASY REACH         │  ← Primary actions, navigation
│  (bottom third)     │  ← Layer Lab: PLAY button, bottom tab bar
└─────────────────────┘
```

**Layer Lab implementation**: 
- Primary CTA (`Button_Play`) positioned in bottom third
- Bottom tab bar (`BottomBar_Menu`) at very bottom
- Resource bar (view-only) at top — no frequent interaction needed
- Side floating buttons (Friends, Ranking) in middle for occasional access

## 2. Navigation Patterns

### Bottom Tab Navigation (Layer Lab: `BottomBar_Menu`)

```
BottomBar_Menu
  [HorizontalLayoutGroup] spacing=0, forceExpandWidth=true
  +-- Tab_Home        // Active: colored icon + label, scaled up
  +-- Tab_Shop        // Inactive: gray icon, no label
  +-- Tab_Play        // Center: often larger, special styling
  +-- Tab_Social      // With notification badge
  +-- Tab_Profile
```

**Tab State Management**:
| State | Visual | Behavior |
|-------|--------|----------|
| Active | Colored icon + text label + highlight bg | Show corresponding screen |
| Inactive | Grayscale icon, no label | Tap to switch |
| Notification | Red badge dot/number on icon | Draw attention |
| Disabled | Grayed out + lock icon | Cannot access (level-gated) |

### Screen-to-Screen Navigation

```
Navigation Flow:
  Lobby ──[Tab]──→ Shop
  Lobby ──[Tab]──→ Social ──[Row tap]──→ Player Profile (popup)
  Lobby ──[Button]──→ Play Stage Select ──[Stage tap]──→ Stage Start (popup)
  Any Screen ──[Back]──→ Previous Screen
```

**Back Navigation**:
- **Full pages**: Back button at bottom-left (Layer Lab: `Button_Prev`)
- **Popups**: Close button at top-right (red square, white X)
- **Fullscreen celebrations**: "Tap to Continue" anywhere
- **Android back button**: Should dismiss current popup or navigate back

### Side Navigation (Layer Lab: Lobby floating buttons)

```
Left side:                    Right side:
  Button_Friends               Button_Ranking
  Button_Gift                  Button_Clan
                               Button_Quest
```

- Positioned in middle vertical zone for thumb access
- Semi-transparent or small when not focused
- May have notification badges
- Animate in/out with screen transitions

## 3. Modal/Popup Interaction Patterns

### Three Modal Families (from Layer Lab)

#### Family 1: Centered Panel Popup (`Popup_*`)
```
Trigger: Button tap or event
Entry: Fade in dim (0→0.7 alpha) + scale panel (0.8→1.0)
Interaction: Content within panel, close at top-right
Exit: Tap close → fade out dim + scale down panel
Blocking: Yes — dim blocks interaction with parent screen
```

**Close button behavior**:
- Position: Top-right corner of panel
- Visual: Red square with white X icon
- Size: 60×60 px minimum
- Tap area: Extends slightly beyond visual bounds

#### Family 2: Dimmed Reward Reveal (`PopupDim_*`)
```
Trigger: Reward earned event
Entry: Fade in dim + reward slides/scales in from center
Interaction: View reward, no close button
Exit: "Tap to Continue" — tap anywhere to dismiss
Blocking: Yes — full screen takeover
```

#### Family 3: Fullscreen Celebration (`PopupFull_*`)
```
Trigger: Level up, milestone, achievement
Entry: Full screen transition (fade/wipe)
Interaction: View achievement, auto-play reward animation
Exit: "Tap to Continue" — tap anywhere after animation completes
Blocking: Yes — nothing else is accessible
```

### Popup Stacking Rules
1. **Maximum 2 popups stacked** — avoid deeper nesting
2. **New popup dims over previous popup** if stacking
3. **Closing returns to previous state** — maintain navigation stack
4. **Escape/Back always closes topmost** popup first

### Dim Overlay Behavior
```
Dim_Background
  [Image]
    Color: (0, 0, 0, 0.7)          // 70% black overlay
    Raycast Target: true             // Block touches to parent screen
  [Button]                           // Optional: tap dim to close popup
    onClick: ClosePopup()
```

## 4. Scroll Interaction Patterns

### Vertical List Scroll (Layer Lab: all 15 ScrollRects)

```
Configuration:
  Direction: Vertical only
  Movement: Elastic (bounce at edges)
  Elasticity: 0.1 (tight, responsive)
  Inertia: true
  Deceleration: 0.135
```

**Scroll UX Guidelines**:
| Aspect | Guideline | Layer Lab Implementation |
|--------|-----------|------------------------|
| Direction | Single-axis only (vertical) | horizontal=false, vertical=true |
| Overscroll | Elastic bounce, not hard stop | movementType=Elastic, elasticity=0.1 |
| Velocity | Natural deceleration with inertia | inertia=true, decelerationRate=0.135 |
| Indicators | Scrollbar auto-hides | AutoHideAndExpandViewport |
| Content | Dynamic height via ContentSizeFitter | Vertical Fit: PreferredSize |

### Scroll Content Types

| Content Type | Row Height | Spacing | Layout | Interaction |
|-------------|-----------|---------|--------|-------------|
| Player list (leaderboard, friends) | 80-100 | 8-12 | VLG | Tap row → detail popup |
| Card grid (collection, shop) | 180-220 | 16-24 | GLG | Tap card → detail view |
| Settings list | 60-80 | 4-8 | VLG | Toggle/tap action |
| Chat messages | Variable | 8 | VLG | Scroll to read |
| Reward calendar | 140-160 | 12 | GLG | Tap cell → claim |

### Pull-to-Refresh (if applicable)
```
Not implemented in Layer Lab, but standard mobile pattern:
  Pull down beyond top → Show refresh spinner
  Release → Trigger data reload
  Complete → Snap back to top
```

## 5. Button State & Feedback Patterns

### State Machine for Game Buttons

```
States:
  NORMAL     → Button visible, tappable
  HIGHLIGHTED → Finger hovering (touch devices: N/A, but kept for controller)
  PRESSED    → Finger down, visual feedback active
  DISABLED   → Grayed out, not tappable
  LOADING    → Spinner replaces label, not tappable
  COOLDOWN   → Timer overlay, temporarily disabled
  
Transitions:
  NORMAL → PRESSED (on touch down)
  PRESSED → NORMAL (on touch up + action triggered)
  NORMAL → DISABLED (when condition not met)
  DISABLED → NORMAL (when condition met again)
```

### CTA (Call-to-Action) Button Hierarchy

```
Visual Priority (highest to lowest):
  1. Primary CTA:    Yellow/Gold, largest, prominent position
                     Example: "PLAY", "CLAIM", "BUY"
  2. Secondary CTA:  Cyan/Blue, medium, below primary
                     Example: "GO", "UPGRADE", "SHARE"  
  3. Tertiary:       Gray/outlined, small
                     Example: "SKIP", "LATER", "CANCEL"
  4. Destructive:    Red, small, requires confirmation
                     Example: "DELETE", "CLOSE"
```

### Notification Badges

```
Badge_Notification
  [Image]                    // Red circle/pill
    Color: (1, 0.2, 0.2, 1) // Bright red
    Size: 24-36 px diameter
  +-- Text_Count
        [TextMeshProUGUI]
        Font Size: 14-18
        Text: "3" or "!"    // Count or alert indicator
        
Position: Top-right corner of parent button/icon
Anchor: (1, 1) relative to parent
Offset: Partially overlapping parent edge
```

**Badge visibility rules**:
- Show when count > 0
- "99+" for counts exceeding 99
- "!" (exclamation) for non-numeric alerts
- Hide immediately when user views/claims content
- Animate on appearance (scale pop)

## 6. Progress Bar Interaction

### Display-Only Progress Bar
```
Slider_XPProgress
  [Slider] interactable=false
  Visual: Filled bar with percentage text overlay
  Animation: Smooth lerp to new value over 0.3-0.5s
  Text overlay: "1,234 / 2,000" or "62%"
```

### Interactive Progress (Slider)
```
Slider_Volume
  [Slider] interactable=true
  Visual: Track + draggable handle
  Feedback: Value updates in real-time as user drags
  Snap: Optional snap to nearest 0.1 increment
```

### Progress Bar Visual States
| State | Fill Color | Behavior |
|-------|-----------|----------|
| Normal | Green | Standard progress |
| Warning | Yellow/Orange | Approaching limit (energy low) |
| Critical | Red | At limit or overdue |
| Complete | Gold with glow | Reward ready to claim |
| Locked | Gray | Feature not unlocked |

## 7. Transition Patterns

### Screen Transitions
```
Full Page Switch:
  Duration: 0.2-0.3s
  Old screen: Fade out (alpha 1→0) or slide out
  New screen: Fade in (alpha 0→1) or slide in
  During transition: Block all input (raycast blocker)

Popup Open:
  Duration: 0.2s
  Dim: Alpha 0→0.7 (ease-out)
  Panel: Scale 0.8→1.0 + Alpha 0→1 (ease-out-back)

Popup Close:
  Duration: 0.15s (faster than open)
  Dim: Alpha 0.7→0
  Panel: Scale 1.0→0.8 + Alpha 1→0
```

### Item Animations
```
Reward Reveal:
  1. Background particle burst
  2. Item scales from 0→1.2→1.0 (overshoot)
  3. Glow pulse
  4. Quantity number counts up
  Duration: 0.5-1.0s total

List Item Appear:
  Stagger: 0.05s between items
  Each item: Slide from right + fade in
  Duration: 0.2s per item

Notification Badge:
  Appear: Scale 0→1.3→1.0 (pop effect)
  Pulse: Optional gentle scale 1.0→1.1→1.0 loop
```

## 8. Error & Loading States

### Loading States
```
Loading Screen:
  - Full screen with game art background
  - Progress bar (real or fake)
  - Tip text rotating

Button Loading:
  - Replace label with spinner icon
  - Disable interaction
  - Timeout after 10s → show retry

Content Loading:
  - Placeholder skeletons in list
  - Shimmer animation on placeholders
  - Replace with real content when loaded
```

### Error Handling
```
Network Error:
  - Toast notification (top or bottom strip)
  - "Connection lost. Retrying..."
  - Auto-retry with exponential backoff
  - After 3 failures → retry button

Validation Error:
  - Inline red text below input field
  - Shake animation on invalid field
  - Clear error on next input change

Purchase Error:
  - Popup with error message
  - "Insufficient gems" with link to shop
  - Never silently fail on purchases
```

### Toast Notifications (Layer Lab: `99_Popup_Toast.png`)
```
Toast_Notification
  Position: Top or bottom, full width
  Duration: 2-3 seconds, auto-dismiss
  Types:
    Info:    Blue strip, info icon
    Success: Green strip, checkmark icon
    Warning: Yellow strip, exclamation icon
    Error:   Red strip, X icon
  Animation: Slide in from edge, pause, slide out
  Behavior: Non-blocking (user can interact with screen behind)
```

## 9. Gesture Support

### Supported Gestures in Mobile Game UI
| Gesture | Where | Action |
|---------|-------|--------|
| **Tap** | Everywhere | Primary interaction |
| **Swipe vertical** | Scroll lists | Scroll content |
| **Swipe horizontal** | Stage select, carousels | Navigate between pages |
| **Long press** | Item cards | Show tooltip/preview |
| **Pinch** | Maps, images (rare) | Zoom |
| **Drag** | Sliders, equipment slots | Adjust value, rearrange |

### Gesture Conflict Resolution
1. **Vertical scroll wins** in scroll views — horizontal swipes pass through
2. **Buttons take priority** over scroll — short tap on button triggers it, drag initiates scroll
3. **Long press delay**: 0.5s before triggering (prevents accidental activation)
4. **Drag threshold**: 10px movement before scroll/drag initiates (prevents jittery taps)

---

*Reference: Layer Lab GUI Pro-SuperCasual — 230 buttons (uniform ColorTint), 15 ScrollRects (vertical elastic), 81 screens with consistent navigation patterns, 3 modal families*
