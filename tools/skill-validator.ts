import { tool } from "@opencode-ai/plugin"
import path from "path"

export default tool({
  description:
    "Deep structural validation of a skill folder. Checks frontmatter, body quality (TODOs, line count), file reference integrity, orphaned resources, and naming conventions. Use before packaging or after editing a skill. Supports --fix for auto-corrections and --json for programmatic output.",
  args: {
    skill_path: tool.schema
      .string()
      .describe(
        "Path to the skill directory to validate (e.g., '.opencode/skills/unity/unity-code')"
      ),
    fix: tool.schema
      .boolean()
      .optional()
      .describe("Auto-fix trivially fixable issues (permissions, trailing whitespace)"),
    json: tool.schema
      .boolean()
      .optional()
      .describe("Output results as JSON instead of human-readable text"),
  },
  async execute(args, context) {
    const script = path.join(
      context.worktree,
      ".opencode/tools/skill-validator.py"
    )
    const flags: string[] = []
    if (args.fix) flags.push("--fix")
    if (args.json) flags.push("--json")

    const skillDir = path.isAbsolute(args.skill_path)
      ? args.skill_path
      : path.join(context.worktree, args.skill_path)

    const result =
      await Bun.$`python3 ${script} ${skillDir} ${flags}`.text()
    return result.trim()
  },
})
