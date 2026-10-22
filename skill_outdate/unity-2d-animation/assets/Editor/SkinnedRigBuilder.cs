using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEditor.Animations;
using UnityEditor.SceneManagement;
using UnityEditor.U2D.Sprites;
using UnityEngine;
using UnityEngine.Rendering.Universal;
using UnityEngine.U2D;
using UnityEngine.U2D.Animation;

namespace Rig2D.EditorTools
{
    /// <summary>
    /// One-click pipeline: split layers + rig.json (from split_character.py) -> skinned, animated, playable character.
    ///
    /// Character folder layout (Assets/&lt;Name&gt;):  Art/Parts/*.png, Art/rig.json  (inputs)
    ///   -> Animations/{Idle,Walk,Run}.anim + &lt;Name&gt;.controller, Prefabs/&lt;Name&gt;.prefab,
    ///      Physics/NoFriction.physicsMaterial2D, Art/Square.png, Assets/Scenes/&lt;Name&gt;Test.unity
    /// Menu: select the character folder or its rig.json, then Tools ▸ 2D Rig ▸ Build Selected Character.
    /// CLI:  unity command eval 'Rig2D.EditorTools.SkinnedRigBuilder.Build("Assets/&lt;Name&gt;"); return "ok";'
    /// Steps: texture import (Sprite, Single, uncompressed, bottom-left pivot) -> bones + mesh + weights via
    /// ISpriteBoneDataProvider / ISpriteMeshDataProvider -> shared skeleton + SpriteSkin per part ->
    /// clips + Speed Animator -> test scene. Safe to re-run (assets overwritten, clip GUIDs kept).
    /// </summary>
    public static class SkinnedRigBuilder
    {
        // Animator thresholds; Character2DController walk/run speeds must straddle RunThreshold.
        const float WalkThreshold = 0.1f;
        const float RunThreshold = 3f;
        const string ScenesDir = "Assets/Scenes";

        // ---------- JSON model (mirrors split_character.py; flat arrays for JsonUtility) ----------
        [Serializable] class RigData { public string name; public float ppu; public BoneData[] bones; public PartData[] parts; public ColliderData collider; public BoundsData bounds; }
        [Serializable] class BoneData { public string name; public string parent; public float[] head; public float[] tail; }
        [Serializable] class ColliderData { public string direction; public float[] offset; public float[] size; }
        [Serializable] class BoundsData { public float[] min; public float[] max; }
        [Serializable]
        class PartData
        {
            public string name; public int order; public int[] rect; public float[] offset; public string[] bones;
            public float[] vertices; public int[] indices; public int[] edges; public int[] boneIndices; public float[] boneWeights;
        }

        /// <summary>Bone pose in character (Visual) space, units. +X axis points head -> tail.</summary>
        internal struct Pose { public Vector2 head; public float angle; public float length; public string parent; }

        [MenuItem("Tools/2D Rig/Build Selected Character")]
        static void BuildSelected()
        {
            string path = AssetDatabase.GetAssetPath(Selection.activeObject);
            if (string.IsNullOrEmpty(path)) { Debug.LogError("[Rig2D] Select a character folder or its Art/rig.json"); return; }
            // Accept the folder itself or anything inside it (rig.json lives in <root>/Art/).
            string root = AssetDatabase.IsValidFolder(path) ? path : Path.GetDirectoryName(Path.GetDirectoryName(path));
            Build(root.Replace('\\', '/'));
        }

        /// <summary>Builds everything for the character folder (e.g. "Assets/Unicorn").</summary>
        public static void Build(string root)
        {
            // No modal "save changes?" prompt (would block CLI/batch runs): refuse to discard unsaved work instead.
            for (int i = 0; i < EditorSceneManager.sceneCount; i++)
                if (EditorSceneManager.GetSceneAt(i).isDirty)
                    throw new InvalidOperationException("Save or discard changes in the open scene before building.");

            string rigPath = $"{root}/Art/rig.json";
            RigData rig = JsonUtility.FromJson<RigData>(File.ReadAllText(rigPath));
            string name = string.IsNullOrEmpty(rig.name) ? Path.GetFileName(root) : rig.name;
            Dictionary<string, Pose> poses = ComputePoses(rig);

            foreach (string dir in new[] { $"{root}/Animations", $"{root}/Prefabs", $"{root}/Physics", ScenesDir })
                Directory.CreateDirectory(dir);
            AssetDatabase.Refresh();

            foreach (PartData part in rig.parts)
                ImportPart($"{root}/Art/Parts/{part.name}.png", part, rig.ppu, poses);
            Sprite square = CreateSquareSprite($"{root}/Art/Square.png");

            var clips = QuadrupedClipFactory.Build($"{root}/Animations", poses);
            AnimatorController controller = BuildController($"{root}/Animations/{name}.controller", clips);

            BuildScene(root, name, rig, poses, controller, square);
            Debug.Log($"[Rig2D] Build finished: {ScenesDir}/{name}Test.unity");
        }

