# Specification Mapping: HTML Design → Unity Properties

## Table of Contents
- [Color Mapping](#color-mapping)
- [Typography Mapping](#typography-mapping)
- [Spacing and Layout Mapping](#spacing-and-layout-mapping)
- [Size and Dimension Mapping](#size-and-dimension-mapping)
- [Border and Shape Mapping](#border-and-shape-mapping)
- [Interaction Mapping](#interaction-mapping)
- [Visibility and Opacity Mapping](#visibility-and-opacity-mapping)
- [Animation and Transition Mapping](#animation-and-transition-mapping)
- [CSS Property Quick Reference](#css-property-quick-reference)

---

## Color Mapping

### HTML → Unity Color Conversion

| HTML Format | Example | Unity Equivalent |
|---|---|---|
| Hex (#RRGGBB) | `#FF5733` | `new Color(1f, 0.341f, 0.2f, 1f)` or Image.color |
| Hex (#RRGGBBAA) | `#FF573380` | `new Color(1f, 0.341f, 0.2f, 0.502f)` |
| RGB | `rgb(255, 87, 51)` | `new Color(255/255f, 87/255f, 51/255f)` |
| RGBA | `rgba(255, 87, 51, 0.5)` | `new Color(1f, 0.341f, 0.2f, 0.5f)` |
| Named | `red`, `white` | `Color.red`, `Color.white` |

### Color Application by Context

| Design Context | Unity Component | Property |
|---|---|---|
| Background color | Image | `color` |
| Text color | TextMeshProUGUI | `color` |
| Border color | Image (outline sprite) | `color` on border Image |
| Button normal | Button > Colors | `normalColor` |
| Button hover | Button > Colors | `highlightedColor` |
| Button pressed | Button > Colors | `pressedColor` |
| Button disabled | Button > Colors | `disabledColor` |
| Overlay/tint | Image | `color` with alpha |
| Shadow | Shadow component | `effectColor` |

### Hex to Unity Conversion Formula
```
R = hex_value / 255f
G = hex_value / 255f
B = hex_value / 255f
A = opacity (0-1) or hex_alpha / 255f
```

---

## Typography Mapping

### Font Properties

| HTML/CSS Property | Unity TMP Property | Notes |
|---|---|---|
| `font-family` | Font Asset | Must use TMP font asset created from TTF/OTF |
| `font-size: 16px` | Font Size: 16 | Direct mapping (design px = TMP points) |
| `font-weight: bold` | Font Style: Bold | Or use bold font asset variant |
| `font-style: italic` | Font Style: Italic | Or use italic font asset variant |
| `font-weight: 700` | Font Style: Bold | 700+ = Bold in TMP |
| `text-transform: uppercase` | Font Style: UpperCase | TMP supports case transforms |
| `letter-spacing: 2px` | Character Spacing: 2 | Direct mapping |
| `line-height: 1.5` | Line Spacing: 50 | TMP line spacing is percentage-based |
| `text-decoration: underline` | Font Style: Underline | Or rich text `<u>` |
| `text-decoration: line-through` | Font Style: Strikethrough | Or rich text `<s>` |

### Text Alignment

| CSS `text-align` | TMP Horizontal Alignment |
|---|---|
| `left` | Left |
| `center` | Center |
| `right` | Right |
| `justify` | Justified |

| CSS `vertical-align` | TMP Vertical Alignment |
|---|---|
| `top` | Top |
| `middle` | Middle |
| `bottom` | Bottom |

### Text Overflow

| CSS `overflow` / `text-overflow` | TMP Overflow Mode |
|---|---|
| `overflow: hidden; text-overflow: ellipsis` | Ellipsis |
| `overflow: hidden` | Truncate |
| `overflow: visible` | Overflow |
| `word-wrap: break-word` | Enable Word Wrapping |

### Line Height Conversion
```
CSS line-height: 1.5 → TMP Line Spacing = (1.5 - 1.0) * 100 = 50
CSS line-height: 24px on 16px font → TMP Line Spacing = ((24/16) - 1) * 100 = 50
```

---

## Spacing and Layout Mapping

### Padding

| CSS | Unity Equivalent |
|---|---|
| `padding: 10px` | LayoutGroup padding: left=10, right=10, top=10, bottom=10 |
| `padding: 10px 20px` | LayoutGroup padding: top=10, bottom=10, left=20, right=20 |
| `padding: 10px 20px 15px 5px` | LayoutGroup padding: top=10, right=20, bottom=15, left=5 |

### Margin
Unity UI has no direct margin concept. Achieve margins via:
- **LayoutElement**: Add to child, set padding on parent layout group
- **Spacer objects**: Empty GameObjects with LayoutElement.preferredWidth/Height
- **RectTransform offsets**: For non-layout-group arrangements

### Gap/Spacing

| CSS | Unity Equivalent |
|---|---|
| `gap: 10px` | LayoutGroup.spacing = 10 |
| `column-gap: 10px` | GridLayoutGroup.spacing.x = 10 |
| `row-gap: 10px` | GridLayoutGroup.spacing.y = 10 |

### Flexbox → Layout Group Mapping

| CSS Flexbox | Unity Layout Group |
|---|---|
| `display: flex; flex-direction: row` | HorizontalLayoutGroup |
| `display: flex; flex-direction: column` | VerticalLayoutGroup |
| `display: grid` | GridLayoutGroup |
| `justify-content: center` | childAlignment: MiddleCenter |
| `justify-content: space-between` | childForceExpandWidth: true |
| `align-items: center` | childAlignment: MiddleCenter/MiddleLeft |
| `flex: 1` | LayoutElement.flexibleWidth = 1 |
| `flex: 0 0 auto` | LayoutElement.flexibleWidth = 0 |
| `flex-wrap: wrap` | Not directly supported; use GridLayoutGroup |

---

## Size and Dimension Mapping

### Width and Height

| CSS | Unity RectTransform |
|---|---|
| `width: 200px` | sizeDelta.x = 200 (with non-stretched anchors) |
| `height: 100px` | sizeDelta.y = 100 (with non-stretched anchors) |
| `width: 100%` | Stretch anchors: anchorMin.x=0, anchorMax.x=1, offsetMin.x=0, offsetMax.x=0 |
| `width: 50%` | anchorMin.x=0.25, anchorMax.x=0.75 (centered) or script-driven |
| `max-width: 400px` | LayoutElement.preferredWidth = 400 with ContentSizeFitter |
| `min-width: 100px` | LayoutElement.minWidth = 100 |

### Aspect Ratio
| CSS | Unity |
|---|---|
| `aspect-ratio: 16/9` | AspectRatioFitter component, aspectMode = FitInParent/EnvelopeParent |

---

## Border and Shape Mapping

### Borders
Unity UI has no native CSS-like border. Achieve borders via:
- **9-slice sprite**: Sprite with border regions set in Sprite Editor
- **Outline component**: `Outline` component on Image (not recommended for production)
- **Nested Images**: Outer Image (border color), inner Image (background color) with padding
- **Custom shader**: For complex border effects

### Border Radius (Rounded Corners)
- Use 9-slice sprites with pre-baked rounded corners
- Or use `UIRoundedCorners` shader/component if available in project
- Specify corner radius in sprite creation matching design spec

### Box Shadow
- Unity has `Shadow` and `Outline` components (limited)
- For design-accurate shadows: use sprite with baked shadow
- Or use custom shader for dynamic shadows

---

## Interaction Mapping

### HTML Element → Unity Component

| HTML Element | Unity Component | Notes |
|---|---|---|
| `<button>` | Button | With Image background + Text child |
| `<input type="text">` | TMP_InputField | Standard text input |
| `<input type="password">` | TMP_InputField | contentType = Password |
| `<input type="number">` | TMP_InputField | contentType = IntegerNumber or DecimalNumber |
| `<input type="checkbox">` | Toggle | isOn = checked state |
| `<input type="radio">` | Toggle + ToggleGroup | Group ensures single selection |
| `<select>` | TMP_Dropdown | With options list |
| `<input type="range">` | Slider | min/max/value mapping |
| `<textarea>` | TMP_InputField | lineType = MultiLineNewline |
| `<a href>` | Button | Styled as text link |
| `<form>` | Panel with children | No direct equivalent; panel container |

### Button States

| CSS State | Unity Button Property |
|---|---|
| `:normal` | Normal Color / Normal Sprite |
| `:hover` | Highlighted Color / Highlighted Sprite |
| `:active` / `:pressed` | Pressed Color / Pressed Sprite |
| `:disabled` | Disabled Color / Disabled Sprite |
| `:focus` | Selected Color / Selected Sprite |

---

## Visibility and Opacity Mapping

| CSS Property | Unity Equivalent |
|---|---|
| `opacity: 0.5` | CanvasGroup.alpha = 0.5 (preferred) or Image/Text color alpha |
| `display: none` | GameObject.SetActive(false) |
| `visibility: hidden` | CanvasGroup.alpha = 0, CanvasGroup.blocksRaycasts = false |
| `pointer-events: none` | CanvasGroup.blocksRaycasts = false |
| `overflow: hidden` | RectMask2D or Mask component on parent |
| `z-index` | Sibling order in hierarchy (later = on top) |

---

## Animation and Transition Mapping

| CSS Transition | Unity Equivalent |
|---|---|
| `transition: opacity 0.3s` | DOTween / Animator: animate CanvasGroup.alpha over 0.3s |
| `transition: transform 0.2s` | DOTween / Animator: animate RectTransform over 0.2s |
| `transition: color 0.15s` | Button transition duration (for Button component) |
| `transform: scale(1.1)` | RectTransform.localScale = Vector3(1.1, 1.1, 1) |
| `transform: rotate(45deg)` | RectTransform.localEulerAngles = Vector3(0, 0, -45) |
| `transform: translateX(100px)` | RectTransform.anchoredPosition += Vector2(100, 0) |

---

## CSS Property Quick Reference

| CSS Property | Unity Component/Property | Category |
|---|---|---|
| `background-color` | Image.color | Color |
| `color` | TextMeshProUGUI.color | Color |
| `font-size` | TextMeshProUGUI.fontSize | Typography |
| `font-weight` | TextMeshProUGUI.fontStyle | Typography |
| `text-align` | TextMeshProUGUI.alignment | Typography |
| `padding` | LayoutGroup.padding | Spacing |
| `margin` | RectTransform offsets / spacers | Spacing |
| `gap` | LayoutGroup.spacing | Spacing |
| `width` | RectTransform.sizeDelta.x | Size |
| `height` | RectTransform.sizeDelta.y | Size |
| `display: flex` | HorizontalLayoutGroup / VerticalLayoutGroup | Layout |
| `display: grid` | GridLayoutGroup | Layout |
| `position: absolute` | Non-layout RectTransform with anchors | Layout |
| `border-radius` | 9-slice sprite with rounded corners | Shape |
| `box-shadow` | Shadow component or baked sprite | Shape |
| `opacity` | CanvasGroup.alpha | Visibility |
| `overflow` | RectMask2D / Mask | Visibility |
| `cursor: pointer` | Button component presence | Interaction |
