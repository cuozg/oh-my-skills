using System;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;
using UnityEditor;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.UI;

/// <summary>
/// Self-test for UnityValidateCommands. Builds throwaway prefabs, scene objects, and an image,
/// calls every validate_* command, and asserts real output: tree text, pixel geometry, clicks,
/// live values, image facts, and error paths. It writes result.txt plus PNGs to -validateOut
/// (default /tmp/unity-validate-selftest), deletes its temp assets, and exits 0 or 1.
///   unity run &lt;project&gt; -- -executeMethod UnityValidateSelfTest.Run [-nographics] [-validateOut &lt;dir&gt;]
/// Under -nographics, shots must throw (no GPU); without it, shots must render correctly.
/// </summary>
public static class UnityValidateSelfTest
{
    const string TmpDir = "Assets/Editor/UnityValidate/_selftest";
    static readonly Color32 k_Bg = new Color32(48, 48, 48, 255); // prefab-shot background
    static readonly Type k_Cmd = Type.GetType("UnityValidateCommands, Assembly-CSharp-Editor");
    static readonly StringBuilder s_Log = new StringBuilder();
    static int s_Fail;
    static string s_Out;

    public static void Run()
    {
        s_Out = ArgValue("-validateOut") ?? "/tmp/unity-validate-selftest"; // never Temp/: Unity wipes it on exit
        bool noGpu = SystemInfo.graphicsDeviceType == GraphicsDeviceType.Null;
        try
        {
            Directory.CreateDirectory(s_Out);
            Log($"unity={Application.unityVersion} graphics={SystemInfo.graphicsDeviceType} commands={(k_Cmd != null ? "found" : "MISSING")}");
            Directory.CreateDirectory(TmpDir);
            var canvas = MakeScalerCanvas();
            var badge = MakeOffsetBadge();
            var cube = MakeCube();
            var image = MakeImage();

            // --- Trees
            Check("prefab tree lists components + inactive", () =>
            {
                var t = (string)Call("PrefabTree", canvas, true);
                return t.Contains("ScalerCanvas (Canvas, CanvasScaler)") && t.Contains("Hidden [inactive]") ? null : t;
            });
            Check("prefab tree without components", () =>
            {
                var t = (string)Call("PrefabTree", canvas, false);
                return !t.Contains("CanvasScaler") && t.Contains("└── Panel") ? null : t;
            });
            var live = new GameObject("LiveRoot");
            new GameObject("Child").transform.SetParent(live.transform, false);
            live.transform.GetChild(0).gameObject.SetActive(false);
            Check("scene tree resolves inactive child path", () =>
            {
                var t = (string)Call("SceneTree", "LiveRoot/Child", true);
                return t == "Child [inactive]" ? null : t;
            });

            // --- Live scene for game shot / click / probe
            var ui = MakeLiveOverlayUI(out var clicks);

            // --- Shots
            if (noGpu)
            {
                Throws<InvalidOperationException>("prefab shot throws without GPU", () => Call("PrefabShot", canvas, s_Out + "/x.png", 0, 0));
                Throws<InvalidOperationException>("game shot throws without GPU", () => Call("GameShot", s_Out + "/x.png", 0, 0, ""));
            }
            else
            {
                Check("prefab shot matches CanvasScaler math (800px panel @ 1170 wide, match width)", () =>
                {
                    var tex = Shot(canvas, "canvas_1170x2532", 1170, 2532);
                    return Near(RedWidth(tex), 800f * 1170f / 1080f, 3) && tex.width == 1170 ? null : $"red={RedWidth(tex)}";
                });
                Check("fixed-size root with demo offset is centered", () =>
                {
                    var tex = Shot(badge, "badge_default", 0, 0);
                    var c = tex.GetPixel(tex.width / 2, tex.height / 2);
                    return c.r > 0.9f && c.g > 0.9f ? null : $"center={c}";
                });
                Check("3d shot frames the object", () =>
                {
                    var tex = Shot(cube, "cube_512", 512, 512);
                    float fg = tex.GetPixels32().Count(p => !Same(p, k_Bg)) / (float)(512 * 512);
                    return fg > 0.1f && fg < 0.95f ? null : $"foreground={fg:P0}";
                });
                Check("game shot: all cameras + overlay UI on top + nested sorting, scaled, then restored", () =>
                {
                    var path = Path.Combine(s_Out, "game_1170x2532.png");
                    var r = Call("GameShot", path, 1170, 2532, "");
                    var tex = Load(path);
                    float scale = 1170f / 1080f;
                    int red = RedWidth(tex);
                    // Blue (1000px, UI camera canvas, order 100) sits under red (800px, overlay): only its sides show.
                    int blue = Row(tex, tex.height / 2).Count(p => p.b > 200 && p.r < 50 && p.g < 50);
                    int green = tex.GetPixels32().Count(p => p.g > 200 && p.r < 50 && p.b < 50);
                    var nested = ui.GetComponentsInChildren<Canvas>().First(c => !c.isRootCanvas);
                    bool restored = ui.renderMode == RenderMode.ScreenSpaceOverlay && ui.sortingOrder == 5 && nested.sortingOrder == 7;
                    bool ok = Near(red, 800 * scale, 3) && Near(blue, 200 * scale, 4) && green > 0 && restored;
                    return ok ? null : $"red={red} blue={blue} green={green} restored={restored} {r}";
                });
            }

            // --- Click (checks run via the internal Click; the command itself is Play Mode only)
            // Occlusion (EventSystem raycast) needs Play Mode; it is covered by the PlayMode check in tools.md.
            Throws<InvalidOperationException>("click command refuses Edit Mode", () => Call("ClickCommand", "OverlayCanvas/Panel/Buy"));
            Throws<InvalidOperationException>("click requires an EventSystem", () => Call("Click", "OverlayCanvas/Panel/Buy", true));
            Check("click fires the button once", () =>
            {
                Call("Click", "OverlayCanvas/Panel/Buy", false);
                return clicks[0] == 1 ? null : $"clicks={clicks[0]}";
            });
            Check("click sends PointerDown (EventTrigger fires)", () =>
            {
                Call("Click", "OverlayCanvas/Panel/Trigger", false);
                return clicks[1] == 1 ? null : $"pointerDowns={clicks[1]}";
            });
            Throws<InvalidOperationException>("click refuses non-interactable", () => Call("Click", "OverlayCanvas/Panel/Locked", false));
            Throws<InvalidOperationException>("click refuses inactive", () => Call("Click", "OverlayCanvas/Panel/Hidden", false));
            Throws<InvalidOperationException>("click refuses non-clickable", () => Call("Click", "OverlayCanvas/Panel", false));

            // --- Probe
            Check("probe reads nested property", () =>
            {
                var r = Call("Probe", "OverlayCanvas/Panel", "RectTransform", "sizeDelta.x").ToString();
                return r.Contains("value = 800") ? null : r;
            });
            Check("probe formats Unity structs invariantly at 4 decimals", () =>
            {
                var r = Call("Probe", "OverlayCanvas/Panel", "RectTransform", "sizeDelta").ToString();
                return r.Contains("value = (800.0000, 400.0000)") ? null : r;
            });
            Check("probe formats enums by name", () =>
            {
                var r = Call("Probe", "OverlayCanvas", "Canvas", "renderMode").ToString();
                return r.Contains("value = ScreenSpaceOverlay") ? null : r;
            });
            Check("probe reads private serialized field", () =>
            {
                var r = Call("Probe", "OverlayCanvas/Panel/Locked", "Button", "m_Interactable").ToString();
                return r.Contains("value = False") ? null : r;
            });
            Check("probe lists members without values", () =>
            {
                var r = Call("Probe", "OverlayCanvas/Panel", "Image", "");
                var members = (string[])r.GetType().GetProperty("members").GetValue(r);
                return members.Any(m => m.StartsWith("m_Sprite")) ? null : string.Join(",", members);
            });
            Throws<ArgumentException>("probe rejects missing component", () => Call("Probe", "OverlayCanvas/Panel", "Nope", "x"));
            Throws<ArgumentException>("probe rejects missing member", () => Call("Probe", "OverlayCanvas/Panel", "Image", "nope"));

            // --- Texture
            Check("texture reports size, alpha, opaque bounds, import", () =>
            {
                var r = Call("TextureInfo", image).ToString();
                bool ok = r.Contains("width = 64") && r.Contains("height = 32")
                    && r.Contains("opaqueBounds = x=10 y=5 w=10 h=10") && r.Contains("touchesEdge = False")
                    && r.Contains("textureType = Sprite");
                return ok ? null : r;
            });
            Check("texture outside the project has no import info", () =>
            {
                var file = Path.Combine(s_Out, "outside.png");
                File.Copy(image, file, true);
                var r = Call("TextureInfo", file).ToString();
                return r.Contains("not an imported project texture") ? null : r;
            });
            Throws<ArgumentException>("texture rejects missing file", () => Call("TextureInfo", "Assets/none.png"));
            var pkgPng = AssetDatabase.FindAssets("t:Texture2D", new[] { "Packages" })
                .Select(AssetDatabase.GUIDToAssetPath).FirstOrDefault(pp => pp.EndsWith(".png"));
            if (pkgPng == null) Log("SKIP texture in Packages/: no package PNG in this project");
            else Check("texture resolves a Packages/ path with import info", () =>
            {
                var r = Call("TextureInfo", pkgPng).ToString();
                return r.Contains("textureType = ") ? null : r;
            });

            // --- Error paths
            Throws<ArgumentException>("tree rejects missing prefab", () => Call("PrefabTree", "Assets/none.prefab", true));
            Throws<ArgumentException>("scene tree rejects missing root", () => Call("SceneTree", "Nope/Missing", true));
            if (!noGpu)
                Throws<ArgumentException>("shot rejects missing prefab", () => Call("PrefabShot", "Assets/none.prefab", s_Out + "/x.png", 0, 0));
        }
        catch (Exception e) { s_Fail++; Log("HARNESS FAIL " + e); }
        finally
        {
            AssetDatabase.DeleteAsset(TmpDir);
            Log($"FAILURES={s_Fail}");
            File.WriteAllText(Path.Combine(s_Out, "result.txt"), s_Log.ToString());
            EditorApplication.Exit(s_Fail == 0 ? 0 : 1);
        }
    }

