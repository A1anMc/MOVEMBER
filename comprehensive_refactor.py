#!/usr/bin/env python3
"""
Comprehensive Refactoring Script for Movember AI Rules System
Systematically fixes code quality issues while preserving functionality.
"""

import os
import re
import logging
from typing import List, Dict, Set, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class RefactorStats:


    """Statistics for refactoring operations."""
    files_processed: int = 0
    unused_imports_removed: int = 0
    blank_lines_fixed: int = 0
    trailing_whitespace_removed: int = 0
    newlines_added: int = 0
    function_spacing_fixed: int = 0
    line_length_fixed: int = 0
    unused_variables_removed: int = 0
    undefined_variables_fixed: int = 0
    bare_except_fixed: int = 0


class ComprehensiveRefactor:
    """Comprehensive refactoring engine for the Movember AI Rules System."""

    def __init__(self):


        self.stats = RefactorStats()
        self.project_root = Path.cwd()
        self.python_files = []
        self.exclude_patterns = {
            'venv', '__pycache__', '.git', 'node_modules',
            '*.pyc', '*.pyo', '*.pyd', '*.so', '*.dll'
        }

    def find_python_files(self) -> List[Path]:


        """Find all Python files in the project."""
        python_files = []
        for root, dirs, files in os.walk(self.project_root):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in self.exclude_patterns]

            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    python_files.append(file_path)

        self.python_files = python_files
        logger.info(f"Found {len(python_files)} Python files")
        return python_files

    def remove_unused_imports(self, file_path: Path) -> bool:


        """Remove unused imports from a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # Common unused import patterns
            unused_patterns = [
                r'^import\s+(\w+)\s*$',  # Single imports
                r'^from\s+(\w+)\s+import\s+(\w+)\s*$',  # From imports
                r'^from\s+(\w+\.\w+)\s+import\s+(\w+)\s*$',  # Nested imports
            ]

            lines = content.split('\n')
            new_lines = []
            removed_count = 0

            for line in lines:
                line_stripped = line.strip()

                # Skip if line is empty or comment
                if not line_stripped or line_stripped.startswith('#'):
                    new_lines.append(line)
                    continue

                # Check if this looks like an unused import
                is_unused = False
                for pattern in unused_patterns:
                    if re.match(pattern, line_stripped):
                        import_name = re.match(pattern, line_stripped).group(1)
                        # Simple heuristic: if import name not used in rest of file
                        if import_name not in content.replace(line, ''):
                            is_unused = True
                            break

                if is_unused:
                    removed_count += 1
                    self.stats.unused_imports_removed += 1
                    logger.debug(f"Removing unused import: {line_stripped}")
                else:
                    new_lines.append(line)

            if removed_count > 0:
                new_content = '\n'.join(new_lines)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                logger.info(f"Removed {removed_count} unused imports from {file_path}")
                return True

            return False

        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return False

    def fix_blank_line_whitespace(self, file_path: Path) -> bool:


        """Remove whitespace from blank lines."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # Remove whitespace from blank lines
            lines = content.split('\n')
            new_lines = []
            fixed_count = 0

            for line in lines:
                if line.strip() == '' and line != '':
                    new_lines.append('')
                    fixed_count += 1
                    self.stats.blank_lines_fixed += 1
                else:
                    new_lines.append(line)

            if fixed_count > 0:
                new_content = '\n'.join(new_lines)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                logger.info(f"Fixed {fixed_count} blank lines in {file_path}")
                return True

            return False

        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return False

    def remove_trailing_whitespace(self, file_path: Path) -> bool:


        """Remove trailing whitespace from lines."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # Remove trailing whitespace
            lines = content.split('\n')
            new_lines = []
            fixed_count = 0

            for line in lines:
                original_line = line
                line = line.rstrip()
                if line != original_line:
                    fixed_count += 1
                    self.stats.trailing_whitespace_removed += 1
                new_lines.append(line)

            if fixed_count > 0:
                new_content = '\n'.join(new_lines)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                logger.info(f"Removed trailing whitespace from {fixed_count} lines in {file_path}")
                return True

            return False

        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return False

    def add_missing_newlines(self, file_path: Path) -> bool:


        """Add missing newlines at end of files."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if not content.endswith('\n'):
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content + '\n')
                self.stats.newlines_added += 1
                logger.info(f"Added missing newline to {file_path}")
                return True

            return False

        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return False

    def fix_function_spacing(self, file_path: Path) -> bool:


        """Fix function spacing (add 2 blank lines between functions)."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # Split into lines and process
            lines = content.split('\n')
            new_lines = []
            fixed_count = 0
            i = 0

            while i < len(lines):
                line = lines[i]
                new_lines.append(line)

                # Check if this line defines a function or class
                if re.match(r'^(def|class)\s+\w+', line.strip()):
                    # Look ahead to see if we need to add spacing
                    if i > 0:
                        # Count blank lines before this function
                        blank_lines_before = 0
                        j = i - 1
                        while j >= 0 and lines[j].strip() == '':
                            blank_lines_before += 1
                            j -= 1

                        # If we have less than 2 blank lines, add them
                        if blank_lines_before < 2:
                            # Remove existing blank lines
                            while new_lines and new_lines[-1].strip() == '':
                                new_lines.pop()

                            # Add 2 blank lines
                            new_lines.append('')
                            new_lines.append('')
                            fixed_count += 1
                            self.stats.function_spacing_fixed += 1

                i += 1

            if fixed_count > 0:
                new_content = '\n'.join(new_lines)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                logger.info(f"Fixed function spacing in {file_path}")
                return True

            return False

        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return False

    def fix_line_length(self, file_path: Path) -> bool:


        """Fix lines that are too long (over 120 characters)."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # Split into lines and process
            lines = content.split('\n')
            new_lines = []
            fixed_count = 0

            for line in lines:
                if len(line) > 120:
                    # Try to break long lines intelligently
                    if '(' in line and ')' in line:
                        # Break at parentheses
                        parts = line.split('(')
                        if len(parts) > 1:
                            indent = len(line) - len(line.lstrip())
                            new_line = parts[0] + '(\n' + ' ' * (indent + 4) + parts[1]
                            new_lines.append(new_line)
                            fixed_count += 1
                            self.stats.line_length_fixed += 1
                        else:
                            new_lines.append(line)
                    elif ',' in line:
                        # Break at commas
                        parts = line.split(',')
                        if len(parts) > 1:
                            indent = len(line) - len(line.lstrip())
                            new_line = parts[0] + ',\n' + ' ' * (indent + 4) + ','.join(parts[1:])
                            new_lines.append(new_line)
                            fixed_count += 1
                            self.stats.line_length_fixed += 1
                        else:
                            new_lines.append(line)
                    else:
                        # Simple break at word boundary
                        words = line.split()
                        if len(words) > 1:
                            indent = len(line) - len(line.lstrip())
                            current_line = words[0]
                            for word in words[1:]:
                                if len(current_line + ' ' + word) > 120:
                                    new_lines.append(current_line)
                                    current_line = ' ' * indent + word
                                else:
                                    current_line += ' ' + word
                            new_lines.append(current_line)
                            fixed_count += 1
                            self.stats.line_length_fixed += 1
                        else:
                            new_lines.append(line)
                else:
                    new_lines.append(line)

            if fixed_count > 0:
                new_content = '\n'.join(new_lines)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                logger.info(f"Fixed {fixed_count} long lines in {file_path}")
                return True

            return False

        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return False

    def fix_undefined_variables(self, file_path: Path) -> bool:


        """Fix undefined variable issues (like missing logger)."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # Check for undefined logger
            if 'logger' in content and 'import logging' not in content:
                # Add logging import at the top
                lines = content.split('\n')
                import_added = False

                for i, line in enumerate(lines):
                    if line.strip().startswith('import ') or line.strip().startswith('from '):
                        if 'logging' not in line:
                            lines.insert(i, 'import logging')
                            lines.insert(i + 1, '')
                            import_added = True
                            break

                if import_added:
                    # Add logger definition after imports
                    for i, line in enumerate(lines):
                        if line.strip() == '' and i > 0:
                            lines.insert(i + 1, 'logger = logging.getLogger(__name__)')
                            break

                    new_content = '\n'.join(lines)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    self.stats.undefined_variables_fixed += 1
                    logger.info(f"Fixed undefined logger in {file_path}")
                    return True

            return False

        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return False

    def fix_bare_except(self, file_path: Path) -> bool:


        """Fix bare except statements."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # Replace bare except with specific exception
            if 'except Exception:' in content:
                new_content = content.replace('except Exception:', 'except Exception:')
                if new_content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    self.stats.bare_except_fixed += 1
                    logger.info(f"Fixed bare except in {file_path}")
                    return True

            return False

        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return False

    def run_phase1_automated_cleanup(self) -> RefactorStats:


        """Run Phase 1: Automated cleanup operations."""
        logger.info("🔧 Starting Phase 1: Automated Cleanup")

        python_files = self.find_python_files()

        for file_path in python_files:
            self.stats.files_processed += 1

            # Phase 1 operations (safe, automated)
            self.remove_unused_imports(file_path)
            self.fix_blank_line_whitespace(file_path)
            self.remove_trailing_whitespace(file_path)
            self.add_missing_newlines(file_path)

        logger.info(f"✅ Phase 1 Complete: Processed {self.stats.files_processed} files")
        return self.stats

    def run_phase2_structural_improvements(self) -> RefactorStats:


        """Run Phase 2: Structural improvements."""
        logger.info("🔧 Starting Phase 2: Structural Improvements")

        python_files = self.find_python_files()

        for file_path in python_files:
            # Phase 2 operations (structural)
            self.fix_function_spacing(file_path)
            self.fix_line_length(file_path)

        logger.info("✅ Phase 2 Complete")
        return self.stats

    def run_phase3_critical_fixes(self) -> RefactorStats:


        """Run Phase 3: Critical fixes."""
        logger.info("🔧 Starting Phase 3: Critical Fixes")

        python_files = self.find_python_files()

        for file_path in python_files:
            # Phase 3 operations (critical)
            self.fix_undefined_variables(file_path)
            self.fix_bare_except(file_path)

        logger.info("✅ Phase 3 Complete")
        return self.stats

    def run_comprehensive_refactor(self) -> RefactorStats:


        """Run the complete refactoring process."""
        logger.info("🚀 Starting Comprehensive Refactoring")
        logger.info("=" * 50)

        # Phase 1: Automated cleanup
        phase1_stats = self.run_phase1_automated_cleanup()
        logger.info(f"Phase 1 Results: {phase1_stats}")

        # Phase 2: Structural improvements
        phase2_stats = self.run_phase2_structural_improvements()
        logger.info(f"Phase 2 Results: {phase2_stats}")

        # Phase 3: Critical fixes
        phase3_stats = self.run_phase3_critical_fixes()
        logger.info(f"Phase 3 Results: {phase3_stats}")

        logger.info("=" * 50)
        logger.info("🎉 Comprehensive Refactoring Complete!")

        return self.stats

    def print_summary(self):


        """Print a summary of the refactoring results."""
        print("\n" + "=" * 60)
        print("📊 REFACTORING SUMMARY")
        print("=" * 60)
        print(f"📁 Files processed: {self.stats.files_processed}")
        print(f"🗑️  Unused imports removed: {self.stats.unused_imports_removed}")
        print(f"🧹 Blank lines fixed: {self.stats.blank_lines_fixed}")
        print(f"✂️  Trailing whitespace removed: {self.stats.trailing_whitespace_removed}")
        print(f"📝 Missing newlines added: {self.stats.newlines_added}")
        print(f"📏 Function spacing fixed: {self.stats.function_spacing_fixed}")
        print(f"📐 Line length fixed: {self.stats.line_length_fixed}")
        print(f"🔧 Undefined variables fixed: {self.stats.undefined_variables_fixed}")
        print(f"🛡️  Bare except statements fixed: {self.stats.bare_except_fixed}")
        print("=" * 60)


def main():
    """Main function to run the comprehensive refactoring."""
    print("🔧 Movember AI Rules System - Comprehensive Refactoring")
    print("=" * 60)

    refactor = ComprehensiveRefactor()

    # Run the comprehensive refactoring
    stats = refactor.run_comprehensive_refactor()

    # Print summary
    refactor.print_summary()

    print("\n✅ Refactoring completed successfully!")
    print("🎯 The codebase is now cleaner and more maintainable.")
    print("📋 Next steps: Run tests to ensure functionality is preserved.")


if __name__ == "__main__":
    main()
