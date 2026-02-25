# Component Mapping Reference

Map HTML design elements to Unity GameObject hierarchy and components.

## HTML → Unity Component Mapping

| HTML Element | Unity GameObject |
|---|---|
| `<div>` container | Panel_ with Image (if bg) or empty GO |
| `<button>` | Button_ with Button component |
| `<span>/<p>/<h1-6>` | Text_ with TextMeshProUGUI |
| `<img>` | Image_ with Image component |
| `<input>` | InputField_ with TMP_InputField |
| `<input checkbox>` | Toggle_ with Toggle |
| `<select>` | Dropdown_ with TMP_Dropdown |
| `display:flex` | Panel_ with H/VerticalLayoutGroup |
| `display:grid` | Panel_ with GridLayoutGroup |
| `overflow:scroll` | ScrollView_ with ScrollRect |

## Naming Convention

Use `{Type}_{Purpose}` format:
- `Panel_`, `Button_`, `Text_`, `Image_`, `Toggle_`, `Slider_`, `InputField_`, `ScrollView_`, `Dropdown_`

## Hierarchy Depth

Maximum hierarchy depth: 5-6 levels. Deeper nesting decreases readability and performance.

## Best Practice

- Layout elements with flexible sizing (flex-direction: row/column)
- Use LayoutGroups instead of hardcoded positions
- Set raycastTarget=false on non-interactive elements (performance critical)
