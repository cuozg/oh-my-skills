---
name: unity-review-code-local
description: "Deep logic review for Unity C# code in the local project. Reviews code changes with surgical focus on logic correctness, edge cases, state management, data flow, and concurrency — then adds review comments directly into the code as inline comments. No report document. No GitHub interaction. Input: commit hash, commit range, branch diff, or a feature/logic description to review. Use when: reviewing logic before commit, validating a feature implementation, auditing business logic, tracing data flow for correctness, reviewing a specific commit. Triggers: 'review code', 'review logic', 'check this logic', 'review commit', 'review my changes', 'logic review', 'code review', 'review this feature'."
---

# Unity Logic Reviewer (Local)

Deep logic review for the local project. Comments go directly into the code as inline comments — no report document, no GitHub interaction.

## Output
Inline review comments added directly into C# source files. No report document.

## Input → Diff Command

| Input | Command |
|:------|:--------|
| None (default) | `git diff` + `git diff --cached` |
| Commit SHA | `git show <hash>` |
| Commit range | `git diff <base>..<head>` |
| Branch | `git diff <branch>...HEAD` |
| Feature/logic request | User describes what to review → find relevant files via grep/LSP |

## Severity

| Severity | Meaning | Action |
|:---------|:--------|:-------|
| 🔴 Critical | Crash, data loss, security, logic that produces wrong results | Must fix |
| 🟡 Major | Logic bugs, missing edge cases, state corruption risk | Should fix |
| 🔵 Minor | Simplification, clearer intent, defensive coding | Fix or acknowledge |

## Load References

Always load:
- [INLINE_COMMENT_FORMAT.md](references/INLINE_COMMENT_FORMAT.md) — how to write and place inline review comments
- [VERIFICATION_GATES.md](references/VERIFICATION_GATES.md) — evidence requirements

## Code Standards Enforcement

Load `unity-code-standards` skill via references: logic-review-patterns.md, architecture-review.md, csharp-quality.md, performance-review.md, unity-specifics.md. Apply findings as inline review comments per [INLINE_COMMENT_FORMAT.md](references/INLINE_COMMENT_FORMAT.md).

## Workflow

1. **Fetch** — Get the diff (see Input table). For feature/logic requests, identify files first via grep/LSP.

2. **Read full context** — For each changed file, read the **entire file** (not just the diff). Logic bugs hide in what surrounds the change.

3. **Deep investigate** (parallel, `run_in_background=true`) — spawn explore agents to gather evidence (see [deep-review-workflow.md](references/deep-review-workflow.md)).

4. **Logic review** — Apply review references against evidence. Full focus areas in [deep-review-workflow.md](references/deep-review-workflow.md): control flow, state management, data flow, edge cases, Unity lifecycle, serialization safety, memory safety.

5. **Add inline comments** — Per [INLINE_COMMENT_FORMAT.md](references/INLINE_COMMENT_FORMAT.md):
   - Use `edit` to insert pro-format review comments directly into source files
   - **Full box format** for 🔴 Critical and 🟡 Major issues:
     ```
     // ╔══════════════════════════════════════════════════════════════
     // ║ REVIEW [SEVERITY]: Problem Title
     // ╟──────────────────────────────────────────────────────────────
     // ║ WHY:  [root cause]
     // ║ WHERE: [evidence — callers, files, data flow]
     // ║ FIX:  [concrete code fix]
     // ╚══════════════════════════════════════════════════════════════
     ```
   - **Quick format** for 🔵 Minor or self-evident issues:
     ```
     // ⚠ REVIEW [🔵 MINOR]: Problem → fix suggestion.
     ```
   - Every comment MUST have: problem name, WHY, and FIX
   - Batch pattern: full box on first, `// ⚠ REVIEW` back-ref on rest

6. **Summarize** — After all comments are placed, give a short verdict to the user:
   - Count of findings by severity
   - List of files modified with comments
   - Top 3 most important issues

## Comment Placement Rules

- **Add** review comments into actual source files using `edit`
- **Never** create a separate report document
- **Never** modify the actual logic — only add review comments
- One issue = one comment. Don't combine.
- Same issue in N places → full box on first, `// ⚠ REVIEW` back-ref on rest
- 🔴 and 🟡 → full box format (╔/╟/╚ borders)
- 🔵 → quick single-line format (⚠ prefix)

## Evidence Rules

- 🔴 needs: caller count + affected files + reproduction scenario
- 🟡 needs: trigger conditions + what state leads to the bug
- 🔵 needs: brief explanation of why current code is suboptimal
- **Never flag without evidence. Investigate before commenting.**

## Rules

**✅ Do's**: Read full file (not just diff). Trace data flow end-to-end. Check assumptions (null, empty, concurrent, out-of-order). Verify event subscribe/unsubscribe pairs and lifecycle ordering. For each branch, ask: "Can this state occur?" Check MonoBehaviour full lifecycle, DI consistency, async conventions, allocation frequency.

**❌ Don'ts**: Never flag style issues as 🔴/🟡. Never suggest behavioral changes beyond the issue. Never skip investigation. Never downgrade severity by fix complexity; severity reflects impact.
