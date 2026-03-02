# Detail Plan Output Format

## Deliverables

3 HTML files per plan — CSS-only, no JavaScript.

| File                        | Content                           |
|-----------------------------|-----------------------------------|
| `{feature}-overview.html`   | Summary, impact, risks, timeline  |
| `{feature}-tasks.html`      | Task breakdown with dependencies  |
| `{feature}-patches.html`    | Per-task code patches             |

File naming: kebab-case feature name, e.g. `player-health-overview.html`

## 10-Step Workflow

1. **Read** — Load entry points, build file inventory: `| File | Role | Lines affected |`
2. **Scope** — Define phases (Foundation → Core → Integration → Polish). State out-of-scope.
3. **Investigate** — Trace cross-system calls. Record `file:line` per dependency.
4. **Plan** — Phases → Tasks → Subtasks. Assign size (XS–XL) and risk.
5. **Generate Patches** — Unified diff `.patch` per changed file.
6. **overview.html** — Summary, phases table, risk matrix.
7. **tasks.html** — Task tree with size, risk, skill, description.
8. **patch.html** — One `<section>` per patch, color-coded diffs.
9. **Save** — All files to `Documents/Plans/{Name}/`.
10. **Review** — User reviews HTML before any task_create.

## File Inventory

```
Documents/Plans/{Name}/
├── overview.html
├── tasks.html
├── patch.html
└── {FileName}.patch  (one per changed file)
```

## Overview HTML Structure

```html
<h1>Feature: {Name}</h1>
<section class="summary">{1-paragraph summary}</section>
<section class="impact"><h2>Impact Analysis</h2><table><!-- files, risk --></table></section>
<section class="risks"><h2>Risk Assessment</h2><table><!-- risk, likelihood, mitigation --></table></section>
<section class="timeline"><h2>Timeline</h2><!-- dependency graph --></section>
```

## Tasks HTML Structure

```html
<h1>Tasks: {Name}</h1>
<div class="task" id="task-1">
  <h2>T1: {subject}</h2>
  <p class="meta">Skill: {name} · Size: {XS-XL} · Blocked by: {ids}</p>
  <p class="description">{what + why + how}</p>
  <h3>Acceptance Criteria</h3>
  <ul><li>{criterion}</li></ul>
</div>
```

## Patches HTML — Diff CSS

```css
.add  { background: #e6ffed; color: #24292e; }
.del  { background: #ffeef0; color: #24292e; }
.meta { background: #f1f8ff; color: #586069; font-style: italic; }
pre   { font-family: monospace; font-size: 13px; overflow-x: auto; }
```

```html
<h1>Patches: {Name}</h1>
<details>
  <summary>T1: {subject}</summary>
  <pre><span class="meta">@@ -10,6 +10,12 @@</span>
<span class="del">-    private int health;</span>
<span class="add">+    private int health = 100;</span></pre>
</details>
```

## CSS Guidelines

- Grade colors: A=#22c55e, B=#3b82f6, C=#eab308, D=#f97316, F=#ef4444
- Use `<details>/<summary>` for collapsible sections
- Monospace font for code/patches
- Print-friendly (no fixed positioning)

## No task_create

Detail plans do NOT auto-create tasks. User reviews HTML first, then approves.
