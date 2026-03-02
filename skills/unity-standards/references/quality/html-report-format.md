# HTML Report Format

## File Naming

`Documents/QualityAudit_{YYYY-MM-DD}.html`

## Rules

- CSS-only — no JavaScript, no external sheets
- Single self-contained `.html` file
- Print-friendly (`@media print` overrides)
- Replace all `{X}` placeholders before saving
- Evidence rows sorted by severity: CRITICAL → WARNING → NOTE
- Top 5 fixes ranked by `severity × frequency`
- No images or external CDN resources

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

## Severity Colors

```css
.finding-critical { border-left: 4px solid #ef4444; }
.finding-high { border-left: 4px solid #f97316; }
.finding-medium { border-left: 4px solid #eab308; }
.finding-low { border-left: 4px solid #6b7280; }
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

- Use `<details>/<summary>` for each category
- First two sections `open` by default
- Summary shows: category name, grade, finding count

## Full Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Unity Quality Audit — {Project} — {Date}</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 960px; margin: 2rem auto; }
    .grade-A { color: #16a34a; } .grade-B { color: #65a30d; }
    .grade-C { color: #d97706; } .grade-D { color: #ea580c; } .grade-F { color: #dc2626; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #e5e7eb; padding: 0.5rem 0.75rem; text-align: left; }
    th { background: #f9fafb; }
    .critical { background: #fef2f2; } .warning { background: #fffbeb; }
    code { background: #f3f4f6; padding: 0.1em 0.3em; border-radius: 3px; font-size: 0.9em; }
  </style>
</head>
<body>
  <h1>Unity Quality Audit</h1>
  <p><strong>Project:</strong> {name} | <strong>Date:</strong> {date} | <strong>Files scanned:</strong> {count}</p>
  <h2>Grade Summary</h2>
  <table>
    <tr><th>Category</th><th>Grade</th><th>Key Finding</th></tr>
    <tr><td>Architecture</td><td class="grade-{X}">{X}</td><td>{summary}</td></tr>
    <tr><td>Performance</td><td class="grade-{X}">{X}</td><td>{summary}</td></tr>
    <tr><td>Best Practices</td><td class="grade-{X}">{X}</td><td>{summary}</td></tr>
    <tr><td>Tech Debt</td><td class="grade-{X}">{X}</td><td>{summary}</td></tr>
  </table>
  <h2>Top 5 Priority Fixes</h2>
  <ol>
    <li><strong>[CRITICAL]</strong> {fix description} — <code>{file}:{line}</code></li>
  </ol>
  <h2>Evidence</h2>
  <table>
    <tr><th>Severity</th><th>Category</th><th>Location</th><th>Detail</th></tr>
    <!-- one row per finding, class="critical" or class="warning" -->
  </table>
</body>
</html>
```
