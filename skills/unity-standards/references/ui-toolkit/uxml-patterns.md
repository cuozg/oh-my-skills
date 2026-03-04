# UXML Patterns

## Template Structure

```xml
<UXML xmlns="UnityEngine.UIElements">
  <Style src="./MainMenu.uss" />

  <VisualElement name="root" class="screen">
    <VisualElement name="header" class="header">
      <Label name="title" class="header__title" text="Main Menu" />
    </VisualElement>

    <VisualElement name="content" class="content">
      <Button name="play-btn" class="button button--primary" text="Play" />
      <Button name="settings-btn" class="button button--secondary" text="Settings" />
    </VisualElement>
  </VisualElement>
</UXML>
```

## BEM Naming Convention

```
block           → .button, .header, .modal
block__element  → .button__icon, .header__title, .modal__backdrop
block--modifier → .button--primary, .header--collapsed, .modal--fullscreen
```

- UXML `name` attribute → kebab-case: `name="play-btn"` (for C# `Q<T>("play-btn")`)
- USS classes → BEM: `class="button button--primary"` (for styling)

## Reusable Templates

```xml
<!-- Components/Card.uxml -->
<UXML xmlns="UnityEngine.UIElements">
  <VisualElement class="card">
    <Label name="card-title" class="card__title" />
    <Label name="card-desc" class="card__description" />
    <VisualElement name="card-actions" class="card__actions" />
  </VisualElement>
</UXML>

<!-- MainScreen.uxml — instantiate reusable template -->
<UXML xmlns="UnityEngine.UIElements">
  <Template src="Components/Card.uxml" name="CardTemplate" />

  <VisualElement class="screen">
    <Instance template="CardTemplate" name="card-1" />
    <Instance template="CardTemplate" name="card-2" />
  </VisualElement>
</UXML>
```

## Element Hierarchy Guidelines

```
Screen (root VisualElement)
├── Header (fixed top bar)
│   ├── Back Button
│   ├── Title Label
│   └── Action Buttons
├── Content (scrollable body)
│   ├── Sections / Cards / Lists
│   └── Interactive elements
└── Footer (fixed bottom bar)
    ├── Navigation tabs
    └── Status indicators
```

## Common Built-in Elements

| Element | Use Case | Key Attributes |
|---------|----------|----------------|
| `Label` | Static/dynamic text | `text` |
| `Button` | Actions | `text`, `clicked` event |
| `TextField` | Text input | `value`, `placeholder` |
| `Toggle` | On/off | `value`, `label` |
| `Slider` | Range input | `value`, `low-value`, `high-value` |
| `DropdownField` | Selection | `choices`, `value` |
| `ScrollView` | Scrollable container | `mode` (vertical/horizontal) |
| `ListView` | Virtualized list | `itemSource`, auto-pools items |
| `ProgressBar` | Progress display | `value`, `title` |
| `Foldout` | Collapsible section | `text`, `value` (open/closed) |

## File Organization

```
Assets/UI/
├── Screens/          ← full-screen UXML (MainMenu.uxml, Settings.uxml)
├── Components/       ← reusable UXML snippets (Card.uxml, Modal.uxml)
├── Styles/           ← USS files (theme.uss, variables.uss, screen-name.uss)
├── Controllers/      ← C# controllers (MainMenuController.cs)
└── Settings/         ← PanelSettings assets
```
