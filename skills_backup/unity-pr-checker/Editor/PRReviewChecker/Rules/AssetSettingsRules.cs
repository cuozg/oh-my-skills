#if UNITY_EDITOR
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;

namespace PRReviewChecker.Rules
{
    /// <summary>
    /// Scans texture and model import settings via AssetDatabase:
    ///   - Textures with Read/Write enabled (doubles VRAM usage)
    ///   - UI sprite textures with mipmaps enabled (wastes memory)
    ///   - Textures larger than 2048 without compression
    ///   - Models with Read/Write meshes enabled
    ///   - Models missing normals (will look flat-shaded)
    ///   - Audio clips with Decompress On Load on large files
    /// </summary>
    public class AssetSettingsRules : IReviewRule
    {
        public RuleCategory Category => RuleCategory.AssetSettings;

        private const int MaxTextureSize  = 2048;
        private const int LargeAudioBytes = 200 * 1024; // 200KB uncompressed

        public List<PRReviewFinding> Scan(string assetsRoot)
        {
            var findings = new List<PRReviewFinding>();

            ScanTextures(findings);
            ScanModels(findings);
            ScanAudio(findings);

            return findings;
        }

        // ---------------------------------------------------------------
        // Textures
        // ---------------------------------------------------------------

        private static void ScanTextures(List<PRReviewFinding> findings)
        {
            var guids = AssetDatabase.FindAssets("t:Texture2D", new[] { "Assets" });
            foreach (var guid in guids)
            {
                var path     = AssetDatabase.GUIDToAssetPath(guid);
                var importer = AssetImporter.GetAtPath(path) as TextureImporter;
                if (importer == null) continue;

                // AS001: Read/Write enabled
                if (importer.isReadable)
                {
                    findings.Add(new PRReviewFinding
                    {
                        Severity     = Severity.P1_MustFix,
                        Category     = RuleCategory.AssetSettings,
                        RuleId       = "AS001",
                        Title        = "Texture Read/Write enabled — doubles VRAM usage",
                        FilePath     = path,
                        Line         = 0,
                        Detail       = path,
                        WhyItMatters = "Read/Write enabled keeps a CPU-side copy of the texture in RAM in addition " +
                                       "to the GPU VRAM copy — effectively doubling memory usage. " +
                                       "On mobile this can cause OOM crashes.",
                        HowToFix     = "Disable Read/Write in Texture Import Settings unless the texture is " +
                                       "explicitly read at runtime (GetPixel, EncodeToJPG, etc.).",
                    });
                }

                // AS002: UI sprite with mipmaps
                if (importer.textureType == TextureImporterType.Sprite && importer.mipmapEnabled)
                {
                    findings.Add(new PRReviewFinding
                    {
                        Severity     = Severity.P1_MustFix,
                        Category     = RuleCategory.AssetSettings,
                        RuleId       = "AS002",
                        Title        = "Sprite texture with mipmaps enabled — wastes ~33% memory",
                        FilePath     = path,
                        Line         = 0,
                        Detail       = path,
                        WhyItMatters = "UI sprites are always rendered at native resolution; mipmap chains " +
                                       "add ~33% memory overhead with no visual benefit.",
                        HowToFix     = "Disable Generate Mip Maps in Texture Import Settings for all Sprite textures.",
                    });
                }

                // AS003: Large texture without compression
                if (importer.maxTextureSize > MaxTextureSize)
                {
                    var settings = importer.GetDefaultPlatformTextureSettings();
                    if (settings.format == TextureImporterFormat.Automatic &&
                        importer.textureCompression == TextureImporterCompression.Uncompressed)
                    {
                        findings.Add(new PRReviewFinding
                        {
                            Severity     = Severity.P1_MustFix,
                            Category     = RuleCategory.AssetSettings,
                            RuleId       = "AS003",
                            Title        = $"Texture >{MaxTextureSize}px imported without compression",
                            FilePath     = path,
                            Line         = 0,
                            Detail       = $"maxTextureSize={importer.maxTextureSize}, compression=Uncompressed",
                            WhyItMatters = "Uncompressed textures at this size can use 16–64MB of VRAM. " +
                                           "On mobile this will OOM kill the app.",
                            HowToFix     = "Set compression to: DXT/BC1 (desktop), ETC2 (Android), ASTC (iOS). " +
                                           "Use platform-specific overrides for best per-platform quality.",
                        });
                    }
                }

                // AS004: Texture not power-of-two (NPOT) without explicit flag
                var tex = AssetDatabase.LoadAssetAtPath<Texture2D>(path);
                if (tex != null)
                {
                    bool isPOT = IsPowerOfTwo(tex.width) && IsPowerOfTwo(tex.height);
                    if (!isPOT && importer.npotScale == TextureImporterNPOTScale.None)
                    {
                        findings.Add(new PRReviewFinding
                        {
                            Severity     = Severity.P2_Suggestion,
                            Category     = RuleCategory.AssetSettings,
                            RuleId       = "AS004",
                            Title        = $"NPOT texture ({tex.width}x{tex.height}) — may fall back to uncompressed on some GPUs",
                            FilePath     = path,
                            Line         = 0,
                            Detail       = $"{tex.width}x{tex.height}",
                            WhyItMatters = "Non-power-of-two textures cannot use block compression (DXT/ETC2) on all platforms. " +
                                           "Some GPUs silently decompress them to RGBA32 at load time.",
                            HowToFix     = "Resize to the nearest power of two, or set NPOT Scale to 'ToNearest' in import settings.",
                        });
                    }
                }
            }
        }