        // ------------------------------------------------------------------------------------------------
        // Bones
        // ------------------------------------------------------------------------------------------------

        static Dictionary<string, Pose> ComputePoses(RigData rig)
        {
            var poses = new Dictionary<string, Pose>();
            foreach (BoneData b in rig.bones)
            {
                Vector2 h = new(b.head[0], b.head[1]);
                Vector2 d = new Vector2(b.tail[0], b.tail[1]) - h;
                poses[b.name] = new Pose
                {
                    head = h,
                    angle = Mathf.Atan2(d.y, d.x) * Mathf.Rad2Deg,
                    length = d.magnitude,
                    parent = string.IsNullOrEmpty(b.parent) ? null : b.parent,
                };
            }
            return poses;
        }

        /// <summary>Pose of <paramref name="bone"/> relative to <paramref name="parent"/>'s frame (units).</summary>
        static void LocalPose(Pose bone, Pose parent, out Vector2 localPos, out float localAngle)
        {
            Quaternion inv = Quaternion.Inverse(Quaternion.Euler(0, 0, parent.angle));
            localPos = inv * (bone.head - parent.head);
            localAngle = bone.angle - parent.angle;
        }

        // ------------------------------------------------------------------------------------------------
        // Texture import + skinning data (bones, geometry, weights)
        // ------------------------------------------------------------------------------------------------

        static void ImportPart(string path, PartData part, float ppu, Dictionary<string, Pose> poses)
        {
            AssetDatabase.ImportAsset(path, ImportAssetOptions.ForceSynchronousImport);
            var importer = (TextureImporter)AssetImporter.GetAtPath(path);

            // Bottom-left pivot: the part GameObject's local position = rect offset -> 1:1 original layout.
            importer.textureType = TextureImporterType.Sprite;
            importer.spriteImportMode = SpriteImportMode.Single;
            importer.mipmapEnabled = false;
            importer.alphaIsTransparency = true;
            importer.filterMode = FilterMode.Bilinear;
            importer.textureCompression = TextureImporterCompression.Uncompressed;
            importer.maxTextureSize = 2048;   // keep >= largest part, else definitionScale != 1
            var settings = new TextureImporterSettings();
            importer.ReadTextureSettings(settings);
            settings.spritePixelsPerUnit = ppu;
            settings.spriteAlignment = (int)SpriteAlignment.BottomLeft;
            settings.spriteMeshType = SpriteMeshType.FullRect;
            settings.spriteGenerateFallbackPhysicsShape = false;
            importer.SetTextureSettings(settings);
            importer.SaveAndReimport();

            var factory = new SpriteDataProviderFactories();
            factory.Init();
            ISpriteEditorDataProvider dp = factory.GetSpriteEditorDataProviderFromObject(importer);
            dp.InitSpriteEditorDataProvider();          // must precede any Get/Set
            GUID id = dp.GetSpriteRects()[0].spriteID;
            Vector2 offset = new(part.offset[0], part.offset[1]);

            // Root bone: rect pixel space (origin = rect bottom-left; importer subtracts the pivot itself).
            // Child bones: pixels, local to the parent's rotated frame. z = depth.
            var bones = new List<SpriteBone>();
            for (int i = 0; i < part.bones.Length; i++)
            {
                Pose p = poses[part.bones[i]];
                int parentIdx = p.parent == null ? -1 : Array.IndexOf(part.bones, p.parent);
                Vector2 pos;
                float angle;
                if (parentIdx < 0) { pos = (p.head - offset) * ppu; angle = p.angle; }
                else { LocalPose(p, poses[part.bones[parentIdx]], out pos, out angle); pos *= ppu; }
                bones.Add(new SpriteBone
                {
                    name = part.bones[i],
                    guid = GUID.Generate().ToString(),
                    position = new Vector3(pos.x, pos.y, i),
                    rotation = Quaternion.Euler(0, 0, angle),   // default(SpriteBone).rotation is (0,0,0,0)!
                    length = p.length * ppu,
                    parentId = parentIdx,
                    color = new Color32(255, (byte)(60 + 15 * i), 60, 255),
                });
            }
            dp.GetDataProvider<ISpriteBoneDataProvider>().SetBones(id, bones);

            int vCount = part.vertices.Length / 2;
            var verts = new Vertex2DMetaData[vCount];
            for (int i = 0; i < vCount; i++)
            {
                int w = i * 4;
                verts[i] = new Vertex2DMetaData
                {
                    position = new Vector2(part.vertices[i * 2], part.vertices[i * 2 + 1]),
                    boneWeight = new BoneWeight
                    {
                        boneIndex0 = part.boneIndices[w], weight0 = part.boneWeights[w],
                        boneIndex1 = part.boneIndices[w + 1], weight1 = part.boneWeights[w + 1],
                        boneIndex2 = part.boneIndices[w + 2], weight2 = part.boneWeights[w + 2],
                        boneIndex3 = part.boneIndices[w + 3], weight3 = part.boneWeights[w + 3],
                    },
                };
            }
            var edges = new Vector2Int[part.edges.Length / 2];
            for (int i = 0; i < edges.Length; i++)
                edges[i] = new Vector2Int(part.edges[i * 2], part.edges[i * 2 + 1]);

            var mesh = dp.GetDataProvider<ISpriteMeshDataProvider>();
            mesh.SetVertices(id, verts);
            mesh.SetIndices(id, part.indices);
            mesh.SetEdges(id, edges);

            // Apply() only writes the importer; the reimport runs 2D Animation's SpritePostProcess (bindposes).
            dp.Apply();
            importer.SaveAndReimport();

            Sprite sprite = AssetDatabase.LoadAssetAtPath<Sprite>(path);
            int bindPoses = sprite.GetBindPoses().Length;
            if (bindPoses != part.bones.Length)
                Debug.LogError($"[Rig2D] {part.name}: expected {part.bones.Length} bindposes, got {bindPoses}");
        }

