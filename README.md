# Oh My OpenCode - Unity Agent Configuration

Configuration files for AI agents to work effectively with this Unity project.

## Installation

```bash
git clone https://github.com/cuozg/oh-my-unity.git ./.opencode
```
```

## Quick Start

1. **Code Review**: *"Review PR #25141 for performance issues."* (uses `unity-review-pr`)
2. **Fix Errors**: *"Fix the compiler errors in the console."* (uses `unity-fix-errors`)
3. **Plan & Implement**: *"Add a player health bar to the UI."* (uses `unity-plan`)
4. **Investigate**: *"How does the matchmaking system work?"* (uses `unity-investigate`)
5. **Refactor**: *"Simplify the coupling in PlayerManager."* (uses `unity-refactor`)

---

## Directory Structure

```
.opencode/
├── README.md            # This file
├── opencode.json        # Plugin and agent configuration
├── commands/            # Slash commands for common workflows
│   ├── git/             # Git operations (comment, squash)
│   ├── unity/           # Unity workflows (plan, debug, deploy, etc.)
│   ├── omo/             # Orchestrator/meta commands (sisyphus, task, etc.)
│   └── skill/           # Skill management (create)
├── rules/               # Project-wide rules agents must follow
│   ├── agent-behavior.md
│   ├── unity-asset-rules.md
│   └── unity-csharp-conventions.md
├── skills/              # Specialized agent capabilities (flat structure)
│   ├── <skill-name>/
│   │   ├── SKILL.md     # Main instructions with YAML frontmatter
│   │   ├── scripts/     # (Optional) Automated execution logic
│   │   ├── references/  # (Optional) Domain knowledge and patterns
│   │   └── assets/      # (Optional) Templates and static resources
│   └── ...
├── package.json
└── bun.lock
```

## Commands

**Location**: `.opencode/commands/`

Slash commands provide quick-access workflows, organized by category:

### Unity (`commands/unity/`)

| Command | Description |
| :--- | :--- |
| `/unity/plan` | Plan Unity features with structured output |
| `/unity/implement-logic` | Implement C# game logic |
| `/unity/fix-errors` | Diagnose and fix errors |
| `/unity/investigate` | Deep-dive code analysis |
| `/unity/review-pr` | Review pull requests on GitHub |
| `/unity/review-pr-local` | Review changes locally |
| `/unity/test` | Create and run tests |
| `/unity/optimize-performance` | Find and fix performance issues |
| `/unity/documentation` | Generate project documentation |
| `/unity/mobile-deploy` | iOS/Android build and deploy |
| `/unity/web-deploy` | WebGL build and deploy |
| `/unity/write-tdd` | Generate Technical Design Documents |
| `/unity/debug` | Deep investigation and debugging |
| `/unity/log-analyze` | Parse and analyze console logs |
| `/unity/refactor` | Safe code transformation |
| `/unity/singleton-audit` | Audit Singleton usage |

### Git (`commands/git/`)

| Command | Description |
| :--- | :--- |
| `/git/comment` | Generate structured commit comments |
| `/git/squash` | Squash and organize commits |

### Orchestrator (`commands/omo/`)

| Command | Description |
| :--- | :--- |
| `/omo/omo` | Delegation to @sisyphus |
| `/omo/sisyphus` | Full orchestrator with skill/category selection |
| `/omo/delegate-task` | Delegate task to best-fit agent |
| `/omo/task` | Delegation to @sisyphus-junior |
| `/omo/plan` | Planning workflow |
| `/omo/ulw` | Ultrawork loop |
| `/omo/prompt` | Improve user's prompt |
| `/omo/find-skill` | Find the corresponding skill |

### Skill (`commands/skill/`)

| Command | Description |
| :--- | :--- |
| `/skill/create` | Create or update a skill |

## Rules

**Location**: `.opencode/rules/`

Rules define project-wide conventions that all agents must follow:

| Rule | Purpose |
| :--- | :--- |
| `agent-behavior.md` | Agent interaction patterns and constraints |
| `unity-csharp-conventions.md` | C# coding style, naming, and patterns |
| `unity-asset-rules.md` | Asset management, prefab, and scene conventions |

---

## Skills

**Location**: `.opencode/skills/`

Skills are **specialized capabilities** that extend the agent's expertise. Each skill lives in its own folder with a flat structure (`skills/<skill-name>/SKILL.md`) and is discovered automatically by the `opencode-agent-skills` plugin via YAML frontmatter.

---

### Unity Development (29 skills)

#### Core Implementation
| Skill | Description |
| :--- | :--- |
| `unity-code` | Expert Unity Developer — clean, commented, performant C# implementation. |
| `unity-editor-tools` | Custom Editor Windows, Inspectors, and UI Toolkit (UXML/USS) interfaces. |
| `unity-tech-art` | Bridge art and code — shaders (HLSL/Shader Graph), asset pipelines, procedural generation. |
| `unity-ui` | Implement UX designs from HTML documents into Unity UI prefabs with 100% fidelity. |
| `unity-refactor` | Safe code transformation — extract, rename, restructure, decouple, remove anti-patterns. |
| `unity-2d` | 2D game development — sprites, tilemaps, 2D physics, animation, sprite atlas, 2D lighting. |
| `unity-serialization` | Serialization patterns and data persistence — JSON, binary, ScriptableObject, save/load. |
| `unity-event-system` | Event-driven architecture — C# events, UnityEvent, ScriptableObject channels, event bus. |
| `unity-object-pooling` | Object pooling patterns — generic pools, particle/UI/projectile pooling, pool warming. |

#### Debugging & Quality
| Skill | Description |
| :--- | :--- |
| `unity-fix-errors` | Systematic diagnosis and resolution of compiler errors, exceptions, and build failures. |
| `unity-debug` | Deep investigation of errors with root cause analysis and debug reports. |
| `unity-investigate` | Deep-dive analysis of logic flow, data structures, serialization, and system behavior. |
| `unity-optimize-performance` | Identification and resolution of FPS, memory, and load time bottlenecks. |
| `unity-test` | Unity Test Framework automation — Edit/Play Mode tests, mocking, coverage. |
| `unity-test-case` | QA test case generation — comprehensive test documents in HTML format. |
| `unity-singleton-auditor` | Audit Singleton usage — initialization order, circular dependencies, anti-patterns. |
| `unity-log-analyzer` | Parse and analyze Unity console logs — classify, group, prioritize errors. |

#### Code Review
| Skill | Description |
| :--- | :--- |
| `unity-review-pr` | Automated GitHub PR reviews with Unity-specific patterns and best practices. |
| `unity-review-pr-local` | Local PR reviews without GitHub posting — generates review as local markdown. |

#### Planning & Documentation
| Skill | Description |
| :--- | :--- |
| `unity-plan` | High-level planning with multi-file HTML output and unified diff patch generation. |
| `unity-plan-detail` | Generate 100% complete code changes for each task in a plan. |
| `unity-plan-executor` | Execute implementation plans from HTML files with exact accuracy. |
| `unity-write-docs` | Technical documentation — README, architecture, API references, onboarding guides. |
| `unity-write-tdd` | Formal Technical Design Document (TDD) generation. |

#### Deployment & Design
| Skill | Description |
| :--- | :--- |
| `unity-mobile-deploy` | iOS/Android — touch controls, mobile optimization, native features, build pipelines. |
| `unity-web-deploy` | WebGL — build configuration, C#/JS interop, browser optimization, PWA features. |
| `unity-build-pipeline` | Build automation — build scripts, Addressables, asset bundles, CI/CD, build size. |
| `unity-ux-design` | UX screen specifications and production-ready scene/prefab hierarchies for mobile games. |
| `unity-game-designer` | Game design documentation — GDD, core loops, progression, economy, monetization. |

### UI Toolkit (9 skills)

| Skill | Description |
| :--- | :--- |
| `ui-toolkit-master` | Master guide — architecture, UXML/USS/C# anatomy, project structure, fundamentals. |
| `ui-toolkit-architecture` | Component-based architecture — custom controls, MVC/MVP, reusable templates. |
| `ui-toolkit-databinding` | Unity 6 runtime data binding — IDataSource, PropertyPath, type converters, binding modes. |
| `ui-toolkit-theming` | Theme Style Sheets (TSS) and design token architecture — dark/light themes, runtime switching. |
| `ui-toolkit-patterns` | Common UI patterns — tabs, inventory grids, modals, stateful buttons, scroll snapping. |
| `ui-toolkit-responsive` | Responsive design — flexbox layout, safe areas, screen adaptation, breakpoints. |
| `ui-toolkit-mobile` | Mobile optimization — touch input, gestures, safe areas, orientation, virtual keyboard. |
| `ui-toolkit-performance` | Performance optimization — profiling, draw calls, virtualization, memory management. |
| `ui-toolkit-debugging` | Debugging and troubleshooting — UI Toolkit Debugger, Event Debugger, common pitfalls. |

### Utilities (6 skills)

| Skill | Description |
| :--- | :--- |
| `flatbuffers-coder` | FlatBuffers for Unity — schemas, C# generation, JSON-to-binary conversion. |
| `mermaid` | Mermaid diagrams — flowcharts, architecture, state machines, data structures. |
| `skill-creator` | Meta-skill for creating and improving other project skills. |
| `skill-router` | Find the best matching skill(s) for a user request — scan, score, and rank. |
| `prompt-improver` | AI Prompt Engineer — rewrite vague prompts into optimized, actionable prompts. |
| `beads` | Distributed git-backed issue tracking with the bd CLI. |

### Bash Scripting (3 skills)

| Skill | Description |
| :--- | :--- |
| `bash-check` | Validate bash scripts for syntax errors, compatibility, and runtime issues. |
| `bash-optimize` | Optimize bash scripts for clarity, performance, and maintainability. |
| `bash-install` | Install software with automatic retry and fallback strategies. |

### Git Operations (3 skills)

| Skill | Description |
| :--- | :--- |
| `git-commit` | Generate clean, meaningful commit messages from code changes. |
| `git-comment` | Generate structured commit comments from PRs or commit hashes. |
| `git-squash` | Squash related commits into organized, well-documented commits. |

---

**Total: 50 skills** in a flat directory structure.
