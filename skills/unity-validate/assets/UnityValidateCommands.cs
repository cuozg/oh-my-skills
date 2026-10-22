using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;
using Unity.Pipeline.Commands;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.Rendering;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

/// <summary>
/// unity-validate evidence tools: Editor-only Pipeline CLI commands that turn "it works" into
/// proof (hierarchy trees, rendered PNGs, live values, UI clicks, image facts).
/// Install: copy to Assets/Editor/UnityValidate/UnityValidateCommands.cs, then `unity command recompile`.
/// Everything is read-only except validate_click, which runs game code and is Play Mode only.
/// </summary>
static class UnityValidateCommands
{
    const int k_DefaultWidth = 1080;
    const int k_DefaultHeight = 1920;

    /// <summary>Print a prefab asset's hierarchy. Read-only: works on an isolated copy.</summary>
    [CliCommand("validate_prefab_tree", "Print a prefab asset's hierarchy tree with component types (read-only)", Tags = new[] { "capture" })]
    static string PrefabTree(
        [CliArg("path", "Prefab asset path, e.g. Assets/UI/ShopPopup.prefab", Required = true)] string path,
        [CliArg("components", "Include component type names (default true)")] bool components = true)
    {
        // LoadPrefabContents loads an isolated copy; the asset and open scenes are never touched.
        var root = PrefabUtility.LoadPrefabContents(path);
        try { return BuildTree(root.transform, components); }
        finally { PrefabUtility.UnloadPrefabContents(root); }
    }

    /// <summary>Print the hierarchy of a live GameObject (open scenes, prefab stage, or Play Mode).</summary>
    [CliCommand("validate_scene_tree", "Print the hierarchy tree of a GameObject in the open scenes, prefab stage, or Play Mode (read-only)", Tags = new[] { "capture" })]
    static string SceneTree(
        [CliArg("root", "Hierarchy path, e.g. Canvas/ShopPopup. Empty = every root object")] string root = "",
        [CliArg("components", "Include component type names (default true)")] bool components = true)
    {
        var roots = CollectRoots();
        if (string.IsNullOrEmpty(root))
            return string.Join("\n", roots.Select(r => BuildTree(r.transform, components)));

        var target = FindByPath(roots, root)
            ?? throw new ArgumentException($"GameObject '{root}' not found in the open scenes / prefab stage.");
        return BuildTree(target, components);
    }

    /// <summary>
    /// Render a prefab to PNG inside a throwaway preview scene. UI prefabs are laid out on a temp
    /// world-space canvas sized the way CanvasScaler would size it on a w×h screen, so the shot
    /// matches a real device of that resolution. 3D prefabs get a framed 3/4 camera and a light.
    /// </summary>
    [CliCommand("validate_prefab_shot", "Render a prefab in an isolated preview scene to a PNG (UI prefabs get a temp canvas)", Tags = new[] { "capture" })]
    static object PrefabShot(
        [CliArg("path", "Prefab asset path, e.g. Assets/UI/ShopPopup.prefab", Required = true)] string path,
        [CliArg("output", "Output PNG path (absolute, or relative to the project root)", Required = true)] string output,
        [CliArg("width", "Screen width in pixels. 0 = CanvasScaler reference width, else 1080")] int width = 0,
        [CliArg("height", "Screen height in pixels. 0 = CanvasScaler reference height, else 1920")] int height = 0)
    {
        RequireGpu();
        var asset = AssetDatabase.LoadAssetAtPath<GameObject>(path)
            ?? throw new ArgumentException($"No prefab at '{path}'.");

        var scene = EditorSceneManager.NewPreviewScene();
        RenderTexture rt = null;
        try
        {
            var instance = (GameObject)PrefabUtility.InstantiatePrefab(asset, scene);
            var scaler = instance.GetComponentInChildren<CanvasScaler>(true);
            bool isUI = instance.transform is RectTransform;

            // Size priority: explicit args, then the prefab's own reference resolution, then portrait phone.
            var reference = scaler != null && scaler.uiScaleMode == CanvasScaler.ScaleMode.ScaleWithScreenSize
                ? scaler.referenceResolution
                : new Vector2(width > 0 ? width : k_DefaultWidth, height > 0 ? height : k_DefaultHeight);
            int w = width > 0 ? width : Mathf.RoundToInt(reference.x);
            int h = height > 0 ? height : Mathf.RoundToInt(reference.y);

            var cam = CreateInScene<Camera>("ValidateCamera", scene);
            cam.scene = scene; // a preview-scene camera renders only its own scene
            cam.clearFlags = CameraClearFlags.SolidColor;
            cam.backgroundColor = new Color(0.19f, 0.19f, 0.19f, 1f);
            rt = new RenderTexture(w, h, 24);
            cam.targetTexture = rt;

            if (isUI) FrameUI(instance, scaler, reference, w, h, cam, scene);
            else Frame3D(instance, cam, scene);

            var fullPath = RenderToFile(new[] { cam }, w, h, output);
            return new { path = fullPath, width = w, height = h, mode = isUI ? "ui" : "3d" };
        }
        finally
        {
            // Closing the preview scene destroys everything created in it.
            EditorSceneManager.ClosePreviewScene(scene);
            if (rt != null) { rt.Release(); UnityEngine.Object.DestroyImmediate(rt); }
        }
    }

