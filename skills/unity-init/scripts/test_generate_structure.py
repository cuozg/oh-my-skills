#!/usr/bin/env python3
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from generate_structure import (
    CLAUDE_BEGIN,
    CLAUDE_END,
    apply_manifest,
    detect_project_info,
    generate_manifest,
    make_asmdef,
    merge_managed_block,
    to_identifier,
)

CO, PJ = "Acme", "Galaxy"
NS = f"{CO}.{PJ}"
ROOT = f"Assets/_{PJ}"


def _file(m, suffix):
    return next(f for f in m["files"] if f["path"].endswith(suffix))


def _refs(m, suffix):
    return json.loads(_file(m, suffix)["content"])["references"]


# ── make_asmdef ──────────────────────────────────────────────────
def test_make_asmdef_basic():
    result = json.loads(make_asmdef(f"{NS}.Core"))
    assert result["name"] == f"{NS}.Core"
    assert result["rootNamespace"] == f"{NS}.Core"
    assert result["references"] == []
    assert result["autoReferenced"] is True
    assert result["overrideReferences"] is False
    assert result["defineConstraints"] == []
    assert result["includePlatforms"] == []


def test_make_asmdef_with_references():
    result = json.loads(make_asmdef(f"{NS}.Features.Board", references=[f"{NS}.Core", f"{NS}.Events"]))
    assert f"{NS}.Core" in result["references"]
    assert f"{NS}.Events" in result["references"]


def test_make_asmdef_editor_only():
    result = json.loads(make_asmdef(f"{NS}.Editor", editor_only=True))
    assert result["includePlatforms"] == ["Editor"]
    assert result["autoReferenced"] is True


def test_make_asmdef_test_assembly():
    result = json.loads(make_asmdef(f"{PJ}.Tests", is_test=True, auto_referenced=False))
    assert result["overrideReferences"] is True
    assert result["autoReferenced"] is False
    assert "UNITY_INCLUDE_TESTS" in result["defineConstraints"]
    assert "nunit.framework.dll" in result["precompiledReferences"]
    assert result["includePlatforms"] == []  # PlayMode by default


def test_make_asmdef_test_editor_only():
    result = json.loads(make_asmdef(f"{PJ}.EditMode.Tests", is_test=True, auto_referenced=False, editor_only=True))
    assert result["includePlatforms"] == ["Editor"]
    assert "UNITY_INCLUDE_TESTS" in result["defineConstraints"]


def test_make_asmdef_custom_namespace():
    result = json.loads(make_asmdef(f"{NS}.UI", root_namespace="Custom.NS"))
    assert result["rootNamespace"] == "Custom.NS"


# ── to_identifier ────────────────────────────────────────────────
def test_to_identifier_cleans_display_names():
    assert to_identifier("My Cool Game!") == "MyCoolGame"
    assert to_identifier("acme-studio") == "AcmeStudio"
    assert to_identifier("3D Racer") == "_3DRacer"
    assert to_identifier("  ") == ""


def test_generate_manifest_sanitizes_names():
    m = generate_manifest("Acme Studio", "Space Game")
    assert m["namespace_root"] == "AcmeStudio.SpaceGame"
    assert "Assets/_SpaceGame/Scripts/Core" in m["directories"]


def test_generate_manifest_rejects_empty_names():
    try:
        generate_manifest("!!!", PJ)
    except ValueError:
        return
    raise AssertionError("expected ValueError for empty company")


# ── generate_manifest: structure ─────────────────────────────────
def test_generate_manifest_defaults_are_generic():
    m = generate_manifest(CO, PJ)
    assert m["company"] == CO
    assert m["project"] == PJ
    assert m["namespace_root"] == NS
    # No game-specific defaults
    assert m["features"] == []
    assert m["ui_controllers"] == []
    assert m["sdk"] is None
    dirs = m["directories"]
    for d in [
        "Assets/Scenes", "Assets/Settings/Build Profiles", "Assets/Settings/Scenes",
        "Assets/Tests/EditMode", "Assets/Tests/PlayMode",
        f"{ROOT}/Audio", f"{ROOT}/Datas/Events", f"{ROOT}/Datas/Levels", f"{ROOT}/Editor",
        f"{ROOT}/Prefabs/GamePlay", f"{ROOT}/Prefabs/Services", f"{ROOT}/Prefabs/UI", f"{ROOT}/Scenes",
        f"{ROOT}/Scripts/Bootstrap", f"{ROOT}/Scripts/Core", f"{ROOT}/Scripts/Events",
        f"{ROOT}/Scripts/Models", f"{ROOT}/Scripts/Systems", f"{ROOT}/Scripts/ViewModels",
    ]:
        assert d in dirs, d


