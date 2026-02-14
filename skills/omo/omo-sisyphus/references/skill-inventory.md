# Skill Inventory Reference

Complete catalog of all 44 available skills with `load_skills` values, multi-skill loading patterns, and intent-to-skill cross-reference. Load this reference when selecting skills for delegation.

## Table of Contents

- [Complete Skill Inventory](#complete-skill-inventory)
  - [Unity — Core Development (16 skills)](#unity--core-development-16-skills)
  - [Unity — UI & UX (3 skills)](#unity--ui--ux-3-skills)
  - [Unity — Art & Rendering (1 skill)](#unity--art--rendering-1-skill)
  - [Unity — Deployment (2 skills)](#unity--deployment-2-skills)
  - [Unity — Documentation (2 skills)](#unity--documentation-2-skills)
  - [Unity — UI Toolkit Sub-Skills (9 skills)](#unity--ui-toolkit-sub-skills-9-skills)
  - [Git (3 skills)](#git-3-skills)
  - [Bash (3 skills)](#bash-3-skills)
  - [Orchestration & Meta (2 skills)](#orchestration--meta-2-skills)
  - [Other / Utility (3 skills)](#other--utility-3-skills)
- [Multi-Skill Loading](#multi-skill-loading)
- [Intent to Skill Cross-Reference](#intent-to-skill-cross-reference)

---

## Complete Skill Inventory

All 44 available skills organized by category. Every `load_skills` value is the exact string to pass.

### Unity — Core Development (16 skills)

| Skill | `load_skills` value | Purpose | Triggers |
|---|---|---|---|
| Unity Code | `unity/unity-code` | Write clean, performant C# — MonoBehaviours, ScriptableObjects, gameplay features | implement, create, code, build |
| Unity Plan | `unity/unity-plan` | High-level planning with task breakdown, estimates, and patch generation | plan, estimate, breakdown, scope |
| Unity Plan Detail | `unity/unity-plan-detail` | Generate 100% complete code changes per task from a plan | detail tasks, generate code per task |
| Unity Plan Executor | `unity/unity-plan-executor` | Execute implementation plans from HTML files with exact fidelity | execute plan, apply plan |
| Unity Investigate | `unity/unity-investigate` | Deep investigation — trace logic, data flow, serialization, systems | how does X work, trace, explain |
| Unity Fix Errors | `unity/unity-fix-errors` | Diagnose and fix compiler errors, broken Play Mode, build failures | fix errors, compiler error, build fail |
| Unity Debug | `unity/unity-debug` | Root cause analysis of runtime errors with debug reports | debug, stack trace, investigate crash |
| Unity Test | `unity/unity-test` | Edit/Play Mode test automation, mocking, coverage | write tests, test coverage |
| Unity Test Case | `unity/unity-test-case` | QA test case document generation for game features | test cases, QA plan, test document |
| Unity Refactor | `unity/unity-refactor` | Safe code transformation — extract, rename, decouple, clean up | refactor, restructure, clean up |
| Unity Optimize Performance | `unity/unity-optimize-performance` | Fix FPS drops, memory leaks, slow load times | optimize, performance, FPS, memory |
| Unity Singleton Auditor | `unity/unity-singleton-auditor` | Audit Singleton usage — init order risks, circular deps, anti-patterns | audit singletons, singleton health |
| Unity Log Analyzer | `unity/unity-log-analyzer` | Parse console logs — classify errors, group duplicates, suggest fixes | analyze logs, triage errors |
| Unity Orchestrator | `unity/unity-orchestrator` | Master Unity tech lead — routes to specialized skills | general Unity request |
| Unity Review PR | `unity/unity-review-pr` | PR review with Unity-specific patterns, performance, best practices | review PR, check changes |
| Unity Review PR Local | `unity/unity-review-pr-local` | Local PR review as markdown — no GitHub posting | local review, offline review |

### Unity — UI & UX (3 skills)

| Skill | `load_skills` value | Purpose | Triggers |
|---|---|---|---|
| Unity UI | `unity/unity-ui` | Implement UX designs from HTML docs into Unity prefabs with 100% fidelity | implement design, build prefab from HTML |
| Unity UX Design | `unity/unity-ux-design` | Generate UX screen specs and production-ready scene/prefab hierarchies | UX spec, screen design, mobile game UI |
| Unity Editor Tools | `unity/unity-editor-tools` | Custom Editor Windows, Inspectors, asset/scene validation utilities | editor window, inspector, editor tool |

### Unity — Art & Rendering (1 skill)

| Skill | `load_skills` value | Purpose | Triggers |
|---|---|---|---|
| Unity Tech Art | `unity/unity-tech-art` | Shaders (HLSL/Shader Graph), artist tools, asset pipelines, procedural content | shader, art pipeline, rendering |

### Unity — Deployment (2 skills)

| Skill | `load_skills` value | Purpose | Triggers |
|---|---|---|---|
| Unity Mobile Deploy | `unity/unity-mobile-deploy` | iOS/Android — touch controls, mobile optimization, native features, builds | mobile, iOS, Android, touch |
| Unity Web Deploy | `unity/unity-web-deploy` | WebGL — build config, C#/JS interop, browser issues, PWA | WebGL, browser, web build |

### Unity — Documentation (2 skills)

| Skill | `load_skills` value | Purpose | Triggers |
|---|---|---|---|
| Unity Write Docs | `unity/unity-write-docs` | README, architecture docs, API references, onboarding guides | documentation, README, API docs |
| Unity Write TDD | `unity/unity-write-tdd` | Technical Design Documents — architecture decisions, API specs, data schemas | TDD, tech spec, design document |

### Unity — UI Toolkit Sub-Skills (9 skills)

These are **nested sub-skills** under `unity/ui-toolkit/`. Use the full path in `load_skills`.

| Skill | `load_skills` value | Purpose | Triggers |
|---|---|---|---|
| UI Toolkit Master | `unity/ui-toolkit/ui-toolkit-master` | Master guide — architecture, UXML/USS/C# triad, project structure | UI Toolkit, UXML, USS |
| UI Toolkit Architecture | `unity/ui-toolkit/ui-toolkit-architecture` | Component-based architecture — custom controls, MVC/MVP, reusable templates | UI architecture, custom control, UxmlElement |
| UI Toolkit Data Binding | `unity/ui-toolkit/ui-toolkit-databinding` | Unity 6 runtime data binding — IDataSource, [CreateProperty], binding modes | data binding, dataSource, CreateProperty |
| UI Toolkit Debugging | `unity/ui-toolkit/ui-toolkit-debugging` | Debugger tools — UI Toolkit Debugger, Event Debugger, common pitfalls | debug UI, element not showing, event not firing |
| UI Toolkit Mobile | `unity/ui-toolkit/ui-toolkit-mobile` | Mobile optimization — touch handling, safe areas, gestures, virtual keyboard | mobile UI, touch input, safe area |
| UI Toolkit Patterns | `unity/ui-toolkit/ui-toolkit-patterns` | Common patterns — tabs, inventory grids, modals, stateful buttons, scroll snap | tab bar, inventory grid, modal popup |
| UI Toolkit Performance | `unity/ui-toolkit/ui-toolkit-performance` | Performance — profiling, draw calls, element pooling, ListView virtualization | UI performance, draw calls, layout thrashing |
| UI Toolkit Responsive | `unity/ui-toolkit/ui-toolkit-responsive` | Responsive design — flexbox, safe areas, breakpoints, screen adaptation | responsive, flexbox, safe area, adaptive |
| UI Toolkit Theming | `unity/ui-toolkit/ui-toolkit-theming` | Theme Style Sheets (TSS) — design tokens, dark/light themes, runtime switching | theme, TSS, design tokens, dark mode |

### Git (3 skills)

| Skill | `load_skills` value | Purpose | Triggers |
|---|---|---|---|
| Git Commit | `git/git-commit` | Generate clean commit messages, stage and commit — no AI metadata | commit, stage and commit |
| Git Squash | `git/git-squash` | Squash commits into organized history for PR prep or release | squash, consolidate commits |
| Git Comment | `git/git-comment` | Generate structured commit comments from PRs or commit hashes | PR comment, commit documentation |

### Bash (3 skills)

| Skill | `load_skills` value | Purpose | Triggers |
|---|---|---|---|
| Bash Check | `bash/bash-check` | Validate bash scripts for syntax, compatibility, and style | check script, validate bash |
| Bash Optimize | `bash/bash-optimize` | Optimize bash scripts for clarity, performance, and best practices | optimize script, refactor bash |
| Bash Install | `bash/bash-install` | Install software with automatic retry and fallback strategies | install, setup dependencies |

### Orchestration & Meta (2 skills)

| Skill | `load_skills` value | Purpose | Triggers |
|---|---|---|---|
| Omo Sisyphus | `omo/omo-sisyphus` | This skill — orchestrate Sisyphus delegations | delegate to sisyphus |
| Omo Hephaestus | `omo/omo-hephaestus` | Agent spawner — auto-routes prompts to appropriate skills | any task, delegation |

### Other / Utility (3 skills)

| Skill | `load_skills` value | Purpose | Triggers |
|---|---|---|---|
| FlatBuffers Coder | `other/flatbuffers-coder` | FlatBuffers for Unity — .fbs schemas, C# generation, JSON-to-binary | schema, flatbuffers, serialize |
| Mermaid | `other/mermaid` | Create Mermaid diagrams — flowcharts, architecture, state machines | diagram, visualize, flowchart |
| Skill Creator | `other/skill-creator` | Guide for creating or updating skills | create skill, update skill |

---

## Multi-Skill Loading

Some tasks benefit from loading multiple skills. Pass them all in `load_skills`.

| Scenario | `load_skills` |
|---|---|
| Implement UI Toolkit screen with data binding | `["unity/unity-code", "unity/ui-toolkit/ui-toolkit-master", "unity/ui-toolkit/ui-toolkit-databinding"]` |
| Build responsive mobile UI | `["unity/ui-toolkit/ui-toolkit-master", "unity/ui-toolkit/ui-toolkit-responsive", "unity/ui-toolkit/ui-toolkit-mobile"]` |
| Plan feature + write TDD | `["unity/unity-plan", "unity/unity-write-tdd"]` |
| Debug + investigate root cause | `["unity/unity-debug", "unity/unity-investigate"]` |
| Implement + write tests | `["unity/unity-code", "unity/unity-test"]` |
| Build themed UI Toolkit components | `["unity/ui-toolkit/ui-toolkit-master", "unity/ui-toolkit/ui-toolkit-theming", "unity/ui-toolkit/ui-toolkit-architecture"]` |
| Refactor + optimize performance | `["unity/unity-refactor", "unity/unity-optimize-performance"]` |
| Implement UI from UX spec | `["unity/unity-ui", "unity/unity-ux-design"]` |
| Fix errors + commit | `["unity/unity-fix-errors", "git/git-commit"]` |
| Review PR locally + generate comment | `["unity/unity-review-pr-local", "git/git-comment"]` |

---

## Intent to Skill Cross-Reference

Comprehensive mapping from user intent to primary skill, with optional additions.

| User Intent | Primary Skill | Optional Additions |
|---|---|---|
| Write/implement C# code | `unity/unity-code` | `unity/unity-test` |
| Plan/estimate/breakdown | `unity/unity-plan` | `unity/unity-write-tdd` |
| Write tests | `unity/unity-test` | `unity/unity-code` |
| Review PR (GitHub) | `unity/unity-review-pr` | — |
| Review PR (local/offline) | `unity/unity-review-pr-local` | `git/git-comment` |
| Execute task file | `unity/unity-plan-executor` | — |
| Detail task plan | `unity/unity-plan-detail` | — |
| Investigate codebase | `unity/unity-investigate` | — |
| Fix compilation errors | `unity/unity-fix-errors` | `git/git-commit` |
| Debug runtime issues | `unity/unity-debug` | `unity/unity-investigate` |
| FlatBuffers schema | `other/flatbuffers-coder` | — |
| Generate diagram | `other/mermaid` | — |
| Check bash script | `bash/bash-check` | `bash/bash-optimize` |
| Optimize bash script | `bash/bash-optimize` | `bash/bash-check` |
| Install software/deps | `bash/bash-install` | — |
| Create/update skill | `other/skill-creator` | — |
| Shader/art pipeline | `unity/unity-tech-art` | — |
| Editor tools/inspectors | `unity/unity-editor-tools` | — |
| Performance optimization | `unity/unity-optimize-performance` | `unity/unity-refactor` |
| Refactoring | `unity/unity-refactor` | `unity/unity-optimize-performance` |
| Mobile deployment | `unity/unity-mobile-deploy` | — |
| WebGL deployment | `unity/unity-web-deploy` | — |
| Build UI from design | `unity/unity-ui` | `unity/unity-ux-design` |
| Design UX screen | `unity/unity-ux-design` | `unity/unity-ui` |
| Documentation | `unity/unity-write-docs` | — |
| Technical Design Doc | `unity/unity-write-tdd` | `unity/unity-plan` |
| Commit changes | `git/git-commit` | — |
| Squash commits | `git/git-squash` | — |
| Generate commit comment | `git/git-comment` | — |
| Audit singletons | `unity/unity-singleton-auditor` | `unity/unity-refactor` |
| Analyze console logs | `unity/unity-log-analyzer` | `unity/unity-fix-errors` |
| Generate QA test cases | `unity/unity-test-case` | `unity/unity-investigate` |
| Build UI Toolkit screens | `unity/ui-toolkit/ui-toolkit-master` | See UI Toolkit sub-skills |
| Theme/design tokens | `unity/ui-toolkit/ui-toolkit-theming` | `unity/ui-toolkit/ui-toolkit-master` |
| `use skill <name> ...` | `<category>/<name>` | — |
| No specific skill | Justify omission; `load_skills=[]` | — |
