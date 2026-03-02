# HTML Report Template — Quality Audit

## File Naming

`Documents/QualityAudit_{YYYY-MM-DD}.html`

## Structure

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
  <p><strong>Project:</strong> {name} &nbsp;|&nbsp; <strong>Date:</strong> {date} &nbsp;|&nbsp;
     <strong>Files scanned:</strong> {count}</p>

  <!-- GRADE SUMMARY -->
  <h2>Grade Summary</h2>
  <table>
    <tr><th>Category</th><th>Grade</th><th>Key Finding</th></tr>
    <tr><td>Architecture</td><td class="grade-{X}">{X}</td><td>{one-line summary}</td></tr>
    <tr><td>Performance</td><td class="grade-{X}">{X}</td><td>{one-line summary}</td></tr>
    <tr><td>Best Practices</td><td class="grade-{X}">{X}</td><td>{one-line summary}</td></tr>
    <tr><td>Tech Debt</td><td class="grade-{X}">{X}</td><td>{one-line summary}</td></tr>
  </table>

  <!-- TOP 5 FIXES -->
  <h2>Top 5 Priority Fixes</h2>
  <ol>
    <li><strong>[CRITICAL]</strong> {fix description} — <code>{file}:{line}</code></li>
    <!-- repeat for each fix -->
  </ol>

  <!-- EVIDENCE TABLE -->
  <h2>Evidence</h2>
  <table>
    <tr><th>Severity</th><th>Category</th><th>Location</th><th>Detail</th></tr>
    <!-- one row per finding, class="critical" or class="warning" -->
  </table>
</body>
</html>
```

## Rules

- Replace all `{X}` placeholders with actual grades and values before saving
- Evidence table rows sorted by severity: CRITICAL first, then WARNING, then NOTE
- Top 5 fixes ranked by `severity × frequency` — most impactful first
- Do not embed images or external CDN resources — keep report self-contained
