# Oh My Unity

A comprehensive skill pack and tooling configuration for AI agents working with Unity projects. Clone it into your OpenCode config directory and get 33 specialized skills and 38 slash commands — all tuned for Unity C# development.

## Installation

### 1. Clone

```bash
git clone https://github.com/cuozg/oh-my-unity.git ./.opencode
```

### 2. Install GitHub CLI (`gh`)

Several skills (PR reviews, PR descriptions, git workflows) use the [GitHub CLI](https://cli.github.com/) to interact with GitHub. Install it and authenticate:

**macOS**
```bash
brew install gh
```

Then authenticate:
```bash
gh auth login
```

> For other platforms, see the [official install docs](https://github.com/cli/cli#installation).

## Skills (33)

> **33 skills** across 9 domains. Each skill loads shared refs, follows a strict workflow, and produces a defined output.

---

## 🔷 unity-code

Write Unity C# code — standards, architecture, security, performance.

```
├── unity-code-quick        ⚡ Fast single-file C#
│   ├─ What: MonoBehaviours, SOs, interfaces, data models, boilerplate
│   ├─ Flow: Receive → match conventions → write
│   └─ Out:  Single .cs, Function
│
├── unity-code-deep         🏗️ Complex multi-file C#
│   ├─ What: Cross-system features, refactors
│   ├─ Flow: Understand → Plan → Implement
│   └─ Out:  Multiple .cs files, Functions
│
└── unity-code-editor       🛠️ Editor tooling
    ├─ What: EditorWindows, Inspectors, PropertyDrawers, Gizmos, Handles
    ├─ Flow: Identify need → implement
    └─ Out:  Production Editor scripts under Editor/
```

---

## 🔍 unity-review

Review code, architecture, assets, prefabs, and project quality.

```
├── unity-review-code-local     📝 Local logic review
│   ├─ Focus: Logic correctness, edge cases, state, data flow, concurrency
│   ├─ Flow:  Fetch changes → Read → Investigate → Review → Add comments
│   ├─ Out:   Inline // ── REVIEW comments + background fix tasks
│   └─ Note:  No GitHub. No commit. User reviews the diff.
│
├── unity-review-code-pr        🔗 GitHub PR logic review
│   ├─ Focus: Same as local + Unity lifecycle/serialization risks
│   ├─ Flow:  Fetch PR → Read → Investigate → Review → Build JSON → Submit
│   └─ Out:   Comments pushed to GitHub PR via API
│
├── unity-review-architecture   🏛️ PR architecture review
│   ├─ Focus: DI, events, assemblies, coupling, patterns
│   └─ Out:   Architecture comments pushed to GitHub PR
│
├── unity-review-asset          🎨 PR asset review
│   ├─ Focus: .mat .shader .meta .controller .anim .fbx .asset
│   ├─ Check: Shader issues, texture memory, animation config, import settings
│   └─ Out:   Asset comments pushed to GitHub PR
│
├── unity-review-prefab         🧩 PR prefab/scene review
│   ├─ Focus: Missing scripts, broken variants, raycasts, hierarchy
│   ├─ Mode:  Parallel — one subagent per file
│   └─ Out:   Prefab/scene comments pushed to GitHub PR
│
├── unity-review-general        ✅ PR quality gate
│   ├─ Focus: Security, correctness, testing, performance, docs
│   ├─ Role:  Sole approval authority — APPROVE or REQUEST_CHANGES
│   └─ Out:   Final decision pushed to GitHub PR
│
└── unity-review-quality        📊 Full project audit (read-only)
    ├─ Focus: Architecture, performance, best practices, tech debt
    ├─ Grade: A–F severity scoring, evidence-based
    └─ Out:   Comprehensive HTML report
```

---

## 🔬 unity-investigate

Analyze codebases, understand systems, trace data flows.

```
├── unity-investigate-quick     💬 Quick Q&A
│   ├─ What: How does X work? What calls Y? Trace the flow.
│   ├─ Flow: Parse → Find (lsp, grep, trace) → Reply
│   ├─ Rule: Speed over ceremony — stop when you can answer
│   └─ Out:  Summary + 1-3 detail blocks, tree format
│
└── unity-investigate-deep      📋 Full investigation report
    ├─ What: Architecture diagrams, execution flows, risk tables
    ├─ Flow: Scope → Discover → Analyze → Write → Summarize
    ├─ Rule: Cite file:line for every claim
    └─ Out:  Documents/Investigations/*.md with Mermaid diagrams
```

---

## 🐛 unity-debug

Diagnose, trace, and fix Unity issues.

```
├── unity-debug-quick       🩺 Interactive diagnosis
│   ├─ What: Propose ≥2 solutions → user picks → delegate fix → loop
│   ├─ Flow: Parse → Investigate → Analyze → Propose → User picks → Fix → Loop
│   └─ Out:  Diagnostic tree + interactive choice. Loops until done.
│
├── unity-debug-deep        🔎 Exhaustive analysis (read-only)
│   ├─ What: Multi-angle: lifecycle, threading, state, data flow, edge cases
│   ├─ Flow: 9-step deep investigation → structured document
│   ├─ Rule: ≥3 angles. 2-4 solutions as WHAT/WHERE. Cite file:line. Never modifies code.
│   └─ Out:  Documents/Debug/ANALYSIS_*.md
│
├── unity-debug-fix         🔧 Auto-fix loop
│   ├─ What: Parse error → root cause → minimal fix → verify → loop
│   ├─ Rule: Minimal changes only. Always lsp_diagnostics after.
│   └─ Out:  Fixed code, zero errors, minimal diff
│
└── unity-debug-log         📋 Debug.Log generator (read-only)
    ├─ What: Color-coded, #if UNITY_EDITOR wrapped log snippets
    ├─ Format: [DBG] prefix, <color=X> tags, $"..." interpolation
    └─ Out:   Text output only — never written to project files
```

---

## 📐 unity-plan

Plan Unity features with codebase-aware task breakdowns.

```
├── unity-plan-quick        ⚡ Small tasks (XS/S)
│   ├─ What: Inline assessment + task_create. Effort & feasibility.
│   ├─ Flow: Parse → Investigate → Cost/risk → Report → Create tasks
│   └─ Out:  ▲ header + cost·hours·risk + ┌ Tasks tree
│
├── unity-plan-deep         🏗️ Complex features (M/L)
│   ├─ What: SHORT plan doc + task_create
│   ├─ Flow: Read → Scope → Investigate → Plan → Doc → Tasks → Validate
│   └─ Out:  Documents/Plans/PLAN_*.md + task hierarchy
│
└── unity-plan-detail       📦 Very large features (XL)
    ├─ What: 3 HTML files + per-task .patch files. No auto task_create.
    ├─ Flow: 10-step: Read → Scope → Investigate → Plan → Patches → HTML × 3 → Save
    ├─ Rule: No JavaScript in HTML. User decides when to register tasks.
    └─ Out:  Documents/Plans/{name}/ — overview.html, tasks.html, patch.html + .patch files
```

---

## 📖 unity-document

Generate technical documentation from real code state.

```
├── unity-document-system   📘 System documentation
│   ├─ What: Architecture, data flows, usage guides, extension guides
│   ├─ Rule: Cite file:line. Mandatory Mermaid. Bullets > prose.
│   └─ Out:  Documents/Systems/{Name}.md
│
└── unity-document-tdd      📐 Technical Design Document
    ├─ What: Architecture decisions, implementation strategy, dependency analysis
    ├─ Rule: No TODO/TBD. Investigate actual codebase first.
    └─ Out:  Documents/TDDs/TDD_{Name}.md
```

---

## 🧪 unity-test

Testing automation for Unity projects.

```
├── unity-test-unit         🔬 Unit tests
│   ├─ What: Edit/Play Mode tests, mocking, coverage maximization
│   ├─ Target: 10+ test cases per class, Arrange-Act-Assert
│   └─ Out:   Test scripts with [Test] / [UnityTest] attributes
│
└── unity-test-case         📋 QA test cases
    ├─ What: Happy paths, edge cases, boundary values, negative tests
    └─ Out:  Documents/TestCases/{Name}_TestCases.html
```

---

## 🔀 git

Git workflow automation.

```
├── git-commit              💾 Commit with clean message
│   ├─ Rule: No AI metadata. Imperative mood. Bullet points.
│   └─ Out:  Local commit. Never pushes.
│
├── git-comment             ✏️ Amend last commit message
│   ├─ Rule: Never amend if pushed. Never push.
│   └─ Out:  Amended local commit with bullet points
│
├── git-squash              📦 Squash commits for PR
│   ├─ Flow: Analyze → Group → Plan → User approval → Execute
│   └─ Out:  Squash plan → user approves → executed
│
└── git-description         📝 Generate PR description
    ├─ What: Deep investigate ALL PR changes → structured description
    └─ Out:  Applied to GitHub PR via gh pr edit
```

---

## 🐚 bash

Shell script tooling.

```
├── bash-check              ✅ Validate scripts
│   ├─ Check: bash -n syntax + ShellCheck lint + manual review
│   └─ Out:   Validation report
│
├── bash-optimize           ⚡ Refactor scripts
│   ├─ What: Clarity, performance, maintainability. No behavior change.
│   └─ Out:  Optimized script + report
│
└── bash-install            📥 Install software
    ├─ What: Auto-retry with fallback. Always verify after install.
    └─ Out:  Installation report
```

---

## 📦 Other

```
├── flatbuffers-coder       🗂️ FlatBuffers pipeline
│   ├─ What: .fbs schemas → C# generation → JSON-to-binary
│   └─ Out:  .fbs + generated C# + binary data
│
├── mermaid                 📊 Diagram creation
│   ├─ What: Flowcharts, sequence diagrams, state machines, architecture
│   └─ Out:  ```mermaid code blocks
│
└── unity-standards          📚 Unity development standards
    ├─ What: Code Standards (13), Review (11), Quality (6), Plan (7), Debug (3), Test (5), Other (3)
    └─ Use:  Other skills load specific refs via read_skill_file
```

---

## ⚡ Commands (38)

Slash commands for quick access to skills and workflows.

```
bash/           check · install · optimize
flatbuffers/    coder
git/            comment · commit · description · squash
mermaid/        create
omo/            atlas · prometheus · sisyphus · sisyphus-junior
skill/          deep · quick
unity/code/     deep · editor · quick
unity/debug/    deep · fix · log · quick
unity/document/ system · tdd
unity/investigate/ deep · quick
unity/plan/     deep · detail · quick
unity/review/   architecture · asset · code-pr · general · local · prefab · quality
unity/test/     case · unit
```
