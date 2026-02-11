---
name: unity-optimize-performance
description: "Fix Unity performance issues. Use when: (1) Low/inconsistent FPS, (2) High memory usage or leaks, (3) Slow load times, (4) Need to audit .claude/skills/unity-optimize-performance/scripts/assets for performance risks."
---

# Unity Performance Optimizer

Diagnose and resolve performance bottlenecks across logic, graphics, and memory.

## Purpose

Identify and fix Unity performance issues — low FPS, GC spikes, memory leaks, slow load times — using profiler data and systematic code/asset audits.

## Input

- **Required**: Performance complaint or metric target (e.g., "game drops to 15 FPS during combat", "memory grows to 2GB")
- **Optional**: Target platform, profiler captures, specific scenes/systems to audit

## Output

A performance report saved to `Documents/Performance/PERFORMANCE_REPORT_[Area]_[YYYYMMDD].md` (per `PERFORMANCE_REPORT.md` template) documenting: profiler findings, bottleneck root causes, fixes applied, and before/after metrics.

## Examples

| User Request | Skill Action |
|:---|:---|
| "Game drops to 15 FPS during combat" | Profile worst CPU frames, find Update-heavy scripts, cache GetComponent calls, report before/after FPS |
| "Memory keeps growing, never goes down" | Audit GC frames, find leaked event subscriptions and un-pooled instantiations, fix and verify |
| "Loading screen takes 30 seconds" | Profile async load, find blocking I/O, implement addressable batching, measure improvement |

## Output Requirement (MANDATORY)

**Every performance report MUST follow the template**: [PERFORMANCE_REPORT.md](.claude/skills/unity-optimize-performance/assets/templates/PERFORMANCE_REPORT.md)

Save output to: `Documents/Performance/PERFORMANCE_REPORT_[Area]_[YYYYMMDD].md`

Read the template first, then populate all sections.

## Optimization Workflow

1. **Baseline**: `coplay-mcp_list_game_objects_in_hierarchy()` for object counts, `coplay-mcp_get_unity_logs()` for high-freq logs
2. **Detect**: `grep_search` for expensive patterns in scripts
3. **Audit Graphics**: `coplay-mcp_list_objects_with_high_polygon_count()` for heavy meshes
4. **Implement**: Object pooling, cache refs, optimize algorithms, combine materials
5. **Validate**: `coplay-mcp_play_game`, check frame timing via `coplay-mcp_get_worst_cpu_frames`, ensure no visual regressions
6. **Document**: Update docs via `/unity-write-docs` if architecture changed

## Red Flags to Find

```bash
# GetComponent in Update
grep -r "GetComponent" --include="*.cs" | grep "Update"

# Camera.main usage
grep -r "Camera\.main" --include="*.cs"

# String concat in loops
grep -r '\" \+ ' --include="*.cs"

# new allocations in Update  
grep -r "new " --include="*.cs" | grep "Update"
```

## Common Fixes

| Problem | Solution |
|---------|----------|
| GetComponent in Update | Cache in Awake/Start |
| Camera.main in loops | Cache reference |
| String concatenation | StringBuilder |
| Frequent Instantiate | Object pooling |
| Too many draw calls | Combine materials, use GPU instancing |
| Large textures | Reduce size, ASTC compression |

## Best Practices

- **Avoid Update**: Event-based or reactive patterns
- **Cache Everything**: Never lookup in loops
- **Pool Objects**: Projectiles, VFX, UI elements
- **Mobile First**: Optimize for lowest-spec target device

---

## MCP Tools Integration

Prefer `coplay-mcp_*` tools for profiling and scene analysis.

| Operation | MCP Tool | Replaces |
|-----------|----------|----------|
| Object counts | `coplay-mcp_list_game_objects_in_hierarchy()` | `manage_scene(get_hierarchy)` |
| High-poly objects | `coplay-mcp_list_objects_with_high_polygon_count(threshold=1000)` | Manual mesh audit |
| Console logs | `coplay-mcp_get_unity_logs()` | `read_console` |
| CPU profiling | `coplay-mcp_get_worst_cpu_frames` | Manual profiler |
| GC profiling | `coplay-mcp_get_worst_gc_frames` | Manual profiler |
| Play/stop | `coplay-mcp_play_game` / `coplay-mcp_stop_game` | `manage_editor` |
| Check compile | `coplay-mcp_check_compile_errors` | `refresh_unity` |
| Editor state | `coplay-mcp_get_unity_editor_state` | Manual checks |
| Object details | `coplay-mcp_get_game_object_info(gameObjectPath="...")` | `manage_asset` |

### Performance Audit Flow

```
1. coplay-mcp_list_game_objects_in_hierarchy()          → Count objects, find bloat
2. coplay-mcp_list_objects_with_high_polygon_count()    → Identify heavy meshes
3. coplay-mcp_play_game                                 → Start profiling session
4. coplay-mcp_get_worst_cpu_frames                      → Find CPU bottlenecks
5. coplay-mcp_get_worst_gc_frames                       → Find GC allocation spikes
6. coplay-mcp_stop_game                                 → Stop profiling
7. [Apply optimizations]
8. coplay-mcp_check_compile_errors                      → Verify changes compile
```