        static Sprite CreateSquareSprite(string path)
        {
            if (!File.Exists(path))
            {
                var tex = new Texture2D(4, 4);
                tex.SetPixels(Enumerable.Repeat(Color.white, 16).ToArray());
                File.WriteAllBytes(path, tex.EncodeToPNG());
                UnityEngine.Object.DestroyImmediate(tex);
                AssetDatabase.ImportAsset(path, ImportAssetOptions.ForceSynchronousImport);
            }
            var imp = (TextureImporter)AssetImporter.GetAtPath(path);
            imp.textureType = TextureImporterType.Sprite;
            imp.spriteImportMode = SpriteImportMode.Single;
            imp.spritePixelsPerUnit = 4;          // 4px -> 1 unit, so transform scale = size in units
            imp.filterMode = FilterMode.Point;
            imp.mipmapEnabled = false;
            imp.SaveAndReimport();
            return AssetDatabase.LoadAssetAtPath<Sprite>(path);
        }

        // ------------------------------------------------------------------------------------------------
        // Animator Controller
        // ------------------------------------------------------------------------------------------------

        static AnimatorController BuildController(string path, QuadrupedClipFactory.Clips clips)
        {
            AssetDatabase.DeleteAsset(path);
            var ctrl = AnimatorController.CreateAnimatorControllerAtPath(path);
            ctrl.AddParameter("Speed", AnimatorControllerParameterType.Float);

            AnimatorStateMachine sm = ctrl.layers[0].stateMachine;
            AnimatorState idle = sm.AddState("Idle", new Vector3(300, 0));
            AnimatorState walk = sm.AddState("Walk", new Vector3(300, 120));
            AnimatorState run = sm.AddState("Run", new Vector3(300, 240));
            idle.motion = clips.idle;
            walk.motion = clips.walk;
            run.motion = clips.run;
            sm.defaultState = idle;

            Link(idle, walk, AnimatorConditionMode.Greater, WalkThreshold);
            Link(walk, idle, AnimatorConditionMode.Less, WalkThreshold);
            Link(walk, run, AnimatorConditionMode.Greater, RunThreshold);
            Link(run, walk, AnimatorConditionMode.Less, RunThreshold);
            AssetDatabase.SaveAssets();
            return ctrl;
        }

