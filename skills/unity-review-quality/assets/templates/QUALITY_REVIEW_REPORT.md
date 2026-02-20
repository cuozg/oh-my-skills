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
<div class="toc">
  <strong>Table of Contents</strong>
  <ul>
    <li><a href="#executive-summary">1. Executive Summary</a></li>
    <li><a href="#project-overview">2. Project Overview</a></li>
    <li><a href="#architecture-review">3. Architecture Review</a></li>
    <li><a href="#code-quality-review">4. Code Quality Review</a></li>
    <li><a href="#performance-review">5. Performance Review</a></li>
    <li><a href="#unity-best-practices">6. Unity Best Practices Review</a></li>
    <li><a href="#project-health">7. Project Health Review</a></li>
    <li><a href="#security-review">8. Security Review</a></li>
    <li><a href="#testing-coverage">9. Testing Coverage</a></li>
    <li><a href="#whats-done-well">10. What's Done Well</a></li>
    <li><a href="#findings-summary">11. All Findings Summary</a></li>
    <li><a href="#tech-debt-roadmap">12. Technical Debt Roadmap</a></li>
    <li><a href="#recommendations">13. Recommendations</a></li>
  </ul>
</div>

<!-- ============================================================ -->
<!-- 1. EXECUTIVE SUMMARY                                          -->
<!-- ============================================================ -->
<h2 id="executive-summary">1. Executive Summary</h2>

<div style="display: flex; align-items: center; margin: 1.5rem 0;">
  <div class="grade-badge grade-[GRADE_LETTER]">[GRADE_LETTER]</div>
  <div>
    <h3 style="margin: 0;">Overall Grade: [GRADE_LETTER]</h3>
    <p style="margin: 0.25rem 0 0;">[1-2 sentence grade justification referencing grading criteria.]</p>
  </div>
</div>

<div class="stats-grid">
  <div class="stat-card">
    <div class="stat-number severity-critical">[N]</div>
    <div class="stat-label">Critical</div>
  </div>
  <div class="stat-card">
    <div class="stat-number severity-high">[N]</div>
    <div class="stat-label">High</div>
  </div>
  <div class="stat-card">
    <div class="stat-number severity-medium">[N]</div>
    <div class="stat-label">Medium</div>
  </div>
  <div class="stat-card">
    <div class="stat-number severity-low">[N]</div>
    <div class="stat-label">Low</div>
  </div>
  <div class="stat-card">
    <div class="stat-number" style="color: var(--green);">[N]</div>
    <div class="stat-label">Total Findings</div>
  </div>
  <div class="stat-card">
    <div class="stat-number" style="color: var(--green);">[N]</div>
    <div class="stat-label">Commendations</div>
  </div>
</div>

<p>[2-4 paragraph executive summary. Cover: overall project state, major strengths, most critical risks, maturity assessment (prototype / pre-production / production / live). This should be readable by a non-technical stakeholder.]</p>

<!-- ============================================================ -->
<!-- 2. PROJECT OVERVIEW                                           -->
<!-- ============================================================ -->
<h2 id="project-overview">2. Project Overview</h2>

