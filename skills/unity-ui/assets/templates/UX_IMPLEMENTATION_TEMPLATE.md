# UX Implementation: [Screen/Component Name]

**Source Design:** [path/to/design.html or document reference]
**Target Prefab:** [Assets/UI/Prefabs/path/PrefabName.prefab]
**Date:** [YYYY-MM-DD]

---

## 1. Design Analysis

### 1.1 Element Inventory

List every visible element from the design document:

| # | Element | Type | Text/Content | Interactive? |
|---|---------|------|-------------|-------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

### 1.2 Visual Specifications

#### Colors
| Purpose | Hex Value | RGBA (0-1) | Applied To |
|---------|-----------|-----------|-----------|
| Background | | | |
| Primary text | | | |
| Secondary text | | | |
| Button primary | | | |
| Button secondary | | | |
| Accent | | | |

#### Typography
| Element | Font | Size | Weight | Color | Alignment |
|---------|------|------|--------|-------|-----------|
| Title | | | | | |
| Body | | | | | |
| Button label | | | | | |
| Caption | | | | | |

#### Spacing
| Context | Value (px) | Notes |
|---------|-----------|-------|
| Section padding | | |
| Element spacing | | |
| Button padding | | |
| Card margin | | |

### 1.3 Interaction Specifications

| Element | Event | Action | Notes |
|---------|-------|--------|-------|
| | Click | | |
| | Toggle | | |
| | Input | | |

### 1.4 Layout Specifications

- **Orientation:** [Portrait / Landscape / Both]
- **Target resolution:** [e.g., 1920x1080]
- **Scaling behavior:** [stretch / fixed / responsive]
- **Scroll behavior:** [none / vertical / horizontal / both]

---

## 2. Prefab Structure

### 2.1 GameObject Hierarchy

```
Root_[ScreenName]
  ├── Panel_Header
  │   ├── ...
  │   └── ...
  ├── Panel_Content
  │   ├── ...
  │   └── ...
  └── Panel_Footer
      ├── ...
      └── ...
```

### 2.2 Hierarchy Notes

- [Explain grouping decisions]
- [Note any nested prefabs needed]
- [Identify reusable components]

---

## 3. Component Configuration

### 3.1 [Element Name]

**GameObject:** `[hierarchy path]`
**Components:**
- [ ] RectTransform: anchors=[min,max], pivot=[x,y], size=[w,h], position=[x,y]
- [ ] Image: sprite=[name], color=[rgba], type=[Simple/Sliced], raycastTarget=[true/false]
- [ ] TextMeshProUGUI: text="[value]", fontSize=[n], fontStyle=[style], color=[rgba], alignment=[align], raycastTarget=false
- [ ] Button: transition=[type], navigation=None
- [ ] LayoutGroup: type=[H/V/Grid], spacing=[n], padding=[l,r,t,b], childAlignment=[align]
- [ ] ContentSizeFitter: horizontal=[mode], vertical=[mode]
- [ ] LayoutElement: preferredWidth=[n], preferredHeight=[n], flexibleWidth=[n]

*(Copy this section for each element)*

---

## 4. Validation

### 4.1 Visual Checklist
- [ ] All colors match design spec exactly
- [ ] All font sizes match design spec
- [ ] All spacing/padding values match design spec
- [ ] All element sizes match design spec
- [ ] Correct sprites/images assigned
- [ ] Text content matches design

### 4.2 Interaction Checklist
- [ ] All buttons have correct click handlers
- [ ] All toggles function correctly
- [ ] All input fields accept correct input types
- [ ] All scroll views scroll in correct direction
- [ ] Navigation flow matches design

### 4.3 Layout Checklist
- [ ] Anchors set correctly for responsive behavior
- [ ] Layout groups spacing matches design
- [ ] ContentSizeFitters on dynamic content
- [ ] Test at target resolution
- [ ] Test at alternate resolutions (if responsive)

### 4.4 Performance Checklist
- [ ] raycastTarget=false on all non-interactive elements
- [ ] No unnecessary nested layout groups
- [ ] Images use appropriate sprite type (Sliced for scalable backgrounds)
- [ ] Text raycastTarget disabled

---

## 5. Implementation Notes

[Any additional notes, edge cases, or decisions made during implementation]