    /// <summary>
    /// Capture what the player sees: a camera plus every Screen Space Overlay canvas. The built-in
    /// `screenshot` renders the camera only, and overlay canvases never draw into a camera, so most
    /// game UI would be missing. Overlays are switched to Screen Space Camera for the capture and
    /// restored afterwards.
    /// </summary>
    [CliCommand("validate_game_shot", "Capture what the player sees: all game cameras by depth INCLUDING Screen Space Overlay UI, to a PNG", Tags = new[] { "capture" })]
    static object GameShot(
        [CliArg("output", "Output PNG path (absolute, or relative to the project root)", Required = true)] string output,
        [CliArg("width", "Pixel width. 0 = top camera's current width (Game view), else 1080")] int width = 0,
        [CliArg("height", "Pixel height. 0 = top camera's current height (Game view), else 1920")] int height = 0,
        [CliArg("camera", "Capture only this camera (GameObject path). Empty = every enabled screen camera, by depth")] string camera = "")
    {
        RequireGpu();
        // A game often splits world and UI across cameras (e.g. a UI camera for Screen Space Camera
        // canvases), so render every camera that draws to the screen, lowest depth first.
        var cams = string.IsNullOrEmpty(camera)
            ? Camera.allCameras.Where(c => c.targetTexture == null && !IsUrpStackOverlay(c)).OrderBy(c => c.depth).ToArray()
            : new[] { FindByPath(CollectRoots(), camera)?.GetComponent<Camera>() ?? throw new ArgumentException($"No Camera at '{camera}'.") };
        if (cams.Length == 0) throw new InvalidOperationException("No enabled camera renders to the screen.");
        var top = cams[cams.Length - 1];

        int w = width > 0 ? width : (top.pixelWidth > 1 ? top.pixelWidth : k_DefaultWidth);
        int h = height > 0 ? height : (top.pixelHeight > 1 ? top.pixelHeight : k_DefaultHeight);

        var canvases = UnityEngine.Object.FindObjectsByType<Canvas>(FindObjectsInactive.Exclude, FindObjectsSortMode.None);
        // Camera-space canvases size themselves from their camera; re-scale them for the RT size.
        var camCanvases = canvases.Where(c => c.isRootCanvas && c.renderMode == RenderMode.ScreenSpaceCamera && cams.Contains(c.worldCamera)).ToArray();
        var roots = canvases
            .Where(c => c.isRootCanvas && c.renderMode == RenderMode.ScreenSpaceOverlay)
            .Select(c => (canvas: c, plane: c.planeDistance, order: c.sortingOrder, worldCam: c.worldCamera))
            .ToArray();
        // Nested canvases with overrideSorting sort on their own; they need the same offset or they
        // would drop behind their converted root.
        var nested = roots.SelectMany(r => r.canvas.GetComponentsInChildren<Canvas>(false))
            .Where(c => !c.isRootCanvas && c.overrideSorting)
            .Select(c => (canvas: c, order: c.sortingOrder))
            .ToArray();
        var rt = new RenderTexture(w, h, 24);
        var prevTargets = cams.Select(c => c.targetTexture).ToArray();
        try
        {
            foreach (var c in cams) c.targetTexture = rt;
            foreach (var o in roots)
            {
                o.canvas.renderMode = RenderMode.ScreenSpaceCamera;
                o.canvas.worldCamera = top; // overlay draws last, so it rides on the top camera
                o.canvas.planeDistance = top.nearClipPlane + 0.01f;
                // Overlay always draws above camera-space UI; a large order offset keeps that true
                // while preserving the order between overlays.
                o.canvas.sortingOrder = Offset(o.order);
                RefreshScaler(o.canvas);
            }
            foreach (var n in nested) n.canvas.sortingOrder = Offset(n.order);
            foreach (var c in camCanvases) RefreshScaler(c);
            Canvas.ForceUpdateCanvases();
            var fullPath = RenderToFile(cams, w, h, output);
            return new { path = fullPath, width = w, height = h, cameras = cams.Select(c => c.name).ToArray(), overlayCanvases = roots.Length };
        }
        finally
        {
            foreach (var n in nested) n.canvas.sortingOrder = n.order;
            foreach (var o in roots)
            {
                o.canvas.renderMode = RenderMode.ScreenSpaceOverlay;
                o.canvas.worldCamera = o.worldCam;
                o.canvas.planeDistance = o.plane;
                o.canvas.sortingOrder = o.order;
                RefreshScaler(o.canvas);
            }
            for (int i = 0; i < cams.Length; i++) cams[i].targetTexture = prevTargets[i];
            foreach (var c in camCanvases) RefreshScaler(c);
            rt.Release();
            UnityEngine.Object.DestroyImmediate(rt);
        }
    }

