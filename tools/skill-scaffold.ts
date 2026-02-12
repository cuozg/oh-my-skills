import { tool } from "@opencode-ai/plugin"
import path from "path"

export default tool({
  description:
    "Smart skill scaffolding with type-aware templates. Creates a pre-populated skill directory (SKILL.md, scripts/, references/, assets/) tailored to unity/bash/git/other domains. 2-3x faster than manual scaffold. Use when creating a new skill from scratch.",
  args: {
    skill_name: tool.schema
      .string()
      .describe("Skill name in hyphen-case (e.g., 'my-new-tool')"),
    type: tool.schema
      .enum(["unity", "bash", "git", "other"])
      .describe("Skill type — determines templates and conventions"),
    output_path: tool.schema
      .string()
      .describe("Directory where skill folder will be created (e.g., '.opencode/skills/unity')"),
    author: tool.schema
      .string()
      .optional()
      .describe("Author name (optional)"),
    json: tool.schema
      .boolean()
      .optional()
      .describe("Output results as JSON"),
  },
  async execute(args, context) {
    const script = path.join(
      context.worktree,
      ".opencode/tools/skill-scaffold.py"
    )
    const outputDir = path.isAbsolute(args.output_path)
      ? args.output_path
      : path.join(context.worktree, args.output_path)

    const flags: string[] = [
      args.skill_name,
      "--type", args.type,
      "--path", outputDir,
    ]
    if (args.author) flags.push("--author", args.author)
    if (args.json) flags.push("--json")

    const result =
      await Bun.$`python3 ${script} ${flags}`.text()
    return result.trim()
  },
})
