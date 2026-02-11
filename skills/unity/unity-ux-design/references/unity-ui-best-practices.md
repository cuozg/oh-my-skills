# Unity UI Best Practices Reference

Quick-reference guide for UX specification authors. Use these guidelines when populating UX spec sections.

---

## Canvas & Layout

### Canvas Scaler Settings

| Mode | Use Case | Reference Resolution |
|------|----------|---------------------|
| Scale With Screen Size | Mobile games (primary) | 1080×1920 (portrait) or 1920×1080 (landscape) |
| Constant Pixel Size | Editor tools, fixed-resolution UI | N/A |
| Constant Physical Size | Accessibility-critical UI | N/A |

- **Match Width Or Height**: Set slider to 0.5 for balanced scaling; use 1 (height) for portrait-dominant games, 0 (width) for landscape-dominant.
- **Pixels Per Unit**: Default 100. Only change if sprites use a different PPU.

### Layout Best Practices

- Use **anchors** to pin UI elements to screen edges or parent bounds — avoid absolute pixel positions.
- Prefer **Layout Groups** (Vertical, Horizontal, Grid) over manual positioning for lists, grids, and stacked content.
- Use **Content Size Fitter** + **Layout Element** for dynamic text that needs to grow/shrink.
- Set **Pivot** intentionally — it affects scaling, rotation origin, and anchor-relative positioning.
- Nest **RectTransform** containers to create logical groups (header, body, footer).

---

## Touch Targets & Input

### Minimum Touch Target Sizes

| Platform | Minimum Size | Recommended Size |
|----------|-------------|-----------------|
| iOS (Apple HIG) | 44×44 pt | 48×48 pt |
| Android (Material) | 48×48 dp | 56×56 dp |
| Unity (practical) | 44×44 units (at reference res) | 48×48 units |

- **Never** place interactive elements smaller than 44×44 at reference resolution.
- Maintain **8px minimum spacing** between adjacent touch targets.
- For thumb-reachable zones on mobile, place primary actions in the **bottom 60%** of the screen.
- Use **EventSystem** with a single **Graphic Raycaster** per Canvas where possible.

### Input Considerations

- Support both tap and hold where contextually appropriate (e.g., buttons with long-press for info).
- Provide **visual feedback** on press (scale, color shift, or highlight) within 100ms.
- Implement **swipe gestures** via `IBeginDragHandler`/`IDragHandler`/`IEndDragHandler` — not raw touch deltas.
- For scrollable lists, use **ScrollRect** with **Scroll Snap** components for paginated content.

---

## Text & Typography

### Text Sizing

| Element | Min Font Size | Recommended |
|---------|--------------|-------------|
| Body text | 14sp | 16–18sp |
| Captions / labels | 12sp | 14sp |
| Headings | 18sp | 20–24sp |
| Buttons | 14sp | 16–18sp |

- Use **TextMeshPro** (TMP) — never legacy `UnityEngine.UI.Text`.
- Enable **Auto Size** with min/max bounds for text that must fit variable containers.
- Set **overflow mode** to Ellipsis or Truncate for bounded text fields — never allow text to clip silently.
- Use **Rich Text** tags for inline styling rather than multiple text objects.

### Localization-Ready Text

- **Never hardcode strings** — use localization keys.
- Design text containers to handle **150% expansion** (English → German/French).
- Right-to-left (RTL) languages: use TMP's RTL support, mirror layout anchors.
- Avoid text inside sprites/textures — it cannot be localized.

---

## Accessibility

### Visual Accessibility

- Maintain **WCAG AA contrast ratio** (4.5:1 for normal text, 3:1 for large text).
- Do not rely on **color alone** to convey state — use icons, labels, or patterns alongside color.
- Support **Dynamic Type / text scaling** — UI must remain functional at 1.5× text size.
- Provide **focus indicators** for gamepad/keyboard navigation (highlight ring or glow).

### Motor Accessibility

- Avoid time-critical tiny targets — provide generous tap windows.
- Support **alternative input**: gamepad, keyboard, switch control where applicable.
- Implement **navigation order** via Unity's `Selectable.navigation` — don't rely on spatial auto-navigation alone.

### Screen Readers

- If targeting accessibility-certified builds, add `AccessibleLabel` components to interactive elements.
- Group related elements with `AccessibleGroup` for logical reading order.

