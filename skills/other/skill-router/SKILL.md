---
name: skill-router
description: "Find the best matching skill(s) for a user request. Scans all installed skills, scores relevance, and returns a ranked list with explanations. Use when: (1) User is unsure which skill to use, (2) Routing a request to the right skill, (3) Discovering available skills for a domain. Triggers: 'which skill', 'find skill', 'route to skill', 'what skill should I use', 'skill for', 'help me pick a skill'."
---

# Skill Router

Match user requests to the best available skill(s).

## Workflow

1. Read user request
2. Scan all `SKILL.md` frontmatter under `.opencode/skills/`
3. Score each skill by relevance (triggers, use-cases, keyword overlap)
4. Return ranked list with explanations

## Scoring

Score skills against the user request using these signals (highest priority first):

| Signal | Weight | Example |
|--------|--------|---------|
| Trigger phrase match | Highest | Request contains `'refactor'` → `unity-refactor` |
| "Use when" case match | High | Request matches a numbered use-case in description |
| Domain keyword overlap | Medium | Request has `'shader'`, skill mentions `'shader'` |
| Name match | Medium | Request mentions skill name directly |
| Token overlap | Low | Generic word overlap between request and description |

## Output Format

Return a markdown table sorted by relevance:

```
| Rank | Skill | Why |
|------|-------|-----|
| 1 | `category/skill-name` | One-line reason this skill matches |
| 2 | `category/skill-name` | One-line reason |
| ... | ... | ... |
```

- Show top 5 matches max
- Skip skills scoring zero
- If one skill is clearly best, say so: **Recommended: `skill-path`**
- If multiple skills are close, note they can be combined: `load_skills=["a", "b"]`

## Rules

- NEVER load or execute the matched skills — only recommend them
- Keep explanations to one sentence each
- If no skill matches, say so and suggest the user describe their task differently
