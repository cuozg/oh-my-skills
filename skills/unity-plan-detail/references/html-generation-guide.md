# HTML Generation Guide

## Constraint: No JavaScript

All output HTML must work without any JavaScript.
- No `<script>` tags
- No `onclick` handlers
- No event listeners
- Use `<details>`/`<summary>` for collapsible sections (pure HTML)

## Inline CSS Patterns

```html
<!-- Diff line coloring -->
<style>
  .add  { background:#e6ffed; color:#24292e; }
  .del  { background:#ffeef0; color:#24292e; }
  .meta { background:#f1f8ff; color:#586069; font-style:italic; }
  pre   { font-family:monospace; font-size:13px; overflow-x:auto; }
  table { border-collapse:collapse; width:100%; }
  th,td { border:1px solid #d0d7de; padding:6px 12px; text-align:left; }
  th    { background:#f6f8fa; }
</style>
```

## Section Structure (patch.html)

```html
<section>
  <h2>Assets/Scripts/Health/HealthSystem.cs</h2>
  <pre>
<span class="meta">@@ -10,6 +10,12 @@</span>
<span class="del">-    private int health;</span>
<span class="add">+    private int health = 100;</span>
  </pre>
</section>
```

## overview.html Required Sections

1. `<h1>` project title + date
2. Phases table: `Phase | Tasks | Risk | Est.`
3. Risk matrix: `Risk | Severity | Mitigation`

## tasks.html Required Sections

1. Task tree (nested `<ul>`)
2. Per-task: subject, size, risk, skill, description
