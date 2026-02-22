# CI/CD Pipeline Templates

Automated build pipelines for GitHub Actions, GitLab CI, and Jenkins.

## GitHub Actions

```yaml
name: Unity Build
on:
  push: { branches: [main, develop] }
  pull_request: { branches: [main] }
env:
  UNITY_LICENSE: ${{ secrets.UNITY_LICENSE }}
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        targetPlatform: [Android, WebGL]
    steps:
      - uses: actions/checkout@v4
        with: { lfs: true }
      - uses: actions/cache@v4
        with:
          path: Library
          key: Library-${{ matrix.targetPlatform }}-${{ hashFiles('Assets/**', 'Packages/**', 'ProjectSettings/**') }}
      - uses: game-ci/unity-builder@v4
        with:
          targetPlatform: ${{ matrix.targetPlatform }}
          buildMethod: BuildScript.Build${{ matrix.targetPlatform }}
      - uses: actions/upload-artifact@v4
        with:
          name: Build-${{ matrix.targetPlatform }}
          path: Builds/${{ matrix.targetPlatform }}
```

## Key Patterns

- **LFS**: Always use `lfs: true` in checkout
- **Caching**: Cache `Library/` folder keyed by platform + asset hash
- **Matrix**: One job per platform to parallelize
- **Exit codes**: Build script must exit(1) on failure in batch mode
- **Licensing**: Store Unity license in GitHub Secrets; set UNITY_LICENSE env var
