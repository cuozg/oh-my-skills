using UnityEngine;
using UnityEditor;
using System.IO;

/// <summary>
/// Configures TextureImporter for AI-generated sprites via CoPlay MCP execute_script.
/// Args: { "path", "spriteMode", "pixelsPerUnit", "filterMode", "maxSize", "compression" }
/// </summary>
public static class SpriteImportConfigurator
{
    public static string Execute(Newtonsoft.Json.Linq.JObject args)
    {
        string path = args["path"]?.ToString();
        if (string.IsNullOrEmpty(path))
            return "ERROR: 'path' argument is required.";

        if (!File.Exists(path))
            return $"ERROR: File not found at '{path}'.";

        TextureImporter importer = AssetImporter.GetAtPath(path) as TextureImporter;
        if (importer == null)
            return $"ERROR: Could not get TextureImporter for '{path}'.";

        string spriteMode = args["spriteMode"]?.ToString() ?? "single";
        importer.textureType = TextureImporterType.Sprite;
        importer.spriteImportMode = spriteMode.ToLower() switch
        {
            "multiple" => SpriteImportMode.Multiple,
            "polygon" => SpriteImportMode.Polygon,
            _ => SpriteImportMode.Single
        };

        int ppu = args["pixelsPerUnit"]?.Value<int>() ?? 100;
        importer.spritePixelsPerUnit = ppu;

        string filterStr = args["filterMode"]?.ToString() ?? "Bilinear";
        importer.filterMode = filterStr.ToLower() switch
        {
            "point" => FilterMode.Point,
            "trilinear" => FilterMode.Trilinear,
            _ => FilterMode.Bilinear
        };

        int maxSize = args["maxSize"]?.Value<int>() ?? 256;
        int[] validSizes = { 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192 };
        int closestSize = 256;
        int minDiff = int.MaxValue;
        foreach (int s in validSizes)
        {
            int diff = Mathf.Abs(s - maxSize);
            if (diff < minDiff) { minDiff = diff; closestSize = s; }
        }

        string compressionStr = args["compression"]?.ToString() ?? "Normal";
        TextureImporterCompression compression = compressionStr.ToLower() switch
        {
            "none" => TextureImporterCompression.Uncompressed,
            "low" => TextureImporterCompression.CompressedLQ,
            "high" => TextureImporterCompression.CompressedHQ,
            _ => TextureImporterCompression.Compressed
        };

        importer.alphaIsTransparency = true;
        importer.mipmapEnabled = false;
        importer.wrapMode = TextureWrapMode.Clamp;
        importer.npotScale = TextureImporterNPOTScale.None;

        TextureImporterPlatformSettings defaultSettings = importer.GetDefaultPlatformTextureSettings();
        defaultSettings.maxTextureSize = closestSize;
        defaultSettings.textureCompression = compression;
        defaultSettings.format = TextureImporterFormat.Automatic;
        importer.SetPlatformTextureSettings(defaultSettings);

        TextureImporterPlatformSettings androidSettings = importer.GetPlatformTextureSettings("Android");
        androidSettings.overridden = true;
        androidSettings.maxTextureSize = closestSize;
        androidSettings.format = TextureImporterFormat.ASTC_6x6;
        androidSettings.textureCompression = compression;
        importer.SetPlatformTextureSettings(androidSettings);

        TextureImporterPlatformSettings iosSettings = importer.GetPlatformTextureSettings("iPhone");
        iosSettings.overridden = true;
        iosSettings.maxTextureSize = closestSize;
        iosSettings.format = TextureImporterFormat.ASTC_6x6;
        iosSettings.textureCompression = compression;
        importer.SetPlatformTextureSettings(iosSettings);

        importer.SaveAndReimport();

        return $"OK: Configured '{path}' — SpriteMode={spriteMode}, PPU={ppu}, Filter={filterStr}, MaxSize={closestSize}, Compression={compressionStr}, Alpha=true, Mipmaps=off, Mobile=ASTC_6x6";
    }
}
