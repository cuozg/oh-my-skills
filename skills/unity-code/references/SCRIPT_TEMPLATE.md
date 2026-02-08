# Script Template

Use this template as the starting point for every new MonoBehaviour. Populate all sections, remove unused regions, and follow the code quality checklist at the bottom.

## Template

```csharp
using UnityEngine;
using UnityEngine.Serialization; // For [FormerlySerializedAs] when renaming fields
using System;
using System.Collections.Generic;

namespace _Project.Scripts.FeatureName // Match directory: Assets/Scripts/FeatureName/
{
    /// <summary>
    /// [PURPOSE]: What this component does and why it exists.
    /// [USAGE]: How other systems interact with it (events, public API).
    /// [DEPENDENCIES]: What it requires (other components, ScriptableObjects).
    /// </summary>
    public class NewScript : MonoBehaviour
    {
        #region Constants

        // Named constants — no magic numbers anywhere in the file
        private const float DefaultSpeed = 5f;
        private const int MaxRetries = 3;

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
        private int _currentRetries;

        #endregion

        #region Events

        /// <summary>Fired when activation state changes. Param: new active state.</summary>
        public event Action<bool> OnActiveChanged;

        #endregion

        #region Lifecycle

        private void Awake()
        {
            // Cache component references here
            // Validate required serialized fields
            if (_target == null)
            {
#if UNITY_EDITOR
                Debug.LogError($"[{nameof(NewScript)}] Target is not assigned!", this);
#endif
            }
        }

        private void OnEnable()
        {
            // Subscribe to events here
        }

        private void OnDisable()
        {
            // Unsubscribe from events here (mirror OnEnable exactly)
            // Kill DOTween animations
            // Stop coroutines
        }

        private void OnDestroy()
        {
            // Dispose native resources
            // Destroy cloned ScriptableObjects
        }

        #endregion

        #region Public Methods

        /// <summary>
        /// [What it does]. [When to call it]. [Side effects].
        /// </summary>
        /// <param name="value">Description of parameter.</param>
        /// <returns>Description of return value.</returns>
        public void Execute(int value)
        {
            // Guard clause — validate input early
            if (value < 0) return;

            ProcessLogic(value);
        }

        #endregion

        #region Private Methods

        /// <summary>Internal processing logic.</summary>
        private void ProcessLogic(int value)
        {
            // Implementation with inline comments explaining WHY, not WHAT
        }

        #endregion
    }
}
```

## Checklist Before Submitting

Run through every item. If any fails, fix before marking complete.

### Structure
- [ ] Namespace matches directory path (`_Project.Scripts.FeatureName`)
- [ ] `/// <summary>` on the class with PURPOSE, USAGE, DEPENDENCIES
- [ ] Regions used: Constants, Serialized Fields, Private Fields, Events, Lifecycle, Public Methods, Private Methods
- [ ] Unused regions deleted (don't leave empty regions)

### Comments
- [ ] XML docs (`/// <summary>`) on every public class, method, property, and event
- [ ] `[Tooltip]` on every `[SerializeField]` for designer clarity
- [ ] `[Header]` groups for related serialized fields
- [ ] Inline comments on non-obvious logic (the *why*)
- [ ] No commented-out code — use version control

### Clean Code
- [ ] No magic numbers — use `const`, `static readonly`, or `[SerializeField]`
- [ ] Clear, descriptive names following conventions (PascalCase methods, _camelCase private fields)
- [ ] Guard clauses at method entry for invalid inputs
- [ ] No deep nesting (4+ levels) — extract methods or use early returns
- [ ] Single responsibility — one reason to change per class

### Unity Safety
- [ ] `if (this == null) return;` after every `await`
- [ ] Event subscriptions (`+=`) in `OnEnable` with matching unsubscribe (`-=`) in `OnDisable`
- [ ] Component references cached in `Awake`, not fetched per-frame
- [ ] No `Find()`/`FindObjectOfType()` — use `[SerializeField]` injection
- [ ] `[FormerlySerializedAs("oldName")]` added when renaming any serialized field
- [ ] Empty Unity callbacks deleted (`Update`, `Start`, `OnGUI`)
- [ ] `Debug.Log` guarded with `#if UNITY_EDITOR`
- [ ] ScriptableObjects cloned with `Instantiate()` before runtime modification

### Syntax Validation
- [ ] All `using` statements present — no unresolved types
- [ ] Braces, parentheses, and brackets all matched
- [ ] All generic types closed (`List<int>`, not `List<>`)
- [ ] String literals properly escaped
- [ ] No compiler warnings
