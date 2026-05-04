---
name: unity-save-data
description: "Design, inspect, implement, and validate Unity save/load systems, serialization formats, migrations, versioning, local/cloud-save boundaries, corrupt-data handling, backup safety, security, privacy, and backward compatibility. MUST use for persistent player data and SDK-managed state. Never delete, migrate, or overwrite saved data without explicit approval."
metadata:
  author: kuozg
  version: "1.0"
---
# unity-save-data

Guide persistent data work with migration safety, validation, security, and platform-aware storage.

## When to use

Use for:

- Save/load architecture and data model decisions.
- Serialization format selection and validation.
- Save versioning and migrations.
- Local save versus cloud-save boundaries.
- Corrupt, missing, or partial data handling.
- Backup and restore safety.
- Security and privacy review for persisted data.

## Discovery

1. Search for existing save paths, serializers, storage APIs, keys, data models, and version fields.
2. Identify whether saves use `Application.persistentDataPath`, PlayerPrefs, JSON, binary, ScriptableObjects, cloud SDKs, or custom services.
3. Locate migration code, backup behavior, encryption/signing, and corruption handling.
4. Identify platform-specific storage concerns and privacy-sensitive fields.
5. Preserve current save files and schemas unless migration is explicitly requested.

## Safety rules

- Do not delete, migrate, overwrite, or reset saved data without explicit user approval.
- Avoid hardcoding platform-specific storage paths when Unity APIs are available.
- Prefer backups before migration or destructive tests.
- Never persist secrets, access tokens, or unnecessary PII in plain text.
- Keep cloud-save responsibilities separate from local serialization unless the user asks for integration.

## Implementation guidance

- Use explicit schema/version fields.
- Validate data before applying it to runtime state.
- Treat missing/corrupt files as expected scenarios.
- Use atomic write patterns where possible: write temp, verify, then replace.
- Keep migrations idempotent and testable.
- Separate serialization DTOs from live runtime objects when practical.

## Validation

Verify:

- Round-trip serialization and deserialization preserves expected values.
- Missing save data creates safe defaults.
- Corrupt or partial save data fails safely and reports useful errors.
- Migration behavior handles old versions and preserves backward compatibility.
- Backup/restore behavior works before destructive operations.
- Platform paths use Unity APIs and are not hardcoded unnecessarily.
- Security/privacy risks for persisted data are documented.

## MCP/tool usage

- Use code search and file reads to discover serializers and storage APIs.
- Use `ReadConsole` or Unity compile checks after code changes.
- Use `RunCommand` only for safe, targeted tests that do not touch real user saves unless sandboxed.
- Use `ManageAsset` for ScriptableObject save templates or config assets where relevant.

## Boundaries

- Delegate cloud SDK setup to `unity-sdk-integration` or `unity-liveops`.
- Delegate runtime gameplay feature code to `unity-code`.
- Delegate package installation to `unity-package-manager`.
- Delegate manual QA plans to `unity-test-case`.

## Handoff

Report save locations, serializers, versioning/migration state, validation evidence, and any approval needed before data migration or deletion.
