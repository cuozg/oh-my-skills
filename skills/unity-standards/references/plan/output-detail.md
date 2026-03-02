# Detail Plan Output Format

## Deliverables

3 HTML files per plan — CSS-only, no JavaScript.

| File                        | Content                           |
|-----------------------------|-----------------------------------|
| `{feature}-overview.html`   | Summary, impact, risks, timeline  |
| `{feature}-tasks.html`      | Task breakdown with dependencies  |
| `{feature}-patches.html`    | Per-task code patches             |

## File Naming

Kebab-case feature name: `player-health-overview.html`

## Overview HTML Structure

```html
<h1>Feature: {Name}</h1>
<section class="summary">{1-paragraph summary}</section>
<section class="impact">
  <h2>Impact Analysis</h2>
  <table><!-- files affected, risk per file --></table>
</section>
<section class="risks">
  <h2>Risk Assessment</h2>
  <table><!-- risk, likelihood, mitigation --></table>
</section>
<section class="timeline">
  <h2>Timeline</h2>
  <!-- dependency graph as ASCII or description -->
</section>
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

## Patches HTML Structure

```html
<h1>Patches: {Name}</h1>
<details>
  <summary>T1: {subject}</summary>
  <pre><code class="lang-diff">{unified diff}</code></pre>
</details>
```

## CSS Guidelines

- Grade colors: A=#22c55e, B=#3b82f6, C=#eab308, D=#f97316, F=#ef4444
- Use `<details>/<summary>` for collapsible sections
- Monospace font for code/patches
- Print-friendly (no fixed positioning)

## No task_create

Detail plans do NOT auto-create tasks. User reviews HTML first, then approves.