    static int Offset(int order) => Mathf.Min(order + 10000, short.MaxValue);

    /// <summary>URP overlay cameras render as part of their base camera's stack, not on their own. Reflection avoids a hard URP reference.</summary>
    static bool IsUrpStackOverlay(Camera c)
    {
        var data = c.GetComponent("UniversalAdditionalCameraData");
        return data != null && data.GetType().GetProperty("renderType")?.GetValue(data)?.ToString() == "Overlay";
    }

    /// <summary>
    /// Click a UI element the way a player would. Refuses targets a player could not click (inactive,
    /// non-interactable, no click handler, or covered by another raycast target) so a pass is real.
    /// </summary>
    [CliCommand("validate_click", "Click a UI element by hierarchy path in Play Mode; fails if a player could not click it", Tags = new[] { "editor/playmode" })]
    static object ClickCommand(
        [CliArg("path", "Hierarchy path, e.g. Canvas/ShopPopup/Btn_Buy", Required = true)] string path)
    {
        if (!Application.isPlaying)
            throw new InvalidOperationException("validate_click runs game code: enter Play Mode first (editor_play).");
        return Click(path, true);
    }

    // Split from the command so the self-test can exercise the checks outside Play Mode, where no
    // EventSystem runs (requireEventSystem = false skips the occlusion raycast).
    static object Click(string path, bool requireEventSystem)
    {
        var target = FindByPath(CollectRoots(), path)
            ?? throw new ArgumentException($"GameObject '{path}' not found.");
        var go = target.gameObject;
        if (!go.activeInHierarchy)
            throw new InvalidOperationException($"'{path}' is inactive: a player cannot click it.");
        var selectable = go.GetComponentInParent<Selectable>();
        if (selectable != null && !selectable.IsInteractable())
            throw new InvalidOperationException($"'{path}' is not interactable ({selectable.GetType().Name}.interactable or a CanvasGroup blocks it).");
        var handler = PressHandler(go)
            ?? throw new InvalidOperationException($"'{path}' has no pointer click/down handler on it or its parents.");

