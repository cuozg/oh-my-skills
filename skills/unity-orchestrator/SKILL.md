---
name: unity-orchestrator
description: "Master Unity technical lead. Use for ALL Unity requests. Analyzes prompts, routes to specialized skills (logic, art, performance, mobile, PR review, debugging), and coordinates multi-step implementations."
---

# Unity Orchestrator

Route tasks to specialized skills and coordinate complex implementations.

## Output Requirement (MANDATORY)

**Every routing decision MUST follow the template**: [ROUTING_DECISION.md](assets/templates/ROUTING_DECISION.md)

Output the routing decision as part of the orchestration log. No file save required.

Read the template first, then populate all sections.

## Quick Routing

### By Intent

| User Intent | Primary Skill | Chain |
|:------------|:--------------|:------|
| "Review PR #X" | `unity-review-pr` | — |
| "Fix this error/crash" | `unity-fix-errors` | → `unity-investigate-code` if root cause unclear |
| "Debug why X happens" | `unity-debug` | → `unity-fix-errors` after diagnosis |
| "Implement [feature]" | `unity-plan` | → `unity-plan-brainstorm` → `unity-plan-tasks` → `unity-task-brainstorm` → `unity-task-executor` |
| "Refactor X" | `unity-implement-logic` | → `unity-test` to verify |
| "Game is slow/laggy" | `unity-optimize-performance` | — |
| "Android/iOS issue" | `unity-mobile-deploy` | — |
| "WebGL problem" | `unity-web-deploy` | — |
| "Create editor tool" | `unity-editor-tools` | + `unity-mcp-basics` for automation |
| "Shader/art pipeline" | `unity-tech-art` | — |
| "Write tests" | `unity-test` | — |
| "Write TDD" | `unity-write-tdd` | + `mermaid` for diagrams |
| "Write docs/README" | `unity-write-docs` | + `mermaid` for architecture |
| "Add data table/schema" | `flatbuffers-coder` | — |
| "How does X work?" | `unity-investigate-code` | — |
| "Create a diagram" | `mermaid` | — |
| "Automate Editor task" | `unity-mcp-basics` | — |
| "Create/update a skill" | `skill-creator` | — |

### Decision Tree: Errors & Debugging

```
User reports error/crash/bug?
├─ Has stack trace or error message?
│  ├─ YES → unity-fix-errors (diagnose + fix)
│  │        └─ Can't find root cause? → unity-investigate-code
│  └─ NO → Ask for console output first
├─ Unexpected behavior (no error)?
│  └─ unity-debug (strategic logging + analysis)
│     └─ Found cause? → unity-fix-errors or unity-implement-logic
└─ Performance issue (slow, lag, memory)?
   └─ unity-optimize-performance
```

### Decision Tree: Feature Implementation

```
User wants new feature?
├─ Small/isolated change (1-2 files)?
│  └─ unity-implement-logic directly
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
| Editor tool with automation | `unity-editor-tools` + `unity-mcp-basics` |
| Performance-critical feature | `unity-implement-logic` + `unity-optimize-performance` |
| Mobile-specific implementation | `unity-implement-logic` + `unity-mobile-deploy` |
| WebGL-specific implementation | `unity-implement-logic` + `unity-web-deploy` |
| Data-driven system | `flatbuffers-coder` + `unity-implement-logic` |
| Documented architecture | `unity-write-docs` + `mermaid` |

For full skill catalog, see [SKILL_CATALOG.md](references/SKILL_CATALOG.md).

## Orchestration Protocol

### 1. Classify & Route

Match user intent to skill(s) using tables above. State which skill you're loading:

> "Loading `unity-fix-errors` to diagnose the NullReferenceException..."

### 2. Delegate

Adopt the specialist skill's workflow completely. Follow its protocols, templates, and best practices.

### 3. Chain (if needed)

When initial skill recommends another, chain explicitly:

> "Root cause identified. Chaining to `unity-implement-logic` for the fix..."

### 4. Verify & Cross-Cut

After completion:
- Verify against original goal
- Check cross-cutting concerns (performance, memory, platform compatibility)
- Run tests if applicable (`unity-test`)

For multi-step coordination patterns, see [ORCHESTRATION_PATTERNS.md](references/ORCHESTRATION_PATTERNS.md).

## Guiding Principles

- **Performance First**: Always consider frame budget impact
- **Safety First**: Non-destructive operations, verify before execution  
- **Tool Mastery**: Use `unityMCP` for Editor automation tasks
- **Document "Why"**: Explain architectural decisions, not just "what"
- **Test Coverage**: Verify changes don't break existing functionality
