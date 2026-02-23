# Output Template

```
{Target} [{type}]
│
│ {1-2 sentences: what it is, what it does}
│
├── {Label}
│   {explanation}
│   └── 📄 File.cs:L##
│
├── {Label}
│   {explanation}
│   └── 📄 File.cs:L##
│
└── risk: {low|medium|high} {justification only if medium/high}
```

---

**type**: `class` | `method` | `system` | `field` | `event` | `interface` | `flow`

**Rules**:
- 1-3 detail branches. Each = label + explanation + file:line leaf.
- Nest sub-details as children when there's a natural hierarchy (caller→callee, parent→child, owner→member).
- Risk = final leaf. `low` = no justification.
- Code snippets only when they clarify — inline under the relevant branch.
- No narration. Just the tree.
