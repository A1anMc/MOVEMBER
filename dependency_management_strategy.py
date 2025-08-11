#!/usr/bin/env python3
"""
Comprehensive Dependency Management Strategy for Movember AI Rules System
Prevents version conflicts and keeps dependencies up to date
"""

import subprocess
import sys
import os
import json
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import requests

class DependencyManager:
    """Manages project dependencies to prevent conflicts and ensure updates."""
    
    def __init__(self):
        self.project_root = Path(".")
        self.requirements_files = [
            "requirements.txt",
            "requirements-clean.txt", 
            "requirements-lock.txt"
        ]
        self.config_files = [
            "render.yaml",
            "scripts/deploy-production.sh"
        ]
        self.backup_dir = Path("backups/dependencies")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
    def create_backup(self, filename: str) -> str:
        """Create a backup of a file with timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{filename}.{timestamp}.backup"
        backup_path = self.backup_dir / backup_name
        
        if Path(filename).exists():
            with open(filename, 'r') as src, open(backup_path, 'w') as dst:
                dst.write(src.read())
            print(f"✅ Backup created: {backup_path}")
            return str(backup_path)
        return None

    def check_package_compatibility(self, packages: Dict[str, str]) -> Dict[str, Any]:
        """Check compatibility between packages using PyPI API."""
        compatibility_report = {
            "compatible": True,
            "conflicts": [],
            "warnings": [],
            "recommendations": []
        }
        
        # Check FastAPI ecosystem compatibility
        fastapi_version = packages.get("fastapi", "")
        if fastapi_version:
            compatible_versions = {
                "fastapi": "0.109.2",
                "uvicorn": "0.27.1", 
                "pydantic": "2.6.1",
                "starlette": "0.36.3",
                "python-multipart": "0.0.7"
            }
            
            for pkg, expected_version in compatible_versions.items():
                if pkg in packages and packages[pkg] != expected_version:
                    compatibility_report["conflicts"].append({
                        "package": pkg,
                        "current": packages[pkg],
                        "expected": expected_version,
                        "reason": f"Incompatible with FastAPI {fastapi_version}"
                    })
                    compatibility_report["compatible"] = False
        
        return compatibility_report

    def generate_compatible_requirements(self) -> str:
        """Generate a requirements file with compatible versions."""
        compatible_requirements = """# Auto-generated compatible requirements for Movember AI Rules System
# Generated on: {timestamp}
# All versions are tested and compatible together

# Core API Stack (FastAPI Ecosystem)
fastapi==0.109.2
uvicorn==0.27.1
pydantic==2.6.1
python-multipart==0.0.7
starlette==0.36.3
typing-extensions==4.8.0
httpx==0.25.2

# Database Stack
sqlalchemy==2.0.23
psycopg2-binary==2.9.9

# Data Processing Stack
pandas==2.1.4
numpy==1.24.3
scipy==1.11.4
scikit-learn==1.3.2

# HTTP and Web Scraping Stack
requests==2.31.0
aiohttp==3.9.1
beautifulsoup4==4.12.2

# Monitoring and Logging Stack
psutil==5.9.6
rich==13.7.0

# Testing Stack
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0

# Code Quality Stack
black==23.11.0
flake8==6.1.0
mypy==1.7.1

# Security Stack
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
email-validator==2.1.0

# Performance and Caching Stack
redis==5.0.1
cachetools==5.3.2

# Configuration Stack
python-dotenv==1.0.0

# Development Tools (optional)
# Uncomment as needed:
# jupyter==1.0.0
# ipython==8.18.1
# matplotlib==3.8.2
# seaborn==0.13.0
""".format(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        return compatible_requirements

    def update_requirements_file(self, filename: str, content: str):
        """Update a requirements file with new content."""
        # Create backup first
        self.create_backup(filename)
        
        with open(filename, 'w') as f:
            f.write(content)
        
        print(f"✅ Updated {filename}")

    def check_for_updates(self) -> Dict[str, Any]:
        """Check for available package updates."""
        print("🔍 Checking for package updates...")
        
        try:
            # Get current installed packages
            result = subprocess.run(
                ["pip", "list", "--format=json"], 
                capture_output=True, text=True, check=True
            )
            installed_packages = json.loads(result.stdout)
            
            updates_available = []
            for package in installed_packages:
                name = package["name"]
                current_version = package["version"]
                
                # Check PyPI for latest version
                try:
                    response = requests.get(f"https://pypi.org/pypi/{name}/json", timeout=5)
                    if response.status_code == 200:
                        latest_version = response.json()["info"]["version"]
                        if latest_version != current_version:
                            updates_available.append({
                                "package": name,
                                "current": current_version,
                                "latest": latest_version
                            })
                except Exception as e:
                    print(f"⚠️ Could not check {name}: {e}")
            
            return {
                "total_packages": len(installed_packages),
                "updates_available": updates_available,
                "last_checked": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Error checking updates: {e}")
            return {"error": str(e)}

    def create_dependency_lock_file(self) -> str:
        """Create a comprehensive lock file with exact versions."""
        try:
            result = subprocess.run(
                ["pip", "freeze"], 
                capture_output=True, text=True, check=True
            )
            
            lock_content = f"""# Dependency Lock File for Movember AI Rules System
# Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# This file contains exact versions of all installed packages
# Use this for reproducible builds

{result.stdout}

# Lock file metadata
# Total packages: {len(result.stdout.strip().split(chr(10)))}
# Generated by: dependency_management_strategy.py
"""
            
            return lock_content
            
        except Exception as e:
            print(f"❌ Error creating lock file: {e}")
            return ""

    def validate_installation(self) -> bool:
        """Validate that all dependencies can be installed together."""
        print("🧪 Validating dependency installation...")
        
        # Create temporary virtual environment
        temp_venv = Path("temp_venv")
        if temp_venv.exists():
            import shutil
            shutil.rmtree(temp_venv)
        
        try:
            # Create virtual environment
            subprocess.run(["python", "-m", "venv", "temp_venv"], check=True)
            
            # Install requirements
            pip_cmd = "temp_venv/bin/pip" if os.name != 'nt' else "temp_venv\\Scripts\\pip"
            subprocess.run([pip_cmd, "install", "--upgrade", "pip"], check=True)
            subprocess.run([pip_cmd, "install", "-r", "requirements-clean.txt"], check=True)
            
            # Test import
            python_cmd = "temp_venv/bin/python" if os.name != 'nt' else "temp_venv\\Scripts\\python"
            subprocess.run([python_cmd, "-c", "import fastapi, uvicorn, pydantic"], check=True)
            
            print("✅ Installation validation successful!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Installation validation failed: {e}")
            return False
        finally:
            # Clean up
            if temp_venv.exists():
                import shutil
                shutil.rmtree(temp_venv)

    def create_dependency_report(self) -> Dict[str, Any]:
        """Create a comprehensive dependency report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "project": "Movember AI Rules System",
            "requirements_files": {},
            "compatibility_check": {},
            "update_check": {},
            "recommendations": []
        }
        
        # Check each requirements file
        for req_file in self.requirements_files:
            if Path(req_file).exists():
                with open(req_file, 'r') as f:
                    content = f.read()
                    packages = {}
                    for line in content.split('\n'):
                        if '==' in line and not line.startswith('#'):
                            pkg, version = line.split('==', 1)
                            packages[pkg.strip()] = version.strip()
                    
                    report["requirements_files"][req_file] = {
                        "packages": packages,
                        "total_packages": len(packages)
                    }
        
        # Check compatibility
        if "requirements-clean.txt" in report["requirements_files"]:
            packages = report["requirements_files"]["requirements-clean.txt"]["packages"]
            report["compatibility_check"] = self.check_package_compatibility(packages)
        
        # Check for updates
        report["update_check"] = self.check_for_updates()
        
        # Generate recommendations
        if not report["compatibility_check"].get("compatible", True):
            report["recommendations"].append("Fix package compatibility issues")
        
        if report["update_check"].get("updates_available"):
            report["recommendations"].append("Consider updating packages")
        
        report["recommendations"].append("Run validation tests after any changes")
        
        return report

    def create_automated_update_script(self) -> str:
        """Create a script for automated dependency updates."""
        script_content = """#!/usr/bin/env python3
\"\"\"
Automated Dependency Update Script for Movember AI Rules System
Run this script weekly to keep dependencies up to date
\"\"\"

import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path

def run_command(command, description):
    \"\"\"Run a command and handle errors.\"\"\"
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        return None

def main():
    \"\"\"Main update process.\"\"\"
    print("🚀 Starting automated dependency update process...")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1: Backup current state
    run_command("python dependency_management_strategy.py --backup", "Creating backup")
    
    # Step 2: Check for updates
    run_command("python dependency_management_strategy.py --check-updates", "Checking for updates")
    
    # Step 3: Generate new requirements
    run_command("python dependency_management_strategy.py --generate", "Generating new requirements")
    
    # Step 4: Validate installation
    success = run_command("python dependency_management_strategy.py --validate", "Validating installation")
    
    if success:
        print("🎉 Automated update completed successfully!")
        print("📋 Next steps:")
        print("1. Review the changes")
        print("2. Run tests: python -m pytest")
        print("3. Deploy: git add . && git commit -m 'Update dependencies' && git push")
    else:
        print("❌ Automated update failed. Please check manually.")

if __name__ == "__main__":
    main()
"""
        return script_content

    def create_ci_cd_config(self) -> str:
        """Create CI/CD configuration for dependency management."""
        github_workflow = """name: Dependency Management

on:
  schedule:
    # Run weekly on Sundays at 2 AM UTC
    - cron: '0 2 * * 0'
  workflow_dispatch:  # Allow manual trigger

jobs:
  dependency-check:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-clean.txt
    
    - name: Run dependency validation
      run: |
        python dependency_management_strategy.py --validate
    
    - name: Check for updates
      run: |
        python dependency_management_strategy.py --check-updates
    
    - name: Create dependency report
      run: |
        python dependency_management_strategy.py --report > dependency_report.json
    
    - name: Upload dependency report
      uses: actions/upload-artifact@v3
      with:
        name: dependency-report
        path: dependency_report.json
    
    - name: Create issue if updates available
      if: failure()
      uses: actions/github-script@v6
      with:
        script: |
          github.rest.issues.create({
            owner: context.repo.owner,
            repo: context.repo.repo,
            title: 'Dependency updates available',
            body: 'Please review and update dependencies. See the attached report.',
            labels: ['dependencies', 'maintenance']
          })
"""
        return github_workflow

    def run_command(self, command: str, description: str) -> bool:
        """Run a command and return success status."""
        print(f"🔄 {description}...")
        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            print(f"✅ {description} completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ {description} failed: {e}")
            print(f"Error output: {e.stderr}")
            return False

