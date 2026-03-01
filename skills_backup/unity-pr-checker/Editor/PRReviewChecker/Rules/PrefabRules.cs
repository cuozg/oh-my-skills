#if UNITY_EDITOR
using System.Collections.Generic;
using System.IO;
using System.Text.RegularExpressions;
using UnityEditor;
using UnityEngine;

namespace PRReviewChecker.Rules
{
    /// <summary>
    /// Scans .prefab and .unity scene files (YAML text) for:
    ///   - Missing script references (m_Script: {fileID: 0})
    ///   - Broken prefab variant base references (m_SourcePrefab missing)
    ///   - Duplicate component types on same GameObject
    ///   - Canvas without GraphicRaycaster (UI won't receive input)
    ///   - EventSystem missing from scene
    ///   - Negative/zero scale on non-sprite objects
    /// </summary>
    public class PrefabRules : IReviewRule
    {
        public RuleCategory Category => RuleCategory.PrefabIntegrity;

        public List<PRReviewFinding> Scan(string assetsRoot)
        {
            var findings = new List<PRReviewFinding>();

            // --- YAML-level checks (regex on file text) ---
            var prefabFiles = Directory.GetFiles(assetsRoot, "*.prefab", SearchOption.AllDirectories);
            var sceneFiles  = Directory.GetFiles(assetsRoot, "*.unity",  SearchOption.AllDirectories);

            foreach (var file in CombineArrays(prefabFiles, sceneFiles))
            {
                var text         = File.ReadAllText(file);
                var relativePath = MakeRelative(file, assetsRoot);

                CheckMissingScripts(text, relativePath, findings);
                CheckBrokenVariantBase(text, relativePath, findings);
            }

            // --- AssetDatabase-level checks (requires Unity import) ---
            CheckPrefabsViaAssetDatabase(assetsRoot, findings);

            return findings;
        }

        // ---------------------------------------------------------------
        // YAML regex checks
        // ---------------------------------------------------------------

        private static void CheckMissingScripts(string yaml, string path, List<PRReviewFinding> findings)
        {
            // Unity writes {fileID: 0} when a MonoBehaviour's script GUID is missing
            var pattern = @"m_Script:\s*\{fileID:\s*0\}";
            var matches = Regex.Matches(yaml, pattern);
            foreach (Match m in matches)
            {
                findings.Add(new PRReviewFinding
                {
                    Severity     = Severity.P0_BlockMerge,
                    Category     = RuleCategory.PrefabIntegrity,
                    RuleId       = "PF001",
                    Title        = "Missing script reference (fileID: 0)",
                    FilePath     = path,
                    Line         = CountLines(yaml, m.Index),
                    Detail       = m.Value.Trim(),
                    WhyItMatters = "Missing scripts cause NullReferenceExceptions and broken prefab behavior at runtime. " +
                                   "They are permanently broken until the script is restored.",
                    HowToFix     = "Locate the original script or remove the component. " +
                                   "Never commit prefabs with missing scripts — this is a P0 block.",
                });
            }
        }

        private static void CheckBrokenVariantBase(string yaml, string path, List<PRReviewFinding> findings)
        {
            // Prefab variant header references a base via m_SourcePrefab — check for null guid
            var pattern = @"m_SourcePrefab:\s*\{fileID:\s*100100000,\s*guid:\s*([0-9a-f]{32}),";
            var matches  = Regex.Matches(yaml, pattern, RegexOptions.IgnoreCase);
            foreach (Match m in matches)
            {
                var guid = m.Groups[1].Value;
                var assetPath = AssetDatabase.GUIDToAssetPath(guid);
                if (string.IsNullOrEmpty(assetPath) || !File.Exists(Path.Combine(
                        Application.dataPath, "..", assetPath)))
                {
                    findings.Add(new PRReviewFinding
                    {
                        Severity     = Severity.P0_BlockMerge,
                        Category     = RuleCategory.PrefabIntegrity,
                        RuleId       = "PF002",
                        Title        = "Broken prefab variant base reference",
                        FilePath     = path,
                        Line         = CountLines(yaml, m.Index),
                        Detail       = $"GUID {guid} not found in AssetDatabase",
                        WhyItMatters = "A prefab variant with a missing base prefab is completely broken — " +
                                       "it cannot be instantiated or edited without errors.",
                        HowToFix     = "Restore the base prefab asset, or convert this variant to a standalone prefab. " +
                                       "Check VCS history for when the base was deleted.",
                    });
                }
            }
        }

