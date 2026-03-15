# Code Scan Patterns for Performance Audit

Grep/AST patterns to find hot-path anti-patterns in Unity C# files.

## Critical — GC Allocations in Update-Family Methods

### Pattern: LINQ in hot paths
```
grep: \.(Where|Select|OrderBy|GroupBy|ToList|ToArray|First|Last|Any|All|Count\(|Sum|Min|Max|Aggregate)\(
context: Check if inside Update/FixedUpdate/LateUpdate
```

### Pattern: String concatenation in hot paths
```
grep: \.text\s*=.*\+.*\.ToString\(\)
grep: Debug\.Log\(.*\+
```

### Pattern: new collection in hot paths
```
grep: new\s+(List|Dictionary|HashSet|Queue|Stack)<
context: Inside Update/FixedUpdate/LateUpdate = critical
```

### Pattern: Boxing
```
grep: string\.Format\(
grep: \(object\)\s*\w+
```

## Critical — Expensive API Calls Per Frame

### Pattern: FindObjectOfType in Update
```
grep: FindObjectOfType|FindObjectsOfType|FindFirstObjectByType|FindAnyObjectByType
context: Fatal if inside Update/FixedUpdate/LateUpdate
```

### Pattern: GetComponent in Update
```
grep: GetComponent<|GetComponent\(|GetComponentInChildren|GetComponentsInChildren
context: Should be cached in Awake/Start
```

### Pattern: GameObject.Find in Update
```
grep: GameObject\.Find\(|GameObject\.FindWithTag\(|GameObject\.FindGameObjectsWithTag\(
context: Should be cached or injected
```

### Pattern: Resources.Load per frame
```
grep: Resources\.Load
context: Should be loaded at init and cached
```

## Warning — Inefficient Patterns

### Pattern: Unsealed MonoBehaviour
```
grep: class\s+\w+\s*:\s*MonoBehaviour
negative: sealed\s+class
note: Non-inherited MBs should be sealed for devirtualization
```

### Pattern: Camera.main in Update (pre-2020.2)
```
grep: Camera\.main
context: Cached since 2020.2 but verify Unity version
```

### Pattern: SendMessage
```
grep: SendMessage\(|BroadcastMessage\(
note: Uses reflection — replace with direct calls or interfaces
```

### Pattern: Allocating coroutine yields
```
grep: new\s+WaitForSeconds|new\s+WaitForEndOfFrame|new\s+WaitForFixedUpdate
note: Cache as static readonly fields
```

## Info — Optimization Opportunities

### Pattern: Material property access
```
grep: \.material\b(?!s)
note: Creates material instance — use sharedMaterial for read, MaterialPropertyBlock for write
```

### Pattern: Transform access in loops
```
grep: \.transform\.position|\.transform\.rotation
context: Inside loops — cache transform reference
```

### Pattern: Missing NonAlloc physics
```
grep: Physics\.(Raycast(?!NonAlloc)|SphereCast(?!NonAlloc)|OverlapSphere(?!NonAlloc)|BoxCast(?!NonAlloc))All
note: Replace with NonAlloc variants
```

## Scan Execution Order

1. **Critical first** — LINQ, FindObjectOfType, GetComponent in Update
2. **Warning** — unsealed MBs, SendMessage, allocating yields
3. **Info** — material access, transform caching, NonAlloc

For each finding: file path, line number, severity, specific fix recommendation.
