# Unity Agent Configuration

This directory contains configuration files for AI agents (like Google Antigravity) to work effectively with this Unity project.

## ⚙️ Installation

To set up the agent configuration in your Unity project, run the following command from your project root:

```bash
# For Google Antigravity
git clone https://github.com/cuozg/oh-my-unity.git ./.agent

# For other agents (Claude, etc.)
git clone https://github.com/cuozg/oh-my-unity.git ./.claude
```

## 🚀 Quick Start

1. **Conduct a Code Review**: *"Review PR #25141 for performance issues."* (Agent uses `/unity-review-pr`)
2. **Fix Compiler/Runtime Errors**: Execute the `/unity-fix-errors` workflow.
3. **Plan & Implement Features**: Execute the `/unity-plan` workflow (e.g., *"Add a player health bar to the UI"*).

---

## 📁 Directory Structure

```
.agent/ or .claude/
├── README.md           # This file
├── agents/             # Agent definitions (orchestrators, core, specialized)
├── docs/               # Documentation on creating agents and best practices
├── rules/              # Project-wide rules agents must follow
├── skills/             # Specialized capabilities for agents
└── workflows/          # Step-by-step procedures for common tasks
```

---

### 🚀 Implementation Pipeline

This project follows a structured engineering pipeline to move from high-level ideas to verified, code-complete features.

```mermaid
graph TD
    Input([Feature Input]) --> Plan[unity-plan]
    Plan -->|Initial Roadmap| Review[unity-plan-review]
    Review -->|Finalized Task List| Detail[unity-plan-detail]
    Detail -->|Task Skeletons in Documents/Tasks/| Brainstorm[unity-plan-brainstorm]
    Brainstorm -->|Execution-Ready Instructions| Executor[unity-plan-executor]
    Executor -->|Specialized Experts| Done([Feature Complete])

    subgraph "Planning & Review Phase"
    Plan
    Review
    end

    subgraph "Engineering Phase"
    Detail
    Brainstorm
    Executor
    end
```

#### Pipeline Stages:

1.  **`unity-plan`**: Analyzes the input specification to produce a high-level roadmap, epics, and costing estimates.
2.  **`unity-plan-review`**: The strategic audit. High-level decomposition is critiqued and refined through user brainstorming to ensure a complete task list.
3.  **`unity-plan-detail`**: Decomposes epics into individual task skeletons. It generates `.md` files in `Documents/Tasks/` defining the requirements and success criteria for each step.
4.  **`unity-plan-brainstorm`**: The technical deep-dive. It uses `unity-investigate-code` to find exact code locations, brainstorms architectural decisions with the user, and provides specific code changes and test cases.
5.  **`unity-plan-executor`**: The final implementation stage. It reads the refined task instructions and coordinates specialized experts (like `unity-implement-logic` or `flatbuffers-coder`) to apply the changes and verify the "Definition of Done".

---

## 📜 Rules

**Location**: `.claude/rules/`

Rules are **always-on** constraints that the agent must follow during every interaction. They define coding standards, asset conventions, and behavioral expectations.

### Current Rules

| File                            | Description                                                           |
| ------------------------------- | --------------------------------------------------------------------- |
| `agent-behavior.md`           | How the agent should interact: safety, proactivity, tool mastery.     |
| `unity-csharp-conventions.md` | C# naming, architecture (SOLID, ScriptableObjects), and performance.  |
| `unity-asset-rules.md`        | Folder structure, asset naming, and optimization for textures/models. |

### How to Add a Rule

1. Create a new `.md` file in `.claude/rules/`.
2. Add YAML frontmatter:
   ```yaml
   ---
   trigger: always_on
   glob: Human Readable Title
   description: What this rule enforces.
   ---
   ```
3. Write the rule content in Markdown.

---

## 🛠️ Skills

**Location**: `.claude/skills/`

Skills are **specialized capabilities** that extend the agent's expertise. Each skill lives in its own folder and contains a `SKILL.md` file with instructions, plus optional helper scripts.

### Current Skills

#### 🎮 Unity Development
| Skill | Description |
| :--- | :--- |
| `unity-orchestrator` | The master Unity technical lead and orchestrator. |
| `unity-mcp-basics` | Mastery of the `unityMCP` toolset for Unity Editor automation. |
| `unity-editor-tools` | Specialist in custom Editor tools, windows, and automation. |
| `unity-implement-logic` | Specialist in implementing C# logic and architectural patterns. |
| `unity-tech-art` | Bridge between art and code (Shaders, Pipeline Automation). |
| `unity-fix-errors` | Systematic diagnosis and resolution of Unity technical errors. |
| `unity-debug` | Deep investigation of errors with strategic Debug.Log and reports. |
| `unity-optimize-performance` | Identification and resolution of performance bottlenecks. |
| `unity-investigate-code` | Deep-dive analysis of C# logic and execution flow tracing. |
| `unity-test` | Automated testing using the Unity Test Framework (Edit/Play Mode). |
| `unity-mobile-deploy` | Specialist in iOS/Android deployment, interop, and optimization. |
| `unity-web-deploy` | Specialist in WebGL deployment, interop, and browser optimization. |

#### 📋 Project Planning
| Skill | Description |
| :--- | :--- |
| `unity-plan` | Requirement decomposition into structured implementation plans. |
| `unity-plan-review` | Facilitates high-level review, brainstorming, and task finalization. |
| `unity-plan-detail` | Decomposes plans into detailed tasks with code and test cases. |
| `unity-plan-brainstorm` | Deep-dive investigation and refined coding instructions for tasks. |
| `unity-plan-executor` | Executes detailed technical tasks based on .md files in Documents/Tasks/. |
| `unity-review-pr` | Automated GitHub PR reviews with commit-ready suggestions. |
| `unity-write-docs` | Expert in crafting technical documentation for projects and APIs. |
| `unity-write-tdd` | Formal Technical Design Document (TDD) generation. |

