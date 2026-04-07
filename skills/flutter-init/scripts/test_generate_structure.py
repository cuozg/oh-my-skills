#!/usr/bin/env python3
"""Tests for Flutter project structure generator."""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from generate_structure import (
    apply_manifest,
    build_tree,
    generate_analysis_options,
    generate_app_dart,
    generate_core_files,
    generate_feature_skeleton,
    generate_gitignore,
    generate_main_dart,
    generate_manifest,
    generate_pubspec,
    generate_readme,
    generate_router_dart,
    generate_theme_dart,
)


# ── Group A: pubspec.yaml generation (6 tests) ─────────────────────────


class TestPubspec:
    def test_generate_pubspec_has_correct_name(self):
        content = generate_pubspec("my_app", "com.example", include_tests=True)
        assert "name: my_app" in content

    def test_generate_pubspec_sdk_constraints(self):
        content = generate_pubspec("demo", "com.example", include_tests=True)
        assert "sdk: ^3.5.0" in content
        assert "flutter: ^3.24.0" in content

    def test_generate_pubspec_dependencies(self):
        content = generate_pubspec("demo", "com.example", include_tests=True)
        deps = [
            "flutter_riverpod:",
            "riverpod_annotation:",
            "go_router:",
            "dio:",
            "freezed_annotation:",
            "json_annotation:",
        ]
        for dep in deps:
            assert dep in content, f"Missing dependency: {dep}"

    def test_generate_pubspec_dev_dependencies(self):
        content = generate_pubspec("demo", "com.example", include_tests=True)
        dev_deps = [
            "riverpod_generator:",
            "build_runner:",
            "freezed:",
            "json_serializable:",
            "flutter_lints:",
            "mocktail:",
        ]
        for dep in dev_deps:
            assert dep in content, f"Missing dev dependency: {dep}"

    def test_generate_pubspec_custom_org(self):
        manifest = generate_manifest(
            org="io.mycompany",
            project="cool_app",
            features=["home"],
            state_management="riverpod",
            include_tests=False,
        )
        assert manifest["org"] == "io.mycompany"

    def test_generate_pubspec_no_mocktail_when_tests_excluded(self):
        content = generate_pubspec("demo", "com.example", include_tests=False)
        assert "mocktail" not in content


# ── Group B: Directory structure (7 tests) ──────────────────────────────


class TestDirectoryStructure:
    def test_manifest_default_directories(self):
        m = generate_manifest(
            org="com.example",
            project="my_app",
            features=["home"],
            state_management="riverpod",
            include_tests=False,
        )
        dirs = m["directories"]
        assert "lib/app" in dirs
        assert "lib/core" in dirs
        assert "lib/core/extensions" in dirs
        assert "lib/core/network" in dirs
        assert "lib/core/utils" in dirs
        assert "lib/l10n" in dirs
        assert "lib/shared" in dirs
        assert "lib/shared/widgets" in dirs
        assert "lib/shared/models" in dirs
        assert "lib/shared/providers" in dirs

    def test_manifest_feature_directories(self):
        m = generate_manifest(
            org="com.example",
            project="my_app",
            features=["auth"],
            state_management="riverpod",
            include_tests=False,
        )
        dirs = m["directories"]
        assert "lib/features/auth/data" in dirs
        assert "lib/features/auth/presentation" in dirs
        assert "lib/features/auth/providers" in dirs

    def test_manifest_multiple_features(self):
        m = generate_manifest(
            org="com.example",
            project="my_app",
            features=["auth", "profile", "settings"],
            state_management="riverpod",
            include_tests=False,
        )
        dirs = m["directories"]
        for feat in ["auth", "profile", "settings"]:
            assert f"lib/features/{feat}/data" in dirs
            assert f"lib/features/{feat}/presentation" in dirs
            assert f"lib/features/{feat}/providers" in dirs

    def test_manifest_no_cross_feature_dirs(self):
        m = generate_manifest(
            org="com.example",
            project="my_app",
            features=["auth", "profile"],
            state_management="riverpod",
            include_tests=False,
        )
        for d in m["directories"]:
            if "features/" in d:
                parts = d.split("features/")[1].split("/")
                feat_name = parts[0]
                assert feat_name in ("auth", "profile"), f"Unexpected feature dir: {d}"

    def test_manifest_empty_features_still_has_core(self):
        m = generate_manifest(
            org="com.example",
            project="my_app",
            features=[],
            state_management="riverpod",
            include_tests=False,
        )
        dirs = m["directories"]
        assert "lib/app" in dirs
        assert "lib/core" in dirs
        assert "lib/shared" in dirs

    def test_manifest_strips_whitespace_features(self):
        m = generate_manifest(
            org="com.example",
            project="my_app",
            features=["  auth  ", "  ", "home"],
            state_management="riverpod",
            include_tests=False,
        )
        dirs = m["directories"]
        assert "lib/features/auth/data" in dirs
        assert "lib/features/home/data" in dirs
        feature_names = set()
        for d in dirs:
            if "features/" in d:
                feature_names.add(d.split("features/")[1].split("/")[0])
        assert "" not in feature_names

    def test_manifest_test_directories_when_included(self):
        m = generate_manifest(
            org="com.example",
            project="my_app",
            features=["auth"],
            state_management="riverpod",
            include_tests=True,
        )
        dirs = m["directories"]
        assert "test" in dirs or any(d.startswith("test/") for d in dirs)
        assert "test/features/auth" in dirs


# ── Group C: File content correctness (7 tests) ────────────────────────


