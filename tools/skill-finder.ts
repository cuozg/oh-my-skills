import { tool } from "@opencode-ai/plugin"
import path from "path"

export default tool({
  description:
    "Find the best matching skill for a given task description. Searches all installed skills by name and description, ranks by relevance. Use when unsure which skill to apply for a task.",
  args: {
    task: tool.schema
      .string()
      .describe("Natural language description of the task (e.g., 'fix compiler errors', 'create a mermaid diagram')"),
  },
  async execute(args, context) {
    const script = path.join(
      context.worktree,
      ".opencode/tools/skill-finder.py"
    )
    const skillsDir = path.join(context.worktree, ".opencode/skills")
    const result =
      await Bun.$`python3 ${script} ${skillsDir} ${args.task}`.text()
    return result.trim()
  },
})
