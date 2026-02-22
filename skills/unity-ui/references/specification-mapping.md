# Specification Mapping: HTML Design → Unity Properties

## Color Mapping

| HTML Format | Unity Equivalent |
|---|---|
| `#RRGGBB` / `#RRGGBBAA` | `new Color(R/255f, G/255f, B/255f, A/255f)` |
| `rgb(r,g,b)` / `rgba(r,g,b,a)` | `new Color(r/255f, g/255f, b/255f, a)` |
| Named (`red`) | `Color.red` |

| Context | Unity Component.Property |
|---|---|
| Background | Image.color |
| Text color | TextMeshProUGUI.color |
| Border | Image.color (outline sprite) |
| Button states | Button.colors (normalColor/highlightedColor/pressedColor/disabledColor) |
| Overlay/tint | Image.color with alpha |
| Shadow | Shadow.effectColor |

## Typography Mapping

| CSS Property | Unity TMP Property |
|---|---|
| `font-family` | Font Asset (TMP font from TTF/OTF) |
| `font-size: 16px` | Font Size: 16 (direct mapping) |
| `font-weight: bold/700+` | Font Style: Bold |
| `font-style: italic` | Font Style: Italic |
| `text-transform: uppercase` | Font Style: UpperCase |
| `letter-spacing: 2px` | Character Spacing: 2 |
| `line-height: 1.5` | Line Spacing: `(1.5 - 1.0) * 100 = 50` |
| `text-decoration: underline` | Font Style: Underline |

| CSS `text-align` | TMP Alignment |
|---|---|
| `left/center/right/justify` | Left/Center/Right/Justified |

| CSS Overflow | TMP Overflow Mode |
|---|---|
| `text-overflow: ellipsis` | Ellipsis |
| `overflow: hidden` | Truncate |
| `overflow: visible` | Overflow |
| `word-wrap: break-word` | Word Wrapping enabled |

## Spacing & Layout Mapping

| CSS | Unity |
|---|---|
| `padding: T R B L` | LayoutGroup.padding (top/right/bottom/left) |
| `gap: 10px` | LayoutGroup.spacing = 10 |
| `column-gap` / `row-gap` | GridLayoutGroup.spacing.x / .y |

**Margin**: No direct equivalent — use LayoutElement padding on parent, spacer GameObjects, or RectTransform offsets.

### Flexbox → Layout Group

| CSS Flexbox | Unity |
|---|---|
| `flex-direction: row` | HorizontalLayoutGroup |
| `flex-direction: column` | VerticalLayoutGroup |
| `display: grid` | GridLayoutGroup |
| `justify-content: center` | childAlignment: MiddleCenter |
| `justify-content: space-between` | childForceExpandWidth: true |
| `flex: 1` | LayoutElement.flexibleWidth = 1 |
| `flex-wrap: wrap` | Use GridLayoutGroup |

## Size & Dimension Mapping

| CSS | Unity RectTransform |
|---|---|
| `width: 200px` | sizeDelta.x = 200 (non-stretched anchors) |
| `height: 100px` | sizeDelta.y = 100 |
| `width: 100%` | Stretch anchors: anchorMin.x=0, anchorMax.x=1, offsets=0 |
| `max-width: 400px` | LayoutElement.preferredWidth = 400 + ContentSizeFitter |
| `min-width: 100px` | LayoutElement.minWidth = 100 |
| `aspect-ratio: 16/9` | AspectRatioFitter (FitInParent/EnvelopeParent) |

## Border & Shape

- **Borders**: 9-slice sprite (recommended), nested Images, or custom shader
- **Border radius**: 9-slice sprites with pre-baked rounded corners
- **Box shadow**: Shadow component (limited) or sprite with baked shadow

## Interaction Mapping

| HTML Element | Unity Component |
|---|---|
| `<button>` | Button + Image + Text child |
| `<input type="text">` | TMP_InputField |

## Advanced CSS-to-Unity Mapping

For complex animations, gradients, filters, blur effects, advanced positioning, and performance-aware CSS patterns, see specification-mapping-advanced.md.
