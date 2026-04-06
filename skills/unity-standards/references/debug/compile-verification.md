# Compile Verification

Patterns for verifying Unity C# compilation — log parsing, error formats, and verification chain.

## Verification Chain

Use the fastest tool that covers your scope:

| Tool | Speed | Scope | When to Use |
|------|-------|-------|-------------|
| `lsp_diagnostics` | Instant | Single-file type/syntax | After every edit |
| Unity MCP `ReadConsole` | Fast | Running Editor state | When Editor is open |
| Unity MCP `GetConsoleLogs` | Fast | All console output | Quick error scan |
| Batchmode compile check | 30s-5m | Full project compile | MCP unavailable, CI, cross-assembly |

**Escalation path:** `lsp_diagnostics` → Unity MCP → batchmode compile check

## When lsp_diagnostics Is Not Enough

- Cross-assembly reference errors (asmdef boundaries)
- Unity-specific compilation contexts (editor-only code, platform defines)
- Script import errors (only surface during domain reload)
- Package version conflicts and assembly resolution failures
- Preprocessor directive issues (`#if UNITY_EDITOR`, `#if UNITY_WEBGL`)
- After bulk changes: package updates, asmdef restructuring, namespace renames

## Unity Error Line Format

Unity uses this regex to parse compiler output (from `MicrosoftCSharpCompilerOutputParser.cs` in UnityCsReference):

```regex
(?P<filename>.+)\((?P<line>\d+),(?P<column>\d+)\):\s*(?P<type>warning|error|info)\s*(?P<id>[^:]*):\s*(?P<message>.*)
```

Example log lines:
```
Assets/Scripts/Player.cs(42,10): error CS0246: The type or namespace name 'Foo' could not be found
Assets/Scripts/Old.cs(10,5): warning CS0618: 'Thing' is obsolete
```

Named groups: `filename`, `line`, `column`, `type` (error|warning|info), `id` (CS####), `message`

## Log Section Markers

```
-----CompilerOutput:-stderr----------
<errors appear here>
-----EndCompilerOutput---------------
```

```
DisplayProgressNotification: Scripts have compiler errors.
```

```
- Finished compile Library/ScriptAssemblies/Assembly-CSharp.dll
```

## Common Compile Error Codes

| Code | Description | Common Fix |
|------|------------|------------|
| CS0246 | Type/namespace not found | Missing `using`, asmdef reference, or deleted class |
| CS0103 | Name does not exist in scope | Typo, wrong scope, missing variable |
| CS0029 | Cannot implicitly convert type | Type mismatch — add cast or fix assignment |
| CS1061 | Type does not contain a definition | Wrong type, missing method, API change |
| CS0234 | Namespace does not exist | Missing package or asmdef dependency |
| CS0117 | Does not contain a definition for member | Static member access on wrong type |
| CS0619 | Member is obsolete and will error | Use the replacement API suggested in message |
| CS0618 | Member is obsolete (warning) | Use replacement API or suppress with `#pragma` if justified |
| CS0168 | Variable declared but never used | Remove unused variable or prefix with `_` |

## Additional Error Patterns

Beyond CS#### compiler errors, also check for:

```
Failed to import script <path>           — Script import failure (encoding, syntax)
Assembly <X> has reference to <Y> which is not included — asmdef dependency missing
Shader error in '<name>': <message>      — Shader compilation failure
```

## Exit Code Caveat

Exit code 0 from Unity batchmode does NOT guarantee zero errors. Always parse the log file as well. Unity exits 0 when:
- `-ignorecompilererrors` is set
- `-executeMethod` catches all exceptions without calling `EditorApplication.Exit(1)`
- `BuildPipeline.BuildPlayer` fails but the calling method doesn't re-throw

Belt-and-suspenders check:
```bash
[ $exit_code -ne 0 ] || grep -qE "error CS|error IL|Scripts have compiler errors" log.txt
```
