# UX Pre-Delivery Checklist for HTML Prototypes

Run through this checklist before delivering any HTML prototype.
Items are ordered by priority. CRITICAL items are blockers.

---

## CRITICAL (must pass before delivery)

- [ ] **Color contrast**: All text meets 4.5:1 ratio against its background. Use `getComputedStyle` to verify.
- [ ] **Focus states visible**: Every focusable element has a visible `:focus` or `:focus-visible` ring.
- [ ] **No color-only meaning**: Status, errors, and categories use text/icon in addition to color.
- [ ] **Touch targets**: All clickable elements are minimum 44x44px with 8px gap between adjacent targets.
- [ ] **No emoji icons**: All icons are inline SVG (Lucide-style). Emoji render inconsistently across platforms and look unprofessional.
- [ ] **Cursor pointer**: `cursor: pointer` on every clickable element -- buttons, cards, links, tabs, toggles.
- [ ] **Form labels**: Every input has a visible `<label>`, not placeholder-only. Placeholders disappear on focus.
- [ ] **Responsive**: No horizontal scroll at 375px or 1440px. Test both. Content reflows, nothing is clipped.

## HIGH (significant quality impact)

- [ ] **Hover states**: All interactive elements change on hover with 150-300ms transition.
- [ ] **Active states**: Buttons show press feedback -- `transform: scale(0.97)` or subtle color shift.
- [ ] **Loading feedback**: Buttons disable and show spinner/text during simulated async operations.
- [ ] **Error states**: Form errors appear next to the relevant field, not only at form top.
- [ ] **Empty states**: Screens with no data show a helpful message and a primary action, never a blank container.
- [ ] **Safe area**: Content avoids notch/home-indicator overlap. Use `env(safe-area-inset-*)` on outer containers.
- [ ] **Transition direction**: Forward navigation slides left. Back slides right. Modals slide up. Tab switches fade.
- [ ] **Transition timing**: Screen transitions 300-400ms. Micro-interactions 150ms. Use `ease-out` curves.
- [ ] **Back navigation**: Every non-root screen has a back button or swipe-back affordance.
- [ ] **Tab bar limit**: Bottom navigation has 5 items max, each with icon AND text label.

## MEDIUM (polish)

- [ ] **Staggered animation**: List items fade in sequentially with 30-50ms stagger per item.
- [ ] **Reduced motion**: Wrap animations in `@media (prefers-reduced-motion: no-preference)`.
- [ ] **Dark mode**: Support both themes via `@media (prefers-color-scheme: dark)`.
- [ ] **Typography scale**: Use consistent sizes -- 12/14/16/18/24/32px. Body line-height 1.5.
- [ ] **Spacing system**: All margins and padding use a 4px/8px grid.
- [ ] **Z-index layers**: content 0, nav 10, sticky 20, modal 100, overlay 200.
- [ ] **Scroll behavior**: `scroll-behavior: smooth`, `-webkit-overflow-scrolling: touch`, hide scrollbars where decorative.
- [ ] **FAB position**: Floating action button sits above tab bar -- `bottom: 80px; right: 16px`.
- [ ] **Input sizing**: All inputs minimum 48px height, 16px font-size (prevents iOS auto-zoom).
- [ ] **Realistic data**: No "Lorem ipsum" or "Test User 1." Use domain-appropriate names, prices, dates.

---

## Quick Validation Script

Add this to any prototype's `<script>` block during development. Remove before delivery.

```javascript
(function validateUX() {
  const issues = [];

  // Check cursor:pointer on clickable elements
  document.querySelectorAll('button, [role="button"], [onclick], a, .clickable, [data-click]').forEach(el => {
    const cursor = getComputedStyle(el).cursor;
    if (cursor !== 'pointer') {
      issues.push(`Missing cursor:pointer -> ${el.tagName}.${el.className.split(' ')[0] || '(no-class)'}`);
    }
  });

  // Check alt text on images
  document.querySelectorAll('img').forEach(el => {
    if (!el.alt) {
      issues.push(`Missing alt text -> <img src="${el.src.slice(-30)}">`);
    }
  });

  // Check minimum font size
  document.querySelectorAll('*').forEach(el => {
    const size = parseFloat(getComputedStyle(el).fontSize);
    if (el.textContent.trim() && size < 12 && el.children.length === 0) {
      issues.push(`Font too small (${size}px) -> ${el.tagName}.${el.className.split(' ')[0] || '(no-class)'}`);
    }
  });

  // Basic contrast check on text elements
  document.querySelectorAll('p, span, a, h1, h2, h3, h4, h5, h6, li, td, th, label, button').forEach(el => {
    const style = getComputedStyle(el);
    const color = style.color;
    const bg = style.backgroundColor;
    if (color === bg && el.textContent.trim()) {
      issues.push(`Zero contrast -> ${el.tagName}: color and background identical`);
    }
  });

  if (issues.length) {
    console.warn(`UX Validation: ${issues.length} issue(s) found`);
    issues.forEach(i => console.warn(`  - ${i}`));
  } else {
    console.log('UX Validation: All checks passed');
  }
})();
```

---

## Usage

The agent reads this checklist after generating a prototype and before delivering it.
Walk through each CRITICAL item. Fix any failures. Then address HIGH items.
MEDIUM items are applied when they fit the prototype's scope.
