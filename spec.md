# unity-code
Write Unity C# code following coding standards, architecture, security, and performance best practices.

## unity-code-quick
Fast single-file C# generation. MonoBehaviours, ScriptableObjects, interfaces, data models, boilerplate. No testing — focus on speed.

### standard
Load relevant unity-shared refs. Match existing codebase conventions (naming, namespaces, patterns).

### workflow
Receive task → match conventions → write C# → verify with lsp_diagnostics.

### output-template
Single `.cs` file, zero compile errors.

## unity-code-deep
Complex multi-file C# implementation. Loads all shared references, follows TDD strictly, investigates before coding, runs tests after writing.

### standard
Load ALL 13 unity-shared code refs. Investigate before writing. Verify references to preserve existing logic.

### workflow
4-phase: Understand (read refs + codebase) → Plan (approach) → Implement (write C#) → Verify (lsp_diagnostics + run tests).

### output-template
Multiple `.cs` files, zero compile errors, tests passing.

## unity-code-editor
Unity Editor C# — custom EditorWindows, Inspectors, PropertyDrawers, ScriptableWizards, editor automation, Gizmos, Handles, UI Toolkit and IMGUI.

### standard
Load editor-patterns.md. Use EDITOR_WINDOW or CUSTOM_INSPECTOR templates as base.

### workflow
4-step: Identify editor need → select template (IMGUI vs UI Toolkit) → implement → verify.

### output-template
Production-ready Editor C# scripts under an `Editor/` folder.

# unity-review
Review code changes, logic, architecture, assets, performance, and security.

## unity-review-code-local
Deep logic review on local code. Adds review comments directly into files, delegates fixes to unity-code-quick. No GitHub interaction.

### standard
Load 8 shared review refs. Focus on logic correctness, edge cases, state management, data flow, concurrency.

### workflow
5-step: Fetch changes → Read files → Investigate context → Review logic → Add `// ── REVIEW` comments + delegate fixes.

### output-template
Inline `// ── REVIEW` comments in source files. Fixes delegated to unity-code-quick as background tasks.

## unity-review-code-pr
Review .cs logic in GitHub PRs. Pushes review comments to GitHub via API. Delegates local fixes to unity-code-quick.

### standard
Load 7 shared review refs. Surgical focus on correctness, edge cases, state/data flow, concurrency, Unity lifecycle/serialization risks.

### workflow
6-step: Fetch PR → Read changed files → Investigate context → Review logic → Build JSON comments → Submit via GitHub API.

### output-template
Review comments pushed directly to the GitHub PR.

## unity-review-architecture
Review PR architecture — dependency management, event systems, assembly structure, cross-system coupling.

### standard
Load review-architecture-patterns.md. Check DI, events, assembly boundaries, coupling patterns.

### workflow
6-step: Fetch PR → Load standards → Investigate architecture → Review patterns → Build JSON → Submit via GitHub API.

### output-template
Architecture review comments pushed to the GitHub PR.

## unity-review-asset
Review asset files (.mat, .shader, .meta, .controller, .anim, .fbx, .asset) in PRs for shader, texture, animation, and import issues.

### standard
Load review-asset-patterns.md. Check shader issues, texture memory, animation config, model import settings.

### workflow
4-step: Fetch PR → Read asset files & apply patterns → Build JSON → Submit via GitHub API.

### output-template
Asset review comments pushed to the GitHub PR.

## unity-review-prefab
Review .prefab and .unity files in PRs for missing scripts, broken variants, raycast issues, hierarchy problems.

### standard
Load review-prefab-patterns.md + review-parallel-workflow.md. Parallel subagent per file.

### workflow
4-step: Fetch PR & filter prefab/scene files → Parallel review (one subagent per file) → Collect & merge results → Submit via GitHub API.

### output-template
Prefab/scene review comments pushed to the GitHub PR.

## unity-review-general
Review PRs against general quality checklists — security, correctness, testing, code quality, performance, documentation.

### standard
Load review-approval-criteria.md + review-general-checklists.md. Sole approval authority — makes APPROVE/REQUEST_CHANGES decision.

### workflow
5-step: Collect prior reviews → Fetch PR → Apply checklists → Build JSON → Submit final decision via GitHub API.

### output-template
Final review with APPROVE or REQUEST_CHANGES decision pushed to the GitHub PR.

## unity-review-quality
Full project quality audit. Produces comprehensive HTML report covering architecture, performance, best practices, technical debt. Read-only.

### standard
Load 6 shared quality refs (approval criteria + 5 quality checklists). Evidence-based, severity-driven, grading A–F.

### workflow
7-step quality audit: scope → investigate → analyze architecture → review performance → assess practices → score → generate report.

### output-template
Comprehensive HTML quality report document. Read-only — never modifies project files.

# unity-investigate
Analyze codebases, understand systems, trace data flows.

## unity-investigate-quick
Quick Q&A about how systems work. Short summary + 1-3 detailed explanations. No report document.

### standard
Speed over ceremony. Stop the moment you can answer.

### workflow
3-step: Parse question → Find answer (lsp, grep, trace) → Reply with template.

### output-template
`## {Target} [{type}]` header + summary + 1-3 detail blocks. Vercel-themed tree with `├──`/`└──` connectors, inline code cyan, bold labels.

## unity-investigate-deep
Deep investigation with full markdown report. Architecture diagrams, execution flows, risk tables, improvement recommendations.

### standard
Load investigation-analysis-rules.md. Evidence-based — cite file:line for every claim.

### workflow
5-step: Scope investigation → Discover architecture → Analyze flows → Write report → Summarize findings.

### output-template
Markdown report at `Documents/Investigations/` with Mermaid diagrams, execution flows, risk tables, and recommendations.

# unity-debug
Diagnose, trace, and fix Unity issues.

## unity-debug-quick
Interactive diagnosis — propose solutions, let user pick, delegate fix. Loops until resolved.

### standard
Load debug-fix-loop.md + common-fixes.md. Minimum 2 solutions per issue.

### workflow
7-step: Parse error → Investigate → Analyze → Propose solutions (min 2) → User picks → Delegate fix to unity-code-quick → Loop.

### output-template
Vercel-themed diagnostic tree + interactive choice prompt. Loops until user stops.

## unity-debug-deep
Exhaustive multi-angle analysis. Produces structured document with root cause, solutions, workarounds, verification steps. Never modifies code.

### standard
Read-only. Minimum 3 investigation angles. 2-4 solutions described as WHAT/WHERE (not code). Cite file:line.

### workflow
9-step deep investigation: scope → lifecycle analysis → threading analysis → state analysis → data flow → edge cases → synthesize → write document → summarize.

### output-template
Analysis document at `Documents/Debug/ANALYSIS_{Subject}_{date}.md`. Never modifies code.

## unity-debug-fix
Parse errors/stack traces, investigate root cause, apply minimal fix, verify with diagnostics. Loops until resolved.

### standard
Load common-fixes.md. Minimal changes only. Always verify with lsp_diagnostics after fix.

### workflow
5-step loop: Parse error → Investigate root cause → Apply minimal fix → Verify (lsp_diagnostics) → Loop if more errors.

### output-template
Fixed code with zero compile errors. Minimal diff.

## unity-debug-log
Generate targeted Debug.Log statements wrapped in #if UNITY_EDITOR. Color-coded, structured. Never modifies project code.

### standard
Load debug-log-reference.md. `#if UNITY_EDITOR` wrapping, `[DBG]` prefix, `<color=X>` tags, `$"..."` interpolation.

### workflow
Analyze target code → generate log snippets grouped by file.

### output-template
Debug.Log snippets as text output only — never written to project files.

# unity-plan
Plan Unity features with codebase-aware task breakdowns.

## unity-plan-quick
Quick planning for small tasks. Inline assessment + task_create. Effort estimates and feasibility checks.

### standard
Load task-system.md, investigation-checklist.md, prometheus-pipeline.md. XS/S tasks.

### workflow
5-step: Parse request → Investigate codebase → Assess cost/risk → Report inline → Create parent + child tasks.

### output-template
`▲ {Name}` header + `{cost} · {hours} · {risk} risk` metadata + `┌ Tasks` tree with `├─`/`└─` branches. Each task: subject + description + `→ skill:{name}`.

## unity-plan-deep
Plan complex features. Short markdown plan (request, impact, task list) at Documents/Plans/ + task_create.

### standard
Load costing-and-types.md, task-system.md, prometheus-pipeline.md. M/L tasks. SHORT plans — not verbose.

### workflow
7-step: Read request → Scope → Investigate codebase → Plan tasks → Generate plan doc → Register tasks → Validate.

### output-template
Short markdown plan at `Documents/Plans/PLAN_{Name}.md` with 8-column task tables + per-task `.patch` files. Creates task hierarchy.

## unity-plan-detail
Deep planning for very large features. 3 HTML files (overview, tasks, patch) + per-task .patch files. No task_create — user decides.

### standard
Load task-patch-requirements.md, costing-and-types.md, prometheus-pipeline.md. XL tasks / refactors. No JavaScript in HTML.

### workflow
10-step: Read → Scope → Investigate → Plan → Generate patches → Build overview HTML → Build tasks HTML → Build patch HTML → Save all → Summarize.

### output-template
3 HTML files + per-task `.patch` files + `tasks.json` at `Documents/Plans/{name}/`. Does NOT create tasks automatically.

# unity-document
Generate technical documentation from real code state.

## unity-document-system
System documentation — architecture, data flows, usage guides, extension guides, dependency maps.

### standard
Read-only, evidence-based (cite file:line). Mandatory Mermaid diagrams. Bullets over prose. Step-by-step extension guides.

### workflow
5-step: Scope system → Discover architecture → Analyze data flows → Write document → Summarize.

### output-template
Document at `Documents/Systems/{Name}.md` with architecture diagrams, data flow maps, usage guides, and extension guides.

## unity-document-tdd
Technical Design Document — technical approach, architecture decisions, implementation strategy with dependency analysis.

### standard
Investigate actual codebase first. No TODO/TBD placeholders. Mandatory sections: Technical Design, Architecture, Approach, Risks, Implementation.

### workflow
5-step: Scope → Investigate codebase → Analyze architecture → Write TDD → Summarize.

### output-template
TDD at `Documents/TDDs/TDD_{Name}.md` with 4-section template covering design, architecture, approach, and risks.

# unity-test
Testing automation for Unity projects.

## unity-test-unit
Unity Test Framework — Edit/Play Mode tests, mocking, comprehensive test suites, coverage maximization.

### standard
Load test-patterns.md, test-assembly-setup.md, test-examples.md. Target 10+ test cases per class.

### workflow
3-step: Analyze target class → Investigate dependencies → Generate test suite (Edit or Play Mode).

### output-template
Unity Test Framework C# scripts with `[Test]` / `[UnityTest]` attributes. Organized by Arrange-Act-Assert.

## unity-test-case
QA test case generation. Deep investigate features, produce comprehensive HTML test case documents.

### standard
Load qa-methodology.md, test-case-patterns.md. Cover happy paths, edge cases, boundary values, negative tests.

### workflow
5-step: Investigate feature → Analyze game logic → Design test cases → Generate HTML → Save document.

### output-template
HTML test case document at `Documents/TestCases/{Name}_TestCases.html`.

# unity-shared
Shared references and standards loaded by all Unity skills. Code standards, pipeline configs, review engine, investigation scripts.

### standard
Not activated directly. Provides: Code Standards (13 refs), Review Checklists (11), Quality (6), Planning (7), Debug (3), Testing (5), Other (3).

### workflow
Other skills load specific refs from this skill via `read_skill_file`. Scripts: `investigate_feature.py`, `trace_logic.py`, `trace_unified.py`, `post_review.py`.

### output-template
N/A — shared resource skill, no direct output.

# git
Git workflow automation.

## git-commit
Generate clean commit messages from code changes. No AI metadata.

### standard
No co-author, committer info, or tool attribution. Imperative mood. Bullet points for multiple changes.

### workflow
Stage changes → diff → generate message → commit. No push.

### output-template
Local git commit with structured message. Never pushes to remote.

## git-comment
Amend last commit with a generated message based on diff analysis. Local only.

### standard
No AI metadata. Never amend if already pushed to remote. Never push.

### workflow
5-step: Read latest diff → Investigate changes → Generate message → Amend commit → Verify.

### output-template
Amended local commit message with short bullet points highlighting important changes.

## git-squash
Squash related commits into organized, well-documented commits for PR prep.

### standard
Present squash plan for user approval before executing. Organize by feature/bugfix.

### workflow
Analyze commit history → group related commits → generate squash plan → present for approval → execute.

### output-template
Squash plan document per `output-template.md`, presented for user approval before executing.

## git-description
Generate and apply PR descriptions from PR links via gh pr edit.

### standard
Deep investigate ALL PR changes — logic, architecture impact, behavioral changes. Follow project PR template.

### workflow
Fetch PR → Investigate all commits → Analyze impact → Generate description → Apply via `gh pr edit`.

### output-template
Structured PR description applied to GitHub PR via `gh pr edit`.

# bash
Shell script tooling.

## bash-check
Validate bash scripts for syntax errors, compatibility, and style.

### standard
Check shell version compatibility. Use `bash -n` for syntax and ShellCheck for linting.

### workflow
6-step: Identify script → detect shell version → syntax check (`bash -n`) → ShellCheck → manual review → report.

### output-template
Structured validation report per `CHECK_REPORT.md`.

## bash-optimize
Refactor bash scripts for clarity, performance, and maintainability.

### standard
Load bash-patterns.md. Apply modern syntax and best practices without changing functionality.

### workflow
3-step: Analyze script → apply optimization patterns → generate report.

### output-template
Optimized script + report per `OPTIMIZATION_REPORT.md`.

## bash-install
Install software with automatic retry and fallback strategies.

### standard
Auto-retry with fallback strategies. Always verify installation after completion.

### workflow
7-step: Identify package → detect environment → choose strategy → execute → verify → handle failures → report.

### output-template
Installation report per `INSTALL_REPORT.md`.

# flatbuffers-coder
FlatBuffers for Unity — .fbs schemas, C# generation, JSON-to-binary conversion, pipeline management.

### standard
Load flatbuffers-schema-pattern.md. Follow FBS_TEMPLATE.md for output structure.

### workflow
Design schema → write `.fbs` → generate C# classes → convert JSON to binary → verify pipeline.

### output-template
`.fbs` schema + generated C# + binary data per `FBS_TEMPLATE.md`.

# mermaid
Create Mermaid diagrams — flowcharts, sequence diagrams, state machines, architecture maps.

### standard
Load mermaid-patterns.md. Choose diagram type that best communicates the concept.

### workflow
Analyze subject → choose diagram type → author Mermaid syntax → validate → embed in ```mermaid blocks.

### output-template
Mermaid diagrams in ` ```mermaid ` code blocks per `DIAGRAM_OUTPUT.md`.

# skill-creator
Guide for creating and optimizing skills — templates, references, scripts, best practices.

### standard
SKILL.md < 100 lines. References < 100 lines each. Progressive disclosure — summary first, details in refs.

### workflow
6-step: Understand need → Plan structure → Init scaffold → Edit SKILL.md + refs → Package → Iterate.

### output-template
New or updated skill directory with `SKILL.md`, `references/`, `scripts/`, `assets/`.