    static object Call(string method, params object[] args)
    {
        try { return k_Cmd.GetMethod(method, BindingFlags.Static | BindingFlags.NonPublic).Invoke(null, args); }
        catch (TargetInvocationException e) { throw e.InnerException; }
    }

    /// <summary>Run a check; it returns null on pass or a failure detail.</summary>
    static void Check(string name, Func<string> check)
    {
        try
        {
            var detail = check();
            if (detail != null) s_Fail++;
            Log($"{(detail == null ? "PASS" : "FAIL")} {name}{(detail == null ? "" : ": " + detail)}");
        }
        catch (Exception e) { s_Fail++; Log($"FAIL {name}: {e.GetType().Name}: {e.Message}"); }
    }

    static void Throws<T>(string name, Action act) where T : Exception
    {
        try { act(); s_Fail++; Log($"FAIL {name}: no exception"); }
        catch (T e) { Log($"PASS {name}: {e.Message}"); }
        catch (Exception e) { s_Fail++; Log($"FAIL {name}: wrong exception {e.GetType().Name}: {e.Message}"); }
    }

    static Texture2D Shot(string prefab, string file, int w, int h)
    {
        var path = Path.Combine(s_Out, file + ".png");
        Call("PrefabShot", prefab, path, w, h);
        return Load(path);
    }

