# Skill Validation Checklist

## Structure Checklist

- [ ] `SKILL.md` exists and is < 100 lines
- [ ] YAML frontmatter has `name` and `description` fields
- [ ] `description` includes trigger phrases, no angle brackets `< >`
- [ ] All 6 sections present: When to Use, Workflow, Rules, Output Format, Reference Files (if any)
- [ ] Writing style is imperative/verb-first — no "you should"
- [ ] No TODO/TBD placeholders
- [ ] Every reference file listed in SKILL.md actually exists
- [ ] Every reference file is < 100 lines

## Mandatory SKILL.md Structure

```
---
name: skill-name
description: one-line, trigger phrases, no angle brackets
---
# skill-name

One-line summary.

## When to Use
## Workflow
## Rules
## Output Format
## Reference Files   ← omit if no refs
```

## Reference File Rules

- One topic per file — split if a file exceeds 100 lines
- Practical instructions, not documentation
- No duplication with SKILL.md content
- Cross-reference other refs/scripts when needed
- Sacrifice grammar for concision

## Progressive Disclosure Levels

| Level | What | Size |
|-------|------|------|
| 1 | Metadata (name + description) | ~100 words, always in context |
| 2 | SKILL.md body | < 100 lines, loaded on trigger |
| 3 | References & scripts | Unlimited, loaded on demand |

## Anti-Patterns to Avoid

- Inlining reference content into SKILL.md
- Creating overlapping skills — combine related topics
- Using second-person ("you should", "you must")
- Long prose paragraphs — use bullets and code blocks
- Empty `scripts/` or `assets/` directories
- Leaving example/placeholder files from `init_skill.py`
- Skill description without trigger phrases

## Quick Validate Command

```bash
python scripts/quick_validate.py skills/my-skill/
```
