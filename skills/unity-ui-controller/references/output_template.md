# Output Template — Unity UI Controller Flow

> Canonical template for `docs/specs/UIs/Controllers/<Name>_Controller.md`.
> Load via `read_skill_file("unity-ui-controller", "references/output_template.md")`.
> Filled canonical example below is `HomeScreenController` (ScreenHome) with its composed
> `SideMenuController` + `PlayLevelController` + persistents `TopMenuController` + `BottomMenuController`.
> Keep structure byte-for-byte; replace `<Placeholders>` with real values. No `TODO`/`TBD`/`FIXME`.

---

```markdown
# <Name> Controller — UI Flow

**Date:** YYYY-MM-DD
**Status:** Approved | In Review | Draft
**Prefab:** `<PrefabName>.prefab` (guid `<Guid>` when known) | `(to be created)`
**Controller:** `Assets/_ZenoUI/Scripts/Runtime/UIController/<ControllerClass>.cs` (`<BaseClass>`) | `(to be created)`
**Namespace:** `<Namespace>` · **Asmdef:** `<Asmdef>`
**Related:** [<Related_Screen>](../Screens/<Related_Screen>.md) · [<Related_Mockup>](../Mockups/<Related_Mockup>.md) · [<Related_Element>](../Elements/<Related_Element>.md) · [<Related_Core>](../Core/<Related_Core>.md)

### Overview

<One sentence: what this controller owns and how it fits in Canvas hierarchy. Example: `HomeScreenController` is the side-only orchestrator for `ScreenHome` — it composes `LeftMenu`/`RightMenu` (`SideMenuController` × 2) + center `Button_Text` (`PlayLevelController`); `TopMenuController` and `BottomMenuController` are persistents outside this screen on `UIManager._canvasRoot`.>

### Composition

```
<CanvasHierarchy — mirrors UIManager._canvasRoot + ScreenContainer + persistents. Example for Home:>
UIManager._canvasRoot (Transform, Canvas root)
 ├─ PersistentTop — TopMenuController (HorizontalLayoutGroup) — CoinChip + HeartChip + Avatar + SettingsButton
 ├─ ScreenContainer
 │   └─ <RootGO> (<ControllerClass> : <BaseClass>, Canvas, CanvasScaler, GraphicRaycaster, CanvasGroup)
 │       ├─ Background_Home (Image, stretch 0,0–1,1)
 │       ├─ LeftMenu (VerticalLayoutGroup, ContentSizeFitter, SideMenuController — 3× Button_Side)
 │       ├─ Button_Text (Image, Button, PlayLevelController — center LV badge)
 │       └─ RightMenu (VerticalLayoutGroup, ContentSizeFitter, SideMenuController — 2× Button_Side)
 └─ PersistentBottom — BottomMenuController (HorizontalLayoutGroup, 5× ButtonBottomMenuController)
```

**File Map:**
```
Assets/_ZenoUI/Prefabs/Screens/<PrefabName>.prefab
Assets/_ZenoUI/Scripts/Runtime/UIController/<ControllerClass>.cs
Assets/_ZenoUI/Scripts/Runtime/ScriptableObjects/<SettingsClass>.cs
Assets/_ZenoUI/Prefabs/Elements/Button_Side.prefab (when dynamically spawned)
```

### Visual Reference

> Compact link table — every mockup tappable maps to a prefab GO and a controller field.
> This is the traceability index for the diagrams below.

| # | Mockup Element (label) | Prefab GO | Prefab File | Controller Field | Mockup Link |
|---|------------------------|-----------|-------------|------------------|-------------|
| 1 | `OFFER.1` — `Button_Side` (icon 🎁 + label + badge ●1) | `LeftMenu/Button_Side` | [`ScreenHome.prefab`](../../../Assets/_ZenoUI/Prefabs/Screens/ScreenHome.prefab) + [`Button_Side.prefab`](../../../Assets/_ZenoUI/Prefabs/Elements/Button_Side.prefab) | [`SideMenuController.offers[0]`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/SideMenuController.cs) `offerId="offer1"` → `"UI.Offer1Popup"` | [`Home_Mockup`](../Mockups/Home_Mockup.md) |
| 2 | `STARTER PACKAGE` — `Button_Side` | `LeftMenu/Button_Side (1)` | same | `offers[1]` `starter_package` → `"UI.StarterPackagePopup"` | same |
| 3 | `STAR CHEST` — `Button_Side` (badge ●3) | `LeftMenu/Button_Side (2)` | same | `offers[2]` `star_chest` → `"UI.StarChestPopup"` | same |
| 4 | `Level 2 — TAP TO PLAY` — `Button_Text` | `ScreenHome/Button_Text` | [`ScreenHome.prefab`](../../../Assets/_ZenoUI/Prefabs/Screens/ScreenHome.prefab) | [`PlayLevelController.playButton`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/PlayLevelController.cs) + `levelText` | same |
| 5 | `NO ADS` — `Button_Side` | `RightMenu/Button_Side` | [`Button_Side.prefab`](../../../Assets/_ZenoUI/Prefabs/Elements/Button_Side.prefab) | `SideMenuController.offers[0]` `no_ads` → `"UI.NoAdsPopup"` | same |
| 6 | `WHEEL` — `Button_Side` | `RightMenu/Button_Side (1)` | same | `offers[1]` `wheel` → `"UI.WheelPopup"` | same |
| 7 | `Coin +` (TopMenu) | `PersistentTop/CoinChip/addButton` | [`TopMenu.prefab`](../../../Assets/_ZenoUI/Prefabs/TopMenu.prefab) | [`TopMenuController.coinChip.addButton`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/TopMenuController.cs) | [`TopMenu_Mockup`](../Mockups/TopMenu_Mockup.md) |
| 8 | `♥ +` (TopMenu) | `PersistentTop/HeartChip/addButton` | same | [`TopMenuController.heartChip.addButton`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/TopMenuController.cs) | same |
| 9 | `⚙ Settings` (TopMenu) | `PersistentTop/settingsButton` | same | [`TopMenuController.settingsButton`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/TopMenuController.cs) | same |
| 10 | `Bottom tabs` (5) | `PersistentBottom/Button_Menu ×5` | [`BottomMenu.prefab`](../../../Assets/_ZenoUI/Prefabs/BottomMenu.prefab) | [`BottomMenuController.tabs[i]`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/BottomMenuController.cs) | [`BottomMenu_Mockup`](../Mockups/BottomMenu_Mockup.md) |

### UI Flow Diagram

> Mermaid `flowchart TD` — every tappable in Visual Reference has one coloured path.
> Colours: tappable `#FFB800`, handler `#7B61FF`, service `#00A67D`, navigation `#FF3B30`.
> Show `DOKill` guards and `SetUpdate(true)` when `Time.timeScale == 0` (e.g. Pause).