    static Texture2D Load(string path)
    {
        var tex = new Texture2D(2, 2);
        tex.LoadImage(File.ReadAllBytes(path));
        return tex;
    }

    static Color32[] Row(Texture2D tex, int y) =>
        Enumerable.Range(0, tex.width).Select(x => (Color32)tex.GetPixel(x, y)).ToArray();

    /// <summary>Count of pure-red pixels on the middle row: the 800px reference panel's on-screen width.</summary>
    static int RedWidth(Texture2D tex) => Row(tex, tex.height / 2).Count(p => p.r > 200 && p.g < 50 && p.b < 50);

    static bool Near(float a, float b, float tolerance) => Mathf.Abs(a - b) <= tolerance;

    static bool Same(Color32 a, Color32 b) => Math.Abs(a.r - b.r) + Math.Abs(a.g - b.g) + Math.Abs(a.b - b.b) <= 6;

    static void Log(string line) => s_Log.AppendLine(line);

    static string ArgValue(string flag)
    {
        var args = Environment.GetCommandLineArgs();
        int i = Array.IndexOf(args, flag);
        return i >= 0 && i + 1 < args.Length ? args[i + 1] : null;
    }

    /// <summary>Canvas root with CanvasScaler (1080x1920, match width), an 800x400 red panel, an inactive child.</summary>
    static string MakeScalerCanvas()
    {
        var go = new GameObject("ScalerCanvas", typeof(RectTransform), typeof(Canvas), typeof(CanvasScaler));
        SetScaler(go.GetComponent<CanvasScaler>());
        var panel = AddPanel(go.transform);
        var hidden = new GameObject("Hidden", typeof(RectTransform));
        hidden.transform.SetParent(panel.transform, false);
        hidden.SetActive(false);
        return Save(go, "ScalerCanvas");
    }

