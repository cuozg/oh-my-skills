#!/usr/bin/env python3
"""
Generate Flutter project folder structure with feature-first architecture.

Usage:
    generate_structure.py --org <reverse.domain> --project <snake_case_name>
        [--features <comma-separated>] [--state-management riverpod]
        [--include-tests] [--output-dir <path>] [--dry-run]

Output: JSON manifest of all paths and file contents to stdout.
"""

import argparse
import json
import sys
from pathlib import Path


GITIGNORE_CONTENT = """\
# Flutter/Dart
.dart_tool/
.packages
build/
.flutter-plugins
.flutter-plugins-dependencies

# IDE
.idea/
.vscode/
*.iml
*.ipr
*.iws

# OS
.DS_Store
Thumbs.db

# Generated
*.g.dart
*.freezed.dart
*.mocks.dart

# Pub
.pub-cache/
.pub/
pubspec.lock
"""

ANALYSIS_OPTIONS_CONTENT = """\
include: package:flutter_lints/flutter.yaml

linter:
  rules:
    prefer_const_constructors: true
    prefer_const_declarations: true
    avoid_print: true
    prefer_single_quotes: true
    sort_constructors_first: true
    unawaited_futures: true
    always_declare_return_types: true
"""


def generate_pubspec(project: str, org: str, include_tests: bool = True) -> str:
    dev_deps = """\
dev_dependencies:
  flutter_test:
    sdk: flutter
  riverpod_generator: ^2.6.0
  build_runner: ^2.4.0
  freezed: ^2.5.0
  json_serializable: ^6.8.0
  flutter_lints: ^5.0.0"""
    if include_tests:
        dev_deps += "\n  mocktail: ^1.0.0"

    return f"""\
name: {project}
description: A new Flutter project.
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: ^3.5.0
  flutter: ^3.24.0

dependencies:
  flutter:
    sdk: flutter
  flutter_riverpod: ^2.6.0
  riverpod_annotation: ^2.6.0
  go_router: ^14.0.0
  dio: ^5.0.0
  freezed_annotation: ^2.4.0
  json_annotation: ^4.9.0

{dev_deps}
"""


def generate_analysis_options() -> str:
    return ANALYSIS_OPTIONS_CONTENT


def generate_main_dart(project: str) -> str:
    return """\
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'app/app.dart';

void main() {
  runApp(const ProviderScope(child: App()));
}
"""


def generate_app_dart() -> str:
    return """\
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'router.dart';
import 'theme.dart';

class App extends ConsumerWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(routerProvider);
    return MaterialApp.router(
      routerConfig: router,
      theme: appTheme,
    );
  }
}
"""


def generate_router_dart(features: list[str]) -> str:
    routes = "        GoRoute(\n          path: '/',\n          builder: (context, state) => const Scaffold(\n            body: Center(child: Text('Home')),\n          ),\n        ),\n"
    for feat in features:
        feat_class = feat.replace("_", " ").title().replace(" ", "")
        routes += f"        GoRoute(\n          path: '/{feat}',\n          builder: (context, state) => const {feat_class}Screen(),\n        ),\n"

    imports = ""
    for feat in features:
        imports += f"import '../features/{feat}/presentation/{feat}_screen.dart';\n"

    return f"""\
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

{imports.rstrip()}

part 'router.g.dart';

@riverpod
GoRouter router(Ref ref) {{
  return GoRouter(
    initialLocation: '/',
    routes: [
{routes}    ],
  );
}}
"""


def generate_theme_dart() -> str:
    return """\
import 'package:flutter/material.dart';

final appTheme = ThemeData(
  colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
  useMaterial3: true,
);
"""


def generate_gitignore() -> str:
    return GITIGNORE_CONTENT


