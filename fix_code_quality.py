#!/usr/bin/env python3
"""
Code Quality Fix Script
Automatically fixes common code quality issues in the Movember AI Rules System.
"""

import re
import glob


def fix_file_endings():
    """Add newlines to files that don't end with one."""
    python_files = glob.glob("**/*.py", recursive=True)
    fixed_count = 0

    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if content and not content.endswith('\n'):
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content + '\n')
                print(f"✅ Fixed file ending: {file_path}")
                fixed_count += 1
        except Exception as e:
            print(f"❌ Error fixing {file_path}: {e}")

    print(f"📊 Fixed {fixed_count} file endings")


def remove_trailing_whitespace():
    """Remove trailing whitespace from all lines."""
    python_files = glob.glob("**/*.py", recursive=True)
    fixed_count = 0

    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            original_lines = lines.copy()
            lines = [line.rstrip() + '\n' for line in lines]

            if lines != original_lines:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                print(f"✅ Fixed trailing whitespace: {file_path}")
                fixed_count += 1
        except Exception as e:
            print(f"❌ Error fixing {file_path}: {e}")

    print(f"📊 Fixed trailing whitespace in {fixed_count} files")


def fix_blank_lines_with_whitespace():
    """Remove whitespace from blank lines."""
    python_files = glob.glob("**/*.py", recursive=True)
    fixed_count = 0

    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            original_lines = lines.copy()
            lines = [line if line.strip() else '\n' for line in lines]

            if lines != original_lines:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                print(f"✅ Fixed blank lines: {file_path}")
                fixed_count += 1
        except Exception as e:
            print(f"❌ Error fixing {file_path}: {e}")

    print(f"📊 Fixed blank lines in {fixed_count} files")


def fix_missing_whitespace_around_operators():
    """Add missing whitespace around operators."""
    python_files = glob.glob("**/*.py", recursive=True)
    fixed_count = 0

    # Common patterns that need whitespace
    patterns = [
        (r'([a-zA-Z0-9_]):([a-zA-Z0-9_])', r'\1: \2'),  # colons
        (r'([a-zA-Z0-9_]):([a-zA-Z0-9_])', r'\1: \2'),  # colons in dicts
    ]

    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            for pattern, replacement in patterns:
                content = re.sub(pattern, replacement, content)

            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Fixed operator spacing: {file_path}")
                fixed_count += 1
        except Exception as e:
            print(f"❌ Error fixing {file_path}: {e}")

    print(f"📊 Fixed operator spacing in {fixed_count} files")


def main():
    """Run all code quality fixes."""
    print("🔧 Starting code quality fixes...")
    print("=" * 50)

    print("\n1. Fixing file endings...")
    fix_file_endings()

    print("\n2. Removing trailing whitespace...")
    remove_trailing_whitespace()

    print("\n3. Fixing blank lines with whitespace...")
    fix_blank_lines_with_whitespace()

    print("\n4. Fixing operator spacing...")
    fix_missing_whitespace_around_operators()

    print("\n" + "=" * 50)
    print("✅ Code quality fixes completed!")
    print("💡 Run 'python -m flake8' to check remaining issues")


if __name__ == "__main__":
    main()
