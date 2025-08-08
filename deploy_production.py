#!/usr/bin/env python3
"""
Production Deployment Script for Movember AI Rules System
Deploys the enhanced system with Phase 1 improvements and Phase 2 ML capabilities
"""

import os
import sys
import subprocess
import shutil
import json
import time
from pathlib import Path
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ProductionDeployment:
    """Production deployment manager for Movember AI Rules System."""
    
    def __init__(self, deployment_dir: str = "production"):
        self.deployment_dir = deployment_dir
        self.backup_dir = f"{deployment_dir}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.config = {
            "api_port": 8000,
            "frontend_port": 3000,
            "database_path": "movember_ai.db",
            "log_level": "INFO",
            "environment": "production"
        }
    
    def deploy(self):
        """Main deployment process."""
        logger.info("🚀 Starting Production Deployment for Movember AI Rules System")
        logger.info("=" * 60)
        
        try:
            # Step 1: Pre-deployment checks
            self._pre_deployment_checks()
            
            # Step 2: Create backup
            self._create_backup()
            
            # Step 3: Prepare deployment directory
            self._prepare_deployment_directory()
            
            # Step 4: Copy application files
            self._copy_application_files()
            
            # Step 5: Install dependencies
            self._install_dependencies()
            
            # Step 6: Configure production settings
            self._configure_production_settings()
            
            # Step 7: Run tests
            self._run_tests()
            
            # Step 8: Start services
            self._start_services()
            
            # Step 9: Health checks
            self._health_checks()
            
            # Step 10: Final verification
            self._final_verification()
            
            logger.info("✅ Production deployment completed successfully!")
            self._print_deployment_summary()
            
        except Exception as e:
            logger.error(f"❌ Deployment failed: {str(e)}")
            self._rollback()
            raise
    
    def _pre_deployment_checks(self):
        """Perform pre-deployment checks."""
        logger.info("🔍 Performing pre-deployment checks...")
        
        # Check Python version
        python_version = sys.version_info
        if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
            raise Exception("Python 3.8+ is required")
        
        # Check required directories
        required_dirs = ["rules", "monitoring", "frontend", "ml_integration"]
        for dir_name in required_dirs:
            if not os.path.exists(dir_name):
                raise Exception(f"Required directory '{dir_name}' not found")
        
        # Check required files
        required_files = [
            "simple_api.py",
            "requirements.txt",
            "frontend/index.html",
            "frontend/dashboard.js"
        ]
        for file_name in required_files:
            if not os.path.exists(file_name):
                raise Exception(f"Required file '{file_name}' not found")
        
        logger.info("✅ Pre-deployment checks passed")
    
    def _create_backup(self):
        """Create backup of existing deployment."""
        logger.info("💾 Creating backup of existing deployment...")
        
        if os.path.exists(self.deployment_dir):
            shutil.copytree(self.deployment_dir, self.backup_dir)
            logger.info(f"✅ Backup created: {self.backup_dir}")
        else:
            logger.info("ℹ️ No existing deployment to backup")
    
    def _prepare_deployment_directory(self):
        """Prepare deployment directory structure."""
        logger.info("📁 Preparing deployment directory...")
        
        # Create deployment directory
        os.makedirs(self.deployment_dir, exist_ok=True)
        
        # Create subdirectories
        subdirs = [
            "api",
            "frontend",
            "logs",
            "data",
            "config",
            "ml_models",
            "backups"
        ]
        
        for subdir in subdirs:
            os.makedirs(os.path.join(self.deployment_dir, subdir), exist_ok=True)
        
        logger.info("✅ Deployment directory structure created")
    
    def _copy_application_files(self):
        """Copy application files to deployment directory."""
        logger.info("📋 Copying application files...")
        
        # Copy API files
        api_files = [
            "simple_api.py",
            "rules/",
            "monitoring/",
            "ml_integration/"
        ]
        
        for file_or_dir in api_files:
            src = file_or_dir
            dst = os.path.join(self.deployment_dir, "api", os.path.basename(file_or_dir))
            
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
        
        # Copy frontend files
        frontend_files = [
            "frontend/index.html",
            "frontend/dashboard.js"
        ]
        
        for file in frontend_files:
            src = file
            dst = os.path.join(self.deployment_dir, "frontend", os.path.basename(file))
            shutil.copy2(src, dst)
        
        # Copy configuration files
        config_files = [
            "requirements.txt",
            "README.md",
            "DASHBOARD_README.md",
            "PHASE1_STATUS_REPORT.md"
        ]
        
        for file in config_files:
            if os.path.exists(file):
                src = file
                dst = os.path.join(self.deployment_dir, "config", os.path.basename(file))
                shutil.copy2(src, dst)
        
        logger.info("✅ Application files copied")
    
    def _install_dependencies(self):
        """Install production dependencies."""
        logger.info("📦 Installing production dependencies...")
        
        requirements_file = os.path.join(self.deployment_dir, "config", "requirements.txt")
        
        if os.path.exists(requirements_file):
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", "-r", requirements_file
                ], check=True, capture_output=True)
                logger.info("✅ Dependencies installed successfully")
            except subprocess.CalledProcessError as e:
                logger.error(f"❌ Failed to install dependencies: {e.stderr.decode()}")
                raise
        else:
            logger.warning("⚠️ No requirements.txt found, skipping dependency installation")
    
    def _configure_production_settings(self):
        """Configure production settings."""
        logger.info("⚙️ Configuring production settings...")
        
        # Create production configuration
        config = {
            "deployment": {
                "timestamp": datetime.now().isoformat(),
                "version": "2.0.0",
                "environment": "production"
            },
            "api": {
                "host": "0.0.0.0",
                "port": self.config["api_port"],
                "workers": 4,
                "log_level": self.config["log_level"]
            },
            "frontend": {
                "port": self.config["frontend_port"],
                "static_files": "frontend"
            },
            "database": {
                "path": self.config["database_path"],
                "backup_interval": "daily"
            },
            "monitoring": {
                "enabled": True,
                "metrics_interval": 30,
                "alerting": True
            },
            "ml": {
                "enabled": True,
                "models_dir": "ml_models",
                "prediction_cache": True
            }
        }
        
        config_file = os.path.join(self.deployment_dir, "config", "production.json")
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Create startup scripts
        self._create_startup_scripts()
        
        logger.info("✅ Production settings configured")
    
    def _create_startup_scripts(self):
        """Create startup scripts for production."""
        logger.info("📜 Creating startup scripts...")
        
        # API startup script
        api_script = f"""#!/bin/bash
# Movember AI Rules System - API Startup Script
cd {os.path.abspath(self.deployment_dir)}/api
export PYTHONPATH=$PYTHONPATH:$(pwd)
python simple_api.py --host 0.0.0.0 --port {self.config['api_port']} --workers 4
"""
        
        api_script_path = os.path.join(self.deployment_dir, "start_api.sh")
        with open(api_script_path, 'w') as f:
            f.write(api_script)
        os.chmod(api_script_path, 0o755)
        
        # Frontend startup script
        frontend_script = f"""#!/bin/bash
# Movember AI Rules System - Frontend Startup Script
cd {os.path.abspath(self.deployment_dir)}/frontend
python -m http.server {self.config['frontend_port']}
"""
        
        frontend_script_path = os.path.join(self.deployment_dir, "start_frontend.sh")
        with open(frontend_script_path, 'w') as f:
            f.write(frontend_script)
        os.chmod(frontend_script_path, 0o755)
        
        # Combined startup script
        combined_script = f"""#!/bin/bash
# Movember AI Rules System - Production Startup Script
echo "🚀 Starting Movember AI Rules System v2.0..."

# Start API
cd {os.path.abspath(self.deployment_dir)}
./start_api.sh &
API_PID=$!

# Wait for API to start
sleep 5

# Start frontend
./start_frontend.sh &
FRONTEND_PID=$!

echo "✅ Services started:"
echo "  API: http://localhost:{self.config['api_port']}"
echo "  Frontend: http://localhost:{self.config['frontend_port']}"
echo "  Dashboard: http://localhost:{self.config['frontend_port']}"
echo ""
echo "⏹️  Press Ctrl+C to stop all services"

# Wait for user to stop
trap "echo '🛑 Stopping services...'; kill $API_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait
"""
        
        combined_script_path = os.path.join(self.deployment_dir, "start_production.sh")
        with open(combined_script_path, 'w') as f:
            f.write(combined_script)
        os.chmod(combined_script_path, 0o755)
        
        logger.info("✅ Startup scripts created")
    
    def _run_tests(self):
        """Run deployment tests."""
        logger.info("🧪 Running deployment tests...")
        
        # Test API startup
        try:
            # Start API in background
            api_process = subprocess.Popen([
                sys.executable, os.path.join(self.deployment_dir, "api", "simple_api.py")
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for API to start
            time.sleep(3)
            
            # Test health endpoint
            import requests
            response = requests.get(f"http://localhost:{self.config['api_port']}/health/", timeout=5)
            
            if response.status_code == 200:
                logger.info("✅ API health check passed")
            else:
                raise Exception("API health check failed")
            
            # Stop API
            api_process.terminate()
            api_process.wait()
            
        except Exception as e:
            logger.error(f"❌ Deployment tests failed: {str(e)}")
            raise
        
        logger.info("✅ All deployment tests passed")
    
    def _start_services(self):
        """Start production services."""
        logger.info("🚀 Starting production services...")
        
        # This would typically start services using systemd, Docker, or similar
        # For this demo, we'll just create the startup script
        logger.info("✅ Production services configured for startup")
    
    def _health_checks(self):
        """Perform health checks."""
        logger.info("🏥 Performing health checks...")
        
        # Check deployment structure
        required_paths = [
            "api/simple_api.py",
            "frontend/index.html",
            "frontend/dashboard.js",
            "config/production.json",
            "start_production.sh"
        ]
        
        for path in required_paths:
            full_path = os.path.join(self.deployment_dir, path)
            if not os.path.exists(full_path):
                raise Exception(f"Health check failed: {path} not found")
        
        logger.info("✅ Health checks passed")
    
    def _final_verification(self):
        """Perform final verification."""
        logger.info("🔍 Performing final verification...")
        
        # Verify file permissions
        startup_script = os.path.join(self.deployment_dir, "start_production.sh")
        if not os.access(startup_script, os.X_OK):
            os.chmod(startup_script, 0o755)
        
        # Create deployment manifest
        manifest = {
            "deployment_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "version": "2.0.0",
            "timestamp": datetime.now().isoformat(),
            "components": {
                "api": "v2.0.0",
                "frontend": "v2.0.0",
                "ml_engine": "v2.0.0",
                "monitoring": "v2.0.0"
            },
            "features": [
                "Phase 1: Foundation Enhancement",
                "Phase 2: Advanced Intelligence",
                "ML Integration",
                "Performance Monitoring",
                "Real-time Analytics",
                "Enhanced Dashboard"
            ]
        }
        
        manifest_file = os.path.join(self.deployment_dir, "deployment_manifest.json")
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        logger.info("✅ Final verification completed")
    
    def _rollback(self):
        """Rollback to previous deployment."""
        logger.info("🔄 Rolling back deployment...")
        
        if os.path.exists(self.backup_dir):
            if os.path.exists(self.deployment_dir):
                shutil.rmtree(self.deployment_dir)
            shutil.move(self.backup_dir, self.deployment_dir)
            logger.info("✅ Rollback completed")
        else:
            logger.warning("⚠️ No backup available for rollback")
    
    def _print_deployment_summary(self):
        """Print deployment summary."""
        logger.info("📊 Deployment Summary")
        logger.info("=" * 40)
        logger.info(f"📍 Deployment Directory: {os.path.abspath(self.deployment_dir)}")
        logger.info(f"🌐 API URL: http://localhost:{self.config['api_port']}")
        logger.info(f"🎨 Dashboard URL: http://localhost:{self.config['frontend_port']}")
        logger.info(f"📁 Backup Location: {self.backup_dir}")
        logger.info("")
        logger.info("🚀 To start the system:")
        logger.info(f"   cd {self.deployment_dir}")
        logger.info("   ./start_production.sh")
        logger.info("")
        logger.info("📋 Features Deployed:")
        logger.info("   ✅ Phase 1: Foundation Enhancement")
        logger.info("   ✅ Phase 2: Advanced Intelligence")
        logger.info("   ✅ ML Integration & Predictive Analytics")
        logger.info("   ✅ Performance Monitoring & Caching")
        logger.info("   ✅ Enhanced Dashboard with Real-time Metrics")
        logger.info("   ✅ Production-ready Configuration")

def main():
    """Main deployment function."""
    deployment = ProductionDeployment()
    deployment.deploy()

if __name__ == "__main__":
    main() 