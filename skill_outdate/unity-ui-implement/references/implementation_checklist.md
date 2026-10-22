# Implementation Checklist — Unity UI Implement

> Load via `read_skill_file("unity-ui-implement", "references/implementation_checklist.md")`.
> Use this file as the working checklist for every `unity-ui-implement` run.
> Copy the tables into your working notes and tick them through Phases 1–5.

---

## 1. Mock Token Table (from Mockup spec Visual Layout HTML)

One row per visual token. Copy hex/size/weight literally — no paraphrasing.

| # | Element (GO path) | Property | Mock Value (literal from HTML `style`) | Prefab Value | Verdict |
|---|-------------------|----------|----------------------------------------|--------------|---------|
| 1 | `<RootName>` | `background` | `linear-gradient(135deg, #1E2142 0%, #2B2F6B 100%)` |  | ✅ / ⚠️ |
| 2 | `Header/HeaderTitleText` | `font` | `Inter 13/800 #FFFFFF letter-spacing 2px` |  |  |
| 3 | `Header/HeaderTitleText` | `TextMeshProUGUI.color` | `#FFFFFF` |  |  |
| 4 | `Card_Achievement/ClaimButton` | `Image.color` (claimable gradient) | `linear-gradient(90deg, #FF7A00, #FFB800)` |  |  |
| 5 | `Card_Achievement/ClaimButton` | `Image.color` (disabled) | `#E9EBF3 border #DDE0EA` |  |  |
| 6 | `ScrollRect` | `padding/spacing` | `VerticalLayoutGroup spacing 12 padding 12` |  |  |
| 7 | `<RootName>` | `border-radius` | `18px` |  |  |
| 8 | `<RootName>` | `box-shadow` | `0 8px 24px rgba(26,30,47,0.10)` |  |  |

Add rows for every `color`, `fontSize`, `fontWeight`, `letterSpacing`, `lineHeight`, `background`, `border`, `border-radius`, `box-shadow`, `padding`, `spacing`, `alpha`, `raycastTarget` in the mock HTML.

---

## 2. Tree Node Table (from Mockup spec Element Tree)

One row per GameObject node. Depth is `0` for root.

| # | Depth | GO Name (backticked) | Components (from `(...)`) | Parent GO | Prefab GO Path | Verdict |
|---|-------|----------------------|---------------------------|-----------|----------------|---------|
| 1 | 0 | `<RootName>` | `RectTransform, CanvasRenderer, <MainController>, CanvasGroup` | — | `<RootName>` |  |
| 2 | 1 | `Header` | `RectTransform, HorizontalLayoutGroup` | `<RootName>` | `<RootName>/Header` |  |
| 3 | 2 | `HeaderTitleText` | `RectTransform, CanvasRenderer, TextMeshProUGUI` | `Header` | `<RootName>/Header/HeaderTitleText` |  |
| 4 | 1 | `ScrollRect` | `RectTransform, Image, Mask, ScrollRect` | `<RootName>` | `<RootName>/ScrollRect` |  |
| 5 | 2 | `Viewport` | `RectTransform, Image, Mask` | `ScrollRect` | `<RootName>/ScrollRect/Viewport` |  |
| 6 | 3 | `ContentContainer` | `RectTransform, VerticalLayoutGroup, ContentSizeFitter` | `Viewport` | `<RootName>/ScrollRect/Viewport/ContentContainer` |  |
| 7 | 4 | `Card_<Item>` | `RectTransform, CanvasRenderer, <CardController>, LayoutElement` | `ContentContainer` | `.../ContentContainer/Card_<Item>` |  |

Sibling order within each parent is the mock visual order — record `siblingIndex` per child and enforce via `SetSiblingIndex`.

---

## 3. Reference Map (from Controller spec Visual Reference + Controller Code)

One row per `[SerializeField]` field. `Component` is the field's type.