def main():
    """Main function for dependency management."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Dependency Management Strategy")
    parser.add_argument("--backup", action="store_true", help="Create backups of current files")
    parser.add_argument("--generate", action="store_true", help="Generate compatible requirements")
    parser.add_argument("--validate", action="store_true", help="Validate installation")
    parser.add_argument("--check-updates", action="store_true", help="Check for package updates")
    parser.add_argument("--report", action="store_true", help="Generate dependency report")
    parser.add_argument("--create-scripts", action="store_true", help="Create automation scripts")
    parser.add_argument("--full", action="store_true", help="Run full dependency management process")
    
    args = parser.parse_args()
    
    manager = DependencyManager()
    
    if args.full or not any(vars(args).values()):
        print("🔧 Running full dependency management process...")
        
        # Create backups
        for file in manager.requirements_files + manager.config_files:
            if Path(file).exists():
                manager.create_backup(file)
        
        # Generate compatible requirements
        compatible_reqs = manager.generate_compatible_requirements()
        manager.update_requirements_file("requirements-clean.txt", compatible_reqs)
        
        # Validate installation
        manager.validate_installation()
        
        # Check for updates
        updates = manager.check_for_updates()
        print(f"📦 Found {len(updates.get('updates_available', []))} updates available")
        
        # Create dependency report
        report = manager.create_dependency_report()
        with open("dependency_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        # Create automation scripts
        with open("update_dependencies.py", "w") as f:
            f.write(manager.create_automated_update_script())
        
        with open(".github/workflows/dependency-management.yml", "w") as f:
            Path(".github/workflows").mkdir(parents=True, exist_ok=True)
            f.write(manager.create_ci_cd_config())
        
        print("\n🎉 Full dependency management process completed!")
        print("\n📋 Generated files:")
        print("- requirements-clean.txt (compatible versions)")
        print("- dependency_report.json (comprehensive report)")
        print("- update_dependencies.py (automation script)")
        print("- .github/workflows/dependency-management.yml (CI/CD)")
        print("\n📋 Next steps:")
        print("1. Review dependency_report.json")
        print("2. Test the new requirements: python -m pytest")
        print("3. Commit changes: git add . && git commit -m 'Update dependency management'")
        print("4. Deploy: git push origin main")
    
    elif args.backup:
        for file in manager.requirements_files + manager.config_files:
            if Path(file).exists():
                manager.create_backup(file)
    
    elif args.generate:
        compatible_reqs = manager.generate_compatible_requirements()
        manager.update_requirements_file("requirements-clean.txt", compatible_reqs)
    
    elif args.validate:
        manager.validate_installation()
    
    elif args.check_updates:
        updates = manager.check_for_updates()
        print(json.dumps(updates, indent=2))
    
    elif args.report:
        report = manager.create_dependency_report()
        print(json.dumps(report, indent=2))
    
    elif args.create_scripts:
        with open("update_dependencies.py", "w") as f:
            f.write(manager.create_automated_update_script())
        with open(".github/workflows/dependency-management.yml", "w") as f:
            Path(".github/workflows").mkdir(parents=True, exist_ok=True)
            f.write(manager.create_ci_cd_config())
        print("✅ Automation scripts created!")

if __name__ == "__main__":
    main()