        var es = EventSystem.current;
        if (es == null && requireEventSystem)
            throw new InvalidOperationException("No EventSystem in the scene: a player could not click anything.");
        var data = new PointerEventData(es) { button = PointerEventData.InputButton.Left };
        string occlusion = "unchecked (self-test, no EventSystem)";
        if (es != null && target is RectTransform rect)
        {
            // Raycast at the element's center: if something else is on top, a player would hit that instead.
            var canvas = go.GetComponentInParent<Canvas>()?.rootCanvas;
            Camera eventCam = null;
            if (canvas != null && canvas.renderMode != RenderMode.ScreenSpaceOverlay)
                eventCam = canvas.worldCamera != null ? canvas.worldCamera : Camera.main; // GraphicRaycaster falls back the same way
            data.position = RectTransformUtility.WorldToScreenPoint(eventCam, rect.TransformPoint(rect.rect.center));
            var hits = new List<RaycastResult>();
            es.RaycastAll(data, hits);
            var top = hits.FirstOrDefault().gameObject;
            // The hit must route to the same handler: a child with its own handler (e.g. a close
            // button over the target) means the player would press that instead.
            if (top == null || PressHandler(top) != handler)
                throw new InvalidOperationException($"'{path}' is covered: a click at its center hits '{(top == null ? "nothing" : HierarchyPath(top.transform))}'.");
            data.pointerCurrentRaycast = data.pointerPressRaycast = hits[0];
            occlusion = "clear";
        }

        // Send the full press sequence the EventSystem sends, so EventTrigger and custom
        // PointerDown/Up handlers fire too, not only onClick.
        data.pointerEnter = go;
        data.rawPointerPress = go;
        data.pressPosition = data.position;
        data.eligibleForClick = true;
        ExecuteEvents.ExecuteHierarchy(go, data, ExecuteEvents.pointerEnterHandler);
        data.pointerPress = ExecuteEvents.ExecuteHierarchy(go, data, ExecuteEvents.pointerDownHandler) ?? handler;
        ExecuteEvents.Execute(data.pointerPress, data, ExecuteEvents.pointerUpHandler);
        ExecuteEvents.Execute(ExecuteEvents.GetEventHandler<IPointerClickHandler>(go) ?? handler, data, ExecuteEvents.pointerClickHandler);
        ExecuteEvents.ExecuteHierarchy(go, data, ExecuteEvents.pointerExitHandler);
        return new { clicked = HierarchyPath(handler.transform), occlusion };
    }

    static GameObject PressHandler(GameObject go) =>
        ExecuteEvents.GetEventHandler<IPointerClickHandler>(go) ?? ExecuteEvents.GetEventHandler<IPointerDownHandler>(go);

    /// <summary>
    /// Read a live value as evidence of game state. Fields are read directly (private
    /// [SerializeField] included); properties run their getter, so avoid ones with side effects
    /// (e.g. Renderer.material instantiates; use sharedMaterial).
    /// </summary>
    [CliCommand("validate_probe", "Read a component field/property on a live GameObject; empty member lists readable members", Tags = new[] { "capture" })]
    static object Probe(
        [CliArg("path", "Hierarchy path, e.g. Canvas/HUD/CoinLabel", Required = true)] string path,
        [CliArg("component", "Component type name, e.g. TextMeshProUGUI or PlayerWallet", Required = true)] string component,
        [CliArg("member", "Field/property, dotted for nesting (e.g. wallet.coins, sizeDelta.x). Empty = list members")] string member = "")
    {
        var target = FindByPath(CollectRoots(), path)
            ?? throw new ArgumentException($"GameObject '{path}' not found.");
        var comps = target.GetComponents<Component>().Where(c => c != null).ToArray();
        var comp = comps.FirstOrDefault(c => c.GetType().Name == component || c.GetType().FullName == component)
            ?? throw new ArgumentException($"No component '{component}' on '{path}'. Has: {string.Join(", ", comps.Select(c => c.GetType().Name))}.");

        if (string.IsNullOrEmpty(member))
            return new { path, component = comp.GetType().Name, members = MemberNames(comp.GetType()) };

        object value = comp;
        foreach (var part in member.Split('.'))
            value = ReadMember(value, part);
        return new { path, component = comp.GetType().Name, member, type = value?.GetType().Name ?? "null", value = Format(value) };
    }