        static void Link(AnimatorState from, AnimatorState to, AnimatorConditionMode mode, float threshold)
        {
            AnimatorStateTransition t = from.AddTransition(to);
            t.hasExitTime = false;
            t.duration = 0.15f;
            t.AddCondition(mode, threshold, "Speed");
        }

        // ------------------------------------------------------------------------------------------------
        // Character hierarchy + test scene
        // ------------------------------------------------------------------------------------------------

        static void BuildScene(string root, string name, RigData rig, Dictionary<string, Pose> poses,
                               AnimatorController controller, Sprite square)
        {
            var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);

            // Camera + global 2D light (URP 2D renderer: Sprite-Lit materials are black without a light).
            var camGo = new GameObject("Main Camera") { tag = "MainCamera" };
            var cam = camGo.AddComponent<Camera>();
            cam.orthographic = true;
            float height = rig.bounds != null && rig.bounds.max != null ? rig.bounds.max[1] - rig.bounds.min[1] : 2.5f;
            cam.orthographicSize = Mathf.Max(3f, height * 1.3f);
            cam.clearFlags = CameraClearFlags.SolidColor;
            cam.backgroundColor = new Color(0.78f, 0.89f, 0.98f);
            camGo.transform.position = new Vector3(0, 1, -10);
            camGo.AddComponent<AudioListener>();
            camGo.AddComponent<UniversalAdditionalCameraData>();
            var light = new GameObject("Global Light 2D").AddComponent<Light2D>();
            light.lightType = Light2D.LightType.Global;
            light.intensity = 1f;

            // Ground platforms (BoxCollider2D), a lower ledge to walk off, walls at both ends.
            var env = new GameObject("Environment").transform;
            var grass = new Color(0.55f, 0.80f, 0.55f);
            var dirt = new Color(0.62f, 0.50f, 0.42f);
            Block(env, "Ground", square, new Vector2(0, -0.5f), new Vector2(40, 1), grass);
            Block(env, "GroundFill", square, new Vector2(0, -3f), new Vector2(40, 4), dirt, collider: false);
            Block(env, "LowerGround", square, new Vector2(28, -2f), new Vector2(16, 1), grass);
            Block(env, "LowerGroundFill", square, new Vector2(28, -4.5f), new Vector2(16, 4), dirt, collider: false);
            Block(env, "WallLeft", square, new Vector2(-20.5f, 3f), new Vector2(1, 8), dirt);
            Block(env, "WallRight", square, new Vector2(36.5f, 2f), new Vector2(1, 8), dirt);

            GameObject character = BuildCharacter(root, name, rig, poses, controller);

            var follow = camGo.AddComponent<CameraFollow2D>();
            var so = new SerializedObject(follow);
            so.FindProperty("target").objectReferenceValue = character.transform;
            so.ApplyModifiedPropertiesWithoutUndo();
            new GameObject("DebugHUD").AddComponent<AnimationDebugHUD>();

            PrefabUtility.SaveAsPrefabAssetAndConnect(character, $"{root}/Prefabs/{name}.prefab", InteractionMode.AutomatedAction);
            string scenePath = $"{ScenesDir}/{name}Test.unity";
            EditorSceneManager.SaveScene(scene, scenePath);
            var scenes = EditorBuildSettings.scenes.ToList();
            if (!scenes.Any(s => s.path == scenePath))
            {
                scenes.Add(new EditorBuildSettingsScene(scenePath, true));
                EditorBuildSettings.scenes = scenes.ToArray();
            }
        }

        static void Block(Transform parent, string name, Sprite sprite, Vector2 center, Vector2 size, Color color, bool collider = true)
        {
            var go = new GameObject(name);
            go.transform.SetParent(parent, false);
            go.transform.position = center;
            go.transform.localScale = new Vector3(size.x, size.y, 1);
            var sr = go.AddComponent<SpriteRenderer>();
            sr.sprite = sprite;
            sr.color = color;
            sr.sortingOrder = -10;
            if (collider) go.AddComponent<BoxCollider2D>();
        }

