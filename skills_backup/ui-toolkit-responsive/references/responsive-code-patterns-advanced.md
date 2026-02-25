# Responsive Code Patterns (Advanced)

> See [responsive-code-patterns.md](responsive-code-patterns.md) for flexbox, safe area handling, and breakpoint classifier.

## Common Responsive Patterns

```css
/* Card grid: 1-col → 2-col → 3-col */
.card-grid { flex-direction: row; flex-wrap: wrap; }
.card-grid__item { width: 50%; }
.screen-sm .card-grid__item { width: 100%; }
.screen-lg .card-grid__item { width: 33.3%; }
.screen-xl .card-grid__item { width: 25%; }

/* Two-pane: sidebar collapses on small */
.split-layout { flex-direction: row; flex-grow: 1; }
.split-layout__sidebar { width: 280px; flex-shrink: 0; }
.split-layout__main { flex-grow: 1; }
.screen-sm .split-layout { flex-direction: column; }
.screen-sm .split-layout__sidebar { width: 100%; max-height: 200px; }
```