def generate_core_files() -> list[dict]:
    constants = """\
abstract class AppConstants {
  static const String appName = 'App';
  static const Duration defaultTimeout = Duration(seconds: 30);
}
"""
    exceptions = """\
class AppException implements Exception {
  const AppException(this.message);

  final String message;

  @override
  String toString() => 'AppException: $message';
}
"""
    dio_client = """\
import 'package:dio/dio.dart';

class DioClient {
  DioClient({String? baseUrl})
      : _dio = Dio(
          BaseOptions(
            baseUrl: baseUrl ?? '',
            connectTimeout: const Duration(seconds: 30),
            receiveTimeout: const Duration(seconds: 30),
          ),
        );

  final Dio _dio;

  Dio get dio => _dio;
}
"""
    return [
        {"path": "lib/core/constants.dart", "content": constants},
        {"path": "lib/core/exceptions.dart", "content": exceptions},
        {"path": "lib/core/network/dio_client.dart", "content": dio_client},
    ]


def generate_feature_skeleton(
    feature: str, include_tests: bool = False
) -> tuple[list[str], list[dict]]:
    dirs = [
        f"lib/features/{feature}/data",
        f"lib/features/{feature}/presentation",
        f"lib/features/{feature}/providers",
    ]
    feat_class = feature.replace("_", " ").title().replace(" ", "")

    repository = f"""\
abstract class {feat_class}Repository {{
  // TODO: Add repository methods
}}
"""
    screen = f"""\
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class {feat_class}Screen extends ConsumerWidget {{
  const {feat_class}Screen({{super.key}});

  @override
  Widget build(BuildContext context, WidgetRef ref) {{
    return Scaffold(
      appBar: AppBar(title: const Text('{feat_class}')),
      body: const Center(
        child: Text('{feat_class} Screen'),
      ),
    );
  }}
}}
"""
    provider = f"""\
import 'package:riverpod_annotation/riverpod_annotation.dart';

// @riverpod
// Future<{feat_class}State> {feature}(Ref ref) async {{
//   // TODO: Implement provider
// }}
"""
    files = [
        {
            "path": f"lib/features/{feature}/data/{feature}_repository.dart",
            "content": repository,
        },
        {
            "path": f"lib/features/{feature}/presentation/{feature}_screen.dart",
            "content": screen,
        },
        {
            "path": f"lib/features/{feature}/providers/{feature}_provider.dart",
            "content": provider,
        },
    ]

    if include_tests:
        dirs.append(f"test/features/{feature}")
        test_content = f"""\
import 'package:flutter_test/flutter_test.dart';

void main() {{
  group('{feat_class}Repository', () {{
    // TODO: Add tests
  }});
}}
"""
        files.append(
            {
                "path": f"test/features/{feature}/{feature}_repository_test.dart",
                "content": test_content,
            }
        )

    return dirs, files


def generate_readme(project: str, features: list[str]) -> str:
    feature_list = "\n".join(f"- {f}" for f in features) if features else "- (none)"
    project_title = project.replace("_", " ").title()
    return f"""\
# {project_title}

## {project}

## Setup

```bash
flutter pub get
dart run build_runner build --delete-conflicting-outputs
```

## Architecture

This project follows a **feature-first** architecture:

```
lib/
  app/          # App-level config (router, theme)
  core/         # Shared utilities, constants, networking
  features/     # One folder per feature (data, presentation, providers)
  l10n/         # Localization
  shared/       # Shared widgets and helpers
```

## Features

{feature_list}
"""


def _generate_l10n_arb(project: str) -> str:
    project_title = project.replace("_", " ").title()
    return json.dumps(
        {"@@locale": "en", "appTitle": project_title},
        indent=2,
        ensure_ascii=False,
    )


