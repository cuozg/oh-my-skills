# Oh My OpenCode - Unity Agent Configuration

Configuration files for AI agents to work effectively with this Unity project.

## Installation

```bash
git clone https://github.com/cuozg/oh-my-unity.git ./.opencode
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
├── commands/            # Slash commands for common workflows
├── rules/               # Project-wide rules agents must follow
│   ├── agent-behavior.md
│   ├── unity-asset-rules.md
│   └── unity-csharp-conventions.md
├── skills/              # Specialized agent capabilities
│   ├── bash/            # Bash scripting skills
│   ├── git/             # Git operation skills
│   ├── omo/             # Agent orchestration skills
│   ├── other/           # Cross-domain utility skills
│   └── unity/           # Unity development skills
├── package.json
└── bun.lock
```

## Commands

**Location**: `.opencode/commands/`

Slash commands provide quick-access workflows. Available commands:

| Command | Description |
| :--- | :--- |
| `/unity-plan` | Plan Unity features with structured output |
| `/unity-implement-logic` | Implement C# game logic |
| `/unity-fix-errors` | Diagnose and fix errors |
| `/unity-investigate` | Deep-dive code analysis |
| `/unity-review-pr` | Review pull requests on GitHub |
| `/unity-review-pr-local` | Review changes locally |
| `/unity-test` | Create and run tests |
| `/unity-optimize-performance` | Find and fix performance issues |
| `/unity-documentation` | Generate project documentation |
| `/unity-mobile-deploy` | iOS/Android build and deploy |
| `/unity-web-deploy` | WebGL build and deploy |
| `/unity-write-tdd` | Generate Technical Design Documents |
| `/git-comment` | Generate structured commit comments |
| `/git-squash` | Squash and organize commits |

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

Skills are **specialized capabilities** that extend the agent's expertise. Each skill lives in its own folder and contains a `SKILL.md` file with instructions, plus optional helper scripts and references.

### Skill Folder Structure

```
skills/<category>/<skill-name>/
├── SKILL.md           # Main instructions with trigger metadata
├── scripts/           # (Optional) Automated execution logic
├── references/        # (Optional) Domain knowledge and patterns
└── assets/            # (Optional) Templates and static resources
```

---

### Unity Development (22 skills)

#### Core Implementation
| Skill | Description |
| :--- | :--- |
| `unity/unity-orchestrator` | Master Unity technical lead. Routes to specialized skills and coordinates multi-step implementations. |
| `unity/unity-code` | Expert Unity Developer — clean, commented, performant C# implementation. |
| `unity/unity-editor-tools` | Custom Editor Windows, Inspectors, and UI Toolkit (UXML/USS) interfaces. |
| `unity/unity-tech-art` | Bridge art and code — shaders (HLSL/Shader Graph), asset pipelines, procedural generation. |
| `unity/unity-ui` | Implement UX designs from HTML documents into Unity UI prefabs with 100% fidelity. |
| `unity/unity-refactor` | Safe code transformation — extract, rename, restructure, decouple, remove anti-patterns. |

#### Debugging & Quality
| Skill | Description |
| :--- | :--- |
| `unity/unity-fix-errors` | Systematic diagnosis and resolution of compiler errors, exceptions, and build failures. |
| `unity/unity-debug` | Deep investigation of errors with root cause analysis and debug reports. |
| `unity/unity-investigate` | Deep-dive analysis of logic flow, data structures, serialization, and system behavior. |
| `unity/unity-optimize-performance` | Identification and resolution of FPS, memory, and load time bottlenecks. |
| `unity/unity-test` | Unity Test Framework automation — Edit/Play Mode tests, mocking, coverage. |
| `unity/unity-test-case` | QA test case generation — comprehensive test documents in HTML format. |

#### Code Review
| Skill | Description |
| :--- | :--- |
| `unity/unity-review-pr` | Automated GitHub PR reviews with Unity-specific patterns and best practices. |
| `unity/unity-review-pr-local` | Local PR reviews without GitHub posting — generates review as local markdown. |

#### Planning & Documentation
| Skill | Description |
| :--- | :--- |
| `unity/unity-plan` | High-level planning with multi-file HTML output and unified diff patch generation. |
| `unity/unity-plan-detail` | Generate 100% complete code changes for each task in a plan. |
| `unity/unity-plan-executor` | Execute implementation plans from HTML files with exact accuracy. |
| `unity/unity-write-docs` | Technical documentation — README, architecture, API references, onboarding guides. |
| `unity/unity-write-tdd` | Formal Technical Design Document (TDD) generation. |

#### Deployment
| Skill | Description |
| :--- | :--- |
| `unity/unity-mobile-deploy` | iOS/Android — touch controls, mobile optimization, native features, build pipelines. |
| `unity/unity-web-deploy` | WebGL — build configuration, C#/JS interop, browser optimization, PWA features. |

#### Design
| Skill | Description |
| :--- | :--- |
| `unity/unity-ux-design` | UX design skill (in development). |

---

### Agent Orchestration (2 skills)
| Skill | Description |
| :--- | :--- |
| `omo/omo-hephaestus` | Agent spawner — analyzes prompts, discovers skills, routes to appropriate skill(s). |
| `omo/omo-sisyphus` | Task orchestrator — delegates to Sisyphus agent with structured prompts and context preservation. |

### Data & Utilities (3 skills)
| Skill | Description |
| :--- | :--- |
| `other/flatbuffers-coder` | FlatBuffers for Unity — schemas, C# generation, JSON-to-binary conversion. |
| `other/mermaid` | Mermaid diagrams — flowcharts, architecture, state machines, data structures. |
| `other/skill-creator` | Meta-skill for creating and improving other project skills. |

### Bash Scripting (3 skills)
| Skill | Description |
| :--- | :--- |
| `bash/bash-check` | Validate bash scripts for syntax errors, compatibility, and runtime issues. |
| `bash/bash-optimize` | Optimize bash scripts for clarity, performance, and maintainability. |
| `bash/bash-install` | Install software with automatic retry and fallback strategies. |

### Git Operations (2 skills)
| Skill | Description |
| :--- | :--- |
| `git/git-comment` | Generate structured commit comments from PRs or commit hashes. |
| `git/git-squash` | Squash related commits into organized, well-documented commits. |

---

**Total: 32 skills** across 5 categories.