def test_generate_manifest_feature_and_controller_dirs():
    m = generate_manifest(CO, PJ, features=["Board"], ui_controllers=["HUD"])
    assert f"{ROOT}/Scripts/Features/Board/Scripts" in m["directories"]
    assert f"{ROOT}/Scripts/ViewControllers/HUD/Scripts" in m["directories"]


def test_generate_manifest_no_resources_folder():
    m = generate_manifest(CO, PJ, features=["Board"])
    for d in m["directories"]:
        assert "Resources" not in d, f"Resources folder found: {d}"


def test_generate_manifest_no_plugins_folder():
    m = generate_manifest(CO, PJ, features=["Board"])
    for d in m["directories"]:
        assert "Plugins" not in d, f"Plugins folder auto-generated: {d}"


def test_generate_manifest_asmdef_files():
    m = generate_manifest(CO, PJ, features=["Board", "Match"], ui_controllers=["HUD", "Popups"])
    paths = [f["path"] for f in m["files"]]
    for p in [
        f"{ROOT}/Scripts/Core/{NS}.Core.asmdef",
        f"{ROOT}/Scripts/Events/{NS}.Events.asmdef",
        f"{ROOT}/Scripts/Models/{NS}.Models.asmdef",
        f"{ROOT}/Scripts/Systems/{NS}.Systems.asmdef",
        f"{ROOT}/Scripts/ViewModels/{NS}.ViewModels.asmdef",
        f"{ROOT}/Scripts/Features/Board/Scripts/{NS}.Features.Board.asmdef",
        f"{ROOT}/Scripts/Features/Match/Scripts/{NS}.Features.Match.asmdef",
        f"{ROOT}/Scripts/ViewControllers/HUD/Scripts/{NS}.ViewControllers.HUD.asmdef",
        f"{ROOT}/Scripts/ViewControllers/Popups/Scripts/{NS}.ViewControllers.Popups.asmdef",
        f"{ROOT}/Scripts/ViewControllers/{NS}.ViewControllers.asmdef",
        f"{ROOT}/Scripts/Bootstrap/{NS}.Bootstrap.asmdef",
        f"{ROOT}/Editor/{NS}.Editor.asmdef",
        f"Assets/Tests/EditMode/{NS}.EditMode.Tests.asmdef",
        f"Assets/Tests/PlayMode/{NS}.PlayMode.Tests.asmdef",
    ]:
        assert p in paths, p


def test_generate_manifest_feature_docs_use_namespace():
    m = generate_manifest(CO, PJ, features=["Board"])
    paths = [f["path"] for f in m["files"]]
    assert f"{ROOT}/Scripts/Features/Board/README.md" in paths
    agents = _file(m, "Features/Board/AGENTS.md")["content"]
    assert f"`{NS}.Events`" in agents
    assert "TenCrush" not in agents


def test_generate_manifest_project_docs():
    m = generate_manifest(CO, PJ)
    paths = [f["path"] for f in m["files"]]
    assert f"{ROOT}/README.md" in paths
    assert f"{ROOT}/AGENTS.md" in paths


# ── generate_manifest: topology ──────────────────────────────────
def test_core_and_events_have_no_deps():
    m = generate_manifest(CO, PJ)
    assert _refs(m, f"{NS}.Core.asmdef") == []
    assert _refs(m, f"{NS}.Events.asmdef") == []


def test_models_refs_core():
    assert _refs(generate_manifest(CO, PJ), f"{NS}.Models.asmdef") == [f"{NS}.Core"]


def test_feature_refs_core_events_only():
    refs = _refs(generate_manifest(CO, PJ, features=["Board", "Match"]), f"{NS}.Features.Board.asmdef")
    assert refs == [f"{NS}.Core", f"{NS}.Events"]


