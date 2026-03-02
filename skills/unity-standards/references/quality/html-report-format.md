# HTML Report Format

## Document Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{Project} Quality Report</title>
  <style>/* all styles inline */</style>
</head>
<body>
  <header><!-- project name, date, overall grade --></header>
  <section id="summary"><!-- grade cards --></section>
  <section id="findings"><!-- per-category findings --></section>
</body>
</html>
```

## Rules

- CSS-only — no JavaScript
- All styles in `<style>` block (no external sheets)
- Single self-contained `.html` file
- Print-friendly (`@media print` overrides)

## Section Order

1. **Header** — project name, audit date, overall grade badge
2. **Summary** — grade cards grid (one per category)
3. **Architecture** — findings list
4. **Performance** — findings list
5. **Best Practices** — findings list
6. **Tech Debt** — findings list

## Grade Colors

| Grade | Background | Text |
|-------|-----------|------|
| A | `#22c55e` | `#fff` |
| B | `#3b82f6` | `#fff` |
| C | `#eab308` | `#000` |
| D | `#f97316` | `#fff` |
| F | `#ef4444` | `#fff` |

## Grade Badge CSS

```css
.grade { display: inline-block; width: 48px; height: 48px;
  border-radius: 8px; text-align: center; line-height: 48px;
  font-size: 24px; font-weight: 700; font-family: monospace; }
.grade-a { background: #22c55e; color: #fff; }
.grade-b { background: #3b82f6; color: #fff; }
.grade-c { background: #eab308; color: #000; }
.grade-d { background: #f97316; color: #fff; }
.grade-f { background: #ef4444; color: #fff; }
```

## Finding Format

```html
<div class="finding finding-{severity}">
  <span class="severity">{Critical|High|Medium|Low}</span>
  <span class="location">{file}:{line}</span>
  <p class="description">{issue description}</p>
  <pre><code>{code snippet}</code></pre>
</div>
```

## Collapsible Sections

```html
<details open>
  <summary>Architecture (Grade: B) — 3 findings</summary>
  <!-- findings here -->
</details>
```

- Use `<details>/<summary>` for each category
- First two sections `open` by default
- Summary shows: category name, grade, finding count

## Severity Colors

```css
.finding-critical { border-left: 4px solid #ef4444; }
.finding-high { border-left: 4px solid #f97316; }
.finding-medium { border-left: 4px solid #eab308; }
.finding-low { border-left: 4px solid #6b7280; }
```
