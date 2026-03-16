#!/usr/bin/env python3
import json
import tempfile
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).parent))
from generate_structure import generate_manifest, make_asmdef, apply_manifest


def test_make_asmdef_basic():
    result = json.loads(make_asmdef("Game.Core"))
    assert result["name"] == "Game.Core"
    assert result["rootNamespace"] == "Game.Core"
    assert result["references"] == []
    assert result["autoReferenced"] is False
    assert result["overrideReferences"] is False
    assert result["defineConstraints"] == []


def test_make_asmdef_with_references():
    result = json.loads(make_asmdef("Game.Combat", references=["Game.Core"]))
    assert result["references"] == ["Game.Core"]


def test_make_asmdef_test_assembly():
    result = json.loads(make_asmdef("Game.Player.Tests", is_test=True))
    assert result["overrideReferences"] is True
    assert "UNITY_INCLUDE_TESTS" in result["defineConstraints"]
    assert "nunit.framework.dll" in result["precompiledReferences"]


def test_make_asmdef_custom_namespace():
    result = json.loads(make_asmdef("Game.UI", root_namespace="Custom.NS"))
    assert result["rootNamespace"] == "Custom.NS"


def test_generate_manifest_defaults():
    m = generate_manifest("Studio", "RPG")
    assert m["company"] == "Studio"
    assert m["project"] == "RPG"
    assert m["namespace_root"] == "Studio.RPG"
    assert m["features"] == ["Player"]
    assert "Assets/_Project/Core/Scripts" in m["directories"]
    assert "Assets/_Project/Features/Player/Scripts" in m["directories"]
    assert "Assets/_Project/Features/Player/Prefabs" in m["directories"]
    assert "Assets/_Project/Features/Player/Art" in m["directories"]
    assert "Assets/_Project/Features/Player/Animations" in m["directories"]
    assert "Assets/_Project/Features/Player/Tests" in m["directories"]
    assert "Assets/_Project/Infrastructure/Scripts" in m["directories"]
    assert "Assets/_Project/UI" in m["directories"]
    assert "Assets/_Project/Settings" in m["directories"]
    assert "Assets/_Project/Art" in m["directories"]
    assert "Assets/_Project/Audio" in m["directories"]
    assert "Assets/_Project/Scenes" in m["directories"]
    assert "Assets/Plugins" in m["directories"]


def test_generate_manifest_no_resources_folder():
    m = generate_manifest("Studio", "RPG")
    for d in m["directories"]:
        assert "Resources" not in d, f"Resources folder found: {d}"


def test_generate_manifest_asmdef_files():
    m = generate_manifest("Studio", "RPG", features=["Player", "Combat"])
    file_paths = [f["path"] for f in m["files"]]

    assert "Assets/_Project/Core/Scripts/Studio.RPG.Core.asmdef" in file_paths
    assert (
        "Assets/_Project/Features/Player/Scripts/Studio.RPG.Player.asmdef" in file_paths
    )
    assert (
        "Assets/_Project/Features/Player/Tests/Studio.RPG.Player.Tests.asmdef"
        in file_paths
    )
    assert (
        "Assets/_Project/Features/Combat/Scripts/Studio.RPG.Combat.asmdef" in file_paths
    )
    assert (
        "Assets/_Project/Features/Combat/Tests/Studio.RPG.Combat.Tests.asmdef"
        in file_paths
    )
    assert (
        "Assets/_Project/Infrastructure/Scripts/Studio.RPG.Infrastructure.asmdef"
        in file_paths
    )


def test_generate_manifest_core_has_no_deps():
    m = generate_manifest("Studio", "RPG")
    core_file = next(
        f for f in m["files"] if "Core" in f["path"] and f["path"].endswith(".asmdef")
    )
    content = json.loads(core_file["content"])
    assert content["references"] == []


def test_generate_manifest_feature_refs_core():
    m = generate_manifest("Studio", "RPG", features=["Player"])
    feat_file = next(
        f
        for f in m["files"]
        if "Player/Scripts" in f["path"] and f["path"].endswith(".asmdef")
    )
    content = json.loads(feat_file["content"])
    assert "Studio.RPG.Core" in content["references"]


