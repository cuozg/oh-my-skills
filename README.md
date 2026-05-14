<p align="center">
  <br />
  <img width="100" src="./icon-200.png" alt="Oh My Skills" />
  <br />
</p>

<h1 align="center">Oh My Skills</h1>

<p align="center">
  <strong>52 battle-tested AI agent skills. 363 reference docs. 398 commits of relentless refinement.</strong>
  <br />
  Built for Unity, Phaser, PixiJS, and full-stack development &mdash; evaluated, iterated, and hardened until they actually work.
</p>

<p align="center">
  <a href="#installation">Installation</a>&nbsp;&nbsp;&bull;&nbsp;&nbsp;<a href="#skills-52">Skills</a>&nbsp;&nbsp;&bull;&nbsp;&nbsp;<a href="#commands-56">Commands</a>&nbsp;&nbsp;&bull;&nbsp;&nbsp;<a href="#architecture">Architecture</a>&nbsp;&nbsp;&bull;&nbsp;&nbsp;<a href="#philosophy">Philosophy</a>
</p>

---

## Why This Exists

Most AI agent skills are written once and abandoned. They hallucinate patterns, miss edge cases, and produce output that looks right but isn't.

**Oh My Skills** is different. Every skill in this pack has been:

- **Written** from real-world project experience, not hypotheticals
- **Evaluated** against concrete test scenarios with pass/fail criteria
- **Refined** across 50+ iteration cycles &mdash; rewrite, eval, fix, re-eval
- **Hardened** with 294 reference documents that ground the agent in real conventions

The result: skills that produce **senior-engineer-quality output** &mdash; code that follows your project's actual patterns, reviews that catch real bugs, plans that map to your real codebase.

---

## Installation

### 1. Clone into your config directory

```bash
# For OpenCode
git clone https://github.com/cuozg/oh-my-skills.git ~/.config/opencode/skills

# For Claude Code / Codex
git clone https://github.com/cuozg/oh-my-skills.git ./.claude/skills
```

### 2. Install GitHub CLI (optional, for git skills)