```mermaid
flowchart TD
    %% ── HomeScreen composition ──
    Home["ScreenHome\nHomeScreenController\n(ScreenCanvasController)"]:::screen

    %% LeftMenu — SideMenuController (3 offers)
    L1["OFFER.1\nButton_Side · LeftMenu[0]\n●1 badge"]:::tap
    L2["STARTER PACKAGE\nButton_Side · LeftMenu[1]"]:::tap
    L3["STAR CHEST\nButton_Side · LeftMenu[2]\n●3 badge"]:::tap
    L1 --> H1["OnOfferClicked(0)\nSideMenuController"]:::handler
    L2 --> H2["OnOfferClicked(1)"]:::handler
    L3 --> H3["OnOfferClicked(2)"]:::handler
    H1 --> FX1["DOKill + DOPunchScale\npulseScale/pulseDuration"]:::fx
    H2 --> FX1
    H3 --> FX1
    FX1 --> S1["Haptic: Selection"]:::svc
    S1 --> N1["UIManager.ShowPopupAsync\n\"UI.Offer1Popup\""]:::nav
    S1 --> N2["\"UI.StarterPackagePopup\""]:::nav
    S1 --> N3["\"UI.StarChestPopup\""]:::nav
    N1 --> ST1["PopupStack: push\nPopup_Offer1 above ScreenHome"]:::state
    N2 --> ST1
    N3 --> ST1

    %% Center — PlayLevelController
    Play["Level 2 — TAP TO PLAY\nButton_Text (400×200)"]:::tap
    Play --> HP["OnPlayClicked()\nPlayLevelController"]:::handler
    HP --> FX2["DOKill + DOPunchScale"]:::fx
    FX2 --> S2["LevelManager<LevelData>.CurrentLevelIndex\nBindLevel() → LV{N}"]:::svc
    S2 --> N4["LoadCurrentLevelAsync()\n→ UIManager.ShowScreenAsync<ScreenPlay>\n(future)"]:::nav
    N4 --> ST2["Screen: Hide(ScreenHome)\n→ Show(ScreenPlay)"]:::state

    %% RightMenu — SideMenuController (2 offers)
    R1["NO ADS\nButton_Side · RightMenu[0]"]:::tap
    R2["WHEEL\nButton_Side · RightMenu[1]"]:::tap
    R1 --> H4["OnOfferClicked(0)"]:::handler
    R2 --> H5["OnOfferClicked(1)"]:::handler
    H4 --> FX1
    H5 --> FX1
    H4 --> N5["\"UI.NoAdsPopup\""]:::nav
    H5 --> N6["\"UI.WheelPopup\""]:::nav
    N5 --> ST1
    N6 --> ST1

    %% Persistents — TopMenu
    Top["PersistentTop\nTopMenuController"]:::screen
    Coin["Coin chip +"]:::tap
    Heart["Heart chip +"]:::tap
    Gear["⚙ Settings"]:::tap
    Coin --> TC1["OnCoinAddClicked()"]:::handler
    Heart --> TC2["OnHeartAddClicked()"]:::handler
    Gear --> TC3["OnSettingsClicked()"]:::handler
    TC1 --> N7["ShowPopupAsync \"UI.ShopPopup\""]:::nav
    TC2 --> N8["ShowPopupAsync \"UI.LivesRefillPopup\""]:::nav
    TC3 --> N9["ShowPopupAsync \"UI.SettingsPopup\""]:::nav
    N7 --> ST1
    N8 --> ST1
    N9 --> ST1

    %% Persistents — BottomMenu
    Bot["PersistentBottom\nBottomMenuController (5 tabs)"]:::screen
    B0["STORE [0]"]:::tap
    B2["HOME [2] ★"]:::tap
    B3["LEADERBOARD [3]"]:::tap
    B4["ACHIEVEMENT [4]"]:::tap
    B0 --> BC["SelectTab(i)\nBottomMenuController"]:::handler
    B2 --> BC
    B3 --> BC
    B4 --> BC
    BC --> FX3["DOAnchorPosY + DOColor\n(DOKill guard)"]:::fx
    FX3 --> N10["UIManager.ShowScreenAsync\n\"UI.StoreScreen\" / \"UI.HomeScreen\" / ..."]:::nav
    N10 --> ST3["Screen: Hide(prev) → Show(next)\nBottomMenu survives (persistent)"]:::state
    BC --> ST4{"No-op if already selected\nor empty prefabPath (reserved [1])"}:::state

    classDef tap fill:#FFB800,stroke:#E99A00,color:#1A1E2F,font-weight:800
    classDef handler fill:#7B61FF,stroke:#5A3FD6,color:#FFFFFF,font-weight:700
    classDef fx fill:#EEF0F6,stroke:#C8CAD8,color:#1A1E2F
    classDef svc fill:#00A67D,stroke:#008A65,color:#FFFFFF
    classDef nav fill:#FF3B30,stroke:#D62A1E,color:#FFFFFF,font-weight:700
    classDef state fill:#F7F8FC,stroke:#E1E3EF,color:#6C7293
    classDef screen fill:#1E2142,stroke:#2B2F6B,color:#FFFFFF,font-weight:800
```

