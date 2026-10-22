# Custom Controls

## UxmlElement Pattern (Unity 6+)

`[UxmlElement]` + `[UxmlAttribute]` are source-generated; the class must be `partial`.
UXML element name defaults to the class name; attribute names become kebab-case
(`MaxValue` -> `max-value`).

```csharp
using UnityEngine.UIElements;

[UxmlElement]
public partial class StatBar : VisualElement
{
    private readonly Label _label;
    private readonly VisualElement _fill;
    private string _text = "Health";
    private float _current = 1f;
    private float _maxValue = 1f;

    [UxmlAttribute] public string Text { get => _text; set { _text = value; Refresh(); } }
    [UxmlAttribute] public float Current { get => _current; set { _current = value; Refresh(); } }
    [UxmlAttribute] public float MaxValue { get => _maxValue; set { _maxValue = value; Refresh(); } }

    public StatBar()
    {
        AddToClassList("stat-bar");

        _label = new Label();
        _label.AddToClassList("stat-bar__label");
        Add(_label);

        var track = new VisualElement();
        track.AddToClassList("stat-bar__track");
        Add(track);

        _fill = new VisualElement();
        _fill.AddToClassList("stat-bar__fill");
        track.Add(_fill);

        Refresh();
    }

    // Setters call this so UXML, UI Builder, and code changes all update visuals
    private void Refresh()
    {
        _label.text = _text;
        float pct = _maxValue > 0 ? _current / _maxValue : 0f;
        _fill.style.width = Length.Percent(pct * 100f);
    }
}
```

## Usage in UXML

Controls inside a C# namespace need that namespace in UXML (e.g. `xmlns:game="MyGame.UI"` -> `<game:StatBar />`).

```xml
<UXML xmlns="UnityEngine.UIElements">
  <StatBar name="health-bar" text="HP" current="75" max-value="100" />
  <StatBar name="mana-bar" text="MP" current="30" max-value="50" />
</UXML>
```

## USS for Custom Control

```css
.stat-bar {
  flex-direction: row;
  align-items: center;
  margin-bottom: var(--space-sm);
}

.stat-bar__label {
  width: 60px;
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
}

.stat-bar__track {
  flex-grow: 1;
  height: 8px;
  background-color: var(--color-surface);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.stat-bar__fill {
  height: 100%;
  background-color: var(--color-primary);
  border-radius: var(--radius-sm);
}
```

## Guidelines

- Derive from `VisualElement` or built-in controls (`BaseField<T>`, `Button`)
- Add BEM classes in constructor: `AddToClassList("block")`, `AddToClassList("block__part")`
- Use `[UxmlAttribute]` for UXML-configurable properties (Unity 6+)
- Keep logic in the control; keep styling in USS
- Expose events for parent controllers: `public event Action<float> OnValueChanged`
- Update visuals from property setters; add `[CreateProperty]` to properties used as binding targets
- Migration only: `UxmlFactory`/`UxmlTraits` are obsolete in Unity 6 - replace with `[UxmlElement]`/`[UxmlAttribute]` when touched
- Deep custom-control work: plugin skill `unity:ui-uitk`