| # | Controller Field | Field Type | Prefab GO Path | GO Component | Assigned | Verdict |
|---|------------------|------------|----------------|--------------|----------|---------|
| 1 | `primaryButton` | `Button` | `<RootName>/Header/CloseButton` | `Button` on that GO | ☐ |  |
| 2 | `titleText` | `TextMeshProUGUI` | `<RootName>/Header/HeaderTitleText` | `TextMeshProUGUI` | ☐ |  |
| 3 | `offers[0]` | `Button` | `LeftMenu/Button_Side` | `Button` | ☐ |  |
| 4 | `offers[1]` | `Button` | `LeftMenu/Button_Side (1)` | `Button` | ☐ |  |
| 5 | `buttonPrefab` | `GameObject` | `Card_<Item>.prefab` asset | — | ☐ |  |
| 6 | `container` | `Transform` | `<RootName>/ScrollRect/Viewport/ContentContainer` | `RectTransform` | ☐ |  |

Array fields: set `arraySize` to spec count and assign each index in spec order. No `None` left.

---

## 4. Wiring Checklist (from Controller spec Interaction Details)

One row per tappable (including dim/backdrop and hardware back when spec lists them).

| # | Element (Mockup label → Prefab GO) | `onClick` Wiring (dynamic `AddListener`) | Stored `UnityAction` | `RemoveListener` in `OnDisable/OnHide/OnDestroy` | Handler | `DOKill` Guard | `SetUpdate(true)` when `timeScale==0` | UIManager Key (literal) | Verdict |
|---|-------------------------------------|------------------------------------------|----------------------|--------------------------------------------------|---------|----------------|----------------------------------------|-------------------------|---------|
| 1 | `OFFER.1` → `LeftMenu/Button_Side` | `btn.onClick.AddListener(() => OnOfferClicked(0))` | `_offerAction0` | `OnDisable` | `OnOfferClicked(0)` | `transform.DOKill()` before `DOPunchScale` | — | `"UI.Offer1Popup"` |  |
| 2 | `TAP TO PLAY` → `Button_Text` | `playButton.onClick.AddListener(_playAction)` | `_playAction` | `OnDisable` | `OnPlayClicked` | `DOKill` | — | `"UI.PlayScreen"` |  |
| 3 | `Pause → Resume` | `resumeButton.onClick.AddListener(_resumeAction)` | `_resumeAction` | `OnHide` | `OnResume` | `DOKill` | `SetUpdate(true)` | `HidePopup` |  |

Rules: **No Inspector `onClick` persistent listeners** — persistent count must be `0` after wiring.

---

## 5. Gap Table (Phase 2 Baseline)

One row per Tree node + per token + per reference. Build after walking the existing prefab/controller.

| # | Item | In Spec | In Prefab/Controller Today | Verdict | Disposition |
|---|------|---------|----------------------------|---------|-------------|
| 1 | `Header/HeaderTitleText` `fontSize 13 weight 800 #FFFFFF` | Mock token `#FFFFFF 13/800` | `12/700 #EEEEEE` | ⚠️ Mismatch | Fix token |
| 2 | `ScrollRect/Viewport/ContentContainer` `ContentSizeFitter` | Tree requires `ContentSizeFitter` | Missing | ⚠️ Spec-Only | Add component |
| 3 | `CanvasGroup` on `<RootName>` | Tree requires `CanvasGroup` | Missing | ⚠️ Spec-Only | Add component |
| 4 | `SideMenuController.offers[0]` → `LeftMenu/Button_Side` | Reference Map row 3 | `Missing (null)` | ⚠️ Missing ref | Assign |
| 5 | `Badge` GO | Tree node `Badge (Image 36×36)` | Not in prefab | ⚠️ Spec-Only | Create GO |
| 6 | `OldBanner` GO | — | In prefab, not in spec | ⚠️ Prefab-Only | Remove (confirm with spec owner) |

Categories: **Aligned / Spec-Only (to add) / Prefab-Only (to remove/rename) / Mismatch (fix value)**. Every row needs a disposition before leaving Phase 2.

---

## 6. Verification Log Template (Phase 5)

Copy this into the PR description or `docs/specs/UIs/<Name>_Implement_Verify.md` and tick before shipping.

