---
name: "screenshot"
description: >
  Use this skill when the user explicitly asks for a desktop or system screenshot — full screen, a
  specific app or window, or a pixel region. Also use when tool-specific capture capabilities are
  unavailable and an OS-level capture is needed. Supports macOS (screencapture), Linux
  (scrot/gnome-screenshot), and Windows (PowerShell). Do not use for in-app screenshots or Unity
  scene captures — those have dedicated tools.
---

# Screenshot Capture

## Save-Location Rules

1. User specifies a path → save there.
2. User asks without a path → save to the OS default screenshot location.
3. Codex needs a screenshot for its own inspection → save to the temp directory.

Always report the saved file path in the response.

## Tool Priority

- Prefer tool-specific capabilities when available (Figma MCP for Figma, Playwright/agent-browser for web/Electron apps).
- Use this skill when explicitly asked, for whole-system desktop captures, or when no better-integrated tool exists.

## Platform Helpers

### macOS — `take_screenshot.py` + `ensure_macos_permissions.sh`

Run permission preflight before any window/app capture, then capture with the Python helper.
See → `references/macos-guide.md`

Quick start:

```bash
bash <path-to-skill>/scripts/ensure_macos_permissions.sh && \
python3 <path-to-skill>/scripts/take_screenshot.py --app "<App>" --mode temp
```

### Linux — `take_screenshot.py`

Requires `scrot`, `gnome-screenshot`, or ImageMagick `import` (auto-selected).
See → `references/linux-guide.md`

Quick start:

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --mode temp
```

### Windows — `take_screenshot.ps1`

PowerShell helper covers all modes (default, temp, explicit path, region, active window, handle).
See → `references/windows-guide.md`

Quick start:

```powershell
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1 -Mode temp
```

## Output Behavior

Script prints one path per capture. Multiple matching windows/displays → multiple paths, suffixed `-w<windowId>` or `-d<display>`. View each path sequentially.

## Error Handling Summary

- **macOS permissions**: run `ensure_macos_permissions.sh` first; if sandbox errors persist, rerun with escalated permissions.
- **macOS no match**: run `--list-windows --app "AppName"`, retry with `--window-id`, ensure app is visible.
- **Linux tool missing**: install `scrot` / `gnome-screenshot` / `imagemagick`; check with `command -v scrot`.
- **Sandbox save failure**: rerun with escalated permissions.

## References

| File | Content |
|------|---------|
| `references/macos-guide.md` | Permission preflight, Python helper patterns, workflow examples, multi-display, direct OS commands |
| `references/linux-guide.md` | Prerequisites, selection logic, Python helper patterns, multi-display, direct OS commands |
| `references/windows-guide.md` | PowerShell helper patterns, multi-display behavior |
