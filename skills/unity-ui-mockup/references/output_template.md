# Output Template — Unity UI Mockup

> Canonical template for `docs/specs/UIs/Mockups/<Name>_Mockup.md`.
> Load via `read_skill_file("unity-ui-mockup", "references/output_template.md")`.
> Filled canonical example: `/Users/cuongnp/Work/ZenoGames/SimpleCasualUI/docs/specs/UIs/Mockups/Achievement_Mockup.md` — structure below is byte-for-byte that file with `<Placeholders>`.

---

```markdown
# <Name> Mockup — Element List

**Date:** YYYY-MM-DD
**Status:** Approved | In Review | Draft
**Prefab:** `<PrefabName>.prefab`
**Related:** [<Related_Screen>](../Screens/<Related_Screen>.md) · [<Related_Element>](../Elements/<Related_Element>.md)

### Visual Layout
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
<!-- Card 1: in-progress -->
<div style="background:white; border:1px solid #E8EAF0; border-left:4px solid #7B61FF; border-radius:12px; padding:10px 12px; display:flex; gap:10px; align-items:flex-start; margin-bottom:10px;">
<div style="width:44px; height:44px; min-width:44px; border-radius:50%; background:#FFF3DC; border:1px solid #FFD18A; display:flex; align-items:center; justify-content:center; font-size:18px;"><ICON_1></div>
<div style="flex:1; min-width:0;">
<div style="display:flex; align-items:center; gap:6px;">
<span style="font-size:12px; font-weight:800; color:#1A1E2F;"><CARD_TITLE_1></span>
<span style="font-size:9px; font-weight:800; color:#7B61FF; background:#F0EFFF; border:1px solid #E0DCFF; padding:1px 6px; border-radius:99px;"><BADGE_1></span>
</div>
<div style="font-size:10px; color:#6C7293; margin-top:1px;"><CARD_DESC_1></div>
<div style="display:flex; align-items:center; gap:8px; margin-top:7px;">
<div style="flex:1; height:8px; background:#EDEEF4; border-radius:99px; overflow:hidden; border:1px solid #E6E8F2;"><div style="width:<PROGRESS_PCT_1>%; height:100%; background: linear-gradient(90deg, #7B61FF, #9A86FF); border-radius:99px;"></div></div>
<span style="font-size:9px; font-weight:800; color:#6C7293; white-space:nowrap;"><PROGRESS_TEXT_1></span>
</div>
<div style="display:inline-flex; align-items:center; gap:6px; margin-top:7px; background:#FFF8E1; border:1px solid #FFE8A3; padding:3px 8px; border-radius:99px;">
<span style="width:14px; height:14px; border-radius:50%; background: linear-gradient(135deg, #FFD54F, #FF8F00); border:1px solid #E99A00; display:inline-flex; align-items:center; justify-content:center; font-size:9px; color:white; font-weight:900;">○</span>
<span style="font-size:10px; font-weight:800; color:#8D6E00;"><REWARD_1></span>
<span style="font-size:8px; font-weight:700; color:#B89A00; letter-spacing:0.5px;">REWARD</span>
</div>
</div>
<div style="display:flex; flex-direction:column; align-items:flex-end; gap:6px;">
<span style="font-size:8px; font-weight:800; color:#8B90AD; background:#EEF0F6; border:1px solid #E1E3EF; padding:2px 6px; border-radius:99px; letter-spacing:0.5px;"><STATE_BADGE_1></span>
<span style="font-size:10px; font-weight:800; color:#9AA0B8; background:#E9EBF3; border:1px solid #DDE0EA; padding:7px 14px; border-radius:8px; letter-spacing:0.6px;">CLAIM</span>
</div>
</div>
<!-- Card 2: claimable -->
<div style="background:white; border:1px solid #FFD18A; border-left:4px solid #00C853; border-radius:12px; padding:10px 12px; display:flex; gap:10px; align-items:flex-start; margin-bottom:10px; box-shadow: 0 0 0 4px rgba(255,122,0,0.08);">
<div style="width:44px; height:44px; min-width:44px; border-radius:50%; background:#E8F5E9; border:1px solid #A5D6A7; display:flex; align-items:center; justify-content:center; font-size:18px; position:relative;"><ICON_2><span style="position:absolute; top:-4px; right:-4px; width:16px; height:16px; background:#00C853; color:white; border-radius:50%; font-size:10px; display:flex; align-items:center; justify-content:center; border:1.5px solid white;">✓</span></div>
<div style="flex:1; min-width:0;">
<div style="display:flex; align-items:center; gap:6px;">
<span style="font-size:12px; font-weight:800; color:#1A1E2F;"><CARD_TITLE_2></span>
<span style="font-size:9px; font-weight:800; color:#1B8E3B; background:#E8F5E9; border:1px solid #A5D6A7; padding:1px 6px; border-radius:99px;">DONE</span>
</div>
<div style="font-size:10px; color:#6C7293; margin-top:1px;"><CARD_DESC_2></div>
<div style="display:flex; align-items:center; gap:8px; margin-top:7px;">
<div style="flex:1; height:8px; background:#EDEEF4; border-radius:99px; overflow:hidden; border:1px solid #E6E8F2;"><div style="width:100%; height:100%; background: linear-gradient(90deg, #00C853, #69F0AE); border-radius:99px;"></div></div>
<span style="font-size:9px; font-weight:800; color:#1A9E4A; white-space:nowrap;"><PROGRESS_TEXT_2></span>
</div>
<div style="display:inline-flex; align-items:center; gap:6px; margin-top:7px; background:#FFF8E1; border:1px solid #FFE8A3; padding:3px 8px; border-radius:99px;">
<span style="width:14px; height:14px; border-radius:50%; background: linear-gradient(135deg, #FFD54F, #FF8F00); border:1px solid #E99A00; display:inline-flex; align-items:center; justify-content:center; font-size:9px; color:white; font-weight:900;">○</span>
<span style="font-size:10px; font-weight:800; color:#8D6E00;"><REWARD_2></span>
<span style="font-size:8px; font-weight:700; color:#B89A00; letter-spacing:0.5px;">REWARD</span>
</div>
</div>
<div style="display:flex; flex-direction:column; align-items:flex-end; gap:6px;">
<span style="font-size:8px; font-weight:800; color:#E65100; background:#FFF3E0; border:1px solid #FFCC80; padding:2px 6px; border-radius:99px; letter-spacing:0.5px;">● CLAIMABLE ★</span>
<span style="font-size:10px; font-weight:900; color:white; background: linear-gradient(90deg, #FF7A00, #FFB800); border:1px solid #FF8F00; padding:7px 14px; border-radius:8px; letter-spacing:0.6px; box-shadow: 0 2px 8px rgba(255,122,0,0.30);">CLAIM</span>
</div>
</div>
<!-- Card 3: placeholder for remaining items -->
<div style="background:white; border:1px dashed #D8DAE6; border-radius:12px; padding:10px 12px; display:flex; gap:10px; align-items:center;">
<div style="width:36px; height:36px; min-width:36px; border-radius:50%; background:#F4F5F9; border:1px solid #E1E3EF; display:flex; align-items:center; justify-content:center; color:#B8BDD4; font-weight:700;">⋯</div>
<div style="flex:1;">
<div style="font-size:11px; font-weight:700; color:#8B90AD;">More <ITEM_PLURAL></div>
<div style="font-size:9px; color:#A8ADC3;">One <b style="color:#8B90AD;">Card_<Item></b> per <ITEM_SINGULAR> — auto-sized by ContentSizeFitter</div>
</div>
<span style="font-size:10px; font-weight:700; color:#B8BDD4; background:white; border:1px solid #E1E3EF; padding:6px 12px; border-radius:8px;">LOCKED</span>
</div>
<div style="text-align:center; font-size:9px; font-weight:600; color:#A8ADC3; letter-spacing:0.7px; margin-top:10px; border-top:1px solid #E6E8F2; padding-top:8px;">↕ SCROLL — ContentContainer (VerticalLayoutGroup) &nbsp;|&nbsp; ScrollRect → Viewport → ContentContainer → Card_<Item> × N</div>
</div>
<!-- Legend -->
<div style="display:flex; flex-wrap:wrap; gap:6px; justify-content:center; padding:8px 10px; background:white; border-top:1px solid #E6E8F2; font-size:9px; font-weight:600; color:#6C7293;">
<span style="display:inline-flex; align-items:center; gap:4px;"><span style="width:8px; height:8px; border-radius:50%; background:#7B61FF; display:inline-block;"></span> In progress</span>
<span style="display:inline-flex; align-items:center; gap:4px;"><span style="width:8px; height:8px; border-radius:50%; background:#00C853; display:inline-block;"></span> Completed</span>
<span style="display:inline-flex; align-items:center; gap:4px;"><span style="width:16px; height:10px; border-radius:99px; background:#E9EBF3; border:1px solid #DDE0EA; display:inline-block;"></span> Claim disabled</span>
<span style="display:inline-flex; align-items:center; gap:4px;"><span style="width:16px; height:10px; border-radius:99px; background: linear-gradient(90deg, #FF7A00, #FFB800); display:inline-block;"></span> Claimable</span>
<span style="color:#A8ADC3; font-weight:500;">○ = soft currency</span>
</div>
</div>
<p style="text-align:center; font-size:11px; color:#6C7293; font-family: Inter,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; margin:8px 0 0;">
<strong style="color:#1A1E2F;"><RootName></strong> — Header + ScrollRect (Viewport → ContentContainer) with <code style="background:#F0EFFF; padding:1px 5px; border-radius:4px; font-size:11px;">Card_<Item></code> rows.
  Top: in-progress (<PROGRESS_TEXT_1>), middle: claimable (<PROGRESS_TEXT_2>), bottom: placeholder for remaining <ITEM_PLURAL>.
</p>

```
┌─ <RootName> ───────────────────────────────┐
│ Header: Title "<TITLE>"                      │
│ ScrollArea:                                       │
│  [Card_<Item>: icon | Title+Desc | bar <PROGRESS_TEXT_1> | reward ○<REWARD_1> | Claim] │
│  [Card_<Item>: icon | Title+Desc | bar <PROGRESS_TEXT_2> | reward ○<REWARD_2> | Claim*] │
│  ... (one per <ITEM_SINGULAR>)                           │
└──────────────────────────────────────────────────┘
```

### Element Tree
* `<RootName>` (RectTransform, CanvasRenderer, <MainController>, CanvasGroup)
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
```

