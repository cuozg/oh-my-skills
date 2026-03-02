# test-case-template.md

## HTML Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{FeatureName} Test Cases</title>
<style>
  body { font-family: Arial, sans-serif; margin: 2rem; color: #222; }
  h1 { border-bottom: 2px solid #444; padding-bottom: 0.5rem; }
  table { border-collapse: collapse; width: 100%; margin-top: 1rem; }
  th { background: #333; color: #fff; padding: 8px 12px; text-align: left; }
  td { border: 1px solid #ccc; padding: 8px 12px; vertical-align: top; }
  tr:nth-child(even) { background: #f9f9f9; }
  .p1 { color: #c00; font-weight: bold; }
  .p2 { color: #e60; }
  .p3 { color: #666; }
  .pass { color: green; } .fail { color: red; } .skip { color: gray; }
</style>
</head>
<body>
<h1>{FeatureName} — Test Cases</h1>
<p>Generated: {Date} | Total: {N} cases</p>
<table>
<thead>
<tr>
  <th>ID</th><th>Title</th><th>Category</th><th>Preconditions</th>
  <th>Steps</th><th>Expected Result</th><th>Priority</th><th>Status</th>
</tr>
</thead>
<tbody>
<!-- TC-001 -->
<tr>
  <td>TC-001</td>
  <td>{Title}</td>
  <td>Happy Path</td>
  <td>{Preconditions}</td>
  <td><ol><li>{Step 1}</li><li>{Step 2}</li></ol></td>
  <td>{Expected}</td>
  <td class="p1">P1</td>
  <td>—</td>
</tr>
</tbody>
</table>
</body>
</html>
```

## Category Labels
- `Happy Path` — normal successful flow
- `Edge Case` — unusual but valid inputs
- `Boundary` — min/max/zero values
- `Negative` — invalid input, error conditions

## Priority Scale
- `P1` — critical path, must pass before release
- `P2` — important, should pass
- `P3` — nice-to-have coverage
