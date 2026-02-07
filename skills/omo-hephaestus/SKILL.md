---
name: omo-hephaestus
description: "Agent spawner for oh-my-opencode (omo). ALWAYS spawn @hephaestus agent via tool call to handle prompts. Self-routing: analyzes prompts, discovers skills by scanning .claude/skills/*/SKILL.md, routes to appropriate skill(s). Triggers: any task, delegation, multi-skill workflows."
---
# Hephaestus Agent Skill

**ALWAYS spawn exactly the @hephaestus agent from oh-my-opencode (omo) to handle prompts via tool calls.**
**ALWAYS search for skill and use them to handle the task**

## Output Requirement (MANDATORY)

**Every routing decision MUST follow the template**: [ROUTING_REPORT.md](.claude/skills/omo-hephaestus/assets/templates/ROUTING_REPORT.md)

Output the routing report as part of the task execution log. No file save required.

Read the template first, then populate all sections.

```
@hephaestus <prompt>
```

## How Hephaestus Works

1. **Spawn @hephaestus** - ALWAYS invoke via tool call: `@hephaestus <prompt>`
2. **Analyze prompt** - Parse user request and identify intent
3. **Discover skills** - Scan `.claude/skills/*/SKILL.md` frontmatter for available skills
4. **Route to skill** - Match intent to skill(s) using trigger patterns
5. **Load skill** - Load the matching skill's SKILL.md
6. **Execute** - Handle tasks with structured /skill-name `<prompt>`

## Skill Discovery Protocol

Scan the `.claude/skills/` directory and read YAML frontmatter from each `SKILL.md`:

```
.claude/skills/*/SKILL.md → extract name + description → match triggers
```

## Available Skills

| Skill                          | Triggers                                                                          |
| :----------------------------- | :-------------------------------------------------------------------------------- |
| `flatbuffers-coder`          | schema, binary data, serialize, fbs file, flatbuffers                             |
| `mermaid`                    | diagram, visualize, flowchart, sequence diagram, draw the flow                    |
| `skill-creator`              | create skill, update skill, new skill                                             |
| `unity-debug`                | debug this error, why is this happening, investigate crash, trace exception       |
| `unity-editor-tools`         | custom Editor Windows, Inspectors, asset validation, batch processors, UI Toolkit |
| `unity-fix-errors`           | compiler errors, exceptions, Play Mode broken, build fails                        |
| `unity-implement-logic`      | new scripts, MonoBehaviours, refactoring, gameplay features                       |
| `unity-investigate-code`     | how does X work, trace the flow, explain this code, what calls this               |
| `unity-mcp-basics`           | automate Editor, MCP tool, batch operations, find GameObject                      |
| `unity-mobile-deploy`        | iOS, Android, touch controls, mobile optimization, native features                |
| `unity-optimize-performance` | low FPS, high memory, slow load times, performance audit                          |
| `unity-plan`                 | plan feature, analyze requirements, break into tasks, estimate effort             |
| `unity-plan-brainstorm`      | review plan, refine decomposition, finalize task list                             |
| `unity-plan-tasks`          | create task skeletons, task requirements from plan                                |
| `unity-task-executor`        | execute task, implement from task guide                                           |
| `unity-task-brainstorm`      | task needs code-level details, investigating codebase                             |
| `unity-review-pr`            | review PR, check PR, PR #123, GitHub PR link                                      |
| `unity-tech-art`             | shaders, HLSL, Shader Graph, asset pipelines, procedural content                  |
| `unity-test`                 | create tests, Edit Mode tests, Play Mode tests, test assemblies                   |
| `unity-web-deploy`           | WebGL, browser issues, C#/JavaScript interop, PWA                                 |
| `unity-write-docs`           | README, documentation, API references, onboarding guides                          |
| `unity-write-tdd`            | Technical Design Document, architecture decisions, specifications                 |

## Routing Logic

```
User prompt received
├─ Error/crash/bug?
│  ├─ Has stack trace → unity-fix-errors
│  ├─ Unexpected behavior → unity-debug
│  └─ Slow/laggy → unity-optimize-performance
├─ New feature?
│  ├─ Small (1-2 files) → unity-implement-logic
│  ├─ Medium → unity-task-brainstorm → unity-task-executor
│  └─ Large/complex → unity-plan (full pipeline)
├─ Review PR? → unity-review-pr
├─ Documentation? → unity-write-docs + mermaid
├─ Data/schema? → flatbuffers-coder
├─ Mobile issue? → unity-mobile-deploy
├─ WebGL issue? → unity-web-deploy
├─ Editor tool? → unity-editor-tools + unity-mcp-basics
├─ Shader/art? → unity-tech-art
├─ Tests? → unity-test
└─ How does X work? → unity-investigate-code
```

## Skill Combinations

| Scenario                     | Combine                                                    |
| :--------------------------- | :--------------------------------------------------------- |
| Feature with docs            | `unity-plan` + `unity-write-tdd` + `mermaid`         |
| Editor tool with automation  | `unity-editor-tools` + `unity-mcp-basics`              |
| Performance-critical feature | `unity-implement-logic` + `unity-optimize-performance` |
| Mobile implementation        | `unity-implement-logic` + `unity-mobile-deploy`        |
| WebGL implementation         | `unity-implement-logic` + `unity-web-deploy`           |
| Data-driven system           | `flatbuffers-coder` + `unity-implement-logic`          |
| Documented architecture      | `unity-write-docs` + `mermaid`                         |

## Execution Pattern

### 1. Analyze Phase

- Parse user prompt
- Identify intent and required skills
- Scan `.claude/skills/` to discover available skills

### 2. Route Phase

- Match intent to skill(s) using routing logic above
- Load the matching skill's SKILL.md
- State which skill is being loaded:
  > "Loading `unity-fix-errors` to diagnose the NullReferenceException..."
  >

### 3. Execute Phase

- Follow the loaded skill's workflow completely
- Spawn subagents for subtasks if needed
- Chain to additional skills when required:
  > "Root cause identified. Chaining to `unity-implement-logic` for the fix..."
  >

### 4. Verify Phase

- Cross-check against original goal
- Validate outputs
- Run tests if applicable (`unity-test`)
- Report final results

## Agent Spawning

When spawning subagents:

```
// Spawn with specific skill
@subagent[skill-name] <subtask-prompt>

// Spawn with self-routing
@subagent <subtask-prompt>
```

## Workflow Example

User prompt: "Fix the NullReferenceException in PlayerController"

Hephaestus execution:

1. **Analyze**: Error fix request detected (has exception name)
2. **Route**: Match triggers → `unity-fix-errors`
3. **Execute**: /`unity-fix-errors <prompt>`
4. **Verify**: Check fix compiles and error resolved

## Error Handling

- If no skill matches, re-scan skills and try broader matching
- If skill execution fails, try alternative skill from combination table
- Report all failures with diagnostic info
