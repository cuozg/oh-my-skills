# Play Mode Test Patterns

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
        var rb = go.AddComponent<Rigidbody>();
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
| `yield return new WaitForSeconds(t)` | Wait real time |
| `yield return new WaitForFixedUpdate()` | Wait physics step |
| `yield return new WaitUntil(() => cond)` | Wait for condition |
| `yield return new WaitForEndOfFrame()` | Wait frame end |

## Scene Loading

```csharp
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
    bullet.AddComponent<Rigidbody>().useGravity = false;
    bullet.GetComponent<Rigidbody>().linearVelocity = Vector3.forward * 10f;
    var wall = GameObject.CreatePrimitive(PrimitiveType.Cube);
    wall.transform.position = Vector3.forward * 3f;
    yield return new WaitForFixedUpdate();
    yield return new WaitForFixedUpdate();
    Physics.Simulate(0.5f);
    yield return null;
}
```

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

## LogAssert — Expect Specific Logs

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
