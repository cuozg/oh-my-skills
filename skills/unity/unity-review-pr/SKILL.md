---
name: unity-review-pr
description: "Expert Unity Developer code reviewer. Reviews PRs, commits, branches, or uncommitted changes with focus on Unity-specific patterns, performance, and best practices. Accepts Pull Request links as input. Use when: reviewing PRs, checking changes, comparing branches. Triggers: 'review PR', 'check changes', 'PR #123', GitHub PR links, commit hashes, branch names."
---

# Unity Code Reviewer

Review code changes as an **expert Unity Developer**. Each issue → separate inline comment the author must resolve before merge.

## Purpose

Automate expert-level Unity code reviews on GitHub PRs, commits, branches, or uncommitted changes — catching Unity-specific anti-patterns, performance regressions, and architectural issues that generic reviewers miss.

## Output

A GitHub PR review submitted via `post_review.sh`, containing:
- Summary body with PR scope, severity counts, acceptance criteria, and impact analysis
- Individual inline comments per issue (one comment = one issue), formatted per [REVIEW_TEMPLATE.md](references/REVIEW_TEMPLATE.md)
- Approval decision: `APPROVE`, `COMMENT`, or `REQUEST_CHANGES`

## Examples

| User Request | Skill Action |
|:-------------|:-------------|
| "Review PR #25141" | Fetch diff via `gh pr diff`, load matching reference files, investigate callers/impact, generate review JSON, submit via `post_review.sh` |
| "Check changes on branch feature/combat" | Run `git diff feature/combat...HEAD`, analyze diff against Unity patterns, post review |
| "Review my uncommitted changes" | Run `git diff` + `git diff --cached`, apply all review criteria, submit inline comments |
| "Review commit abc1234" | Run `git show abc1234`, investigate changed methods for callers, generate review |

## Output Requirement (MANDATORY)

> [!CAUTION]
> **MUST follow [REVIEW_TEMPLATE.md](references/REVIEW_TEMPLATE.md) for output format — no variations.**
> All review logic, criteria, and decision rules live HERE — the template is output format only.

Submit using: `.opencode/skills/unity/unity-review-pr/scripts/post_review.sh <pr_number> /tmp/review.json`

## Input

| Input Type | Detection | Commands |
|:-----------|:----------|:---------|
| **No arguments** | Default | `git diff`, `git diff --cached`, `git status --short` |
| **Commit hash** | SHA or short hash | `git show <hash>` |
| **Branch name** | Branch identifier | `git diff <branch>...HEAD` |
| **PR URL/number** | Contains "github.com", "pull", or PR number | `gh pr view`, `gh pr diff` |

## Severity Guide

- **🔴 Critical**: Crash, data loss, memory leak, severe perf regression → blocks merge
- **🟡 Major**: Conditional failure, encapsulation break, subtle bugs → should fix before merge
- **🔵 Minor**: Style, conventions, minor improvements → nice to fix, not blocking

**Approval logic:** Any 🔴 → `REQUEST_CHANGES` · Only 🟡/🔵 → `COMMENT` · Clean → `APPROVE`

---

## Reference Files — What to Load and When

Load reference files based on **what changed in the diff**. Always load REVIEW_TEMPLATE.md.

| Changed File Types | Load Reference | Why |
|:-------------------|:---------------|:----|
| `.cs` files | [LOGIC_REVIEW.md](references/LOGIC_REVIEW.md) | C# anti-patterns, Unity performance, async safety, investigation patterns |
| `.prefab`, `.unity` files | [PREFAB_REVIEW.md](references/PREFAB_REVIEW.md) | Script refs, prefab variants, hierarchy, UI config, serialization |
| `.mat`, `.shader`, `.meta`, `.controller`, `.anim`, `.asset` | [ASSET_REVIEW.md](references/ASSET_REVIEW.md) | Materials, textures, animation, audio, component properties |
| New system, refactor, architecture change | [BLUEPRINT_REVIEW.md](references/BLUEPRINT_REVIEW.md) | SOLID, Unity architecture, system design, API design |
| **Always** | [REVIEW_TEMPLATE.md](references/REVIEW_TEMPLATE.md) | Output format (JSON structure, inline comment format) |

**Multiple types changed?** Load ALL matching references. Most PRs touch `.cs` + `.prefab` → load both LOGIC_REVIEW.md and PREFAB_REVIEW.md.

---

## Investigation Rules

**Never flag an issue without investigating callers/impact first.**

- Every 🔴 must include evidence (caller count, affected files)
- Every 🟡 must explain conditions under which the issue manifests
- Each reference file contains domain-specific grep patterns and report templates

### Priority Investigation Order

1. Method signature changes → find all callers (see LOGIC_REVIEW.md)
2. Event/delegate changes → find all subscribers (see LOGIC_REVIEW.md)
3. Serialized field changes → check prefabs/assets (see LOGIC_REVIEW.md + PREFAB_REVIEW.md)
4. Inheritance changes → check all derived types (see LOGIC_REVIEW.md)
5. Public API changes → check cross-assembly impact (see BLUEPRINT_REVIEW.md)
6. Prefab/scene changes → run asset issue grep patterns (see PREFAB_REVIEW.md)
7. UI changes → audit RaycastTarget, Canvas, Layout (see PREFAB_REVIEW.md)
8. Material/texture changes → verify shader, compression, imports (see ASSET_REVIEW.md)

---

## Workflow

### Phase 1: Fetch Changes

```bash
# PR
gh pr diff <number> --patch
gh pr view <number> --json title,body,files

# Uncommitted
git diff && git diff --cached && git status --short
```

