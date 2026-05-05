---
name: goal-verify
description: "Verify one goal by checking every acceptance criterion one by one against the codebase. Do not batch-verify criteria. Searches repo for code/test evidence and generates structured test reports with per-criterion verdicts. Use after goal-execute to validate implementation. Auto-triages quick vs deep mode."
---

# goal-verify

Third gate in the goals pipeline.

```
goal-create   →   goal-improve   →   goal-execute   →   goal-verify
  write          critique          execute          verify
```

`goal-create` defines what "done" means. `goal-execute` builds it. **`goal-verify`
answers the single question**: *did we actually meet the acceptance
criteria we wrote down?* If the criteria themselves are weak, `goal-improve`
critiques and improves the goal before another execution pass.

The skill is deliberately read-only against the target repo (it writes
**only** the test report). It never edits source, never marks criteria
complete, never updates `Master.md`. Those actions belong to other skills.

---

## The Iron Law

> **Every acceptance criterion gets one verdict — `✅ Met`, `⚠️ Partial`,
> or `❌ Unmet` — backed by file-path evidence or an explicit
> "no evidence found" note. No verdict is handwaved.**

If you cannot produce evidence for a criterion, it is `❌ Unmet`. Period.
A criterion marked `- [x]` in the goal file is trusted as `✅ Met` (the
author attested to it) but the evidence columns still populate from the
repo scan.

---

## Document Export Contract

**Every `goal-verify` run MUST:**

1. Parse one goal file at `Docs/Goals/<feature>/<task>.md`.
2. Extract YAML frontmatter (`status`, `priority`, `created`, `updated`,
   `depends_on`) and the `## Acceptance Criteria` checklist.
