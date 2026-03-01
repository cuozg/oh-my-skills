# Output Template

Use markdown formatting — NOT a single code block. Tree connectors (`├──`, `│`, `└──`) for hierarchical sections.

## Color Legend

| Element | Format | Visual Role |
| :--- | :--- | :--- |
| Target title | `🔍 **Target** [{type}]` | **Bold** — investigation subject |
| Section labels | `**Label**` | **White bold** — structure |
| File references | `` `File.cs:L##` `` | **Cyan** — clickable targets |
| Class.Method | `` `ClassName.Method` `` | **Cyan** — code identifiers |
| Key values / states | `` `null` `` `` `true` `` `` `Awake` `` | **Cyan** — highlight data |
| Risk level | 🟢 `LOW` 🟡 `MEDIUM` 🟠 `HIGH` | Emoji + inline code |
| Flow steps | `├──` `└──` with `` `Class.Method` `` | Tree + cyan |
| Tree connectors | `├──` `│` `└──` | Structure lines |

## Template

---

🔍 **{Target}** [{type}]

> {1-2 sentences: what it is, what it does. Cite `File.cs:L##`.}

**{Label}**
├── {explanation citing `Class.Method` → `File.cs:L##`}
├── {sub-detail if needed}
└── 📄 `File.cs:L##`

**{Label}**
├── {explanation citing `Class.Method` → `File.cs:L##`}
└── 📄 `File.cs:L##`

**risk:** 🟢 `LOW` | 🟡 `MEDIUM` | 🟠 `HIGH` — {justification only if medium/high}

---

## Rules

- **type**: `class` | `method` | `system` | `field` | `event` | `interface` | `flow`
- **branches**: 1-3 detail branches. Each = bold label + explanation + file:line leaf.
- **nesting**: Nest sub-details as children for natural hierarchies (caller→callee, parent→child, owner→member).
- **risk**: Final line. 🟢 `LOW` = no justification needed.
- **Inline code** for: file refs, class names, method names, field names, values (`null`, `0`, `false`).
- **Bold** for: section labels, target title, important observations.
- **Code snippets**: Inline under the relevant branch only when it clarifies — never dump full methods.
- **Cite `File.cs:L##`** in inline code for every claim.
- **No narration** before or after the tree. Just the tree.
- **No wrapping in a single code block** — use markdown formatting for visual hierarchy.
