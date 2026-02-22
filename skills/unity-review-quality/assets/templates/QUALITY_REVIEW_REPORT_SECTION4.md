<!-- PART 4/8 of QUALITY_REVIEW_REPORT.md -->
<!-- Split template chunk: keep order and concatenate parts to reconstruct full template. -->

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
