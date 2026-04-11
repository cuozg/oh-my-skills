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

Generates or edits images using Google Gemini's Imagen API. Defaults to `imagen-4.0-generate-001` and the bundled CLI (`scripts/image_gen.py`) for deterministic, reproducible runs.

## When to use
- Generate a new image (concept art, product shot, cover, website hero, game asset, logo, wireframe)
- Edit an existing image (inpainting, masked edits, background replacement, object removal, style transfer, transparent background)
- Batch runs (many prompts or variants across prompts)

## Decision tree (generate vs edit vs batch)
- If the user provides an input image (or says "edit/retouch/inpaint/mask/translate/change only X") → **edit**
- Else if the user needs many different prompts/assets → **generate-batch**
- Else → **generate**

## CLI path resolution
The bundled CLI lives at `scripts/image_gen.py` relative to this skill's directory. Resolve the path dynamically — do not hardcode an absolute path:

```bash
# Use the skill directory to locate the script
python "<skill-dir>/scripts/image_gen.py" <command> <args>
```

If using `run_skill_script`, call it directly:
```
run_skill_script(skill="imagegen", script="scripts/image_gen.py", arguments=["generate", "--prompt", "...", "--dry-run"])
```

## Workflow
1. Decide intent: generate vs edit vs batch (decision tree above).
2. Collect inputs up front: prompt(s), exact text (verbatim), constraints/avoid list, and any input image(s)/mask(s).
3. If batch: write temporary JSONL under `tmp/imagegen/` (one job per line), run once, then delete it.
4. Augment prompt into a structured spec (see `references/prompt-augmentation.md`) without inventing new creative requirements.
5. Pick the right aspect ratio for the use case (see "Aspect ratio guidance" below).
6. Run bundled CLI: `python <skill-dir>/scripts/image_gen.py <command> <args>` (see `references/cli.md` for recipes).
7. Validate outputs — check file exists, file size is reasonable (>10KB for a real image), and report the output path to the user. If the generation returned no images or an empty file, that's a content policy or safety filter issue (see "Error recovery" below).
8. If the result doesn't satisfy constraints, iterate: make a single targeted change (prompt wording, negative prompt, or mask), re-run, re-check. Don't change multiple things at once.
9. Save/return final outputs and note the final prompt + flags used.

## Aspect ratio guidance
Pick aspect ratio based on intended use — don't always default to 1:1:

| Use case | Aspect ratio | Why |
|---|---|---|
| App icon, avatar, profile pic | `1:1` | Square format expected |
| Website hero, banner, header | `16:9` | Wide landscape fills hero sections |
| Mobile wallpaper, story, portrait | `9:16` | Tall portrait for mobile screens |
| Blog header, feature image | `4:3` | Slightly wide, versatile |
| Product card, social post | `4:3` | Slightly wide, versatile |
| Game concept art, cinematic | `16:9` | Wide cinematic framing |
| Logo, icon, texture | `1:1` | Square for flexibility |
| Infographic, poster | `3:4` | Portrait layout for vertical flow |

## Error recovery
The Imagen API can reject requests or return empty results for several reasons. Handle them:

- **Safety filter block** (no images returned): The prompt triggered content policy. Rephrase to be less specific about people, violence, or sensitive topics. Add `--person-generation ALLOW_ADULT` if the request involves people and is appropriate.
- **Rate limit (429)**: The CLI has built-in retry with exponential backoff. If it still fails after retries, wait 60 seconds and try again.
- **Empty result / 0 images**: Check that the prompt isn't too vague or contradictory. Try a simpler prompt first to confirm API connectivity, then add complexity.
- **Content policy rejection for edits**: When editing images with people, the safety filter is stricter. Use explicit invariants ("change only the background; keep the person unchanged") and consider `--safety-filter-level BLOCK_ONLY_HIGH` if appropriate.

When an error occurs, don't just re-run the same prompt. Diagnose which part caused the issue and make a targeted fix.

## Temp and output conventions
- Use `tmp/imagegen/` for intermediate files (JSONL batches); delete when done.
- Write final artifacts under `output/imagegen/` when working in this repo.
- Use `--out` or `--out-dir` to control output paths; keep filenames stable and descriptive.

## Dependencies
Python packages (prefer `uv`):
```
uv pip install google-genai pillow
```
Or with pip:
```
python3 -m pip install google-genai pillow
```

## Environment
- **`GEMINI_API_KEY`** (or `GOOGLE_API_KEY`) required for **generation** API calls (no API key = dry-run only).
- **Edit operations** require Vertex AI mode: set `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION` (default: `us-central1`) with Application Default Credentials (ADC). See [ADC setup](https://cloud.google.com/docs/authentication/application-default-credentials).
- The CLI automatically loads API keys from `.env` files in this priority order (first match wins):
  1. Explicit `--env-file <path>` flag
  2. `<project>/.env.local` (current working directory)
  3. `<project>/.env`
  4. `~/.env.local`
  5. `~/.env`
- OS environment variables already set take precedence over `.env` file values.
- If missing everywhere: user creates key at https://aistudio.google.com/apikey and sets it locally.
- Never ask user to paste the key; ask them to set it as an environment variable or in a `.env` file and confirm when ready.

## Defaults & rules
- Model: `imagen-4.0-generate-001` for generation; `imagen-3.0-capability-001` for edits (unless user explicitly asks for a different model).
- Assume generate unless user explicitly says "edit".
- Use Google GenAI Python SDK (`google-genai` package) for all API calls; never raw HTTP.
- Prefer bundled CLI (`scripts/image_gen.py`) over writing one-off scripts.
- If result isn't clearly relevant or doesn't satisfy constraints, iterate with small targeted prompt changes; only ask a question if a missing detail blocks success.
- Always use `--force` when re-running a generation to overwrite the previous attempt.

## Reference map
- **`references/prompt-augmentation.md`**: Use-case taxonomy + spec template + augmentation rules.
- **`references/prompting.md`**: Prompting principles (structure, constraints, iteration patterns, use-case tips).
- **`references/cli.md`**: How to run image generation/edits/batches via CLI (commands, flags, recipes).
- **`references/image-api.md`**: API parameter quick reference (aspect ratios, models, config objects, edit reference images).
- **`references/sample-prompts-generate.md`**: Copy/paste prompts for generation workflows.
- **`references/sample-prompts-edit.md`**: Copy/paste prompts for edit workflows.
- **`references/sample-prompts-website.md`**: Website asset recipes (hero, cards, backgrounds, etc.).
- **`references/sample-prompts-game.md`**: Game asset recipes (concept art, items, environments, etc.).
- **`references/sample-prompts-asset-types.md`**: Asset-type templates (wireframes, logos, mockups, etc.).
