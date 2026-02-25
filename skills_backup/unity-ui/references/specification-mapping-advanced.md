# Specification Mapping - Advanced Conversions

## Advanced CSS → Unity Conversions

### Gradients

| CSS | Unity |
|---|---|
| `linear-gradient(to right, #fff, #000)` | Image sprite with gradient OR use shader on material |
| `radial-gradient(center, #fff 0%, #000 100%)` | Custom 9-slice sprite |

### Filters & Effects

| CSS | Unity |
|---|---|
| `filter: blur(5px)` | Shadow + LayoutElement or separate blurred sprite |
| `filter: brightness(1.2)` | Image.color with multiplied brightness |
| `filter: saturate(1.5)` | Material with color adjustment shader |
| `drop-shadow(2px 2px 4px rgba(0,0,0,0.5))` | Shadow component or sprite with baked shadow |

### Complex Positioning

| CSS | Unity RectTransform |
|---|---|
| `position: absolute; bottom: 0; right: 0;` | AnchorMax=(1,0), AnchorMin=(1,0), Pivot=(1,0), Offset=(0,0) |
| `position: sticky; top: 20px;` | Custom LayoutGroup or ScrollRect with header pinning script |
| `transform: translateY(-50%)` | anchoredPosition.y = -size.y / 2 (vertical center) |

## State Machine Mappings

Complex CSS pseudo-classes map to state management:

| CSS | Unity Pattern |
|---|---|
| `:hover` → `:active` transition | Button.OnPointerEnter() → scale/color tween |
| `:focus` → `:blur` | InputField.onSelect/onDeselect |
| `@media (max-width: 480px)` | CanvasScaler detect + LayoutGroup override |
| `:disabled` | Button.interactable = false |

## Animation State Mapping

Complex CSS animations translate to Animator state machines:
- Define animation states (Idle, Hover, Pressed, Disabled)
- Trigger transitions on Button.OnPointerEnter/Exit
- Use Animator parameters (isHovered, isPressed, isDisabled)

## Responsive Breakpoint Mapping

| CSS Breakpoint | Canvas Scale Mode |
|---|---|
| 320px-480px (mobile) | Reference (800x600) |
| 481px-768px (tablet) | Reference (1024x768) |
| 769px+ (desktop) | Reference (1920x1080) |

Override CanvasScaler via script on game startup.
