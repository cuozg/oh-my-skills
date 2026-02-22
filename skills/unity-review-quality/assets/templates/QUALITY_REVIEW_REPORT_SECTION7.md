<!-- PART 7/8 of QUALITY_REVIEW_REPORT.md -->
<!-- Split template chunk: keep order and concatenate parts to reconstruct full template. -->

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
