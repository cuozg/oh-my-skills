---
name: omo-sisyphus
description: "Orchestrator that delegates tasks to Sisyphus agent via call_omo_agent(subagent_type='sisyphus'). Generates structured prompts with mandatory skill loading, /handoff context preservation, and Atlas manual review compliance. Use for complex tasks requiring planning, delegation, or multi-step work. Triggers: 'delegate to sisyphus', 'use sisyphus', complex multi-step requests."
---

# Sisyphus Orchestrator

Delegate tasks to Sisyphus via `call_omo_agent(subagent_type="sisyphus")`.

## Purpose

Orchestrate complex, multi-step tasks by generating structured delegation prompts, dispatching them to Sisyphus, and ensuring mandatory skill loading, context preservation, and Atlas review compliance.

## Input

- **Required**: Task description with clear intent
- **Required**: Skill selection — map intent to a skill from the Complete Skill Inventory
- **Optional**: `session_id` for boulder continuation (validate via `session_list()`/`session_info()` first)

## Safety Rules (NON-NEGOTIABLE)

Apply to BOTH the orchestrator AND any delegated subagent:

- `subagent_type` is ALWAYS `"sisyphus"` — no exceptions
- **NEVER** push to git remotes or add AI metadata (`Co-authored-by:`, `Tool-generated-by:`, etc.) to commits
- **NEVER** run destructive git operations (merge, rebase, tag, force-push)
- **NEVER** perform destructive actions (file/asset deletion, scene overwrites) without explicit user confirmation
- Commits: current branch only, short imperative messages, zero AI metadata
- Every delegation prompt MUST include these restrictions in its MUST NOT DO section

Violation = **critical failure**.

---

## Critical: `load_skills` is REQUIRED

**`load_skills` is a REQUIRED parameter** for `call_omo_agent(subagent_type="sisyphus")`. Omitting it causes "Invalid arguments" errors and the subagent will lack domain knowledge.

```python
# CORRECT — always pass load_skills
call_omo_agent(
    subagent_type="sisyphus",
    load_skills=["unity/unity-code"],  # REQUIRED — category/skill-name format
    description="Implement health regen",
    prompt="..."
)

# WRONG — missing load_skills → fails or produces poor results
call_omo_agent(
    subagent_type="sisyphus",
    description="Implement health regen",
    prompt="..."
)
```

### Skill Path Format

Skills use `category/skill-name` format in `load_skills`. Categories: `unity/`, `omo/`, `other/`, `bash/`, `git/`.

```
load_skills=["unity/unity-code"]                           # NOT "unity-code"
load_skills=["other/skill-creator"]                        # NOT "skill-creator"
load_skills=["other/flatbuffers-coder"]                    # NOT "flatbuffers-coder"
load_skills=["git/git-commit"]                             # NOT "git-commit"
load_skills=["unity/ui-toolkit/ui-toolkit-master"]         # NOT "ui-toolkit-master" — nested sub-skill
load_skills=["unity/ui-toolkit/ui-toolkit-databinding"]    # NOT "unity/ui-toolkit-databinding"
```

> **UI Toolkit sub-skills** use a deeper path: `unity/ui-toolkit/{sub-skill-name}`. There are 9 sub-skills under this prefix.

---

## Quick Lookup — Common Tasks

Find the right skill fast. For full descriptions, see the Complete Skill Inventory below.

| I want to... | `load_skills` value |
|---|---|
| Write or implement C# code | `unity/unity-code` |
| Plan a feature with task breakdown | `unity/unity-plan` |
| Fix compiler errors | `unity/unity-fix-errors` |
| Debug runtime issues | `unity/unity-debug` |
| Write unit/play mode tests | `unity/unity-test` |
| Review a PR | `unity/unity-review-pr` |
| Refactor existing code | `unity/unity-refactor` |
| Optimize performance | `unity/unity-optimize-performance` |
| Build UI from a design spec | `unity/unity-ui` |
| Design a UX screen | `unity/unity-ux-design` |
| Build UI Toolkit components | `unity/ui-toolkit/ui-toolkit-master` |
| Create editor tools/inspectors | `unity/unity-editor-tools` |
| Work with shaders/art pipeline | `unity/unity-tech-art` |
| Commit changes | `git/git-commit` |
| Create/update a skill | `other/skill-creator` |
| Generate a Mermaid diagram | `other/mermaid` |
| Work with FlatBuffers | `other/flatbuffers-coder` |

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