### Notes for filler

- Replace `<Name>`, `<RootName>`, `<PrefabName>`, `<MainController>`, `<CardController>`, `<Item>`, `<TITLE>`, `<SUBTITLE>`, `<CARD_TITLE_*>`, `<CARD_DESC_*>`, `<PROGRESS_*>`, `<REWARD_*>`, `<ICON_*>`, `<ITEM_SINGULAR>` / `<ITEM_PLURAL>` with real names. Example values from Achievement: `ScreenAchievement`, `Card_Achievement`, `ACHIEVEMENTS` / `TRACK YOUR MILESTONES`, `First Win` / `Collector`, `3 / 10` / `10 / 10`, `×100` / `×200`, `🏆` / `⭐`.
- Keep 2-space indentation per depth in Element Tree (`* `, `  * `, `    * ` …).
- Every node lists attached components in `(...)` — include layout/mask/input components, not just transforms.
- Show at least two card-state variants in Visual Layout (In Progress `3/10` muted Claim vs Claimable `10/10` gradient Claim) — exactly as in Achievement.
- Visual order is fixed: **HTML View** (styled div) → **caption `<p>`** → **ASCII Layout** (fenced code block directly below) → **Element Tree** — do not wrap ASCII in `<details>` and do not insert `Element Inventory` between them.
- For non-list screens, replace the ScrollRect block with the screen's actual regions (e.g. `ButtonContainer` → `Button_Cancel`/`Button_Confirm`) but keep the same three-section order and component-annotation style.
- Related links use relative paths to `../Screens/`, `../Popups/`, `../Elements/`, `../Controllers/`.
- Never leave `TODO`/`TBD`/`FIXME` in the final file.
