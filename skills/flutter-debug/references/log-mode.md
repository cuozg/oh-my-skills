# Log Mode — Debug Logging Snippets

Generate structured logging snippets for tracing values and method execution. Output only — never write to project files.

## When to Use

- User says "add debug logs," "trace this value," "logging for this method"
- Need to instrument a service, repository, or widget for debugging

## Format

Use `package:logger` with `[ClassName.methodName]` prefix:

```dart
final _log = Logger('ClassName');
_log.d('[ClassName.method] Loading user id=$userId');
_log.i('[ClassName.method] Loaded ${users.length} users');
_log.w('[ClassName.method] Cache miss for key=$key');
_log.e('[ClassName.method] Failed', error: e, stackTrace: st);
```

## Production Safety

Guard with `kDebugMode` or `assert()`:

```dart
if (kDebugMode) {
  _log.d('[MyService.fetch] payload=$payload');
}
assert(() { _log.d('[MyService.fetch] payload=$payload'); return true; }());
```

## Templates

**Entry/Exit**: `_log.d('[Svc.method] called param=$p'); ... _log.d('[Svc.method] result=$r');`

**Error boundary**: `try { ... } catch (e, st) { _log.e('[Cls.method] failed', error: e, stackTrace: st); rethrow; }`

**State change**: `_log.i('[Notifier.update] $oldState -> $newState');`

**API call**: `_log.d('[Repo.fetch] GET $url'); _log.d('[Repo.fetch] ${res.statusCode} (${res.body.length}b)');`

## Rules

- **Output only** — print as code block, never write to project files
- **Structured prefix** — always `[ClassName.methodName]` format
- **Log levels** — `d` debug, `i` info, `w` warning, `e` error
- **Never log sensitive data** — no passwords, tokens, PII, API keys
- **Guard for production** — `kDebugMode` or `assert()` for verbose logs
