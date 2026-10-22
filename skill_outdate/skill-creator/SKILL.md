---
name: skill-creator
description: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.
---

# Skill Creator

Create and iteratively improve skills. Core loop: Draft → Test → Evaluate → Improve → Repeat.

## Skill Structure

```
skill-name/
├── SKILL.md          (required: YAML frontmatter + markdown instructions)
└── Bundled Resources (optional)
    ├── scripts/      Executable code for deterministic/repetitive tasks
    ├── references/   Docs loaded into context as needed
    └── assets/       Templates, icons, fonts
```

**SKILL.md targets:** Under 500 lines (ideal). Put detail in `references/`. YAML requires `name` + `description`.

**Description field:** Primary trigger mechanism. Make it "pushy" — list specific contexts and phrases that should trigger the skill. Agents tend to under-trigger; compensate with explicit use-case coverage.

## Workflow

### 1. Capture Intent
Extract from conversation: tools used, steps, corrections, input/output formats. Ask only what's missing:
- What should this skill enable?
- When should it trigger? (phrases, contexts)
- What's the expected output format?
- Are test cases needed? (yes for verifiable outputs; often no for subjective tasks)

### 2. Interview & Research
Ask about edge cases, input/output formats, success criteria, dependencies. Check available MCPs. Research in parallel via subagents when useful.

### 3. Write SKILL.md
Write draft, then review with fresh eyes. Prefer imperative form. Explain the **why** — smart agents follow reasoning over mandates. Avoid ALL-CAPS MUST whenever possible. Keep lean.

### 4. Create Test Cases
2–3 realistic prompts a real user would type. Save to `evals/evals.json`:
```json
{"skill_name": "example", "evals": [{"id": 1, "prompt": "...", "expected_output": "..."}]}
```

### 5. Run & Evaluate
See `agents/` for spawning test runs, grading, benchmarking, and launching the viewer:
- **Spawn runs** — one with-skill + one baseline per test case, all in same turn (with-skill AND baseline, never sequential)
- **Draft assertions** while runs are in progress
- **Grade** via `agents/grader.md`; **aggregate** via `scripts/aggregate_benchmark`
- **Launch viewer**: `nohup python eval-viewer/generate_review.py <workspace>/iteration-N --skill-name "name" --benchmark <workspace>/iteration-N/benchmark.json > /dev/null 2>&1 &`
- **Read feedback** from `feedback.json` after user reviews. Kill server after: `kill $VIEWER_PID`

### 6. Improve
Generalize from feedback → lean prompt → explain why → bundle repeated work (if all 3 test cases wrote `create_chart.py`, put it in `scripts/`). Iterate: improve → rerun in `iteration-N+1/` → viewer with `--previous-workspace` → repeat.

### 7. Optimize Description (Optional)
After skill is done:
```bash
python -m scripts.run_loop --eval-set <path> --skill-path <path> --model <model-id> --max-iterations 5 --verbose
```
Generates 20 eval queries (10 should-trigger, 10 should-not-trigger). Review via `assets/eval_review.html`. Apply `best_description` to SKILL.md frontmatter.

## Writing Principles

1. **Generalize** — rules preventing a class of problem, not just this example
2. **Keep lean** — remove instructions not pulling their weight
3. **Explain why** — `"Read X before Y — prevents overwriting state"` beats `"ALWAYS read X"`
4. **Bundle repeated work** — if multiple test runs independently wrote the same script, bundle it

## Environment Notes

- **Claude Code:** Full workflow — subagents, viewer server, description optimization
- **Claude.ai:** Run tests inline, present results in conversation, skip benchmarks and description optimization
- **Cowork:** Use `--static <output_path>` for viewer (no display), feedback via downloaded `feedback.json`
- **Updating existing skill:** Preserve original directory name + `name` frontmatter. Copy to writable location before editing if installed path is read-only.

## Reference Files

- `agents/grader.md` — grading assertions against outputs
- `agents/comparator.md` — blind A/B comparison
- `agents/analyzer.md` — analyzing why one version won + benchmark patterns
- `references/schemas.md` — JSON schemas for evals.json, grading.json, benchmark.json
