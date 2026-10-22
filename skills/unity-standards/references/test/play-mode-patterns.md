# Play Mode Test Patterns

Use Play Mode only when the proof needs the player loop: MonoBehaviour lifecycle,
coroutines, physics, input, UI events, Animator, or scene loading. Play Mode test
asmdefs leave `includePlatforms` empty (setup: `naming-conventions.md`).
Attribute table: `edit-mode-patterns.md`.

## Basic UnityTest

```csharp
using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

public class PlayerPlayTests
{
    [UnityTest]
    public IEnumerator Player_FallsWithGravity()
    {
        var go = new GameObject("Player");
        go.AddComponent<Rigidbody>();
        float startY = go.transform.position.y;
        yield return new WaitForSeconds(0.5f);
        Assert.Less(go.transform.position.y, startY);
        Object.Destroy(go);
    }
}
```

## Yield Patterns

| Yield | Use |
|-------|-----|
| `yield return null` | Wait one frame |
| `yield return new WaitForSeconds(t)` | Wait scaled game time |
| `yield return new WaitForSecondsRealtime(t)` | Wait unscaled time |
| `yield return new WaitForFixedUpdate()` | Wait physics step |
| `yield return new WaitUntil(() => cond)` | Wait for condition |
| `yield return new WaitForEndOfFrame()` | Wait frame end |

## Scene Loading

The scene must be in the build scene list (Build Profiles in Unity 6).

```csharp
using UnityEngine.SceneManagement;

[UnityTest]
public IEnumerator MainMenu_LoadsCleanly()
{
    yield return SceneManager.LoadSceneAsync("MainMenu");
    var canvas = Object.FindFirstObjectByType<Canvas>();
    Assert.IsNotNull(canvas, "MainMenu must have a Canvas");
}
```

## Physics Simulation

```csharp
[UnityTest]
public IEnumerator Projectile_HitsTarget()
{
    var bullet = GameObject.CreatePrimitive(PrimitiveType.Sphere);
    var rb = bullet.AddComponent<Rigidbody>();
    rb.useGravity = false;
    rb.linearVelocity = Vector3.forward * 10f;   // Unity 6 name (was velocity)
    var wall = GameObject.CreatePrimitive(PrimitiveType.Cube);
    wall.transform.position = Vector3.forward * 3f;

    yield return new WaitForSeconds(0.5f);      // let auto-simulation run

    Assert.Less(bullet.transform.position.z, wall.transform.position.z, "Bullet must stop at the wall");
    Object.Destroy(bullet);
    Object.Destroy(wall);
}
```

For deterministic stepping, set `Physics.simulationMode = SimulationMode.Script`,
call `Physics.Simulate(Time.fixedDeltaTime)` in a loop, and restore the mode in teardown.

## UnitySetUp / UnityTearDown

```csharp
private GameObject _player;

[UnitySetUp]
public IEnumerator SetUp()
{
    yield return SceneManager.LoadSceneAsync("TestScene");
    _player = GameObject.Find("Player");
}

[UnityTearDown]
public IEnumerator TearDown()
{
    if (_player != null) Object.Destroy(_player);
    yield return null;
}
```

## LogAssert - Expect Specific Logs

Works in both modes. An unexpected `Debug.LogError`/exception log fails the test;
call `LogAssert.Expect` before the code that logs.

```csharp
[UnityTest]
public IEnumerator MissingRef_LogsError()
{
    LogAssert.Expect(LogType.Error, "Missing weapon reference");
    var go = new GameObject().AddComponent<WeaponSystem>();
    yield return null; // let Start() run
    Object.Destroy(go.gameObject);
}
```
