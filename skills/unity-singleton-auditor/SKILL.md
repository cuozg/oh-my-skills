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

**Input**: Optional: directory to audit (default `Assets/Scripts/`), focus area (`dependencies`/`null-checks`/`init-order`/`all`).

**Output**: Audit report — singleton registry, dependency graph, circular dependencies, unsafe access points, anti-patterns, prioritized fixes. Saved to `Documents/Audits/SINGLETON_AUDIT_[YYYYMMDD].md`.

## Workflow

1. **Discover**: Run `python3 .opencode/skills/unity/unity-singleton-auditor/scripts/audit_singletons.py Assets/Scripts/` → JSON with all Singleton declarations and `.Instance` access points
2. **Analyze Dependencies**: Build directed graph (A→B = A accesses B.Instance), detect cycles via DFS, flag 5+ dependency coupling, flag Awake-time cross-access
3. **Pattern Audit**: Check each Singleton against audit table below
4. **Report**: Generate markdown report with summary, registry, cycles (Mermaid graph), unsafe access list, recommendations

## Pattern Audit Checks

| Check | What To Look For | Severity |
|:---|:---|:---|
| Null-check before Instance | Missing `if (X.Instance != null)` or `HasInstance` | High |
| Circular dependency | A.Instance in B, B.Instance in A | Critical |
| Awake-time access | Singleton.Instance in another Singleton's Awake() | High |
| Excessive coupling | References 5+ other Singletons | Medium |
| Public mutable fields | `public` non-readonly fields | Medium |
| Missing base.Awake() | Override Awake without calling base | High |
| Non-manager Singleton | Doesn't manage state/resources but uses Singleton | Low |

## Best Practices

- Run audit before major refactors — know the dependency landscape first
- Focus on Critical/High severity — Low items are informational
- Use `lsp_find_references` to verify audit script findings
- Don't refactor during audit — create follow-up tasks for fixes