```mermaid
sequenceDiagram
    participant U as User Tap
    participant B as Button (GO)
    participant C as Controller Handler
    participant H as Haptic / DOTween
    participant S as Service / Manager
    participant M as UIManager
    participant UI as UI State

    U->>B: tap `Button_Side` OFFER.1
    B->>C: onClick → OnOfferClicked(0)
    C->>H: DOKill + DOPunchScale
    C->>H: HapticType.Selection
    C->>M: ShowPopupAsync("UI.Offer1Popup")
    M->>UI: push PopupStack<br/>Popup_Offer1 visible above ScreenHome
    UI-->>U: dim + card; close reveals ScreenHome

    U->>B: tap `Button_Text` Level 2
    B->>C: OnPlayClicked()
    C->>H: DOPunchScale
    C->>S: LevelManager.CurrentLevelIndex → LV{N}
    C->>M: LoadCurrentLevelAsync()
    M->>UI: Hide(ScreenHome) → Show(ScreenPlay)
    UI-->>U: board placeholder (SDK) + HUD
```

### Tree Flow

> Depth-first interaction tree. Each leaf shows `→ UI: <change> | Logic: <call> | Nav: <key>`.
> Indent exactly 2 spaces per level (`* `, `  * `, `    * `).

* `UIManager._canvasRoot` (Transform, Canvas root)
  * `PersistentTop` (`TopMenuController`, HorizontalLayoutGroup, `TopMenuSettings`) — Avatar + CoinChip + HeartChip + SettingsButton
    * `CoinChip/addButton` (Button) — tap `+` → [`TopMenuController.OnCoinAddClicked`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/TopMenuController.cs) → UI: `DOKill` + `DOPunchScale` (pulse) | Logic: `HapticType.Selection` | Nav: `UIManager.ShowPopupAsync<PopupCanvasController>("UI.ShopPopup")` → `PopupStack.push(ShopPopup)`
    * `HeartChip/addButton` (Button) — tap `+` → [`TopMenuController.OnHeartAddClicked`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/TopMenuController.cs) → UI: `DOKill` + `DOPunchScale` | Logic: `HapticType.Selection` | Nav: `ShowPopupAsync("UI.LivesRefillPopup")`
    * `settingsButton` (Button, Image) — tap `⚙` → [`TopMenuController.OnSettingsClicked`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/TopMenuController.cs) → UI: `DOKill` + `DOPunchScale` | Logic: `HapticType.Selection` | Nav: `ShowPopupAsync<PopupCanvasController>("UI.SettingsPopup")` → stacked above current screen
    * `avatarButton` (Button) — tap avatar → [`TopMenuController.OnAvatarClicked`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/TopMenuController.cs) → Nav: `ShowPopupAsync("UI.ProfilePopup")`
    * `CurrencyBalanceChangedEvent` (EventBus) → [`TopMenuController.OnCurrencyChanged`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/TopMenuController.cs) → UI: `coinChip.balanceText N0` + `heartChip.countText` + `DOPunchScale` + `timerText MM:SS` / `FULL` | Logic: `ServiceLocator.TryGet<ICurrencyService>().GetBalance(id)` (once on enable, then mirror via event) + heart regen coroutine | Nav: none
  * `ScreenContainer`
    * `ScreenHome` ([`HomeScreenController`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/HomeScreenController.cs) : `ScreenCanvasController`, Canvas, CanvasScaler, GraphicRaycaster, CanvasGroup)
      * `Background_Home` (RectTransform, CanvasRenderer, Image — stretch 0,0–1,1, rgba(0,0,0,0.784)) — non-interactive
      * `LeftMenu` ([`SideMenuController`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/SideMenuController.cs), VerticalLayoutGroup spacing 12, ContentSizeFitter)
        * `Button_Side` (RectTransform, CanvasRenderer, Image, Button, LayoutElement 72×72) — `OFFER.1` (icon 🎁, badge ●1)
          * `Icon` (Image 100×100) + `Label` (TextMeshProUGUI 180×40) + `Badge` (Image 36×36 anchor 1,1) / `BadgeText` (TextMeshProUGUI 18)
          * tap → [`SideMenuController.OnOfferClicked(0)`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/SideMenuController.cs) → UI: `DOKill` + `DOPunchScale(pulseScale, pulseDuration)` + `SetUpdate(true)` | Logic: `HapticType.Selection` | Nav: `UIManager.ShowPopupAsync<PopupCanvasController>("UI.Offer1Popup")` → `PopupStack.push(Popup_Offer1)` (close reveals `ScreenHome`)
        * `Button_Side (1)` — `STARTER PACKAGE` → tap → `OnOfferClicked(1)` → Nav: `"UI.StarterPackagePopup"`
        * `Button_Side (2)` — `STAR CHEST` (badge ●3) → tap → `OnOfferClicked(2)` → Nav: `"UI.StarChestPopup"`
      * `Button_Text` (RectTransform, CanvasRenderer, Image, Button 400×200, [`PlayLevelController`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/PlayLevelController.cs))
        * `Text (TMP)` (TextMeshProUGUI "Level 2", fontSize 65.6) + `badgeBackground` (Image)
        * tap → [`PlayLevelController.OnPlayClicked`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/PlayLevelController.cs) → UI: `DOPunchScale` + [`PlayLevelController.BindLevel`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/PlayLevelController.cs) reads `LevelManager<LevelData>.Service.CurrentLevelIndex` → `LV{N}` (InvariantCulture) | Logic: `LevelManager.LoadCurrentLevelAsync()` | Nav: `UIManager.ShowScreenAsync<ScreenCanvasController>("UI.PlayScreen")` (future; SDK placeholder today)
        * lifecycle: `HomeScreenController.OnInit` → `playLevel?.BindLevel()`; `OnShow` → `BindLevel()` (refresh after gameplay)
      * `RightMenu` ([`SideMenuController`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/SideMenuController.cs), VerticalLayoutGroup spacing 12, ContentSizeFitter)
        * `Button_Side` — `NO ADS` → tap → `OnOfferClicked(0)` → Nav: `"UI.NoAdsPopup"`
        * `Button_Side (1)` — `WHEEL` → tap → `OnOfferClicked(1)` → Nav: `"UI.WheelPopup"`
  * `PersistentBottom` ([`BottomMenuController`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/BottomMenuController.cs), HorizontalLayoutGroup, `BottomMenuSettings`)
    * `ButtonBottomMenuController[0]` (`Button_Menu`, Button + RectTransform tabRect + Image tabGraphic + vfxObject) — `STORE` → tap → [`BottomMenuController.SelectTab(0)`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/BottomMenuController.cs) → UI: `DOKill` + `DOAnchorPosY(moveYOffset)` + `DOColor(selectedColor/defaultColor)` + `vfxObject.SetActive(selected)` | Logic: `HapticType.Selection` (via child controller) | Nav: `UIManager.ShowScreenAsync<ScreenCanvasController>("UI.StoreScreen")` → `Hide(prevScreen)` + `Show(StoreScreen)`; BottomMenu survives (persistent)
    * `ButtonBottomMenuController[1]` — `(reserved)` → tap → `SelectTab(1)` → UI: highlight only | Logic: none | Nav: no-op (empty `screenPrefabPath`)
    * `ButtonBottomMenuController[2]` — `HOME ★` (default selected) → tap → `SelectTab(2)` → Nav: `"UI.HomeScreen"` (no-op if already on Home)
    * `ButtonBottomMenuController[3]` — `LEADERBOARD` → tap → `SelectTab(3)` → Nav: `"UI.LeaderboardScreen"`
    * `ButtonBottomMenuController[4]` — `ACHIEVEMENT` → tap → `SelectTab(4)` → Nav: `"UI.AchievementScreen"`
    * invariant: single-active; `SelectTab` no-ops if `index == _currentIndex` or out of bounds; `WireListeners` uses captured `int capturedIndex` + stored `UnityAction` → `RemoveListener` on `OnDisable`/`OnDestroy`

