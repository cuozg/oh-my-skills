# Dragon Crashers — Architecture in Practice

## UIView Base Class — Template Method

```csharp
public class UIView : IDisposable {
    protected bool m_HideOnAwake = true;
    protected VisualElement m_TopElement;
    public UIView(VisualElement topElement) {
        m_TopElement = topElement ?? throw new ArgumentNullException(nameof(topElement));
        Initialize();
    }
    public virtual void Initialize() { if (m_HideOnAwake) Hide(); SetVisualElements(); RegisterButtonCallbacks(); }
    protected virtual void SetVisualElements() { }
    protected virtual void RegisterButtonCallbacks() { }
    public virtual void Show() => m_TopElement.style.display = DisplayStyle.Flex;
    public virtual void Hide() => m_TopElement.style.display = DisplayStyle.None;
    public virtual void Dispose() { }
}
```

Template: cache Q() in `SetVisualElements()`, register events in `RegisterButtonCallbacks()`, fire static events — no business logic in views.

## Screen Controller — Thin Coordinator

```csharp
public class HomeScreenController : MonoBehaviour {
    [SerializeField] LevelSO m_LevelData;
    void OnEnable() => HomeEvents.PlayButtonClicked += OnPlayGameLevel;
    void OnDisable() => HomeEvents.PlayButtonClicked -= OnPlayGameLevel;
    void Start() => HomeEvents.LevelInfoShown?.Invoke(m_LevelData);
    public void OnPlayGameLevel() {
        HomeEvents.MainMenuExited?.Invoke();
        SceneManager.LoadSceneAsync(m_LevelData.sceneName);
    }
}
```

Controller knows data (`LevelSO`) + services (`SceneManager`). View knows `VisualElement`. Communication via static events only.

## TabbedMenuController — Reusable Sub-Controller

```csharp
[System.Serializable]
public struct TabbedMenuIDs {
    public string tabClassName, selectedTabClassName, unselectedContentClassName;
    public string tabNameSuffix, contentNameSuffix;
}
public class TabbedMenuController {
    readonly VisualElement m_Root; readonly TabbedMenuIDs m_IDs;
    public TabbedMenuController(VisualElement root, TabbedMenuIDs ids) { m_Root = root; m_IDs = ids; }
    public void RegisterTabCallbacks() =>
        m_Root.Query<VisualElement>(className: m_IDs.tabClassName).ForEach(t => t.RegisterCallback<ClickEvent>(OnTabClick));
    // OnTabClick: deselect all tabs, select clicked tab, swap content visibility via suffix replacement
}
```

Convention-based tab↔content mapping via suffix replacement.

## Custom Controls — HealthBarComponent

```csharp
public class HealthBarComponent : VisualElement {
    // ⚠️ DC uses deprecated UxmlFactory/UxmlTraits — migrate to [UxmlElement] + [UxmlAttribute]
    Label _titleLabel, _healthStat; VisualElement _progress;
    public HealthBarComponent() {
        AddToClassList("health-bar__container");
        var titleBg = new VisualElement(); titleBg.AddToClassList("health-bar__title_background"); Add(titleBg);
        _titleLabel = new Label(); _titleLabel.AddToClassList("health-bar__title"); titleBg.Add(_titleLabel);
        var bg = new VisualElement(); bg.AddToClassList("health-bar__background"); Add(bg);
        _progress = new VisualElement(); _progress.AddToClassList("health-bar__progress"); bg.Add(_progress);
        _healthStat = new Label(); _healthStat.AddToClassList("health-bar__label"); _progress.Add(_healthStat);
    }
    void SetHealth(int cur, int max) {
        _healthStat.text = $"{cur}/{max}";
        if (max > 0) _progress.style.width = Length.Percent(Mathf.Clamp((float)cur / max * 100, 0f, 100f));
    }
}
```

## SlideToggle — BaseField<bool>

```csharp
public class SlideToggle : BaseField<bool> {
    // ⚠️ DC uses deprecated UxmlFactory — migrate to [UxmlElement]
    VisualElement m_Input, m_Knob;
    public SlideToggle(string label = null) : base(label, null) {
        AddToClassList("slide-toggle");
        m_Input = this.Q(className: BaseField<bool>.inputUssClassName);
        m_Knob = new(); m_Knob.AddToClassList("slide-toggle__input-knob"); m_Input.Add(m_Knob);
        RegisterCallback<ClickEvent>(evt => { value = !value; evt.StopPropagation(); });
    }
    public override void SetValueWithoutNotify(bool newValue) {
        base.SetValueWithoutNotify(newValue);
        m_Input.EnableInClassList("slide-toggle__input--checked", newValue);
    }
}
```

**Why `BaseField<bool>`:** Auto `ChangeEvent<bool>`, built-in label, `INotifyValueChanged<bool>` for binding.

## Naming & Composite Views

BEM convention: `.health-bar__container`, `.slide-toggle__input--checked`. Parent views create sub-views in `Initialize()`, cascade `Dispose()`.

## Dynamic UI — VisualTreeAsset.Instantiate()

```csharp
// Pattern: VisualTreeAsset.Instantiate() → new Controller(data) → SetVisualElements → SetGameData → RegisterCallbacks → parent.Add(elem)
// Use Instantiate() for <50 items. ListView for 100+ items.
```

## Button.userData

```csharp
m_BuyButton.userData = m_ShopItemData;  // no closures needed
m_BuyButton.RegisterCallback<ClickEvent>(BuyAction);
m_BuyButton.RegisterCallback<PointerMoveEvent>(evt => evt.StopImmediatePropagation()); // prevent ScrollView drag
```

## UIManager — Single-Document Navigation

```csharp
// Single UIDocument with subtree views. All views share one root.
// SetupViews(): root.Q<VisualElement>("HomeScreen") → new HomeView(...)
// ShowModalView(newView): current.Hide() → previous=current → current=newView.Show()
// Overlay: previous=current, overlayView.Show() (no hide)
// OnDisable: foreach(v in allViews) v.Dispose()
```

Single UIDocument, subtree views. Modal replaces; overlay stacks.