    /// <summary>
    /// Live scene: world camera (depth 0) + UI camera (depth 1) with a camera-space canvas (order 100)
    /// holding a 1000x100 blue bar, and an overlay canvas (order 5) holding the 800x400 red panel with
    /// a nested override-sorting canvas (order 7, green), and Buy / Trigger / Locked / Hidden controls.
    /// clicks[0] counts Buy clicks, clicks[1] counts Trigger PointerDowns.
    /// </summary>
    static Canvas MakeLiveOverlayUI(out int[] clicks)
    {
        var camGo = new GameObject("Main Camera", typeof(Camera)) { tag = "MainCamera" };
        camGo.transform.position = new Vector3(0, 0, -10);
        var cam = camGo.GetComponent<Camera>();
        cam.clearFlags = CameraClearFlags.SolidColor;
        cam.backgroundColor = Color.black;

        var uiCam = new GameObject("UICam", typeof(Camera)).GetComponent<Camera>();
        uiCam.clearFlags = CameraClearFlags.Depth;
        uiCam.depth = 1;
        var camCanvasGo = new GameObject("CamCanvas", typeof(RectTransform), typeof(Canvas), typeof(CanvasScaler));
        var camCanvas = camCanvasGo.GetComponent<Canvas>();
        camCanvas.renderMode = RenderMode.ScreenSpaceCamera;
        camCanvas.worldCamera = uiCam;
        camCanvas.planeDistance = 5;
        camCanvas.sortingOrder = 100;
        SetScaler(camCanvasGo.GetComponent<CanvasScaler>());
        var bar = AddPanel(camCanvasGo.transform);
        bar.name = "BlueBar";
        ((RectTransform)bar.transform).sizeDelta = new Vector2(1000, 100);
        bar.GetComponent<Image>().color = Color.blue;

        var go = new GameObject("OverlayCanvas", typeof(RectTransform), typeof(Canvas), typeof(CanvasScaler), typeof(GraphicRaycaster));
        var canvas = go.GetComponent<Canvas>();
        canvas.renderMode = RenderMode.ScreenSpaceOverlay;
        canvas.sortingOrder = 5;
        SetScaler(go.GetComponent<CanvasScaler>());
        var panel = AddPanel(go.transform);

        var badge = new GameObject("NestedSorting", typeof(RectTransform), typeof(Canvas), typeof(Image));
        badge.transform.SetParent(panel.transform, false);
        var badgeRt = (RectTransform)badge.transform;
        badgeRt.anchorMin = badgeRt.anchorMax = new Vector2(1f, 0f);
        badgeRt.sizeDelta = new Vector2(50, 50);
        badgeRt.anchoredPosition = new Vector2(-40, 40);
        badge.GetComponent<Image>().color = Color.green;
        var badgeCanvas = badge.GetComponent<Canvas>();
        badgeCanvas.overrideSorting = true;
        badgeCanvas.sortingOrder = 7;

        var counter = new int[2];
        clicks = counter;
        AddButton(panel.transform, "Buy", true).onClick.AddListener(() => counter[0]++);
        var trigger = new GameObject("Trigger", typeof(RectTransform), typeof(Image), typeof(UnityEngine.EventSystems.EventTrigger));
        trigger.transform.SetParent(panel.transform, false);
        ((RectTransform)trigger.transform).sizeDelta = new Vector2(10, 10);
        ((RectTransform)trigger.transform).anchoredPosition = new Vector2(0, 150); // off the middle row RedWidth samples
        var entry = new UnityEngine.EventSystems.EventTrigger.Entry { eventID = UnityEngine.EventSystems.EventTriggerType.PointerDown };
        entry.callback.AddListener(_ => counter[1]++);
        trigger.GetComponent<UnityEngine.EventSystems.EventTrigger>().triggers.Add(entry);
        AddButton(panel.transform, "Locked", false);
        AddButton(panel.transform, "Hidden", true).gameObject.SetActive(false);
        return canvas;
    }

