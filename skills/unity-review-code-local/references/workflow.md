# Load References

Always load the output format reference:
- [INLINE_COMMENT_FORMAT.md](INLINE_COMMENT_FORMAT.md) — comment format, severity tokens, delegation markers

Load shared review engine and common rules from `unity-shared`:

```python
read_skill_file("unity-shared", "references/review-engine.md")
read_skill_file("unity-shared", "references/common-rules.md")
read_skill_file("unity-shared", "references/tool-usage.md")
```

## Workflow

1. **Fetch** — Get diff (see `tool-usage.md` Input table). For feature/logic requests, identify files via grep/LSP first.
2. **Read full context** — Read the **entire file** for each changed file, not just the diff.
3. **Deep investigate** (parallel) — Spawn explore agents per `deep-workflow.md`: call-site analysis, state flow, data contracts.
4. **Logic review** — Apply all loaded review checklists + `deep-workflow.md` focus areas. Enforce `gates.md` evidence rules.
5. **Comment + Delegate** — For each finding:
   - Insert a short `// ── REVIEW` comment (per [INLINE_COMMENT_FORMAT.md](INLINE_COMMENT_FORMAT.md)).
   - For 🔴/🟡 findings: delegate the fix to `unity-code-quick` via `task(category="quick", load_skills=["unity-code-quick"], run_in_background=true)`.
   - Include in the delegation prompt: file path, line number, the review comment, and the exact fix to apply.
   - Multiple fixes → multiple parallel background tasks. Collect results after all complete.
