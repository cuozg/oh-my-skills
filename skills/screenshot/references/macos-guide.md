# macOS Screenshot Guide

## Permission Preflight

Run once before any window/app capture. Checks Screen Recording permission, requests it in one place.
Routes Swift module cache to `$TMPDIR/codex-swift-module-cache` to avoid extra sandbox module-cache prompts.

```bash
bash <path-to-skill>/scripts/ensure_macos_permissions.sh
```

Combine preflight + capture in one command to minimize sandbox approval prompts:

```bash
bash <path-to-skill>/scripts/ensure_macos_permissions.sh && \
python3 <path-to-skill>/scripts/take_screenshot.py --app "Codex"
```

For Codex inspection runs (temp output):

```bash
bash <path-to-skill>/scripts/ensure_macos_permissions.sh && \
python3 <path-to-skill>/scripts/take_screenshot.py --app "<App>" --mode temp
```

## Python Helper — Common Patterns

```bash
# Default location (user asked for "a screenshot")
python3 <path-to-skill>/scripts/take_screenshot.py

# Temp (Codex visual check)
python3 <path-to-skill>/scripts/take_screenshot.py --mode temp

# Explicit path
python3 <path-to-skill>/scripts/take_screenshot.py --path output/screen.png

# App/window by name (substring match; captures all matching windows)
python3 <path-to-skill>/scripts/take_screenshot.py --app "Codex"

# Specific window title within an app
python3 <path-to-skill>/scripts/take_screenshot.py --app "Codex" --window-name "Settings"

# List window IDs before capturing
python3 <path-to-skill>/scripts/take_screenshot.py --list-windows --app "Codex"

# Pixel region (x,y,w,h)
python3 <path-to-skill>/scripts/take_screenshot.py --mode temp --region 100,200,800,600

# Focused/active window
python3 <path-to-skill>/scripts/take_screenshot.py --mode temp --active-window

# Specific window id
python3 <path-to-skill>/scripts/take_screenshot.py --window-id 12345
```

The script prints one path per capture. Multiple matching windows/displays → multiple paths, suffixed `-w<windowId>` or `-d<display>`. View each path sequentially.

## Workflow Examples

"Take a look at \<App\> and tell me what you see": capture to temp, view each printed path in order.

```bash
bash <path-to-skill>/scripts/ensure_macos_permissions.sh && \
python3 <path-to-skill>/scripts/take_screenshot.py --app "<App>" --mode temp
```

"Design from Figma doesn't match implementation": use Figma MCP/skill first, then capture running app to temp, compare raw screenshots before any manipulation.

## Multi-Display Behavior

Full-screen captures save **one file per display** when multiple monitors are connected.
Use `--window-id` or `--app` to target a specific display/window.

## Direct OS Commands (fallback when helper unavailable)

```bash
# Full screen to path
screencapture -x output/screen.png

# Pixel region
screencapture -x -R100,200,800,600 output/region.png

# Specific window id
screencapture -x -l12345 output/window.png

# Interactive selection
screencapture -x -i output/interactive.png
```

## Error Handling

- "screen capture checks are blocked in the sandbox" / "could not create image from display" / Swift `ModuleCache` errors → rerun with escalated permissions.
- App/window capture returns no matches → run `--list-windows --app "AppName"`, retry with `--window-id`, ensure app is visible on screen.
