---
name: omo-sisyphus
description: "Agent spawner for oh-my-opencode (omo). Spawns @sisyphus agent with user-provided skill-name and prompt. No auto-routing - user specifies skill directly. Format: @sisyphus skill-name prompt"
---
# Sisyphus Agent Skill

**ALWAYS spawn @sisyphus agent with the skill-name provided by user.**

## Input Format

User provides:
```
<skill-name> <prompt>
```

## Trigger Call

```
@sisyphus <skill-name> <prompt>
```

## Examples

```
@sisyphus unity-fix-errors Fix the NullReferenceException in PlayerController
@sisyphus unity-plan Plan the new inventory system feature
@sisyphus unity-review-pr Review PR #25143
@sisyphus mermaid Draw the flow of the login system
@sisyphus flatbuffers-coder Create schema for player data
```

## Available Skills

| Skill                        | Description                                               |
| :--------------------------- | :-------------------------------------------------------- |
| `flatbuffers-coder`          | schema, binary data, serialize, fbs file                  |
| `mermaid`                    | diagram, visualize, flowchart, sequence diagram           |
| `skill-creator`              | create skill, update skill, new skill                     |
| `unity-debug`                | debug errors, investigate crash, trace exception          |
| `unity-editor-tools`         | custom Editor Windows, Inspectors, UI Toolkit             |
| `unity-fix-errors`           | compiler errors, exceptions, build fails                  |
| `unity-implement-logic`      | new scripts, MonoBehaviours, gameplay features            |
| `unity-investigate-code`     | how does X work, trace the flow, explain code             |
| `unity-mcp-basics`           | automate Editor, MCP tool, batch operations               |
| `unity-mobile-deploy`        | iOS, Android, mobile optimization                         |
| `unity-optimize-performance` | low FPS, high memory, performance audit                   |
| `unity-plan`                 | plan feature, break into tasks, estimate effort           |
| `unity-plan-brainstorm`      | task needs code-level details                             |
| `unity-plan-detail`          | create task skeletons, task requirements                  |
| `unity-plan-executor`        | execute task, implement from task guide                   |
| `unity-plan-review`          | review plan, finalize task list                           |
| `unity-review-pr`            | review PR, check PR, GitHub PR link                       |
| `unity-tech-art`             | shaders, HLSL, Shader Graph, procedural content           |
| `unity-test`                 | create tests, Edit Mode tests, Play Mode tests            |
| `unity-web-deploy`           | WebGL, browser issues, C#/JavaScript interop              |
| `unity-write-docs`           | README, documentation, API references                     |
| `unity-write-tdd`            | Technical Design Document, specifications                 |

## Workflow

1. **Receive** - User provides `<skill-name> <prompt>`
2. **Spawn** - `@sisyphus <skill-name> <prompt>`
3. **Execute** - Agent handles task using the specified skill, follow the skill's workflow exactly
4. **Report** - Return results to user