class TestFileContent:
    def test_main_dart_has_provider_scope(self):
        content = generate_main_dart("my_app")
        assert "ProviderScope" in content
        assert "import 'package:flutter_riverpod/flutter_riverpod.dart'" in content

    def test_app_dart_has_material_app_router(self):
        content = generate_app_dart()
        assert "MaterialApp.router" in content
        assert "ConsumerWidget" in content
        assert "routerConfig" in content

    def test_router_dart_has_go_router(self):
        content = generate_router_dart(["home", "profile"])
        assert "GoRouter" in content
        assert "GoRoute" in content
        assert "'/home'" in content or "/home" in content
        assert "'/profile'" in content or "/profile" in content

    def test_theme_dart_has_theme_data(self):
        content = generate_theme_dart()
        assert "ThemeData" in content
        assert "ColorScheme.fromSeed" in content
        assert "useMaterial3: true" in content

    def test_analysis_options_includes_flutter_lints(self):
        content = generate_analysis_options()
        assert "package:flutter_lints/flutter.yaml" in content

    def test_analysis_options_has_required_rules(self):
        content = generate_analysis_options()
        rules = [
            "prefer_const_constructors",
            "prefer_const_declarations",
            "avoid_print",
            "prefer_single_quotes",
            "sort_constructors_first",
            "unawaited_futures",
            "always_declare_return_types",
        ]
        for rule in rules:
            assert rule in content, f"Missing lint rule: {rule}"

    def test_gitignore_has_flutter_patterns(self):
        content = generate_gitignore()
        assert ".dart_tool/" in content
        assert "build/" in content
        assert ".flutter-plugins" in content

    def test_gitignore_excluded_when_disabled(self):
        m = generate_manifest(
            org="com.example",
            project="my_app",
            features=["home"],
            state_management="riverpod",
            include_tests=False,
            include_gitignore=False,
        )
        gitignore = next((f for f in m["files"] if f["path"] == ".gitignore"), None)
        assert gitignore is None


# ── Group D: Architectural constraints (3 tests) ───────────────────────


class TestArchitecturalConstraints:
    def test_feature_file_naming_conventions(self):
        m = generate_manifest(
            org="com.example",
            project="my_app",
            features=["user_profile"],
            state_management="riverpod",
            include_tests=False,
        )
        config_roots = {"README.md", "pubspec.yaml", "analysis_options.yaml"}
        for f in m["files"]:
            basename = Path(f["path"]).name
            if f["path"].startswith(".") or basename in config_roots:
                continue
            stem = Path(f["path"]).stem
            assert stem == stem.lower(), f"Non-snake_case file: {f['path']}"
            assert " " not in stem, f"Space in filename: {f['path']}"

    def test_feature_has_three_layers(self):
        m = generate_manifest(
            org="com.example",
            project="my_app",
            features=["auth", "settings"],
            state_management="riverpod",
            include_tests=False,
        )
        dirs = m["directories"]
        for feat in ["auth", "settings"]:
            assert f"lib/features/{feat}/data" in dirs
            assert f"lib/features/{feat}/presentation" in dirs
            assert f"lib/features/{feat}/providers" in dirs

    def test_no_stateful_widget_in_generated_code(self):
        m = generate_manifest(
            org="com.example",
            project="my_app",
            features=["auth", "home"],
            state_management="riverpod",
            include_tests=False,
        )
        for f in m["files"]:
            assert "StatefulWidget" not in f["content"], (
                f"StatefulWidget found in {f['path']}"
            )


# ── Group E: CLI + apply (6 tests) ─────────────────────────────────────


class TestApplyAndCli:
    def test_apply_manifest_creates_all_dirs(self):
        m = generate_manifest(
            org="com.example",
            project="my_app",
            features=["home"],
            state_management="riverpod",
            include_tests=True,
            include_gitignore=True,
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            apply_manifest(m, tmpdir)
            root = Path(tmpdir)
            for d in m["directories"]:
                assert (root / d).is_dir(), f"Missing directory: {d}"

    def test_apply_manifest_writes_all_files(self):
        m = generate_manifest(
            org="com.example",
            project="my_app",
            features=["home"],
            state_management="riverpod",
            include_tests=True,
            include_gitignore=True,
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            created = apply_manifest(m, tmpdir)
            root = Path(tmpdir)
            for f in m["files"]:
                fpath = root / f["path"]
                assert fpath.is_file(), f"Missing file: {f['path']}"
                assert fpath.read_text() == f["content"]
            assert len(created) > 0

    def test_dry_run_outputs_json(self):
        m = generate_manifest(
            org="com.example",
            project="my_app",
            features=["home"],
            state_management="riverpod",
            include_tests=False,
        )
        # Manifest should be JSON-serializable
        json_str = json.dumps(m, indent=2)
        parsed = json.loads(json_str)
        assert parsed["project"] == "my_app"
        assert "directories" in parsed
        assert "files" in parsed

    def test_tree_output_readable(self):
        m = generate_manifest(
            org="com.example",
            project="my_app",
            features=["home"],
            state_management="riverpod",
            include_tests=False,
        )
        assert isinstance(m["tree"], str)
        assert len(m["tree"]) > 0
        assert "lib/" in m["tree"] or "lib" in m["tree"]

    def test_readme_contains_project_name(self):
        content = generate_readme("cool_app", ["auth", "home"])
        assert "cool_app" in content

    def test_l10n_arb_file_generated(self):
        m = generate_manifest(
            org="com.example",
            project="my_app",
            features=["home"],
            state_management="riverpod",
            include_tests=False,
        )
        arb_file = next(
            (f for f in m["files"] if f["path"].endswith("app_en.arb")), None
        )
        assert arb_file is not None, "app_en.arb not found in manifest files"
        arb_content = json.loads(arb_file["content"])
        assert arb_content["@@locale"] == "en"


if __name__ == "__main__":
    import pytest

    sys.exit(pytest.main([__file__, "-v"]))
