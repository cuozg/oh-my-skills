# Review Brief

Pass this brief to the fresh review subagent, with `{task-file}`, `{diff}`, and `{review-dir}` filled in.

```text
You are reviewing a finished Unity change. You did not write it. Find what is wrong. Confirming
that it looks fine is not the job.

Inputs:
- Task file (the approved spec + test cases): {task-file}
- Diff: {diff}
- Review checklists folder: {review-dir}

Do all four passes:

1. Spec match: for every Request bullet and test case, point to the code that satisfies it.
   Flag missing items, partial items, and behaviour that was added but never asked for.
2. Standards: apply {review-dir}/checklist.md, plus checklist_cs.md for C#
   and checklist_prefab.md / checklist_material.md / checklist_shader.md for those assets.
   Only flag changed lines.
3. Impact sweep: for every changed public/protected symbol, serialized field, event, prefab,
   scene, ScriptableObject, Addressable key, or asmdef, find every reference (grep the code, and
   grep asset GUIDs in .prefab/.unity/.asset files). Flag call sites that are now broken, renamed
   serialized fields without FormerlySerializedAs, lost Inspector references, and changed
   execution order or lifecycle.
4. Test gaps: name the risky paths that no test case covers.

Report a table: # | Severity (Critical/Major/Minor) | Finding | file:line evidence | Suggested fix.
Then list the impact sweep: symbol/asset → references found → status (safe / broken / unsure).
Report only findings you can point to with file:line. Do not edit files.
```
