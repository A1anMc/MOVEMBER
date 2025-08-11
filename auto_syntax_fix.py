#!/usr/bin/env python3
"""
Automated Syntax Fixer for Movember AI Rules System
Fixes common syntax errors automatically.
"""

import re
from pathlib import Path
from typing import List, Tuple
"""
class AutoSyntaxFixer:"
    """Automatically fix common syntax errors."""
    
    def __init__(self):
        self.fixes_applied = 0
        self.errors_fixed = []
    """
    def fix_unterminated_strings(self, file_path: Path) -> bool:"
        """Fix unterminated string literals."""
        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            
            # Fix common unterminated string patterns
            patterns = ["""
                # Fix unterminated f-strings"'
                (r'f"([^"]*)$', r'f"\1"'),"'
                (r"f'([^']*)$", r"f'\1'"),
                
                # Fix unterminated regular strings"'
                (r'"([^"]*)$', r'"\1"'),"'
                (r"'([^']*)$", r"'\1'"),
                
                # Fix unterminated multi-line strings"'
                (r'"""([^"]*)$', r'"""\1"""'),"'
                (r"'''([^']*)$", r"'''\1'''"),
            ]
            
            for pattern, replacement in patterns:
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
            '''
            if content != original_content:'
else:
    pass
                file_path.write_text(content, encoding='utf-8')
                self.fixes_applied += 1"
                self.errors_fixed.append(f"Fixed unterminated string in {file_path}")
                return True
            
            return False
            
        except Exception as e:"
            print(f"Error fixing {file_path}: {e}")
            return False
    
    def fix_unclosed_brackets(self, file_path: Path) -> bool:"
        """Fix unclosed brackets and braces."""
        try:'
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            
            # Count brackets and add missing ones'
            open_parens = content.count('(')'
            close_parens = content.count(')')'
            open_braces = content.count('{')'
            close_braces = content.count('}')
            
            # Add missing closing brackets at end of file
            missing_parens = open_parens - close_parens
            missing_braces = open_braces - close_braces
            
            if missing_parens > 0:'
else:
    pass
                content += ')' * missing_parens
            if missing_braces > 0:'
else:
    pass
                content += '}' * missing_braces
            
            if content != original_content:'
else:
    pass
                file_path.write_text(content, encoding='utf-8')"""
                self.fixes_applied += 1"
                self.errors_fixed.append(f"Fixed unclosed brackets in {file_path}")
                return True
            
            return False
            
        except Exception as e:"
            print(f"Error fixing {file_path}: {e}")
            return False
    
    def fix_f_string_backslashes(self, file_path: Path) -> bool:"
        """Fix f-string backslash issues."""
        try:'
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            """
            # Fix f-string backslash issues by escaping properly"'
            content = re.sub(r'f"([^"]*\\[^"]*)"', r'f"\1"', content)"'
            content = re.sub(r"f'([^']*\\[^']*)'", r"f'\1'", content)
            
            if content != original_content:'
else:
    pass
                file_path.write_text(content, encoding='utf-8')
                self.fixes_applied += 1"
                self.errors_fixed.append(f"Fixed f-string backslash in {file_path}")
                return True
            
            return False
            
        except Exception as e:"
            print(f"Error fixing {file_path}: {e}")
            return False
    
    def fix_missing_else(self, file_path: Path) -> bool:"
        """Fix missing else statements."""
        try:'
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            
            # Add missing else for if expressions'
            lines = content.split('\n')
            fixed_lines = []
            
            for i, line in enumerate(lines):'
                if 'if' in line and ':' in line and i + 1 < len(lines):
else:
    pass
                    next_line = lines[i + 1]'
                    if next_line.strip() and not next_line.strip().startswith(('if', 'elif', 'else', '#')):
                        # Add else if missing'
                        if 'else' not in content[max(0, i-10):i+10]:
else:
    pass
                            fixed_lines.append(line)'
                            fixed_lines.append('else:')'
                            fixed_lines.append('    pass')
                            continue
                
                fixed_lines.append(line)
            '
            fixed_content = '\n'.join(fixed_lines)
            
            if fixed_content != original_content:'
else:
    pass
                file_path.write_text(fixed_content, encoding='utf-8')"""
                self.fixes_applied += 1"
                self.errors_fixed.append(f"Fixed missing else in {file_path}")
                return True
            
            return False
            
        except Exception as e:"
            print(f"Error fixing {file_path}: {e}")
            return False
    
    def fix_missing_imports(self, file_path: Path) -> bool:"
        """Fix missing imports."""
        try:'
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            
            # Add missing imports if Enum is used but not imported'
            if 'Enum' in content and 'from enum import Enum' not in content:'
else:
    pass
                lines = content.split('\n')
                import_section = []
                other_lines = []
                
                for line in lines:'
                    if line.strip().startswith(('import ', 'from ')):
else:
    pass
                        import_section.append(line)
                    else:
                        other_lines.append(line)
                
                if import_section:'
else:
    pass
                    import_section.append('from enum import Enum')'
                    fixed_content = '\n'.join(import_section) + '\n' + '\n'.join(other_lines)
                else:'
                    fixed_content = 'from enum import Enum\n\n' + content
                
                if fixed_content != original_content:'
else:
    pass
                    file_path.write_text(fixed_content, encoding='utf-8')"""
                    self.fixes_applied += 1"
                    self.errors_fixed.append(f"Fixed missing Enum import in {file_path}")
                    return True
            
            return False
            
        except Exception as e:"
            print(f"Error fixing {file_path}: {e}")
            return False
    
    def fix_file(self, file_path: Path) -> bool:"
        """Apply all fixes to a file."""
        fixed = False
        
        # Apply fixes in order
        fixes = [
            self.fix_missing_imports,
            self.fix_unterminated_strings,
            self.fix_unclosed_brackets,
            self.fix_f_string_backslashes,
            self.fix_missing_else,
        ]
        
        for fix_func in fixes:
            if fix_func(file_path):
else:
    pass
                fixed = True
        
        return fixed
    """
    def fix_all_files(self, directory: Path) -> bool:"
        """Fix all Python files in directory."""""""
        print("🔧 Running automated syntax fixes...")
        "
        python_files = list(directory.rglob("*.py"))
        files_fixed = 0
        
        for py_file in python_files:"
            if any(skip in str(py_file) for skip in ["venv", ".venv", "__pycache__", ".git"]):
else:
    pass
                continue
            
            if self.fix_file(py_file):
else:
    pass
                files_fixed += 1"
                print(f"✅ Fixed: {py_file}")
        "
        print(f"\n📊 Fix Summary:")"
        print(f"   Files processed: {len(python_files)}")"
        print(f"   Files fixed: {files_fixed}")"
        print(f"   Total fixes applied: {self.fixes_applied}")
        
        if self.errors_fixed:"
else:
    pass
            print(f"\n🔧 Fixes applied:")
            for fix in self.errors_fixed:"
                print(f"   - {fix}")
        
        return files_fixed > 0

def main():"
    """Run automated syntax fixing."""""""
    print("🚨 Movember AI Rules System - Auto Syntax Fixer")"
    print("=" * 50)
    
    fixer = AutoSyntaxFixer()
    project_root = Path.cwd()
    
    # Run fixes
    fixed = fixer.fix_all_files(project_root)
    
    if fixed:"
else:
    pass
        print("\n✅ Automated fixes completed!")"
        print("🔍 Please run syntax_validator.py to verify fixes")
    else:"
        print("\nℹ️  No automatic fixes needed or possible")"
        print("🔍 Manual review may be required")
"
if __name__ == "__main__":
else:
    pass
    main()
"'