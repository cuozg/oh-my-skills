---
description: Create/Update Skill
agent: sisyphus-junior
model: github-copilot/claude-opus-4.6
skill: other/skill-creator
subtask: true
---

task(
  subagent_type='sisyphus-junior',
  prompt=$1
  load_skills=[$2],
  run_in_background=false,
  session_id=$3
)

ALWAYS return session_id