```markdown
# <Name> Implement — Verification Log

**Date:** YYYY-MM-DD
**Mockup:** `docs/specs/UIs/Mockups/<Name>_Mockup.md`
**Controller:** `docs/specs/UIs/Controllers/<Name>_Controller.md`
**Prefab:** `Assets/_ZenoUI/Prefabs/{Screens,Popups,Elements}/<Name>.prefab`
**Controller:** `Assets/_ZenoUI/Scripts/Runtime/UIController/<Name>Controller.cs`

### A. Mock Parity (pixel tokens)
- [ ] Every Image/TMP color hex matches mock HTML style exactly
- [ ] Every TMP font/size/weight/letterSpacing/alignment matches mock
- [ ] Every background/gradient/border/radius/shadow/padding/spacing matches mock
- [ ] Sibling order (GetSiblingIndex walk) matches mock visual order top-to-bottom
- [ ] Screenshots: Inspector token values side-by-side with mock HTML

### B. Tree Parity (structure)
- [ ] Depth-first walk: every Tree node ticks one prefab GO at same depth/name, zero unticked
- [ ] Every Tree component list present on prefab GO (type exact)
- [ ] No extra GO nodes or components not in spec (except RectTransform)
- [ ] Layout/mask/input components not omitted (ContentSizeFitter, Mask, CanvasGroup, etc.)

### C. Reference Completeness (controller)
- [ ] Every Reference Map row assigned — zero None/Missing; array sizes match spec
- [ ] All onClick dynamic AddListener with stored UnityAction + RemoveListener in OnDisable/OnHide/OnDestroy
- [ ] Inspector onClick persistent count == 0 on every Button
- [ ] Every tween has DOKill guard; pause flows use SetUpdate(true)
- [ ] Every UIManager key is literal from spec and exists in AddressableAssetSettings (or marked to-be-created)
- [ ] SerializedObject Missing scan: PASS
- [ ] Console: zero errors/warnings after save + reimport
- [ ] PlayMode smoke: tap each tappable per Interaction Details → correct UI change + service call + navigation, no MissingReferenceException

### Evidence
- Prefab hierarchy dump (fmt walk output):
```
<paste fmt() output>
```
- Missing scan output:
```
<paste scan output — PASS: All controller references assigned>
```
- Gaps closed: <N> / <N> rows from Gap Table resolved
```

---

## 7. Quick Commands (Unity MCP)

```csharp
// Hierarchy walk (baseline + final)
System.Func<GameObject,int,string> fmt=null;
fmt=(go,d)=>{
  var sb=new System.Text.StringBuilder();
  var pad=new string(' ',d*2);
  var cs=go.GetComponents<Component>();
  var ns=new System.Collections.Generic.List<string>();
  foreach(var c in cs) if(c!=null) ns.Add(c.GetType().Name);
  sb.AppendLine($"{pad}* `{go.name}` ({string.Join(", ", ns)})");
  for(int i=0;i<go.transform.childCount;i++) sb.Append(fmt(go.transform.GetChild(i).gameObject,d+1));
  return sb.ToString();
};
var prefab=UnityEditor.AssetDatabase.LoadAssetAtPath<GameObject>("Assets/_ZenoUI/Prefabs/Screens/<Name>.prefab");
return fmt(prefab,0);

// Sibling order check
var root=UnityEditor.AssetDatabase.LoadAssetAtPath<GameObject>("Assets/_ZenoUI/Prefabs/Screens/<Name>.prefab");
for(int i=0;i<root.transform.childCount;i++) UnityEngine.Debug.Log($"{i}: {root.transform.GetChild(i).name}");

// Missing reference scan
var go=UnityEditor.AssetDatabase.LoadAssetAtPath<GameObject>("Assets/_ZenoUI/Prefabs/Screens/<Name>.prefab");
var ctrl=go.GetComponent<ZenoGames.UI.<ControllerClass>>();
var so=new UnityEditor.SerializedObject(ctrl);
var it=so.GetIterator();
bool missing=false;
while(it.NextVisible(true)){
  if(it.propertyType==UnityEditor.SerializedPropertyType.ObjectReference && it.objectReferenceValue==null){
    UnityEngine.Debug.LogError($"Missing: {it.displayName} ({it.name})", go);
    missing=true;
  }
}
UnityEngine.Debug.Log(missing?"FAIL":"PASS: All controller references assigned");

// Inspector onClick persistent count
foreach(var b in go.GetComponentsInChildren<UnityEngine.UI.Button>(true)){
  var count=b.onClick.GetPersistentEventCount();
  if(count>0) UnityEngine.Debug.LogWarning($"{b.name} has {count} persistent onClick — must be 0", b);
}
```