def test_viewmodels_refs_core_events():
    refs = _refs(generate_manifest(CO, PJ), f"{NS}.ViewModels.asmdef")
    assert f"{NS}.Core" in refs and f"{NS}.Events" in refs


def test_editor_refs_features_and_editor_only():
    m = generate_manifest(CO, PJ, features=["Board", "Match"])
    parsed = json.loads(_file(m, f"{NS}.Editor.asmdef")["content"])
    assert parsed["includePlatforms"] == ["Editor"]
    assert f"{NS}.Features.Board" in parsed["references"]
    assert f"{NS}.Features.Match" in parsed["references"]


def test_bootstrap_refs_only_generated_features():
    refs = _refs(generate_manifest(CO, PJ, features=["Player"]), f"{NS}.Bootstrap.asmdef")
    assert refs == [f"{NS}.Core", f"{NS}.Events", f"{NS}.Features.Player"]


def test_bootstrap_has_no_missing_feature_refs():
    m = generate_manifest(CO, PJ, features=["Player", "Enemy"])
    asm_names = {json.loads(f["content"])["name"] for f in m["files"] if f["path"].endswith(".asmdef")}
    for ref in _refs(m, f"{NS}.Bootstrap.asmdef"):
        assert ref in asm_names, f"Bootstrap references missing assembly {ref}"


def test_viewcontroller_root_refs_submodules():
    refs = _refs(generate_manifest(CO, PJ, ui_controllers=["HUD", "Popups"]), f"{NS}.ViewControllers.asmdef")
    assert f"{NS}.ViewModels" in refs
    assert f"{NS}.ViewControllers.HUD" in refs
    assert f"{NS}.ViewControllers.Popups" in refs


def test_tests_setup():
    m = generate_manifest(CO, PJ, features=["Board"])
    parsed = json.loads(_file(m, f"{NS}.EditMode.Tests.asmdef")["content"])
    assert parsed["includePlatforms"] == ["Editor"]
    assert parsed["autoReferenced"] is False
    assert "UNITY_INCLUDE_TESTS" in parsed["defineConstraints"]
    assert "nunit.framework.dll" in parsed["precompiledReferences"]
    assert f"{NS}.Features.Board" in parsed["references"]
    parsed_p = json.loads(_file(m, f"{NS}.PlayMode.Tests.asmdef")["content"])
    assert parsed_p["includePlatforms"] == []
    assert f"{NS}.Bootstrap" in parsed_p["references"]


# ── .gitignore / SDK / misc ──────────────────────────────────────
def test_gitignore_included_keeps_claude_dir_tracked():
    m = generate_manifest(CO, PJ, include_gitignore=True)
    content = next(f for f in m["files"] if f["path"] == ".gitignore")["content"]
    assert "[Ll]ibrary/" in content
    assert "[Uu]ser[Ss]ettings/" in content
    assert ".claude/settings.local.json" in content
    assert "\n.claude/\n" not in content


def test_gitignore_excluded():
    m = generate_manifest(CO, PJ, include_gitignore=False)
    assert not any(f["path"] == ".gitignore" for f in m["files"])


def test_sdk_scaffold():
    m = generate_manifest(CO, PJ, sdk="CoreKit")
    assert m["sdk"]["namespace"] == f"{CO}.CoreKit"
    for d in ["Assets/_CoreKit/Scripts/Core", "Assets/_CoreKit/Scripts/Events", "Assets/_CoreKit/Editor"]:
        assert d in m["directories"]
    assert _refs(m, f"{CO}.CoreKit.Core.asmdef") == []
    assert json.loads(_file(m, f"{CO}.CoreKit.Editor.asmdef")["content"])["includePlatforms"] == ["Editor"]


def test_no_sdk_by_default():
    m = generate_manifest(CO, PJ)
    assert m["sdk"] is None
    assert not any("_CoreKit" in d for d in m["directories"])


def test_strips_whitespace_features():
    m = generate_manifest(CO, PJ, features=["  Board  ", "  ", "Match"])
    assert m["features"] == ["Board", "Match"]


def test_empty_features():
    m = generate_manifest(CO, PJ, features=[])
    assert f"{ROOT}/Scripts/Features" not in m["directories"]
    assert f"{ROOT}/Scripts/Core" in m["directories"]