    /// <summary>
    /// Report the facts a generated or imported image is judged on. Pixels come from the source
    /// file (not the imported texture, which import may resize or compress); import settings come
    /// from the TextureImporter when the file is a project asset.
    /// </summary>
    [CliCommand("validate_texture", "Report an image's real pixels (size, alpha, opaque bounds) and its import settings (read-only)", Tags = new[] { "assets" })]
    static object TextureInfo(
        [CliArg("path", "Asset path (Assets/...) or any PNG/JPG file path", Required = true)] string path)
    {
        // Unity maps the virtual Assets/ and Packages/ roots to physical folders in Path.GetFullPath
        // (registry packages live under Library/PackageCache).
        bool isAssetPath = path.StartsWith("Assets/") || path.StartsWith("Packages/");
        var file = isAssetPath ? Path.GetFullPath(path) : ResolvePath(path);
        var assetPath = isAssetPath ? path : ToAssetPath(file);
        if (!File.Exists(file)) throw new ArgumentException($"No file at '{file}'.");
        var tex = new Texture2D(2, 2, TextureFormat.RGBA32, false);
        try
        {
            if (!tex.LoadImage(File.ReadAllBytes(file)))
            {
                // PSD/TGA/EXR import fine but LoadImage decodes only PNG/JPG: report import facts only.
                if (!(AssetImporter.GetAtPath(assetPath ?? "") is TextureImporter ti))
                    throw new ArgumentException($"'{path}' is not a PNG/JPG and not an imported texture.");
                ti.GetSourceTextureWidthAndHeight(out var sw, out var sh);
                return new { path, width = sw, height = sh, pixels = "N/A – not PNG/JPG, pixel facts unavailable", import = ImportInfo(assetPath) };
            }
            int w = tex.width, h = tex.height, transparent = 0, partial = 0;
            int minX = w, minY = h, maxX = -1, maxY = -1;
            var px = tex.GetPixels32();
            for (int i = 0; i < px.Length; i++)
            {
                byte a = px[i].a;
                if (a == 0) { transparent++; continue; }
                if (a < 255) partial++;
                int x = i % w, y = h - 1 - i / w; // GetPixels32 is bottom-up; report top-left origin like image editors
                minX = Math.Min(minX, x); maxX = Math.Max(maxX, x);
                minY = Math.Min(minY, y); maxY = Math.Max(maxY, y);
            }
            bool empty = maxX < 0;
            return new
            {
                path,
                width = w,
                height = h,
                transparentPct = Math.Round(100.0 * transparent / px.Length, 2),
                semiTransparentPct = Math.Round(100.0 * partial / px.Length, 2),
                opaqueBounds = empty ? "none (fully transparent)" : $"x={minX} y={minY} w={maxX - minX + 1} h={maxY - minY + 1} (top-left origin)",
                // Content touching the border usually means the image was cropped or has no padding.
                touchesEdge = !empty && (minX == 0 || minY == 0 || maxX == w - 1 || maxY == h - 1),
                import = ImportInfo(assetPath),
            };
        }
        finally { UnityEngine.Object.DestroyImmediate(tex); }
    }

    static object ImportInfo(string assetPath)
    {
        if (assetPath == null || !(AssetImporter.GetAtPath(assetPath) is TextureImporter ti)) return "N/A – not an imported project texture";
        string Platform(string name)
        {
            var s = ti.GetPlatformTextureSettings(name);
            return s.overridden ? $"{s.format} max={s.maxTextureSize}" : "default";
        }
        return new
        {
            textureType = ti.textureType.ToString(),
            spriteMode = ti.spriteImportMode.ToString(),
            pixelsPerUnit = ti.spritePixelsPerUnit,
            spriteBorderLBRT = ti.spriteBorder.ToString(),
            spritePivot = ti.spritePivot.ToString(),
            maxSize = ti.maxTextureSize,
            compression = ti.textureCompression.ToString(),
            mipmaps = ti.mipmapEnabled,
            alphaIsTransparency = ti.alphaIsTransparency,
            sRGB = ti.sRGBTexture,
            readable = ti.isReadable,
            npotScale = ti.npotScale.ToString(),
            filterMode = ti.filterMode.ToString(),
            android = Platform("Android"),
            iOS = Platform("iPhone"),
        };
    }

