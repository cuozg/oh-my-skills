# UI Toolkit Code Templates

> DC patterns → [project-patterns.md](project-patterns.md). QuizU patterns → [quizu-patterns.md](quizu-patterns.md). Theme tokens → `ui-toolkit-theming/SKILL.md`. Advanced patterns → [code-templates-advanced.md](code-templates-advanced.md).

## 1. Base Screen (UXML + USS)

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements">
  <ui:VisualElement name="screen-root" class="screen">
    <ui:VisualElement name="header" class="header">
      <ui:Button name="btn-back" class="btn-icon btn-back"/>
      <ui:Label name="title" class="header-title" text="Title"/>
      <ui:VisualElement class="header-spacer"/>
    </ui:VisualElement>
    <ui:ScrollView name="content" class="content" mode="Vertical" horizontal-scroller-visibility="Hidden"/>
    <ui:VisualElement name="footer" class="footer"/>
  </ui:VisualElement>
</ui:UXML>
```

```css
.screen { flex-grow:1; flex-direction:column; }
.header { flex-direction:row; align-items:center; height:56px; padding:0 16px; flex-shrink:0; }
.content { flex-grow:1; }
.footer { flex-direction:row; height:64px; flex-shrink:0; }
```

## 2. UIScreen (QuizU Stack Nav)

```csharp
public abstract class UIScreen
{
    protected VisualElement m_RootElement, m_Screen;
    public UIScreen(VisualElement root) { m_RootElement = root; Initialize(); }
    protected abstract void Initialize();
    public virtual void Show() { m_Screen.RemoveFromClassList("screen-hidden"); m_Screen.AddToClassList("screen-visible"); }
    public virtual void Hide() { m_Screen.RemoveFromClassList("screen-visible"); m_Screen.AddToClassList("screen-hidden"); }
}
```

## 3. Custom Control (`[UxmlElement]`, Unity 6+)

> DC uses legacy `UxmlFactory`/`UxmlTraits` — see [project-patterns.md](project-patterns.md).

```csharp
[UxmlElement]
public partial class CustomCard : VisualElement
{
    [UxmlAttribute] public string Title { get => _title?.text ?? ""; set { if (_title != null) _title.text = value; } }
    Label _title;
    public CustomCard()
    {
        AddToClassList("custom-card");
        _title = new Label { name = "title" }; Add(_title);
        RegisterCallback<PointerDownEvent>(e => { ToggleInClassList("custom-card--selected"); e.StopPropagation(); });
    }
}
```