def generate_manifest(
    org: str,
    project: str,
    features: list[str] | None = None,
    state_management: str = "riverpod",
    include_tests: bool = False,
    include_gitignore: bool = True,
) -> dict:
    features = [
        f.strip() for f in (features if features is not None else ["home"]) if f.strip()
    ]

    directories: list[str] = []
    files: list[dict] = []

    # Core directories (matches flutter-standards/code-organization.md)
    core_dirs = [
        "lib",
        "lib/app",
        "lib/core",
        "lib/core/extensions",
        "lib/core/network",
        "lib/core/utils",
        "lib/features",
        "lib/l10n",
        "lib/shared",
        "lib/shared/widgets",
        "lib/shared/models",
        "lib/shared/providers",
    ]
    directories.extend(core_dirs)

    # Core files
    files.append({"path": "lib/main.dart", "content": generate_main_dart(project)})
    files.append({"path": "lib/app/app.dart", "content": generate_app_dart()})
    files.append(
        {"path": "lib/app/router.dart", "content": generate_router_dart(features)}
    )
    files.append({"path": "lib/app/theme.dart", "content": generate_theme_dart()})
    files.extend(generate_core_files())

    # Pubspec, analysis options, readme
    files.append(
        {
            "path": "pubspec.yaml",
            "content": generate_pubspec(project, org, include_tests),
        }
    )
    files.append(
        {"path": "analysis_options.yaml", "content": generate_analysis_options()}
    )
    files.append({"path": "README.md", "content": generate_readme(project, features)})

    # l10n
    files.append(
        {"path": "lib/l10n/app_en.arb", "content": _generate_l10n_arb(project)}
    )

    # Gitignore
    if include_gitignore:
        files.append({"path": ".gitignore", "content": generate_gitignore()})

    # Feature skeletons
    for feat in features:
        feat_dirs, feat_files = generate_feature_skeleton(feat, include_tests)
        directories.extend(feat_dirs)
        files.extend(feat_files)

    # Test root dir
    if include_tests:
        directories.append("test")

    tree = build_tree(directories, files)

    return {
        "org": org,
        "project": project,
        "features": features,
        "state_management": state_management,
        "directories": sorted(set(directories)),
        "files": files,
        "tree": tree,
    }


def build_tree(directories: list[str], files: list[dict]) -> str:
    all_paths = sorted(set(directories + [f["path"] for f in files]))
    dir_set = set(directories)
    lines = []
    for p in all_paths:
        suffix = "/" if p in dir_set else ""
        lines.append(f"{p}{suffix}")
    return "\n".join(lines)


def apply_manifest(manifest: dict, output_dir: str) -> list[str]:
    root = Path(output_dir)
    created = []

    for d in manifest["directories"]:
        path = root / d
        path.mkdir(parents=True, exist_ok=True)
        created.append(str(path))

    for f in manifest["files"]:
        path = root / f["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f["content"])
        created.append(str(path))

    return created


def main():
    parser = argparse.ArgumentParser(
        description="Generate Flutter project folder structure"
    )
    parser.add_argument(
        "--org", required=True, help="Reverse domain (e.g., com.example)"
    )
    parser.add_argument("--project", required=True, help="Project name in snake_case")
    parser.add_argument(
        "--features",
        default="home",
        help="Comma-separated feature names (default: home)",
    )
    parser.add_argument(
        "--state-management",
        default="riverpod",
        help="State management approach (default: riverpod)",
    )
    parser.add_argument(
        "--include-tests",
        action="store_true",
        default=False,
        help="Scaffold test/ directory",
    )
    parser.add_argument(
        "--no-gitignore",
        action="store_true",
        default=False,
        help="Skip .gitignore generation",
    )
    parser.add_argument(
        "--output-dir", default=None, help="Apply structure to this directory"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Print manifest JSON without creating files",
    )

    args = parser.parse_args()

    if args.state_management != "riverpod":
        print(
            f"{args.state_management} support coming soon",
            file=sys.stderr,
        )
        sys.exit(1)

    features = [f.strip() for f in args.features.split(",") if f.strip()]

    manifest = generate_manifest(
        org=args.org,
        project=args.project,
        features=features,
        state_management=args.state_management,
        include_tests=args.include_tests,
        include_gitignore=not args.no_gitignore,
    )

    if args.dry_run or not args.output_dir:
        print(json.dumps(manifest, indent=2))
    else:
        created = apply_manifest(manifest, args.output_dir)
        print(
            json.dumps(
                {
                    "status": "success",
                    "created_count": len(created),
                    "tree": manifest["tree"],
                    "paths": created,
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
