# PR Specialist Reviews

When a PR contains mixed file types, run specialist reviews in parallel. Each specialist has its own focus area, checklist, and rules.

## Routing Table

| File Pattern | Specialist | Parallelism |
|---|---|---|
| `.cs` (Minor PR) | Code review — single pass | 1 subagent (all 6 criteria inline) |
| `.cs` (Large PR) | Code review — parallel | 6 subagents (one per criterion) |
| `.prefab`, `.unity` | Prefab/Scene review | 1 subagent per file |
| `.mat`, `.shader`, `.meta`, `.controller`, `.anim`, `.fbx`, `.asset` | Asset review | 1 subagent for all asset files |
| `.cs` with new systems/services/managers, `.asmdef` changes | Architecture review | 1 subagent |

Spawn all applicable specialists in the same turn — do not wait for one to finish before starting others.

## Code Review (.cs files)

### Minor PR (single-pass)

Review all `.cs` files yourself in one pass:
1. Load all 6 checklist sections from `read_skill_file("unity-standards", "references/review/checklist.md")`
2. Check every item against the changed code
3. Produce findings as `[{path, line, severity, title, body}]`

### Large PR (parallel subagents)

Spawn 6 parallel subagents per `unity-standards/references/review/parallel-review-criteria.md`:

| # | Criterion | Checklist Section | Focus |
|---|-----------|-------------------|-------|
| 1 | Logic | `## 1. Logic` | Null guards, boundaries, edge cases, state, data flow |
| 2 | Unity Lifecycle | `## 2. Unity Lifecycle` | Execution order, destroy timing, subscribe symmetry |
| 3 | Serialization | `## 3. Serialization` | Field renames, type changes, enum stability, SO risks |
| 4 | Performance | `## 4. Performance` | Hot-path allocations, component lookup, physics, rendering |
| 5 | Security | `## 5. Security` | Input validation, secrets, debug code, network |
| 6 | Concurrency | `## 6. Concurrency` | Main thread rule, async/await, Jobs, race conditions |

For Large PRs, also check:
- 7: Architecture — `## 7. Architecture` (triggers when new systems/managers introduced)

**Subagent prompt:**
```
TASK: Review these C# files for {criterion_name} issues only.

CHECKLIST: Load `read_skill_file("unity-standards", "references/review/checklist.md")`
           Check every item under section `## {N}. {criterion_name}`.

FILES:
{for each .cs file: path, full content, and diff patch}

MUST DO:
- Check EVERY checklist item against the changed code
- Report as JSON array: [{path, line, severity, title, body}]
- severity must be one of: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "STYLE"
- Include a suggestion block in body for MEDIUM+ findings
- Focus ONLY on your assigned criterion
- Return empty array [] if no issues found

MUST NOT DO:
- Review criteria outside your assigned section
- Report issues on unchanged lines (only review code touched by the PR)
- Report stylistic issues that contradict project conventions
```

## Architecture Review

**Triggers when:** New systems/services/managers introduced, `.asmdef` changes, DI setup changes.

Uses `review/checklist.md` section `## 7. Architecture` plus these additional rules:

| Pattern | Severity | Reason |
|---------|----------|--------|
| `FindObjectOfType` or `GameObject.Find` in production code | CRITICAL | Runtime coupling, fragile, slow |
| Concrete class injection (not interface) | WARNING | Blocks testing, tight coupling |
| Assemblies with bidirectional references | CRITICAL | Circular dependency, build order issues |
| Static singleton access from non-manager classes | WARNING | Hidden dependency, hard to test |
| Classes > 300 lines without clear single responsibility | NOTE | God object risk |
| Event systems without unsubscription | WARNING | Memory leak, duplicate handlers |

Architecture review posts inline comments only — it does not approve/reject on its own. The final decision aggregates all specialists.

## Asset Review

**Triggers when:** PR contains `.mat`, `.shader`, `.meta`, `.controller`, `.anim`, `.fbx`, or `.asset` files.

Uses `review/checklist.md` section `## 8. Assets & Prefabs` plus these additional rules:

| Pattern | Severity | Reason |
|---------|----------|--------|
| Textures > 2048px on mobile platform | WARNING | Memory budget, load time |
| `Read/Write Enabled` on meshes | WARNING | Doubles runtime memory |
| Missing mip maps on world-space textures | NOTE | Aliasing, GPU cache inefficiency |
| Animation clips with `loop = false` on locomotion | WARNING | Unexpected animation stops |
| Uncompressed audio in `.meta` | WARNING | Unnecessary build size |
| Shaders referencing removed properties | CRITICAL | Pink/missing materials at runtime |
| Materials with null shader | CRITICAL | Rendering failure |
| `.anim` with sub-1% blend tree thresholds | NOTE | Unreachable animation states |

## Prefab/Scene Review

**Triggers when:** PR contains `.prefab` or `.unity` files.

**Execution:** Spawn one subagent per `.prefab`/`.unity` file — do NOT process sequentially.

Uses `review/checklist.md` section `## 8. Assets & Prefabs` plus these additional rules:

| Pattern | Severity | Reason |
|---------|----------|--------|
| `m_Script: {fileID: 0}` | CRITICAL | Missing MonoBehaviour, null ref at runtime |
| Prefab variant missing base GUID | CRITICAL | Broken variant chain |
| UI Image/Panel with `raycastTarget: 1` + no interactable | WARNING | Unnecessary input processing |
| Hierarchy depth > 8 | NOTE | Transform traversal cost, maintenance burden |
| Non-uniform scale on rigidbody | WARNING | Physics collision shape distortion |
| `activeSelf: 0` on root prefab | NOTE | Likely unintentional disabled state |
| Duplicate component types (except colliders) | WARNING | Redundant processing, ambiguous state |

Aggregate findings per file — produce one comment block per `.prefab`/`.unity` file.

## Aggregation

After all specialist reviews complete:

1. Merge all findings into a single list
2. Deduplicate by (path, line) — keep highest severity when same location flagged by multiple specialists
3. Sort by file path → line number
4. Pass aggregated findings to the final decision step (step 8 of `pr-review-workflow.md`)

Severity precedence: CRITICAL > HIGH > MEDIUM > LOW > STYLE