## Intent → Skill Cross-Reference

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

---

## Workflow

### 1. Plan Delegation

Before every `call_omo_agent()`, state:

```
Delegating via call_omo_agent():
- subagent_type: "sisyphus"
- Action: [code|plan|test|review|...]
- Skill: [skill-name]
- Expected outcome: [success criteria]
```

### 2. Generate Prompt

Read template at `assets/templates/DELEGATION_PROMPT.md` and fill placeholders. Every prompt MUST:

1. Start with "FIRST: Load Required Skill" pointing to `.opencode/skills/{category}/{skill-name}/SKILL.md`
2. Include atomic task description and concrete expected outcome
3. MUST DO: follow skill, create todos, run diagnostics, `Read` all modified files, comply with `.opencode/rules/`
4. MUST NOT DO: push to remotes, add AI metadata, destructive actions without confirmation
5. Include "Use `/handoff` if context is getting long"

### 3. Delegate

```python
# Sync — need result before next step
call_omo_agent(
    subagent_type="sisyphus",
    load_skills=["unity/unity-code"],  # REQUIRED — match task to skill
    description="Brief task description",
    run_in_background=False,
    prompt="..."
)

# Background — parallel independent tasks
call_omo_agent(
    subagent_type="sisyphus",
    load_skills=["unity/unity-optimize-performance"],  # REQUIRED
    description="Brief task description",
    run_in_background=True,
    prompt="..."
)
# Collect later: background_output(task_id="...")

# Resume previous session (boulder continuation)
call_omo_agent(
    subagent_type="sisyphus",
    load_skills=["unity/unity-code"],  # REQUIRED even on resume
    session_id="ses_abc123",  # Validated session_id
    description="Continue implementation",
    run_in_background=False,
    prompt="..."
)
```

---

## Subagent Selection Guide

Not all tasks require Sisyphus. Choose the right agent:

| Subagent | Use When | Example |
|---|---|---|
| **sisyphus** | Complex implementation, multi-step work, tasks needing a skill | "Implement inventory system from plan" |
| **explore** | Codebase exploration, finding patterns, architecture understanding | "How is matchmaking structured?" |
| **oracle** | Quick factual answers, API lookups, targeted questions | "What's the signature of PlayerManager.Init?" |
| **librarian** | Session history, finding previous work, context retrieval | "What did we do in yesterday's session?" |

### Spawning Examples

**Example 1: Explore first, then implement**
```python
# Understand the system before implementing
explore_result = call_omo_agent(
    subagent_type="explore",
    description="Understand PlayerHealth system",
    run_in_background=False,
    prompt="Trace how player health is managed — find related scripts, data flow, UI bindings."
)

# Then delegate implementation with loaded skill
call_omo_agent(
    subagent_type="sisyphus",
    load_skills=["unity/unity-code"],  # REQUIRED
    description="Add health regeneration feature",
    run_in_background=False,
    prompt="FIRST: Load Required Skill\n..."  # Fill DELEGATION_PROMPT.md template
)
```

**Example 2: Parallel Sisyphus tasks**
```python
# Two independent tasks in parallel
call_omo_agent(
    subagent_type="sisyphus",
    load_skills=["unity/unity-optimize-performance"],  # REQUIRED
    description="Optimize particle system",
    run_in_background=True,
    prompt="..."
)
call_omo_agent(
    subagent_type="sisyphus",
    load_skills=["unity/unity-refactor"],  # REQUIRED
    description="Refactor UI controllers",
    run_in_background=True,
    prompt="..."
)
# Collect: background_output(task_id="...")
```

