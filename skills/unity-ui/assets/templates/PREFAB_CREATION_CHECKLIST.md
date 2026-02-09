# Prefab Creation Checklist

Use this checklist before marking a UX → Prefab implementation as complete.

**Prefab:** [Name]
**Design Source:** [Reference]

---

## Pre-Implementation

- [ ] Design document fully analyzed — all elements inventoried
- [ ] All required sprites/textures identified and available
- [ ] All required fonts/TMP font assets available
- [ ] Color palette extracted and documented
- [ ] Typography specifications extracted
- [ ] Spacing/layout specifications extracted
- [ ] Interaction requirements documented

## Structure

- [ ] GameObject hierarchy matches design structure
- [ ] Naming convention followed: `{Type}_{Purpose}`
- [ ] Hierarchy depth ≤ 5 levels (where possible)
- [ ] Related elements grouped under Panel_ containers
- [ ] No orphaned or unnecessary GameObjects

## RectTransform

- [ ] All anchors set correctly for intended responsive behavior
- [ ] All pivots set appropriately for element purpose
- [ ] Sizes match design spec (width, height)
- [ ] Positions match design layout
- [ ] Stretched elements use correct anchor spread + offsets

## Visual Fidelity

- [ ] Background colors match design hex values
- [ ] Text colors match design hex values
- [ ] Font sizes match design spec (px → TMP points)
- [ ] Font weights/styles match design (Bold, Italic, etc.)
- [ ] Text alignment matches design (horizontal + vertical)
- [ ] Image sprites correctly assigned
- [ ] Image types correct (Simple, Sliced, Filled as needed)
- [ ] Preserve Aspect Ratio set correctly on images
- [ ] No unintended color tinting on images

## Layout

- [ ] Layout groups match design arrangement (H/V/Grid)
- [ ] Layout group spacing matches design gap/spacing values
- [ ] Layout group padding matches design padding values
- [ ] Child alignment set correctly
- [ ] childForceExpand settings match design intent
- [ ] childControlSize settings correct
- [ ] ContentSizeFitter on dynamic-content containers
- [ ] LayoutElement on children needing size overrides

## Typography

- [ ] All text uses TextMeshProUGUI (NOT legacy Text)
- [ ] Correct TMP Font Asset assigned
- [ ] Font sizes match design
- [ ] Line spacing matches design line-height
- [ ] Character spacing matches design letter-spacing
- [ ] Text overflow mode set correctly (Ellipsis/Truncate/Overflow)
- [ ] Word wrapping enabled/disabled as per design
- [ ] Auto-size only where design specifies responsive text

## Interactions

- [ ] All buttons have Button component
- [ ] Button transition type set (ColorTint/SpriteSwap/Animation)
- [ ] Button navigation set to None (unless keyboard nav needed)
- [ ] Button state colors/sprites match design hover/pressed/disabled states
- [ ] All toggles have Toggle component with correct ToggleGroup
- [ ] All input fields have TMP_InputField with correct contentType
- [ ] Input field placeholder text matches design
- [ ] All dropdowns have TMP_Dropdown with correct options
- [ ] All sliders configured with correct min/max/direction
- [ ] ScrollRect configured with correct scroll direction and behavior

## Performance

- [ ] raycastTarget = false on ALL non-interactive elements
- [ ] raycastTarget = false on ALL TextMeshProUGUI (unless clickable)
- [ ] No excessive nesting of layout groups (max 2-3 deep)
- [ ] RectMask2D used instead of Mask where possible
- [ ] No unnecessary Image components (empty containers use empty GO)
- [ ] CanvasGroup used for group opacity rather than individual alpha

## Final Verification

- [ ] Prefab saved and named correctly
- [ ] Prefab location follows project folder structure
- [ ] All sprite references resolved (no missing references)
- [ ] All font references resolved
- [ ] Test at target resolution — matches design
- [ ] Test at alternate aspect ratios (if responsive)
- [ ] No console warnings or errors related to UI
- [ ] Element count matches design (nothing missing, nothing extra)