> Popup stack note: `PopupCanvasController` + `UIManager._popupStack` (Stack<PopupCanvasController>).
> `ShowPopupAsync` pushes + `Show()` (CanvasGroup `DOFade` alpha 0→1, `interactable=true`, `blocksRaycasts=true`, `SetUpdate(true)` for pause).
> `HidePopup(top)` pops + `Hide()` (DOFade 1→0); `HidePopup(closeAll:true)` empties stack; `CloseAndDestroyPopup` pops-if-top + `Destroy(go)` + removes from `_activeByType`.
> Dim tap (`Background_Dim` Button) → `HidePopup` (or `CloseAndDestroyPopup` for Win/Lose continue flows).

### Interaction Details

> One row per tappable. `Next UI` = what the user sees change. `Logic` = service/manager/event call. `Nav` = UIManager key. Links are literal.

| # | Element (Mockup → Prefab) | Wiring (`WireListeners`) | Handler | Next UI (visual change) | Logic / Service | Navigation (Addressable key) |
|---|---------------------------|--------------------------|---------|-------------------------|-----------------|------------------------------|
| 1 | `OFFER.1` — `LeftMenu/Button_Side` | `SideMenuController.Awake → SpawnButtons() → btn.onClick.AddListener(() => OnOfferClicked(0))` stored `UnityAction`; `OnDisable → RemoveListener` | [`SideMenuController.OnOfferClicked(0)`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/SideMenuController.cs) | `Badge` ●1 stays; `DOKill` + `DOPunchScale(pulseScale, pulseDuration, ease)` on `Button_Side.transform`; dim + popup card fades in (`CanvasGroup.DOFade 0→1, SetUpdate(true)`) | `HapticManager.Haptic(HapticType.Selection)` | `UIManager.ShowPopupAsync<PopupCanvasController>("UI.Offer1Popup")` → `PopupStack.push` |
| 2 | `STARTER PACKAGE` — `LeftMenu/Button_Side (1)` | same `AddListener(OnOfferClicked(1))` | `OnOfferClicked(1)` | same punch | same haptic | `"UI.StarterPackagePopup"` |
| 3 | `STAR CHEST` — `LeftMenu/Button_Side (2)` | same `AddListener(OnOfferClicked(2))` | `OnOfferClicked(2)` | same punch; badge ●3 | same haptic | `"UI.StarChestPopup"` |
| 4 | `Level 2 — TAP TO PLAY` — `ScreenHome/Button_Text` | `PlayLevelController.Awake → playButton.onClick.AddListener(OnPlayClicked)` stored `UnityAction`; `OnDisable → RemoveListener` | [`PlayLevelController.OnPlayClicked`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/PlayLevelController.cs) | `DOPunchScale` on `Button_Text.transform`; label `Level 2` refreshed via [`BindLevel()`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/PlayLevelController.cs) → `levelText.text = $"LV{N}"` (`InvariantCulture`, `CurrentLevelIndex+1`) | `ServiceLocator.Get<ILevelManager<LevelData>>().CurrentLevelIndex` + `LoadCurrentLevelAsync()` | (SDK) `UIManager.ShowScreenAsync<ScreenCanvasController>("UI.PlayScreen")` — board placeholder 1:1 `AspectRatioFitter` + `PlayHudController` HUD |
| 5 | `NO ADS` — `RightMenu/Button_Side` | `SideMenuController` same | `OnOfferClicked(0)` | same punch | same haptic | `"UI.NoAdsPopup"` |
| 6 | `WHEEL` — `RightMenu/Button_Side (1)` | same | `OnOfferClicked(1)` | same punch | same haptic | `"UI.WheelPopup"` |
| 7 | `Coin +` — `PersistentTop/CoinChip/addButton` | [`TopMenuController.Awake → WireListeners()`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/TopMenuController.cs) `coinChip.addButton.onClick.AddListener(_coinAddAction)` stored `UnityAction`; `OnDisable → UnwireListeners → RemoveListener` | [`TopMenuController.OnCoinAddClicked`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/TopMenuController.cs) | `coinChip.balanceText DOKill + DOPunchScale` (on `CurrencyBalanceChangedEvent`, not on click) | Never `ICurrencyService.Grant` from UI (gameplay-owned) | `ShowPopupAsync<PopupCanvasController>("UI.ShopPopup")` (virtual `ShowPopupAsync<T>` seam for tests) |
| 8 | `♥ +` — `PersistentTop/HeartChip/addButton` | same `heartChip.addButton.onClick.AddListener(_heartAddAction)` | [`TopMenuController.OnHeartAddClicked`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/TopMenuController.cs) | `heartChip.countText DOPunchScale` on event | — | `ShowPopupAsync("UI.LivesRefillPopup")` |
| 9 | `⚙` — `PersistentTop/settingsButton` | `settingsButton.onClick.AddListener(_settingsAction)` | [`TopMenuController.OnSettingsClicked`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/TopMenuController.cs) | — | `HapticType.Selection` | `ShowPopupAsync<PopupCanvasController>("UI.SettingsPopup")` (`ZenoGames.Feature.Setting.UI.SettingsPopupCanvasController` when asmdef ref exists; fallback `PopupCanvasController`) |
| 10 | `Avatar` — `PersistentTop/avatarButton` | `avatarButton.onClick.AddListener(_avatarAction)` | [`TopMenuController.OnAvatarClicked`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/TopMenuController.cs) | `AvatarController.Bind(profile)` / `Clear()` placeholder | `ServiceLocator.TryGet<IUserProfileService>()` | `ShowPopupAsync("UI.ProfilePopup")` |
| 11 | `Coin balance` (event) | `OnEnable → EventBus.Subscribe(_onCurrencyChanged)` stored `Action<CurrencyBalanceChangedEvent>`; `OnDisable → Unsubscribe` | [`TopMenuController.OnCurrencyChanged`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/TopMenuController.cs) | `coinChip.balanceText.text = N0` + `DOKill` + `DOPunchScale` when `e.CurrencyId == coinId` | `GetEffectiveCoinId()`: `coinChip.currencyId` → `settings.coinCurrencyId` → `"coin"` fallback | — |
| 12 | `Heart balance` (event + timer) | same subscription | same `OnCurrencyChanged` (heart branch) | `heartChip.countText` + `timerText MM:SS` (`FormatTimer` CeilToInt) or `"FULL"` when `>= heartMax`; `timerText.DOColor(timerUrgentColor)` when `<60s`; `DOPunchScale` on count change; regen coroutine `HeartTimerRoutine` ticks `timerTickInterval` | `GetEffectiveHeartId()` → `settings.heartCurrencyId` → `"heart"`; `ServiceLocator.TryGet<ICurrencyService>().GetBalance` once on enable; local `nextRegenUtc` countdown; `heartRegenDurationSec` reset on each regen | — |
| 13 | `STORE` tab — `PersistentBottom[0]` | [`BottomMenuController.Awake → WireListeners()`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/BottomMenuController.cs) `tabs[i].Button.onClick.AddListener(capturedIndex => SelectTab(capturedIndex))` stored `UnityAction`; `OnDisable → UnwireListeners` | [`BottomMenuController.SelectTab(0)`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/BottomMenuController.cs) | `DOKill` + `DOAnchorPosY(moveYOffset)` + `DOColor(selectedColor)` on `tabRect/tabGraphic`; `vfxObject.SetActive(true)`; previous tab `ResetState()` | `HapticType.Selection` (via `ButtonBottomMenuController.Highlight`) | `UIManager.ShowScreenAsync<ScreenCanvasController>("UI.StoreScreen")` → `Hide(prevScreen)` + `Show(StoreScreen)` |
| 14 | `HOME` tab — `PersistentBottom[2]` ★ | same | `SelectTab(2)` | same highlight (★ when selected) | — | `"UI.HomeScreen"` (no-op if `_currentIndex == 2`) |
| 15 | `LEADERBOARD` / `ACHIEVEMENT` — `PersistentBottom[3,4]` | same | `SelectTab(3)` / `SelectTab(4)` | same | — | `"UI.LeaderboardScreen"` / `"UI.AchievementScreen"` |
| 16 | `Pause → Resume` (Play HUD) | `PlayHudController` `pauseButton.onClick.AddListener(OnPauseClicked)` | `OnPauseClicked` → `UIManager.ShowPopupAsync<PausePopupCanvasController>("UI.PausePopup")` → [`PausePopupCanvasController.OnShow`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/PausePopupCanvasController.cs) | `Time.timeScale = 0` + `SoundManager.PauseBGM` (soft duck); popup `DOFade` with `SetUpdate(true)` still runs while paused | `Time.timeScale` + `SoundManager` | stacked `PausePopup` |
| 17 | `Pause → Home` (destructive) | `homeButton.onClick.AddListener(OnHome)` | [`PausePopupCanvasController.OnHome`](../../../Assets/_ZenoUI/Scripts/Runtime/UIController/PausePopupCanvasController.cs) | Confirm guard | `HapticType.Warning` | `ShowPopupAsync<ConfirmPopupCanvasController>("UI.ConfirmPopup")` ("Quit to Home?") → on `Confirmed`: `UIManager.HidePopup(pause, closeAll:true)` + `ShowScreenAsync<HomeScreenController>("UI.HomeScreen")` + `Time.timeScale=1`; on cancel: stay on Pause |

