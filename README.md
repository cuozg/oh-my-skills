# Oh My OpenCode - Unity Agent Configuration

Configuration files for AI agents to work effectively with this Unity project.

## Installation

```bash
git clone https://github.com/cuozg/oh-my-unity.git ./.opencode
```
```

## Quick Start

1. **Code Review**: *"Review PR #25141 for performance issues."* (uses `unity-review-code-pr`)
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
│   ├── git/             # Git operations (description, squash)
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

Slash commands provide quick-access workflows, organized by category. Each command loads a specific skill to handle the task.