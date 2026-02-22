## Base Components USS (Token-Consuming)

```css
.screen { flex-grow: 1; background-color: var(--color-bg-primary); padding: var(--space-8); }
.btn { padding: var(--space-2) var(--space-4); border-radius: var(--radius-md); font-size: var(--font-size-md); -unity-font-style: bold; border-width: 0; transition: background-color var(--transition-fast) var(--ease-default); }
.btn-primary { background-color: var(--color-primary-500); color: var(--color-text-inverse); }
.btn-primary:hover { background-color: var(--color-primary-700); }
.btn-primary:active { background-color: var(--color-primary-900); }
```

## Theme-Aware Custom Control — StatusBadge

```csharp
[UxmlElement]
public partial class StatusBadge : VisualElement {
    readonly Label _label;
    [UxmlAttribute] public string Text { get => _label.text; set => _label.text = value; }
    [UxmlAttribute] public StatusType Status { get => _status; set { _status = value; UpdateStatusClass(); } }
    StatusType _status;
    public enum StatusType { Success, Warning, Error }
    public StatusBadge() { AddToClassList("status-badge"); _label = new Label(); Add(_label); }
    // UpdateStatusClass: remove all status-badge--* classes, add matching one via switch
}
```

```css
.status-badge { padding: var(--space-1) var(--space-3); border-radius: var(--radius-full); }
.status-badge--success { background-color: var(--color-status-success); }
.status-badge--warning { background-color: var(--color-status-warning); }
.status-badge--error { background-color: var(--color-status-error); }
```

<!-- See also: theming-code-patterns-part2.md -->
