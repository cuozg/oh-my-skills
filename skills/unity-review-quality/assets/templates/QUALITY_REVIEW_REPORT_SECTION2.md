<!-- PART 2/8 of QUALITY_REVIEW_REPORT.md -->
<!-- Split template chunk: keep order and concatenate parts to reconstruct full template. -->

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

