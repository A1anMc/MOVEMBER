#!/usr/bin/env python3
"""Quick syntax fixes for remaining issues."""

def fix_ml_pipeline():
    """Fix the incomplete if statement in data_pipeline.py."""
    with open('ml_integration/data_pipeline.py', 'r') as f:
        content = f.read()
    
    # Fix the incomplete if statement
    old_line = 'labels["approval_probability"] = 1.0 if grant_data.get(\n            "score", 0) >= 7.0 else 0.5 if grant_data.get'
    new_line = '        score = grant_data.get("score", 0)\n        labels["approval_probability"] = 1.0 if score >= 7.0 else 0.5 if score >= 5.0 else 0.2'
    
    content = content.replace(old_line, new_line)
    
    with open('ml_integration/data_pipeline.py', 'w') as f:
        f.write(content)

def fix_integration_file():
    """Fix the unclosed brace in integration.py."""
    with open('rules/domains/movember_ai/integration.py', 'r') as f:
        content = f.read()
    
    # Add missing closing brace
    if content.count('{') > content.count('}'):
        content += '\n}\n'
    
    with open('rules/domains/movember_ai/integration.py', 'w') as f:
        f.write(content)

def fix_auto_syntax_fix():
    """Fix the auto_syntax_fix.py file itself."""
    with open('auto_syntax_fix.py', 'r') as f:
        content = f.read()
    
    # Fix the broken docstring
    content = content.replace('"""\nAutomated Syntax Fixer for Movember AI Rules System"""\nFixes common syntax errors automatically."\n"""', 
                             '"""\nAutomated Syntax Fixer for Movember AI Rules System\nFixes common syntax errors automatically.\n"""')
    
    with open('auto_syntax_fix.py', 'w') as f:
        f.write(content)

def fix_remaining_strings():
    """Fix remaining unterminated strings."""
    files_to_fix = [
        ('tests/test_integration_systems.py', 398),
        ('rules/examples/user_validation_rules.py', 67),
        ('monitoring/automated_alerts.py', 159)
    ]
    
    for file_path, line_num in files_to_fix:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Simple fix: add closing quote if missing
            lines = content.split('\n')
            if line_num - 1 < len(lines):
                line = lines[line_num - 1]
                if line.count('"') % 2 == 1:  # Odd number of quotes
                    lines[line_num - 1] = line + '"'
                elif line.count("'") % 2 == 1:  # Odd number of single quotes
                    lines[line_num - 1] = line + "'"
            
            with open(file_path, 'w') as f:
                f.write('\n'.join(lines))
        except Exception as e:
            print(f"Could not fix {file_path}: {e}")

if __name__ == "__main__":
    print("🔧 Applying quick syntax fixes...")
    fix_ml_pipeline()
    fix_integration_file()
    fix_auto_syntax_fix()
    fix_remaining_strings()
    print("✅ Quick fixes applied!")