<h3>2.1 Project Metrics</h3>
<table>
  <tr><th>Metric</th><th>Value</th></tr>
  <tr><td>Total C# Scripts</td><td>[N]</td></tr>
  <tr><td>Total Lines of Code (C#)</td><td>[N]</td></tr>
  <tr><td>Scenes</td><td>[N]</td></tr>
  <tr><td>Prefabs</td><td>[N]</td></tr>
  <tr><td>Assembly Definitions</td><td>[N]</td></tr>
  <tr><td>Shaders / Shader Graphs</td><td>[N] / [N]</td></tr>
  <tr><td>ScriptableObjects</td><td>[N]</td></tr>
  <tr><td>Third-Party Packages</td><td>[N]</td></tr>
  <tr><td>TODO / FIXME / HACK Count</td><td>[N] / [N] / [N]</td></tr>
  <tr><td>Empty Update() Methods</td><td>[N]</td></tr>
  <tr><td>Singleton Count</td><td>[N]</td></tr>
</table>

<h3>2.2 Project Structure</h3>
<pre><code>[Project folder tree — top 2-3 levels under Assets/. Highlight organizational patterns (feature-based, type-based, hybrid).]</code></pre>

<h3>2.3 Package Dependencies</h3>
<table>
  <tr><th>Package</th><th>Version</th><th>Notes</th></tr>
  <!-- Repeat for each significant package -->
  <tr><td><code>[package.name]</code></td><td>[version]</td><td>[Any concern: outdated, deprecated, known issues]</td></tr>
</table>

<!-- ============================================================ -->
<!-- 3. ARCHITECTURE REVIEW                                        -->
<!-- ============================================================ -->
<h2 id="architecture-review">3. Architecture Review</h2>

<h3>3.1 High-Level Architecture</h3>
<p>[Describe the overall architectural pattern: MVC, ECS, Manager-based, event-driven, etc. Assess whether it's intentional or emergent.]</p>

<h3>3.2 Dependency & Coupling Analysis</h3>
<table>
  <tr><th>Pattern</th><th>Count</th><th>Assessment</th></tr>
  <tr><td>Singletons</td><td>[N]</td><td>[Healthy / Overused / Anti-pattern]</td></tr>
  <tr><td>Static Access</td><td>[N]</td><td>[Assessment]</td></tr>
  <tr><td>Interface Usage</td><td>[N]</td><td>[Assessment]</td></tr>
  <tr><td>Event-driven Communication</td><td>[N]</td><td>[Assessment]</td></tr>
  <tr><td>Service Locator / DI</td><td>[N]</td><td>[Assessment]</td></tr>
</table>

<h3>3.3 Assembly Definitions</h3>
<p>[Map assembly structure. Identify circular references, missing references, overly broad assemblies, or lack of assembly definitions entirely.]</p>

<h3>3.4 SOLID Principles Assessment</h3>
<table>
  <tr><th>Principle</th><th>Rating</th><th>Evidence</th></tr>
  <tr><td>Single Responsibility</td><td>[Good / Fair / Poor]</td><td>[Key examples]</td></tr>
  <tr><td>Open/Closed</td><td>[Good / Fair / Poor]</td><td>[Key examples]</td></tr>
  <tr><td>Liskov Substitution</td><td>[Good / Fair / Poor]</td><td>[Key examples]</td></tr>
  <tr><td>Interface Segregation</td><td>[Good / Fair / Poor]</td><td>[Key examples]</td></tr>
  <tr><td>Dependency Inversion</td><td>[Good / Fair / Poor]</td><td>[Key examples]</td></tr>
</table>

<h3>3.5 Architecture Findings</h3>
<!-- Repeat finding-card for each finding in this category -->
<div class="finding-card [critical|high|medium|low]">
  <strong><span class="severity-[critical|high|medium|low]">[SEVERITY]</span></strong> — [Finding Title]
  <br><code>[File.cs:LineNumber]</code>
  <br><strong>Issue</strong>: [What's wrong and why it matters]
  <br><strong>Impact</strong>: [Real-world consequence]
  <br><strong>Fix</strong>: [Concrete actionable fix]
</div>

<!-- ============================================================ -->
<!-- 4. CODE QUALITY REVIEW                                        -->
<!-- ============================================================ -->
<h2 id="code-quality-review">4. Code Quality Review</h2>

<h3>4.1 Code Metrics</h3>
<table>
  <tr><th>Metric</th><th>Value</th><th>Assessment</th></tr>
  <tr><td>Largest Files (top 5)</td><td>[File.cs: N lines, ...]</td><td>[God class risk?]</td></tr>
  <tr><td>Average Method Length</td><td>[N lines]</td><td>[Acceptable / Too long]</td></tr>
  <tr><td>Max Nesting Depth</td><td>[N]</td><td>[Acceptable / Excessive]</td></tr>
  <tr><td>Magic Numbers Found</td><td>[N]</td><td>[Assessment]</td></tr>
  <tr><td>Empty Catch Blocks</td><td>[N]</td><td>[Assessment]</td></tr>
</table>

<h3>4.2 Naming Conventions</h3>
<p>[Assess consistency: PascalCase for classes/methods, camelCase for locals, _camelCase for private fields. Note violations and whether project follows a clear standard.]</p>

<h3>4.3 Error Handling</h3>
<p>[Assess try/catch patterns, null checking, guard clauses, error propagation. Note any swallowed exceptions or missing null checks on critical paths.]</p>

<h3>4.4 Documentation</h3>
<p>[Assess XML doc comments, inline comments quality, README presence, code self-documentation.]</p>

<h3>4.5 Code Quality Findings</h3>
<!-- Repeat finding-card for each finding -->
<div class="finding-card [critical|high|medium|low]">
  <strong><span class="severity-[critical|high|medium|low]">[SEVERITY]</span></strong> — [Finding Title]
  <br><code>[File.cs:LineNumber]</code>
  <br><strong>Issue</strong>: [What's wrong]
  <br><strong>Impact</strong>: [Consequence]
  <br><strong>Fix</strong>: [Actionable fix]
</div>

<!-- ============================================================ -->
<!-- 5. PERFORMANCE REVIEW                                         -->
<!-- ============================================================ -->
<h2 id="performance-review">5. Performance Review</h2>

<h3>5.1 CPU Hot Paths</h3>
<p>[Assess Update/FixedUpdate/LateUpdate methods. List per-frame allocations, expensive operations (GetComponent, Find, LINQ in hot paths), string concatenation.]</p>

<h3>5.2 Memory & GC</h3>
<p>[Assess allocation patterns, event subscription leaks, unmanaged resource disposal, static collection growth, object pooling usage.]</p>

<h3>5.3 GPU & Rendering</h3>
<p>[Assess draw call patterns, batching effectiveness, shader complexity, overdraw risks, texture memory, LOD usage.]</p>

<h3>5.4 Asset Optimization</h3>
<table>
  <tr><th>Asset Type</th><th>Count</th><th>Issues Found</th></tr>
  <tr><td>Textures</td><td>[N]</td><td>[Oversized, wrong compression, read/write enabled, etc.]</td></tr>
  <tr><td>Audio</td><td>[N]</td><td>[Wrong load type, uncompressed, etc.]</td></tr>
  <tr><td>Meshes</td><td>[N]</td><td>[Read/write enabled, high poly without LOD, etc.]</td></tr>
  <tr><td>Animations</td><td>[N]</td><td>[Unoptimized curves, redundant keyframes, etc.]</td></tr>
</table>

<h3>5.5 Loading & Streaming</h3>
<p>[Assess scene loading strategy (sync vs async), Addressables usage, asset bundle management, loading screen implementation.]</p>

<h3>5.6 Performance Findings</h3>
<!-- Repeat finding-card for each finding -->
<div class="finding-card [critical|high|medium|low]">
  <strong><span class="severity-[critical|high|medium|low]">[SEVERITY]</span></strong> — [Finding Title]
  <br><code>[File.cs:LineNumber]</code>
  <br><strong>Issue</strong>: [What's wrong]
  <br><strong>Impact</strong>: [Estimated cost: CPU ms, memory MB, GC KB/frame]
  <br><strong>Fix</strong>: [Actionable fix]
</div>

<!-- ============================================================ -->
<!-- 6. UNITY BEST PRACTICES REVIEW                                -->
<!-- ============================================================ -->
<h2 id="unity-best-practices">6. Unity Best Practices Review</h2>

<h3>6.1 MonoBehaviour Lifecycle</h3>
<p>[Assess Awake/Start/OnEnable/OnDisable/OnDestroy balance. Check for initialization in wrong lifecycle methods, missing cleanup, coroutine lifecycle management.]</p>

<h3>6.2 Serialization</h3>
<p>[Assess SerializeField usage, FormerlySerializedAs for refactoring safety, runtime SO mutation risks, interface serialization patterns.]</p>

<h3>6.3 Scene & Prefab Management</h3>
<p>[Assess scene organization, prefab nesting, missing script references, Canvas configuration, prefab variant usage.]</p>

<h3>6.4 Input System</h3>
<p>[Assess input handling: legacy vs New Input System, input action organization, platform-specific input handling.]</p>

<h3>6.5 Async & Coroutine Patterns</h3>
<p>[Assess coroutine lifecycle, async/await usage, cancellation token handling, fire-and-forget patterns, UniTask adoption.]</p>

<h3>6.6 Unity Best Practices Findings</h3>
<!-- Repeat finding-card for each finding -->
<div class="finding-card [critical|high|medium|low]">
  <strong><span class="severity-[critical|high|medium|low]">[SEVERITY]</span></strong> — [Finding Title]
  <br><code>[File.cs:LineNumber]</code>
  <br><strong>Issue</strong>: [What's wrong]
  <br><strong>Impact</strong>: [Consequence]
  <br><strong>Fix</strong>: [Actionable fix]
</div>

<!-- ============================================================ -->
<!-- 7. PROJECT HEALTH REVIEW                                      -->
<!-- ============================================================ -->
<h2 id="project-health">7. Project Health Review</h2>

<h3>7.1 Project Settings Audit</h3>
<table>
  <tr><th>Setting</th><th>Current Value</th><th>Recommended</th><th>Status</th></tr>
  <tr><td>Scripting Backend</td><td>[IL2CPP / Mono]</td><td>[Recommendation based on target]</td><td>[OK / Warning]</td></tr>
  <tr><td>API Compatibility</td><td>[.NET Standard 2.1 / .NET Framework]</td><td>[Recommendation]</td><td>[OK / Warning]</td></tr>
  <tr><td>Managed Stripping Level</td><td>[Value]</td><td>[Recommendation]</td><td>[OK / Warning]</td></tr>
  <tr><td>VSync</td><td>[Value]</td><td>[Recommendation]</td><td>[OK / Warning]</td></tr>
  <tr><td>Quality Levels</td><td>[Count]</td><td>[Recommendation]</td><td>[OK / Warning]</td></tr>
  <!-- Add more rows for Physics, Graphics, etc. -->
</table>

<h3>7.2 Version Control</h3>
<p>[Assess .gitignore completeness, .gitattributes for LFS, binary asset handling, branch strategy signals.]</p>

<h3>7.3 Build Configuration</h3>
<p>[Assess scene build list, build target settings, player settings per platform, define symbols.]</p>

<h3>7.4 Editor Configuration</h3>
<p>[Assess .editorconfig presence, code style settings, editor-only vs runtime code separation.]</p>

<h3>7.5 Project Health Findings</h3>
<!-- Repeat finding-card for each finding -->
<div class="finding-card [critical|high|medium|low]">
  <strong><span class="severity-[critical|high|medium|low]">[SEVERITY]</span></strong> — [Finding Title]
  <br><code>[File/Setting]</code>
  <br><strong>Issue</strong>: [What's wrong]
  <br><strong>Impact</strong>: [Consequence]
  <br><strong>Fix</strong>: [Actionable fix]
</div>

<!-- ============================================================ -->
<!-- 8. SECURITY REVIEW                                            -->
<!-- ============================================================ -->
<h2 id="security-review">8. Security Review</h2>

<h3>8.1 Data Security</h3>
<p>[Assess sensitive data handling: API keys in code, PlayerPrefs for sensitive data, encryption usage, secure communication.]</p>

<h3>8.2 Code Security</h3>
<p>[Assess input validation, deserialization safety, debug code in production builds, logging sensitive data.]</p>

<h3>8.3 Security Findings</h3>
<!-- Repeat finding-card or "No issues found." -->
<div class="finding-card [critical|high|medium|low]">
  <strong><span class="severity-[critical|high|medium|low]">[SEVERITY]</span></strong> — [Finding Title]
  <br><code>[File.cs:LineNumber]</code>
  <br><strong>Issue</strong>: [What's wrong]
  <br><strong>Impact</strong>: [Consequence]
  <br><strong>Fix</strong>: [Actionable fix]
</div>

<!-- ============================================================ -->
<!-- 9. TESTING COVERAGE                                           -->
<!-- ============================================================ -->
<h2 id="testing-coverage">9. Testing Coverage</h2>

<h3>9.1 Test Infrastructure</h3>
<table>
  <tr><th>Metric</th><th>Value</th></tr>
  <tr><td>Test Assemblies</td><td>[N]</td></tr>
  <tr><td>Edit Mode Tests</td><td>[N]</td></tr>
  <tr><td>Play Mode Tests</td><td>[N]</td></tr>
  <tr><td>Total Test Methods</td><td>[N]</td></tr>
  <tr><td>Test-to-Code Ratio</td><td>[N:N]</td></tr>
</table>

<h3>9.2 Coverage Assessment</h3>
<p>[Assess which systems have test coverage, which critical paths are untested, test quality (do tests actually assert meaningful behavior?), mocking patterns.]</p>

<h3>9.3 Testing Findings</h3>
<!-- Repeat finding-card or "No issues found." -->
<div class="finding-card [critical|high|medium|low]">
  <strong><span class="severity-[critical|high|medium|low]">[SEVERITY]</span></strong> — [Finding Title]
  <br><code>[File/Path]</code>
  <br><strong>Issue</strong>: [What's wrong]
  <br><strong>Impact</strong>: [Consequence]
  <br><strong>Fix</strong>: [Actionable fix]
</div>

<!-- ============================================================ -->
<!-- 10. WHAT'S DONE WELL                                          -->
<!-- ============================================================ -->
<h2 id="whats-done-well">10. What's Done Well</h2>

<p>[Acknowledge positive patterns. A fair review highlights strengths, not just problems.]</p>

<!-- Repeat well-done card for each commendation -->
<div class="well-done">
  <strong>[Commendation Title]</strong>
  <br>[Description of what's done well and why it matters. Cite specific files/patterns as evidence.]
</div>

<!-- ============================================================ -->
<!-- 11. ALL FINDINGS SUMMARY                                      -->
<!-- ============================================================ -->
<h2 id="findings-summary">11. All Findings Summary</h2>

<p>Total: <strong>[N]</strong> findings — <span class="severity-critical">[N] Critical</span>, <span class="severity-high">[N] High</span>, <span class="severity-medium">[N] Medium</span>, <span class="severity-low">[N] Low</span></p>

<table>
  <tr>
    <th>#</th>
    <th>Severity</th>
    <th>Category</th>
    <th>Finding</th>
    <th>Location</th>
    <th>Fix</th>
  </tr>
  <!-- Repeat for EVERY finding, sorted by severity (Critical first, then High, Medium, Low) -->
  <tr>
    <td>[1]</td>
    <td><span class="severity-[critical|high|medium|low]">[SEVERITY]</span></td>
    <td><span class="tag tag-category">[Architecture|Code Quality|Performance|Unity|Project Health|Security|Testing]</span></td>
    <td>[Finding description]</td>
    <td><code>[File.cs:Line]</code></td>
    <td>[Concise fix]</td>
  </tr>
</table>

<!-- ============================================================ -->
<!-- 12. TECHNICAL DEBT ROADMAP                                    -->
<!-- ============================================================ -->
<h2 id="tech-debt-roadmap">12. Technical Debt Roadmap</h2>

<p>[Organize findings into a prioritized action plan with time horizons.]</p>

<h3>12.1 Immediate (This Sprint / &lt; 1 Week)</h3>
<!-- Items that block shipping or cause crashes/data loss -->
<div class="roadmap-item">
  <span class="priority-label priority-immediate">P0</span> [Task description]
  <br><em>Addresses findings: #[N], #[N]</em>
  <br><em>Estimated effort: [hours/days]</em>
</div>

<h3>12.2 Short-Term (1-2 Sprints / 2-4 Weeks)</h3>
<!-- High-impact improvements -->
<div class="roadmap-item">
  <span class="priority-label priority-short">P1</span> [Task description]
  <br><em>Addresses findings: #[N], #[N]</em>
  <br><em>Estimated effort: [hours/days]</em>
</div>

<h3>12.3 Medium-Term (1-2 Months)</h3>
<!-- Architectural improvements, refactoring -->
<div class="roadmap-item">
  <span class="priority-label priority-medium">P2</span> [Task description]
  <br><em>Addresses findings: #[N], #[N]</em>
  <br><em>Estimated effort: [days/weeks]</em>
</div>

<h3>12.4 Long-Term (Quarterly Planning)</h3>
<!-- Nice-to-have improvements, polish -->
<div class="roadmap-item">
  <span class="priority-label priority-long">P3</span> [Task description]
  <br><em>Addresses findings: #[N], #[N]</em>
  <br><em>Estimated effort: [weeks]</em>
</div>

<!-- ============================================================ -->
<!-- 13. RECOMMENDATIONS                                           -->
<!-- ============================================================ -->
<h2 id="recommendations">13. Recommendations</h2>

<h3>13.1 Quick Wins (High Impact, Low Effort)</h3>
<ol>
  <li>[Recommendation with expected benefit]</li>
</ol>

<h3>13.2 Strategic Improvements (High Impact, Higher Effort)</h3>
<ol>
  <li>[Recommendation with expected benefit]</li>
</ol>

<h3>13.3 Process Improvements</h3>
<ol>
  <li>[Recommendation: CI/CD, code review practices, testing strategy, etc.]</li>
</ol>

<h3>13.4 Tools & Automation</h3>
<ol>
  <li>[Recommended tools, linters, analyzers, or automation to prevent regression]</li>
</ol>

<!-- ============================================================ -->
<!-- FOOTER                                                        -->
<!-- ============================================================ -->
<hr style="border: 1px solid var(--border); margin: 3rem 0 1rem;">
<p style="color: var(--text-muted); font-size: 0.85em; text-align: center;">
  Generated by <strong>unity-review-quality</strong> skill &nbsp;|&nbsp; [YYYY-MM-DD]
  <br>This report is read-only analysis. No project files were modified during this review.
</p>

</div>
</body>
</html>
```

---

## Template Usage Instructions

1. **Replace ALL `[PLACEHOLDERS]`** with actual data from your investigation
2. **Severity classes**: Use `critical`, `high`, `medium`, `low` for CSS classes
3. **Grade badge**: Replace `grade-[GRADE_LETTER]` with `grade-A`, `grade-B`, `grade-C`, `grade-D`, or `grade-F`
4. **Finding cards**: Duplicate the `finding-card` div for each finding in each section
5. **Well-done cards**: Duplicate the `well-done` div for each commendation
6. **Roadmap items**: Duplicate the `roadmap-item` div for each action item
7. **Findings table (Section 11)**: Must list EVERY finding from ALL sections, sorted by severity
8. **No empty sections**: If a section has no findings, write "No issues found." — do NOT delete the section
9. **Evidence required**: Every finding MUST include `File.cs:LineNumber` or `Setting/Path` — no speculative findings
10. **Output path**: Save as `Documents/Reviews/QUALITY_REVIEW_[ProjectName]_[YYYYMMDD].html`
