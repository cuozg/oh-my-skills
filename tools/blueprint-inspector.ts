import { tool } from "@opencode-ai/plugin"
import path from "path"

export default tool({
  description:
    "Inspect Unity Blueprint data files (JSON). Parse a Blueprint file, show its schema (field names, types, sample values), record count, and validate structure. Use for exploring DataManager data sources.",
  args: {
    file: tool.schema
      .string()
      .describe(
        "Path to the Blueprint JSON file (relative to project root or absolute)"
      ),
    sample_count: tool.schema
      .number()
      .optional()
      .describe("Number of sample records to display (default: 3)"),
  },
  async execute(args, context) {
    const filePath = path.isAbsolute(args.file)
      ? args.file
      : path.join(context.directory, args.file)
    const samples = args.sample_count ?? 3
    const script = path.join(
      context.worktree,
      ".opencode/tools/blueprint-inspector.py"
    )
    const result =
      await Bun.$`python3 ${script} ${filePath} ${samples}`.text()
    return result.trim()
  },
})