---

## Safe Areas & Notches

- Use **Screen.safeArea** to inset UI away from notches, rounded corners, and system bars.
- Apply safe area padding to the **outermost Canvas container** — not individual elements.
- Test with notch simulators: iPhone (Dynamic Island, notch), Android (punch-hole, cutout).
- **Bottom safe area**: Account for home indicator (iOS) and gesture navigation bar (Android).

---

## Performance

### Canvas Optimization

- Split UI into **multiple Canvases** — static elements on one Canvas, frequently-changing elements on another.
- Avoid modifying elements on a Canvas with many children — it triggers full Canvas rebuild.
- Use **Canvas Group** for batch alpha/interactability changes instead of per-element toggling.
- Disable **Raycast Target** on non-interactive elements (backgrounds, decorations, labels).

### Image & Sprite Optimization

- Use **Sprite Atlases** — group sprites by screen/feature for efficient batching.
- Prefer **9-slice sprites** for resizable backgrounds over large full-resolution images.
- Use **Image Type: Sliced** for panels/borders, **Tiled** for repeating patterns.
- Target **max 2048×2048** atlas size for mobile; **4096×4096** for desktop.

### Object Pooling for UI

- Pool frequently shown/hidden elements (list items, notification badges, popups).
- Use `SetActive(false)` + reposition rather than `Instantiate`/`Destroy`.
- Pre-warm pools during loading screens, not during gameplay.

---

## Navigation & Flow

### Screen Transitions

- Use **consistent transition patterns**: slide for forward navigation, slide-back for return, fade for modals.
- Transition duration: **200–300ms** for most transitions; **150ms** for small elements.
- Use **CanvasGroup.alpha** for fade transitions — it's cheaper than material property animation.
- Block input during transitions to prevent double-taps and race conditions.

### Modal & Popup Patterns

- Modals should **dim the background** (overlay with 50–70% opacity black).
- Provide explicit **close affordance** (X button, tap-outside-to-close, or back button).
- Stack modals with a **modal manager** — never allow untracked popup layering.
- Back button (Android) / swipe-back (iOS) should close the topmost modal.

### Navigation Architecture

- Maintain a **screen stack** for back-navigation support.
- Use a **screen manager / router** pattern — screens don't know about each other directly.
- Deep-link support: every screen should be reachable by ID/route for server-driven navigation.

---

## State Management

### Element States

Every interactive element should define these states:

| State | Visual Treatment | Example |
|-------|-----------------|---------|
| Default | Normal appearance | Button idle |
| Pressed | Scale down 95%, darken 10% | Finger on button |
| Disabled | 50% opacity, no raycast | Insufficient currency |
| Loading | Spinner overlay, disable input | Waiting for server |
| Error | Red border/outline, error text | Validation failure |
| Selected | Highlight ring or fill change | Tab active |
| Hover | Subtle highlight (desktop only) | Mouse over |

### Data-Driven UI

- Bind UI to **view models** — UI reads state, doesn't own it.
- Use **reactive updates** (events, observables) — avoid polling in `Update()`.
- Handle **null/empty/loading states** explicitly in every data-bound element.
- Show **skeleton screens** or shimmer placeholders during data fetch — never empty space.

---

## Common UI Patterns (Unity-Specific)

| Pattern | Implementation | Notes |
|---------|---------------|-------|
| Scrollable list | `ScrollRect` + `VerticalLayoutGroup` + pooled items | Use `ScrollRect.onValueChanged` for lazy loading |
| Tab bar | `ToggleGroup` + `Toggle` per tab | `Toggle.onValueChanged` → show/hide panels |
| Popup/Modal | Instantiate from prefab, parent to overlay Canvas | Use `CanvasGroup` for fade-in |
| Toast notification | Pool at top Canvas, auto-hide with `DOTween`/coroutine | Stack from top, slide down |
| Progress bar | `Image` with `fillAmount` (Filled type) | Animate with `DOTween` or lerp |
| Countdown timer | TMP text, update via coroutine or `InvokeRepeating` | Format: `mm:ss` or `hh:mm:ss` |
| Currency display | TMP text + icon sprite | Animate count-up for purchases |
| Loading overlay | Full-screen `CanvasGroup` with spinner | Block all input underneath |