**Example 3: Multi-skill UI Toolkit delegation**
```python
# Building a themed, responsive UI Toolkit screen with data binding
call_omo_agent(
    subagent_type="sisyphus",
    load_skills=[
        "unity/ui-toolkit/ui-toolkit-master",       # Core UI Toolkit knowledge
        "unity/ui-toolkit/ui-toolkit-databinding",   # Data binding patterns
        "unity/ui-toolkit/ui-toolkit-theming",       # Theme/design tokens
        "unity/ui-toolkit/ui-toolkit-responsive",    # Responsive layout
    ],
    description="Build settings screen with UI Toolkit",
    run_in_background=False,
    prompt="FIRST: Load Required Skills\n..."
)
```

**Example 4: Design-then-implement workflow**
```python
# Step 1: Generate UX spec
call_omo_agent(
    subagent_type="sisyphus",
    load_skills=["unity/unity-ux-design"],  # REQUIRED
    description="Design lobby screen UX spec",
    run_in_background=False,
    prompt="FIRST: Load Required Skill\n..."
)

# Step 2: Implement from spec
call_omo_agent(
    subagent_type="sisyphus",
    load_skills=["unity/unity-ui", "unity/unity-code"],  # Multi-skill
    description="Implement lobby screen from UX spec",
    run_in_background=False,
    prompt="FIRST: Load Required Skill\n..."
)
```

**Example 5: Long task with /handoff**
```python
call_omo_agent(
    subagent_type="sisyphus",
    load_skills=["unity/unity-code"],  # REQUIRED
    description="Implement full lobby screen",
    run_in_background=False,
    prompt="""FIRST: Load Required Skill
    Load: .opencode/skills/unity/unity-code/SKILL.md

    Task: Implement lobby screen with player stats, matchmaking, and chat.

    MUST DO:
    - Use /handoff if context is getting long — preserves full context
      for continuation in a new session. PREFER /handoff over compaction.
    ..."""
)
```

---

## Context Preservation

**For long-running tasks, always use `/handoff`** instead of letting context compact:
- `/handoff` creates a detailed summary preserving full context for the next session
- Include "Use `/handoff` if context is getting long" in every delegation prompt
- To resume: pass the previous `session_id` to `call_omo_agent()` (boulder continuation)
- Always validate `session_id` via `session_list()`/`session_info()` before resuming

---

## Anti-Patterns

| Bad | Good |
|---|---|
| `subagent_type="explore"` for implementation | `subagent_type="sisyphus"` |
| Missing `load_skills` parameter | `load_skills=["category/skill-name"]` — ALWAYS required |
| `load_skills=["unity-code"]` (no category) | `load_skills=["unity/unity-code"]` (category/name) |
| `load_skills=["skill-creator"]` | `load_skills=["other/skill-creator"]` |
| `load_skills=["ui-toolkit-master"]` (missing nested path) | `load_skills=["unity/ui-toolkit/ui-toolkit-master"]` |
| Missing skill load section in prompt | "FIRST: Load Required Skill" at top |
| No git restrictions in MUST NOT DO | Include push/metadata restrictions |
| Prompt generation before loading skill | Load skill first, then generate |
| Subagent skips `Read` on modified files | Require `Read` on all changed files |
| Passing unvalidated `session_id` | Verify via `session_list()` first |

---

## Output

Successful delegation produces:
1. **Delegation log** — subagent_type, action, skill, expected outcome (before each call)
2. **Subagent result** — completed work from Sisyphus
3. **File verification** — all modified files confirmed read (Atlas review compliance)
4. **Clean commits** — if committing: no AI metadata, imperative messages only

---

## Path Reference

- Skills: `.opencode/skills/{category}/{skill-name}/SKILL.md`
- UI Toolkit sub-skills: `.opencode/skills/unity/ui-toolkit/{sub-skill-name}/SKILL.md`
- Rules: `.opencode/rules/{agent-behavior,unity-csharp-conventions,unity-asset-rules}.md`
- Categories: `unity/`, `omo/`, `other/`, `bash/`, `git/`
- Use `skill(name="{category}/{skill-name}")` for automatic path resolution
- Skills live under `.opencode/skills/`, NOT `.claude/skills/`
- **Total skills**: 44 (16 Unity core + 3 UI/UX + 1 art + 2 deploy + 2 docs + 9 UI Toolkit + 3 git + 3 bash + 2 omo + 3 other)
