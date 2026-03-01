#!/usr/bin/env python3
"""
Unity Skill Validator
Based on Anthropic official validation patterns
Validates SKILL.md files in .opencode/skills/unity/
"""

import re
import sys
from pathlib import Path
from typing import Tuple, List
import yaml

# Validation constants
MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
NAME_PATTERN = re.compile(r'^[a-z0-9/-]+$')
REQUIRED_FIELDS = ['name', 'description']
ALLOWED_FIELDS = ['name', 'description', 'license', 'allowed-tools', 'metadata', 'compatibility']

# Unity-specific trigger keywords to check for
UNITY_TRIGGER_KEYWORDS = [
    'unity', 'monobehaviour', 'scriptableobject', 'prefab', 'scene', 'gameobject',
    'component', 'asset', 'editor', 'inspector', 'debug', 'optimize', 'performance',
    'ui toolkit', 'uxml', 'uss', 'mobile', 'shader', 'animation', 'physics',
    'test', 'build', 'deploy', 'refactor', 'code', 'script'
]

class ValidationError:
    def __init__(self, level: str, message: str):
        self.level = level  # ERROR, WARNING, INFO
        self.message = message
    
    def __str__(self):
        return f"[{self.level}] {self.message}"

def validate_skill(skill_path: Path) -> Tuple[bool, List[ValidationError]]:
    """Validate a single SKILL.md file."""
    errors = []
    
    # Check file exists
    if not skill_path.exists():
        errors.append(ValidationError('ERROR', f"SKILL.md not found at {skill_path}"))
        return False, errors
    
    # Read file
    try:
        content = skill_path.read_text(encoding='utf-8')
    except Exception as e:
        errors.append(ValidationError('ERROR', f"Cannot read file: {e}"))
        return False, errors
    
    # Extract frontmatter
    if not content.startswith('---'):
        errors.append(ValidationError('ERROR', "Missing YAML frontmatter (must start with ---)"))
        return False, errors
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        errors.append(ValidationError('ERROR', "Invalid frontmatter format (missing closing ---)"))
        return False, errors
    
    frontmatter_text = parts[1]
    body = parts[2].strip()
    
    # Parse YAML
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as e:
        errors.append(ValidationError('ERROR', f"Invalid YAML: {e}"))
        return False, errors
    
    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in frontmatter:
            errors.append(ValidationError('ERROR', f"Missing required field: {field}"))
    
    # Check for unknown fields
    for field in frontmatter.keys():
        if field not in ALLOWED_FIELDS:
            errors.append(ValidationError('WARNING', f"Unknown field: {field} (allowed: {', '.join(ALLOWED_FIELDS)})"))
    
    # Validate name
    if 'name' in frontmatter:
        name = frontmatter['name']
        if not isinstance(name, str):
            errors.append(ValidationError('ERROR', "Field 'name' must be a string"))
        else:
            if len(name) > MAX_NAME_LENGTH:
                errors.append(ValidationError('ERROR', f"Name too long ({len(name)} > {MAX_NAME_LENGTH} chars)"))
            if not NAME_PATTERN.match(name):
                errors.append(ValidationError('ERROR', f"Name must be kebab-case (lowercase, hyphens only): {name}"))
    
    # Validate description
    if 'description' in frontmatter:
        desc = frontmatter['description']
        if not isinstance(desc, str):
            errors.append(ValidationError('ERROR', "Field 'description' must be a string"))
        else:
            if len(desc) > MAX_DESCRIPTION_LENGTH:
                errors.append(ValidationError('ERROR', f"Description too long ({len(desc)} > {MAX_DESCRIPTION_LENGTH} chars)"))
            if '<' in desc or '>' in desc:
                errors.append(ValidationError('ERROR', "Description contains angle brackets (< or >)"))
            
            # Check for trigger keywords
            desc_lower = desc.lower()
            found_triggers = [kw for kw in UNITY_TRIGGER_KEYWORDS if kw in desc_lower]
            if len(found_triggers) < 3:
                errors.append(ValidationError('WARNING', f"Description has few Unity trigger keywords ({len(found_triggers)} found, recommend 5+)"))
            
            # Check for "Use when:" pattern
            if 'use when:' not in desc_lower and 'triggers:' not in desc_lower:
                errors.append(ValidationError('WARNING', "Description missing 'Use when:' or 'Triggers:' section"))
    
    # Check body length (token economy)
    word_count = len(body.split())
    if word_count > 2000:
        errors.append(ValidationError('WARNING', f"Body is long ({word_count} words). Consider splitting into SKILL.md + references/"))

    # Validate shared references (read_skill_file usage)
    ref_errors = validate_shared_references(skill_path, body)
    errors.extend(ref_errors)
    
    # Check for safety constraints if skill name suggests destructive operations
    name_lower = frontmatter.get('name', '').lower()
    destructive_patterns = ['delete', 'remove', 'refactor', 'deploy', 'build', 'fix']
    if any(pattern in name_lower for pattern in destructive_patterns):
        if 'safety' not in body.lower() and 'constraint' not in body.lower() and 'confirmation' not in body.lower():
            errors.append(ValidationError('WARNING', "Skill suggests destructive operations but lacks safety constraint documentation"))
    
    # Success if no ERROR level issues
    has_errors = any(e.level == 'ERROR' for e in errors)
    return not has_errors, errors

