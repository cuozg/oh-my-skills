# Linux Screenshot Guide

## Prerequisites

The Python helper (`take_screenshot.py`) automatically selects the first available tool:

1. `scrot`
2. `gnome-screenshot`
3. ImageMagick `import`

If none are available, ask the user to install one:

```bash
sudo apt-get install scrot          # recommended
sudo apt-get install gnome-screenshot
sudo apt-get install imagemagick
```

Check availability:

```bash
command -v scrot && echo "scrot ok"
command -v gnome-screenshot && echo "gnome-screenshot ok"
command -v import && echo "imagemagick ok"
```

## Capability Constraints

- `--app`, `--window-name`, `--list-windows` — **macOS-only**. Not supported on Linux.
- Coordinate regions (`--region`) require `scrot` or ImageMagick `import`.
- Use `--active-window` or `--window-id` for window targeting on Linux.

## Python Helper — Common Patterns

```bash
# Default location
python3 <path-to-skill>/scripts/take_screenshot.py

# Temp (Codex visual check)
python3 <path-to-skill>/scripts/take_screenshot.py --mode temp

# Explicit path
python3 <path-to-skill>/scripts/take_screenshot.py --path output/screen.png

# Pixel region (x,y,w,h) — requires scrot or imagemagick
python3 <path-to-skill>/scripts/take_screenshot.py --mode temp --region 100,200,800,600

# Active window
python3 <path-to-skill>/scripts/take_screenshot.py --mode temp --active-window

# Specific window id (when available)
python3 <path-to-skill>/scripts/take_screenshot.py --window-id 12345
```

## Multi-Display Behavior

Full-screen captures use the **virtual desktop** (all monitors in one image).
Use `--region` to isolate a single display when needed.

## Direct OS Commands (fallback when helper unavailable)

```bash
# Full screen
scrot output/screen.png
gnome-screenshot -f output/screen.png
import -window root output/screen.png

# Pixel region
scrot -a 100,200,800,600 output/region.png
import -window root -crop 800x600+100+200 output/region.png

# Active window
scrot -u output/window.png
gnome-screenshot -w -f output/window.png
```

## Error Handling

- Region/window capture fails → check tool availability with `command -v scrot`, `command -v gnome-screenshot`, `command -v import`.
- If saving to OS default location fails with permission errors in a sandbox → rerun with escalated permissions.
