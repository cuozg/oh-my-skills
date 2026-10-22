# Compile Verification

Patterns for verifying Unity C# compilation - verification chain, log parsing, and
error formats. Editor access rules and preflight: `references/other/unity-cli-routing.md`.

## Verification Chain

Use the fastest step that covers your scope; escalate when it cannot.

| Step | How | Scope | When to Use |
|------|-----|-------|-------------|
| 0. IDE diagnostics | Editor integration (e.g. VS Code C# Dev Kit, Rider) problems list | Single-file type/syntax | Fast check after each edit; never final proof |
| 1. Live Editor | `unity status --format json` (state `ready`) → `unity command recompile --caller plugin --skill <skill>` → scan errors with the console/log command `unity command --query log` lists | Full project as the Editor compiles it | GUI or batch Editor reachable |
| 2. Safe Mode check | `unity pipeline list --format json` → `data.summary.instancesInSafeMode > 0` → `grep` `<project>/Logs/Editor.log` | Errors that blocked Editor startup | Editor open but CLI cannot connect |
| 3. Headless | `unity run <project> -- -logFile <path>`, or `unity test <project> --mode EditMode --format json` | Full project compile (plus tests) | No live Editor, CI, cross-assembly changes |

Rules:
- Run `unity command --format json` first; use only commands this Editor lists.
- Headless runs need the project closed in the GUI Editor.
- Never pass `-batchmode` / `-quit` to `unity run` / `unity test` / `unity build`.
- Read logs through `grep`, never dump them whole.

```bash
# Log scan (Safe Mode or headless): CS errors plus the global failure marker
grep -nE 'error CS[0-9]{4}|Scripts have compiler errors' <project>/Logs/Editor.log   # headless: the -logFile path
```

## When IDE Diagnostics Are Not Enough

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

Primary signal is the `error CS####` lines above. These markers may also appear
(exact text varies by Unity version):

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
| CS0029 | Cannot implicitly convert type | Type mismatch - add cast or fix assignment |
| CS1061 | Type does not contain a definition | Wrong type, missing method, API change |
| CS0234 | Namespace does not exist | Missing package or asmdef dependency |
| CS0117 | Does not contain a definition for member | Static member access on wrong type |
| CS0619 | Member is obsolete and will error | Use the replacement API suggested in message (see `references/quality/best-practices-audit.md`) |
| CS0618 | Member is obsolete (warning) | Use replacement API or suppress with `#pragma` if justified |
| CS0168 | Variable declared but never used | Remove the variable; for `catch (Exception e)` drop `e` |

## Additional Error Patterns

Beyond CS#### compiler errors, also check for:

```
Failed to import script <path>           - Script import failure (encoding, syntax)
Assembly <X> has reference to <Y> which is not included - asmdef dependency missing
Shader error in '<name>': <message>      - Shader compilation failure
```

## Exit Code Caveat

Exit code 0 does NOT guarantee zero compile errors. Always parse the log too.

- `unity test`: `8` = tests failed; `6` = run never produced a verdict (often compile
  errors or an Editor crash - grep the log).
- `unity run` / `unity build` can still exit 0 when:
  - `--execute-method` code catches all exceptions without calling `EditorApplication.Exit(1)`
  - `BuildPipeline.BuildPlayer` fails but the method ignores `BuildReport.summary.result`

Belt-and-suspenders check:
```bash
[ $exit_code -ne 0 ] || grep -qE "error CS|error IL|Scripts have compiler errors" <logfile>
```
