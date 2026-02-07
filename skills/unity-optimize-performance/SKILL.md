---
name: unity-optimize-performance
description: "Fix Unity performance issues. Use when: (1) Low/inconsistent FPS, (2) High memory usage or leaks, (3) Slow load times, (4) Need to audit .claude/skills/unity-optimize-performance/scripts/assets for performance risks."
---

# Unity Performance Optimizer

Diagnose and resolve performance bottlenecks across logic, graphics, and memory.

## Output Requirement (MANDATORY)

**Every performance report MUST follow the template**: [PERFORMANCE_REPORT.md](.claude/skills/unity-optimize-performance/assets/templates/PERFORMANCE_REPORT.md)

Save output to: `Documents/Performance/PERFORMANCE_REPORT_[Area]_[YYYYMMDD].md`

Read the template first, then populate all sections.

## Optimization Workflow

1. **Baseline**: `manage_scene(get_hierarchy)` for object counts, `read_console` for high-freq logs
2. **Detect**: `grep_search` for expensive patterns in scripts
3. **Audit Graphics**: `manage_asset` for large assets, `manage_material` for complex shaders
4. **Implement**: Object pooling, cache refs, optimize algorithms, combine materials
5. **Validate**: Play Mode, check frame timing, ensure no visual regressions
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
