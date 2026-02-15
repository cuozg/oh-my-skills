# Mobile UX Interaction Patterns for Game UI

## 1. Touch Interaction Design

### Touch Target Sizing
| Element Type | Min Size | Recommended |
|---|---|---|
| Primary CTA (Play, Buy) | 80×80 | 200-400×100-120 |
| Standard button | 60×60 | 150-300×70-90 |
| Icon button (Close, Add) | 44×44 | 60-80×60-80 |
| List row (tappable) | 44h | 70-100h |
| Tab bar item | 44×44 | screenW/tabCount × 60-80 |
| Grid cell | 44×44 | 100-200×100-200 |

### Touch Feedback (ColorTint)
```
Normal:      rgba(1.0, 1.0, 1.0, 1.0)
Pressed:     rgba(0.78, 0.78, 0.78, 1.0)
Disabled:    rgba(0.78, 0.78, 0.78, 0.5)
```
- Primary CTA: tint + optional scale 0.95. Icon: tint only. List Row: bg highlight.

### Touch Zones: **Top**: status/resources (view-only), **Middle**: content (scrollable), **Bottom third**: primary actions, nav tabs

## 2. Navigation Patterns

### Bottom Tab Navigation
| State | Visual | Behavior |
|---|---|---|
| Active | Colored icon + text + highlight bg | Show screen |
| Inactive | Grayscale icon, no label | Tap to switch |
| Notification | Red badge dot/number | Draw attention |
| Disabled | Grayed + lock icon | Level-gated |

### Back Navigation
- **Full pages**: Back button bottom-left
- **Popups**: Close button top-right (red, white X)
- **Celebrations**: "Tap to Continue" anywhere
- **Android back**: Dismiss topmost popup or navigate back

## 3. Modal/Popup Patterns

### Three Modal Families
| Family | Entry | Exit | Blocking |
|---|---|---|---|
| Centered Panel | Fade dim + scale 0.8→1.0 | Close btn → reverse | Yes, dim overlay |
| Reward Reveal | Fade dim + reward scales in | Tap anywhere | Yes, full takeover |
| Fullscreen Celebration | Full screen transition | Tap after animation | Yes |

### Popup Rules
- Max 2 popups stacked; closing returns to previous state
- Escape/Back closes topmost first
- Dim overlay: `rgba(0,0,0,0.7)`, raycastTarget=true

## 4. Scroll Patterns

### Configuration
```
Direction: Vertical only | Movement: Elastic | Elasticity: 0.1
Inertia: true | Deceleration: 0.135
```

### Content Types
| Type | Row Height | Layout | Interaction |
|---|---|---|---|
| Player list | 80-100 | VLG | Tap → detail popup |
| Card grid | 180-220 | GLG | Tap → detail view |
| Settings list | 60-80 | VLG | Toggle/tap |
| Chat | Variable | VLG | Scroll to read |

## 5. Button States

### State Machine
NORMAL → PRESSED (touch down) → NORMAL (touch up + action)
NORMAL ↔ DISABLED (condition)
Optional: LOADING (spinner), COOLDOWN (timer overlay)

### CTA Hierarchy
1. **Primary**: Yellow/Gold, largest — "PLAY", "CLAIM"
2. **Secondary**: Cyan/Blue, medium — "GO", "UPGRADE"
3. **Tertiary**: Gray/outlined, small — "SKIP", "CANCEL"
4. **Destructive**: Red, small, requires confirm — "DELETE"

### Notification Badges
- Red circle 24-36px, top-right of parent, partially overlapping
- "99+" for high counts, "!" for non-numeric
- Scale pop animation on appear

## 6. Progress Bars
| State | Fill Color | Meaning |
|---|---|---|
| Normal | Green | Standard |
| Warning | Yellow/Orange | Approaching limit |
| Critical | Red | At limit |
| Complete | Gold + glow | Reward claimable |

## 7. Transitions

### Screen: 0.2-0.3s fade/slide, block input during
### Popup Open: 0.2s, dim 0→0.7, panel scale 0.8→1.0 (ease-out-back)
### Popup Close: 0.15s (faster), reverse
### Reward Reveal: particle burst → item scale 0→1.2→1.0 → glow → count up (0.5-1.0s)
### List Items: Stagger 0.05s, slide from right + fade (0.2s each)

## 8. Error & Loading States

- **Button Loading**: Replace label with spinner, disable, timeout 10s → retry
- **Network Error**: Toast + auto-retry with backoff, after 3 fails → retry button
- **Validation Error**: Inline red text + shake animation
- **Toast**: Top/bottom strip, 2-3s auto-dismiss, non-blocking. Colors: Info=Blue, Success=Green, Warning=Yellow, Error=Red

## 9. Gesture Support

| Gesture | Action | Conflict Resolution |
|---|---|---|
| Tap | Primary interaction | Buttons > scroll |
| Vertical swipe | Scroll lists | Wins in scroll views |
| Horizontal swipe | Navigate pages | Passes through in vertical scroll |
| Long press (0.5s) | Tooltip/preview | Delay prevents accidental |
| Drag (10px threshold) | Adjust/rearrange | Threshold prevents jittery taps |
