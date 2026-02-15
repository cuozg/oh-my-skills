---
name: skill-router
description: "Find the best matching skill(s) for a user request. Scans all installed skills, scores relevance, and returns a ranked list with explanations. Use when: (1) User is unsure which skill to use, (2) Routing a request to the right skill, (3) Discovering available skills for a domain. Triggers: 'which skill', 'find skill', 'route to skill', 'what skill should I use', 'skill for', 'help me pick a skill'."
---

# Skill Router

## Workflow

1. Read user request
2. Scan all `SKILL.md` frontmatter under `.opencode/skills/`
3. Score each skill by relevance
4. Return ranked list

## Scoring (priority order)

1. **Trigger phrase match** (highest) — request contains trigger word
2. **"Use when" case match** — matches numbered use-case
3. **Domain keyword overlap** — shared domain terms
4. **Name match** — request mentions skill name
5. **Token overlap** (lowest) — generic word overlap

## Output

```
| Rank | Skill | Why |
|------|-------|-----|
| 1 | `category/skill-name` | One-line reason |
```

- Top 5 max, skip zero-scoring skills
- Clear best → **Recommended: `skill-path`**
- Close matches → suggest `load_skills=["a", "b"]`

## Rules

- NEVER load/execute matched skills — only recommend
- One sentence per explanation
- No match → say so, suggest rephrasing
