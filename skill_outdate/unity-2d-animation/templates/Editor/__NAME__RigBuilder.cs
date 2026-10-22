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

namespace __NAME__.EditorTools
{
    /// <summary>
    /// One-click pipeline for the __NAME__ subject: split layers + rig.json -> skinned, animated, testable prefab.
    /// Per-subject copy of the unity-2d-animation template: edit freely when this subject needs something else.
    ///
    /// Inputs : Assets/__NAME__/Art/Parts/*.png + Art/rig.json (from Tools~/split___LOWER__.py)
    /// Outputs: Animations/*.anim + __NAME__.controller, Prefabs/__NAME__.prefab, Physics/NoFriction,
    ///          Art/Square.png, Scenes/__NAME__Test.unity (added to Build Settings)
    /// CLI    : unity command eval '__NAME__.EditorTools.__NAME__RigBuilder.Build(); return "ok";'
    /// Steps  : texture import (Sprite, Single, uncompressed, bottom-left pivot) -> bones + mesh + weights via
    ///          ISpriteBoneDataProvider / ISpriteMeshDataProvider -> shared skeleton + SpriteSkin per part ->
    ///          __NAME__ClipFactory clips + Animator wiring -> test scene. Safe to re-run (clip GUIDs kept).
    /// </summary>
    public static class __NAME__RigBuilder
    {
        const string Root = "Assets/__NAME__";
        // Character = Rigidbody2D + collider + __NAME__Controller (move/run/jump). Object = static, clip preview only.
        // static readonly (not const) so the unused branch doesn't raise unreachable-code warnings.
        static readonly bool HasLocomotion = __HAS_LOCOMOTION__;

        // ---------- JSON model (mirrors the splitter; flat arrays for JsonUtility) ----------
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

        /// <summary>Bone pose in subject (Visual) space, units. +X axis points head -> tail.</summary>
        internal struct Pose { public Vector2 head; public float angle; public float length; public string parent; }