def test_empty_ui_controllers():
    m = generate_manifest(CO, PJ, ui_controllers=[])
    assert f"{ROOT}/Scripts/ViewControllers" in m["directories"]
    assert not any("ViewControllers/HUD" in f["path"] for f in m["files"])


def test_namespace_consistency():
    m = generate_manifest("MyStudio", "Platformer", features=["Player"])
    for f in m["files"]:
        if f["path"].endswith(".asmdef"):
            content = json.loads(f["content"])
            assert content["name"].startswith("MyStudio.Platformer")
            assert content["rootNamespace"] == content["name"]


def test_tree_output():
    m = generate_manifest(CO, PJ)
    assert isinstance(m["tree"], str) and ROOT in m["tree"]


def test_no_features_still_generates_bootstrap_editor():
    paths = [f["path"] for f in generate_manifest(CO, PJ, features=[])["files"]]
    assert f"{ROOT}/Scripts/Bootstrap/{NS}.Bootstrap.asmdef" in paths
    assert f"{ROOT}/Editor/{NS}.Editor.asmdef" in paths


# ── CLAUDE.md ────────────────────────────────────────────────────
def _claude(m):
    return next(f for f in m["files"] if f["path"] == "CLAUDE.md")


def test_claude_md_generated_by_default_as_managed_block():
    f = _claude(generate_manifest(CO, PJ))
    assert f["mode"] == "managed-block"
    assert f["content"].startswith(CLAUDE_BEGIN)
    assert f["content"].rstrip().endswith(CLAUDE_END)


def test_claude_md_can_be_disabled():
    m = generate_manifest(CO, PJ, include_claude_md=False)
    assert not any(f["path"] == "CLAUDE.md" for f in m["files"])


def test_claude_md_has_mandatory_cli_and_skill_rules():
    c = _claude(generate_manifest(CO, PJ))["content"]
    assert "## MANDATORY — Unity CLI" in c
    assert "## MANDATORY — Unity Skills" in c
    for token in ["unity status", "unity command", "unity test", "unity pipeline list",
                  "--caller plugin --skill", "unity:unity-cli"]:
        assert token in c, token
    for skill in ["unity-standards", "unity-editor", "unity-test-unit", "unity-debug", "unity-log",
                  "unity-review-pr", "unity-technical", "unity-costing", "unity-wbs", "unity-document"]:
        assert f"`{skill}`" in c, skill


def test_claude_md_reflects_inputs_without_hardcoding():
    m = generate_manifest(CO, PJ, features=["Player"], ui_controllers=["HUD"], sdk="CoreKit",
                          pipeline="HDRP", unity_version="6000.3.1f1")
    c = _claude(m)["content"]
    assert "6000.3.1f1" in c
    assert "HDRP" in c
    assert f"`{NS}`" in c
    assert "`Player`" in c and "`HUD`" in c
    assert "Assets/_CoreKit/" in c
    assert f"{NS}.Events" in c
    for leaked in ["ZenoGames", "TenCrush", "ZenoSDK"]:
        assert leaked not in c


def test_claude_md_default_version_when_unknown():
    c = _claude(generate_manifest(CO, PJ))["content"]
    assert "Unity 6 LTS" in c
    assert "_none yet_" in c  # no features listed


def test_claude_md_compile_regex_is_escaped():
    c = _claude(generate_manifest(CO, PJ))["content"]
    assert "error CS[0-9]{4}" in c


# ── merge_managed_block ──────────────────────────────────────────
BLOCK = f"{CLAUDE_BEGIN}\nNEW\n{CLAUDE_END}\n"


def test_merge_creates_when_missing():
    assert merge_managed_block(None, BLOCK) == BLOCK


def test_merge_appends_and_keeps_user_content():
    out = merge_managed_block("# My rules\nKeep me.\n", BLOCK)
    assert out.startswith("# My rules\nKeep me.\n")
    assert out.endswith(BLOCK)


def test_merge_replaces_only_block():
    existing = f"# Top\n\n{CLAUDE_BEGIN}\nOLD\n{CLAUDE_END}\n\n# Bottom\n"
    out = merge_managed_block(existing, BLOCK)
    assert "OLD" not in out and "NEW" in out
    assert out.startswith("# Top\n") and out.rstrip().endswith("# Bottom")


