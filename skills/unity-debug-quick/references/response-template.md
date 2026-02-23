# Response Template

Use markdown formatting — NOT a single code block. Tree connectors (`├──`, `│`, `└──`) for hierarchical sections.

## Color Legend (Vercel Theme)

| Element | Format | Visual Role |
| :--- | :--- | :--- |
| Issue title | `🔴 **Title**` | **Red bold** — primary alert |
| Section headers | `**root cause**`, `**solutions**` | **White bold** — structure |
| Severity | 🔴 `CRITICAL` 🟠 `HIGH` 🟡 `MEDIUM` ⚪ `LOW` | Emoji + inline code |
| File references | `` `File.cs:L##` `` | **Cyan** — clickable targets |
| Class.Method | `` `ClassName.Method` `` | **Cyan** — code identifiers |
| Key values / states | `` `null` `` `` `false` `` `` `destroyed` `` | **Cyan** — highlight data |
| Failure point | `⛔` + **bold text** | **Red** — crash site |
| Observation / symptom | `👁️` + *italic* | Visual marker |
| Recommended solution | `✅ **Title** [RECOMMENDED]` | **Green bold** |
| Other solutions | `◻️ **Title**` | **Dim bold** |
| Effort tags | `› SMALL` `› MEDIUM` `› LARGE` | Gray chevron |
| Workaround | `⚠️ **workaround:**` | **Yellow** — caution |
| Labels | `**approach:**` `**where:**` | **Bold** inline |
| Tree connectors | `├──` `│` `└──` | Structure lines |

## Template

---

🔴 **{Issue Title}**

> {1-2 sentences: what is wrong, where, what the user observes. Cite `File.cs:L##`.}

**impact**
├── {AffectedSystem} — {how it is affected}
├── {AffectedSystem} — {how it is affected}
└── **severity:** 🔴 `CRITICAL` | 🟠 `HIGH` | 🟡 `MEDIUM` | ⚪ `LOW` — {justification}

**root cause**

> {2-4 sentences: WHY it happens — trace to origin. Every claim cites `File.cs:L##`.}

  **flow**
  ├── `Class.Method` → `File.cs:L##` — {what happens}
  ├── `Class.Method` → `File.cs:L##` — {what happens}
  ├── `Class.Method` → `File.cs:L##` — {what happens}
  └── ⛔ `Class.Method` → `File.cs:L##` — **{failure point}**

  **repro**
  ├── {concrete step}
  ├── {concrete step}
  └── 👁️ *{observable symptom}*

**solutions**

  ✅ **{Title}** [RECOMMENDED]
  ├── **approach:** {1-2 sentences}
  ├── **where:** `File.cs:L##` — `Method`
  ├── **trade-off:** {pros and cons}
  └── › SMALL | MEDIUM | LARGE

  ◻️ **{Title}**
  ├── **approach:** {1-2 sentences}
  ├── **where:** `File.cs:L##` — `Method`
  ├── **trade-off:** {pros and cons}
  └── › SMALL | MEDIUM | LARGE

  ⚠️ **workaround:** {temporary bypass, or "none — root cause must be fixed"}

**verify**
├── {apply solution}
├── {trigger the scenario}
└── {confirm expected behavior}

**prevent**
├── {actionable practice}
└── {actionable practice}

**🔧 Which solution should I apply?**

> Pick a number (or type `skip` to move on, `stop` to end):
>
> 1️⃣ {Solution 1 Title} [RECOMMENDED]
> 2️⃣ {Solution 2 Title}
> 3️⃣ {Solution 3 Title} *(if applicable)*

---

## Rules

- **Minimum 2 solutions**, maximum 4. Mark exactly one `✅ [RECOMMENDED]`.
- **Cite `File.cs:L##`** in inline code for every claim — root cause, flow, solution `where`.
- **Flow tree**: 2-8 nodes from trigger to ⛔ failure. Use `├──` / `└──` connectors. Last node = ⛔.
- **Repro tree**: concrete steps, last node = 👁️ observable symptom.
- **Verify tree**: minimum 2 nodes confirming the fix works.
- **Prevent tree**: 1-3 actionable practices, not generic advice.
- **Inline code** for: file refs, class names, method names, field names, values (`null`, `0`, `false`).
- **Bold** for: failure descriptions, section labels, solution titles.
- **No narration** before or after the tree — except the interactive prompt at the end.
- **No wrapping in a single code block** — use markdown formatting for visual hierarchy.
- Solutions describe approach and location — no code in the tree. Code changes happen during fix delegation.
- Severity uses emoji + inline code: 🔴 `CRITICAL`, 🟠 `HIGH`, 🟡 `MEDIUM`, ⚪ `LOW`.
- **Interactive prompt is MANDATORY** — always end with the numbered choice prompt.
- User says `skip` → ask if there is another issue to investigate.
- User says `stop` → end the session.
