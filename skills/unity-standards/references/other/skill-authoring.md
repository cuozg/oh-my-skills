# Skill Authoring Rules

## Structure

```
skill-name/
+-- SKILL.md          <- required, compact router
+-- scripts/          <- deterministic code, must have tests
+-- references/       <- on-demand docs, split by task surface
+-- assets/           <- templates/images, never loaded into context
```

## SKILL.md Requirements

- Keep SKILL.md short enough to route quickly; move details into references
- YAML frontmatter: `name` (required), `description` (required)
- Name: hyphen-case (lowercase letters, digits, hyphens only)
- Description: no angle brackets (`<` or `>`)
- Description: specific about WHAT + WHEN to use
- Writing style: imperative/infinitive (verb-first)
- Reference bundled resources - don't inline their content

## Reference Files

- Keep each reference focused; split when a file covers unrelated task surfaces
- Practical instructions, not documentation
- Can cross-reference other refs/scripts
- Loaded on demand only when the current task needs that surface

## Scripts

- Prefer Python/Node over Bash (cross-platform)
- MUST have tests - run until green
- Include `requirements.txt` for Python
- No line limit, but must compile and run cleanly

## Progressive Disclosure

| Level | Content              | When Loaded         | Budget    |
|-------|----------------------|---------------------|-----------|
| 1     | Name + description   | Always in context   | ~100 words|
| 2     | SKILL.md body        | On skill trigger    | < 5k words|
| 3     | Refs/scripts/assets  | On-demand           | Unlimited |

## Anti-Patterns

- Long prose in SKILL.md - keep terse
- Inlining reference content into SKILL.md
- Skipping tests for scripts
- Using bash when Python/Node works
- Leaving placeholder files from init
- Creating overlapping skills - combine related topics
- Writing "you should" - use imperative form
- Duplicating content between SKILL.md and references
