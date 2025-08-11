#!/usr/bin/env python3
"""
Syntax Validator for Movember AI Rules System
Validates all Python files for syntax errors before deployment.
"""

import sys
from pathlib import Path

def validate_syntax():
    """Validate all Python files for syntax errors."""
    project_root = Path.cwd()
    errors = []
    
    print("🔍 Running comprehensive syntax validation...")
    
    for py_file in project_root.rglob("*.py"):
        # Skip virtual environments and cache
        if any(skip in str(py_file) for skip in ["venv", ".venv", "__pycache__", ".git"]):
            continue
            
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                compile(f.read(), str(py_file), 'exec')
            print(f"✅ {py_file}")
        except SyntaxError as e:
            error_msg = f"{py_file}: {e}"
            errors.append(error_msg)
            print(f"❌ {error_msg}")
        except Exception as e:
            error_msg = f"{py_file}: Unexpected error - {e}"
            errors.append(error_msg)
            print(f"❌ {error_msg}")
    
    if errors:
        print(f"\n❌ Found {len(errors)} syntax errors:")
        for error in errors:
            print(f"  {error}")
        return False
    else:
        print(f"\n✅ All syntax checks passed! ({len(list(project_root.rglob('*.py')))} files validated)")
        return True

def validate_critical_imports():
    """Validate critical imports work."""
    print("\n🔍 Checking critical imports...")
    
    critical_imports = [
        ("API", "from api.movember_api import app"),
        ("Rules Engine", "from rules.core.engine import RuleEngine"),
        ("Movember AI", "from rules.domains.movember_ai import MovemberAIRulesEngine")
    ]
    
    all_valid = True
    for name, import_stmt in critical_imports:
        try:
            exec(import_stmt)
            print(f"✅ {name}: {import_stmt}")
        except Exception as e:
            print(f"❌ {name}: {import_stmt} failed - {e}")
            all_valid = False
    
    return all_valid

def main():
    """Run complete syntax validation."""
    print("🚨 Movember AI Rules System - Syntax Validator")
    print("=" * 50)
    
    # Validate syntax
    syntax_ok = validate_syntax()
    
    # Validate imports
    imports_ok = validate_critical_imports()
    
    print("\n" + "=" * 50)
    if syntax_ok and imports_ok:
        print("🎉 ALL VALIDATIONS PASSED!")
        print("✅ Ready for deployment")
        sys.exit(0)
    else:
        print("❌ VALIDATION FAILED!")
        print("🚨 Please fix issues before deployment")
        sys.exit(1)

if __name__ == "__main__":
    main()