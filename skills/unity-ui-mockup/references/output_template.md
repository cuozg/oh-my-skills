# Output Template — Unity UI Mockup

> Canonical template for `docs/specs/UIs/Mockups/<Name>_Mockup.md`.
> Load via `read_skill_file("unity-ui-mockup", "references/output_template.md")`.
> See `docs/specs/UIs/Mockups/Achievement_Mockup.md` for a filled canonical example.

---

```markdown
# <Name> Mockup — Element List

**Date:** YYYY-MM-DD
**Status:** Approved | In Review | Draft
**Prefab:** `<PrefabName>.prefab` (`<Namespace>.<ControllerClass>`)
**Related:** [<Related_Screen>](../Screens/<Related_Screen>.md) · [<Related_Element>](../Elements/<Related_Element>.md)

### Visual Layout

<!-- Preferred: HTML-styled mockup (as in Achievement_Mockup.md) for high-fidelity list/card screens.
     Fallback: ASCII-only box-drawing is always acceptable. When using HTML, include an ASCII
     wireframe inside <details> for diff-friendly review. -->

<!-- OPTION A — HTML-styled (recommended for scroll lists with card states) -->
<div style="max-width:520px; margin:16px auto; border:1px solid #E1E3EF; border-radius:18px; overflow:hidden; font-family: Inter, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background:#EEF0F6; box-shadow: 0 8px 24px rgba(26,30,47,0.10);">
<!-- Header -->
<div style="background: linear-gradient(135deg, #1E2142 0%, #2B2F6B 100%); color:white; padding:14px 16px 12px; text-align:center;">
<div style="font-size:13px; font-weight:800; letter-spacing:2px; line-height:1;"><TITLE></div>
<div style="width:56px; height:2px; background:#FFB800; border-radius:1px; margin:7px auto 0;"></div>
<div style="font-size:9px; font-weight:600; letter-spacing:1px; opacity:0.62; margin-top:6px;"><SUBTITLE></div>
</div>
<!-- ScrollRect → Viewport → ContentContainer -->
<div style="padding:12px; background:#F7F8FC;">
<div style="font-size:9px; font-weight:700; letter-spacing:0.8px; color:#8B90AD; text-align:center; margin-bottom:8px;">SCROLLRECT (Vertical) → Viewport (Mask) → ContentContainer (VerticalLayoutGroup)</div>
<!-- Repeat Card_<Item> per row; show at least 2 states: In Progress + Claimable/Completed -->
<!-- Card: icon | Title+Desc | ProgressBar + ProgressText | RewardContainer | ClaimButton -->
</div>
<!-- Legend (optional): map colors to states -->
<div style="display:flex; flex-wrap:wrap; gap:6px; justify-content:center; padding:8px 10px; background:white; border-top:1px solid #E6E8F2; font-size:9px; font-weight:600; color:#6C7293;">
<span style="display:inline-flex; align-items:center; gap:4px;"><span style="width:8px; height:8px; border-radius:50%; background:#7B61FF; display:inline-block;"></span> In progress</span>
<span style="display:inline-flex; align-items:center; gap:4px;"><span style="width:8px; height:8px; border-radius:50%; background:#00C853; display:inline-block;"></span> Completed</span>
<span style="display:inline-flex; align-items:center; gap:4px;"><span style="width:16px; height:10px; border-radius:99px; background:#E9EBF3; border:1px solid #DDE0EA; display:inline-block;"></span> Claim disabled</span>
<span style="display:inline-flex; align-items:center; gap:4px;"><span style="width:16px; height:10px; border-radius:99px; background: linear-gradient(90deg, #FF7A00, #FFB800); display:inline-block;"></span> Claimable</span>
</div>
</div>

<!-- OPTION B — ASCII-only (always valid; use when HTML is overkill) -->
```
┌─ <RootName> ────────────────────────────────────┐
│ Header: Title "<TITLE>"                          │
│ ScrollArea (ScrollRect → Viewport → Content):    │
│  [Card_<Item>: icon | Title+Desc | bar 3/10 | reward ○×100 | Claim] │
│  [Card_<Item>: icon | Title+Desc | bar 10/10 | reward ○×200 | Claim*] │
│  ... (one per item)                              │
└─────────────────────────────────────────────────┘
```

<details>
<summary><strong>ASCII wireframe (reference)</strong></summary>

```
┌─ <RootName> ────────────────────────────────────┐
│ Header: Title "<TITLE>"                          │
│ ScrollArea:                                      │
│  [Card_<Item>: icon | Title+Desc | bar 3/10 | reward ○×100 | Claim] │
│  [Card_<Item>: icon | Title+Desc | bar 10/10 | reward ○×200 | Claim*] │
│  ... (one per item)                              │
└─────────────────────────────────────────────────┘
```

</details>

### Element Tree
* `<RootGameObjectName>` (RectTransform, CanvasRenderer, <MainController>, CanvasGroup)
  * `Header` (RectTransform, HorizontalLayoutGroup)
    * `HeaderTitleText` (RectTransform, CanvasRenderer, TextMeshProUGUI)
  * `ScrollRect` (RectTransform, Image, Mask, ScrollRect)
    * `Viewport` (RectTransform, Image, Mask)
      * `ContentContainer` (RectTransform, VerticalLayoutGroup, ContentSizeFitter)
        * `Card_<Item>` (RectTransform, CanvasRenderer, <CardController>, LayoutElement)
          * `CategoryIcon` (RectTransform, CanvasRenderer, Image)
          * `InfoContainer` (RectTransform, VerticalLayoutGroup)
            * `TitleText` (RectTransform, CanvasRenderer, TextMeshProUGUI)
            * `DescText` (RectTransform, CanvasRenderer, TextMeshProUGUI)
            * `ProgressBar` (RectTransform, Slider, Image)
              * `Background` (RectTransform, CanvasRenderer, Image)
              * `FillArea` (RectTransform)
                * `Fill` (RectTransform, CanvasRenderer, Image)
              * `ProgressText` (RectTransform, CanvasRenderer, TextMeshProUGUI)
          * `RewardContainer` (RectTransform, HorizontalLayoutGroup)
            * `RewardIcon` (RectTransform, CanvasRenderer, Image)
            * `RewardAmountText` (RectTransform, CanvasRenderer, TextMeshProUGUI)
          * `ClaimButton` (RectTransform, CanvasRenderer, Image, Button)
            * `ClaimText` (RectTransform, CanvasRenderer, TextMeshProUGUI)
  * `LoadingIndicator` (RectTransform, CanvasRenderer, Image)
  * `EmptyStateView` (RectTransform, CanvasRenderer, TextMeshProUGUI)

### Element Inventory
- `Header` / `HeaderTitleText`: Title TMP with localized string key.
- `ScrollRect` → `Viewport` (Mask) → `ContentContainer` (VerticalLayoutGroup + ContentSizeFitter): Vertical scroll; one `Card_<Item>` per data row, auto-sized.
- `Card_<Item>` (`LayoutElement`): Reused row prefab. States — In Progress (muted Claim), Claimable/Completed (highlighted Claim + full progress), Locked (dashed/placeholder).
- `ProgressBar` (`Slider`): `Background` + `FillArea`/`Fill` + `ProgressText` (`x / y`).
- `RewardContainer` (`HorizontalLayoutGroup`): `RewardIcon` (soft currency) + `RewardAmountText` (`×N`).
- `ClaimButton` (`Button` + `Image`): Disabled when not claimable; gradient/highlight when claimable.
- `LoadingIndicator` / `EmptyStateView`: Siblings of `ScrollRect`; toggled by controller for async/empty states.
```

### Notes for filler

- Replace `<Name>`, `<RootName>`, `<PrefabName>`, `<ControllerClass>`, `<CardController>`, `<Item>` with real names.
- Keep 2-space indentation per depth in Element Tree (`* `, `  * `, `    * ` …).
- Every node lists attached components in `(...)` — include layout/mask/input components, not just transforms.
- Show at least two card-state variants in Visual Layout (e.g. In Progress `3/10` vs Claimable `10/10`).
- For non-list screens, replace the ScrollRect block with the screen's actual regions (e.g. `ButtonContainer` → `Button_Cancel`/`Button_Confirm`) — see Achievement mockup for the list pattern and adapt.
- Related links use relative paths to `../Screens/`, `../Popups/`, `../Elements/`, `../Controllers/`.
- Never leave `TODO`/`TBD`/`FIXME` in the final file.