> Stack & lifecycle contracts (from `UIManager.cs` + `CanvasController.cs`):
> `Show()` = `OnPreShow` → `DOFade 0→1` (`fadeInDuration 0.25s Ease.OutQuad`, `SetUpdate(true)`) → `OnShow` → `IsVisible=true`, `CanvasGroup alpha=1, interactable=true, blocksRaycasts=true`.
> `Hide()` = `OnPreHide` → `DOFade 1→0` (`fadeOutDuration 0.20s Ease.InQuad`) → `OnHide` → `IsVisible=false`, `alpha=0, interactable=false, blocksRaycasts=false`. `HideImmediate` skips tween.
> Out-of-bounds `SelectTab` and redundant tap (`_currentIndex == index`) are no-ops (logged in Editor).

### State Changes

> Before → After for each primary flow. Useful for reviewers to eyeball.

| Flow | Before | After | Visually |
|------|--------|-------|----------|
| Tap `OFFER.1` | `ScreenHome` visible, `PopupStack=[]`, `IsVisible(Home)=true` | `ScreenHome` still visible dimmed behind; `Popup_Offer1 IsVisible=true`, `PopupStack=[Popup_Offer1]`, `alpha=1` | Dim overlay + card slides/fades in |
| Tap `TAP TO PLAY` | `Level 2` label `LV2` | `ScreenPlay` visible, `ScreenHome` hidden (`IsVisible=false, alpha=0`), level index +1 on return (refreshed in `HomeScreenController.OnShow → BindLevel()`) | Full-screen swap via `ShowScreenAsync` hide/show |
| Tap `STORE` tab | `CurrentScreen=HomeScreen`, `CurrentIndex=2` | `CurrentScreen=StoreScreen`, `CurrentIndex=0`, prev tab `ResetState` (Y=0, color=default) | Bottom tab lifts (`DOAnchorPosY`) + recolour + bottom content scrolls to top (`verticalNormalizedPosition=1`) |
| `CurrencyBalanceChangedEvent(coin, +500)` | `coinChip.balanceText="1,500"` | `"2,000"` + `DOPunchScale` pulse | Chip text pops |
| `Heart regen tick` | `timerText="01:23"` | `"01:22"` → … → `"00:00"` → `countText+1` + `FULL` when `>=heartMax` | Countdown ticks; urgent red when `<60s` |
| `Pause → Resume` | `Time.timeScale=1`, gameplay running | `Time.timeScale=0`, `PausePopup IsVisible=true`, BGM ducked; on Resume → `timeScale=1`, popup hidden, BGM resumed | Game freezes; dim + PAUSED card |

