# Output Template

## `{Target}` `[{type}]`

{1-2 sentences: what it is, what it does}

**{Label}** — `File.cs:L##` — {explanation}

**{Label}** — `File.cs:L##` — {explanation}

risk: `low|medium|high` {justification only if medium/high}

---

**type**: `class` | `method` | `system` | `field` | `event` | `interface` | `flow`

**Rules**:
- 1-3 details. Each = bold label + file:line + explanation.
- Refs inline. No separate section.
- Risk = single line. `low` = no justification.
- Code snippets only when they clarify.
- No narration. Just answer.