    static void RequireGpu()
    {
        // -nographics has no GPU: Camera.Render draws nothing and the PNG would be a blank frame.
        // Fail loudly; fake evidence is worse than none.
        if (SystemInfo.graphicsDeviceType == GraphicsDeviceType.Null)
            throw new InvalidOperationException("No graphics device (-nographics). Run in a live Editor or batch mode without -nographics.");
    }

    /// <summary>Render the cameras in order into their shared targetTexture and write it as PNG; returns the absolute path.</summary>
    static string RenderToFile(Camera[] cams, int w, int h, string output)
    {
        var tex = new Texture2D(w, h, TextureFormat.RGB24, false);
        var prevActive = RenderTexture.active;
        try
        {
            foreach (var cam in cams) cam.Render();
            RenderTexture.active = cams[0].targetTexture;
            tex.ReadPixels(new Rect(0, 0, w, h), 0, 0);
            tex.Apply();
            var fullPath = ResolvePath(output);
            Directory.CreateDirectory(Path.GetDirectoryName(fullPath));
            File.WriteAllBytes(fullPath, tex.EncodeToPNG());
            return fullPath;
        }
        finally
        {
            RenderTexture.active = prevActive;
            UnityEngine.Object.DestroyImmediate(tex);
        }
    }

    static string ProjectRoot => Path.GetDirectoryName(Application.dataPath);

    static string ResolvePath(string p) => Path.IsPathRooted(p) ? p : Path.GetFullPath(Path.Combine(ProjectRoot, p));

    static string ToAssetPath(string fullPath)
    {
        var root = ProjectRoot.Replace('\\', '/') + "/";
        var f = fullPath.Replace('\\', '/');
        return f.StartsWith(root, StringComparison.OrdinalIgnoreCase) ? f.Substring(root.Length) : null;
    }

    /// <summary>Re-run CanvasScaler after a render-mode change; OnEnable recomputes the scale factor.</summary>
    static void RefreshScaler(Canvas canvas)
    {
        var scaler = canvas.GetComponent<CanvasScaler>();
        if (scaler == null || !scaler.enabled) return;
        scaler.enabled = false;
        scaler.enabled = true;
    }

    const BindingFlags k_Members = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly;

    /// <summary>Field first, then parameterless property, walking base types so inherited privates resolve.</summary>
    static object ReadMember(object obj, string name)
    {
        if (obj == null) throw new ArgumentException($"Cannot read '{name}' of null.");
        for (var type = obj.GetType(); type != null; type = type.BaseType)
        {
            var f = type.GetField(name, k_Members);
            if (f != null) return f.GetValue(obj);
            var p = type.GetProperty(name, k_Members);
            if (p != null && p.CanRead && p.GetIndexParameters().Length == 0) return p.GetValue(obj);
        }
        throw new ArgumentException($"No field or property '{name}' on {obj.GetType().Name}.");
    }

    /// <summary>Names only: listing values would run every property getter, some with side effects.</summary>
    static string[] MemberNames(Type type)
    {
        var names = new List<string>();
        for (var t = type; t != null && t != typeof(MonoBehaviour) && t != typeof(Behaviour) && t != typeof(Component); t = t.BaseType)
        {
            names.AddRange(t.GetFields(k_Members).Where(f => !f.Name.Contains("<")).Select(f => $"{f.Name}: {f.FieldType.Name}"));
            names.AddRange(t.GetProperties(k_Members).Where(p => p.CanRead && p.GetIndexParameters().Length == 0).Select(p => $"{p.Name}: {p.PropertyType.Name} (property)"));
        }
        return names.Distinct().ToArray();
    }

