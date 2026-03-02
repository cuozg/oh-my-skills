# Test Case Format

## HTML Structure

```html
<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<title>Test Cases — {Feature}</title>
<style>
  body { font-family: system-ui; margin: 2rem; background: #1a1a2e; color: #e0e0e0; }
  h1 { color: #00d4ff; border-bottom: 2px solid #00d4ff; padding-bottom: 0.5rem; }
  table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
  th { background: #16213e; color: #00d4ff; padding: 10px; text-align: left; }
  td { padding: 8px 10px; border-bottom: 1px solid #2a2a4a; }
  tr:hover { background: #1f1f3a; }
  .p0 { color: #ff4444; font-weight: bold; }
  .p1 { color: #ff8c00; }
  .p2 { color: #ffd700; }
  .p3 { color: #88cc88; }
  .pass { color: #4caf50; } .fail { color: #f44336; } .skip { color: #999; }
</style>
</head><body>
<h1>Test Cases — {Feature}</h1>
<table>
<tr><th>ID</th><th>Category</th><th>Steps</th><th>Expected</th><th>Priority</th><th>Status</th></tr>
<!-- rows here -->
</table>
</body></html>
```

## Priority Levels

| Level | Class | Use |
|-------|-------|-----|
| P0 | `p0` | Critical — blocks release |
| P1 | `p1` | High — core functionality |
| P2 | `p2` | Medium — secondary flows |
| P3 | `p3` | Nice-to-have — polish |

## Categories

| Category | Description |
|----------|-------------|
| Happy Path | Normal expected usage |
| Edge Case | Boundary values, limits |
| Error | Invalid input, failure modes |
| Performance | Load, stress, timing |
| Regression | Previously fixed bugs |

## Row Example

```html
<tr>
  <td>TC-001</td>
  <td>Happy Path</td>
  <td>1. Open inventory<br>2. Click item<br>3. Click "Use"</td>
  <td>Item consumed, effect applied, count decremented</td>
  <td><span class="p0">P0</span></td>
  <td><span class="pass">PASS</span></td>
</tr>
```

## ID Convention

Format: `TC-{NNN}` — sequential per feature. Group by category in table order:
1. Happy Path (TC-001–099)
2. Edge Case (TC-100–199)
3. Error (TC-200–299)
4. Performance (TC-300–399)
