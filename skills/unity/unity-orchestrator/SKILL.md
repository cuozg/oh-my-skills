---
name: unity-orchestrator
description: "Master Unity technical lead. Use for ALL Unity requests. Analyzes prompts, routes to specialized skills (logic, art, performance, mobile, PR review, debugging), and coordinates multi-step implementations."
---

# Unity Orchestrator

Route tasks to specialized skills and coordinate complex implementations.

## Output Requirement (MANDATORY)

**Every routing decision MUST follow the template**: [ROUTING_DECISION.md](.claude/skills/unity-orchestrator/assets/templates/ROUTING_DECISION.md)

Output the routing decision as part of the orchestration log. No file save required.

Read the template first, then populate all sections.

## Quick Routing

### By Intent

| User Intent | Primary Skill | Chain |
|:------------|:--------------|:------|
| "Review PR #X" | `unity-review-pr` | — |
| "Fix this error/crash" | `unity-fix-errors` | → `unity-investigate` if root cause unclear |
| "Debug why X happens" | `unity-debug` | → `unity-fix-errors` after diagnosis |
| "Implement [feature]" | `unity-plan` | → `unity-plan-brainstorm` → `unity-plan-tasks` → `unity-task-brainstorm` → `unity-task-executor` |
| "Refactor X" | `unity-code` | → `unity-test` to verify |
| "Game is slow/laggy" | `unity-optimize-performance` | — |
| "Android/iOS issue" | `unity-mobile-deploy` | — |
| "WebGL problem" | `unity-web-deploy` | — |
| "Create editor tool" | `unity-editor-tools` | + `unity-mcp` for automation |
| "Shader/art pipeline" | `unity-tech-art` | — |
| "Write tests" | `unity-test` | — |
| "Write TDD" | `unity-write-tdd` | + `mermaid` for diagrams |
| "Write docs/README" | `unity-write-docs` | + `mermaid` for architecture |
| "Add data table/schema" | `flatbuffers-coder` | — |
| "How does X work?" | `unity-investigate` | — |
| "Create a diagram" | `mermaid` | — |
| "Automate Editor task" | `unity-mcp` | — |
| "Create/update a skill" | `skill-creator` | — |

### Decision Tree: Errors & Debugging

```
User reports error/crash/bug?
├─ Has stack trace or error message?
│  ├─ YES → unity-fix-errors (diagnose + fix)
│  │        └─ Can't find root cause? → unity-investigate
│  └─ NO → Ask for console output first
├─ Unexpected behavior (no error)?
│  └─ unity-debug (strategic logging + analysis)
│     └─ Found cause? → unity-fix-errors or unity-code
└─ Performance issue (slow, lag, memory)?
   └─ unity-optimize-performance
```

### Decision Tree: Feature Implementation

```
User wants new feature?
├─ Small/isolated change (1-2 files)?
│  └─ unity-code directly
├─ Medium feature (known scope)?
│  └─ unity-task-brainstorm → unity-task-executor
└─ Large/complex feature?
   └─ Full pipeline:
      unity-plan → unity-plan-brainstorm → unity-plan-tasks 
      → unity-task-brainstorm → unity-task-executor
```

### Skill Combinations

| Scenario | Combine |
|:---------|:--------|
| New feature with documentation | `unity-plan` + `unity-write-tdd` + `mermaid` |
| Editor tool with automation | `unity-editor-tools` + `unity-mcp` |
| Performance-critical feature | `unity-code` + `unity-optimize-performance` |
| Mobile-specific implementation | `unity-code` + `unity-mobile-deploy` |
| WebGL-specific implementation | `unity-code` + `unity-web-deploy` |
| Data-driven system | `flatbuffers-coder` + `unity-code` |
| Documented architecture | `unity-write-docs` + `mermaid` |

For full skill catalog, see [SKILL_CATALOG.md](.claude/skills/unity-orchestrator/references/SKILL_CATALOG.md).

## Orchestration Protocol

### 1. Classify & Route

Match user intent to skill(s) using tables above. State which skill you're loading:

> "Loading `unity-fix-errors` to diagnose the NullReferenceException..."

### 2. Delegate

Adopt the specialist skill's workflow completely. Follow its protocols, templates, and best practices.

### 3. Chain (if needed)

When initial skill recommends another, chain explicitly:

> "Root cause identified. Chaining to `unity-code` for the fix..."

### 4. Verify & Cross-Cut

After completion:
- Verify against original goal
- Check cross-cutting concerns (performance, memory, platform compatibility)
- Run tests if applicable (`unity-test`)

For multi-step coordination patterns, see [ORCHESTRATION_PATTERNS.md](.claude/skills/unity-orchestrator/references/ORCHESTRATION_PATTERNS.md).

## Guiding Principles

- **Performance First**: Always consider frame budget impact
- **Safety First**: Non-destructive operations, verify before execution  
- **Tool Mastery**: Use `coplay-mcp_*` tools for Editor automation tasks
- **Document "Why"**: Explain architectural decisions, not just "what"
- **Test Coverage**: Verify changes don't break existing functionality

---

## MCP Tools Integration

Route `coplay-mcp_*` tools to the correct specialist skill. Key tool-to-skill mappings:

| MCP Tool | Route To |
|----------|----------|
| `coplay-mcp_check_compile_errors` | `unity-code`, `unity-fix-errors`, `unity-test` |
| `coplay-mcp_get_unity_logs` | `unity-fix-errors`, `unity-debug`, `unity-optimize-performance` |
| `coplay-mcp_play_game` / `stop_game` | `unity-fix-errors`, `unity-debug`, `unity-test` |
| `coplay-mcp_execute_script` | `unity-test`, `unity-editor-tools` |
| `coplay-mcp_get_worst_cpu_frames` / `get_worst_gc_frames` | `unity-optimize-performance` |
| `coplay-mcp_create_material` / `assign_shader_to_material` | `unity-tech-art` |
| `coplay-mcp_list_game_objects_in_hierarchy` / `get_game_object_info` | `unity-investigate`, `unity-debug` |
| `coplay-mcp_get_unity_editor_state` | Any skill needing project context |