Several skills (PR reviews, PR descriptions, git workflows) use the [GitHub CLI](https://cli.github.com/):

```bash
brew install gh && gh auth login
```

> For other platforms, see the [official install docs](https://github.com/cli/cli#installation).

That's it. Skills auto-activate based on your requests.

---

## The Numbers

| Metric | Count |
|:---|---:|
| Specialized skills | **52** |
| Reference documents | **363** |
| Commits of refinement | **398+** |
| Eval & refinement iterations | **53+** |
| Unity standards reference files | **56** |
| Slash commands | **56** |
| Covered domains | **11** |

---

<a id="philosophy"></a>

## Philosophy: Eval-Driven Skill Development

Skills aren't written &mdash; they're **forged**.

```
 Write v1       Eval against       Identify        Rewrite &       Re-eval
 of skill  -->  real scenarios -->  failures   -->  harden     -->  until pass
     |                                                                  |
     '--- repeat 3-10x per skill until output is indistinguishable ----'
                         from a senior engineer's work
```

### The 3-Tier Progressive Disclosure System

Every skill uses a **token-efficient architecture** that loads only what's needed:

```
Tier 1 ── Metadata          Always in context       ~100 words    name + description
Tier 2 ── SKILL.md          Loaded on trigger        <100 lines   workflow + tool list + rules
Tier 3 ── References        Loaded on demand         Deep docs    standards, checklists, templates
```

**Why this matters:** A naive skill dumps everything into context and wastes tokens. Our 3-tier system means the agent gets surgical precision &mdash; Tier 1 for routing, Tier 2 for workflow, Tier 3 only when the specific reference is needed.

### The Standards Hub Pattern

Instead of duplicating conventions across skills, **shared standards hubs** act as the single source of truth:

```
unity-standards/references/          56 files across 9 categories
├── code-standards/                  Naming, formatting, patterns, architecture
├── review/                          Checklists, PR format, parallel review
├── plan/                            Sizing, risk, task structure, dependencies
├── quality/                         A-F grading, audit templates
├── ui-toolkit/                      UXML, USS, C# bindings, custom controls
├── test/                            Edit/Play mode, coverage, naming
├── debug/                           Diagnosis, common errors, log format
├── optimization/                    Build, rendering, memory, mobile, Jobs/Burst
└── other/                           Mermaid, FlatBuffers, skill authoring
```

Any skill can pull a specific reference on demand:
```python
read_skill_file("unity-standards", "references/code-standards/naming.md")
```

**Rule:** When delegating any Unity task, always include the corresponding standards skill:
```python
task(category="quick", load_skills=["unity-standards", "unity-code"], prompt="...")
```

---

<a id="architecture"></a>

## Architecture

Every domain skill pulls from its standards hub. The hub holds the conventions; the skill holds the workflow.

```mermaid
graph TD
    US[unity-standards<br/>56 reference files] --> UC[unity-code]
    US --> UE[unity-editor]
    US --> URL[unity-review-local]
    US --> URP[unity-review-pr]
    US --> UI[unity-investigate]
    US --> UD[unity-debug]
    US --> UDL[unity-debug-log]
    US --> UDoc[unity-document]
    US --> UProf[unity-profiler]
    US --> UTU[unity-test-unit]
    US --> UTC[unity-test-case]
    US --> UUI[unity-uitoolkit]
    US --> UPI[unity-init]
    US --> USpec[unity-spec]
    US --> UOpt[unity-optimize]
    US --> UWgl[unity-webgl]
    US --> UPro[unity-prototype]
    US --> UCost[unity-costing]
    US --> UAG[unity-asset-generation]
    US --> UA[unity-audio]
    US --> UL[unity-liveops]
    US --> ULoc[unity-localization]
    US --> UM[unity-mobile]
    US --> UPS[unity-project-settings]
    US --> UQA[unity-qa-automation]
    US --> USD[unity-save-data]
    US --> USI[unity-sdk-integration]

    style US fill:#E04E39,color:#fff,stroke:#C03E2B

    style UC fill:#1a1a2e,color:#fff,stroke:#E04E39
    style UE fill:#1a1a2e,color:#fff,stroke:#E04E39
    style URL fill:#1a1a2e,color:#fff,stroke:#E04E39
    style URP fill:#1a1a2e,color:#fff,stroke:#E04E39
    style UI fill:#1a1a2e,color:#fff,stroke:#E04E39
    style UD fill:#1a1a2e,color:#fff,stroke:#E04E39
    style UDL fill:#1a1a2e,color:#fff,stroke:#E04E39
    style UDoc fill:#1a1a2e,color:#fff,stroke:#E04E39
    style UProf fill:#1a1a2e,color:#fff,stroke:#E04E39
    style UTU fill:#1a1a2e,color:#fff,stroke:#E04E39
    style UTC fill:#1a1a2e,color:#fff,stroke:#E04E39
    style UUI fill:#1a1a2e,color:#fff,stroke:#E04E39
    style UPI fill:#1a1a2e,color:#fff,stroke:#E04E39
    style USpec fill:#1a1a2e,color:#fff,stroke:#E04E39
    style UOpt fill:#1a1a2e,color:#fff,stroke:#E04E39
    style UWgl fill:#1a1a2e,color:#fff,stroke:#E04E39
    style UPro fill:#1a1a2e,color:#fff,stroke:#E04E39
    style UCost fill:#1a1a2e,color:#fff,stroke:#E04E39
    style UAG fill:#1a1a2e,color:#fff,stroke:#E04E39
    style UA fill:#1a1a2e,color:#fff,stroke:#E04E39
    style UL fill:#1a1a2e,color:#fff,stroke:#E04E39
    style ULoc fill:#1a1a2e,color:#fff,stroke:#E04E39
    style UM fill:#1a1a2e,color:#fff,stroke:#E04E39
    style UPS fill:#1a1a2e,color:#fff,stroke:#E04E39
    style UQA fill:#1a1a2e,color:#fff,stroke:#E04E39
    style USD fill:#1a1a2e,color:#fff,stroke:#E04E39
    style USI fill:#1a1a2e,color:#fff,stroke:#E04E39
```

---

<a id="skills-52"></a>

## Skills (52)

52 skills across 11 domains. Each skill auto-triages complexity, loads shared references on demand, and produces defined outputs.

### Unity &mdash; Runtime Code

| Skill | What it does | Modes |
|:---|:---|:---|
| **unity-code** | Write, extend, or refactor runtime C# | Quick / Deep / Optimize |
| **unity-optimize** | Performance &mdash; code hot paths, build settings, audits | Code / Settings / Audit |
| **unity-editor** | Custom inspectors, windows, drawers, gizmos, handles | Quick / Deep |
| **unity-uitoolkit** | Runtime UI &mdash; UXML, USS, C# bindings, custom controls | &mdash; |
| **unity-webgl** | JSLib plugins, WebGL builds, templates, deployment | JSLib / Build / Template |
| **unity-prototype** | Playable prototypes from game ideas | &mdash; |
| **unity-save-data** | Design and implement save/load systems, serialization | &mdash; |
| **unity-localization** | Multilingual UI, string tables, localized assets | &mdash; |
| **unity-audio** | SFX, music loops, trimming, normalization | &mdash; |
| **unity-asset-generation** | Sprites, textures, materials, animations | &mdash; |

### Unity &mdash; Quality & Review

| Skill | What it does | Modes |
|:---|:---|:---|
| **unity-review-local** | Code review and project audit for local changes | Local |
| **unity-review-pr** | Comprehensive GitHub PR reviews | PR |
| **unity-debug** | Diagnose and fix bugs, from compile errors to intermittent issues | Fix / Quick / Deep |
| **unity-debug-log** | Formatted Debug.Log snippets for tracing values | &mdash; |
| **unity-investigate** | Codebase analysis, system tracing, architecture reports | Quick / Deep |
| **unity-profiler** | CPU spikes, GC pressure, rendering bottlenecks | &mdash; |
| **unity-test-unit** | Edit/Play mode unit tests (10+ per class, AAA pattern) | &mdash; |
| **unity-test-case** | QA test case documentation (HTML output) | &mdash; |
| **unity-qa-automation** | Smoke checks, scene validation, regression evidence | &mdash; |

### Unity &mdash; Planning & Docs

| Skill | What it does | Modes |
|:---|:---|:---|
| **unity-costing** | XL feature breakdown (10+ days), epic/task trees | &mdash; |
| **unity-document** | Evidence-based Unity system docs in Docs/Systems/ | Single-pass |
| **unity-spec** | Game Design Specification (GDD) | &mdash; |
| **unity-init** | Project scaffolding &mdash; folders, .asmdef, namespaces | &mdash; |
| **unity-standards** | **56 reference files** &mdash; the single source of truth | Hub |
| **unity-project-settings** | Tags, layers, build/quality settings | &mdash; |
| **unity-liveops** | Remote config, analytics, ads, IAP | &mdash; |
| **unity-mobile** | Android/iOS specific validation, permissions, builds | &mdash; |
| **unity-sdk-integration** | SDK package management, boundaries, samples | &mdash; |

### Games &mdash; Phaser & PixiJS

| Skill | What it does |
|:---|:---|
| **phaser-coder** | Write, review, debug, or explain Phaser 3 code |
| **pixijs-coder** | PixiJS v8 &mdash; apps, shaders, filters, animations |

### Full-Stack & Infrastructure

| Skill | What it does |
|:---|:---|
| **nextjs-backend** | API routes, server actions, auth, multi-tenant (App Router) |
| **ui-ux** | UI/UX design intelligence &mdash; 67 styles, 96 palettes, 13 stacks |

### Git Workflow

| Skill | What it does |
|:---|:---|
| **git-commit** | Stage + commit with clean imperative messages |
| **git-comment** | Rewrite last commit message |
| **git-squash** | Squash commits into clean logical units |
| **git-pr** | Generate + apply PR titles and descriptions |
| **git-clear** | Delete all comments from a GitHub PR |

### Autonomous Execution

| Skill | What it does |
|:---|:---|
| **goal-create** | Create structured goals with acceptance criteria |
| **goal-execute** | Execute one goal end-to-end with criterion evidence |
| **goal-verify** | Verify one goal criterion by criterion |
| **goal-loop** | Loop incomplete goals through execute and verify cycles |
| **session-retrospective** | Post-session learning &mdash; improve skills from experience |

### Shell & CLI

| Skill | What it does |
|:---|:---|
| **bash-check** | Validate scripts (syntax + ShellCheck) |
| **bash-optimize** | Refactor scripts without behavior change |
| **bash-install** | Install software with auto-retry + verification |

### Specialized

| Skill | What it does |
|:---|:---|
| **flatbuffers-coder** | .fbs schemas, C# generation, binary serialization |
| **mcp-builder** | Build MCP servers (Python FastMCP / Node SDK) |
| **skill-creator** | Create, modify, benchmark, and optimize skills |

### Productivity & Output

| Skill | What it does |
|:---|:---|
| **visual-explainer** | Self-contained HTML pages for visual explanations |
| **mermaid** | Flowcharts, sequence diagrams, state machines |
| **imagegen** | Generate + edit images via Google Gemini Imagen API |
| **screenshot** | Desktop/system screenshots (macOS, Linux, Windows) |

---

<a id="commands-56"></a>

## Commands (56)

Slash commands for direct access to specific skills.

```
bash/             check   install   optimize
flatbuffers/      coder
git/              clear   comment   commit   pr   squash
goal/             create   execute   loop   verify
image/            gen
mcp/              build
mermaid/          create
nextjs/           backend
openai/           docs
phaser/           coder
pixijs/           coder
plugin/           create
screenshot/       capture
session/          retrospective
skill/            create   install
ui-ux/            design

unity/            init   investigate   liveops   localization   mobile
                  optimize   prototype   qa/automation   standards
                  webgl
unity/asset/      gen
unity/audio/      process
unity/code/       editor   write
unity/debug/      fix   log   profiler
unity/document/   spec   system
unity/plan/       costing
unity/project/    settings
unity/review/     local   pr
unity/save/       data
unity/sdk/        integration
unity/test/       case   unit
unity/ui/         toolkit
visual/           explainer
```

---

## How Skills Are Built

Each skill goes through a rigorous development cycle:

```
1. AUTHOR       Write SKILL.md with workflow, tool whitelist, rules
                Write reference docs grounding the agent in real patterns

2. EVALUATE     Run against real-world test scenarios
                Grade output: correctness, pattern adherence, completeness

3. IDENTIFY     Find failure modes — hallucinated patterns, missed edge cases,
                vague instructions that let the agent drift

4. HARDEN       Rewrite weak sections, add guardrails, tighten constraints
                Add "MUST DO" / "MUST NOT DO" rules for observed failure modes

5. RE-EVALUATE  Run the same scenarios again — verify failures are fixed
                Run NEW scenarios — verify no regressions

6. REPEAT       Until the skill produces output indistinguishable
                from a senior engineer working on the same codebase
```

The `skill-creator` skill automates parts of this process &mdash; it can benchmark skills with variance analysis, run eval suites, and optimize trigger descriptions for routing accuracy.

---

## Contributing

Found a bug in a skill? Have an idea for a new one? PRs welcome.

The bar: every skill must produce output you'd accept in a code review from a senior engineer. If it doesn't, it needs more eval cycles.

---

<p align="center">
  <sub>Built with obsessive iteration by <a href="https://github.com/cuozg">@cuozg</a></sub>
</p>
"center">
  <sub>Built with obsessive iteration by <a href="https://github.com/cuozg">@cuozg</a></sub>
</p>