    static string Format(object v)
    {
        switch (v)
        {
            case null: return "null";
            case UnityEngine.Object o: return o == null ? "null (destroyed)" : $"{o.name} ({o.GetType().Name})";
            case string s: return s;
            case float f: return f.ToString("R", CultureInfo.InvariantCulture);
            case double d: return d.ToString("R", CultureInfo.InvariantCulture);
            case Enum en: return en.ToString(); // before IFormattable: enums reject numeric formats
            // Vector/Color/Rect default to 2 decimals, which hides small differences.
            case IFormattable u when v.GetType().Namespace == "UnityEngine": return u.ToString("F4", CultureInfo.InvariantCulture);
            case IFormattable n: return n.ToString(null, CultureInfo.InvariantCulture);
            case IEnumerable e:
                var items = e.Cast<object>().Take(21).ToList();
                return "[" + string.Join(", ", items.Take(20).Select(Format)) + (items.Count > 20 ? ", …" : "") + "]";
            default: return v.ToString();
        }
    }

    static string HierarchyPath(Transform t) => t.parent == null ? t.name : HierarchyPath(t.parent) + "/" + t.name;

    /// <summary>
    /// Lay the UI out on a world-space canvas whose size mimics CanvasScaler.ScaleWithScreenSize on
    /// a w×h screen, then point an orthographic camera at it. World space avoids depending on
    /// screen-space canvas/scaler updates, which need an Editor frame to run.
    /// </summary>
    static void FrameUI(GameObject instance, CanvasScaler scaler, Vector2 reference, int w, int h, Camera cam, Scene scene)
    {
        float scale = ScaleFactor(scaler, reference, w, h);
        var canvasSize = new Vector2(w, h) / scale;

        var canvas = instance.GetComponent<Canvas>();
        if (canvas == null)
        {
            // Prefab is a panel, not a canvas: host it on a temp canvas like a real screen would.
            canvas = CreateInScene<Canvas>("ValidateCanvas", scene);
            instance.transform.SetParent(canvas.transform, false);

            // A fixed-size component root (button, badge) keeps the offset it had in some demo
            // scene, often off-screen. Center it; stretched roots (screens) keep their real layout.
            var root = (RectTransform)instance.transform;
            if (root.anchorMin == root.anchorMax)
            {
                root.anchorMin = root.anchorMax = new Vector2(0.5f, 0.5f);
                root.anchoredPosition = Vector2.zero;
            }
        }
        canvas.renderMode = RenderMode.WorldSpace;

        var rect = (RectTransform)canvas.transform;
        rect.SetPositionAndRotation(Vector3.zero, Quaternion.identity);
        rect.localScale = Vector3.one;
        rect.pivot = new Vector2(0.5f, 0.5f);
        rect.sizeDelta = canvasSize;

        cam.orthographic = true;
        cam.orthographicSize = canvasSize.y / 2f;
        cam.transform.position = new Vector3(0f, 0f, -100f);
        cam.nearClipPlane = 0.1f;
        cam.farClipPlane = 1000f;

        // Layout groups and TMP regenerate on canvas update; run it before and after the layout pass.
        Canvas.ForceUpdateCanvases();
        LayoutRebuilder.ForceRebuildLayoutImmediate(rect);
        Canvas.ForceUpdateCanvases();
    }

    /// <summary>Same math as CanvasScaler.HandleScaleWithScreenSize.</summary>
    static float ScaleFactor(CanvasScaler scaler, Vector2 reference, int w, int h)
    {
        if (scaler == null || scaler.uiScaleMode != CanvasScaler.ScaleMode.ScaleWithScreenSize) return 1f;
        float sx = w / reference.x, sy = h / reference.y;
        switch (scaler.screenMatchMode)
        {
            case CanvasScaler.ScreenMatchMode.Expand: return Mathf.Min(sx, sy);
            case CanvasScaler.ScreenMatchMode.Shrink: return Mathf.Max(sx, sy);
            default: return Mathf.Pow(2f, Mathf.Lerp(Mathf.Log(sx, 2f), Mathf.Log(sy, 2f), scaler.matchWidthOrHeight));
        }
    }