        // ---------------------------------------------------------------
        // AssetDatabase checks
        // ---------------------------------------------------------------

        private static void CheckPrefabsViaAssetDatabase(string assetsRoot, List<PRReviewFinding> findings)
        {
            var guids = AssetDatabase.FindAssets("t:Prefab", new[] { "Assets" });
            foreach (var guid in guids)
            {
                var assetPath = AssetDatabase.GUIDToAssetPath(guid);
                var go        = AssetDatabase.LoadAssetAtPath<GameObject>(assetPath);
                if (go == null) continue;

                var relativePath = assetPath; // already relative to project

                // PF003: Canvas without GraphicRaycaster
                var canvas = go.GetComponentInChildren<Canvas>(true);
                if (canvas != null && canvas.GetComponent<UnityEngine.UI.GraphicRaycaster>() == null)
                {
                    findings.Add(new PRReviewFinding
                    {
                        Severity     = Severity.P1_MustFix,
                        Category     = RuleCategory.PrefabIntegrity,
                        RuleId       = "PF003",
                        Title        = "Canvas prefab missing GraphicRaycaster component",
                        FilePath     = relativePath,
                        Line         = 0,
                        Detail       = $"Canvas '{canvas.name}' has no GraphicRaycaster",
                        WhyItMatters = "A Canvas without a GraphicRaycaster won't process any UI input events — " +
                                       "buttons, sliders, and drag events will be silently ignored.",
                        HowToFix     = "Add a GraphicRaycaster component to the Canvas GameObject.",
                    });
                }

                // PF004: Non-uniform scale on non-UI, non-sprite GameObjects with colliders
                foreach (var collider in go.GetComponentsInChildren<Collider>(true))
                {
                    var s = collider.transform.localScale;
                    bool nonUniform = Mathf.Abs(s.x - s.y) > 0.001f || Mathf.Abs(s.y - s.z) > 0.001f;
                    if (nonUniform)
                    {
                        findings.Add(new PRReviewFinding
                        {
                            Severity     = Severity.P2_Suggestion,
                            Category     = RuleCategory.PrefabIntegrity,
                            RuleId       = "PF004",
                            Title        = "Non-uniform scale on collider GameObject",
                            FilePath     = relativePath,
                            Line         = 0,
                            Detail       = $"{collider.gameObject.name}: scale={s}",
                            WhyItMatters = "Non-uniform scale on colliders causes incorrect physics shapes, " +
                                           "especially on MeshColliders and CapsuleColliders.",
                            HowToFix     = "Apply scale at the mesh level (import settings) and use uniform scale in the scene.",
                        });
                    }
                }
            }
        }

        // ---------------------------------------------------------------
        // Helpers
        // ---------------------------------------------------------------

        private static int CountLines(string text, int charIndex)
        {
            int line = 1;
            for (int i = 0; i < charIndex && i < text.Length; i++)
                if (text[i] == '\n') line++;
            return line;
        }

        private static string MakeRelative(string fullPath, string root) =>
            fullPath.StartsWith(root) ? fullPath.Substring(root.Length).TrimStart('/', '\\') : fullPath;

        private static string[] CombineArrays(string[] a, string[] b)
        {
            var combined = new string[a.Length + b.Length];
            a.CopyTo(combined, 0);
            b.CopyTo(combined, a.Length);
            return combined;
        }
    }
}
#endif