### Controller Code

> Current code for this controller (or new controller scaffold when `(to be created)`).
> Show the wiring, lifecycle, handlers, and test seams. Keep smart comments on `DOKill` guards,
> stored `UnityAction` identity, and `UIManager` keys.

```csharp
// File: Assets/_ZenoUI/Scripts/Runtime/UIController/<ControllerClass>.cs
// Namespace: ZenoGames.UI — Base: <BaseClass> (ScreenCanvasController / PopupCanvasController / MonoBehaviour)
// Prefab: <PrefabName>.prefab — Settings: <SettingsClass> (when applicable)

using System.Globalization; // For N0 / InvariantCulture balance + level formatting
using System.Threading.Tasks;
using DG.Tweening;
using TMPro;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;
using ZenoGames.Interface; // IAssetManager, ICurrencyService, ILevelManager, ServiceLocator, EventBus

namespace ZenoGames.UI
{
    /// <summary>
    /// One-line role + where it sits in Canvas hierarchy (persistent vs ScreenContainer).
    /// Attach to <RootGO> in <PrefabName>.prefab.
    /// </summary>
    public class <ControllerClass> : <BaseClass>
    {
        [Header("Config")]
        [SerializeField] private <SettingsClass> settings;

        [Header("Elements — wired to prefab children")]
        [SerializeField] private Button primaryButton;          // e.g. playButton / closeButton / confirmButton
        [SerializeField] private TextMeshProUGUI titleText;     // e.g. levelText / balanceText / headerTitle
        // [SerializeField] private SideMenuController leftMenu, rightMenu; // when composing side menus
        // [SerializeField] private Transform container; [SerializeField] private GameObject buttonPrefab; // when spawning

        // Stored delegate identities — required so RemoveListener matches AddListener (lambda identity fix).
        private UnityAction _primaryAction;
        // private UnityAction _secondaryAction;
        // private System.Action<CurrencyBalanceChangedEvent> _onCurrencyChanged;

        // ----- Test seams -----
        public <SettingsClass> Settings => settings;
        // public IReadOnlyList<...> Wired => _wired; // when spawning

        protected override void Awake()
        {
            base.Awake();
            // Cache original scales / colours for DOKill + DOPunchScale restore.
            _primaryAction = OnPrimaryClicked;
            // _secondaryAction = OnSecondaryClicked;
            // _onCurrencyChanged = OnCurrencyChanged;
            WireListeners();
        }

        private void OnEnable()
        {
            // Re-wire after SetActive toggle; guard against double wiring.
            if (_primaryAction != null) WireListenersIfNeeded();
            // EventBus.Subscribe(_onCurrencyChanged);
            // BindAvatar(); InitBalances(); StartHeartTimer(); // when mirroring currency
        }

        private void OnDisable()
        {
            // EventBus.Unsubscribe(_onCurrencyChanged);
            UnwireListeners();
        }

        protected override void OnDestroy()
        {
            base.OnDestroy();
            UnwireListeners();
            // DOKill all tween targets to prevent orphaned tweens after Destroy.
            primaryButton?.transform.DOKill();
            titleText?.DOKill();
            titleText?.transform.DOKill();
        }

        // ----- Wiring (dynamic only — never Inspector onClick) -----

        private void WireListeners()
        {
            UnwireListeners();
            if (primaryButton != null && _primaryAction != null)
                primaryButton.onClick.AddListener(_primaryAction);
            // if (secondaryButton != null && _secondaryAction != null)
            //     secondaryButton.onClick.AddListener(_secondaryAction);
        }

        private void WireListenersIfNeeded()
        {
            // Guard for OnEnable after SetActive(false/true) cycle.
            // Implement via _isWired bool or _wired.Count == 0 check.
        }

        private void UnwireListeners()
        {
            if (primaryButton != null && _primaryAction != null)
                primaryButton.onClick.RemoveListener(_primaryAction);
            // if (secondaryButton != null && _secondaryAction != null)
            //     secondaryButton.onClick.RemoveListener(_secondaryAction);
        }

        // ----- Lifecycle (ScreenCanvasController / PopupCanvasController hooks) -----

        protected override void OnInit()
        {
            base.OnInit();
            // One-time init: refresh labels, build spawned children.
            // e.g. playLevel?.BindLevel();
        }

        protected override void OnShow()
        {
            base.OnShow();
            // Refresh on every show (e.g. level may have advanced while away).
            // Time.timeScale = 0; // for PausePopup
        }

        protected override void OnHide()
        {
            base.OnHide();
            // Time.timeScale = 1; // restore
        }

        // ----- Handlers — one per tappable, each shows UI change + logic + navigation -----

        /// <summary>
        /// Primary CTA tapped — punch, haptic, then navigate.
        /// Linked from <PrefabName>.prefab → <RootGO>/Button_Text (Button) via primaryButton field.
        /// </summary>
        private void OnPrimaryClicked()
        {
            // Smart comment: DOKill before every tween to avoid stacking when user spams.
            primaryButton?.transform.DOKill();
            primaryButton?.transform.DOPunchScale(Vector3.one * 0.08f, 0.22f, 1, 0.5f);

            // HapticType.Selection for normal, Warning for destructive.
            // ServiceLocator.Get<IHapticService>()?.Haptic(HapticType.Selection);

            // Navigation — literal Addressable key, never guessed.
            _ = ShowPopupAsync<PopupCanvasController>("UI.<TargetPopup>");
            // or: _ = UIManager.ShowScreenAsync<ScreenCanvasController>("UI.<TargetScreen>");
            // or: UIManager.HidePopup(this); UIManager.CloseAndDestroyPopup(this);
        }

        /// <summary>
        /// Destructive path — must go through ConfirmPopup guard.
        /// </summary>
        private async void OnDestructiveClicked()
        {
            var confirm = await UIManager.ShowPopupAsync<PopupCanvasController>("UI.ConfirmPopup");
            // confirm.Bind("Quit to Home?"); // set message via controller API
            // if (await confirm.WaitForResultAsync() != ConfirmResult.Confirmed) return; // cancelled → stay
            // UIManager.HidePopup(this, closeAll: true);
            // _ = UIManager.ShowScreenAsync<ScreenCanvasController>("UI.HomeScreen");
        }

        // ----- Helpers -----

        /// <summary>Virtual UIManager seam so EditMode tests can override without Addressables.</summary>
        protected virtual Task<T> ShowPopupAsync<T>(string key) where T : PopupCanvasController
            => UIManager.ShowPopupAsync<T>(key);

        /// <summary>Test hook — force wire without toggling active.</summary>
        public void WireForTest() => WireListeners();

        /// <summary>Test hook — force unwire.</summary>
        public void UnwireForTest() => UnwireListeners();
    }
}
```

