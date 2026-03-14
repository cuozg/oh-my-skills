# PR Specialist Reviews

When a PR contains mixed file types, run specialist reviews in parallel. Each review type has its own checklist in unity-standards and specific rules below.

## Code Review (.cs files)

**Routing**: Assess size per `size-assessment.md`. Minor → single-pass; Large → parallel subagents.

**Subagent criteria** (from `unity-standards/references/review/parallel-review-criteria.md`):
1. Logic — `review/logic-checklist.md`
2. Lifecycle — `review/unity-lifecycle-risks.md`
3. Serialization — `review/serialization-risks.md`
4. Performance — `review/performance-checklist.md`
5. Concurrency — `review/concurrency-checklist.md`
6. Security — `review/security-checklist.md`

**For Large PRs**, also check architecture:
7. Architecture — `review/architecture-checklist.md`

## Architecture Review

Triggers when: new systems/services/managers introduced, `.asmdef` changes, DI setup changes.

Additional rules beyond the architecture checklist:
- `FindObjectOfType` or `GameObject.Find` in production code → CRITICAL
- Concrete class injection (not interface) → WARNING
- Assemblies with bidirectional references → CRITICAL
- Static singleton access from non-manager classes → WARNING
- Classes > 300 lines without clear single responsibility → NOTE
- Event systems without unsubscription → WARNING
- Post inline comments — do not approve/reject from architecture review alone

## Asset Review (.mat, .shader, .meta, .controller, .anim, .fbx, .asset)

Checklist: `unity-standards/references/review/asset-checklist.md`

Additional rules:
- Textures > 2048px on mobile → WARNING
- `Read/Write Enabled` on meshes → WARNING (doubles memory)
- Missing mip maps on world-space textures → NOTE
- Animation clips with `loop = false` on locomotion → WARNING
- Uncompressed audio in `.meta` → WARNING
- Shaders referencing removed properties → CRITICAL
- Materials with null shader → CRITICAL
- `.anim` with sub-1% blend tree thresholds → NOTE

## Prefab/Scene Review (.prefab, .unity)

Checklist: `unity-standards/references/review/prefab-checklist.md`

**Execution**: Spawn one subagent per `.prefab`/`.unity` file — do NOT process sequentially.

Additional rules:
- `m_Script: {fileID: 0}` → CRITICAL (missing MonoBehaviour)
- Prefab variant missing base GUID → CRITICAL
- UI Image/Panel with `raycastTarget: 1` + no interactable → WARNING
- Hierarchy depth > 8 → NOTE
- Non-uniform scale on rigidbody → WARNING
- `activeSelf: 0` on root prefab → NOTE (likely unintentional)
- Duplicate component types (except colliders) → WARNING
- Aggregate per file — one comment block per file

## Aggregation

After all specialist reviews complete:
1. Merge all findings into single list
2. Deduplicate by (path, line) — keep highest severity
3. Sort by file path → line number
4. Pass to final decision step