def test_generate_manifest_test_refs_feature_and_core():
    m = generate_manifest("Studio", "RPG", features=["Player"])
    test_file = next(
        f
        for f in m["files"]
        if "Player/Tests" in f["path"] and f["path"].endswith(".asmdef")
    )
    content = json.loads(test_file["content"])
    assert "Studio.RPG.Player" in content["references"]
    assert "Studio.RPG.Core" in content["references"]
    assert content["overrideReferences"] is True


def test_generate_manifest_infra_refs_all():
    m = generate_manifest("Studio", "RPG", features=["Player", "Combat"])
    infra_file = next(
        f
        for f in m["files"]
        if "Infrastructure" in f["path"] and f["path"].endswith(".asmdef")
    )
    content = json.loads(infra_file["content"])
    assert "Studio.RPG.Core" in content["references"]
    assert "Studio.RPG.Player" in content["references"]
    assert "Studio.RPG.Combat" in content["references"]


def test_generate_manifest_gitignore_included():
    m = generate_manifest("Studio", "RPG", include_gitignore=True)
    gitignore = next((f for f in m["files"] if f["path"] == ".gitignore"), None)
    assert gitignore is not None
    assert "[Ll]ibrary/" in gitignore["content"]
    assert "[Uu]tmp/" in gitignore["content"]


def test_generate_manifest_gitignore_excluded():
    m = generate_manifest("Studio", "RPG", include_gitignore=False)
    gitignore = next((f for f in m["files"] if f["path"] == ".gitignore"), None)
    assert gitignore is None


def test_generate_manifest_multiple_features():
    m = generate_manifest("Acme", "Shooter", features=["Player", "Weapons", "AI"])
    dirs = m["directories"]
    assert "Assets/_Project/Features/Player/Scripts" in dirs
    assert "Assets/_Project/Features/Weapons/Scripts" in dirs
    assert "Assets/_Project/Features/AI/Scripts" in dirs


def test_generate_manifest_tree_output():
    m = generate_manifest("Studio", "RPG")
    assert isinstance(m["tree"], str)
    assert len(m["tree"]) > 0
    assert "Assets" in m["tree"]


def test_generate_manifest_namespace_consistency():
    m = generate_manifest("MyStudio", "Platformer", features=["Player"])
    for f in m["files"]:
        if f["path"].endswith(".asmdef"):
            content = json.loads(f["content"])
            assert content["name"].startswith("MyStudio.Platformer")
            assert content["rootNamespace"] == content["name"]


def test_apply_manifest_creates_structure():
    m = generate_manifest("Test", "Game", features=["Player"], include_gitignore=True)
    with tempfile.TemporaryDirectory() as tmpdir:
        created = apply_manifest(m, tmpdir)
        root = Path(tmpdir)

        assert (root / "Assets/_Project/Core/Scripts").is_dir()
        assert (root / "Assets/_Project/Features/Player/Scripts").is_dir()
        assert (root / "Assets/_Project/Features/Player/Prefabs").is_dir()
        assert (root / "Assets/_Project/Features/Player/Tests").is_dir()
        assert (root / "Assets/Plugins").is_dir()

        core_asmdef = root / "Assets/_Project/Core/Scripts/Test.Game.Core.asmdef"
        assert core_asmdef.is_file()
        content = json.loads(core_asmdef.read_text())
        assert content["name"] == "Test.Game.Core"

        assert (root / ".gitignore").is_file()
        assert len(created) > 0


def test_apply_manifest_empty_features():
    m = generate_manifest("Co", "Proj", features=[])
    with tempfile.TemporaryDirectory() as tmpdir:
        apply_manifest(m, tmpdir)
        root = Path(tmpdir)
        assert (root / "Assets/_Project/Core/Scripts").is_dir()
        assert not (root / "Assets/_Project/Features").exists()


def test_generate_manifest_strips_whitespace_features():
    m = generate_manifest("Co", "Proj", features=["  Player  ", "  ", "Combat"])
    feature_dirs = [d for d in m["directories"] if "Features" in d]
    feature_names = set()
    for d in feature_dirs:
        parts = d.split("Features/")
        if len(parts) > 1:
            feature_names.add(parts[1].split("/")[0])
    assert "Player" in feature_names
    assert "Combat" in feature_names
    assert "" not in feature_names


if __name__ == "__main__":
    import pytest

    sys.exit(pytest.main([__file__, "-v"]))