        // ---------------------------------------------------------------
        // Models
        // ---------------------------------------------------------------

        private static void ScanModels(List<PRReviewFinding> findings)
        {
            var guids = AssetDatabase.FindAssets("t:Model", new[] { "Assets" });
            foreach (var guid in guids)
            {
                var path     = AssetDatabase.GUIDToAssetPath(guid);
                var importer = AssetImporter.GetAtPath(path) as ModelImporter;
                if (importer == null) continue;

                // AS005: Read/Write meshes enabled
                if (importer.isReadable)
                {
                    findings.Add(new PRReviewFinding
                    {
                        Severity     = Severity.P1_MustFix,
                        Category     = RuleCategory.AssetSettings,
                        RuleId       = "AS005",
                        Title        = "Mesh Read/Write enabled — doubles CPU memory usage",
                        FilePath     = path,
                        Line         = 0,
                        Detail       = path,
                        WhyItMatters = "Read/Write enabled keeps mesh data in CPU RAM after upload to GPU. " +
                                       "For a 10,000-poly mesh this doubles the memory footprint.",
                        HowToFix     = "Disable Read/Write unless mesh data is modified at runtime " +
                                       "(MeshCollider.sharedMesh, procedural mesh, etc.).",
                    });
                }

                // AS006: Normals import mode set to None on non-simple mesh
                if (importer.importNormals == ModelImporterNormals.None)
                {
                    findings.Add(new PRReviewFinding
                    {
                        Severity     = Severity.P2_Suggestion,
                        Category     = RuleCategory.AssetSettings,
                        RuleId       = "AS006",
                        Title        = "Model importing with normals disabled — will render flat-shaded",
                        FilePath     = path,
                        Line         = 0,
                        Detail       = $"importNormals=None",
                        WhyItMatters = "Meshes without normals cannot respond to lighting — " +
                                       "they will appear uniformly lit (flat-shaded) regardless of material.",
                        HowToFix     = "Set Import Normals to 'Import' (use baked normals from DCC) or " +
                                       "'Calculate' (Unity recalculates from geometry).",
                    });
                }
            }
        }

        // ---------------------------------------------------------------
        // Audio
        // ---------------------------------------------------------------

        private static void ScanAudio(List<PRReviewFinding> findings)
        {
            var guids = AssetDatabase.FindAssets("t:AudioClip", new[] { "Assets" });
            foreach (var guid in guids)
            {
                var path     = AssetDatabase.GUIDToAssetPath(guid);
                var importer = AssetImporter.GetAtPath(path) as AudioImporter;
                if (importer == null) continue;

                var settings = importer.defaultSampleSettings;

                // AS007: Decompress on load for large audio files
                if (settings.loadType == AudioClipLoadType.DecompressOnLoad)
                {
                    var clip = AssetDatabase.LoadAssetAtPath<AudioClip>(path);
                    if (clip != null && clip.samples * 2 > LargeAudioBytes) // rough: 16-bit PCM
                    {
                        findings.Add(new PRReviewFinding
                        {
                            Severity     = Severity.P1_MustFix,
                            Category     = RuleCategory.AssetSettings,
                            RuleId       = "AS007",
                            Title        = "Large audio clip set to Decompress On Load",
                            FilePath     = path,
                            Line         = 0,
                            Detail       = $"~{clip.samples * 2 / 1024}KB uncompressed, loadType=DecompressOnLoad",
                            WhyItMatters = "Decompress On Load decodes the full audio into RAM when loaded. " +
                                           "For music or long ambience tracks this can use 20–100MB+ of RAM.",
                            HowToFix     = "Background music: use 'Streaming'. Short SFX: use 'Compressed In Memory'. " +
                                           "Only use DecompressOnLoad for clips <200KB that play frequently.",
                        });
                    }
                }
            }
        }

        // ---------------------------------------------------------------
        // Helpers
        // ---------------------------------------------------------------

        private static bool IsPowerOfTwo(int n) => n > 0 && (n & (n - 1)) == 0;
    }
}
#endif
