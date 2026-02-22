<!-- PART 5/8 of QUALITY_REVIEW_REPORT.md -->
<!-- Split template chunk: keep order and concatenate parts to reconstruct full template. -->

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
