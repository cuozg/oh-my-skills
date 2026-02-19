---
name: unity-review-code
description: "Review Unity code changes before commit or PR creation. Self-review uncommitted/staged changes with Unity-specific checklists (performance, lifecycle, serialization, assets), verification gates, and evidence-based findings. Outputs local markdown report. Use when: completing a task, before committing, before creating a PR, after fixing bugs, after refactoring. Triggers: 'review code', 'review changes', 'review before commit', 'self-review', 'check my changes', 'review my work', 'pre-commit review', 'code review'."
---

# Unity Code Reviewer (Pre-Commit)

Review code changes before commit or PR. Output local markdown report with evidence-based findings.

## Input → Diff Command

| Input | Command |
|:------|:--------|
| None (default) | `git diff` + `git diff --cached` |
| Staged only | `git diff --cached` |
| Branch | `git diff <branch>...HEAD` |
| Commit range | `git diff <base>..<head>` |
| Specific files | `git diff -- <paths>` |

## Severity Levels

| Severity | Meaning | Action |
|:---------|:--------|:-------|
| 🔴 Critical | Crash, data loss, security, memory leak in hot path | **Must fix** before commit |
| 🟡 Major | Logic bugs, missing error handling, arch violations | **Should fix** before commit |
| 🔵 Minor | Code quality, conventions, naming | Fix or acknowledge |
| 💚 Suggestion | Readability, modern patterns, micro-optimization | Optional |

## Load References by Changed Files

Always load:
- [REVIEW_CHECKLISTS.md](references/REVIEW_CHECKLISTS.md) — Unity-specific + general checklists
- [VERIFICATION_GATES.md](references/VERIFICATION_GATES.md) — evidence requirements, verification protocol
- [OUTPUT_FORMAT.md](references/OUTPUT_FORMAT.md) — report template

## Workflow

1. **Fetch** diff (see Input table). Count changed lines to determine review depth.

   | Changed Lines | Depth |
   |:--------------|:------|
   | < 50 | Security + Correctness + Performance only |
   | 50–300 | All checklists |
   | > 300 | Flag scope. Prioritize Security + Correctness. Note risk in summary. |

2. **Context Gathering** (parallel, `run_in_background=true`) — spawn agents **before** reading full diff.

   **`@explore` agents (1-3):**

   | Agent | Task |
   |:------|:-----|
   | Codebase patterns | Read changed files + surrounding context. Identify conventions, architecture, existing patterns. |
   | Impact analysis | Find callers, subscribers, derived types, prefab/SO refs for modified public members. Count call sites. |
   | Related tests | Find existing test files for changed code. Check if test updates are needed. |

   **`@librarian` agents (0-1, when external library involved):**

   | Agent | Task |
   |:------|:-----|
   | Library docs | Fetch API docs, known issues for new/updated packages. |

3. **Review** — Collect agent results. Apply [REVIEW_CHECKLISTS.md](references/REVIEW_CHECKLISTS.md) against evidence.

   **By file type:**

   | Changed Files | Checklist Section |
   |:------|:----------|
   | `.cs` | C# Logic & Performance patterns |
   | `.prefab`, `.unity` | Prefab & Scene patterns |
   | `.mat`, `.shader`, `.meta`, `.controller`, `.anim`, `.fbx`, `.asset` | Asset patterns |

   **Evidence rules:** 🔴 needs caller count + affected files. 🟡 needs trigger conditions. **Never flag without evidence.**

4. **Verify** — Apply [VERIFICATION_GATES.md](references/VERIFICATION_GATES.md). Run build/tests if available. Evidence before claims.

5. **Generate** — Create report per [OUTPUT_FORMAT.md](references/OUTPUT_FORMAT.md) at `Documents/Reviews/<identifier>_review.md`.
   Use `./skills/unity-review-code/scripts/create_review.sh <identifier>` to initialize output file.

6. **Report** — Summarize findings to user with verdict and action items.

## Verdict

| Condition | Verdict | Action |
|:----------|:--------|:-------|
| Any 🔴 Critical | ❌ **NOT READY** | Fix before commit |
| 🟡 Major only | ⚠️ **NEEDS WORK** | Fix or justify before commit |
| Only 🔵/💚 | ✅ **READY** | Safe to commit (with optional improvements) |
| No issues | ✅ **CLEAN** | Commit |

## Rules

- ✅ One issue = one finding. Investigate before flagging. Always provide evidence.
- ✅ Same issue in N files → full explanation on first, short ref on rest (batch pattern).
- ✅ Run verification commands before claiming build/tests pass.
- ✅ Check changed files against ALL applicable checklists.
- ❌ Never flag without evidence. Never claim "tests pass" without running them.
- ❌ Never combine multiple issues into one finding. Never skip verification gates.
- ❌ Never suggest changes that alter behavior beyond the flagged issue.
