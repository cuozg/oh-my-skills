# UX Implementation: [Screen/Component Name]

**Source Design:** [path/to/design.html]
**Target Prefab:** [Assets/UI/Prefabs/path/PrefabName.prefab]
**Date:** [YYYY-MM-DD]

---

## 1. Design Analysis

### Element Inventory
| # | Element | Type | Text/Content | Interactive? |
|---|---------|------|-------------|-------------|
| 1 | | | | |

### Visual Specifications

**Colors**
| Purpose | Hex | RGBA (0-1) | Applied To |
|---------|-----|-----------|-----------|
| Background | | | |
| Primary text | | | |
| Button primary | | | |

**Typography**
| Element | Font | Size | Weight | Color | Alignment |
|---------|------|------|--------|-------|-----------|
| Title | | | | | |
| Body | | | | | |

**Spacing**: Section padding / Element spacing / Button padding / Card margin

### Interactions
| Element | Event | Action |
|---------|-------|--------|
| | Click | |

### Layout
- **Orientation / Resolution / Scaling / Scroll behavior**

---

## 2. Prefab Structure

```
Root_[ScreenName]
  ├── Panel_Header
  ├── Panel_Content
  └── Panel_Footer
```

---

## 3. Component Configuration

### [Element Name]
**GameObject:** `[path]`
- [ ] RectTransform: anchors, pivot, size, position
- [ ] Image: sprite, color, type, raycastTarget
- [ ] TextMeshProUGUI: text, fontSize, color, alignment, raycastTarget=false
- [ ] Button: transition, navigation=None
- [ ] LayoutGroup: type, spacing, padding, childAlignment
- [ ] ContentSizeFitter / LayoutElement as needed

---

## 4. Validation

- [ ] Colors/fonts/spacing match design spec
- [ ] All buttons/toggles/inputs function correctly
- [ ] Anchors and layout groups configured for responsive behavior
- [ ] raycastTarget=false on non-interactive elements
- [ ] Test at target and alternate resolutions

---

## 5. Implementation Notes

[Edge cases, decisions made during implementation]
