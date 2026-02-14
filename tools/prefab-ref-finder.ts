import { tool } from "@opencode-ai/plugin"
import path from "path"

export default tool({
  description:
    "Find Unity prefab, scene, and asset files that reference a C# script by GUID. Use before renaming, moving, or deleting scripts to find which assets would break.",
  args: {
    target: tool.schema
      .string()
      .describe(
        "C# file path (relative to project root), class name, or 32-char GUID"
      ),
    types: tool.schema
      .string()
      .optional()
      .describe(
        "Comma-separated asset types to search: prefab, scene, asset (default: prefab,scene)"
      ),
  },
  async execute(args, context) {
    const script = path.join(
      context.worktree,
      ".opencode/tools/prefab-ref-finder.py"
    )
    const cmdArgs = [script, args.target, context.directory]
    if (args.types) {
      cmdArgs.push("--types", args.types)
    }
    try {
      const result = await Bun.$`python3 ${cmdArgs}`.text()
      return result.trim()
    } catch (e: any) {
      if (e?.stdout) return e.stdout.toString().trim()
      if (e?.stderr) return `Error: ${e.stderr.toString().trim()}`
      return `Error: ${e?.message ?? String(e)}`
    }
  },
})
