<!-- PART 1/8 of QUALITY_REVIEW_REPORT.md -->
<!-- Split template chunk: keep order and concatenate parts to reconstruct full template. -->

# Quality Review Report Template

> **Instructions**: Copy this template. Fill EVERY section. Do NOT delete sections — mark empty sections with "No issues found." Output as HTML.

---

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Quality Review: [PROJECT_NAME]</title>
<style>
  :root {
    --bg: #1a1a2e; --surface: #16213e; --surface-alt: #0f3460;
    --text: #e0e0e0; --text-muted: #a0a0a0; --accent: #e94560;
    --green: #4ecca3; --yellow: #f0c040; --orange: #e87040; --red: #e94560;
    --border: #2a2a4a; --code-bg: #0d1b2a;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; padding: 2rem; }
  .container { max-width: 1200px; margin: 0 auto; }
  h1 { font-size: 2rem; color: var(--accent); border-bottom: 2px solid var(--accent); padding-bottom: 0.5rem; margin-bottom: 1.5rem; }
  h2 { font-size: 1.5rem; color: var(--green); margin: 2rem 0 1rem; border-bottom: 1px solid var(--border); padding-bottom: 0.3rem; }
  h3 { font-size: 1.2rem; color: var(--text); margin: 1.5rem 0 0.75rem; }
  h4 { font-size: 1rem; color: var(--text-muted); margin: 1rem 0 0.5rem; }
  p, li { color: var(--text); margin-bottom: 0.5rem; }
  code { background: var(--code-bg); padding: 0.15rem 0.4rem; border-radius: 3px; font-size: 0.9em; color: var(--green); }
  pre { background: var(--code-bg); padding: 1rem; border-radius: 6px; overflow-x: auto; margin: 0.75rem 0; border: 1px solid var(--border); }
  pre code { padding: 0; background: none; }
  table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
  th { background: var(--surface-alt); color: var(--green); text-align: left; padding: 0.75rem; border: 1px solid var(--border); font-weight: 600; }
  td { padding: 0.75rem; border: 1px solid var(--border); vertical-align: top; }
  tr:nth-child(even) { background: var(--surface); }
  .grade-badge { display: inline-block; font-size: 3rem; font-weight: 700; width: 80px; height: 80px; line-height: 80px; text-align: center; border-radius: 12px; margin-right: 1.5rem; vertical-align: middle; }
  .grade-A { background: var(--green); color: var(--bg); }
  .grade-B { background: #6ecf7e; color: var(--bg); }
  .grade-C { background: var(--yellow); color: var(--bg); }
  .grade-D { background: var(--orange); color: var(--bg); }
  .grade-F { background: var(--red); color: #fff; }
  .severity-critical { color: var(--red); font-weight: 700; }
  .severity-high { color: var(--orange); font-weight: 600; }
  .severity-medium { color: var(--yellow); }
  .severity-low { color: var(--text-muted); }
  .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin: 1rem 0; }
  .stat-card { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 1rem; text-align: center; }
  .stat-number { font-size: 2rem; font-weight: 700; }
  .stat-label { font-size: 0.85rem; color: var(--text-muted); margin-top: 0.25rem; }
  .finding-card { background: var(--surface); border-left: 4px solid var(--border); border-radius: 0 6px 6px 0; padding: 1rem 1.25rem; margin: 0.75rem 0; }
  .finding-card.critical { border-left-color: var(--red); }
  .finding-card.high { border-left-color: var(--orange); }
  .finding-card.medium { border-left-color: var(--yellow); }
  .finding-card.low { border-left-color: var(--text-muted); }
  .tag { display: inline-block; padding: 0.15rem 0.5rem; border-radius: 3px; font-size: 0.8em; margin-right: 0.3rem; }
  .tag-category { background: var(--surface-alt); color: var(--green); }
  .well-done { background: var(--surface); border-left: 4px solid var(--green); border-radius: 0 6px 6px 0; padding: 1rem 1.25rem; margin: 0.75rem 0; }
  .toc { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 1.5rem; margin: 1.5rem 0; }
  .toc a { color: var(--green); text-decoration: none; }
  .toc a:hover { text-decoration: underline; }
  .toc ul { list-style: none; padding-left: 1.25rem; }
  .toc > ul { padding-left: 0; }
  .meta-info { color: var(--text-muted); font-size: 0.9em; margin-bottom: 2rem; }
  .roadmap-item { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 1rem 1.25rem; margin: 0.75rem 0; }
  .priority-label { font-weight: 600; margin-right: 0.5rem; }
  .priority-immediate { color: var(--red); }
  .priority-short { color: var(--orange); }
  .priority-medium { color: var(--yellow); }
  .priority-long { color: var(--text-muted); }
</style>
</head>
<body>
<div class="container">

<!-- ============================================================ -->
<!-- HEADER                                                        -->
<!-- ============================================================ -->
<h1>Quality Review: [PROJECT_NAME]</h1>
<div class="meta-info">
  <strong>Date</strong>: [YYYY-MM-DD] &nbsp;|&nbsp;
  <strong>Unity Version</strong>: [UNITY_VERSION] &nbsp;|&nbsp;
  <strong>Render Pipeline</strong>: [URP/HDRP/Built-in] &nbsp;|&nbsp;
  <strong>Target Platforms</strong>: [PLATFORMS] &nbsp;|&nbsp;
  <strong>Scripting Backend</strong>: [IL2CPP/Mono]
  <br>
  <strong>Reviewer</strong>: AI Quality Reviewer &nbsp;|&nbsp;
  <strong>Scope</strong>: Full project audit
</div>

<!-- ============================================================ -->
<!-- TABLE OF CONTENTS                                             -->
<!-- ============================================================ -->
