# ASSET_POSTPROCESSOR_TEMPLATE.cs

```csharp
using UnityEditor;
using UnityEngine;

namespace _Project.Editor.Automation
{
    /// <summary>
    /// Automates asset import settings based on naming conventions.
    /// </summary>
    public class CustomAssetImporter : AssetPostprocessor
    {
        // Executes before texture is imported
        private void OnPreprocessTexture()
        {
            TextureImporter importer = (TextureImporter)assetImporter;
            string path = assetPath.ToLower();

            // Example Rule: Normal Maps
            if (path.Contains("_normal"))
            {
                importer.textureType = TextureImporterType.NormalMap;
                importer.sRGBTexture = false;
            }
            
            // Example Rule: UI Textures
            if (path.Contains("/ui/"))
            {
                importer.mipmapEnabled = false;
                importer.textureCompression = TextureImporterCompression.Uncompressed;
            }
        }

        // Executes before model is imported
        private void OnPreprocessModel()
        {
            ModelImporter importer = (ModelImporter)assetImporter;
            
            // Default optimizations
            importer.optimizeMesh = true;
            importer.importAnimation = assetPath.Contains("/Animations/");
        }
    }
}
```
