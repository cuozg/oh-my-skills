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

See [architecture-dc-patterns-advanced.md](architecture-dc-patterns-advanced.md) for custom controls, BaseField patterns, and UIManager navigation.