        [MenuItem("Tools/2D Rig/Build __NAME__")]
        public static void Build()
        {
            // No modal "save changes?" prompt (would block CLI runs): refuse to discard unsaved work instead.
            for (int i = 0; i < EditorSceneManager.sceneCount; i++)
                if (EditorSceneManager.GetSceneAt(i).isDirty)
                    throw new InvalidOperationException("Save or discard changes in the open scene before building.");

            RigData rig = JsonUtility.FromJson<RigData>(File.ReadAllText($"{Root}/Art/rig.json"));
            Dictionary<string, Pose> poses = ComputePoses(rig);

            foreach (string dir in new[] { "Animations", "Prefabs", "Physics", "Scenes" })
                Directory.CreateDirectory($"{Root}/{dir}");
            AssetDatabase.Refresh();

            foreach (PartData part in rig.parts)
                ImportPart($"{Root}/Art/Parts/{part.name}.png", part, rig.ppu, poses);
            Sprite square = CreateSquareSprite($"{Root}/Art/Square.png");

            Dictionary<string, AnimationClip> clips = __NAME__ClipFactory.Build($"{Root}/Animations", poses);
            AnimatorController controller = BuildController($"{Root}/Animations/__NAME__.controller", clips);

            BuildScene(rig, poses, controller, square);
            Debug.Log($"[__NAME__RigBuilder] Build finished: {Root}/Scenes/__NAME__Test.unity");
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
            importer.maxTextureSize = 4096;   // keep >= largest part, else definitionScale != 1 and bones scale
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
                Debug.LogError($"[__NAME__RigBuilder] {part.name}: expected {part.bones.Length} bindposes, got {bindPoses}");
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
        // Animator Controller: one state per clip (named like the clip); __NAME__ClipFactory.Wire adds the
        // parameters + transitions that are specific to this subject.
        // ------------------------------------------------------------------------------------------------

        static AnimatorController BuildController(string path, Dictionary<string, AnimationClip> clips)
        {
            AssetDatabase.DeleteAsset(path);
            var ctrl = AnimatorController.CreateAnimatorControllerAtPath(path);
            AnimatorStateMachine sm = ctrl.layers[0].stateMachine;
            var states = new Dictionary<string, AnimatorState>();
            int row = 0;
            foreach (var kv in clips)
            {
                AnimatorState s = sm.AddState(kv.Key, new Vector3(300 + 300 * (row / 6), 120 * (row % 6)));
                s.motion = kv.Value;
                states[kv.Key] = s;
                row++;
            }
            sm.defaultState = states[clips.Keys.First()];   // first clip = entry state
            __NAME__ClipFactory.Wire(ctrl, states);
            AssetDatabase.SaveAssets();
            return ctrl;
        }

        // ------------------------------------------------------------------------------------------------
        // Subject hierarchy + test scene
        // ------------------------------------------------------------------------------------------------

        static void BuildScene(RigData rig, Dictionary<string, Pose> poses, AnimatorController controller, Sprite square)
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
            camGo.transform.position = new Vector3(0, height * 0.5f, -10);
            camGo.AddComponent<AudioListener>();
            camGo.AddComponent<UniversalAdditionalCameraData>();
            var light = new GameObject("Global Light 2D").AddComponent<Light2D>();
            light.lightType = Light2D.LightType.Global;
            light.intensity = 1f;

            // Ground (BoxCollider2D). Characters also get a lower ledge to drop off and walls at both ends.
            var env = new GameObject("Environment").transform;
            var grass = new Color(0.55f, 0.80f, 0.55f);
            var dirt = new Color(0.62f, 0.50f, 0.42f);
            Block(env, "Ground", square, new Vector2(0, -0.5f), new Vector2(40, 1), grass);
            Block(env, "GroundFill", square, new Vector2(0, -3f), new Vector2(40, 4), dirt, collider: false);
            if (HasLocomotion)
            {
                Block(env, "LowerGround", square, new Vector2(28, -2f), new Vector2(16, 1), grass);
                Block(env, "LowerGroundFill", square, new Vector2(28, -4.5f), new Vector2(16, 4), dirt, collider: false);
                Block(env, "WallLeft", square, new Vector2(-20.5f, 3f), new Vector2(1, 8), dirt);
                Block(env, "WallRight", square, new Vector2(36.5f, 2f), new Vector2(1, 8), dirt);
            }

            GameObject subject = BuildSubject(rig, poses, controller);

            if (HasLocomotion)
            {
                var follow = camGo.AddComponent<CameraFollow2D>();
                var so = new SerializedObject(follow);
                so.FindProperty("target").objectReferenceValue = subject.transform;
                so.ApplyModifiedPropertiesWithoutUndo();
            }
            new GameObject("DebugHUD").AddComponent<__NAME__DebugHUD>();

            PrefabUtility.SaveAsPrefabAssetAndConnect(subject, $"{Root}/Prefabs/__NAME__.prefab", InteractionMode.AutomatedAction);
            string scenePath = $"{Root}/Scenes/__NAME__Test.unity";
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

        static GameObject BuildSubject(RigData rig, Dictionary<string, Pose> poses, AnimatorController controller)
        {
            var go = new GameObject("__NAME__");

            if (HasLocomotion)
            {
                // Physics on the root, which is never flipped.
                var rb = go.AddComponent<Rigidbody2D>();
                rb.constraints = RigidbodyConstraints2D.FreezeRotation;
                rb.interpolation = RigidbodyInterpolation2D.Interpolate;
                rb.collisionDetectionMode = CollisionDetectionMode2D.Continuous;
                rb.gravityScale = 3f;
                var capsule = go.AddComponent<CapsuleCollider2D>();
                FitCollider(capsule, rig);
                capsule.sharedMaterial = NoFrictionMaterial($"{Root}/Physics/NoFriction.physicsMaterial2D");
                // Looked up by name so object subjects (no controller script) still compile; TypeCache also
                // finds it when the project uses asmdefs.
                Type ctrlType = TypeCache.GetTypesDerivedFrom<MonoBehaviour>()
                    .FirstOrDefault(t => t.FullName == "__NAME__.__NAME__Controller");
                if (ctrlType != null) go.AddComponent(ctrlType);
                else Debug.LogError("[__NAME__RigBuilder] __NAME__Controller not found (HasLocomotion = true)");
            }

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
                sr.sprite = AssetDatabase.LoadAssetAtPath<Sprite>($"{Root}/Art/Parts/{part.name}.png");
                sr.sortingOrder = part.order;
                var skin = pgo.AddComponent<SpriteSkin>();
                skin.SetRootBone(boneTf[part.bones[0]]);
                SpriteSkinState state = skin.SetBoneTransforms(part.bones.Select(n => boneTf[n]).ToArray());
                if (state != SpriteSkinState.Ready)
                    Debug.LogError($"[__NAME__RigBuilder] SpriteSkin on {part.name} is {state}");
            }
            return go;
        }

        /// <summary>Explicit collider from rig.json, else a capsule fitted to the subject bounds (feet at y=0).</summary>
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