    /// <summary>Frame every renderer from a 3/4 angle and add a key light (preview scenes have none).</summary>
    static void Frame3D(GameObject instance, Camera cam, Scene scene)
    {
        var renderers = instance.GetComponentsInChildren<Renderer>();
        var bounds = renderers.Length > 0 ? renderers[0].bounds : new Bounds(instance.transform.position, Vector3.one);
        foreach (var r in renderers) bounds.Encapsulate(r.bounds);

        float radius = Mathf.Max(bounds.extents.magnitude, 0.01f);
        cam.fieldOfView = 30f;
        float distance = radius / Mathf.Sin(15f * Mathf.Deg2Rad); // fit the bounding sphere in a 30° FOV
        var forward = new Vector3(1f, -0.6f, 1f).normalized;
        cam.transform.position = bounds.center - forward * distance;
        cam.transform.LookAt(bounds.center);
        cam.nearClipPlane = distance * 0.01f;
        cam.farClipPlane = distance + radius * 2f;

        var light = CreateInScene<Light>("ValidateLight", scene);
        light.type = LightType.Directional;
        light.transform.rotation = Quaternion.Euler(50f, -30f, 0f);
    }

    static T CreateInScene<T>(string name, Scene scene) where T : Component
    {
        var go = new GameObject(name);
        SceneManager.MoveGameObjectToScene(go, scene);
        return go.AddComponent<T>();
    }

    /// <summary>Prefab stage root when one is open, else every loaded scene root (+ DontDestroyOnLoad in Play Mode).</summary>
    static GameObject[] CollectRoots()
    {
        var stage = PrefabStageUtility.GetCurrentPrefabStage();
        if (stage != null) return new[] { stage.prefabContentsRoot };

        var roots = Enumerable.Range(0, SceneManager.sceneCount)
            .Select(SceneManager.GetSceneAt)
            .Where(s => s.isLoaded)
            .SelectMany(s => s.GetRootGameObjects())
            .ToList();

        if (Application.isPlaying)
        {
            // DontDestroyOnLoad roots are only reachable through an object living in that scene.
            var probe = new GameObject("ValidateProbe");
            UnityEngine.Object.DontDestroyOnLoad(probe);
            roots.AddRange(probe.scene.GetRootGameObjects().Where(g => g != probe));
            UnityEngine.Object.DestroyImmediate(probe);
        }
        return roots.ToArray();
    }

    /// <summary>Resolve "Root/Child/Leaf"; Transform.Find also matches inactive children.</summary>
    static Transform FindByPath(GameObject[] roots, string path)
    {
        var parts = path.Trim('/').Split(new[] { '/' }, 2);
        foreach (var r in roots.Where(r => r.name == parts[0]))
        {
            var t = parts.Length == 1 ? r.transform : r.transform.Find(parts[1]);
            if (t != null) return t;
        }
        return null;
    }

    static string BuildTree(Transform root, bool components)
    {
        var sb = new StringBuilder().AppendLine(Label(root, components));
        AppendChildren(sb, root, "", components);
        return sb.ToString().TrimEnd();
    }

    static void AppendChildren(StringBuilder sb, Transform parent, string indent, bool components)
    {
        for (int i = 0; i < parent.childCount; i++)
        {
            var child = parent.GetChild(i);
            bool last = i == parent.childCount - 1;
            sb.Append(indent).Append(last ? "└── " : "├── ").AppendLine(Label(child, components));
            AppendChildren(sb, child, indent + (last ? "    " : "│   "), components);
        }
    }

    /// <summary>"Name (CompA, CompB) [prefab: X.prefab] [inactive]". Transform is skipped: every node has one.</summary>
    static string Label(Transform t, bool components)
    {
        var sb = new StringBuilder(t.name);
        if (components)
        {
            var names = t.GetComponents<Component>()
                .Where(c => !(c is Transform))
                .Select(c => c == null ? "MissingScript!" : c.GetType().Name)
                .ToArray();
            if (names.Length > 0) sb.Append(" (").Append(string.Join(", ", names)).Append(')');
        }
        if (PrefabUtility.IsAnyPrefabInstanceRoot(t.gameObject))
            sb.Append(" [prefab: ").Append(Path.GetFileName(PrefabUtility.GetPrefabAssetPathOfNearestInstanceRoot(t.gameObject))).Append(']');
        if (!t.gameObject.activeSelf) sb.Append(" [inactive]");
        return sb.ToString();
    }
}
