<!-- PART 3/8 of QUALITY_REVIEW_REPORT.md -->
<!-- Split template chunk: keep order and concatenate parts to reconstruct full template. -->

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
