---
name: unity-localization
description: "Implement, inspect, and validate Unity localization for locale setup, string tables, localized assets, font fallback, RTL handling, UI overflow, missing translations, and localization QA. MUST use for Unity Localization package work, multilingual UI/content checks, fallback behavior, and text coverage validation. Delegate package setup to unity-package-manager when installation or removal is required."
metadata:
  author: kuozg
  version: "1.0"
---
# unity-localization

Support multilingual Unity projects by discovering localization setup, making targeted changes, and validating content coverage and UI risks.

## When to use

Use for:

- Locale setup and selected locale behavior.
- String tables, asset tables, localized assets, and localized references.
- Font fallback and glyph coverage.
- RTL language considerations and mirrored UI risks.
- Localization QA, missing translations, fallback behavior, and text overflow checks.

## Discovery

1. Check `Packages/manifest.json` and `Packages/packages-lock.json` for `com.unity.localization` before assuming the package exists.
2. Search for localization tables, `LocalizationSettings`, `LocalizedString`, `LocalizedAsset`, locale assets, and table collections.
3. Inspect UI text components and fonts used by localized screens.
4. Identify source-language ownership and product copy guidance before rewriting user-facing text.
5. If Unity Localization is missing and setup is required, delegate package installation to `unity-package-manager`.

## MCP tool usage

- Use `ManageAsset(Search/GetInfo)` to locate localization settings, tables, locales, fonts, prefabs, and scenes.
- Use `ManageGameObject(GetComponents)` to inspect UI text components in scenes or prefabs.
- Use `PackageManager_GetData` for package metadata; delegate package changes to `unity-package-manager`.
- Use `ReadConsole` or `GetConsoleLogs` after localization asset or package changes.
- Use scene capture tools when validating visual overflow or RTL layout.

## Safety rules

- Do not assume Unity Localization is installed without checking package configuration.
- Do not rewrite user-facing text without explicit product guidance.
- Preserve table keys unless the user asks for key migration.
- Prefer adding missing entries over renaming existing keys.
- Treat RTL layout changes as visual/UI work and validate them in context.

## Validation

Verify:

- Required locales and table collections exist.
- Missing translations, missing keys, and fallback entries are identified.
- Fallback behavior is configured for absent translations or assets.
- Font assets cover target language glyph ranges or have fallback chains.
- UI text does not overflow or truncate in target languages where visual validation is requested.
- RTL languages have alignment, ordering, and layout risks documented.
- Unity console has no localization package, table, asset, or serialization errors.

## Boundaries

- Delegate package installation/removal to `unity-package-manager`.
- Delegate UI construction to `unity-uitoolkit` or `unity-code` depending on UI stack.
- Delegate manual QA test plans to `unity-test-case`.
- Delegate generated localized art/audio to relevant asset skills.

## Handoff

Report localization package state, assets inspected, missing coverage, fallback/font/overflow findings, and recommended next translation or UI QA steps.
