# Skill Authoring Rules

## Structure

```
skill-name/
├── SKILL.md          ← required, < 100 lines
├── scripts/          ← deterministic code, must have tests
├── references/       ← on-demand docs, < 100 lines each
└── assets/           ← templates/images, never loaded into context
```

## SKILL.md Requirements

- **< 100 lines** — hard limit
- YAML frontmatter: `name` (required), `description` (required)
- Name: hyphen-case (lowercase letters, digits, hyphens only)
- Description: no angle brackets (`<` or `>`)
- Description: specific about WHAT + WHEN to use
- Writing style: imperative/infinitive (verb-first)
- Reference bundled resources — don't inline their content

## Reference Files

- Each file < 100 lines — split if larger
- Practical instructions, not documentation
- Can cross-reference other refs/scripts
- Loaded on-demand via `read_skill_file`

## Scripts

- Prefer Python/Node over Bash (cross-platform)
- MUST have tests — run until green
- Include `requirements.txt` for Python
- No line limit, but must compile and run cleanly

## Progressive Disclosure

| Level | Content              | When Loaded         | Budget    |
|-------|----------------------|---------------------|-----------|
| 1     | Name + description   | Always in context   | ~100 words|
| 2     | SKILL.md body        | On skill trigger    | < 5k words|
| 3     | Refs/scripts/assets  | On-demand           | Unlimited |

## Anti-Patterns

- Long prose in SKILL.md — keep terse
- Inlining reference content into SKILL.md
- Skipping tests for scripts
- Using bash when Python/Node works
- Leaving placeholder files from init
- Creating overlapping skills — combine related topics
- Writing "you should" — use imperative form
- Duplicating content between SKILL.md and references