def validate_shared_references(skill_path: Path, body: str) -> List[ValidationError]:
    """Validate read_skill_file() usage and detect broken markdown links to unity-shared."""
    errors = []
    skills_root = skill_path.parent.parent  # skills/ directory
    shared_refs_dir = skills_root / 'unity-shared' / 'references'

    # Pattern: broken markdown links to ../unity-shared/references/
    md_link_pattern = re.compile(r'\.\.[\/]unity-shared[\/]references[\/]([\w.-]+\.md)')
    # Pattern: read_skill_file("unity-shared", "references/X.md")
    rsf_pattern = re.compile(r'read_skill_file\(["\']unity-shared["\'],\s*["\']references[\/]([\w.-]+\.md)["\']\)')

    md_link_files = set(md_link_pattern.findall(body))
    rsf_files = set(rsf_pattern.findall(body))

    # Check 1: markdown links WITHOUT corresponding read_skill_file() calls
    orphan_links = md_link_files - rsf_files
    for filename in sorted(orphan_links):
        errors.append(ValidationError('WARNING',
            f"Broken markdown link to ../unity-shared/references/{filename} — "
            f"use read_skill_file(\"unity-shared\", \"references/{filename}\") instead"))

    # Check 2: read_skill_file() targets must exist on disk
    for filename in sorted(rsf_files):
        target_file = shared_refs_dir / filename
        if not target_file.exists():
            errors.append(ValidationError('ERROR',
                f"read_skill_file target missing: unity-shared/references/{filename}"))

    # Check 3: detect ../unity-shared/ markdown links to non-reference paths (e.g. SKILL.md)
    broad_link_pattern = re.compile(r'\.\.[\/]unity-shared[\/](?!references[\/])([\w./-]+\.md)')
    broad_links = broad_link_pattern.findall(body)
    for link_target in sorted(set(broad_links)):
        errors.append(ValidationError('WARNING',
            f"Broken markdown link to ../unity-shared/{link_target} — "
            f"content will NOT load at runtime"))

    return errors

def validate_directory(skills_dir: Path) -> dict:
    """Validate all SKILL.md files in a directory tree."""
    results = {}
    
    for skill_file in skills_dir.rglob('SKILL.md'):
        relative_path = skill_file.relative_to(skills_dir)
        is_valid, errors = validate_skill(skill_file)
        results[str(relative_path)] = {
            'valid': is_valid,
            'errors': errors
        }
    
    return results

def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        target = Path(sys.argv[1])
    else:
        target = Path(__file__).parent / 'unity'
    
    if not target.exists():
        print(f"Error: {target} does not exist")
        sys.exit(1)
    
    if target.is_file():
        # Validate single file
        is_valid, errors = validate_skill(target)
        print(f"\n{'✅ VALID' if is_valid else '❌ INVALID'}: {target}")
        for error in errors:
            print(f"  {error}")
        sys.exit(0 if is_valid else 1)
    
    # Validate directory
    print(f"🔍 Validating skills in: {target}\n")
    results = validate_directory(target)
    
    # Summary
    total = len(results)
    valid_count = sum(1 for r in results.values() if r['valid'])
    invalid_count = total - valid_count
    
    # Print results
    for skill_path, result in sorted(results.items()):
        status = '✅' if result['valid'] else '❌'
        print(f"{status} {skill_path}")
        
        if result['errors']:
            for error in result['errors']:
                print(f"    {error}")
            print()
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 Validation Summary:")
    print(f"   Total skills: {total}")
    print(f"   ✅ Valid: {valid_count}")
    print(f"   ❌ Invalid: {invalid_count}")
    
    if invalid_count > 0:
        print(f"\n⚠️  {invalid_count} skill(s) need attention")
        sys.exit(1)
    else:
        print(f"\n🎉 All skills valid!")
        sys.exit(0)

if __name__ == '__main__':
    main()
