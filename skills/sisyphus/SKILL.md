---
name: sisyphus
description: "Agent spawner for oh-my-opencode (omo). Use this skill when you need to delegate tasks to a specialized @sisyphus agent. The agent reads prompts, uses unity-orchestrator to route to appropriate skills, and executes tasks using ultrawork (ulw) pattern. Triggers: task delegation, multi-skill orchestration, complex workflows requiring agent coordination."
---

# Sisyphus Agent Skill

Spawn the @sisyphus agent from oh-my-opencode (omo) to handle prompts via tool calls.

## How Sisyphus Works

Sisyphus is an agent spawner that:
1. **Reads the incoming prompt** - Analyzes user request
2. **Uses unity-orchestrator** - Routes to the appropriate skill(s)
3. **Executes as ultrawork (ulw)** - Handles tasks with structured work pattern

## Spawning Sisyphus

Invoke @sisyphus agent as a tool call with the following pattern:

```
@sisyphus <prompt>
```

## Ultrawork (ULW) Pattern

All tasks handled by Sisyphus follow the ultrawork protocol:

### 1. Analyze Phase
- Parse the user prompt
- Identify intent and required skills
- Load `unity-orchestrator` skill to route the request

### 2. Route Phase
Use unity-orchestrator's routing table:

| User Intent | Primary Skill | Chain |
|:------------|:--------------|:------|
| "Review PR #X" | `unity-review-pr` | — |
| "Fix error/crash" | `unity-fix-errors` | → `unity-investigate-code` |
| "Debug why X happens" | `unity-debug` | → `unity-fix-errors` |
| "Implement [feature]" | `unity-plan` | → full pipeline |
| "Refactor X" | `unity-implement-logic` | → `unity-test` |
| "Performance issue" | `unity-optimize-performance` | — |
| "Android/iOS issue" | `unity-mobile-deploy` | — |
| "WebGL problem" | `unity-web-deploy` | — |
| "Editor tool" | `unity-editor-tools` | + `unity-mcp-basics` |
| "Shader/art" | `unity-tech-art` | — |
| "Write tests" | `unity-test` | — |
| "Write docs" | `unity-write-docs` | + `mermaid` |
| "Data schema" | `flatbuffers-coder` | — |
| "How does X work?" | `unity-investigate-code` | — |

### 3. Execute Phase
- Spawn subagents via tool calls for each subtask
- Coordinate results between subagents
- Report completion status

### 4. Verify Phase
- Cross-check against original goal
- Validate outputs from subagents
- Report final results

## Agent Spawning Protocol

When spawning subagents:

```
// Spawn with specific skill
@subagent[skill-name] <subtask-prompt>

// Spawn with orchestrator routing
@subagent <subtask-prompt>
```

## Configuration

Sisyphus uses opencode configuration for MCP server connections:

```json
{
  "mcp": {
    "server-name": {
      "type": "remote",
      "url": "http://host:port/mcp/",
      "headers": { "Authorization": "Bearer <token>" },
      "enabled": true
    }
  }
}
```

## Integration with oh-my-opencode

The skill integrates with SST OpenCode's native MCP support:
- Auto-detects MCP servers via `opencode.json`
- Uses bearer token authentication
- Supports project and agent registration

## Workflow Example

User prompt: "Fix the NullReferenceException in PlayerController"

Sisyphus execution:
1. **Analyze**: Error fix request detected
2. **Route**: unity-orchestrator → `unity-fix-errors`
3. **Execute**: Spawn subagent with `unity-fix-errors` skill
4. **Verify**: Check fix compiles and error resolved

## Error Handling

- If skill not found, fall back to `unity-orchestrator` for guidance
- If subagent fails, retry with alternative skill chain
- Report all failures with diagnostic info
