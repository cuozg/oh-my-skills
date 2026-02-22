# Mobile UX Interaction Patterns — Advanced

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
