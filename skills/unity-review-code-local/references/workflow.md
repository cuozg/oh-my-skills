# unity-review-code-local — Workflow

## 1. Fetch Changes

Get diff per `common-rules.md` Input table (loaded via `read_skill_file("unity-shared", "references/common-rules.md")`). For feature/logic requests, identify files via grep/LSP first.

## 2. Read Full Context

Read the **entire file** for each changed file, not just the diff.

## 3. Deep Investigate (Parallel)

Spawn explore agents per `review-deep-workflow.md` (loaded via `read_skill_file`): call-site analysis, state flow, data contracts. Enforce `review-gates.md` evidence rules.

## 4. Logic Review

Apply all loaded review checklists + deep-workflow focus areas:
- Control flow correctness
- State management safety
- Data flow integrity
- Edge cases and boundaries
- Unity lifecycle compliance
- Serialization safety
- Memory safety and allocations

## 5. Comment + Delegate

For each finding:
- Insert a short `// ── REVIEW` comment (per `output-template.md`).
- For 🔴/🟡 findings: delegate the fix to `unity-code-quick` via background task:
  ```
  task(category="quick", load_skills=["unity-code-quick"], run_in_background=true)
  ```
- Include in delegation prompt: file path, line number, review comment, exact fix to apply.
- 🔵/🟢 findings: comment only — no delegation.
- Multiple fixes → multiple parallel background tasks. Collect results after all complete.

## Rules

- **Review only** — insert `// ── REVIEW` comments only. Never apply code fixes directly. Only 🔴/🟡 get delegated to `unity-code-quick`.
- Comments are short, focused, highlight-style. No verbose explanations.
- Never commit. Never push. User reviews the combined diff.
