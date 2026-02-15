# Unity UI Best Practices

## Canvas
- **Overlay**: Default game UI | **Camera**: 3D interaction/post-processing | **World**: In-world (health bars)
- Scaler: `ScaleWithScreenSize`, ref from design, Match=0.5
- Separate canvases for static vs animated elements

## RectTransform
```
Full stretch:  anchorMin(0,0) anchorMax(1,1)
Center fixed:  anchor(0.5,0.5) sizeDelta(w,h)
Top-left:      anchor(0,1) pivot(0,1)
```
| Use | anchorMin | anchorMax | Pivot |
|---|---|---|---|
| Center popup | (0.5,0.5) | (0.5,0.5) | (0.5,0.5) |
| Top bar | (0,1) | (1,1) | (0.5,1) |
| Bottom bar | (0,0) | (1,0) | (0.5,0) |
| Full screen | (0,0) | (1,1) | (0.5,0.5) |

Pivot: match growth direction. Lists grow down → pivot(0.5,1).

## Layout
- **HLG**: `childForceExpandWidth`=true for equal widths
- **VLG**: `childControlHeight=false` + `LayoutElement.preferredHeight`
- **Grid**: `cellSize` from design, `constraint=FixedColumnCount`
- **ContentSizeFitter**: ScrollRect content → `verticalFit=PreferredSize`
- **LayoutElement**: `preferred` for target, `flexible` for proportional fill

## TMP
- Always TMP over legacy | `raycastTarget=false` on non-interactive text | Auto Size only if design specifies

## Image
Simple=backgrounds/icons | Sliced=9-slice panels | Filled=progress bars | `raycastTarget=false` unless clickable | `preserveAspect=true` for icons

## Interaction
- **Button**: Navigation=None, ColorTint or SpriteSwap
- **Toggle**: +ToggleGroup for radio
- **ScrollRect**: Single axis, elastic, inertia=true, deceleration=0.135
- **InputField**: Set contentType

## Performance
1. `raycastTarget=false` on ALL non-interactive (biggest impact)
2. Animated elements on sub-canvas
3. Disable layout groups after initial if static
4. Pool list items/popups; SetActive over Destroy
5. RectMask2D over Mask
6. CanvasGroup.alpha over individual Image.alpha

## Naming
`Panel_`, `Button_`, `Text_`, `Image_`, `Toggle_`, `Slider_`, `InputField_`, `ScrollView_`, `Dropdown_`

## Rules
**DON'T**: Legacy Text, raycast=true on decorative, 3+ nested layouts, Update() for UI state, hardcoded positions, Mask over RectMask2D
**DO**: Match design spec exactly, layout groups for repeats, test multiple resolutions, ContentSizeFitter for dynamic text
