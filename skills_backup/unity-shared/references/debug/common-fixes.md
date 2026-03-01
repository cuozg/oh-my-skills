# Common Unity Error Fixes

Quick-reference for known error patterns. Match error type → apply standard fix approach.

## Error → Fix Table

| Error | Typical Fix |
| :--- | :--- |
| `NullReferenceException` | Add null guard, verify serialized reference in Inspector, check `GetComponent` return |
| `MissingReferenceException` | Object was destroyed — check `this == null` after `await`, use `TryGetComponent` |
| `IndexOutOfRangeException` | Validate array/list bounds before access, check `Count`/`Length` |
| `InvalidOperationException` | Collection modified during enumeration — copy to temp list, or use reverse iteration |
| `StackOverflowException` | Recursive call without base case — check property setter calling itself |
| `ArgumentNullException` | Validate parameters at method entry, add early returns |
| Race Condition / Timing | Verify `async`/`await` order, use `UniTask.WhenAll`, check lifecycle state |
| `CS0246` Type not found | Missing `using` directive, assembly definition reference, or package not installed |
| `CS0103` Name not found | Variable not in scope — check spelling, scope boundaries, `static` context |
| `CS0029` Cannot convert | Type mismatch — add cast, use correct generic parameter, check nullable |

## Assembly / Package Errors

- **asmdef conflict**: Check `Assembly-CSharp.asmdef` references, ensure no circular refs
- **Package import error**: `Window > Package Manager > Remove + Reimport`, check `manifest.json`
- **Missing namespace**: Add assembly reference in `.asmdef` file, or add `using` directive

## Serialization Errors

- **Missing script on prefab**: GUID mismatch — find `.cs.meta` GUID, match to prefab YAML `m_Script`
- **Serialization depth limit**: Break circular SO references, use ID-based lookups instead of direct refs
- **Type mismatch on deserialize**: Field type changed — add `[FormerlySerializedAs]` or migration script

## Build Failures

- **IL2CPP errors**: Check reflection usage, add `[Preserve]` attribute, review `link.xml`
- **Shader compilation**: Check platform-specific keywords, `#pragma` directives
- **Scene not in build**: `File > Build Settings > Add Open Scenes`

## Investigation Priority

1. **Stack Trace First**: Top of trace = immediate trigger, bottom = origin
2. **Clean Slate**: Clear console, reproduce — transient errors may self-resolve
3. **Isolate**: Reproduce in empty scene if systemic
4. **Evidence-Based**: Only declare fixed if error no longer appears after repro steps

## Safety

- **Backup before destructive fixes** — user confirmation for scene/prefab modifications
- **Fix ONLY the reported error** — no refactoring beyond fix scope
- **Verify after every fix** — `lsp_diagnostics` on changed files, then repro steps
