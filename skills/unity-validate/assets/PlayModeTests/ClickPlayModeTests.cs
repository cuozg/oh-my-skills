using System;
using System.Collections;
using System.Linq;
using System.Reflection;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.TestTools;
using UnityEngine.UI;

// Verifies validate_click's Play Mode paths (EventSystem raycast occlusion, world-space
// camera fallback, full press sequence) that the Edit Mode self-test cannot reach.
public class ClickPlayModeTests
{
    static object Click(string path)
    {
        var t = AppDomain.CurrentDomain.GetAssemblies().Select(a => a.GetType("UnityValidateCommands")).First(x => x != null);
        try { return t.GetMethod("ClickCommand", BindingFlags.Static | BindingFlags.NonPublic).Invoke(null, new object[] { path }); }
        catch (TargetInvocationException e) { throw e.InnerException; }
    }

    static Button MakeButton(Transform parent, string name, Vector2 size, Action onClick)
    {
        var go = new GameObject(name, typeof(RectTransform), typeof(Image), typeof(Button));
        go.transform.SetParent(parent, false);
        ((RectTransform)go.transform).sizeDelta = size;
        var b = go.GetComponent<Button>();
        b.onClick.AddListener(() => onClick());
        return b;
    }

    [UnityTest]
    public IEnumerator Occlusion_WorldSpaceFallback_PressSequence()
    {
        new GameObject("EventSystem", typeof(EventSystem));
        var cam = new GameObject("Main Camera", typeof(Camera)) { tag = "MainCamera" };
        cam.transform.position = new Vector3(0, 0, -10);

        var overlay = new GameObject("Overlay", typeof(RectTransform), typeof(Canvas), typeof(GraphicRaycaster));
        overlay.GetComponent<Canvas>().renderMode = RenderMode.ScreenSpaceOverlay;
        int buy = 0, close = 0, downs = 0;
        var buyBtn = MakeButton(overlay.transform, "Buy", new Vector2(200, 100), () => buy++);
        var trigger = buyBtn.gameObject.AddComponent<EventTrigger>();
        var e = new EventTrigger.Entry { eventID = EventTriggerType.PointerDown };
        e.callback.AddListener(_ => downs++);
        trigger.triggers.Add(e);
        yield return null;

        var r = Click("Overlay/Buy").ToString();
        Assert.That(r, Does.Contain("occlusion = clear"));
        Assert.AreEqual(1, buy, "onClick");
        Assert.AreEqual(1, downs, "PointerDown via EventTrigger");

        // A child with its own handler on top (close button over the target) must count as covered.
        MakeButton(buyBtn.transform, "Close", new Vector2(200, 100), () => close++);
        yield return null;
        var ex = Assert.Throws<InvalidOperationException>(() => Click("Overlay/Buy"));
        Assert.That(ex.Message, Does.Contain("covered").And.Contain("Close"));
        Assert.AreEqual(1, buy, "covered click must not fire");
        UnityEngine.Object.Destroy(buyBtn.transform.Find("Close").gameObject);

        // A full-screen blocker on top must count as covered.
        var blocker = new GameObject("Blocker", typeof(RectTransform), typeof(Image));
        blocker.transform.SetParent(overlay.transform, false);
        var brt = (RectTransform)blocker.transform;
        brt.anchorMin = Vector2.zero; brt.anchorMax = Vector2.one; brt.sizeDelta = Vector2.zero;
        yield return null;
        Assert.Throws<InvalidOperationException>(() => Click("Overlay/Buy"));
        UnityEngine.Object.Destroy(blocker);
        overlay.SetActive(false);

        // World Space canvas with worldCamera unset: must fall back to Camera.main, not report covered.
        var world = new GameObject("World", typeof(RectTransform), typeof(Canvas), typeof(GraphicRaycaster));
        world.GetComponent<Canvas>().renderMode = RenderMode.WorldSpace;
        var wrt = (RectTransform)world.transform;
        wrt.sizeDelta = new Vector2(400, 400);
        wrt.localScale = Vector3.one * 0.01f;
        int worldClicks = 0;
        MakeButton(world.transform, "Play", new Vector2(200, 100), () => worldClicks++);
        yield return null;
        r = Click("World/Play").ToString();
        Assert.That(r, Does.Contain("occlusion = clear"));
        Assert.AreEqual(1, worldClicks);
    }
}
