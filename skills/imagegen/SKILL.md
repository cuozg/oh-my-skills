---
name: "imagegen"
description: >
  Use this skill when the user asks to generate, create, or edit images — concept art, product shots,
  icons, logos, textures, illustrations, or batch variants. Covers generation from text prompts and
  editing existing images (background removal/replacement, inpainting, style transfer, object removal).
  MUST use when the user says "generate an image," "create an icon," "make me a picture," "I need a
  hero image," "swap/remove the background," "edit this photo," "make it look like [style]," "batch of
  icons," "placeholder art," or describes needing any visual asset casually. Also triggers on: game
  assets (sprites, textures, UI icons), website visuals (hero images, blog headers), product photo
  edits, logo generation, infographics, or any request to produce an image from a description. Runs
  the bundled CLI (scripts/image_gen.py) and requires GEMINI_API_KEY or GOOGLE_API_KEY.
---

# Image Generation Skill

Generate or edit images using Google Gemini Imagen API. Defaults: `imagen-4.0-generate-001` (generate), `imagen-3.0-capability-001` (edit). Use bundled CLI `scripts/image_gen.py`.

## Decision Tree

- User provides input image OR says "edit/retouch/inpaint/mask/change only X" → **edit**
- Multiple different prompts/assets needed → **generate-batch**
- Otherwise → **generate**

## Workflow

1. Decide intent (decision tree above)
2. Collect: prompt(s), exact text (verbatim), constraints/avoid list, input image(s)/mask(s)
3. Batch: write temp JSONL to `tmp/imagegen/` (one job per line), run once, delete after
4. Augment prompt via `references/prompt-augmentation.md` (don't invent new requirements)
5. Pick aspect ratio (see table below)
6. Run CLI: `python <skill-dir>/scripts/image_gen.py <command> <args>`
7. Validate: file exists, size >10KB, report output path
8. Iterate with ONE targeted change if result doesn't satisfy constraints

## Aspect Ratios

| Use case | Ratio |
|----------|-------|
| App icon, avatar, logo, texture | `1:1` |
| Website hero, banner, cinematic | `16:9` |
| Mobile wallpaper, story, portrait | `9:16` |
| Blog header, product card | `4:3` |
| Infographic, poster | `3:4` |

## CLI

```bash
python "<skill-dir>/scripts/image_gen.py" <command> <args>
# Or via run_skill_script:
run_skill_script(skill="imagegen", script="scripts/image_gen.py", arguments=["generate", "--prompt", "...", "--dry-run"])
```

## Error Recovery

- **Safety filter / no images returned**: rephrase — less specific about people/violence. Add `--person-generation ALLOW_ADULT` if appropriate.
- **Rate limit (429)**: CLI has built-in retry. Wait 60s if still failing.
- **Empty result**: simplify prompt first to confirm API, then add complexity.
- **Edit policy rejection**: add explicit invariants ("change only background; keep person unchanged").

Always diagnose which part caused the issue — don't re-run same prompt.

## Environment

- `GEMINI_API_KEY` or `GOOGLE_API_KEY` for generation
- Edit operations: Vertex AI mode — set `GOOGLE_CLOUD_PROJECT` + `GOOGLE_CLOUD_LOCATION` + ADC
- CLI loads `.env` from: `--env-file` → `<project>/.env.local` → `<project>/.env` → `~/.env.local` → `~/.env`
- Never ask user to paste the key — ask them to set it as env var or `.env` file

## Rules

- `--force` when re-running to overwrite previous attempt
- Use Google GenAI Python SDK (`google-genai`) — never raw HTTP
- Prefer bundled CLI over writing one-off scripts
- Temp files: `tmp/imagegen/` · Final output: `output/imagegen/`

## References

- `references/prompt-augmentation.md` — taxonomy, spec template, augmentation rules
- `references/cli.md` — commands, flags, recipes
- `references/image-api.md` — API params, models, edit reference images
- `references/prompting.md` — prompting principles, iteration patterns
- `references/sample-prompts-*.md` — copy/paste prompts by category (generate, edit, website, game, asset-types)
