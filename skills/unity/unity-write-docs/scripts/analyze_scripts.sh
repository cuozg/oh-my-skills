#!/bin/bash

# Simple script to extract Unity-related metadata for documentation

echo "=== Public Classes & Interfaces ==="
grep -r "public class\|public interface" Assets/Scripts --include="*.cs" | sed 's/.*public //' | sort -u

echo -e "\n=== Serialized Fields ==="
grep -r "\[SerializeField\]" Assets/Scripts --include="*.cs" | cut -d: -f1 | sort | uniq -c

echo -e "\n=== Scriptable Objects ==="
grep -r "ScriptableObject" Assets/Scripts --include="*.cs" | cut -d: -f1 | sort -u

echo -e "\n=== Custom Editors ==="
grep -r "\[CustomEditor\|\[CanEditMultipleObjects\]" Assets/Scripts --include="*.cs" | cut -d: -f1 | sort -u
