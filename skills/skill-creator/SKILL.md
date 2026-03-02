---
name: skill-creator
description: Author new AI skills — SKILL.md under 100 lines, references under 100 lines, progressive disclosure. Triggers — 'create skill', 'new skill', 'skill authoring', 'build a skill', 'make a skill'.
---
# skill-creator

Create well-structured AI skills using progressive disclosure: metadata → SKILL.md body → bundled references.

## When to Use

- Building a new skill for a recurring task or domain
- Restructuring an existing skill that has grown too large
- Adding reference files to an existing skill
- Auditing a skill against the validation checklist

## Workflow

1. **Gather** — Collect 2-3 concrete usage examples from the user
2. **Scope** — Identify what belongs in SKILL.md vs. references vs. scripts
3. **Create** — Make the skill directory and `references/` subdirectory with `mkdir -p`
4. **Write** — Author `SKILL.md` using the mandatory structure (frontmatter + 6 sections)
5. **Add refs** — Write reference files for detail that exceeds SKILL.md scope
6. **Validate** — Run `quick_validate.py` or check the checklist manually

## Rules

- Keep SKILL.md under 100 lines — push detail to references
- Keep every reference file under 100 lines — split if larger
- Write in imperative form — verb-first, no "you should"
- Never inline reference content into SKILL.md
- No TODO/TBD placeholders in any file
- Combine related topics into one skill rather than creating overlapping skills
- Token budget drives everything: lean SKILL.md = faster skill loading

## Output Format

Skill directory with `SKILL.md` + zero or more files under `references/`.
Scripts go in `scripts/` only when deterministic automation is needed (include tests).

## Reference Files

- `references/skill-checklist.md` — validation checklist, mandatory structure, anti-patterns, and common mistakes

Load references on demand via `read_skill_file("skill-creator", "references/{file}")`.