    static void SetScaler(CanvasScaler scaler)
    {
        scaler.uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize;
        scaler.referenceResolution = new Vector2(1080, 1920);
        scaler.matchWidthOrHeight = 0f;
    }

    static GameObject AddPanel(Transform parent)
    {
        var panel = new GameObject("Panel", typeof(RectTransform), typeof(Image));
        panel.transform.SetParent(parent, false);
        ((RectTransform)panel.transform).sizeDelta = new Vector2(800, 400);
        panel.GetComponent<Image>().color = Color.red;
        return panel;
    }

    // Buttons sit in the panel's top-left corner so they never cover the middle row RedWidth samples.
    static Button AddButton(Transform parent, string name, bool interactable)
    {
        var go = new GameObject(name, typeof(RectTransform), typeof(Image), typeof(Button));
        go.transform.SetParent(parent, false);
        var rt = (RectTransform)go.transform;
        rt.anchorMin = rt.anchorMax = new Vector2(0f, 1f);
        rt.sizeDelta = new Vector2(10, 10);
        rt.anchoredPosition = new Vector2(10, -10);
        go.GetComponent<Image>().color = Color.red;
        var button = go.GetComponent<Button>();
        button.interactable = interactable;
        button.transition = Selectable.Transition.None;
        return button;
    }

    /// <summary>Component-style prefab (no Canvas) whose root carries an off-screen demo offset.</summary>
    static string MakeOffsetBadge()
    {
        var go = new GameObject("Badge", typeof(RectTransform), typeof(Image));
        var rt = (RectTransform)go.transform;
        rt.sizeDelta = new Vector2(200, 200);
        rt.anchoredPosition = new Vector2(-2000, 1500);
        return Save(go, "Badge");
    }

    static string MakeCube() => Save(GameObject.CreatePrimitive(PrimitiveType.Cube), "Cube");

    /// <summary>64x32 transparent PNG with an opaque 10x10 block at top-left (10,5), imported as Sprite.</summary>
    static string MakeImage()
    {
        var tex = new Texture2D(64, 32, TextureFormat.RGBA32, false);
        tex.SetPixels32(Enumerable.Repeat(new Color32(0, 0, 0, 0), 64 * 32).ToArray());
        for (int x = 10; x < 20; x++)
            for (int yTop = 5; yTop < 15; yTop++)
                tex.SetPixel(x, 31 - yTop, Color.white); // SetPixel is bottom-up
        tex.Apply();
        var path = $"{TmpDir}/Generated.png";
        File.WriteAllBytes(path, tex.EncodeToPNG());
        UnityEngine.Object.DestroyImmediate(tex);
        AssetDatabase.ImportAsset(path);
        var importer = (TextureImporter)AssetImporter.GetAtPath(path);
        importer.textureType = TextureImporterType.Sprite;
        importer.SaveAndReimport();
        return path;
    }

    static string Save(GameObject go, string name)
    {
        var path = $"{TmpDir}/{name}.prefab";
        PrefabUtility.SaveAsPrefabAsset(go, path);
        UnityEngine.Object.DestroyImmediate(go);
        return path;
    }
}
