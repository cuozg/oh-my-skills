---
name: bash-install
description: "Install software, packages, and tools with automatic retry and fallback strategies. Use this skill when: (1) Installing CLI tools or packages, (2) Setting up development dependencies, (3) An installation fails and alternative methods are needed, (4) Verifying installed software works correctly."
---

# Bash Install

Install software and tools with automatic verification and fallback strategies when installation fails.

## Purpose

Reliably install CLI tools, packages, and development dependencies across macOS and Linux — automatically retrying with fallback package managers when the primary method fails.

## Input

- **Required**: Package or tool name to install (e.g., `shellcheck`, `jq`, `node`).
- **Optional**: Specific version, target platform, or preferred package manager.

## Output

A structured installation report (following the INSTALL_REPORT.md template) delivered directly to the user, confirming installed version, install path, and any post-install steps — or documenting all failed attempts with next-step suggestions.

## Examples

| Trigger | Input | What Happens |
|---------|-------|--------------|
| "Install shellcheck" | `shellcheck` | Detects OS, tries brew/apt, verifies with `shellcheck --version` |
| "Set up Node.js v20" | `node`, version=20 | Tries brew/nvm/apt, pins version, verifies |
| "Install failed, try another way" | Prior failed package | Escalates to next strategy (direct download, source build) |

## Output Requirement (MANDATORY)

**Every installation report MUST follow the template**: [INSTALL_REPORT.md](.claude/skills/bash-install/assets/templates/INSTALL_REPORT.md)

Output the report directly to the user. No file save required.

Read the template first, then populate all sections.

## Workflow

### 1. Identify What to Install

Confirm the package/tool name and intended purpose. Ask clarifying questions if needed:
- What is the package name?
- What version is required (if specific)?
- What is the target platform (macOS, Linux, etc.)?

### 2. Detect System Environment

```bash
# Detect OS
uname -s

# Detect architecture
uname -m

# Check available package managers
which brew && echo "Homebrew available"
which apt && echo "APT available"
which yum && echo "YUM available"
which dnf && echo "DNF available"
which pacman && echo "Pacman available"
which npm && echo "NPM available"
which pip3 && echo "pip3 available"
```

### 3. Installation Strategy Order

Try installation methods in this priority order:

#### macOS
1. **Homebrew** (preferred): `brew install <package>`
2. **MacPorts**: `sudo port install <package>`
3. **NPM** (for JS tools): `npm install -g <package>`
4. **pip** (for Python tools): `pip3 install <package>`
5. **Direct download**: curl/wget binary or installer
6. **Build from source**: git clone + make

#### Linux (Debian/Ubuntu)
1. **APT** (preferred): `sudo apt install <package>`
2. **Snap**: `sudo snap install <package>`
3. **Flatpak**: `flatpak install <package>`
4. **NPM/pip**: Same as macOS
5. **Direct download/source**: Same as macOS

#### Linux (RHEL/Fedora)
1. **DNF/YUM**: `sudo dnf install <package>`
2. **Snap/Flatpak**: Same as above
3. **NPM/pip/source**: Same as above

### 4. Execute Installation

Attempt the first method:

```bash
# Example: Homebrew on macOS
brew install <package>
```

Capture the exit code:
```bash
if [ $? -eq 0 ]; then
  echo "✅ Installation successful"
else
  echo "❌ Installation failed, trying next method..."
fi
```

### 5. Verify Installation

Always verify after installation:

```bash
# Method 1: Check command exists
command -v <package> && echo "✅ Command available"

# Method 2: Check version
<package> --version

# Method 3: Run a simple test command
<package> --help
```

### 6. Handle Failures

When installation fails, follow this escalation:

**Step 1: Diagnose the failure**
```bash
# Check error messages
# Common issues:
# - Permission denied → use sudo or fix permissions
# - Not found → update package index or try different source
# - Dependency missing → install dependencies first
# - Version conflict → specify version or resolve conflicts
```

**Step 2: Try alternative method**
Move to next installation method in the priority list.

**Step 3: Search for alternatives**
```bash
# Homebrew: search for similar packages
brew search <keyword>

# APT: search packages
apt search <keyword>
```

**Step 4: Direct binary download**
```bash
# Download from official release page
curl -L -o /tmp/<package> <release-url>
chmod +x /tmp/<package>
sudo mv /tmp/<package> /usr/local/bin/
```

**Step 5: Build from source**
```bash
git clone <repo-url>
cd <repo>
./configure && make && sudo make install
```

### 7. Report Results

After successful installation:
- Confirm the installed version
- Show the installation path
- Provide any post-installation setup steps

After all methods exhausted:
- List all attempted methods and their errors
- Suggest manual intervention steps
- Provide links to official documentation

## Common Package Managers Quick Reference

| Manager | Install | Search | Update Index |
|---------|---------|--------|--------------|
| brew | `brew install` | `brew search` | `brew update` |
| apt | `sudo apt install` | `apt search` | `sudo apt update` |
| dnf | `sudo dnf install` | `dnf search` | `sudo dnf check-update` |
| npm | `npm install -g` | `npm search` | N/A |
| pip | `pip3 install` | `pip3 search` | N/A |

## Troubleshooting Checklist

- [ ] Package manager index updated?
- [ ] Correct package name? (may differ by OS)
- [ ] Sufficient permissions?
- [ ] Dependencies installed?
- [ ] No version conflicts?
- [ ] Network connectivity OK?
- [ ] Disk space available?
