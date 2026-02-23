# Output Template

Every response from this skill uses this exact tree structure. No alternative formats.

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

## Fields

- **type**: `class` | `method` | `system` | `field` | `event` | `interface` | `flow`
- **branches**: 1-3 detail branches. Each = label + explanation + file:line leaf.
- **nesting**: Nest sub-details as children for natural hierarchies (caller→callee, parent→child, owner→member).
- **risk**: Final leaf. `low` = no justification needed.
- **code**: Inline under the relevant branch only when it clarifies.
- **narration**: None. No preamble, no summary after. Just the tree.
