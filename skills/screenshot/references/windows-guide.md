# Windows Screenshot Guide

## PowerShell Helper

Run the helper:

```powershell
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1
```

## Common Patterns

```powershell
# Default location (user asked for "a screenshot")
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1

# Temp (Codex visual check)
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1 -Mode temp

# Explicit path
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1 -Path "C:\Temp\screen.png"

# Pixel region (x,y,w,h)
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1 -Mode temp -Region 100,200,800,600

# Active window (ask user to focus it first)
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1 -Mode temp -ActiveWindow

# Specific window handle (only when provided)
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1 -WindowHandle 123456
```

## Multi-Display Behavior

Full-screen captures use the **virtual desktop** (all monitors in one image).
Use `-Region` to isolate a single display when needed.

## Error Handling

- If saving to OS default location fails with permission errors in a sandbox → rerun with escalated permissions.
- Always report the saved file path in the response.
