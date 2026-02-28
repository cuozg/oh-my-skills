# C# Quality Review Checklist

## Nullable Reference Types

- [ ] `<Nullable>enable</Nullable>` in .csproj
- [ ] Nullable types explicitly declared with `?`
- [ ] Non-nullable properties initialized (not left as default)
- [ ] No `!` (null-forgiving) without documented reason
- [ ] Null checks use pattern matching (`is null`, `is not null`)
- [ ] No unnecessary null checks on DI-injected dependencies

## Access Modifiers

- [ ] Fields are `private` (or `private readonly`)
- [ ] Helper classes are `internal sealed`
- [ ] Only API boundaries are `public`
- [ ] No public fields (use properties)
- [ ] `[SerializeField]` private fields for Unity inspector

## Exception Handling

### Throwing
- [ ] Exceptions thrown for error conditions (not logged-and-continued)
- [ ] `ArgumentNullException.ThrowIfNull()` for null guards
- [ ] `ArgumentException.ThrowIfNullOrEmpty()` for string guards
- [ ] `ArgumentOutOfRangeException` for range violations
- [ ] `KeyNotFoundException` for missing dictionary entries
- [ ] `InvalidOperationException` for invalid state transitions
- [ ] Custom exceptions for domain-specific errors

### Catching
- [ ] `catch (OperationCanceledException)` handled separately from general exceptions
- [ ] No empty catch blocks
- [ ] No `catch (Exception)` that swallows without re-throw
- [ ] Specific exception types caught (not bare `Exception`)
- [ ] Exception details preserved when re-throwing (`throw;` not `throw ex;`)

## Logging

### ILogger Usage
- [ ] `ILogger` used for runtime logging (injected via DI)
- [ ] No `Debug.Log` in runtime code (only `#if UNITY_EDITOR`)
- [ ] No logging in constructors
- [ ] No null-conditional on logger (`this.logger.Debug()` not `this.logger?.Debug()`)
- [ ] No manual prefixes (logger handles automatically)
- [ ] No conditional compilation guards around logger calls
- [ ] Appropriate log levels: Debug for diagnostics, Info for significant events, Warning for recoverable issues

### Log Quality
- [ ] No verbose/unnecessary logs (entering method, exiting method)
- [ ] Log messages are actionable (include relevant data)
- [ ] No sensitive data in logs (passwords, tokens, PII)
- [ ] No string concatenation in log calls (use interpolation)


See [csharp-hygiene.md](csharp-hygiene.md) for canonical naming conventions.
