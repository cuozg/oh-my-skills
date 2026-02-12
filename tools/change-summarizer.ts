import { tool } from "@opencode-ai/plugin"
import path from "path"

export default tool({
  description:
    "Summarize uncommitted git changes with context: files changed, systems affected, risk level, and suggested test areas. Understands Unity project structure (Managers, Controllers, DataManagers, Singletons).",
  args: {
    staged_only: tool.schema
      .boolean()
      .optional()
      .describe("If true, only analyze staged changes (default: false, all uncommitted)"),
    path_filter: tool.schema
      .string()
      .optional()
      .describe("Only analyze changes under this path (e.g., 'Assets/Scripts/DailyBoss')"),
  },
  async execute(args, context) {
    const script = path.join(
      context.worktree,
      ".opencode/tools/change-summarizer.py"
    )
    const cmdArgs = [script, context.directory]
    if (args.staged_only) {
      cmdArgs.push("--staged-only")
    }
    if (args.path_filter) {
      cmdArgs.push("--path-filter", args.path_filter)
    }
    const result = await Bun.$`python3 ${cmdArgs}`.text()
    return result.trim()
  },
})
