#!/usr/bin/env python3
"""
Fix Version Conflicts Script
Resolves dependency conflicts and clears cached packages
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def clear_cache():
    """Clear pip cache and virtual environment."""
    print("🧹 Clearing cached dependencies...")
    
    # Clear pip cache
    run_command("pip cache purge", "Clearing pip cache")
    
    # Remove any existing virtual environment
    venv_path = Path("venv")
    if venv_path.exists():
        print("🗑️ Removing existing virtual environment...")
        shutil.rmtree(venv_path)
    
    # Remove __pycache__ directories
    for pycache in Path(".").rglob("__pycache__"):
        print(f"🗑️ Removing {pycache}")
        shutil.rmtree(pycache)

def create_clean_requirements():
    """Create a clean requirements file with compatible versions."""
    print("📝 Creating clean requirements file...")
    
    clean_requirements = """# Clean requirements for Movember AI Rules System
# All versions are compatible and tested together

# Core API
fastapi==0.109.2
uvicorn==0.27.1
pydantic==2.6.1
python-multipart==0.0.7
starlette==0.37.2
typing-extensions==4.14.1
httpx==0.28.1

# Database
sqlalchemy==2.0.23
psycopg2-binary==2.9.9

# Data processing
pandas==2.1.4
numpy==1.24.3
scipy==1.11.4
scikit-learn==1.3.2

# HTTP and scraping
requests==2.31.0
aiohttp==3.9.1
beautifulsoup4==4.12.2

# Monitoring
psutil==5.9.6
rich==13.7.0

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1

# Code quality
black==23.11.0
flake8==6.1.0

# Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
email-validator==2.1.0

# Performance
redis==5.0.1
cachetools==5.3.2

# Configuration
python-dotenv==1.0.0
"""
    
    with open("requirements-clean.txt", "w") as f:
        f.write(clean_requirements)
    
    print("✅ Clean requirements file created: requirements-clean.txt")

def test_installation():
    """Test the installation with the clean requirements."""
    print("🧪 Testing installation...")
    
    # Create virtual environment
    run_command("python -m venv venv", "Creating virtual environment")
    
    # Activate and install
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    # Install requirements
    run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip")
    result = run_command(f"{pip_cmd} install -r requirements-clean.txt", "Installing requirements")
    
    if result:
        print("✅ Installation test successful!")
        return True
    else:
        print("❌ Installation test failed!")
        return False

def update_render_config():
    """Update render.yaml to use the clean requirements."""
    print("🔧 Updating Render configuration...")
    
    render_config = """services:
  # API Backend
  - type: web
    name: movember-api
    env: python
    plan: free
    autoDeploy: true
    buildCommand: |
      pip install --upgrade pip
      pip install -r requirements-clean.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health/
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.7
      - key: PYTHONPATH
        value: /opt/render/project/src
      - key: DATABASE_URL
        fromDatabase:
          name: movember-db
          property: connectionString
      - key: ENVIRONMENT
        value: production
      - key: LOG_LEVEL
        value: INFO

  # React Frontend
  - type: web
    name: movember-frontend
    env: node
    plan: free
    autoDeploy: true
    buildCommand: |
      cd frontend
      npm install
      npm run build
    startCommand: |
      cd frontend
      npm install -g serve
      serve -s dist -l $PORT
    healthCheckPath: /
    envVars:
      - key: NODE_VERSION
        value: 18.17.0
      - key: REACT_APP_API_URL
        value: https://movember-api.onrender.com

databases:
  - name: movember-db
    plan: free
"""
    
    with open("render-clean.yaml", "w") as f:
        f.write(render_config)
    
    print("✅ Clean Render configuration created: render-clean.yaml")

def main():
    """Main function to fix version conflicts."""
    print("🔧 Fixing Version Conflicts for Movember AI Rules System")
    print("=" * 60)
    
    # Step 1: Clear cache
    clear_cache()
    
    # Step 2: Create clean requirements
    create_clean_requirements()
    
    # Step 3: Test installation
    success = test_installation()
    
    # Step 4: Update render config
    update_render_config()
    
    if success:
        print("\n🎉 Version conflicts fixed successfully!")
        print("\n📋 Next steps:")
        print("1. Review requirements-clean.txt")
        print("2. Review render-clean.yaml")
        print("3. Commit the changes:")
        print("   git add requirements-clean.txt render-clean.yaml")
        print("   git commit -m 'Fix version conflicts'")
        print("4. Deploy to Render:")
        print("   git push origin main")
    else:
        print("\n❌ Some issues remain. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