3. For each criterion, produce a verdict and evidence.
4. Write the report to `Docs/Goals/{feature-name}/{kebab-case-test}.md` (path
   derived from the goal's location under `Docs/Goals/`).
5. Return the counts `{total, met, partial, unmet}` on stdout.

**Every `goal-verify` run MUST NOT:**

- Edit the goal file itself (use `goal-create` for that).
- Mark checkboxes `- [x]` (use `goal-create` or `goal-improve`).
- Update `Docs/Goals/Master.md` (derived by `goal-create`).
- Write source code or tests (use the domain-specific skills).
- Run the project's test suite (out of scope — see Non-Goals).

---

## Workflow

### Phase 1 · Parse

Input: path to a goal file under `Docs/Goals/`.

```bash
python skills/goal-verify/scripts/parse_goal.py Docs/Goals/search/add-full-text-search.md
```

Produces a structured dict:

```json
{
  "path": "Docs/Goals/search/add-full-text-search.md",
  "title": "[Search] Add Full-Text Search",
  "frontmatter": {"status": "in-progress", "priority": "high", ...},
  "sections": {"Objective": "...", "Context": "...", "Constraints": "...", "Notes": "..."},
  "acceptance_criteria": [
    {"text": "GET /api/search?q=<term> returns ...", "checked": false, "line_no": 23},
    ...
  ],
  "warnings": []
}
```

Surface `warnings` to the user if any appear (missing frontmatter keys,
invalid status, zero checkboxes).

### Phase 2 · Verify

For each criterion, the verifier:

1. Extracts candidate **paths**, **code spans** (`` `foo` ``), **quoted
   literals**, **symbols** (CamelCase or `snake_case` identifiers), and
   fallback **keywords**.
2. Checks path existence inside the repo.
3. Searches source via `rg` (falls back to `grep -rn`).
4. Scans `tests/`, `test/`, `__tests__/` for files mentioning any symbol.
5. Emits a verdict:

| Verdict | When |
|---------|------|
| `✅ Met` | Criterion is `- [x]` **OR** (code hit(s) **AND** test file(s)) |
| `⚠️ Partial` | Code/path evidence exists but tests are missing or paths are partially absent |
| `❌ Unmet` | No referenced path exists, or no code/test evidence at all |

### Phase 3 · Report

```bash
python skills/goal-verify/scripts/run_tests.py \
    Docs/Goals/search/add-full-text-search.md \
    --root . \
    --mode quick
```

Writes `Docs/Goals/search/add-full-text-search-test.md` with:

- YAML frontmatter (`kind: test-report`, `pass_rate`, `test_coverage`, …)
- Echoed **Objective**
- **Criteria Matrix** (one row per criterion)
- **Summary** (counts + pass rate + test coverage)
- **Test Results** (per-criterion detail with evidence)
- **Recommendations** (one bullet per gap)

See `references/test-template.md` for a filled example.

### Mode selection

- `--mode quick` (default for ≤5 criteria): concise evidence, first 2
  code hits per criterion.
- `--mode deep` (default for ≥10 criteria): full evidence, up to 5 code
  hits per criterion, richer recommendations.

If omitted, mode is inferred from criteria count.

---

## End-to-End Example

Goal file (`Docs/Goals/auth/add-jwt-auth.md`):

```markdown
---
status: in-progress
priority: high
created: 2026-04-15
updated: 2026-04-19
depends_on: []
---

# [Auth] Add JWT Authentication

## Objective
Protect API routes with stateless JWT auth.

## Acceptance Criteria
- [x] `POST /api/auth/login` returns `{token}` on valid credentials
- [x] Middleware `requireAuth` rejects requests without a valid token with `401`
- [ ] Tokens expire after 24h
- [ ] Documented in `docs/auth.md`
```

Run:

```bash
python skills/goal-verify/scripts/run_tests.py Docs/Goals/auth/add-jwt-auth.md
```

Output (excerpt):

```
✓ report: Docs/Goals/auth/add-jwt-auth-test.md
  2 met · 1 partial · 1 unmet · 4 total
```

The generated report includes:

```markdown
## Criteria Matrix

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | `POST /api/auth/login` returns `{token}` on valid credentials | ✅ Met | `src/routes/auth.ts:14`, test: `tests/auth.test.ts` |
| 2 | Middleware `requireAuth` rejects requests without a valid token with `401` | ✅ Met | `src/middleware/requireAuth.ts:9`, test: `tests/middleware.test.ts` |
| 3 | Tokens expire after 24h | ⚠️ Partial | `src/routes/auth.ts:22` (no matching tests) |
| 4 | Documented in `docs/auth.md` | ❌ Unmet | referenced path(s) missing: `['docs/auth.md']` |
```

---

## Integration With the Pipeline

| Upstream skill | What it produces | goal-verify reads |
|----------------|------------------|-----------------|
| `goal-create` | `Docs/Goals/<feature>/<task>.md` with frontmatter + criteria | goal file |
| `goal-execute` | Commits that implement those criteria | the repo state |

| Downstream skill | What it produces | goal-verify provides |
|------------------|------------------|--------------------|
| `goal-improve` | Goal critique and rewritten goal criteria | ambiguous or low-quality criteria |

**Typical flow:**

1. `goal-create` creates `Docs/Goals/search/add-full-text-search.md`.
2. `goal-execute` lands commits on a feature branch.
3. `goal-verify` writes `Docs/Goals/search/add-full-text-search-test.md`.
4. If any `❌`/`⚠️` comes from implementation gaps, run `goal-execute` again with the concrete findings.
5. If any `❌`/`⚠️` comes from vague, untestable, or poorly designed criteria, run `goal-improve` before another execution pass.

---

## CLI Reference

```bash
# Full pipeline
python skills/goal-verify/scripts/run_tests.py <goal.md> [--root .] [--mode quick|deep] [--out path] [--print]

# Inspect the parser output
python skills/goal-verify/scripts/parse_goal.py <goal.md>

# Inspect verification results only
python skills/goal-verify/scripts/verify_implementation.py <goal.md> [--root .]

# Render a report from pre-computed JSON
python skills/goal-verify/scripts/generate_report.py <goal.json> <results.json> <out.md> [--mode quick|deep]
```

### Exit codes (`run_tests.py`)

| Code | Meaning |
|------|---------|
| 0 | Report written, all criteria `✅ Met` |
| 1 | Report written, at least one `⚠️ Partial` or `❌ Unmet` |
| 2 | Usage or input error (missing goal file, invalid args) |
| 3 | Unexpected internal failure |

---

## Rules

1. **One goal per run.** Never batch-test multiple goals in a single
   invocation; each gets its own report for clean diffing.
2. **Report path is deterministic.** `Docs/Goals/{feature-name}/{task}.md` →
   `Docs/Goals/{feature-name}/{task}-test.md`. Never write anywhere else
   unless `--out` is explicit.
3. **One criterion at a time.** Verify each acceptance criterion independently.
   Do not merge, group, summarize, or batch criteria into a shared verdict.
4. **Never edit the goal file.** Even if a criterion is obviously
   satisfied, `goal-verify` does not mark it `- [x]`. Author attestation
   is the goal owner's job.
5. **Evidence or no evidence — never opinion.** If the verifier cannot
   find evidence, say so. Do not guess based on file names.
6. **Respect `--root`.** All path checks and searches happen under
   `--root` (default: current directory). A goal file outside the repo
   is still parsed, but searches stay inside the repo.
7. **Warn loudly on malformed goals.** Missing frontmatter keys, invalid
   `status` or `priority` values, or zero checkboxes surface as
   `warnings` in the parser output.
8. **Stdlib only.** Scripts must not import third-party packages. YAML
   frontmatter is parsed by hand; ripgrep is optional.
9. **Deterministic output.** Running `goal-verify` twice on an unchanged
   repo yields byte-identical reports, modulo the `generated` timestamp.

---

## Non-Goals

- **Running unit or integration tests.** Use the project's own runner
  (`pytest`, `npm test`, `go test`, `dotnet test`). `goal-verify` only
  *locates* test files; it does not execute them.
- **Writing new tests.** Use `flutter-test`, `unity-test-unit`, or the
  equivalent for your stack.
- **Mutating `Master.md` or checkboxes.** Handled by `goal-create` and
  `goal-improve`.
- **Code review.** Use `unity-review`, `flutter-review`, or the matching
  review skill.

---

## File Layout

```
skills/goal-verify/
├── SKILL.md                                 ← this file
├── scripts/
│   ├── run_tests.py                         ← orchestrator (entry point)
│   ├── parse_goal.py                        ← goal file parser
│   ├── verify_implementation.py             ← evidence scanner
│   └── generate_report.py                   ← Markdown renderer
└── references/
    ├── test-template.md                     ← filled example report
    └── acceptance-criteria-guide.md         ← how to write testable criteria
```

All four scripts are executable (`chmod +x`) and runnable standalone.
