---
name: unity-review-prefab
description: PR prefab and scene review — missing scripts, broken variants, raycasts, hierarchy. Triggers — 'review prefabs', 'prefab review', 'scene review', 'check prefabs'.
---
# unity-review-prefab

Review `.prefab` and `.unity` scene files changed in a GitHub PR for missing scripts, broken variants, raycast blockers, and hierarchy issues — using parallel subagents per file.

## When to Use

- A PR adds or modifies prefabs or scene files
- Checking for missing MonoBehaviour references after a rename or delete
- Auditing UI canvas hierarchy for raycast-blocker leaks

## Workflow

1. **Fetch PR** — list changed files via `gh api repos/{owner}/{repo}/pulls/{pr}/files`
2. **Filter prefab/scene files** — select `.prefab` and `.unity` files
3. **Spawn subagents** — one `task` per file (parallel); each subagent receives the file path and checklist
4. **Per-file checks** — each subagent reads raw YAML; checks for missing scripts, broken variant bases, orphaned transforms, raycast blockers, and hierarchy depth
5. **Collect results** — aggregate findings from all subagents
6. **Post comments** — build payload and submit via `gh api` for each finding

## Rules

- Spawn one subagent per `.prefab` / `.unity` file — do not process sequentially
- Flag `m_Script: {fileID: 0}` as CRITICAL (missing MonoBehaviour)
- Flag prefab variant with missing base prefab GUID as CRITICAL
- Flag UI `Image` or `Panel` with `raycastTarget: 1` and no interactable component as WARNING
- Flag hierarchy depth > 8 levels as NOTE
- Flag transforms with non-uniform scale on rigidbody objects as WARNING
- Flag `activeSelf: 0` on root prefab GameObjects as NOTE (likely unintentional)
- Flag duplicate component types on the same GameObject (except colliders) as WARNING
- Aggregate per file before posting — one review comment block per file, not per finding
- Use severity prefix: `[CRITICAL]`, `[WARNING]`, `[NOTE]` in every comment

## Output Format

Prefab/scene comments posted to the GitHub PR, grouped by file. Print a local summary of subagent results and CRITICAL count.

## Reference Files

- `references/prefab-review-checklist.md` — missing scripts, broken variants, raycast, hierarchy checklist

Load references on demand via `read_skill_file("unity-review-prefab", "references/prefab-review-checklist")`.
