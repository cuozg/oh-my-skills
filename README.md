# Oh My Unity

A comprehensive skill pack and tooling configuration for AI agents working with Unity projects. Clone it into your OpenCode config directory and get 65+ specialized skills, 12 custom tools, 30 slash commands, and 4 agent personas — all tuned for Unity C# development.

## Installation

```bash
git clone https://github.com/cuozg/oh-my-unity.git ./.opencode
```

## Quick Start

Just ask naturally. Skills are auto-routed based on your request:

| What you say | What fires |
|---|---|
| *"Review PR #123 for performance issues."* | `unity-review-code-pr` |
| *"Fix the compiler errors in the console."* | `unity-fix-errors` |
| *"How does the matchmaking system work?"* | `unity-investigate-quick` |
| *"Deep dive into the inventory architecture."* | `unity-investigate-deep` |
| *"Plan the player health bar feature."* | `unity-document-plan` |
| *"Simplify the coupling in PlayerManager."* | `unity-refactor` |
| *"Write tests for the quest system."* | `unity-test-unit` |
| *"Generate a sprite for an iron sword icon."* | `unity-sprite-gen` |

## What's Included

### Skills (65)

Organized by domain:

**Unity Core (38)** — Implementation, debugging, planning, review, testing, deployment

| Category | Skills |
|---|---|
| Code | `unity-code-deep`, `unity-code-standards`, `unity-fix-errors`, `unity-refactor` |
| Debug | `unity-debug-quick`, `unity-debug-deep`, `unity-debug-fix`, `unity-debug-log` |
| Document | `unity-document-plan`, `unity-document-plan-detail`, `unity-document-plan-quick`, `unity-document-system`, `unity-document-tdd`, `unity-write-tdd`, `unity-write-docs` |
| Investigate | `unity-investigate-quick`, `unity-investigate-deep` |
| Review | `unity-review-code-local`, `unity-review-code-pr`, `unity-review-architecture`, `unity-review-asset`, `unity-review-prefab`, `unity-review-general`, `unity-review-quality` |
| Test | `unity-test-unit`, `unity-test-case` |
| Design | `unity-game-designer`, `unity-ux-design`, `unity-ui` |
| Systems | `unity-event-system`, `unity-serialization`, `unity-object-pooling`, `unity-singleton-auditor` |
| Performance | `unity-optimize-performance`, `unity-build-pipeline` |
| Deploy | `unity-mobile-deploy`, `unity-web-deploy` |
| Art | `unity-tech-art`, `unity-sprite-gen`, `unity-2d` |
| Execute | `unity-plan-executor`, `unity-log-analyzer` |

**UI Toolkit (9)** — Full coverage of Unity's retained-mode UI framework

`ui-toolkit-master` · `ui-toolkit-architecture` · `ui-toolkit-databinding` · `ui-toolkit-debugging` · `ui-toolkit-mobile` · `ui-toolkit-patterns` · `ui-toolkit-performance` · `ui-toolkit-responsive` · `ui-toolkit-theming`

**Git (4)** — Commit messages, squash, PR descriptions, comment amending

`git-commit` · `git-comment` · `git-description` · `git-squash`

**Bash (3)** — Script checking, optimization, installation

`bash-check` · `bash-optimize` · `bash-install`

**Tooling & Meta (11)** — Skill creation, routing, diagrams, data serialization

`skill-creator` · `skill-router` · `prompt-improver` · `mermaid` · `flatbuffers-coder` · `beads`

### Tools (12)

Custom MCP tools for codebase analysis, registered via `.ts`/`.py` pairs:

| Tool | Purpose |
|---|---|
| `blueprint-inspector` | Parse and inspect Unity Blueprint JSON data files |
| `change-summarizer` | Summarize uncommitted git changes with risk assessment |
| `codebase-health` | File counts, largest files, TODO/HACK density, singleton audit |
| `impact-analyzer` | Blast radius analysis for C# classes before modification |
| `prefab-ref-finder` | Find prefab/scene/asset references to a script by GUID |
| `skill-deps` | Dependency graph for skill integrity checking |
| `skill-finder` | Find the best skill match for a task description |
| `skill-scaffold` | Generate new skill directories with domain-aware templates |
| `skill-scaffold-generator` | Extended scaffold with type-aware templates |
| `skill-validator` | Deep structural validation of skill folders |
| `unity-log-analyzer` | Parse Unity console logs, classify errors, suggest fixes |

### Commands (30)

Slash commands grouped by namespace:

| Namespace | Commands |
|---|---|
| `/git` | `comment`, `description`, `review`, `squash` |
| `/omo` | `plan`, `prompt`, `quick`, `ulw` |
| `/skill` | `deep`, `quick` |
| `/unity/debug` | `deep`, `fix`, `log`, `quick` |
| `/unity/document` | `plan`, `plan-detail`, `plan-quick`, `system`, `tdd` |
| `/unity/investigate` | `deep`, `quick` |
| `/unity/review` | `architecture`, `asset`, `code-pr`, `general`, `local`, `prefab`, `quality` |
| `/unity/test` | `case`, `unit` |

### Agents (4)

| Agent | Role |
|---|---|
| `omo` | Primary orchestration agent |
| `sisyphus-raw-proxy` | Raw proxy for Sisyphus orchestrator |
| `unity-code-reviewer` | Specialized C# code review agent |
| `unity-debugger` | Specialized Unity debugging agent |

### Rules (3)

Always-on behavioral guidelines applied to every agent interaction:

- **`agent-behavior`** — Core safety, communication, and interaction patterns
- **`unity-asset-rules`** — Asset handling conventions
- **`unity-csharp-conventions`** — C# coding standards for Unity projects

## Project Structure

```
oh-my-unity/
├── AGENT.md              # Core agent behavior rules (always-on)
├── README.md
├── agents/               # 4 agent persona definitions
├── commands/             # 30 slash commands (git/, omo/, skill/, unity/)
├── rules/                # 3 always-on rule sets
├── skills/               # 65 skill directories
│   └── validate_skill.py # Skill validation script
├── tools/                # 12 custom MCP tools (.ts/.py pairs)
├── Documents/            # Generated investigation reports
└── memory/               # Persistent memory blocks
```

## License

MIT
