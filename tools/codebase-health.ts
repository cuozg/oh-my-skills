import { tool } from "@opencode-ai/plugin"
import path from "path"

export default tool({
  description:
    "Analyze Unity codebase health metrics: file counts by type, largest C# files, TODO/FIXME/HACK counts, empty Update() methods, Singleton usage count, and script line count distribution. Use to get a quick project health overview.",
  args: {
    scope: tool.schema
      .string()
      .optional()
      .describe(
        "Subdirectory to scope analysis (relative to Assets/Scripts/). Defaults to all scripts."
      ),
  },
  async execute(args, context) {
    const scriptsDir = args.scope
      ? path.join(context.directory, "Assets/Scripts", args.scope)
      : path.join(context.directory, "Assets/Scripts")
    const script = path.join(
      context.worktree,
      ".opencode/tools/codebase-health.py"
    )
    try {
      const result =
        await Bun.$`python3 ${script} ${scriptsDir}`.text()
      return result.trim()
    } catch (e: any) {
      if (e?.stdout) return e.stdout.toString().trim()
      if (e?.stderr) return `Error: ${e.stderr.toString().trim()}`
      return `Error: ${e?.message ?? String(e)}`
    }
  },
})