def test_merge_is_idempotent():
    once = merge_managed_block("# Mine\n", BLOCK)
    assert merge_managed_block(once, BLOCK) == once


# ── detect_project_info ──────────────────────────────────────────
def _fake_project(tmp: Path, deps: dict):
    (tmp / "ProjectSettings").mkdir(parents=True)
    (tmp / "Packages").mkdir()
    (tmp / "ProjectSettings/ProjectSettings.asset").write_text(
        "PlayerSettings:\n  companyName: Acme Studio\n  productName: Space Game\n")
    (tmp / "ProjectSettings/ProjectVersion.txt").write_text(
        "m_EditorVersion: 6000.0.47f1\nm_EditorVersionWithRevision: 6000.0.47f1 (abc)\n")
    (tmp / "Packages/manifest.json").write_text(json.dumps({"dependencies": deps}))


def test_detect_project_info_reads_unity_files():
    with tempfile.TemporaryDirectory() as d:
        _fake_project(Path(d), {"com.unity.render-pipelines.universal": "17.0.3"})
        info = detect_project_info(d)
    assert info == {"company": "AcmeStudio", "project": "SpaceGame",
                    "unity_version": "6000.0.47f1", "pipeline": "URP"}


def test_detect_pipeline_variants():
    cases = [
        ({"com.unity.render-pipelines.high-definition": "17.0.3"}, "HDRP"),
        ({"com.unity.render-pipelines.universal": "17.0.3", "com.unity.feature.2d": "2.0.1"}, "URP2D"),
        ({"com.unity.ugui": "2.0.0"}, "Built-in"),
    ]
    for deps, expected in cases:
        with tempfile.TemporaryDirectory() as d:
            _fake_project(Path(d), deps)
            assert detect_project_info(d)["pipeline"] == expected


def test_detect_project_info_empty_dir():
    with tempfile.TemporaryDirectory() as d:
        assert detect_project_info(d) == {}
    assert detect_project_info(None) == {}


# ── apply_manifest ───────────────────────────────────────────────
def test_apply_manifest_creates_structure():
    m = generate_manifest(CO, PJ, features=["Board"], include_gitignore=True)
    with tempfile.TemporaryDirectory() as tmpdir:
        result = apply_manifest(m, tmpdir)
        root = Path(tmpdir)
        for d in [f"{ROOT}/Scripts/Core", f"{ROOT}/Scripts/Features/Board/Scripts",
                  f"{ROOT}/Scripts/Bootstrap", f"{ROOT}/Editor", "Assets/Tests/EditMode"]:
            assert (root / d).is_dir(), d
        core = root / f"{ROOT}/Scripts/Core/{NS}.Core.asmdef"
        assert json.loads(core.read_text())["name"] == f"{NS}.Core"
        assert (root / f"{ROOT}/Scripts/Features/Board/AGENTS.md").is_file()
        assert (root / ".gitignore").is_file()
        assert (root / "CLAUDE.md").read_text().startswith(CLAUDE_BEGIN)
        assert result["created"] and not result["skipped"]


def test_apply_manifest_never_overwrites_existing_files():
    m = generate_manifest(CO, PJ, features=["Board"], include_gitignore=True)
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        readme = root / f"{ROOT}/Scripts/Features/Board/README.md"
        readme.parent.mkdir(parents=True)
        readme.write_text("real docs")
        (root / ".gitignore").write_text("custom\n")
        result = apply_manifest(m, tmpdir)
        assert readme.read_text() == "real docs"
        assert (root / ".gitignore").read_text() == "custom\n"
        assert str(readme) in result["skipped"]


def test_apply_manifest_merges_existing_claude_md():
    m = generate_manifest(CO, PJ)
    with tempfile.TemporaryDirectory() as tmpdir:
        claude = Path(tmpdir) / "CLAUDE.md"
        claude.write_text("# Team rules\nDo X.\n")
        result = apply_manifest(m, tmpdir)
        text = claude.read_text()
        assert text.startswith("# Team rules\nDo X.\n")
        assert CLAUDE_BEGIN in text
        assert str(claude) in result["updated"]
        # Re-run is idempotent
        apply_manifest(m, tmpdir)
        assert claude.read_text() == text


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-q"]))
