# USS Styling

## Selector Types

```css
/* Type selector — matches element type */
Button { background-color: #333; }

/* Class selector — primary styling method */
.button { padding: 8px 16px; }
.button--primary { background-color: var(--color-primary); }
.button__icon { width: 24px; height: 24px; }

/* Name selector — specific element */
#submit-btn { font-size: 18px; }

/* Pseudo-classes */
.button:hover { background-color: var(--color-hover); }
.button:active { scale: 0.98; }
.button:focus { border-color: var(--color-focus); }
.button:disabled { opacity: 0.5; }
```

## Custom Properties (Variables)

```css
:root {
  /* Colors */
  --color-primary: rgb(0, 122, 255);
  --color-secondary: rgb(88, 86, 214);
  --color-bg: rgb(28, 28, 30);
  --color-surface: rgb(44, 44, 46);
  --color-text: rgb(255, 255, 255);
  --color-text-secondary: rgb(174, 174, 178);
  --color-hover: rgba(255, 255, 255, 0.1);
  --color-focus: rgb(0, 122, 255);

  /* Spacing */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;

  /* Typography */
  --font-size-sm: 12px;
  --font-size-md: 14px;
  --font-size-lg: 18px;
  --font-size-xl: 24px;

  /* Borders */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
}
```

## Flexbox Layout

```css
/* Horizontal row with centered items */
.row {
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}

/* Vertical stack with gap */
.stack {
  flex-direction: column;
  padding: var(--space-md);
}
.stack > * { margin-bottom: var(--space-sm); }

/* Fill available space */
.fill { flex-grow: 1; }

/* Fixed size */
.sidebar { width: 280px; flex-shrink: 0; }

/* Responsive child */
.content { flex-grow: 1; min-width: 0; }
```

## Performance Rules

- BEM single-class selectors (`.button--primary`) over deep hierarchy (`.container > .menu > Button`)
- Selector cost = N1 (classes on element) × N2 (USS files loaded)
- Avoid `:hover` on deeply nested elements — triggers re-style on every mouse move
- Use USS files over inline styles — inline styles allocate per-element memory
- Keep USS files focused: one per screen + one shared variables file
