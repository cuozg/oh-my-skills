# install-strategies.md

## Package Manager Priority by OS

| OS | Primary | Fallback 1 | Fallback 2 |
|---|---|---|---|
| macOS | Homebrew (`brew install`) | MacPorts | build from source |
| Ubuntu/Debian | apt (`apt-get install`) | snap | build from source |
| Alpine/CI | apk (`apk add`) | — | — |
| Any (Python) | pip (`pip install`) | pipx | conda |
| Any (Node) | npm / yarn | pnpm | — |

## Retry Pattern

```bash
install_with_retry() {
  local cmd="$1" max=3 attempt=1
  until eval "$cmd"; do
    if (( attempt >= max )); then
      echo "FAIL: install failed after $max attempts" >&2
      return 1
    fi
    echo "Retry $attempt/$max — waiting 5s..."
    sleep 5
    (( attempt++ ))
  done
}
```

## Verification Commands

```bash
# Generic
which tool && tool --version

# Python package
python -c "import package; print(package.__version__)"

# Node package
node -e "require('package')"

# System service
systemctl is-active service-name
```

## Fallback Chain Pattern

```bash
install_tool() {
  echo "Attempting brew install..."
  brew install "$1" 2>/dev/null && return 0

  echo "Brew failed, trying pip..."
  pip install "$1" 2>/dev/null && return 0

  echo "All install methods failed for $1" >&2
  return 1
}
```

## Common Failure Modes

| Error | Cause | Fix |
|---|---|---|
| `E: Unable to lock` | apt lock held | Wait or `kill` process |
| `Network timeout` | Transient | Retry with backoff |
| `Permission denied` | Needs sudo | Prepend `sudo` |
| `No such package` | Wrong name | Check registry for correct name |
