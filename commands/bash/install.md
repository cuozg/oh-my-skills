---
description: Install software, packages, and tools with retry and fallback
agent: sisyphus-junior
subtask: true
---
Use skill bash-install to install $ARGUMENTS

# Bash Install — Workflow

## 1. Identify What to Install
Confirm package name, version (if specific), target platform.

## 2. Detect System Environment
```bash
uname -s        # OS
uname -m        # Architecture
which brew apt yum dnf pacman npm pip3 2>/dev/null
```

## 3. Installation Strategy Order

**macOS**: brew → MacPorts → npm → pip3 → direct download → source build
**Debian/Ubuntu**: apt → snap → flatpak → npm/pip → direct download → source
**RHEL/Fedora**: dnf/yum → snap/flatpak → npm/pip → source

## 4. Execute Installation
```bash
brew install <package>  # or apt/dnf/npm equivalent
if [ $? -eq 0 ]; then echo "✅ Success"; else echo "❌ Failed, trying next..."; fi
```

## 5. Verify Installation
```bash
command -v <package>
<package> --version
```

## 6. Handle Failures
1. **Diagnose**: permission denied → sudo; not found → update index; dependency missing → install deps
2. **Try next method** in priority list
3. **Search alternatives**: `brew search <keyword>` / `apt search <keyword>`
4. **Direct binary**: `curl -L -o /tmp/<pkg> <url> && chmod +x && sudo mv /usr/local/bin/`
5. **Build from source**: `git clone && ./configure && make && sudo make install`

## 7. Report Results
Success: version, path, post-install steps. Failure: all attempts, errors, manual next steps.

## Package Managers Quick Reference

| Manager | Install | Search | Update Index |
|---------|---------|--------|--------------|
| brew | `brew install` | `brew search` | `brew update` |
| apt | `sudo apt install` | `apt search` | `sudo apt update` |
| dnf | `sudo dnf install` | `dnf search` | `sudo dnf check-update` |
| npm | `npm install -g` | `npm search` | N/A |
| pip | `pip3 install` | `pip3 search` | N/A |
