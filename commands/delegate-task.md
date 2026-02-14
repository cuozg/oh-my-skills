---
description: Delegation to @sisyphus-junior |1.Prompt|2.Skill|3.Session_id|
agent: sisyphus-junior
model: github-copilot/claude-opus-4.6
subtask: true
---

task(
  subagent_type='sisyphus',
  prompt=$1
  load_skills=[$2],
  run_in_background=false,
  session_id=$3
)

ALWAYS return session_id