        static GameObject BuildCharacter(string root, string name, RigData rig, Dictionary<string, Pose> poses, AnimatorController controller)
        {
            var go = new GameObject(name);

            // Physics on the root, which is never flipped.
            var rb = go.AddComponent<Rigidbody2D>();
            rb.constraints = RigidbodyConstraints2D.FreezeRotation;
            rb.interpolation = RigidbodyInterpolation2D.Interpolate;
            rb.collisionDetectionMode = CollisionDetectionMode2D.Continuous;
            rb.gravityScale = 3f;
            var capsule = go.AddComponent<CapsuleCollider2D>();
            FitCollider(capsule, rig);
            capsule.sharedMaterial = NoFrictionMaterial($"{root}/Physics/NoFriction.physicsMaterial2D");
            go.AddComponent<Character2DController>();

            // Visual child: flipped for facing; owns the Animator so clip paths start at the root bones.
            var visual = new GameObject("Visual").transform;
            visual.SetParent(go.transform, false);
            var animator = visual.gameObject.AddComponent<Animator>();
            animator.runtimeAnimatorController = controller;
            animator.applyRootMotion = false;

            // Shared skeleton matching the sprite bindposes at rest.
            var boneTf = new Dictionary<string, Transform>();
            foreach (BoneData b in rig.bones)
            {
                Pose p = poses[b.name];
                var t = new GameObject(b.name).transform;
                if (p.parent == null)
                {
                    t.SetParent(visual, false);
                    t.localPosition = p.head;
                    t.localRotation = Quaternion.Euler(0, 0, p.angle);
                }
                else
                {
                    t.SetParent(boneTf[p.parent], false);
                    LocalPose(p, poses[p.parent], out Vector2 lp, out float la);
                    t.localPosition = lp;
                    t.localRotation = Quaternion.Euler(0, 0, la);
                }
                boneTf[b.name] = t;
            }

            var parts = new GameObject("Parts").transform;
            parts.SetParent(visual, false);
            foreach (PartData part in rig.parts.OrderBy(p => p.order))
            {
                var pgo = new GameObject(part.name);
                pgo.transform.SetParent(parts, false);
                pgo.transform.localPosition = new Vector3(part.offset[0], part.offset[1], 0);
                var sr = pgo.AddComponent<SpriteRenderer>();
                sr.sprite = AssetDatabase.LoadAssetAtPath<Sprite>($"{root}/Art/Parts/{part.name}.png");
                sr.sortingOrder = part.order;
                var skin = pgo.AddComponent<SpriteSkin>();
                skin.SetRootBone(boneTf[part.bones[0]]);
                SpriteSkinState state = skin.SetBoneTransforms(part.bones.Select(n => boneTf[n]).ToArray());
                if (state != SpriteSkinState.Ready)
                    Debug.LogError($"[Rig2D] SpriteSkin on {part.name} is {state}");
            }
            return go;
        }

        /// <summary>Explicit collider from rig.json, else a capsule fitted to the character bounds (feet at y=0).</summary>
        static void FitCollider(CapsuleCollider2D capsule, RigData rig)
        {
            if (rig.collider != null && rig.collider.size != null && rig.collider.size.Length == 2)
            {
                capsule.direction = rig.collider.direction == "Vertical" ? CapsuleDirection2D.Vertical : CapsuleDirection2D.Horizontal;
                capsule.offset = new Vector2(rig.collider.offset[0], rig.collider.offset[1]);
                capsule.size = new Vector2(rig.collider.size[0], rig.collider.size[1]);
                return;
            }
            Vector2 min = new(rig.bounds.min[0], rig.bounds.min[1]);
            Vector2 max = new(rig.bounds.max[0], rig.bounds.max[1]);
            Vector2 size = new((max.x - min.x) * 0.6f, (max.y - Mathf.Max(min.y, 0f)) * 0.6f);
            capsule.direction = size.x >= size.y ? CapsuleDirection2D.Horizontal : CapsuleDirection2D.Vertical;
            capsule.size = size;
            capsule.offset = new Vector2((min.x + max.x) * 0.5f, size.y * 0.5f);
        }

        static PhysicsMaterial2D NoFrictionMaterial(string path)
        {
            var mat = AssetDatabase.LoadAssetAtPath<PhysicsMaterial2D>(path);
            if (mat == null)
            {
                mat = new PhysicsMaterial2D("NoFriction") { friction = 0f, bounciness = 0f };
                AssetDatabase.CreateAsset(mat, path);
            }
            return mat;
        }
    }
}