#### 📊 Data & Architecture
| Skill | Description |
| :--- | :--- |
| `flatbuffers-coder` | Specialist in FlatBuffers schema and data management. |
| `mermaid` | Specialist in visual diagrams and architectural mapping (Mermaid). |

#### 🐚 Bash Scripting
| Skill | Description |
| :--- | :--- |
| `bash-check` | Validate and check bash shell scripts for correctness and compatibility. |
| `bash-optimize` | Optimize and refactor bash shell scripts for clarity and performance. |
| `bash-install` | Install software/packages with automatic retry and fallback strategies. |

#### 🤖 Agents & Meta
| Skill | Description |
| :--- | :--- |
| `sisyphus` | Autonomous task execution and sub-agent orchestration. |
| `skill-creator` | Meta-skill for creating and improving other project skills. |


### Skill Folder Structure

```
skills/<skill-name>/
├── SKILL.md           # Main instructions with trigger metadata
├── scripts/           # (Optional) Automated execution logic
├── references/        # (Optional) Domain knowledge and patterns
└── assets/            # (Optional) Templates and static resources
```

### How to Create a Skill

The `skill-creator` skill provides a guided workflow for creating new skills. Use it when you want to create or improve a skill.

#### Using the skill-creator Skill

**Trigger the skill** by asking: *"Create a new skill for [your use case]"* or *"Help me build a skill that does [X]"*

The skill guides you through a 6-step process:

1. **Understand** - Gather concrete examples of how the skill will be used
2. **Plan** - Identify what scripts, references, and assets are needed
3. **Initialize** - Run `init_skill.py` to scaffold the skill directory
4. **Edit** - Implement resources and write SKILL.md instructions
5. **Package** - Run `package_skill.py` to validate and bundle the skill
6. **Iterate** - Refine based on real usage

#### Quick Manual Creation

For simple skills, you can create them manually:

1. Create a folder: `.claude/skills/<your-skill-name>/`.
2. Add a `SKILL.md` file with:
   ```yaml
   ---
   name: your-skill-name
   description: Detailed triggers of when to use this skill.
   ---
   # Your Skill Name

   Procedural instructions for the agent...
   ```
3. Add supporting resources in `scripts/`, `references/`, or `assets/`.

#### Helper Scripts

| Script | Usage | Description |
|--------|-------|-------------|
| `init_skill.py` | `.claude/skills/skill-creator/scripts/init_skill.py <skill-name> --path <output-dir>` | Scaffolds a new skill directory with SKILL.md template and example folders |
| `package_skill.py` | `.claude/skills/skill-creator/scripts/package_skill.py <path/to/skill-folder>` | Validates and packages skill into a distributable `.skill` file |

#### Key Principles

- **Concise is key** - Only include what Claude doesn't already know
- **Progressive disclosure** - Keep SKILL.md lean (<500 lines), use `references/` for detailed docs
- **Appropriate freedom** - High freedom for flexible tasks, low freedom for fragile operations
- **No clutter** - Don't create README, CHANGELOG, or other auxiliary docs inside skills

---

## 🔄 Workflows

**Location**: `.claude/workflows/`

Workflows are **step-by-step procedures** for complex, repetitive tasks. They can be invoked with a slash command (e.g., `/fix-errors`).

### Current Workflows

| Command                         | Description                                                                       |
| ------------------------------- | --------------------------------------------------------------------------------- |
| `/unity-fix-errors`           | Diagnose and fix Unity compiler or runtime errors.                                |
| `/unity-documentation`        | Create and maintain technical project documentation.                              |
| `/unity-optimize-performance` | Identify and resolve performance bottlenecks.                                     |
| `/unity-implement-logic`      | Implement or refactor Unity C# logic and gameplay systems.                        |
| `/unity-mobile-deploy`        | Optimize, build, and deploy the project to iOS and Android.                       |
| `/unity-review-pr`            | Conduct a full code review on a GitHub Pull Request.                              |
| `/unity-plan`                 | Investigate requirements and produce a detailed implementation plan with costing. |
| `/unity-investigate-code`     | Deep-dive into complex logic, execution flows, and feature implementations.       |
| `/unity-write-tdd`            | Generate a Technical Design Document (TDD) based on the WWE 2025 template.        |
| `/unity-test`                 | Create and run automated tests using the Unity Test Framework.                    |
| `/unity-web-deploy`           | Optimize, build, and deploy the project to the WebGL platform.                    |

### How to Create a Workflow

1. Create a new `.md` file: `.claude/workflows/<your-workflow>.md`.
2. Add YAML frontmatter with a description:
   ```yaml
   ---
   description: What this workflow does.
   ---
   ```
3. Write numbered steps. Use `// turbo` above a step to auto-run it, or `// turbo-all` anywhere to auto-run all steps.

---

## 🤖 Agents

**Location**: `.claude/agents/`

Agents are specialized AI personas designed for specific roles in game development. They are organized into categories:

- **`orchestrators/`**: High-level coordinators (e.g., `unity-tech-lead`).
- **`core/`**: Cross-cutting concerns (Performance, Build, QA, Code Review).
- **`specialized/`**: Domain experts (Graphics, Networking, Animation).
- **`platforms/`**: Platform-specific agents (Mobile, VR).
- **`universal/`**: Non-Unity roles (Game Design, Audio).

See `.claude/docs/creating-agents.md` for how to create a new agent.

---

For more details, see the files in `.claude/docs/`.
