# Prefab Creation Checklist

**Prefab:** [Name] | **Design Source:** [Reference]

---

## Pre-Implementation
- [ ] Design fully analyzed — elements, sprites, fonts, colors, typography, spacing, interactions documented

## Structure
- [ ] Hierarchy matches design, naming: `{Type}_{Purpose}`, depth ≤ 5
- [ ] Related elements grouped under Panel_ containers

## RectTransform
- [ ] Anchors set for responsive behavior, pivots appropriate
- [ ] Sizes/positions match design, stretched elements use correct offsets

## Visual Fidelity
- [ ] Colors match hex values, font sizes/weights/styles match spec
- [ ] Text alignment correct, sprites assigned with correct Image type
- [ ] Preserve Aspect Ratio set correctly, no unintended tinting

## Layout
- [ ] Layout groups match arrangement (H/V/Grid), spacing/padding correct
- [ ] childForceExpand/childControlSize set correctly
- [ ] ContentSizeFitter on dynamic content, LayoutElement for size overrides

## Typography
- [ ] All text uses TextMeshProUGUI (NOT legacy Text)
- [ ] Font asset, sizes, line/character spacing, overflow mode correct

## Interactions
- [ ] Buttons: transition type, navigation=None, state colors/sprites
- [ ] Toggles with ToggleGroup, InputFields with correct contentType
- [ ] Dropdowns with options, Sliders with min/max, ScrollRect configured

## Performance
- [ ] raycastTarget=false on ALL non-interactive elements and text
- [ ] RectMask2D over Mask, no unnecessary Image components
- [ ] CanvasGroup for group opacity, max 2-3 layout group nesting

## Final
- [ ] Prefab saved/named correctly, all references resolved
- [ ] Test at target and alternate resolutions, no console warnings