### Phase 2: Investigate Codebase

**Delegate to subagent** — understand patterns, not just diffs.

Use `@explore` or `@librarian` to:
- Read full files for context around changed lines
- Find callers of changed methods (grep patterns in reference files)
- Trace event subscribers; verify unsubscribe pairs
- Check for similar patterns elsewhere needing the same fix
- Identify breaking change impact (signatures, serialization, interfaces)
- Verify Unity lifecycle correctness (Awake → OnEnable → Start order)

**For asset file changes** (`.prefab`, `.unity`, `.mat`, `.asset`, `.meta`):
- Run prefab/asset investigation patterns from PREFAB_REVIEW.md and ASSET_REVIEW.md
- Audit RaycastTarget on all Image/Text components in changed prefabs
- Verify shader/material assignments are valid
- Check texture import settings match platform requirements
- Validate component properties (AudioSource, Animator, ParticleSystem settings)
- **Every asset issue MUST use the three-part format**: Issue, Why, Suggestion (see ASSET_REVIEW.md §7 and REVIEW_TEMPLATE.md)

### Phase 3: Generate Acceptance Criteria

Analyze PR changes → create testable acceptance criteria by category:

- **UI Verification**: Layout, rendering, animation, responsive behavior, RaycastTarget correctness
- **Functional Verification**: Feature logic, edge cases, error handling
- **Performance Verification**: Frame drops, memory, GC spikes, load times
- **Data Verification**: Save migration, serialization, config values, no breaking changes
- **Asset Verification**: Prefab integrity, material/shader assignment, texture imports, component properties

Each criterion must reference actual classes, methods, and scenarios from the PR.

### Phase 4: Create Review JSON

Build `/tmp/review.json` per **[REVIEW_TEMPLATE.md](references/REVIEW_TEMPLATE.md)**.

1. Write summary body with PR number, scope, assessment, acceptance criteria
2. Count issues by severity: 🔴 Breaking · 🟡 Potential · 🔵 Quality
3. One `comments` entry per issue — never combine
4. Each comment: `path`, `line` (right side of diff), `side: "RIGHT"`, `body` (formatted per template)
5. Include `suggestion` code blocks for actionable fixes
6. Add Impact Analysis (files investigated, breaking call sites found)
7. **For asset issues**: Verify every comment passes the self-check in [ASSET_REVIEW.md §7](references/ASSET_REVIEW.md) — Issue ✓ Why ✓ Suggestion ✓

**Line number rules:** Use right-side line number. For deleted lines, use last line of surrounding context. `side` always `"RIGHT"`.

### Phase 5: Submit

```bash
.opencode/skills/unity/unity-review-pr/scripts/post_review.sh <pr_number> /tmp/review.json
```

Verify submission succeeds. If it fails, check: valid JSON, correct PR number, line numbers exist in diff.

**Fallback for merged/closed PRs:**
```bash
gh pr comment <number> --body "## Post-Merge Review\n\n<body>"
```

**Fallback for API errors:**
```bash
gh api -X POST -H "Accept: application/vnd.github+json" \
  repos/{owner}/{repo}/pulls/{pr_number}/reviews \
  -f body="[REVIEW BODY]" -f event="COMMENT"
```

---

## Critical Rules

### ✅ Always

1. Follow [REVIEW_TEMPLATE.md](references/REVIEW_TEMPLATE.md) for output format
2. Load the correct reference files based on changed file types (see table above)
3. Apply ALL review criteria from loaded reference files — Unity patterns first
4. Generate Acceptance Criteria based on PR changes
5. Submit using `post_review.sh` — verify posted successfully
6. Each issue = separate `comments` entry
7. Submit even if PR is merged/closed
8. **Every asset issue comment MUST include all three parts: Issue, Why, Suggestion** — verify against the self-check in [ASSET_REVIEW.md §7](references/ASSET_REVIEW.md) before posting

### ❌ Never

1. Deviate from REVIEW_TEMPLATE.md output format
2. Skip Acceptance Criteria section
3. Combine multiple issues into one comment
4. Skip GitHub submission
5. Flag issues without investigating callers/impact
6. Miss Unity-specific patterns (Update allocations, async safety, lifecycle)
7. Ignore RaycastTarget on decorative Image/Text in UI prefabs
8. Skip prefab/material/texture checks when those files are in the diff
9. **Post an asset issue missing Issue, Why, or Suggestion** — incomplete asset comments are rejected

**Review is incomplete until each issue is a resolvable comment on GitHub.**

---

## MCP Tools Integration

Optionally verify compilation and runtime behavior after reviewing code changes.

| Operation | MCP Tool | Use Case |
| --------- | -------- | -------- |
| Check compilation | `unityMCP_check_compile_errors` | Verify PR changes compile cleanly |
| Read console | `unityMCP_get_unity_logs(show_errors=true)` | Check for runtime errors post-merge |
| Play/stop game | `unityMCP_play_game` / `unityMCP_stop_game` | Smoke-test PR changes in Editor |
| Inspect hierarchy | `unityMCP_list_game_objects_in_hierarchy()` | Verify scene structure changes |
| Get object details | `unityMCP_get_game_object_info(gameObjectPath="...")` | Validate component/property changes |

### Post-Review Verification (Optional)

```
1. unityMCP_check_compile_errors         → confirm PR compiles
2. unityMCP_get_unity_logs(show_errors=true) → check for warnings/errors
3. unityMCP_play_game                    → smoke-test if needed
4. unityMCP_stop_game                    → end test session
```
