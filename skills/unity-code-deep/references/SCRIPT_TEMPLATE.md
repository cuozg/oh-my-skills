# Script Template

Use as starting point for every new MonoBehaviour. Populate all sections, remove unused regions.

## Template

```csharp
using UnityEngine;
using UnityEngine.Serialization;
using System;
using System.Collections.Generic;

namespace _Project.Scripts.FeatureName
{
    /// <summary>
    /// [PURPOSE]: What this component does.
    /// [USAGE]: How other systems interact with it.
    /// [DEPENDENCIES]: What it requires.
    /// </summary>
    public class NewScript : MonoBehaviour
    {
        #region Constants
        private const float DefaultSpeed = 5f;
        #endregion

        #region Serialized Fields
        [Header("Configuration")]
        [Tooltip("Movement speed in units per second")]
        [SerializeField] private float _speed = DefaultSpeed;

        [Header("References")]
        [Tooltip("Drag the target transform from the scene")]
        [SerializeField] private Transform _target;
        #endregion

        #region Private Fields
        private bool _isActive;
        #endregion

        #region Events
        public event Action<bool> OnActiveChanged;
        #endregion

        #region Lifecycle
        private void Awake()
        {
            if (_target == null)
            {
#if UNITY_EDITOR
                Debug.LogError($"[{nameof(NewScript)}] Target is not assigned!", this);
#endif
            }
        }
        private void OnEnable() { /* Subscribe to events */ }
        private void OnDisable() { /* Unsubscribe, kill tweens, stop coroutines */ }
        private void OnDestroy() { /* Dispose native resources */ }
        #endregion

        #region Public Methods
        /// <summary>[What]. [When to call]. [Side effects].</summary>
        public void Execute(int value)
        {
            if (value < 0) return;
            ProcessLogic(value);
        }
        #endregion

        #region Private Methods
        private void ProcessLogic(int value) { /* WHY comments, not WHAT */ }
        #endregion
    }
}
```

## Checklist

### Structure
- [ ] Namespace matches directory path
- [ ] `/// <summary>` on class with PURPOSE/USAGE/DEPENDENCIES
- [ ] Regions used, unused regions deleted

### Comments
- [ ] XML docs on every public member
- [ ] `[Tooltip]` on every `[SerializeField]`, `[Header]` groups
- [ ] No commented-out code

### Clean Code
- [ ] No magic numbers — use `const`/`static readonly`/`[SerializeField]`
- [ ] Guard clauses at method entry
- [ ] No deep nesting (4+ levels)
- [ ] Single responsibility per class

### Unity Safety
- [ ] `if (this == null) return;` after every `await`
- [ ] Events: `+=` in OnEnable, `-=` in OnDisable
- [ ] Components cached in `Awake`, no per-frame `Find()`/`GetComponent()`
- [ ] `[FormerlySerializedAs]` when renaming serialized fields
- [ ] Empty callbacks deleted, `Debug.Log` guarded with `#if UNITY_EDITOR`
- [ ] ScriptableObjects cloned before runtime modification
