---
name: unity-task-executor
description: "Execute detailed tasks. Use when: (1) Task guide ready from unity-task-brainstorm, (2) Implementing C#/.claude/skills/unity-task-executor/assets/data, (3) Coordinating specialists for planned task."
---

# Unity Plan Executor

Execute task instructions using specialized skills.

## Output Requirement (MANDATORY)

**Every execution report MUST follow the template**: [EXECUTION_REPORT.md](.claude/skills/unity-task-executor/assets/templates/EXECUTION_REPORT.md)

Update the task file status and output the execution report to the user.

Read the template first, then populate all sections.

## Workflow

1. **Read**: Load `Documents/Tasks/[Number][Epic][Task].md`
2. **Select Specialist**:
   - Logic → `unity-implement-logic`
   - Shaders/Tools → `unity-tech-art`
   - Data → `flatbuffers-coder`
   - Editor → `unity-editor-tools`
3. **Implement**: Follow task guide step-by-step, adapt to current codebase
4. **Verify**: Compile check after each step
5. **Self-Correct**: If guide fails, use `unity-investigate-code` to fix
6. **Complete**: Update task file with "Completed" status

## Execution Checklist

- [ ] Read full task guide
- [ ] Identify specialist skill(s) needed
- [ ] Apply code changes as specified
- [ ] Compile succeeds
- [ ] Tests pass (if defined)
- [ ] Report modified files

## Best Practices

- **Atomic**: Complete one task fully before next
- **Validate**: Compile after every change
- **Specialist Persona**: Adopt loaded skill's best practices
- **Transparency**: Report exactly what was modified/created