> For composed screens (e.g. `HomeScreenController` side-only), the controller is intentionally thin —
> it only owns `leftMenu`/`rightMenu`/`playLevel` fields and refreshes `playLevel.BindLevel()` in
> `OnInit`/`OnShow`. Each child (`SideMenuController`, `PlayLevelController`, `TopMenuController`,
> `BottomMenuController`) is documented in its own `*_Controller.md` with the same template; link to them
> from `Related` and from Tree Flow leaves.

### Verification

- [ ] Every tappable in `Visual Reference` has one row in `Interaction Details`, one path in `UI Flow Diagram`, one leaf in `Tree Flow`.
- [ ] Every `UIManager` key is a literal string present in `AddressableAssetSettings` (or marked `(to be created)`).
- [ ] Every `onClick` shows dynamic `AddListener` with stored `UnityAction` + `RemoveListener` in `OnDisable`/`OnHide`/`OnDestroy`; no Inspector `onClick`.
- [ ] Every tween shows `DOKill` guard; pause flows use `SetUpdate(true)`.
- [ ] `CanvasController` lifecycle (`OnInit`/`OnPreShow`/`OnShow`/`OnPreHide`/`OnHide` + `IsVisible` + `CanvasGroup` alpha/interactable/blocksRaycasts) is respected.
- [ ] `Controller Code` compiles against `ZenoGames.UI` + `ZenoGames.Interface` + `DOTween` + `TextMeshPro`.
- [ ] No `TODO`/`TBD`/`FIXME`; all `Related` links resolve; mermaid blocks render.
```

---

## Template Usage Notes

- **Keep structure byte-for-byte.** Section order is `Overview → Composition → Visual Reference → UI Flow Diagram → Tree Flow → Interaction Details → State Changes → Controller Code → Verification`. Do not reorder, wrap in `<details>`, or insert extra sections.
- **Every arrow traceable.** If you cannot point to a mockup label + prefab GO + controller field + `onClick` wiring + handler + service call + UIManager key for a flow arrow, the arrow must not exist.
- **Prefer the example.** The `HomeScreenController` example above uses real guids (`ScreenHome.prefab` `770dd50366a754d39ad489dbd600cccf`, `Button_Side` `d628eda2f5f13405f932c41ad8cab250`, `SideMenuSettings` `5810730efa7834d0b94b9def81952a92`) and real code paths. Copy its style when filling a new controller.
- **New controller scaffold.** When `Controller: (to be created)`, the `Controller Code` section becomes the creation spec — propose a compiling scaffold (namespace `ZenoGames.UI`, base `ScreenCanvasController`/`PopupCanvasController`/`MonoBehaviour`, `[SerializeField]` fields mirroring prefab children, lifecycle hooks, wiring, handlers, and test seams). Mark new files in `File Map`.
- **Stack semantics.** Screens hide the previous `CurrentScreen`; popups push onto `PopupStack` (LIFO); `closeAll` empties the stack; `CloseAndDestroyPopup` removes from `_activeByType` + destroys `GameObject`.
