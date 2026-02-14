---
description: 'Audit Unity Singleton usage across C# scripts. Detect MonoBehaviour
  initialization order risks, circular dependencies, missing null-checks, and Singleton
  anti-patterns in Unity projects. Use when: (1) Reviewing Singleton health in Unity
  codebase, (2) Detecting circular Singleton dependencies, (3) Finding unsafe Instance
  access without null-checks, (4) Auditing Unity startup sequence and Awake/Start
  order, (5) Identifying Singletons that should be ScriptableObjects or plain classes.
  Triggers: ''audit singletons'', ''singleton health'', ''singleton dependencies'',
  ''check singleton usage'', ''Unity initialization order'', ''MonoBehaviour singleton'',
  ''singleton pattern review''.'
name: unity-singleton-auditor
---

# Unity Singleton Auditor

Audit `Singleton<T>` usage across Unity C# codebases — detect circular dependencies, unsafe access patterns, initialization order risks, and anti-pattern violations.

## Purpose

Large Unity projects (like WWE Champions with 100+ singletons) accumulate Singleton usage that becomes hard to reason about. This skill systematically audits all Singleton classes and their consumers to surface risks before they become runtime bugs.

## Input

- **Optional**: Specific directory to audit (defaults to `Assets/Scripts/`)
- **Optional**: Focus area — `dependencies`, `null-checks`, `init-order`, or `all` (default: `all`)

## Output

An audit report documenting:
1. **Singleton Registry** — all classes extending `Singleton<T>` with file locations
2. **Dependency Graph** — which Singletons reference which other Singletons
3. **Circular Dependencies** — any A→B→A cycles detected
4. **Unsafe Access** — `Instance` usage without null/`HasInstance` checks
5. **Anti-Patterns** — Singletons with mutable public state, missing `Awake()` calls, etc.
6. **Recommendations** — prioritized list of fixes

## Examples

| User Request | Skill Action |
|:---|:---|
| "Audit singletons in the project" | Run full audit — registry, deps, cycles, unsafe access, anti-patterns |
| "Check singleton dependencies" | Focus on dependency graph and circular dependency detection |
| "Find unsafe singleton access" | Scan for `.Instance.` usage without null-checks |
| "What's the singleton initialization order?" | Trace Awake/Start order and flag ordering risks |

## Workflow

### Phase 1: Discovery

1. Run the audit script to collect raw data:
   ```bash
   python3 .opencode/skills/unity/unity-singleton-auditor/scripts/audit_singletons.py Assets/Scripts/
   ```
2. The script outputs JSON with:
   - All Singleton class declarations
   - All `.Instance` access points per file
   - Cross-reference matrix

### Phase 2: Dependency Analysis

1. Build a directed graph: Singleton A → Singleton B (A accesses B.Instance)
2. Detect cycles using DFS cycle detection
3. Flag any Singleton that accesses 5+ other Singletons (coupling smell)
4. Flag any Singleton accessed in `Awake()` of another Singleton (init-order risk)

### Phase 3: Pattern Audit

Check each Singleton for:

| Check | What To Look For | Severity |
|:---|:---|:---|
| Null-check before Instance | `if (X.Instance != null)` or `if (X.HasInstance)` missing | High |
| Circular dependency | A.Instance used in B, B.Instance used in A | Critical |
| Awake-time access | Singleton.Instance in another Singleton's Awake() | High |
| Excessive coupling | Singleton references 5+ other Singletons | Medium |
| Public mutable fields | `public` non-readonly fields on Singleton | Medium |
| Missing base.Awake() | Override Awake without calling base.Awake() | High |
| Non-manager Singleton | Class doesn't manage state/resources but uses Singleton | Low |

### Phase 4: Report Generation

Generate a markdown report with:

```markdown
# Singleton Audit Report — [Project Name]
## Date: YYYY-MM-DD

### Summary
- Total Singletons: N
- Circular Dependencies: N
- Unsafe Access Points: N
- Anti-Patterns Found: N

### Singleton Registry
| Class | File | Dependencies | Dependents |

### Circular Dependencies
[Mermaid graph showing cycles]

### Unsafe Access (Top Priority)
[List of files with unsafe .Instance access]

### Recommendations
1. [Prioritized fixes]
```

Save to: `Documents/Audits/SINGLETON_AUDIT_[YYYYMMDD].md`

## Best Practices

1. **Run audit before major refactors** — know the dependency landscape first
2. **Focus on Critical/High severity** — Low severity items are informational
3. **Use LSP tools to verify** — `lsp_find_references` confirms audit script findings
4. **Check startup scene** — `GearStartupScene` Awake order matters most
5. **Don't refactor during audit** — audit is read-only; create follow-up tasks for fixes

## MCP Tools Integration

- `lsp_find_references` — verify dependency connections found by script
- `lsp_goto_definition` — trace Singleton base class hierarchy
- `lsp_symbols` — find all classes inheriting from Singleton
- `ast_grep_search` — pattern-match `Singleton<$T>` declarations
- `grep` — find `.Instance` access patterns across codebase
